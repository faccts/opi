from typing import Literal

from pydantic import field_validator

from opi.input.blocks import Block, NumList

__all__ = ("BlockRel",)


class BlockRel(Block):
    """Class to model %rel block in ORCA"""

    _name: str = "rel"
    method: Literal["dkh", "zora", "iora", "ioramm", "x2c"] | None = None
    fpfwtrafo: bool | None = None
    finitenuc: bool | None = None
    modeldens: Literal["rhohf", "rhodkh", "rhozora"] | None = None
    mode: int | None = None
    order: int | None = None
    modelpot: Literal["ven", "vc", "vxa", "vlda", "vpc"] | None = None
    picturechange: int | None = None
    socopt: int | None = None
    onecenter: bool | None = None
    xalpha: float | None = None
    dkh1cautoaux: bool | None = None
    lightatomthresh: int | None = None
    dlu: bool | None = None
    storagelevel: int | None = None
    socenergy: bool | None = None
    scalezora: bool | None = None
    printlevel: int | None = None
    c: float | None = None
    eps: float | None = None
    soctype: int | None = None
    socmaxcenter: (
        Literal["somf(1x)", "ri-somf(1x)", "veff-soc", "veff(-2x)-soc", "amfi", "amfi-a"] | None
    ) = None
    socprintlevel: int | None = None
    socoff: int | None = None
    socflags: NumList | None = None
    zeff: NumList | None = None

    @field_validator("socflags", "zeff", mode="before")
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
