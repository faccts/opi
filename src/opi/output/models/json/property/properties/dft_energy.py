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
    nalphael: StrictNonNegativeInt
        Number of alpha electrons
    nbetael: StrictNonNegativeInt
        Number of beta electrons
    ntotalel: StrictNonNegativeInt
        Total number of electrons
    eexchange: StrictFiniteFloat
        Calculated exchange energy
    ecorr: StrictFiniteFloat
        Calculated correlation energy
    ecnl: StrictFiniteFloat
        Calculated energy of the charge neutral level
    exc: StrictFiniteFloat
        Calculated exchange-correlation energy
    eembed: StrictFiniteFloat
        Calculated energy from embedded DFT
    finalen: StrictFiniteFloat
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
