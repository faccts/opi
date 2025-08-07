from pydantic import StrictBool, StrictInt, StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictPositiveInt,
)


class Polarizability(GetItem):
    """
    This class contains information about the polarizability of the molecule

    Attributes
    ----------
    method: StrictStr | None, default = None
        Used Method: SCF, DFT, CC or similar
    level: StrictStr | None, default = None
        Type and relaxation of Density like Electron Density
    mult : StrictPositiveInt | None, default = None
        Multiplicity of the electronic state
    state : StrictInt | None, default = None
        Electronic state
    irrep : StrictInt | None, default = None
        Irreducible representation of the electronic state
    doatomicpolar: StrictBool | None, default = None
        Should the dipole atom calculation be done
    rawcartesian: list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]] | None, default = None
        Raw data of the cartesian product
    diagonalizedtensor: list[StrictFiniteFloat] | None, default = None
        Diagonalized tenors
    orientation: list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]] | None, default = None
        Orientation of the polarization vector
    isotropicpolar: StrictFiniteFloat | None, default = None
        Isotropic polarity
    """

    method: StrictStr | None = None
    level: StrictStr | None = None
    mult: StrictPositiveInt | None = None
    state: StrictInt | None = None
    irrep: StrictInt | None = None
    doatomicpolar: StrictBool | None = None
    rawcartesian: list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]] | None = None
    diagonalizedtensor: list[list[StrictFiniteFloat]] | None = None
    orientation: list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]] | None = None
    isotropicpolar: StrictFiniteFloat | None = None
