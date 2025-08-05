from pydantic import StrictBool

from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeFloat,
    StrictPositiveFloat,
    StrictPositiveInt,
)
from opi.output.models.json.property.properties.population_analysis import PopulationAnalysis


class MbisPopulationAnalysis(PopulationAnalysis):
    """This class contains the information about the MIBS population analysis

    Attributes
    ----------
    thresh: StrictPositiveFloat | None, default = None
        Threshold for printing orbitals
    niter: StrictPositiveInt | None, default = None
        Number of iterations
    largeprint: StrictBool | None, default = None
        Has "Largeprint" been used
    densa: StrictPositiveFloat | None, default = None
        Integrated alpha density
    densb: StrictPositiveFloat | None, default = None
        Integrated beta density
    spin: list[list[StrictFloat]] | None, default = None
        list of the spin populations
    npopval: list[list[NonNegativeFloat]] | None, default = None
        Population value of each atom
    sigmaval: list[list[StrictFloat]] | None, default = None
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
