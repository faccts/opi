from pathlib import Path
from typing import Iterator


class CubeOutput:
    """
    Class that stores the path to a cube file and provides easy access to the cube
    data via the cube property. Reads the cube file upon access to cube property.
    """

    def __init__(self, path: Path):
        if path.is_file():
            self._path = path
        else:
            raise FileNotFoundError(f"{path} is not a valid file.")

    @property
    def path(self) -> Path:
        """Read only access to the path."""
        return self._path

    @property
    def cube(self) -> str:
        """
        Reads the cube data from file at stored path and returns it as string.

        Raises
        ----------
        FileNotFoundError
            If the cube file does not exist.
        """
        return self._path.read_text()

    def iter_cube(self) -> Iterator[str]:
        """
        Lazily yields lines from the cube file (memory efficient).
        """
        with self._path.open("r") as f:
            for line in f:
                yield line

    def __iter__(self) -> Iterator[str]:
        return self.iter_cube()

    def __str__(self) -> str:
        """Returns the name of the class and the path the object holds"""
        return f"{self.__class__.__name__}({self.path})"
