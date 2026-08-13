import re

from opi.input.blocks.base import BlockABC
from opi.input.blocks.util import NoCaseDict

__all__ = [
    "Block",
]


_NAME_PATTERN = re.compile(r"^[a-zA-Z_][a-zA-Z_0-9]*$")


class Block(BlockABC):
    """
    Class used to create arbitrary blocks that have not yet been implemented in OPI. The key-value pairs for an arbitrary
    block option are stored as arbitrary options, hence both must be strings.

    Within an `Input`, blocks are keyed by their name, so an arbitrary block cannot be added
    twice under the same name.

    Examples
    --------

    >> arbit_block = Block(name='arbitrary_block', values = {'arbitrary_key': 'arbitrary_value'})


    """

    def __init__(self, name: str, values: dict[str, str] | None = None, aftercoord: bool = False):
        """

        Parameters
        ----------
        name: str
            Name of arbitrary block

        values: dict[str, str] | None
            Values to be added to the block. They will be added as arbitrary options, so both key and value must be strings.

        aftercoord: bool, default: False
            Sets whether block will appear before or after coordinates in the ORCA .inp file.
        """
        super().__init__(aftercoord=aftercoord)

        name = self._normalize(name)
        self._name = name
        if values:
            self._arbitrary = NoCaseDict(values)

    def _normalize(self, name: str) -> str:
        """
        Normalize the arbitrary block name with `Block.normalize_name()` and validate it.

        Parameters
        ----------
        name: str
            User-given name of arbitrary block.

        Returns
        -------
        str
            Normalized string.

        Raises
        ------
        ValueError
            If user-given name is invalid, or an ORCA block with that name is already implemented.
        """
        name = self.normalize_name(name)

        if not _NAME_PATTERN.fullmatch(name):
            raise ValueError("Invalid name for ORCA block")

        block_class = BlockABC.get_block_class(name)

        if block_class:
            raise ValueError(
                f"ORCA block with this name already exists. Use {block_class.__name__} instead."
            )

        return name
