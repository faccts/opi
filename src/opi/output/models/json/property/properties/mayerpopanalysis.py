from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeInt,
    StrictPositiveFloat,
    StrictPositiveInt,
)
from opi.output.models.json.property.properties.popanalysis import PopulationAnalysis


class MayerPopulationAnalysis(PopulationAnalysis):
    """
    Has the Information about the Mayer population analyses

    Attributes
    ----------
    bondthresh: StrictPositiveFiniteFloat
        Threshold for the bound order to be printed
    nbondordersprint: StrictPositiveInt
        Number of bounds
    bondorders: list[list[StrictFiniteFloat]]
        Bound order of each Bound
    components: list[tuple[StrictNonNegativeInt, StrictPositiveInt, StrictPositiveInt, StrictPositiveInt]]
        The indices and atomic numbers of the bonding atoms
    na : list[list[StrictFiniteFloat]]
        Mulliken gross atomic population
    za: list[list[StrictFiniteFloat]]
        Total nuclear charge
    qa: list[list[StrictFiniteFloat]]
        Mulliken gross atomic charge
    va: list[list[StrictFiniteFloat]]
        Mayer's total valence
    bva: list[list[StrictFiniteFloat]]
        Mayer's bonded valence
    fa: list[list[StrictFiniteFloat]]
        Mayer's free valence
    """

    bondthresh: StrictPositiveFloat | None = None
    nbondordersprint: StrictPositiveInt | None = None
    bondorders: list[list[StrictFiniteFloat]] | None = None
    components: (
        list[
            tuple[
                StrictNonNegativeInt,
                StrictPositiveInt,
                StrictPositiveInt,
                StrictPositiveInt,
            ]
        ]
        | None
    ) = None
    na: list[list[StrictFiniteFloat]] | None = None
    za: list[list[StrictFiniteFloat]] | None = None
    qa: list[list[StrictFiniteFloat]] | None = None
    va: list[list[StrictFiniteFloat]] | None = None
    bva: list[list[StrictFiniteFloat]] | None = None
    fa: list[list[StrictFiniteFloat]] | None = None
