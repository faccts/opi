from pydantic import StrictBool, StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeFloat,
    StrictNonNegativeInt,
    StrictPositiveFloat,
    StrictPositiveInt,
)


class Spectrum(GetItem):
    """
    This class contains the information about calculated spectra like UVVis or ECD spectra

    Attributes
    ----------
    density_name: StrictStr | None, default = None
        Name of property with used theory
    temperature: StrictNonNegativeFloat | None, default = None
        Assumed temperature in the calculation
    method: StrictPositiveInt | None, default = None
        Method used in this calculation
    relcorrection: StrictPositiveInt | None, default = None
        Type of relativistic treatment in quasi degenerate perturbation theory in this calculation
    denstype: StrictNonNegativeInt | None, default = None
        Used density type in this calculation
    deritype: StrictNonNegativeInt | None, default = None
        Type of derived used in this calculation
    denslevel: StrictNonNegativeInt | None, default = None
        Source of density
    representation: StrictStr | None, default = None
        Used representation (passible Unknown, Length, Velocity)
    pointgroup: StrictStr | None, default = None
        Pointgroup of the molecule
    ntrans: StrictNonNegativeInt | None, default = None
        Number of transition states modeled in the calculation
    dohighermoments: StrictBool | None, default = None
        Are higher moments supposed to be used
    states: list[tuple[StrictNonNegativeInt, StrictNonNegativeInt, StrictPositiveInt, StrictNonNegativeInt]]| None, default = None
        Contains the initial and final states
    multiplicities: list[tuple[StrictPositiveFloat, StrictPositiveFloat]] | None, default = None
        Contains the multiplicity of the initial and final state
    excitationenergies: list[list[StrictFiniteFloat]] | None, default = None
        Contains the excitation energies for all modeled transition
    """

    density_name: StrictStr | None = None
    temperature: StrictNonNegativeFloat | None = None
    method: StrictPositiveInt | None = None
    relcorrection: StrictPositiveInt | None = None
    denstype: StrictNonNegativeInt | None = None
    deritype: StrictNonNegativeInt | None = None
    denslevel: StrictNonNegativeInt | None = None
    representation: StrictStr | None = None
    pointgroup: StrictStr | None = None
    ntrans: StrictNonNegativeInt | None = None
    dohighermoments: StrictBool | None = None
    states: (
        list[
            tuple[
                StrictNonNegativeInt,
                StrictNonNegativeInt,
                StrictPositiveInt,
                StrictNonNegativeInt,
            ]
        ]
        | None
    ) = None
    multiplicities: list[tuple[StrictPositiveFloat, StrictPositiveFloat]] | None = None
    excitationenergies: list[list[StrictFiniteFloat]] | None = None
