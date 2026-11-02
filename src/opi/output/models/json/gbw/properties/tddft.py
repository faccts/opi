from pydantic import Field, StrictInt, field_validator

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeInt,
)


class TdDft(GetItem):
    """
    This class contains the information about the TD-DFT

    Attributes
    ----------
    iroot: StrictInt
        The root to be optimized
    orbwin: list[StrictNonNegativeInt]
        Orbital Window
    x: list[list[StrictFiniteFloat]]
        Amplitudes for cis/tda-td-dft (active occupied x virtual)
    xy: list[list[StrictFiniteFloat]]
        X+Y amplitudes for rpa/td-dft (active occupied x virtual)
    """

    iroot: StrictInt | None = Field(default=None, serialization_alias="IRoot")
    orbwin: list[StrictNonNegativeInt] | None = Field(default=None, serialization_alias="OrbWin")
    x: list[list[StrictFiniteFloat]] | None = Field(default=None, serialization_alias="X")
    xy: list[list[StrictFiniteFloat]] | None = Field(
        default=None, alias="x+y", serialization_alias="X+Y"
    )

    @field_validator("x", "xy", mode="before")
    @classmethod
    def amplitudes_init(
        cls, amplitudes: list[float | list[float]] | None
    ) -> list[list[float]] | None:
        """
        Wrap scalar rows into single-element lists, so that the amplitudes are always 2D.

        Parameters
        ----------
        amplitudes: list[float | list[float]] | None
            Amplitudes as written by ORCA
        """
        if amplitudes is None:
            return None
        return [row if isinstance(row, list) else [row] for row in amplitudes]
