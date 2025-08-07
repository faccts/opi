from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictPositiveInt,
)


class Led(GetItem):
    """
    This class contains information about the LED calculation

    Attributes
    ----------
    numoffragments: StrictPositiveInt | None, default = None
        Number of used fragments
    electrostref: list[tuple[StrictFiniteFloat, StrictFiniteFloat]] | None, default = None
        Electrostatics reference
    exchangeref: list[tuple[StrictFiniteFloat, StrictFiniteFloat]] | None, default = None
        Exchange reference
    dispcontr: list[tuple[StrictFiniteFloat, StrictFiniteFloat]] | None, default = None
        Strong Pair Dispersion contribution
    dispweak: list[tuple[StrictFiniteFloat, StrictFiniteFloat]] | None, default = None
        Dispersion Weak pairs
    sumnondisstrong: StrictFiniteFloat | None, default = None
        Sum of non dispersive correlation strong pairs
    sumnondisweak: StrictFiniteFloat | None, default = None
        Sum of non dispersive correlation weak pairs
    """

    numoffragments: StrictPositiveInt | None = None
    electrostref: list[list[StrictFiniteFloat]] | None = None
    exchangeref: list[list[StrictFiniteFloat]] | None = None
    dispcontr: list[list[StrictFiniteFloat]] | None = None
    dispweak: list[list[StrictFiniteFloat]] | None = None
    sumnondisstrong: StrictFiniteFloat | None = None
    sumnondisweak: StrictFiniteFloat | None = None
    corrint: list[list[StrictFiniteFloat]] | None = None
    refint: list[list[StrictFiniteFloat]] | None = None
    totint: list[list[StrictFiniteFloat]] | None = None
