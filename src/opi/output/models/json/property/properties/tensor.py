from pydantic import StrictInt, StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeFloat,
    StrictPositiveFloat,
    StrictPositiveInt,
)


class Tensor(GetItem):
    """
    This class contains the A-Tensors of the epr calculation

    Attributes
    ----------
    method: StrictStr | None, default = None
        Used method in this calculation
    level: StrictStr | None, default = None
        Type and relaxation of density
    mult : StrictPositiveInt | None, default = None
        Multiplicity of the electronic state
    state : int | None, default = None
        Electronic state
    irrep : int | None, default = None
        Irreducible representation of the electronic state
    numofnucs: StrictPositiveInt | None, default = None
        Number of calculated nuclei
    nuc: list[StrictPositiveInt] | None, default = None
        list of used nuclei
    elem: list[StrictPositiveInt] | None, default = None
        Atomic number of the nucleus
    isotope: list[StrictPositiveFloat] | None, default = None
        Used isotope of the element
    i: list[StrictNonNegativeFloat] | None, default = None
        Spin of nucleus
    pfac: list[StrictPositiveFloat] | None, default = None
        Prefactor in MHz
    araw: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None, default = None
        Raw tensors of each tensor
    aeigenvalues: list[list[list[StrictFiniteFloat]]] | None, default = None
        Eigenvalue of each tensor
    aiso: list[StrictFiniteFloat] | None, default = None
        Iso value of each tensor
    orientation: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None, default = None
        Eigenvectors of each tensor
    """

    method: StrictStr | None = None
    level: StrictStr | None = None
    mult: StrictPositiveInt | None = None
    state: StrictInt | None = None
    irrep: StrictInt | None = None
    numofnucs: StrictPositiveInt | None = None
    nuc: list[StrictPositiveInt] | None = None
    elem: list[StrictPositiveInt] | None = None
    isotope: list[StrictPositiveFloat] | None = None
    i: list[StrictNonNegativeFloat] | None = None
    pfac: list[StrictPositiveFloat] | None = None
    araw: list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None = None
    aeigenvalues: list[list[list[StrictFiniteFloat]]] | None = None
    aiso: list[StrictFiniteFloat] | None = None
    orientation: (
        list[list[tuple[StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]]] | None
    ) = None
