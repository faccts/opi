from typing import Any

from pydantic import field_validator

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
    mdci: StrictNonNegativeFloat | None = None
        Time spend in the MDCI modulen
    prop: StrictNonNegativeFloat | None, default = None
        Time of property generation
    propint: StrictNonNegativeFloat | None, default = None
        Time to evaluate property integrals
    scf: StrictNonNegativeFloat | None, default = None
        Time of solving the SCF
    scfgrad: StrictNonNegativeFloat | None, default = None
        Time of gradient calculation
    sum: StrictNonNegativeFloat | None, default = None
        Total time of the calculation
    """

    gstep: StrictNonNegativeFloat | None = None
    gtoint: StrictNonNegativeFloat | None = None
    mdci: StrictNonNegativeFloat | None = None
    prop: StrictNonNegativeFloat | None = None
    propint: StrictNonNegativeFloat | None = None
    scf: StrictNonNegativeFloat | None = None
    scfgrad: StrictNonNegativeFloat | None = None
    sum: StrictNonNegativeFloat | None = None

    @field_validator("*", mode="before")
    @classmethod
    def _clamp_negative_timings(cls, value: Any) -> Any:
        """
        Clamp negative timings to zero.

        ORCA can report slightly negative timings due to timer resolution, which would
        otherwise fail the non-negative validation of the fields.
        """
        if isinstance(value, float) and value < 0:
            return 0.0
        return value
