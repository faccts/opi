from pydantic import StrictInt, StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeInt,
    StrictPositiveInt,
)


class PopulationAnalysis(GetItem):
    """
    Has the Information about the different population analysis

    Attributes
    ----------
    natoms: StrictPositiveInt | None, default = None
        Numbers of atoms
    atno : list[list[StrictPositiveInt]] | None, default = None
        Atom-number according to the position in the periodic table
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
    atomiccharges: list[list[StrictFiniteFloat]] | None, default = None
        Charges of the atoms according to the population analysis
    """

    natoms: StrictPositiveInt | None = None
    atno: list[list[StrictNonNegativeInt]] | None = None
    method: StrictStr | None = None
    level: StrictStr | None = None
    mult: StrictPositiveInt | None = None
    state: StrictInt | None = None
    irrep: StrictInt | None = None
    atomiccharges: list[list[StrictFiniteFloat]] | None = None


class MullikenPopulationAnalysis(PopulationAnalysis):
    """This class contains the information about the Mulliken population analysis"""


class LoewdinPopulationAnalysis(PopulationAnalysis):
    """This class contains the information about the Loewdin population analysis"""


class ChelpgPopulationAnalysis(PopulationAnalysis):
    """This class contains the information about the CHELPG population analysis"""
