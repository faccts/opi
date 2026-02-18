from pydantic import Field, StrictInt, field_validator

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictPositiveInt,
)


class TdDft(GetItem):
    """
    This class contains the information about the TD-DFT

    Attributes
    ----------
    iroot: StrictInt
        The root to be optimized
    orbwin: list[StrictPositiveInt]
        Orbital Window
    x: StrictNonNegativeFloat
        AO basis amplitudes for cis/tda-td-dft
    xy: StrictNonNegativeFloat
        AO basis amplitudes for rpa/td-dft
    """

    iroot: StrictInt | None = None
    orbwin: list[StrictPositiveInt] | None = None
    x: list[list[StrictFiniteFloat]] | None = None
    xy: list[StrictFiniteFloat] | None = Field(default=None, alias="x+y")

    @field_validator("x", mode="before")
    @classmethod
    def x_init(cls, x: list[float | list[float]]) -> list[list[float]]:
        """
        Parameters
        ----------
        x
        """
        x_list = []
        for x_i in x:
            if isinstance(x_i, list):
                x_list.append(x_i)
            else:
                x_list.append([x_i])
        return x_list
