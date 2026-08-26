from pydantic import Field, StrictInt, StrictStr, field_validator

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
    energy: StrictFiniteFloat
        Excitation energy of `iroot` in Hartree
    irrep: StrictStr
        Irreducible representation of `iroot`
    multiplicity: StrictPositiveInt
        Multiplicity of `iroot`
    tda: StrictStr
        Whether the Tamm-Dancoff approximation was used ("ON" or "OFF")
    orbwin: list[StrictPositiveInt]
        Orbital Window
    x: list[list[StrictFiniteFloat]]
        AO basis amplitudes for cis/tda-td-dft
    xy: list[list[StrictFiniteFloat]]
        AO basis amplitudes X+Y for rpa/td-dft
    x_minus_y: list[list[StrictFiniteFloat]]
        AO basis amplitudes X-Y for rpa/td-dft
    """

    iroot: StrictInt | None = Field(default=None, serialization_alias="IRoot")
    energy: StrictFiniteFloat | None = Field(default=None, serialization_alias="Energy")
    irrep: StrictStr | None = Field(default=None, serialization_alias="Irrep")
    multiplicity: StrictPositiveInt | None = Field(default=None, serialization_alias="Multiplicity")
    tda: StrictStr | None = Field(default=None, serialization_alias="TDA")
    orbwin: list[StrictPositiveInt] | None = Field(default=None, serialization_alias="OrbWin")
    x: list[list[StrictFiniteFloat]] | None = Field(default=None, serialization_alias="X")
    xy: list[list[StrictFiniteFloat]] | None = Field(
        default=None, alias="x+y", serialization_alias="X+Y"
    )
    x_minus_y: list[list[StrictFiniteFloat]] | None = Field(
        default=None, alias="x-y", serialization_alias="X-Y"
    )

    @field_validator("x", "xy", "x_minus_y", mode="before")
    @classmethod
    def amplitudes_init(cls, amplitudes: list[float | list[float]]) -> list[list[float]]:
        """
        ORCA writes the amplitudes as a list of rows, but a row holding a single value is
        written as a plain number instead of a list. Those are wrapped here.

        Parameters
        ----------
        amplitudes
        """
        amplitudes_list = []
        for row in amplitudes:
            if isinstance(row, list):
                amplitudes_list.append(row)
            else:
                amplitudes_list.append([row])
        return amplitudes_list
