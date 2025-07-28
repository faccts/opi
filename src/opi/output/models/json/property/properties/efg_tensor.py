from pydantic import StrictFloat, StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeFloat,
    StrictPositiveFloat,
    StrictPositiveInt,
)


class EfgTensor(GetItem):
    """
    This class contains the Tensors of the EPR calculation

    Attributes
    ----------
    method: StrictStr
        Used method in this calculation
    level: StrictStr
        Type and relaxation of density
    numofnucs: StrictPositiveInt
        Number of calculated nuclei
    nuc: list[StrictPositiveInt]
        list of used nuclei
    elems: list[StrictPositiveInt]
        Atomic number of the nucleus
    isotope: list[StrictPositiveFloat]
        Used isotope of the element
    i: list[StrictNonNegativeFloat]
        Spin of nucleus
    qfac: list[StrictFiniteFloat]
        Prefactor in MHz
    v: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]]
        Possible raw tensors of each tensor
    veigenvalues: list[list[StrictFiniteFloat]]
        eigenvalue of each tensor
    viso: list[tuple[StrictFiniteFloat]]
        iso value of each tensor
    orientation: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]]
        eigenvectors of each tensor
    """

    method: StrictStr | None = None
    level: StrictStr | None = None
    numofnucs: StrictPositiveInt | None = None
    nuc: list[StrictPositiveInt] | None = None
    elems: list[StrictPositiveInt] | None = None
    isotope: list[StrictPositiveFloat] | None = None
    i: list[StrictNonNegativeFloat] | None = None
    qfac: list[StrictFloat] | None = None
    v: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None = None
    veigenvalues: list[list[list[StrictFiniteFloat]]] | None = None
    viso: list[StrictFiniteFloat] | None = None
    orientation: (
        list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None
    ) = None
