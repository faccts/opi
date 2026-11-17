from pydantic import Field, StrictStr

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

    basis: list[Base] | None = Field(default=None, serialization_alias="Basis")
    basisauxc: list[Base] | None = Field(default=None, serialization_alias="BasisAuxC")
    basisauxj: list[Base] | None = Field(default=None, serialization_alias="BasisAuxJ")
    basisauxjk: list[Base] | None = Field(default=None, serialization_alias="BasisAuxJK")
    coords: list[StrictFiniteFloat] | None = Field(default=None, serialization_alias="Coords")
    elementlabel: StrictStr | None = Field(default=None, serialization_alias="ElementLabel")
    elementnumber: StrictNonNegativeInt | None = Field(
        default=None, serialization_alias="ElementNumber"
    )
    idx: StrictNonNegativeInt | None = Field(default=None, serialization_alias="Idx")
    loewdincharge: StrictFiniteFloat | None = Field(
        default=None, serialization_alias="LoewdinCharge"
    )
    mullikencharge: StrictFiniteFloat | None = Field(
        default=None, serialization_alias="MullikenCharge"
    )
    nuclearcharge: StrictFiniteFloat | None = Field(
        default=None, serialization_alias="NuclearCharge"
    )
