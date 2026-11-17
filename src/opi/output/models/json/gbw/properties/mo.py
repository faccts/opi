from pydantic import Field, StrictFloat, StrictInt, StrictStr

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

    mocoefficients: list[StrictFloat] | None = Field(
        default=None, serialization_alias="MOCoefficients"
    )
    occupancy: StrictNonNegativeFloat | None = Field(default=None, serialization_alias="Occupancy")
    orbitalenergy: StrictFloat | None = Field(default=None, serialization_alias="OrbitalEnergy")
    orbitalsymlabel: StrictStr | None = Field(default=None, serialization_alias="OrbitalSymLabel")
    orbitalsymmetry: StrictInt | None = Field(default=None, serialization_alias="OrbitalSymmetry")
