from typing import Literal

from opi.output.models.base.strict_types import StrictFiniteFloat
from opi.output.models.json.property.properties.energy import Energy


class Mp2EnergyBase(Energy):
    """
    This is the base class for MP2 energies

    Attributes
    ----------
    refenergy: StrictFiniteFloat | None, default = None
        Reference energy
    correnergy: StrictFiniteFloat | None, default = None
        MP2 correlation energy
    """

    refenergy: list[list[StrictFiniteFloat]] | None = None
    correnergy: list[list[StrictFiniteFloat]] | None = None


class Mp2Energy(Mp2EnergyBase):
    """This class contains information about the MP2 energy"""

    method: Literal["MP2"]


class Mp2OOEnergy(Mp2EnergyBase):
    """This class contains information about the orbital-optimized MP2 energy"""

    method: Literal["MP2(OO)"]
