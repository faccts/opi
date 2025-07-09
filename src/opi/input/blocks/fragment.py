import re
from typing import Annotated

from pydantic import BaseModel, Field, field_validator

from opi.input.blocks import IntGroup

__all__ = ("FragList", "Fragment", "Frags")


class FragList(IntGroup):
    """Class used to model the `rigidfrags`, `relaxfrags`, `relaxhfrags`, `ghostfrags`, `constrainfragments` attributes in `BlockGeom`"""

    def __str__(self) -> str:
        return f"{super().__str__()} end"


class Fragment(BaseModel):
    """
    Class to model the fragment for the `Frags` class

    Attributes
    ----------
    fragmentid: int
        ID of fragment
    atoms: IntGroup
        Group of atoms for fragment
    """

    fragmentid: Annotated[int, Field(gt=0)]
    atoms: IntGroup

    def __str__(self) -> str:
        return f"{self.fragmentid} {str(self.atoms)} end"

    @classmethod
    def from_string(cls, string: str) -> "Fragment":
        """
        Parameters
        ----------
        string : str
        """
        re_frag = re.compile(
            r"""
                \s*                             
                (?P<fragmentid>\d+)\s+                  # Fragment: int
                \{\s*
                (?P<atoms>
                    (?:\d+(?::\d+)?\s*)+                # Integer or range, repeated with optional spaces
                )\s*                                         
                                      
                """,
            re.VERBOSE,
        )

        res = re_frag.match(string)

        if not res:
            raise ValueError("String not valid")

        groups = res.groupdict()
        return cls(**groups)

    @field_validator("atoms", mode="before")
    @classmethod
    def atoms_init(cls, atoms: str | IntGroup) -> IntGroup:
        """
        Parameters
        ----------
        atoms : str | IntGroup
        """
        if isinstance(atoms, IntGroup):
            return atoms
        else:
            return IntGroup.init(atoms)


class Frags(BaseModel):
    """
    Class to model the `frags` attribute for `BlockGeom`

    Attributes
    ----------
    frags: list[`Fragment`]
        list of fragment definitions of type `Fragment`
    """

    frags: list[Fragment] = Field(default_factory=list, min_length=1)

    def __str__(self) -> str:
        s = "\n     " + "\n     ".join(str(c) for c in self.frags)
        return s
