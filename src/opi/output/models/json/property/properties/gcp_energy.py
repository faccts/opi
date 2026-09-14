from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import StrictFiniteFloat


class GcpEnergy(GetItem):
    """
    This class contains the geometrical counterpoise (gCP) correction and related
    short-range basis set corrections.

    Attributes
    ----------
    gcp_energy: StrictFiniteFloat | None, default = None
        Energy of the geometrical counterpoise correction. ORCA reports the plain gCP correction
        (e.g. r2SCAN-3c), the combined gCP+basis set correction (e.g. HF-3c) and the short-range
        basis (SRB) correction (e.g. B97-3c) in this field.
    """

    gcp_energy: StrictFiniteFloat | None = None
