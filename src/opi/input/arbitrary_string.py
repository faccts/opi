from enum import StrEnum

__all__ = (
    "ArbitraryStringPos",
    "ArbitraryString",
)


class ArbitraryStringPos(StrEnum):
    """
    Position of `ArbitraryString`.

    Attributes:
        TOP: Place at very top of input file.
        BOTTOM: Place at very bottom of input file.
        BEFORE_COORDS: Place a bottom of input file, but before the coords block (i.e. "*xyz")
    """

    TOP = "top"
    BOTTOM = "bottom"
    BEFORE_COORDS = "before_coords"


class ArbitraryString:
    """
    Class to hold an arbitrary string that gets inserted into the input file.
    This is meant to inject extra input parameters not supported by this interface into the input.

    Attributes
    ----------
    string : str
        The string to be inserted.
    pos : ArbitraryStringPos | str
        Relative position of string within the input file.
    """

    def __init__(
        self,
        string: str,
        pos: ArbitraryStringPos | str = ArbitraryStringPos.BEFORE_COORDS,
    ) -> None:
        # // String
        self._string: str = ""
        self.string = string
        # // Pos
        if isinstance(pos, str):
            try:
                pos = ArbitraryStringPos(pos)
            except ValueError:
                raise
        self.pos: ArbitraryStringPos = pos

    @property
    def string(self) -> str:
        return self._string

    @string.setter
    def string(self, string: str) -> None:
        """
        Parameters
        ----------
        string : str
        """
        if not isinstance(string, str):
            raise TypeError(f"{self.__class__.__name__}.string: must be of type str!")
        # > Stripping trailing whitespaces
        string = string.rstrip()
        if not string:
            raise ValueError(
                f"{self.__class__.__name__}.string: must contain more than just whitespaces!"
            )
        self._string = string

    def format_orca(self) -> str:
        """
        Return the arbitrary string formatted for the ORCA input file.
        """
        return str(self.string)

    def __str__(self) -> str:
        return self.string

    def __hash__(self) -> int:
        """
        Using hash of string as has of class.
        This makes sure that two copies of the same string but different `pos` are treated identically.
        """
        return hash(self.string)

    def __eq__(self, other: object) -> bool:
        """Two ArbitraryString instances are considered equal when the string values are equal."""
        if not isinstance(other, ArbitraryString):
            return False
        return self.string == other.string
