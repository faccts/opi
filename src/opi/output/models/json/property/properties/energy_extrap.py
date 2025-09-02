from pydantic import StrictBool

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictPositiveInt,
)


class EnergyExtrapolation(GetItem):
    """
    This class contains information about the used Energy extrapolation

    Attributes
    ----------
    doep1: StrictBool | None, default = None
        Do extrapolation with one method
    doep2: StrictBool | None, default = None
        Do extrapolation with two methods and the same basis set
    doep3: StrictBool | None, default = None
        Do extrapolation with two methods and three basis sets
    dogradients: StrictBool | None, default = None
        Extrapolate energy gradient
    numofenergies: StrictPositiveInt | None, default = None
        How many energies are used
    scfenergies: list[list[StrictFiniteFloat]] | None, default = None
        list of the used energies
    scfcbs: StrictFiniteFloat | None, default = None
        SCF Energy extrapolated for complete basis set
    correnergies: list[list[StrictFiniteFloat]] | None, default = None
        Used correlation energies
    corrcbs: StrictFiniteFloat | None, default = None
        Extrapolated correlation energy for correlation energy
    ccsdtenergyx: StrictFiniteFloat | None, default = None
        CCSD(T] energy extrapolation, not used if only doep1 = true
    totalcbs: StrictFiniteFloat | None, default = None
        Total extrapolated energy
    """

    doep1: StrictBool | None = None
    doep2: StrictBool | None = None
    doep3: StrictBool | None = None
    dogradients: StrictBool | None = None
    numofenergies: StrictPositiveInt | None = None
    scfenergies: list[list[StrictFiniteFloat]] | None = None
    scfcbs: StrictFiniteFloat | None = None
    correnergies: list[list[StrictFiniteFloat]] | None = None
    corrcbs: StrictFiniteFloat | None = None
    ccsdtenergyx: StrictFiniteFloat | None = None
    totalcbs: StrictFiniteFloat | None = None
