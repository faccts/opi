from __future__ import annotations
from collections.abc import Sequence as AbstractSequence
import subprocess

from typing import IO, Callable, Sequence, Literal, TypeAlias, Final, TypeGuard, TYPE_CHECKING
import threading
from contextlib import ExitStack, contextmanager
from pathlib import Path

CaptureType = Literal[-1]
if TYPE_CHECKING:
    assert subprocess.PIPE == -1
CAPTURE: Final[CaptureType] = subprocess.PIPE


StreamDestination: TypeAlias = int | Path | str | IO[str] | Callable[[str], None]
StreamTargetSpec: TypeAlias = StreamDestination | Sequence[StreamDestination]
StreamTargets: TypeAlias = tuple[StreamDestination, ...]


class TextStreamFanout(IO[str]):
    """
    A Python-side fanout stream.

    This is not passed directly to subprocess.
    Instead, reader threads read from subprocess.PIPE and call this object's write().
    """

    def __init__(self) -> None:
        self._streams: list[IO[str]] = []
        self._callbacks: list[Callable[[str], None]] = []
        self._capture_enabled = False
        self._captured_chunks: list[str] = []
        self._lock = threading.Lock()

    @property
    def active(self) -> bool:
        return self._capture_enabled or bool(self._streams) or bool(self._callbacks)

    def add_capture(self):
        self._capture_enabled = True

    def add_stream(self, stream: IO[str]):
        self._streams.append(stream)

    def add_callback(self, callback: Callable[[str], None]):
        self._callbacks.append(callback)

    def write(self, text: str) -> int:
        with self._lock:
            if self._capture_enabled:
                self._captured_chunks.append(text)

            for stream in self._streams:
                stream.write(text)
                stream.flush()

            for callback in self._callbacks:
                callback(text)

        return len(text)

    def flush(self):
        with self._lock:
            for stream in self._streams:
                stream.flush()

    def get_captured(self) -> str:
        return "".join(self._captured_chunks)


def _is_writable_stream(value: object) -> TypeGuard[IO[str]]:
    return callable(getattr(value, "write", None))


def target_spec_to_stream_targets(targets: StreamTargetSpec) -> StreamTargets:
    """
    Normalize either:
        stdout="capture"
        stdout=Path("out.txt")
        stdout=[Path("out.txt"), "capture"]
    into a tuple of stream targets.
    """
    if targets == ():
        return ()

    # Important: "capture" is itself a str, and str is a Sequence[str],
    # so we must handle it before the generic Sequence case.
    if targets == subprocess.PIPE:
        return (CAPTURE,)

    if isinstance(targets, int):
        raise TypeError("Only 'subprocess.PIPE' is allowed as 'int' input")

    # convert str filename to Path
    if isinstance(targets, str):
        targets = Path(targets)

    if isinstance(targets, Path) or callable(targets) or _is_writable_stream(targets):
        return (targets,)

    if isinstance(targets, AbstractSequence):
        normalized: list[StreamDestination] = []
        for index, target in enumerate(targets):
            try:
                normalized.extend(target_spec_to_stream_targets(target))  # type: ignore[arg-type]
            except TypeError as exc:
                raise TypeError(f"Unsupported stream target at index {index}: {target!r}") from exc
        return tuple(normalized)

    raise TypeError(f"Unsupported stream target: {targets!r}")


def concatentate_stream_targets(*targets: StreamTargetSpec) -> StreamTargets:
    return sum(map(target_spec_to_stream_targets, targets), start=())


@contextmanager
def open_text_stream_fanout(targets: StreamTargetSpec):
    normalized = target_spec_to_stream_targets(targets)

    with ExitStack() as stack:
        multi = TextStreamFanout()

        for target in normalized:
            if target == subprocess.PIPE:
                multi.add_capture()

            elif isinstance(target, Path):
                file = stack.enter_context(target.open("w", encoding="utf-8"))
                multi.add_stream(file)

            elif callable(target):
                multi.add_callback(target)

            elif hasattr(target, "write"):
                multi.add_stream(target)  # type: ignore[arg-type]

            else:
                raise TypeError(f"Unsupported stream target: {target!r}")

        yield multi


def pump_text_stream(
    stream: IO[str],
    target: TextStreamFanout,
    errors: list[BaseException],
) -> None:
    try:
        for line in stream:
            target.write(line)
    except BaseException as exc:
        errors.append(exc)
    finally:
        try:
            stream.close()
        except Exception:
            pass
