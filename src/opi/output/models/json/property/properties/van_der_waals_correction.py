from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import StrictFiniteFloat


class VdwCorrection(GetItem):
    """
    This class contains the VDW-correction for DFT-Calculation

    Attributes
    ----------
    vdw: StrictFiniteFloat | None, default = None
        Used correction for the VDW effect
    vdw_atomic: list[list[StrictFiniteFloat]] | None, default = None
        atomic decomposition of London dispersion energy (ADLD)
    """

    vdw: StrictFiniteFloat | None = None
    vdw_atomic: list[list[StrictFiniteFloat]] | None = None
