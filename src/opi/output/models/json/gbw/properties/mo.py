from pydantic import StrictFloat, StrictInt, StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import StrictNonNegativeFloat


class MO(GetItem):
    """
    This class contains information about

    Attributes
    ----------
    mocoefficients: list[StrictFloat]
        Coefficient of the molecular orbitals
    occupancy: StrictNonNegativeFloat
        Occupancy of the molecular orbital
    orbitalenergy: StrictFloat
        Energy of the molecular orbital
    orbitalsymlabel: StrictStr
        Symmetry label of the molecular orbital
    orbitalsymmetry: StrictInt
        Symmetry of the molecular orbital
    """

    mocoefficients: list[StrictFloat] | None = None
    occupancy: StrictNonNegativeFloat | None = None
    orbitalenergy: StrictFloat | None = None
    orbitalsymlabel: StrictStr | None = None
    orbitalsymmetry: StrictInt | None = None
