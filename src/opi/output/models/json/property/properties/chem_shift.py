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
    method: StrictStr
        Used Method in this calculation
    level: StrictStr
        Type and relaxation of density
    numofnucs: StrictPositiveInt
        Number of calculated nuclei
    nuc: list[StrictNonNegativeInt]
        Index of the nuclei
    elems: list[StrictPositiveInt]
        Number of the place of the Element in the periodic table
    stot: list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]
        Total tensor
    orientation: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]]
        Eigenvectors
    stoteigen: list[list[list[StrictFiniteFloat]]]
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
