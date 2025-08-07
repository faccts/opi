from pydantic import StrictStr

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

    energyunit: StrictStr | None = None
    mos: list[MO] | None = None
    orbitallabels: list[StrictStr] | None = None
