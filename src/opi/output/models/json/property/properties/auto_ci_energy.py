from typing import Literal

from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeInt,
)
from opi.output.models.json.property.properties.energy import Energy


class AutoCiEnergy(Energy):
    """
    This class contains information about the Auto CI Energy

    Attributes
    -----------
    method: Literal["AUTOCI"]
    String that identifies the method that was used for the energy calculation.
    Is used for identifying different energy types.
    numofel: StrictNonNegativeInt | None, default = None
        Number of electrons
    numofcorrel: StrictNonNegativeInt | None, default = None
        Number of corr-electrons
    numofalphacorrel: StrictNonNegativeInt | None, default = None
        Number of corr-electrons with an alpha spin
    numofbetacorell: StrictNonNegativeInt | None, default = None
        Number of corr-electrons with a beta spin
    refenergy: StrictFiniteFloat | None, default = None
        Energy reference
    correnergy: StrictFiniteFloat | None, default = None
        Total energy contribution of the electron-correlation
    """

    method: Literal["AUTOCI"]
    numofel: StrictNonNegativeInt | None = None
    numofcorrel: StrictNonNegativeInt | None = None
    numofalphacorrel: StrictNonNegativeInt | None = None
    numofbetacorrel: StrictNonNegativeInt | None = None
    refenergy: list[list[StrictFiniteFloat]] | None = None
    correnergy: list[list[StrictFiniteFloat]] | None = None
