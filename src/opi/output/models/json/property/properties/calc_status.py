from pydantic import StrictStr

from opi.output.models.base.get_item import GetItem


class CalculationStatus(GetItem):
    """
    Contains information about the calculation Status

    Attributes
    ----------
    progname: StrictStr | None, default = None
        Name of the program
    status: StrictStr | None, default = None
        gives the status of the Calculation, if it terminated normally or if it get stuck
    version: StrictStr | None, default = None
        gives the status of the Calculation, if it terminated normally or if it get stuck
    """

    progname: StrictStr | None = None
    status: StrictStr | None = None
    version: StrictStr | None = None
