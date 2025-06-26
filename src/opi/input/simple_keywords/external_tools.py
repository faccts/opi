from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

# > Name of API to be imported
__all__ = ("ExternalTools",)


class ExternalTools(SimpleKeywordBox):
    """Enum to store all simple keywords of type ExternalTools"""

    EXTOPT = SimpleKeyword("extopt")  # Use external energy/gradient