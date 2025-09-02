from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeInt,
)


class NaturalOrbitals(GetItem):
    """
    This class contains the information about the natural orbitals in a broken symmetry calculation

    Attributes
    ----------
    nel: StrictNonNegativeInt | None, default = None
        Number of electrons
    nsomo: StrictNonNegativeInt | None, default = None
        Number of SOMO
    ndomo: StrictNonNegativeInt | None, default = None
        Number of DOMO
    nvmo: StrictNonNegativeInt | None, default = None
        Number of Virtual MO
    nnatoorbs: StrictNonNegativeInt | None, default = None
        Number of natural orbitals
    occuno: list[list[StrictFloat]] | None, default = None
        Number of occupation
    occunso: list[list[StrictFiniteFloat]] | None, default = None
        Number of occupation SO
    """

    nel: StrictNonNegativeInt | None = None
    nsomo: StrictNonNegativeInt | None = None
    ndomo: StrictNonNegativeInt | None = None
    nvmo: StrictNonNegativeInt | None = None
    nnatoorbs: StrictNonNegativeInt | None = None
    occuno: list[list[StrictFiniteFloat]] | None = None
    occunso: list[list[StrictFiniteFloat]] | None = None
