from pydantic import StrictBool, StrictInt, StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeFloat,
    StrictPositiveInt,
)


class DipoleMoment(GetItem):
    """
    Has the Information about the dipole moment calculated by the ORCA Job

    Attributes
    ----------
    method: StrictStr | None, default = None
        Used method: SCF, DFT, CC or similar
    level: StrictStr | None, default = None
        Typ and relaxation of the density
    mult: StrictPositiveInt | None, default = None
        Multiplicity of the molecule
    state : StrictInt | None, default = None
        Electronic state
    irrep : StrictInt | None, default = None
        Irreducible representation of the electronic state
    doatomicdipole: StrictBool | None, default = None
        Should the dipole atom calculation be done
    dipoleeleccontrib: list[list[StrictFiniteFloat]] | None, default = None
        Contribution of the electrons on the dipole moment in all three dimensions - x, y, z
    dipolenuccontrib: list[list[StrictFiniteFloat]] | None, default = None
        Contribution of the nucleus on the dipole moment in all three dimensions - x, y, z
    dipolemagnitude: StrictNonNegativeFloat | None, default = None
        Float absolute dipole moment independent of direction
    dipoletotal: list[list[StrictFiniteFloat]] | None, default = None
        Total dipole moment in all three dimensions - x, y, z
    """

    method: StrictStr | None = None
    level: StrictStr | None = None
    mult: StrictPositiveInt | None = None
    state: StrictInt | None = None
    irrep: StrictInt | None = None
    doatomicdipole: StrictBool | None = None
    dipoleeleccontrib: list[list[StrictFiniteFloat]] | None = None
    dipolenuccontrib: list[list[StrictFiniteFloat]] | None = None
    dipolemagnitude: StrictNonNegativeFloat | None = None
    dipoletotal: list[list[StrictFiniteFloat]] | None = None
