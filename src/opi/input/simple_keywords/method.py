from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Method",)


class Method(SimpleKeywordBox):
    """Enum to store all simple keywords of type Method."""

    HF = ORCAKeyword("hf")
    """ORCAKeyword: Hartee-Fock."""
    HF_3C = ORCAKeyword("hf-3c")
    """ORCAKeyword: 3c methods, do not require dispersion correction or basis set."""
