from pydantic import StrictFloat

from opi.output.models.base.get_item import GetItem


class Densities(GetItem):
    """
    This class contains the information about the Densities.

    Attributes
    ----------
    scfp: list[list[StrictFloat]]
        Density matrix from SCF.
    scfr: list[list[StrictFloat]]
        Spin-density matrix from SCF. (P_alpha - P_beta)
    """

    scfp: list[list[StrictFloat]] | None = None
    scfr: list[list[StrictFloat]] | None = None
