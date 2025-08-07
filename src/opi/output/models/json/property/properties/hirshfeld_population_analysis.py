from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeFloat,
)
from opi.output.models.json.property.properties.population_analysis import PopulationAnalysis


class HirshfeldPopulationAnalysis(PopulationAnalysis):
    """
    Has the Information about the Hirshfeld population analysis

    Attributes
    ----------
    densa: StrictNonNegativeFiniteFloat | None, default = None
        Density of alpha electrons
    densb: StrictNonNegativeFiniteFloat | None, default = None
        Density of beta electrons
    spin: list[list[StrictFiniteFloat]] | None, default = None
        list of the spin densities, at the atoms
    """

    densa: StrictNonNegativeFloat | None = None
    densb: StrictNonNegativeFloat | None = None
    spin: list[list[StrictFiniteFloat]] | None = None
