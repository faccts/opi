from opi.output.models.base.get_item import GetItem
from opi.output.models.json.property.properties.calc_info import CalcInfo
from opi.output.models.json.property.properties.calc_status import (
    CalculationStatus,
)
from opi.output.models.json.property.properties.calc_time import (
    CalculationTiming,
)
from opi.output.models.json.property.properties.geometries import Geometries
from opi.output.models.json.property.properties.pal import PalFlags


class PropertyResults(GetItem):
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
    pal_flags: PalFlags default = None
        Contains information about the parallel Jobs used in the calculation
    """

    calculation_info: CalcInfo | None = None
    calculation_status: CalculationStatus | None = None
    calculation_timings: CalculationTiming | None = None
    pal_flags: PalFlags | None = None
    geometries: list[Geometries] | None = None
