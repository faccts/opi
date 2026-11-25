from pydantic import Field, StrictInt, StrictStr, field_validator

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeInt,
    StrictPositiveInt,
)


class TdDft(GetItem):
    """
    This class contains the information about the TD-DFT

    Attributes
    ----------
    iroot: StrictInt
        The root to be optimized
    energy: StrictFiniteFloat
        Excitation energy of `iroot` in Hartree
    irrep: StrictStr
        Irreducible representation of `iroot`
    multiplicity: StrictPositiveInt
        Multiplicity of `iroot`
    tda: StrictStr
        Whether the Tamm-Dancoff approximation was used ("ON" or "OFF")
    orbwin: list[StrictNonNegativeInt]
        Orbital Window
    x: list[list[StrictFiniteFloat]]
        Amplitudes for cis/tda-td-dft (active occupied x virtual)
    xy: list[list[StrictFiniteFloat]]
        X+Y amplitudes for rpa/td-dft (active occupied x virtual)
    x_minus_y: list[list[StrictFiniteFloat]]
        X-Y amplitudes for rpa/td-dft (active occupied x virtual)
    """

    iroot: StrictInt | None = Field(default=None, serialization_alias="IRoot")
    energy: StrictFiniteFloat | None = Field(default=None, serialization_alias="Energy")
    irrep: StrictStr | None = Field(default=None, serialization_alias="Irrep")
    multiplicity: StrictPositiveInt | None = Field(default=None, serialization_alias="Multiplicity")
    tda: StrictStr | None = Field(default=None, serialization_alias="TDA")
    orbwin: list[StrictNonNegativeInt] | None = Field(default=None, serialization_alias="OrbWin")
    x: list[list[StrictFiniteFloat]] | None = Field(default=None, serialization_alias="X")
    xy: list[list[StrictFiniteFloat]] | None = Field(
        default=None, alias="x+y", serialization_alias="X+Y"
    )
    x_minus_y: list[list[StrictFiniteFloat]] | None = Field(
        default=None, alias="x-y", serialization_alias="X-Y"
    )

    @field_validator("x", "xy", "x_minus_y", mode="before")
    @classmethod
    def amplitudes_init(
        cls, amplitudes: list[float | list[float]] | None
    ) -> list[list[float]] | None:
        """
        ORCA writes the amplitudes as a list of rows, but a row holding a single value is
        written as a plain number instead of a list. Those are wrapped here, so that the
        amplitudes are always 2D.

        Parameters
        ----------
        amplitudes: list[float | list[float]] | None
            Amplitudes as written by ORCA
        """
        if amplitudes is None:
            return None
        return [row if isinstance(row, list) else [row] for row in amplitudes]
