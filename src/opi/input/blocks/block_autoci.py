from typing import Literal

from opi.input.blocks import BlockABC

_all__ = ("BlockAutoCI",)


class BlockAutoCI(BlockABC):
    """Class to model %autoci block in ORCA"""

    _name: str = "autoci"
    # > options
    citype: (
        Literal[
            "cid",
            "cisd",
            "cisdt",
            "ccd",
            "ccsd",
            "ccsdt",
            "cepa(0)",
            "qcisd",
            "cc2",
            "cc3",
            "ccsd[t]",
            "ccsd(t)",
            "ccsdt-1",
            "ccsdt-2",
            "ccsdt-3",
            "ccsdt-4",
            "fic-mrci",
            "fic-mrcepa(0)",
            "fic-mracpf",
            "fic-mraqcc",
            "fic-ddci3",
            "fic-mrcc",
            "mp2",
            "mp3",
            "mp4(sdq)",
            "mp4",
            "mp5",
        ]
        | None
    ) = None
