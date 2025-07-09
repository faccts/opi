from typing import Literal

from pydantic import field_validator

from opi.input.blocks import Block, InputFilePath

__all__ = ("BlockLoc",)


class BlockLoc(Block):
    """Class to model %loc block in ORCA"""

    _name: str = "loc"
    locmet: (
        Literal[
            "pipekmezey",
            "pm",
            "fosterboys",
            "fb",
            "iaoibo",
            "iaoboys",
            "newboys",
            "ahfb",
            "pmvvo",
            "livvo",
        ]
        | None
    ) = None
    locmetvirt: (
        Literal[
            "pipekmezey",
            "pm",
            "fosterboys",
            "fb",
            "iaoibo",
            "iaoboys",
            "newboys",
            "ahfb",
            "pmvvo",
            "livvo",
        ]
        | None
    ) = None
    printlevel: int | None = None
    maxiter: int | None = None
    randomize: bool | None = None
    occ: bool | None = None
    virt: bool | None = None
    t_core: float | None = None
    t_strong: float | None = None
    t_bond: float | None = None
    tol: float | None = None
    orbspread: bool | None = None
    popmethod: Literal["mulliken", "loewdin"] | None = None
    iaobasis: (
        Literal["scf_sv", "sto_3g", "mini", "ano_sz", "ano_rcc_mb", "minao_auto_pp"] | None
    ) = None
    loctol: float | None = None
    loctolled: float | None = None
    loctolrel: float | None = None
    dvdnroots: int | None = None
    dvdnrootsfinal: int | None = None
    dvdmaxdim: int | None = None
    dvdmaxiter: int | None = None
    file: InputFilePath | None = None

    @field_validator("file", mode="before")
    @classmethod
    def path_from_string(cls, path: str | InputFilePath) -> InputFilePath:
        """
        Parameters
        ----------
        path : str | InputFilePath
        """
        if isinstance(path, str):
            return InputFilePath.from_string(path)
        else:
            return path
