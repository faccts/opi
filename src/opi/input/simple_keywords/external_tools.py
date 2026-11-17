from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

# > Name of API to be imported
__all__ = ("ExternalTools",)


class ExternalTools(SimpleKeywordBox):
    """Enum to store all simple keywords of type ExternalTools."""

    EXTOPT = ORCAKeyword("extopt")
    """ORCAKeyword: Use external energy/gradient."""
