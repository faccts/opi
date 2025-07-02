from typing import List, Literal

from pydantic import BaseModel, field_validator

from opi.input.blocks.base import Block, InputFilePath, InputString
from opi.input.blocks.fragment import Fragment, Frags

__all__ = ("FragDefinition", "BlockFrag")


class FragDefinition(Frags):
    """
    Class to model definition `attribute` in `BlockFrag`
    """

    def __str__(self) -> str:
        return super().__str__() + "\n    end"


class FragProc(BaseModel):
    """
    Class to model `fragproc` attribute in `BlockFrag`
    """

    flags: List[
        Literal[
            "extlib",
            "connectivity",
            "atomic",
            "functionalgroups",
            "coarsegrained",
            "notassigned",
            "backbone",
            "seqbackbone",
            "aabackbone",
            "aminoacids",
            "aasidechains",
            "aascfinegrained",
            "nabackbone",
            "nabbfinegrained",
            "seqnabackbone",
            "nucleoticacid",
            "nasidechains",
            "solvents",
            "water",
            "extend",
            "fusebyatoms",
            "delextlib",
            "delconnectivity",
            "delatomic",
            "delfunctionalgroups",
            "delcoarsegrained",
            "delbackbone",
            "delseqbackbone",
            "delaabackbone",
            "delaminoacids",
            "delaasidechains",
            "delaascfinegrained",
            "delnabackbone",
            "delnabbfinegrained",
            "delseqnabackbone",
            "delnucleoticacid",
            "delnasidechains",
            "delsolvents",
            "delwater",
        ]
    ]

    def __str__(self) -> str:
        return " ".join(self.flags)

    @classmethod
    def from_string(cls, inp: str) -> "FragProc":
        """
        Parameters
        ----------
        inp: str

        Returns
        -------
        FragProc
        """
        parts = [part.strip().lower() for part in inp.split(",")]
        return cls(flags=parts)


class BlockFrag(Block):
    """Class to model %frag block in ORCA"""

    _name: str = "frag"
    printlevel: int | None = None
    storefrags: bool | None = None
    dointerfragbonds: bool | None = None
    fragproc: FragProc | None = None
    usetopology: bool | None = None
    printinputflags: bool | None = None
    topolfile: InputFilePath | None = None
    definition: FragDefinition | None = None
    xyzfraglib: InputString | None = None

    @field_validator("definition", mode="before")
    @classmethod
    def frags_str(cls, strings: list[str] | str) -> Frags:
        """
        Parameters
        ----------
        strings : list[str] | str
        """
        try:
            if isinstance(strings, list):
                frags = [Fragment.from_string(s) for s in strings]
            else:
                frags = [Fragment.from_string(strings)]
        except Exception as e:
            raise ValueError(f"Failed to parse constraints: {e}")

        return FragDefinition(frags=frags)

    @field_validator("topolfile", mode="before")
    @classmethod
    def path_from_string(cls, path: str | InputFilePath) -> InputFilePath:
        """
        Parameters
        ----------
        path : str | InputFilePath
        """
        if isinstance(path, str):
            return InputFilePath.from_string(path)
        else:
            return path

    @field_validator("xyzfraglib", mode="before")
    @classmethod
    def init_inputstring(cls, string: str | InputString) -> InputString:
        """
        Parameters
        ----------
        string : str | InputString
        """
        if isinstance(string, str):
            return InputString(string=string.strip())
        else:
            return string

    @field_validator("fragproc", mode="before")
    @classmethod
    def init_fragproc(cls, inp: FragProc | str) -> FragProc:
        """
        Parameters
        ----------
        inp: FragProc | str

        Returns
        -------
        FragProc
        """
        if isinstance(inp, str):
            return FragProc.from_string(inp)
        else:
            return inp
