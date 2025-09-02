from pydantic import StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import StrictFiniteFloat


class Coordinates(GetItem):
    """
    Contains the coordinates of the atoms of the molecule

    Attributes
    ----------
    type: StrictStr | None, default = None
        The type of the coordinates
    units: StrictStr | None, default = None
        The unit of the coordinates
    cartesians: list[tuple[StrictStr, StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]] | None, default = None
        Contains the name
    """

    type: StrictStr | None = None
    units: StrictStr | None = None
    cartesians: (
        list[tuple[StrictStr, StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]] | None
    ) = None
