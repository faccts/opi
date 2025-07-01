from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Method",)


class Method(SimpleKeywordBox):
    """Enum to store all simple keywords of type Method.

    Attributes
    ----------
    HF : SimpleKeyword
        Hartee-Fock
    HF_3C : SimpleKeyword
        3c methods, do not require dispersion correction or basis set
    """

    HF = SimpleKeyword("hf")
    HF_3C = SimpleKeyword("hf-3c")
