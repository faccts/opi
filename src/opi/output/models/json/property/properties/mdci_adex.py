from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictPositiveInt,
)


class MdciAdex(GetItem):
    """
    This class contains information about the atomic decomposition of
    exchange (ADEX).

    Attributes
    ----------
    numoffragments: StrictPositiveInt | None, default = None
        Number of fragments defined in the adex scheme
    adexatomic_loewdin: list[list[StrictFiniteFloat]] | None, default = None
        atomic exchange contributions based on Loewdin populations
    adexfrag_loewdin: list[list[StrictFiniteFloat]] | None, default = None
        fragment exchange contributions based on Loewdin populations
    adexatomic_mulliken: list[list[StrictFiniteFloat]] | None, default = None
        atomic exchange contributions based on Mulliken populations
    adexfrag_mulliken: list[list[StrictFiniteFloat]] | None, default = None
        fragment exchange contributions based on Mulliken populations
    """

    numoffragments: StrictPositiveInt | None = None
    adexatomic_loewdin: list[list[StrictFiniteFloat]] | None = None
    adexfrag_loewdin: list[list[StrictFiniteFloat]] | None = None
    adexatomic_mulliken: list[list[StrictFiniteFloat]] | None = None
    adexfrag_mulliken: list[list[StrictFiniteFloat]] | None = None
