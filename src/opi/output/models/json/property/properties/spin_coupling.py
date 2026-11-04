from pydantic import StrictInt, StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeInt,
    StrictPositiveFloat,
    StrictPositiveInt,
)


class SpinSpinCoupling(GetItem):
    """
    This class contains the information about the spin spin coupling

    Attributes
    ----------
    method: StrictStr | None, default = None
        Used Method in this calculation
    level: StrictStr | None, default = None
        Type and relaxation of density
    mult: StrictPositiveInt | None, default = None
        Multiplicity
    irrep: StrictNonNegativeInt | None, default = None
        Irreducible representation
    state: StrictInt | None, default = None
        Electronic state
    numofnucpairs: StrictPositiveInt | None, default = None
        Number of nuclei pairs to calculate
    numofnucpairsdso: StrictPositiveInt | None, default = None
        Number of nuclear pairs to calculate DSO
    numofnucpairspso: StrictPositiveInt | None, default = None
        Number of nuclear pairs to calculate PSO
    numofnucpairsfc: StrictPositiveInt | None, default = None
        Number of nuclear pairs to calculate FC
    numofnucpairssd: StrictPositiveInt | None, default = None
        Number of nuclear pairs to calculate SD
    pairsinfo: list[tuple[StrictNonNegativeInt, StrictPositiveInt, StrictNonNegativeInt, StrictPositiveInt]] | None, default = None
        Index 1 (0-based), atomic number 1, index 2 (0-based) and atomic number 2 of the atoms that build a pair
    pairsdistances: list[list[StrictPositiveFloat]] | None, default = None
        Distance of each pair
    pairstotalssciso: list[list[StrictPositiveFloat]] | None, default = None
        Spi-Spin coupling constant of each pair
    """

    method: StrictStr | None = None
    level: StrictStr | None = None
    mult: StrictPositiveInt | None = None
    irrep: StrictNonNegativeInt | None = None
    state: StrictInt | None = None
    numofnucpairs: StrictPositiveInt | None = None
    numofnucpairsdso: StrictPositiveInt | None = None
    numofnucpairspso: StrictPositiveInt | None = None
    numofnucpairsfc: StrictPositiveInt | None = None
    numofnucpairssd: StrictPositiveInt | None = None
    pairsinfo: (
        list[
            tuple[
                StrictNonNegativeInt,
                StrictPositiveInt,
                StrictNonNegativeInt,
                StrictPositiveInt,
            ]
        ]
        | None
    ) = None
    pairsdistances: list[list[StrictPositiveFloat]] | None = None
    pairstotalssciso: list[list[StrictFiniteFloat]] | None = None
