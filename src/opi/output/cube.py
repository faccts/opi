from pathlib import Path


class CubeOutput:
    """
    Class that stores the path to a cube file and provides easy access to the cube
    data via the cube property.
    """

    def __init__(self, path: Path):
        if path.is_file():
            self._path = path
        else:
            raise FileNotFoundError(f"{path} is not a valid file.")

    @property
    def path(self) -> Path:
        """Returns the path to the cube file."""
        return self._path

    @property
    def cube(self) -> str:
        """
        Reads the cube data from file and returns it as string.

        Raises
        ----------
        FileNotFoundError
            If the cube file does not exist anymore.
        """
        return self._path.read_text()

    def __str__(self) -> str:
        return self.cube
