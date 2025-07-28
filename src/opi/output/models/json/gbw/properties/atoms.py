from pydantic import StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeInt,
)
from opi.output.models.json.gbw.properties.base import Base


class Atoms(GetItem):
    """
    Contains information about the Atoms in the calculation

    Attributes
    ----------
    basis: list[Base]
        Contains the information about the basis
    basisauxc: list[Base] | None default None
        Contains the information about the basis aux c
    basisauxj: list[Base] | None default None
        Contains the information about the basis auxj
    basisauxjk: list[Base] | None default None
        Contains the information about the basis auxjk
    coords: list[StrictFiniteFloat]
        Coordinates of the atom
    elementlabel: StrictStr
        Label of the element according to the PSE
    elementnumber: StrictNonNegativeInt
        Number of the element according to the PSE
    idx StrictNonNegativeInt
        Index of the atom
    loewdincharge: StrictFiniteFloat
        loewdincharge at the atom
    mullicancharge: StrictFiniteFloat
        mullikencharge at the atom
    nuclearcharge: StrictFiniteFloat
        nuclearcharge at the atom
    """

    basis: list[Base] | None = None
    basisauxc: list[Base] | None = None
    basisauxj: list[Base] | None = None
    basisauxjk: list[Base] | None = None
    coords: list[StrictFiniteFloat] | None = None
    elementlabel: StrictStr | None = None
    elementnumber: StrictNonNegativeInt | None = None
    idx: StrictNonNegativeInt | None = None
    loewdincharge: StrictFiniteFloat | None = None
    mullikencharge: StrictFiniteFloat | None = None
    nuclearcharge: StrictFiniteFloat | None = None
