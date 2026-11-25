from pydantic import StrictInt, StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeInt,
    StrictPositiveInt,
)


class ChemicalShift(GetItem):
    """
    This class contains the information about the chemical shift for NMR calculations

    Attributes
    ----------
    method: StrictStr | None, default = None
        Used Method in this calculation
    level: StrictStr
        Type and relaxation of density
    mult: StrictPositiveInt | None, default = None
        Multiplicity
    irrep: StrictNonNegativeInt | None, default = None
        Irreducible representation
    state: StrictInt | None, default = None
        Electronic state
    numofnucs: StrictPositiveInt | None, default = None
        Number of calculated nuclei
    nuc: list[StrictNonNegativeInt] | None, default = None
        Index of the nuclei
    elems: list[StrictPositiveInt] | None, default = None
        Number of the place of the Element in the periodic table
    siso: list[StrictFiniteFloat] | None, default = None
        Isotropic shielding constant of each nucleus in ppm
    saniso: list[StrictFiniteFloat] | None, default = None
        Shielding anisotropy of each nucleus in ppm
    stot: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None, default = None
        Total tensor
    sdso: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None, default = None
        Diamagnetic spin-orbit contribution to the total tensor
    spso: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None, default = None
        Paramagnetic spin-orbit contribution to the total tensor
    orientation: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None, default = None
        Eigenvectors
    stoteigen: list[list[list[StrictFiniteFloat]]] | None, default = None
        Eigenvalues
    """

    method: StrictStr | None = None
    level: StrictStr | None = None
    mult: StrictPositiveInt | None = None
    irrep: StrictNonNegativeInt | None = None
    state: StrictInt | None = None
    numofnucs: StrictPositiveInt | None = None
    nuc: list[StrictNonNegativeInt] | None = None
    elems: list[StrictPositiveInt] | None = None
    siso: list[StrictFiniteFloat] | None = None
    saniso: list[StrictFiniteFloat] | None = None
    stot: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None = None
    sdso: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None = None
    spso: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None = None
    orientation: (
        list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None
    ) = None
    stoteigen: list[list[list[StrictFiniteFloat]]] | None = None
