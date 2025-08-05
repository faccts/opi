from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictPositiveInt,
)


class RoCiEnergy(GetItem):
    """
    This class contains infos about the restricted open shell CI energies

    Attributes
    ----------
    multiplicities: list[list[StrictPositiveFloat]] | None, default = None
        list of the multiplicities of the states
    energies: list[Lis[StrictFiniteFloat]] | None, default = None
        Energies of the stats
    refenergy: StrictFiniteFloat | None, default = None
        Reference energy
    correnergy: StrictFiniteFloat | None, default = None
        Correlation energy
    totalenergy: StrictFiniteFloat | None, default = None
        Total energy
    """

    multiplicities: list[list[StrictPositiveInt]] | None = None
    energies: list[list[StrictFiniteFloat]] | None = None
    refenergy: StrictFiniteFloat | None = None
    correnergy: StrictFiniteFloat | None = None
    totalenergy: StrictFiniteFloat | None = None
