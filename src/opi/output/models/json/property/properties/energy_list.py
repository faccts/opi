from typing import ClassVar, Iterator

from pydantic import ConfigDict, RootModel

from opi.output.models.json.property.properties.auto_ci_energy import (
    AutoCiEnergy,
)
from opi.output.models.json.property.properties.cas_energy import (
    CasEnergy,
    Caspt2Energy,
)
from opi.output.models.json.property.properties.cis_energy import CisEnergy
from opi.output.models.json.property.properties.energy import Energy
from opi.output.models.json.property.properties.mdci_energy import (
    Mdcisd_t_Energies,
    MdcisdEnergies,
)
from opi.output.models.json.property.properties.mp2_energy import (
    Mp2Energy,
    Mp2OOEnergy,
)
from opi.output.models.json.property.properties.scf_energy import ScfEnergy

# Available energy types in ORCA
EnergyTypes = (
    ScfEnergy
    | MdcisdEnergies
    | Mdcisd_t_Energies
    | CasEnergy
    | Caspt2Energy
    | AutoCiEnergy
    | Mp2Energy
    | Mp2OOEnergy
    | CisEnergy
    | Energy
)


# Define a list of energies using a RootModel
class EnergyList(RootModel[list[EnergyTypes]]):
    """RootModel for identifying different ORCA energy types based on their `method` string"""

    model_config: ClassVar[ConfigDict] = {  # type: ignore
        "discriminator": "method"
    }

    def __iter__(self) -> Iterator[EnergyTypes]:  # type: ignore
        return iter(self.root)

    def __getitem__(self, index: int) -> EnergyTypes:
        return self.root[index]

    def __len__(self) -> int:
        return len(self.root)
