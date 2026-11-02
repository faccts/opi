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
    xy: list[list[StrictFiniteFloat]]
        AO basis amplitudes for rpa/td-dft, shaped (active occupied x virtual)
    """

    iroot: StrictInt | None = Field(default=None, serialization_alias="IRoot")
    orbwin: list[StrictPositiveInt] | None = Field(default=None, serialization_alias="OrbWin")
    x: list[list[StrictFiniteFloat]] | None = Field(default=None, serialization_alias="X")
    xy: list[list[StrictFiniteFloat]] | None = Field(
        default=None, alias="x+y", serialization_alias="X+Y"
    )

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

    @field_validator("xy", mode="before")
    @classmethod
    def xy_init(cls, xy: list[float | list[float]]) -> list[list[float]]:
        """Normalize x+y to the 2-D array ORCA writes (#300).

        Parameters
        ----------
        xy
        """
        if xy and not isinstance(xy[0], list):
            # a flat payload is a single row, not one row per amplitude
            return [xy]
        return xy
