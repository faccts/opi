import re
from typing import Annotated, Literal

from pydantic import BaseModel, Field, model_validator

from opi.input.blocks.util import CaseInsensitiveLiteralModel

__all__ = ("Internal", "Internals")


class GeomWrapper(CaseInsensitiveLiteralModel):
    """
    Base class for all custom classes used for `BlockGeom`
    """

    mode: str
    atom1: Annotated[int, Field(ge=0)] | Literal["*"] | None = None
    atom2: Annotated[int, Field(ge=0)] | Literal["*"] | None = None
    atom3: Annotated[int, Field(ge=0)] | Literal["*"] | None = None
    atom4: Annotated[int, Field(ge=0)] | Literal["*"] | None = None

    def __str__(self) -> str:
        return f"{{ {' '.join(str(val) for key, val in self.__dict__.items() if val is not None)} }} end"

    def validate_mode(self, obj: "GeomWrapper") -> None:
        """
        This function validates whether the given data aligns with the mode selected by the user

        Parameters
        ----------
        obj : "GeomWrapper"
        """
        # Mode B requires atom1, atom2; atom3 and atom4 must be None
        if obj.mode == "B":
            if not (obj.atom1 is not None and obj.atom2 is not None) or any(
                x is not None for x in [obj.atom3, obj.atom4]
            ):
                raise ValueError("Wrong format for mode B")

        # Mode A requires atom1, atom2, atom3; atom4 must be None
        elif obj.mode == "A":
            if (
                not all(x is not None for x in [obj.atom1 and obj.atom2 and obj.atom3])
                or obj.atom4 is not None
            ):
                raise ValueError("Wrong format for mode A")

        # Mode D requires all atoms
        elif obj.mode == "D":
            if not all(
                x is not None for x in [obj.atom1 and obj.atom2 and obj.atom3 and obj.atom4]
            ):
                raise ValueError("Wrong format for mode D")


class GeomWrapperBox(BaseModel):
    """Class to model a collection of `GeomWrapper` objects"""

    def __str__(self) -> str:
        return f"{{ {' '.join(str(val) for key, val in self.__dict__.items() if val is not None)} }} end"


class Internal(GeomWrapper):
    """
    Class to model individual internal coordinates for `Internals` class

    Attributes
    -----------
    mode: {"A","B","D","I"}
        Define mode
    atom1: int
        Define first atom
    atom2: int
        Define second atom
    atom3: int
        Define third atom
    atom4: int
        Define fourth atom
    """

    mode: Literal["A", "B", "D", "I"]
    atom1: Annotated[int, Field(gt=0)]
    atom2: Annotated[int, Field(gt=0)]
    atom3: Annotated[int, Field(gt=0)] | None = None
    atom4: Annotated[int, Field(gt=0)] | None = None

    @model_validator(mode="after")
    def validate_attributes(self) -> "Internal":
        super().validate_mode(self)

        if self.mode == "I":
            if not (self.atom1 and self.atom2 and self.atom3 and self.atom4):
                raise ValueError("Wrong format for mode I")

        return self

    @classmethod
    def from_string(cls, string: str) -> "Internal":
        """
        Parameters
        ----------
        string : str
        """
        re_internal = re.compile(
            r"""
                \{?\s*                               # Optional opening brace with optional whitespace
                (?P<mode>[AaBbDdIi])\s+              # Mode: A, B, D or I (case insensitive)
                (?P<atom1>\d+)\s+                    # atom1: digit
                (?P<atom2>\d+)\s*                    # atom2: digit    
                (?P<atom3>\d+)?\s*                   # Optional atom3
                (?P<atom4>\d+)?\s*                   # Optional atom4
                }?                                   # Optional closing brace
                """,
            re.VERBOSE,
        )
        res = re_internal.match(string.upper())
        if not res:
            raise ValueError("String not valid")

        groups = res.groupdict()
        return cls(**groups)

    def __str__(self) -> str:
        return (
            f"{{ {' '.join(str(val) for key, val in self.__dict__.items() if val is not None)} }}"
        )


class Internals(GeomWrapperBox):
    """
    Class to model `internals`

    Attributes
    ----------
    internals: list[`Internal`]
        list of internal coordinate definitions of type `Internal`
    """

    internals: list[Internal]

    def __str__(self) -> str:
        s = "\n     " + "\n     ".join(str(c) for c in self.internals) + "\n    end"

        return s
