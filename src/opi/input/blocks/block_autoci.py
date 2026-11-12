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
            "CISDT",
            "CCD",
            "CCSD",
            "CCSDT",
            "CEPA(0)",
            "QCISD",
            "CC2",
            "CC3",
            "CCSD[T]",
            "CCSD(T)",
            "CCSDT-1",
            "CCSDT-2",
            "CCSDT-3",
            "CCSDT-4",
            "FIC-MRCI",
            "FIC-MRCEPA(0)",
            "FIC-MRACPF",
            "FIC-MRAQCC",
            "FIC-DDCI3",
            "FIC-MRCC",
            "MP2",
            "MP3",
            "MP4(SDQ)",
            "MP4",
            "MP5",
        ]
        | None
    ) = None
