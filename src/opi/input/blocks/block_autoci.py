from typing import Literal

from opi.input.blocks import BlockABC

_all__ = ("BlockAutoCI",)


class BlockAutoCI(BlockABC):
    """Class to model %autoci block in ORCA"""

    _name: str = "autoci"
    # > options
    citype: (
        Literal[
            "CID",
            "CISD",
            "CCSD",
            "CEPA0",
            "FICMRCI",
            "FICMRCEPA0",
            "FICMRACPF",
            "FICMRAQCC",
            "FICDDCI3",
            "FICMRCC",
        ]
        | None
    ) = None
