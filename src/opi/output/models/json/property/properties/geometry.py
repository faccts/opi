from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictNonNegativeInt,
    StrictPositiveInt,
)
from opi.output.models.json.property.properties.coord import Coordinates


class Geometry(GetItem):
    """
    Has the Information about the geometry of the Molecule used in the ORCA job

    Attributes
    ----------
    natoms: StrictPositiveInt
        Number of atoms
    ncorelessecp: StrictNonNegativeInt
        Number of core-less ECPs
    nghostatoms: StrictNonNegativeInt
        Number of ghost atoms
    coordinates: Coordinates
        Coordinates of all the atoms
    fragments: list[list[StrictPostivieInt]]
        Contains Fragment IDs of atoms
    """

    natoms: StrictPositiveInt | None = None
    ncorelessecp: StrictNonNegativeInt | None = None
    nghostatoms: StrictNonNegativeInt | None = None
    coordinates: Coordinates | None = None
    fragments: list[list[StrictPositiveInt]] | None = None
