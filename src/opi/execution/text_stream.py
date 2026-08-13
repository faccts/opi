from __future__ import annotations

import subprocess
import threading
from collections.abc import Sequence as AbstractSequence
from contextlib import ExitStack, contextmanager
from pathlib import Path
from typing import (
    IO,
    Callable,
    Final,
    Iterator,
    Sequence,
    TypeAlias,
    TypeGuard,
)

CaptureType = int  # > -1 is the sentinel value used by subprocess
CAPTURE: Final[CaptureType] = subprocess.PIPE


StreamDestination: TypeAlias = int | Path | str | IO[str] | Callable[[str], None]
StreamTargetSpec: TypeAlias = StreamDestination | Sequence[StreamDestination]
StreamTargets: TypeAlias = tuple[StreamDestination, ...]


class TextStreamFanout:
    """
    The TextStreamFannout class is a Python-side fanout dispatch helper
    for writing to multiple StreamTargets when running commands using
    subprocess.POpen. TextStreamFannout is not passed into subprocess.POpen
    directly, instead TextStreamFannout receives data from subprocess.PIPE
    then redirects to the stream targets.

    Attributes
    ----------
    _streams: list[IO[str]]
        Text streams such as file handles that implements the IO interface.
    _callbacks: list[Callable[[str], None]]
        List of callbacks to send lines of the subprocess output.
    _capture_enabled: bool
        Boolean flag to determine whether to capture the output of the subprocess
        into _captured_chunks. The captured output can then be returned to the user.
    _lock: threading.Lock:
        Allow thread-safe writing to target streams
    """

    def __init__(self) -> None:
        self._streams: list[IO[str]] = []
        self._callbacks: list[Callable[[str], None]] = []
        self._capture_enabled = False
        self._captured_chunks: list[str] = []
        self._lock = threading.Lock()

    @property
    def active(self) -> bool:
        """Determine whether the fanout has any targets that need to be captured."""
        return self._capture_enabled or bool(self._streams) or bool(self._callbacks)

    def add_capture(self) -> None:
        """Capture output text which can be accessed through `get_captured()`."""
        self._capture_enabled = True

    def add_stream(self, stream: IO[str]) -> None:
        """Append IO stream to the list of streams."""
        self._streams.append(stream)

    def add_callback(self, callback: Callable[[str], None]) -> None:
        """Append line callback to the list of callbacks."""
        self._callbacks.append(callback)

    def write(self, text: str) -> int:
        """Writes text to all target streams.

        Parameters
        ----------
        text: str
            Text chunk to send to all target streams.

        Returns
        -------
        int
            Length of text sent to all streams.
        """
        with self._lock:
            if self._capture_enabled:
                self._captured_chunks.append(text)

            for stream in self._streams:
                stream.write(text)
                stream.flush()

            for callback in self._callbacks:
                callback(text)

        return len(text)

    def flush(self) -> None:
        """Flush all streams."""
        with self._lock:
            for stream in self._streams:
                stream.flush()

    def get_captured(self) -> str:
        """Concatenate captured text into single str output."""
        return "".join(self._captured_chunks)


def _is_writable_stream(value: object) -> TypeGuard[IO[str]]:
    """
    Determines whether `value` is a writable stream.

    To be considered a writable stream, the object must have a
    callable write method.

    Parameters
    ----------
    value: object
        Object to be tested

    Returns
    -------
    TypeGuard[IO[str]]
        True if the object is determined to be a writable stream.

    Notes
    -----
    Implementation can be improved to check whether the object adheres
    to the full IO spec. Currently any object with a write method is
    considered to be a writable stream.
    """
    return callable(getattr(value, "write", None))


def target_spec_to_stream_targets(targets: StreamTargetSpec) -> StreamTargets:
    """
    Normalizes `TargetDestination` and `Sequence[TargetDesination]` into a
    `tuple[TargetDestination, ...]` to be used by the `TextStreamFanout` class.

    Parameters
    ----------
    targets : StreamTargetSpec
        Single or multiple target streams.

    Returns
    -------
    StreamTargets
        Tuple of target streams.

    Raises
    ------
    TypeError
        Raised if the type of `targets` is not a supported stream target.
    """
    if targets == ():
        return ()

    # > Capture output is denoted by subprocess.PIPE (matches subprocess.run semantics)
    if targets == subprocess.PIPE:
        return (CAPTURE,)

    # > Any other `int` value is not supported
    if isinstance(targets, int):
        raise TypeError("Only 'subprocess.PIPE' is allowed as 'int' input")

    # > normalize string filename to `Path`
    if isinstance(targets, str):
        targets = Path(targets)

    # > Any single file path, callable or writable stream gets normalized to a single tuple
    if isinstance(targets, Path) or callable(targets) or _is_writable_stream(targets):
        return (targets,)

    # > Iterate over the sequence flattening all results into a single tuple.
    if isinstance(targets, AbstractSequence):
        normalized: list[StreamDestination] = []
        for index, target in enumerate(targets):
            try:
                normalized.extend(target_spec_to_stream_targets(target))
            except TypeError as exc:
                raise TypeError(f"Unsupported stream target at index {index}: {target!r}") from exc
        return tuple(normalized)

    # > Any other types are unsupported.
    raise TypeError(f"Unsupported stream target: {targets!r}")


def concatentate_stream_targets(*targets: StreamTargetSpec) -> StreamTargets:
    """Concatenates multiple stream targets into a single tuple."""
    return sum(map(target_spec_to_stream_targets, targets), start=())


@contextmanager
def open_text_stream_fanout(targets: StreamTargetSpec) -> Iterator[TextStreamFanout]:
    """
    Context manager that creates an instance of `TextStreamFanout` which can be
    used to pipe the output from a subprocess to multiple target streams. Closes all
    open streams on exit.

    Parameters
    ----------
    targets : StreamTargetSpec
        Single or multiple stream targets to use in the fanout.

    Yields
    ------
    TextStreamFanout
        Fanout object that dispatches all values passed into the `write` method
        to the target streams.

    Raises
    ------
    TypeError
        Raised if an unsupported stream target is encountered.
    """
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
            elif _is_writable_stream(target):
                multi.add_stream(target)

            else:
                raise TypeError(f"Unsupported stream target: {target!r}")

        yield multi


def pump_text_stream(
    stream: IO[str],
    target: TextStreamFanout,
    errors: list[Exception],
) -> None:
    """
    Pumps the output from `stream` to the `target` fanout.

    Intended to be used to listen to a subprocess's stdout or
    stderr stream then iterates over every line sending it to the
    target fanout. Any errors that occur during this process are
    accumulated in the `errors` list.

    Parameters
    ----------
    stream : IO[str]
        Input stream from a subprocess's stdout or stderr.
    target : TextStreamFanout
        Target fanout to dispatch lines from the input stream.
    errors : list[Exception]
        Error accumulation list, any errors that occur on write are
        captured and appended to the list.
    """
    try:
        for line in stream:
            target.write(line)
    except Exception as exc:
        # > Exceptions are raised as part of an ExceptionGroup
        # > at the end of `run_subprocess_with_fanout()`
        errors.append(exc)
    finally:
        try:
            stream.close()
        except Exception:
            pass
