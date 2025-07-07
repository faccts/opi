"""
Module that holds the main class for input handling.
"""

import os
from pathlib import Path

from opi.input.arbitrary_string import (
    ArbitraryString,
    ArbitraryStringPos,
)
from opi.input.blocks.base import Block
from opi.input.simple_keywords.base import SimpleKeyword

__all__ = ("Input",)


class Input:
    """
    The main input class that manages the simple keywords and blocks options of the ORCA input.

    Attributes
    ----------
    _simple_keywords | simple_keywords: list[SimpleKeyword]
        List of simple keywords to be put into the ORCA input.
        Access to this attribute should be done through the respective `add_simple_keywords/remove_.../clear_...` methods.
    _blocks | blocks: dict[type[Block], Block]
        Dict of blocks to be put into the ORCA input.
        Access to this attribute should be done through the respective `add_blocks/remove_.../clear_...` methods.
    _arbitrary_strings | arbitrary_strings: list[ArbitraryString]
        List of arbitrary string to be put into the ORCA input.
        Access to this attribute should be done through the respective `add_arbitrary_string/remove_.../clear_...` methods.
    _ncores | ncores: int | None
        Number of cores to used.
    _memory | memory: int | None
        Memory per CPU core in MiB.
    _moinp | moinp: Path | None
        `%moinp` file to be used.
    """

    def __init__(self) -> None:
        # ---------------------------------
        # > MEMBER VARIABLES
        # ---------------------------------
        # // Simple Keywords
        self._simple_keywords: list[SimpleKeyword] = []
        # // Block options
        self._blocks: dict[type[Block], Block] = {}
        # // Arbitrary strings
        self._arbitrary_strings: list[ArbitraryString] = []

        # ---------------------------------
        # > Special input variables
        # ---------------------------------
        # // Number of CPU cores
        self._ncores: int | None = None
        # // Memory per core
        self._memory: int | None = None
        # // '%moinp'
        self._moinp: Path | None = None

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # > PROPERTIES
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    @property
    def simple_keywords(self) -> "list[SimpleKeyword] | None":
        return self._simple_keywords

    @simple_keywords.setter
    def simple_keywords(self, value: list[SimpleKeyword] | None) -> None:
        """
        Parameters
        ----------
        value : list[SimpleKeyword] | None
        """
        raise AttributeError(
            "simple_keywords is private, use the add_simple_keywords/get_simple_keywords function for access."
        )

    @property
    def blocks(self) -> dict[type[Block], Block] | None:
        return self._blocks

    @blocks.setter
    def blocks(self, value: dict[type[Block], Block] | None) -> None:
        """
        Parameters
        ----------
        value : dict[type[Block] | Block] | None
        """
        raise AttributeError(
            "blocks is private, use the add_blocks/get_blocks function for access."
        )

    @property
    def arbitrary_strings(self) -> "list[ArbitraryString] | None":
        return self._arbitrary_strings

    @arbitrary_strings.setter
    def arbitrary_strings(self, value: list[ArbitraryString] | None) -> None:
        """
        Parameters
        ----------
        value : list[ArbitraryString] | None
        """
        raise AttributeError(
            "arbitrary_strings is private, use the add_arbitrary_strings/get_arbitrary_strings function for access."
        )

    @property
    def ncores(self) -> int | None:
        return self._ncores

    @ncores.setter
    def ncores(self, value: int | None) -> None:
        """
        Parameters
        ----------
        value : int | None
        """
        if value is not None and value < 0:
            raise ValueError(f"{self.__class__.__name__}.ncores must be a positive integer.")
        # << END OF IF
        self._ncores = value

    @property
    def memory(self) -> int | None:
        return self._memory

    @memory.setter
    def memory(self, value: int | None) -> None:
        """
        Parameters
        ----------
        value : int | None
        """
        if value is not None and value < 0:
            raise ValueError(f"{self.__class__.__name__}.memory must be a positive integer.")
        # << END OF IF
        self._memory = value

    @property
    def moinp(self) -> Path | None:
        return self._moinp

    @moinp.setter
    def moinp(self, value: Path | str | os.PathLike[str] | None) -> None:
        """
        Parameters
        ----------
        value : Path | str | os.PathLike[str] | None
        """
        if value is not None:
            try:
                value = Path(value).resolve()
            except Exception as err:
                raise ValueError(f"{self.__class__.__name__}.moinp: Invalid path.") from err
            else:
                if not value.is_file():
                    raise FileNotFoundError(
                        f"{self.__class__.__name__}.moinp: File does not exist: {value}"
                    )
        # << END OF IF
        self._moinp = value

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # > METHODS
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    # ----------------------------------------------------------------------
    # > SIMPLE KEYWORDS
    # ----------------------------------------------------------------------
    def add_simple_keywords(
        self,
        *keywords: str | SimpleKeyword,
        strict: bool = False,
    ) -> None:
        """
        Add one or more simple keywords to the Calculator.

        The keywords are stored in the class attribute `_simple_keywords`.

        Parameters
        ----------
        *keywords : str | SimpleKeyword
            One or more simple keywords to add.
        strict : bool, default: False
            If True, a ValueError is raised if any keyword has already been added.
            If False (default), adding existing keywords is ignored.

        Raises
        ------
        ValueError
            If `strict` is True and a keyword has already been added.

        Example
        --------
        ::

         >>c = Calculator(basename = input)
         >>c.input.add_simple_keywords([Dft.TPSS, BasisSets.DEF2_TZVP])

        This adds method TPSS and basis set def2-TZVP to Calculator._simple_keywords
        """

        for keyword in keywords:
            # > Convert string to simple keyword.
            if isinstance(keyword, str):
                simple_keyword = SimpleKeyword(keyword)
            else:
                simple_keyword = keyword

            # > Add simple keyword to calculator.
            if simple_keyword not in self._simple_keywords:
                self._simple_keywords.append(simple_keyword)
            elif strict:
                raise ValueError(f"Strict: Simple Keyword {simple_keyword} has already been added")

    def remove_simple_keywords(
        self,
        *keywords: str | SimpleKeyword,
        strict: bool = False,
    ) -> None:
        """
        Remove one or more simple keywords from the Calculator.

        Parameters
        ----------
        *keywords : str | SimpleKeyword
            One or more simple keywords to remove.
        strict : bool, default: False
            If True, a ValueError is raised if any of the specified keywords is not present.
            If False, ignore keywords that are not present

        Raises
        ------
        ValueError
            If `strict` is True and keyword is not found
        """
        if not self._simple_keywords:
            if strict:
                raise ValueError(
                    "Strict: No simple keywords have been added. So no keyword can be removed"
                )
            else:
                return

        for keyword in keywords:
            # > Convert string to simple keyword.
            if isinstance(keyword, str):
                simple_keyword = SimpleKeyword(keyword.lower())
            else:
                simple_keyword = keyword

            # > Remove simple keyword if present.
            if simple_keyword in self._simple_keywords:
                self._simple_keywords.remove(simple_keyword)
            elif strict:
                raise ValueError(
                    f"Strict: No simple keyword {simple_keyword} has been added. So it cannot be removed."
                )

    def _has_simple_keyword(self, keyword: str | SimpleKeyword, /) -> bool:
        """
        Check if a keyword has been added to the Calculator

        Parameters
        ----------
        keyword : str | SimpleKeyword
            The simple keyword to check

        Returns
        -------
        bool
            True if the simple keyword is present in Calculator, False otherwise.
        """
        if not self._simple_keywords:
            return False
        if isinstance(keyword, str):
            return SimpleKeyword(keyword.lower()) in self._simple_keywords
        else:
            return keyword in self._simple_keywords

    def has_simple_keywords(self, *keywords: str | SimpleKeyword) -> tuple[bool, ...]:
        """
        Check if one or more simple keywords have been added to the Calculator.

        Parameters
        ----------
        *keywords : str or SimpleKeyword
            One or more simple keywords to check.

        Returns
        -------
        tuple[bool, ....]
            A tuple of booleans, where each element is True if the corresponding keyword is present
            in the Calculator, and False otherwise.
        """
        return tuple(self._has_simple_keyword(keyword) for keyword in keywords)

    def _get_simple_keyword(
        self, keyword: str | SimpleKeyword, /, *, create_missing: bool = False
    ) -> SimpleKeyword | None:
        """
        Retrieve a simple keyword that has been added to the Calculator.

        Parameters
        ----------
        keyword : str | SimpleKeyword
            the simple keyword to retrieve
        create_missing : bool, default = False
            if True, the keyword will be generated if it is missing, and it is requested,
            if False, return None if the keyword is missing

        Returns
        -------
        SimpleKeyword | None
            If the simple keyword exists, or it was created, it is returned, else None is returned.
        """
        if isinstance(keyword, str):
            simple_keyword: SimpleKeyword = SimpleKeyword(keyword.lower())
        else:
            simple_keyword = keyword

        if self._simple_keywords:
            if simple_keyword in self._simple_keywords:
                for calculator_keyword in self._simple_keywords:
                    if simple_keyword == calculator_keyword:
                        return calculator_keyword
            elif create_missing:
                self.add_simple_keywords(simple_keyword)
                return simple_keyword
            return None
        elif create_missing:
            self.add_simple_keywords(simple_keyword)
            return simple_keyword
        else:
            return None

    def get_simple_keywords(
        self,
        *keywords: str | SimpleKeyword,
        create_missing: bool = False,
    ) -> list[SimpleKeyword]:
        """
        Retrieve one or more simple keyword that have been added to the Calculator.

        Parameters
        ----------
        keywords : str | SimpleKeyword
            One or more simple keywords to retrieve.
        create_missing : bool, default = False
            If True, keywords will be generated if they are missing, and they are requested.
            If False, missing keywords will not be generated if they are missing.

        Returns
        -------
        List[SimpleKeyword]
            A list of all requested simple keywords if they exist, or if they were created.
            Empty list if all keywords are missing and `create_missing` is False.
        """
        keywords_to_return: list[SimpleKeyword] = []
        for keyword in keywords:
            keyword_to_return = self._get_simple_keyword(keyword, create_missing=create_missing)
            # > check if keyword was found/created
            if keyword_to_return:
                keywords_to_return.append(keyword_to_return)

        return keywords_to_return

    def clear_simple_keywords(self, *, strict: bool = False) -> None:
        """
        Function to remove all simple keywords from Calculator._simple_keywords by setting it to None

        Parameters
        ----------
        strict : bool, default: False
            If True, raise a ValueError if there are no simple keywords to remove.
            If False (default), does nothing since there are no simple keywords to remove.

        Raises
        -------
        ValueError
            If `strict` is True and no simple keywords are present.
        """
        if not self._simple_keywords:
            if strict:
                raise ValueError(
                    "Strict: No simple keywords have been added, so none can be cleared."
                )
            else:
                return

        self._simple_keywords.clear()

    # ----------------------------------------------------------------------
    # > BLOCKS
    # ----------------------------------------------------------------------
    def add_blocks(
        self,
        *blocks: Block,
        strict: bool = False,
        overwrite: bool = False,
    ) -> None:
        """
        Add one or more blocks to the Calculator's `blocks` attribute.

        Parameters
        ----------
        *blocks : Block
            One or more blocks to add
        strict : bool, default: False
            If True, raise a ValueError if a block has already been added.
            If False (default), does nothing if a block has already been added.
        overwrite : bool, default: False
            If True, blocks that are already present will be overwritten (strict is ignored)
            If False (default), existing blocks are not overwritten

        Example
        -------
        ::

         >>c = Calculator(basename = input)
         >>b = Block(d3s6=0.64,d3a1=0.3065)
         >>c.input.add_blocks(b)

        Variables without assigned value will be assigned default value (usually None)
        """
        for block in blocks:
            if type(block) not in self._blocks:
                self._blocks[type(block)] = block
            elif overwrite:
                self._blocks[type(block)] = block
            elif strict:
                raise ValueError(f"Strict: Block for {block.name} has already been added")

    def remove_blocks(self, *blocks: Block, strict: bool = False) -> None:
        """
        Remove one or more blocks from the Calculator's `blocks` attribute.

        Parameters
        ----------
        *blocks : Block
            One or more blocks to remove.
        strict : bool, default: False
            If True, raise a ValueError if block was not found in the Calculator.
            If False (default), silently ignore blocks that are not present.

        Raises
        -------
        ValueError
            If `strict` is True and one or more of the specified blocks are not present.
        """
        if not self._blocks:
            if strict:
                raise ValueError("Strict: No blocks have been added")
            else:
                return

        for block in blocks:
            t_block = type(block)
            if t_block in self._blocks:
                self._blocks.pop(t_block)
            elif strict:
                raise ValueError(
                    f"Strict: Block '{block.name}' does not exist so it cannot be removed."
                )

    def _has_block(self, block: Block | type[Block], /) -> bool:
        """
        Check whether a block has been added to the Calculator.

        Parameters
        ----------
        block : Block | type[Block]
            The block or block type to check

        Returns
        -------
        bool
            True if the block is present in the Calculator, False otherwise.
        """
        if not self._blocks:
            return False

        if isinstance(block, Block):
            block_type = type(block)
        else:
            block_type = block

        if self._blocks:
            return block_type in self._blocks
        else:
            return False

    def has_blocks(self, *blocks: Block) -> tuple[bool, ...]:
        """
        Check whether one or more blocks have been added to the Calculator.

        Parameters
        ----------
        *blocks : Block
            One or more blocks to check.

        Returns
        -------
        tuple[bool, ...]
            A tuple of bools which are True if the block are present in the Calculator, False otherwise.
        """
        return tuple(self._has_block(block) for block in blocks)

    def _get_block(self, block: type[Block], /, *, create_missing: bool = False) -> Block | None:
        """
        Retrieve a block that has been added to the Calculator.

        Parameters
        ----------
        block : type[Block]
            The block to retrieve
        create_missing : bool, default: False
            If True and the block is missing, add it and return it.
            If False (default), return None if the block is missing.

        Returns
        -------
        Block | None
            The requested block if it exists, or if it was created.
            None if the block is missing and `create_missing` is False.
        """
        if self._blocks:
            if block in self._blocks:
                return self._blocks[block]
            elif create_missing:
                created_block = block()
                self.add_blocks(created_block)
                return created_block
            else:
                return None
        elif create_missing:
            created_block = block()
            self.add_blocks(created_block)
            return created_block
        else:
            return None

    def get_blocks(
        self, *blocks: type[Block], create_missing: bool = False
    ) -> dict[type[Block], Block]:
        """
        Retrieve one or more blocks that have been added to the Calculator.

        Parameters
        ----------
        *blocks : type[Block]
            One or more block to retrieve.
        create_missing : bool, default: False
            If True and a block is missing, add it and return it.
            If False (default), missing blocks will be skipped.

        Returns
        -------
        dict[type[Block], Block]
            A Dictionary with the requested Blocks if they existed or were generated.
        """
        blocks_to_return = {}
        for block in blocks:
            block_to_return = self._get_block(block, create_missing=create_missing)
            # > check if block was found/created
            if block_to_return:
                blocks_to_return[block] = block_to_return
        return blocks_to_return

    def clear_blocks(self, *, strict: bool = False) -> None:
        """
        Remove all blocks that have been added to the Calculator by setting _blocks to None.

        Parameters
        ----------
        strict : bool, default: False
            If True, raise a ValueError if there are no blocks to remove.
            If False (default), does nothing since there are no blocks to remove.

        Raises
        -------
        ValueError
            If `strict` is True and no blocks are present.
        """
        if not self._blocks:
            if strict:
                raise ValueError("Strict: No blocks have been added so none can be cleared.")
            else:
                return

        self._blocks.clear()

    # ----------------------------------------------------------------------
    # > ARBITRARY STRINGS
    # ----------------------------------------------------------------------
    def add_arbitrary_string(
        self, string: str, /, *, pos: ArbitraryStringPos | str | None = None
    ) -> None:
        """
        Add an arbitrary string.

        Parameters
        ----------
        string : str
            Arbitrary string to be added
        pos : ArbitraryStringPos | str | None, default: None
            Coordinates of the arbitrary string within the input file.
            For details look into the `ArbitraryStringPos` class.
        """

        arb_string = ArbitraryString(string=string)
        if pos is not None:
            arb_string.pos = ArbitraryStringPos(pos)
        self._arbitrary_strings.append(arb_string)

    def remove_arbitrary_string(
        self, string: str | ArbitraryString, /, *, strict: bool = False
    ) -> None:
        """
        Remove arbitrary string from Calculator.

        Parameters
        ----------
        string : str
            Arbitrary string to remove.
        strict : bool, default: False
            If True, raise a ValueError if no arbitrary string was added.
            If False (default), does nothing if no arbitrary string was added.

        Raises
        -------
        ValueError
            If `strict` is True and no arbitrary string is present.
        """
        if not self._arbitrary_strings:
            if strict:
                raise ValueError("No arbitrary string added so none can be removed.")
        else:
            arb_string = ArbitraryString(string=string) if isinstance(string, str) else string
            self._arbitrary_strings.remove(arb_string)

    def clear_arbitrary_strings(self, *, strict: bool = False) -> None:
        """
        Clear all arbitrary strings from Calculator and set _arbitrary_strings to None.

        Parameters
        ----------
        strict : bool, default: False
            If True, raise a ValueError if no arbitrary string was added.
            If False (default), does nothing since there is no string available to clear.

        Raises
        -------
        ValueError
            If `strict` is True and no arbitrary string is present.
        """
        if not self._arbitrary_strings:
            if strict:
                raise ValueError("No arbitrary strings added.")
        else:
            self._arbitrary_strings.clear()
