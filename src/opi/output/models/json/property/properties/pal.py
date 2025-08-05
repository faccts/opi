from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import StrictPositiveInt


class PalFlags(GetItem):
    """
    This class contains the information about the PAL flags

    Attributes
    ----------
    diskflag: StrictPositiveInt | None, default = None
        Number of Disk-Flag set
    """

    diskflag: StrictPositiveInt | None = None
