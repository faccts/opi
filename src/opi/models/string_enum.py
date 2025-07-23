from enum import StrEnum
from typing import Self

__all__ = [
    "StringEnum",
]


class StringEnum(StrEnum):
    """
    Variant of StrEnum that allows case-insensitive conversion of a plain string into the corresponding Enum member.
    """

    @classmethod
    def _missing_(cls, value: object, /) -> Self:
        """
        Raises
        ------
        TypeError: If input value cannot be cast to string.
        ValueError: If input value is not part of the Enum.
        """
        value_org = value
        try:
            # > Any value that can be cast into a string is supported.
            value = str(value)
        except (TypeError, ValueError):
            raise TypeError(f"Value {value} cannot be converted to {cls.__name__}")

        # > Case-fold value
        value = value.casefold()

        for member in cls:
            if member.value.casefold() == value:
                return member
        # > No suitable member found
        raise ValueError(f"Unknown Enum member: {value_org}")
