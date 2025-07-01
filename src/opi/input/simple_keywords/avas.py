from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Avas",)


class Avas(SimpleKeywordBox):
    """Enum to store all simple keywords of type Avas.

    Attributes
    ----------
    AVAS_DOUBLE_D : SimpleKeyword
        CASSCF initial guess
    AVAS_DOUBLE_DS : SimpleKeyword
        CASSCF initial guess
    AVAS_DOUBLE_F : SimpleKeyword
        CASSCF initial guess
    AVAS_VALENCE_D : SimpleKeyword
        CASSCF initial guess
    AVAS_VALENCE_DS : SimpleKeyword
        CASSCF initial guess
    AVAS_VALENCE_F : SimpleKeyword
        CASSCF initial guess
    """

    AVAS_DOUBLE_D = SimpleKeyword("avas(double-d)")
    AVAS_DOUBLE_DS = SimpleKeyword("avas(double-ds)")
    AVAS_DOUBLE_F = SimpleKeyword("avas(double-f)")
    AVAS_VALENCE_D = SimpleKeyword("avas(valence-d)")
    AVAS_VALENCE_DS = SimpleKeyword("avas(valence-ds)")
    AVAS_VALENCE_F = SimpleKeyword("avas(valence-f)")
