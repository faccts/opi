from pydantic import StrictStr

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
    numofnucs: StrictPositiveInt | None, default = None
        Number of calculated nuclei
    nuc: list[StrictNonNegativeInt] | None, default = None
        Index of the nuclei
    elems: list[StrictPositiveInt] | None, default = None
        Number of the place of the Element in the periodic table
    stot: list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]] | None, default = None
        Total tensor
    orientation: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None, default = None
        Eigenvectors
    stoteigen: list[list[list[StrictFiniteFloat]]] | None, default = None
        Eigenvalues
    """

    method: StrictStr | None = None
    level: StrictStr | None = None
    numofnucs: StrictPositiveInt | None = None
    nuc: list[StrictNonNegativeInt] | None = None
    elems: list[StrictPositiveInt] | None = None
    stot: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None = None
    orientation: (
        list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None
    ) = None
    stoteigen: list[list[list[StrictFiniteFloat]]] | None = None
