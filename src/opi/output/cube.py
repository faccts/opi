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

        Returns
        ----------
        str
            Returns a string with the cube data.

        Raises
        ----------
        FileNotFoundError
            If the cube file does not exist.
        """
        return self._path.read_text()

    def __iter__(self) -> Iterator[str]:
        """
        Lazily yields lines from the cube file (memory efficient).

        Returns
        ----------
        Iterator[str]
            Iterator that yields the cube data line by line.

        Raises
        ----------
        FileNotFoundError
            If the cube file does not exist.
        """
        return iter(self._path.open())

    def __str__(self) -> str:
        """Returns the name of the class and the path the object holds"""
        return f"{self.__class__.__name__}({self.path})"
