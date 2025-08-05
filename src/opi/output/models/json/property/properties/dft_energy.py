from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeInt,
)


class DftEnergy(GetItem):
    """
    This class contains the information about the DFT-energy.

    Attributes
    ----------
    nalphael: StrictNonNegativeInt | None, default = None
        Number of alpha electrons
    nbetael: StrictNonNegativeInt | None, default = None
        Number of beta electrons
    ntotalel: StrictNonNegativeInt | None, default = None
        Total number of electrons
    eexchange: StrictFiniteFloat | None, default = None
        Calculated exchange energy
    ecorr: StrictFiniteFloat | None, default = None
        Calculated correlation energy
    ecnl: StrictFiniteFloat | None, default = None
        Calculated energy of the charge neutral level
    exc: StrictFiniteFloat | None, default = None
        Calculated exchange-correlation energy
    eembed: StrictFiniteFloat | None, default = None
        Calculated energy from embedded DFT
    finalen: StrictFiniteFloat | None, default = None
        Total calculated energy
    """

    nalphael: StrictNonNegativeInt | None = None
    nbetael: StrictNonNegativeInt | None = None
    ntotalel: StrictNonNegativeInt | None = None
    eexchange: StrictFiniteFloat | None = None
    ecorr: StrictFiniteFloat | None = None
    ecnl: StrictFiniteFloat | None = None
    exc: StrictFiniteFloat | None = None
    eembed: StrictFiniteFloat | None = None
    finalen: StrictFiniteFloat | None = None
