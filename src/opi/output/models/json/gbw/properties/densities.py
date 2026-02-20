from pydantic import StrictFloat

from opi.output.models.base.get_item import GetItem


class Densities(GetItem):
    """
    This class contains the information about the Densities.

    Attributes
    ----------
    scfp: list[list[StrictFloat]]
        Density matrix from SCF.
    """

    scfp: list[list[StrictFloat]]
