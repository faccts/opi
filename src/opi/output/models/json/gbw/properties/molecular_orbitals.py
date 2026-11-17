from pydantic import Field, StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.json.gbw.properties.mo import MO


class MolecularOrbitals(GetItem):
    """
    This class contains Information about the molecular orbital

    Attributes
    ----------
    energyunit: StrictStr
        Unit of the energy
    mos: MO
        Information about the molecular Orbitals
    orbitallabels: list[StrictStr]
        Orbital label of each orbital
    """

    energyunit: StrictStr | None = Field(default=None, serialization_alias="EnergyUnit")
    mos: list[MO] | None = Field(default=None, serialization_alias="MOs")
    orbitallabels: list[StrictStr] | None = Field(default=None, serialization_alias="OrbitalLabels")
