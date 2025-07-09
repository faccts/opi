from typing import Literal

from opi.input.blocks import Block

__all__ = ("BlockIce",)


class BlockIce(Block):
    """Class to model %ice block in ORCA"""

    _name: str = "ice"

    # > Options
    nel: int | None = None
    norb: int | None = None
    nroots: int | None = None
    mult: int | None = None
    irrep: int | None = None
    tgen: float | None = None
    tvar: float | None = None
    etol: float | None = None
    icetype: Literal["CFGs", "CSFs", "DETs"] | None = None
    # > algorithm details
    integrals: Literal["exact", "ri"] | None
