from typing import Any, Iterator, TextIO


class TrackingTextIO:
    """Class that keeps track of the line number in TextIO"""

    def __init__(self, stream: TextIO) -> None:
        self._stream: TextIO = stream
        self.line_number: int = 0

    def readline(self, *args: Any, **kwargs: Any) -> str:
        line = self._stream.readline(*args, **kwargs)
        if line:
            self.line_number += 1
        return line

    def readlines(self, *args: Any, **kwargs: Any) -> list[str]:
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

    def __iter__(self) -> Iterator[str]:
        for line in self._stream:
            self.line_number += 1
            yield line

    def __getattr__(self, name: str) -> Any:
        # Tell mypy that this forwards to the underlying TextIO
        return getattr(self._stream, name)

    def __next__(self) -> Any:
        line = self.file.readline()
        if line == "":
            raise StopIteration
        self.line_number += 1
        return line
