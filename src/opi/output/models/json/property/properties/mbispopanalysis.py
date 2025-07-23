from pydantic import StrictBool

from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeFloat,
    StrictPositiveFloat,
    StrictPositiveInt,
)
from opi.output.models.json.property.properties.popanalysis import PopulationAnalysis


class MbisPopulationAnalysis(PopulationAnalysis):
    """This class contains the information about the MIBS population analysis

    Attributes
    ----------
    thresh: PositiveFloat
        Threshold for printing orbitals
    niter: PositiveInt
        Number of iterations
    largeprint: StrictBool
        Has "Largeprint" been used
    densa: PositiveFloat
        Integrated alpha density
    densb: PositiveFloat
        Integrated beta density
    spin: list[list[StrictFloat]]
        list of the spin populations
    npopval: list[list[NonNegativeFloat]]
        Population value of each atom
    sigmaval: list[list[StrictFloat]]
        list of sigma value of the atoms
    """

    thresh: StrictPositiveFloat | None = None
    niter: StrictPositiveInt | None = None
    largeprint: StrictBool | None = None
    densa: StrictPositiveFloat | None = None
    densb: StrictPositiveFloat | None = None
    spin: list[list[StrictFiniteFloat]] | None = None
    npopval: list[list[StrictNonNegativeFloat]] | None = None
    sigmaval: list[list[StrictFiniteFloat]] | None = None
