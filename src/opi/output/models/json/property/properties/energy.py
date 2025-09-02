from pydantic import StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictPositiveInt,
)


class Energy(GetItem):
    """
    Base class for energies that were calculated in the ORCA job

    Attributes
    ----------
    method: StrictStr | None, default = None
        String that identifies the method that was used for the energy calculation.
        Is used for discriminating different energy types
    mult: list[list[StrictPositiveInt]] | None, default = None
        List of electronic multiplicities
    totalenergy: list[list[StrictFiniteFloat]] | None, default = None
        The total calculated Energy
    """

    method: StrictStr | None = None
    mult: list[list[StrictPositiveInt]] | None = None
    totalenergy: list[list[StrictFiniteFloat]] | None = None
