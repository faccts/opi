from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictPositiveInt,
)


class MdciAdld(GetItem):
    """
    This class contains information about the atomic decomposition of
    London dispersion (ADLD).

    Attributes
    ----------
    numoffragments: StrictPositiveInt | None, default = None
        Number of fragments defined in the adld scheme
    adldcorratomic_loewdin: list[list[StrictFiniteFloat]] | None, default = None
        atomic correlation contributions based on Loewdin populations
    adldcorrfrag_loewdin: list[list[StrictFiniteFloat]] | None, default = None
        fragment correlation contributions based on Loewdin populations
    adlddispatomic_loewdin: list[list[StrictFiniteFloat]] | None, default = None
        atomic dispersion contributions based on Loewdin populations
    adlddispfrag_loewdin: list[list[StrictFiniteFloat]] | None, default = None
        fragment dispersion contributions based on Loewdin populations
    adldcorratomic_mulliken: list[list[StrictFiniteFloat]] | None, default = None
        atomic correlation contributions based on Mulliken populations
    adldcorrfrag_mulliken: list[list[StrictFiniteFloat]] | None, default = None
        fragment correlation contributions based on Mulliken populations
    adlddispatomic_mulliken: list[list[StrictFiniteFloat]] | None, default = None
        atomic dispersion contributions based on Mulliken populations
    adlddispfrag_mulliken: list[list[StrictFiniteFloat]] | None, default = None
        atomic dispersion contributions based on Mulliken populations
    """

    numoffragments: StrictPositiveInt | None = None
    adldcorratomic_loewdin: list[list[StrictFiniteFloat]] | None = None
    adldcorrfrag_loewdin: list[list[StrictFiniteFloat]] | None = None
    adlddispatomic_loewdin: list[list[StrictFiniteFloat]] | None = None
    adlddispfrag_loewdin: list[list[StrictFiniteFloat]] | None = None
    adldcorratomic_mulliken: list[list[StrictFiniteFloat]] | None = None
    adldcorrfrag_mulliken: list[list[StrictFiniteFloat]] | None = None
    adlddispatomic_mulliken: list[list[StrictFiniteFloat]] | None = None
    adlddispfrag_mulliken: list[list[StrictFiniteFloat]] | None = None
