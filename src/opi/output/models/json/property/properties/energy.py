from pydantic import StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictPositiveInt,
)


def first_energy(
    values: list[list[StrictFiniteFloat]] | None,
) -> StrictFiniteFloat | None:
    """
    Unpack an energy that ORCA stores as a nested list holding a single element.

    Parameters
    ----------
    values : list[list[StrictFiniteFloat]] | None
        Energy as it is stored in the JSON output.

    Returns
    -------
    StrictFiniteFloat | None
        The energy as a plain float or None if `values` holds no energy.
    """
    if not values or not values[0]:
        return None
    return values[0][0]


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

    @property
    def energy(self) -> StrictFiniteFloat | None:
        """
        The total energy in Eh as a plain float.

        Shortcut for `totalenergy[0][0]`, as ORCA stores single energies as a nested list holding a
        single element. None if the output contains no total energy.
        """
        return first_energy(self.totalenergy)
