from typing import Literal

from opi.output.models.base.strict_types import StrictFiniteFloat
from opi.output.models.json.property.properties.energy import Energy, first_energy


class Mp2EnergyBase(Energy):
    """
    This is the base class for MP2 energies

    Attributes
    ----------
    refenergy: list[list[StrictFiniteFloat]] | None, default = None
        Reference energy
    correnergy: list[list[StrictFiniteFloat]] | None, default = None
        MP2 correlation energy
    """

    refenergy: list[list[StrictFiniteFloat]] | None = None
    correnergy: list[list[StrictFiniteFloat]] | None = None

    @property
    def reference_energy(self) -> StrictFiniteFloat | None:
        """
        The reference energy in Eh as a plain float.

        Shortcut for `refenergy[0][0]`. None if the output contains no reference energy.
        """
        return first_energy(self.refenergy)

    @property
    def correlation_energy(self) -> StrictFiniteFloat | None:
        """
        The correlation energy in Eh as a plain float.

        Shortcut for `correnergy[0][0]`. None if the output contains no correlation energy.
        """
        return first_energy(self.correnergy)


class Mp2Energy(Mp2EnergyBase):
    """This class contains information about the MP2 energy"""

    method: Literal["MP2"]


class Mp2OOEnergy(Mp2EnergyBase):
    """This class contains information about the orbital-optimized MP2 energy"""

    method: Literal["MP2(OO)"]
