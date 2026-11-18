from pydantic import Field, StrictFloat, StrictStr

from opi.output.models.base.get_item import GetItem

SHELL_LETTERS = "spdfghiklmn"
"""
Letters of the angular momenta l = 0, 1, ..., 10 as used for shells in the gbw data, i.e., the
letter of angular momentum l is `SHELL_LETTERS[l]`. ORCA skips "j" and supports up to l = 10.
"""


class Base(GetItem):
    """
    Contains the information about the base of the atoms

    Attributes
    ----------
    coefficients: list[StrictFloat]
        Coefficients of the basis functions
    exponents: list[StrictFloat]
        Exponents of the Basis functions
    shell: StrictStr
        Shell of the Basis set
    """

    coefficients: list[StrictFloat] | None = Field(default=None, serialization_alias="Coefficients")
    exponents: list[StrictFloat] | None = Field(default=None, serialization_alias="Exponents")
    shell: StrictStr | None = Field(default=None, serialization_alias="Shell")
