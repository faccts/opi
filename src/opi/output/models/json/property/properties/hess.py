from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import StrictFiniteFloat


class Hessian(GetItem):
    """
    Contains the information about the Hessian matrix and vibration Mods.

    Attributes
    ----------
    hessian: list[list[list[StrictFloat]]] | None, default = None
        Hessian-Matrix for the molecule
    modes: list[list[list[StrictFloat]]] | None, default = None
        Vibration-modes
    """

    hessian: list[list[StrictFiniteFloat]] | None = None
    modes: list[list[StrictFiniteFloat]] | None = None
