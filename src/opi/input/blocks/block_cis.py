from typing import Literal

from pydantic import field_validator

from opi.input.blocks import Block, NumList

__all__ = ("BlockCis",)


class BlockCis(Block):
    """Class to model %cis block in ORCA"""

    _name: str = "cis"
    nroots: int | None = None
    iroot: int | None = None
    irootmult: Literal["singlet", "triplet"] | None = None
    maxdim: int | None = None
    maxiter: int | None = None
    nguessmat: int | None = None
    maxcore: int | None = None
    etol: float | None = None
    rtol: float | None = None
    tda: bool | None = None
    lrcpcm: bool | None = None
    cpcmeq: bool | None = None
    donto: bool | None = None
    saveunrnatorb: bool | None = None
    spinflip: bool | None = None
    soc: bool | None = None
    socgrad: bool | None = None
    triplets: bool | None = None
    dotrans: bool | None = None
    dcorr: int | None = None
    doscs: bool | None = None
    intaccxc: float | None = None
    gridxc: int | None = None
    gridx: int | None = None
    ntostates: NumList | None = None
    scspar: NumList | None = None
    ewin: NumList | None = None

    @field_validator("ntostates", "ewin", "scspar", mode="before")
    @classmethod
    def numlist_from_list(cls, inp: NumList | list[int] | list[float]) -> NumList:
        """
        Parameters
        ----------
        inp : NumList | list[int] | list[float]
        """
        if isinstance(inp, list):
            return NumList(inp)
        else:
            return inp
