from typing import Literal

from opi.output.models.base.strict_types import StrictNonNegativeInt
from opi.output.models.json.property.properties.energy import Energy


class CisEnergy(Energy):
    """
    Has the Information about energies that were calculated in the ORCA job

    Attributes
    ----------
    method: Literal["TDA/CIS"]
    String that identifies the method that was used for the energy calculation.
    Is used for identifying different energy types
    block: list[list[StrictNonNegativeInt]] | None, default = None
    nblocks: StrictNonNegativeInt | None, default = None
    nroots: list[list[StrictNonNegativeInt]] | None, default = None
    ntotalroots: StrictNonNegativeInt | None, default = None
    relcorr: str | None, default = None
    root: list[list[StrictNonNegativeInt]] | None, default = None
    dcorr: float | None, default = None
        (D) correction algorithm
    e0: float | None, default = None
        Energy of the ground state
    mode: str | None, default = None
    multp1: bool | None, default = None
        if the higher multiplicity was also done
    """

    method: Literal["TDA/CIS"]
    block: list[list[StrictNonNegativeInt]] | None = None
    nblocks: StrictNonNegativeInt | None = None
    nroots: list[list[StrictNonNegativeInt]] | None = None
    ntotalroots: StrictNonNegativeInt | None = None
    relcorr: str | None = None
    root: list[list[StrictNonNegativeInt]] | None = None
    dcorr: float | None = None
    e0: float | None = None
    mode: str | None = None
    multp1: bool | None = None
