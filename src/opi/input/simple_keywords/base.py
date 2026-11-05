__all__ = ("ORCAKeyword", "SimpleKeywordBox")


class SimpleKeywordBox:
    """
    Base class for groups of related ``ORCAKeyword`` constants.

    Each concrete subclass (e.g. ``Task``, ``Dft``, ``BasisSet``) declares its
    members as class-level ``ORCAKeyword`` attributes.
    """

    @classmethod
    def from_string(cls, s: str) -> "ORCAKeyword":
        """
        Look up an ``ORCAKeyword`` by string across all attributes.

        Matching is case-insensitive and checks the keyword value, the
        attribute name, and the optional alias — in that order. A match on the
        keyword value or attribute name is returned immediately; an alias is
        only accepted if it resolves to exactly one keyword.

        Parameters
        ----------
        s : str
            String used to create ORCAKeyword object

        Returns
        -------
        ORCAKeyword
            Simple keyword from string

        Raises
        ------
        ValueError
            If no matching keyword is found in the registry, or if an alias
            matches more than one keyword.
        """
        norm = s.lower()
        # Keywords matched through an alias; resolved after the loop since aliases may be shared
        alias_matches: dict[str, ORCAKeyword] = {}

        # Here the function will loop over all attributes both existing and inherited by the current class.
        # The simple keywords are structured such that, for example, the larger `Scf` grouping is a child class of the semantically smaller groupings,
        # such as `ScfConvergence`, `ScfThreshold` and so on. From these attributes the simple keyword are selected and checked as to
        # whether they match the input string.
        for attr_name in dir(cls):
            # Get the value associated with attribute
            candidate_attr = getattr(cls, attr_name)
            if attr_name.startswith("_") or not isinstance(
                candidate_attr, ORCAKeyword
            ):  # Skip private/magic attributes or non-Simple Keyword attributes
                continue
            # Case 1: if the user searches for keyword through how it would appear in ORCA input
            if candidate_attr.keyword.lower() == norm:
                return candidate_attr
            # Case 2: if the user searches for keyword through how it is stored in OPI
            if attr_name.lower() == norm:
                return candidate_attr
            # Case 3: if the user searches for keyword through a known alias
            if candidate_attr.alias and any(a.lower() == norm for a in candidate_attr.alias):
                alias_matches[attr_name] = candidate_attr

        # An alias may be shared between groups (e.g. "tight" for `Scf` and `Opt`), so only
        # accept it if it points to a single keyword
        if len(set(alias_matches.values())) == 1:
            return next(iter(alias_matches.values()))
        if alias_matches:
            raise ValueError(
                f"Keyword {s} is ambiguous in class {cls.__name__}, it matches: {list(alias_matches)}"
            )

        # In the case that no matches are found, raise ValueError
        raise ValueError(f"Keyword {s} not found in class {cls.__name__}")

    @classmethod
    def find_keyword(cls, inp: "ORCAKeyword | str") -> "ORCAKeyword":
        """
        Resolve a string or ``ORCAKeyword`` to a valid ``ORCAKeyword``.

        Accepts a bare string or an existing ``ORCAKeyword`` (whose ``.keyword``
        string is used for the lookup).

        Parameters
        ----------
        inp : ORCAKeyword | str
            Input that is resolved into ORCAKeyword.

        Returns
        -------
        ORCAKeyword
            Found simple keyword

        Raises
        ------
        ValueError
            If ``inp`` is not a str or ORCAKeyword, or if the string is not
            found.
        """
        # If input is ORCAKeyword, convert to string representation
        if isinstance(inp, ORCAKeyword):
            inp = inp.keyword

        if not isinstance(inp, str):
            raise ValueError(
                f"{cls.__name__} expects a str or ORCAKeyword, got {type(inp).__name__}: {inp!r}"
            )

        return cls.from_string(inp)

    @classmethod
    def validate_keyword(cls, inp: "ORCAKeyword | str") -> "ORCAKeyword":
        """
        Validate that a string or ``ORCAKeyword`` belongs to this keyword group.

        Behaves like ``find_keyword()``: the input is resolved within this class,
        including inherited groups (e.g. ``Scf`` contains ``ScfThreshold``), and the
        matching keyword is returned.

        Parameters
        ----------
        inp : ORCAKeyword | str
            Keyword or string to validate.

        Returns
        -------
        ORCAKeyword
            The matching keyword of this class.

        Raises
        ------
        ValueError
            If ``inp`` is not a str or ORCAKeyword, if it is not found in this
            class, or if it only matches an alias shared by several keywords.
        """
        return cls.find_keyword(inp)


class ORCAKeyword:
    """
    A single ORCA simple keyword (e.g. ``SP``, ``PBE``, ``def2-SVP``).

    Instances are used as typed constants inside ``SimpleKeywordBox`` subclasses
    and can also be constructed directly from a raw string for ad-hoc keywords.

    Two simple keywords compare equal if their keywords match case-insensitively, since
    `format_orca()` lowercases the keyword and ORCA itself ignores the case. Hence, keywords
    that only differ in case are duplicates of each other.

    Attributes
    ----------
    keyword : str
        The keyword string as it will appear in the ORCA ``.inp`` file.
    alias : list[str] | None
        Optional alternative name(s) accepted by ``SimpleKeywordBox.from_string``.
    """

    _keyword: str
    alias: list[str] | None = None

    def __init__(self, keyword: str, alias: str | list[str] | None = None) -> None:
        """
        Parameters
        ----------
        keyword : str
            Keyword string for the ORCA input line. Leading/trailing whitespace
            is stripped; an empty string raises ``ValueError``.
        alias : str | list[str], optional
            Alternative lookup name for ``SimpleKeywordBox.from_string``.
        """
        self.keyword = keyword
        self.alias = [alias] if isinstance(alias, str) else alias

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
        return self.keyword.lower().__hash__()

    def __str__(self) -> str:
        return self.format_orca()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ORCAKeyword):
            return False
        return self.keyword.lower() == other.keyword.lower()
