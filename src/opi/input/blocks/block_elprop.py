from typing import Literal

from pydantic import field_validator

from opi.input.blocks import Block, NumList

__all__ = ("BlockElprop",)


class BlockElprop(Block):
    """Class to model %elprop block in ORCA"""

    _name: str = "elprop"
    printlevel: int | None = None
    dipole: bool | None = None
    quadrupole: bool | None = None
    polarvelocity: bool | None = None
    polardipquad: bool | None = None
    polarquadquad: bool | None = None
    kinetic: bool | None = None
    efield: float | None = None
    polar: Literal["analytic", "semianalytic", "numeric"] | None = None
    freq_real: float | None = None
    freq_imag: float | None = None
    dipoleatom: bool | None = None
    quadrupoleatom: bool | None = None
    polaratom: int | None = None
    solver: Literal["cg", "diis", "pople"] | None = None
    maxiter: int | None = None
    maxdiis: int | None = None
    tol: float | None = None
    levelshift: float | None = None
    origin: (
        Literal[
            "centerofmass",
            "centerofnuccharge",
            "centerofnuclearcharge",
            "centerofelcharge",
            "centerofspindens",
            "centerofspindensity",
        ]
        | NumList
        | None
    ) = None

    @field_validator("origin", mode="before")
    @classmethod
    def numlist_from_list(cls, inp: NumList | str | list[int] | list[float]) -> NumList | str:
        """
        Parameters
        ----------
        inp : NumList | str | list[int] | list[float]
        """
        if isinstance(inp, list):
            return NumList(inp)
        else:
            return inp
