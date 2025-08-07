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
    method: StrictStr | None, default = None
        Used method in this calculation
    level: StrictStr | None, default = None
        Type and relaxation of density
    numofnucs: StrictPositiveInt | None, default = None
        Number of calculated nuclei
    nuc: list[StrictPositiveInt] | None, default = None
        list of used nuclei
    elems: list[StrictPositiveInt] | None, default = None
        Atomic number of the nucleus
    isotope: list[StrictPositiveFloat] | None, default = None
        Used isotope of the element
    i: list[StrictNonNegativeFloat] | None, default = None
        Spin of nucleus
    qfac: list[StrictFiniteFloat] | None, default = None
        Prefactor in MHz
    v: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None, default = None
        Possible raw tensors of each tensor
    veigenvalues: list[list[StrictFiniteFloat]] | None, default = None
        eigenvalue of each tensor
    viso: list[tuple[StrictFiniteFloat]] | None, default = None
        iso value of each tensor
    orientation: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None, default = None
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
