import types
from io import StringIO
from typing import Any, Optional, TextIO, Type


class TrackingTextIO:
    """Class that keeps track of the line number in TextIO"""

    def __init__(self, stream: str | TextIO) -> None:
        # > declare self._stream for mypy
        self._stream: TextIO
        if isinstance(stream, str):
            self._stream = StringIO(stream)
        else:
            self._stream = stream
        self.line_number: int = 0

    def __enter__(self) -> "TrackingTextIO":
        return self

    def __exit__(
        self,
        _exc_type: Optional[Type[BaseException]],
        _exc_value: Optional[BaseException],
        _traceback: Optional[types.TracebackType],
    ) -> bool | None:
        self._stream.close()
        return None

    def __iter__(self) -> "TrackingTextIO":
        return self

    def __getattr__(self, name: str) -> Any:
        # Tell mypy that this forwards to the underlying TextIO
        return getattr(self._stream, name)

    def __next__(self) -> str:
        line = self._stream.readline()
        if not line:
            raise StopIteration
        self.line_number += 1
        return line

    def readline(self, *args: Any, **kwargs: Any) -> str:
        line = self._stream.readline(*args, **kwargs)
        if line:
            self.line_number += 1
        return line

    def readlines(self, *args: Any, **kwargs: Any) -> list[str]:
        """Reads all lines from the stream and returns them as a list"""
        lines = self._stream.readlines(*args, **kwargs)
        self.line_number += len(lines)
        return lines

    def seek(self, offset: int, whence: int = 0) -> int:
        """Seek to a new position and recompute line_number accordingly."""
        pos = self._stream.seek(offset, whence)

        # Recompute line number from start of file up to current position
        current_pos = self._stream.tell()
        self._stream.seek(0)
        content_up_to_pos = self._stream.read(current_pos)
        self.line_number = content_up_to_pos.count("\n")
        self._stream.seek(current_pos)

        return pos
