from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictNonNegativeFloat,
)


class CalculationTiming(GetItem):
    """
    Has the Information about the calculation Timing

    Attributes
    ----------
    gstep: StrictNonNegativeFloat | None, default = None
        Time of geometry steps
    gtoint: StrictNonNegativeFloat | None, default = None
        Time of integral generation
    prop: StrictNonNegativeFloat | None, default = None
        Time of property generation
    scf: StrictNonNegativeFloat | None, default = None
        Time of solving the SCF
    scfgrad: StrictNonNegativeFloat | None, default = None
        Time of gradient calculation
    sum: StrictNonNegativeFloat | None, default = None
        Total time of the calculation
    """

    gstep: StrictNonNegativeFloat | None = None
    gtoint: StrictNonNegativeFloat | None = None
    prop: StrictNonNegativeFloat | None = None
    scf: StrictNonNegativeFloat | None = None
    scfgrad: StrictNonNegativeFloat | None = None
    sum: StrictNonNegativeFloat | None = None
