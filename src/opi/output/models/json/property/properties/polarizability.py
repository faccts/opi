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
    method: StrictStr
        Used Method: SCF, DFT, CC or similar
    level: StrictStr
        Type and relaxation of Density like Electron Density
    mult : StrictPositiveInt
        Multiplicity of the electronic state
    state : StrictInt
        Electronic state
    irrep : StrictInt
        Irreducible representation of the electronic state
    doatomicpolar: StrictBool
        Should the dipole atom calculation be done
    rawcartesian: list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]
        Raw data of the cartesian product
    diagonalizedtensor: list[StrictFiniteFloat]
        Diagonalized tenors
    orientation: list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]
        Orientation of the polarization vector
    isotropicpolar: StrictFiniteFloat
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
