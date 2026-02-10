from opi.output.models.json.property.properties.calc_info import CalcInfo
from opi.output.models.json.property.properties.calc_status import (
    CalculationStatus,
)
from opi.output.models.json.property.properties.calc_time import (
    CalculationTiming,
)
from opi.output.models.json.property.properties.geometries import Geometries
from opi.output.models.json_loadable import JSONLoadable


class PropertyResults(JSONLoadable):
    """
    Has all the information calculated in the ORCA job

    Attributes
    ----------
    calculation_info: CalcInfo
        contains general information about the calculation
    calculation_status: CalculationStatus
        contains information about the Status of the calculation
    calculation_timings : CalculationTiming
        contains timings of the calculation
    """

    calculation_info: CalcInfo | None = None
    calculation_status: CalculationStatus | None = None
    calculation_timings: CalculationTiming | None = None
    geometries: list[Geometries] | None = None
