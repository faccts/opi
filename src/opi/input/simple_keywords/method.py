from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Method",)


class Method(SimpleKeywordBox):
    """Enum to store all simple keywords of type Method."""

    HF = SimpleKeyword("hf")
    """SimpleKeyword: Hartee-Fock."""
    HF_3C = SimpleKeyword("hf-3c")
    """SimpleKeyword: 3c methods, do not require dispersion correction or basis set."""
