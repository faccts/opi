from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Avas",)


class Avas(SimpleKeywordBox):
    """Enum to store all simple keywords of type Avas."""

    AVAS_DOUBLE_D = ORCAKeyword("avas(double-d)")
    """ORCAKeyword: CASSCF initial guess."""
    AVAS_DOUBLE_DS = ORCAKeyword("avas(double-ds)")
    """ORCAKeyword: CASSCF initial guess."""
    AVAS_DOUBLE_F = ORCAKeyword("avas(double-f)")
    """ORCAKeyword: CASSCF initial guess."""
    AVAS_VALENCE_D = ORCAKeyword("avas(valence-d)")
    """ORCAKeyword: CASSCF initial guess."""
    AVAS_VALENCE_DS = ORCAKeyword("avas(valence-ds)")
    """ORCAKeyword: CASSCF initial guess."""
    AVAS_VALENCE_F = ORCAKeyword("avas(valence-f)")
    """ORCAKeyword: CASSCF initial guess."""
