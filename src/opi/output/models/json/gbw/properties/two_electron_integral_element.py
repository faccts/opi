from pydantic import StrictFloat

from opi.output.models.base.strict_types import StrictNonNegativeInt

TwoElectronIntegralElement = tuple[
    StrictNonNegativeInt,
    StrictNonNegativeInt,
    StrictNonNegativeInt,
    StrictNonNegativeInt,
    StrictFloat,
]
