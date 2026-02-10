__all__ = ("SimpleKeyword",)


class SimpleKeywordBox:
    pass


class SimpleKeyword:
    """
    Class to represent simple keywords used in ORCA input files
    Simple keywords are keywords that have a public name and a keyword
    The public name is the name of the keyword that is used in the input file
    The keyword is the name of the keyword that is used in the ORCA input file

    Attributes
    ----------
    keyword: str
        simple keyword as it will appear in the ORCA .inp file
    """

    def __init__(self, keyword: str) -> None:
        self._keyword: str = ""
        self.keyword = keyword
        self._name: str = ""
        # self.name = name

    @property
    def keyword(self) -> str:
        return self._keyword

    @keyword.setter
    def keyword(self, value: str) -> None:
        """
        Parameters
        ----------
        value : str
        """
        if not isinstance(value, str):
            raise TypeError(f"{self.__class__.__name__}.keyword: must of type str!")
        # > Stripping trailing whitespaces
        value = value.rstrip()
        if not value:
            raise ValueError(
                f"{self.__class__.__name__}.keyword: must contain more than just whitespaces!"
            )
        self._keyword = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Parameters
        ----------
        value : str
        """
        if not isinstance(value, str):
            raise TypeError(f"{self.__class__.__name__}.name: must be of type str!")
        # > Stripping trailing whitespaces
        value = value.rstrip()
        if not value:
            raise ValueError(
                f"{self.__class__.__name__}.name: must contain more than just whitespaces!"
            )
        self._name = value

    def format_orca(self) -> str:
        """
        Function to format simple keyword for ORCA input file

        Returns
        -------
        str
            Formatted string for ORCA input file
        """
        return self.keyword.lower()

    def __hash__(self) -> int:
        return self.keyword.__hash__()

    def __str__(self) -> str:
        return self.format_orca()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SimpleKeyword):
            return False
        return self.keyword == other.keyword
