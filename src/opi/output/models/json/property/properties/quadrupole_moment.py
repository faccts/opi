from pydantic import StrictBool, StrictInt, StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import StrictFiniteFloat


class QuadrupoleMoment(GetItem):
    """
    Has the Information about the quadrupole moment calculated by the ORCA Job

    Attributes
    ----------
    method: StrictStr | None, default = None
        Used method: SCF, DFT, CC or similar
    level: StrictStr | None, default = None
        Type of density like electron density
    mult: StrictInt | None, default = None
        Multiplicity of the element
    state: StrictInt | None, default = None
        Electronic state
    irrep: StrictInt | None, default = None
        Irreducible representation
    doatomicquad: StrictBool | None, default = None
        Should the quadrupole atom calculation be done
    isotropicquadmoment: StrictFloat | None, default = None
        Isotopic quadruple moment
    quadeleccontrib: list[list[StrictNegativeFloat]] | None, default = None
        Contribution of the electrons on the quadrupole moments with 6 components in space - xx, yy, zz, xy, xz, yz
    quadnuccontrib: list[list[StrictPositiveFloat]] | None, default = None
        Contribution of the nucleus on the quadrupole moments with 6 components in space - xx, yy, zz, xy, xz, yz
    quadtotal: list[list[StrictFiniteFloat]] | None, default = None
        Total quadruple moments with 6 components in space - xx, yy, zz, xy, xz, yz
    quaddiagonalized: list[list[StrictFinteFloat]] | None, default = None
        Diagonalized quadruple matrix
    """

    method: StrictStr | None = None
    level: StrictStr | None = None
    mult: StrictInt | None = None
    irrep: StrictInt | None = None
    state: StrictInt | None = None
    doatomicquad: StrictBool | None = None
    isotropicquadmoment: StrictFiniteFloat | None = None
    quadeleccontrib: list[list[StrictFiniteFloat]] | None = None
    quadnuccontrib: list[list[StrictFiniteFloat]] | None = None
    quadtotal: list[list[StrictFiniteFloat]] | None = None
    quaddiagonalized: list[list[StrictFiniteFloat]] | None = None
