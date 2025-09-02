from pydantic import StrictInt, StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeFloat,
    StrictPositiveInt,
)


class NucGradient(GetItem):
    """
    This class contains information about the SCF nuclear gradients

    Attributes
    ----------
    natoms: StrictPositiveInt | None, default = None
        Number of atoms in the calculation
    method : StrictStr | None, default = None
        Underlying electronic structure method
    level : StrictStr | None, default = None
        Source of density e.g. linearized, un-relaxed, relaxed
    mult : StrictPositiveInt | None, default = None
        Multiplicity of the electronic state
    state : StrictInt | None, default = None
        Electronic state
    irrep : StrictInt | None, default = None
        Irreducible representation of the electronic state
    gradnorm: StrictNonNegativeFiniteFloat | None, default = None
        Total norm of all gradients
    grad: list[list[StrictFiniteFloat]] | None, default = None
        Gradient for each atom in each dimension
    """

    natoms: StrictPositiveInt | None = None
    method: StrictStr | None = None
    level: StrictStr | None = None
    mult: StrictPositiveInt | None = None
    state: StrictInt | None = None
    irrep: StrictInt | None = None
    gradnorm: StrictNonNegativeFloat | None = None
    grad: list[list[StrictFiniteFloat]] | None = None
