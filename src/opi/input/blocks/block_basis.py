import re

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from opi.input.blocks.base import Block, InputFilePath
from opi.input.simple_keywords import (
    SimpleKeyword,
)
from opi.utils.element import Element

__all__ = (
    "NewBasis",
    "FragBasis",
    "FragAux",
    "FragEcp",
    "FragCabs",
    "FragAuxJ",
    "FragAuxJK",
    "FragAuxC",
    "BlockBasis",
)


class NewBasis(BaseModel):
    """
    Class to model `newauxgto`, `addauxgto`,`newauxjgto`,`addauxjgto`,`newauxcgto`,`addauxcgto`,`newauxxgto`,`addauxxgto` attributes in `BlockBasis`.

    Attributes
    -----------
    element: `Element`
        Element for which basis is defined
    basis: `SimpleKeyword`
        Basis set keyword to be defined

    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    element: Element
    basis: SimpleKeyword

    def __str__(self) -> str:
        return f'{str(self.element)} "{self.basis.format_orca()}" end'


class FragBasis(BaseModel):
    """
    Class to model `fragbasis` attribute in `BlockBasis`.
    Also base class for `FragAux`, `FragAuxJ`, `FragAuxJK`, `FragAuxC`, `FragCabs`, `FragEcp`.

    Attributes
    ----------
    frag : dict[int, SimpleKeyword]
        A dictionary mapping atomic indices to basis set keywords.
    name: str
        Used to identify the class for the ORCA input

    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    frag: dict[int, SimpleKeyword]
    name: str = "fragbasis"

    @field_validator("frag")
    @classmethod
    def check_fragments(cls, values: dict[int, SimpleKeyword]) -> dict[int, SimpleKeyword]:
        """
        Parameters
        ----------
        values : dict[int | SimpleKeyword]
        """
        if any(k <= 0 for k in values.keys()):
            raise ValueError("All integers must be positive")

        return values

    def __str__(self) -> str:
        s = ""
        s += f'{list(self.frag.keys())[0]} "{list(self.frag.values())[0]}" '
        for key, value in list(self.frag.items())[1:]:
            s += f'\n    {self.name} {key} "{value}" '

        return s

    @classmethod
    def from_string(cls, inp: str) -> "FragBasis":
        """
        Parameters
        ----------
        inp : str

        Returns
        --------
        FragBasis
        """
        re_fragbasis = re.compile(
            r"""
                    \s*
                    (?P<frag>
                        (?:
                        \s*(\d+)\s+(\w+)\s*
                        (?:\n)?(?:,)?
                        )+
                    )
            """,
            re.VERBOSE,
        )

        res = re_fragbasis.match(inp.lower())
        if not res:
            raise ValueError("String not valid")
        frag = res.group("frag")
        inner_pattern = re.compile(r"\s*(\d+)\s+([\w]+)\s*(?:\n)?(?:,)?")
        pairs = inner_pattern.findall(frag)

        # Build dict[int, str]
        frag_dict = {int(k): v.strip() for k, v in pairs}
        for v in frag_dict:
            frag_dict[v] = SimpleKeyword(frag_dict[v])

        return cls(frag=frag_dict)


class FragAux(FragBasis):
    """
    Class to model `fragaux` attribute in `BlockBasis`
    """

    name: str = "fragaux"


class FragAuxJ(FragBasis):
    """
    Class to model `fragauxj` attribute in `BlockBasis`
    """

    name: str = "fragauxj"


class FragAuxJK(FragBasis):
    """
    Class to model `fragauxjk` attribute in `BlockBasis`
    """

    name: str = "fragauxjk"


class FragAuxC(FragBasis):
    """
    Class to model `fragauxc` attribute in `BlockBasis`
    """

    name: str = "fragauxc"


class FragCabs(FragBasis):
    """
    Class to model `fragcabs` attribute in `BlockBasis`
    """

    name: str = "fragcabs"


class FragEcp(FragBasis):
    """
    Class to model `fragecp` attribute in `BlockBasis'
    """

    name: str = "fragecp"


class BlockBasis(Block):
    """Class to model %basis block in ORCA"""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    _name: str = "basis"
    decontract: bool | None = None  # do decontract all basis sets
    uncontract: bool | None = None  # do not decontract all basis sets
    decontractbas: bool | None = None  # do decontract the orbital basis set
    uncontractbas: bool | None = None  # do not decontract the orbital basis set
    decontractaux: bool | None = None  # do decontract the aux basis set
    uncontractaux: bool | None = None  # do not decontract the aux basis set
    decontractauxj: bool | None = None  # do decontract the aux basis set
    uncontractauxj: bool | None = None  # do not decontract the aux basis set
    decontractauxc: bool | None = None  # do decontract the aux basis set
    uncontractauxc: bool | None = None  # do not decontract the aux basis set
    decontractauxx: bool | None = None  # do decontract the aux basis set
    uncontractauxx: bool | None = None  # do not decontract the aux basis set
    decontractauxjk: bool | None = None  # do decontract the aux basis set
    uncontractauxjk: bool | None = None  # do not decontract the aux basis set
    decontractcabs: bool | None = None  # do decontract the aux basis set
    uncontractcabs: bool | None = None  # do not decontract the aux basis set
    anobasis: bool | None = None  # Is an ano basis?
    prune: bool | None = None  # remove linear dependencies
    trimautoaux: bool | None = None  # trim auto aux
    pcdtrimbas: int | None = (
        None  # Trim thWe basis set with pivoted cholesky decomposition. Example: PCDTrimBas Overlap or  PCDTrimBas Coulomb
    )
    pcdtrimauxj: int | None = (
        None  # Trim the basis set with pivoted cholesky decomposition. Example: PCDTrimBas Overlap or  PCDTrimBas Coulomb
    )
    pcdtrimauxjk: int | None = (
        None  # Trim the basis set with pivoted cholesky decomposition. Example: PCDTrimBas Overlap or  PCDTrimBas Coulomb
    )
    pcdtrimauxc: int | None = (
        None  # Trim the basis set with pivoted cholesky decomposition. Example: PCDTrimBas Overlap or  PCDTrimBas Coulomb
    )
    pcdtrimauxx: int | None = (
        None  # Trim the basis set with pivoted cholesky decomposition. Example: PCDTrimBas Overlap or  PCDTrimBas Coulomb
    )
    pcdtrimcabs: int | None = (
        None  # Trim the basis set with pivoted cholesky decomposition. Example: PCDTrimBas Overlap or  PCDTrimBas Coulomb
    )
    pcdthresh: float | None = None  # threshold for pcdtrim, chosen automatically if <0
    pcdtrimkeepunique: bool | None = (
        None  # whether to make sure basis sets stay the same over unique groups of atoms
    )
    allowghostecp: bool | None = None  # allow ecps for for ghostatoms
    basis: SimpleKeyword | None = None
    auxj: SimpleKeyword | None = None
    gtoaux: SimpleKeyword | None = None
    auxbasis: SimpleKeyword | None = None
    aux: SimpleKeyword | None = None
    auxc: SimpleKeyword | None = None  # **
    auxx: SimpleKeyword | None = None  # **
    ecp: SimpleKeyword | None = None
    auxjk: SimpleKeyword | None = None
    cabs: SimpleKeyword | None = None
    gtocabs: SimpleKeyword | None = None
    cabsbasis: SimpleKeyword | None = None
    gtoname: InputFilePath | None = None
    gtoauxname: InputFilePath | None = None
    gtoauxjname: InputFilePath | None = None
    gtoauxcname: InputFilePath | None = None
    gtoauxxname: InputFilePath | None = None
    gtoauxjkname: InputFilePath | None = None
    gtocabsname: InputFilePath | None = None
    newgto: NewBasis | None = None
    addgto: NewBasis | None = None
    newauxgto: NewBasis | None = None
    addauxgto: NewBasis | None = None
    newauxjgto: NewBasis | None = None
    addauxjgto: NewBasis | None = None
    newauxcgto: NewBasis | None = None
    addauxcgto: NewBasis | None = None
    newauxxgto: NewBasis | None = None
    addauxxgto: NewBasis | None = None
    newauxjkgto: NewBasis | None = None
    addauxjkgto: NewBasis | None = None
    fragbasis: FragBasis | None = None
    fragaux: FragAux | None = None
    fragauxj: FragAuxJ | None = None
    fragauxc: FragAuxC | None = None
    fragauxjk: FragAuxJK | None = None
    fragcabs: FragCabs | None = None
    fragecp: FragEcp | None = None
    readfragbasis: InputFilePath | None = None
    readfragaux: InputFilePath | None = None
    readfragauxj: InputFilePath | None = None
    readfragauxc: InputFilePath | None = None
    readfragauxjk: InputFilePath | None = None
    readfragcabs: InputFilePath | None = None
    readfragecp: InputFilePath | None = None
    newecp: NewBasis | None = None
    delecp: Element | None = None

    @field_validator(
        "readfragbasis",
        "readfragaux",
        "readfragauxj",
        "readfragauxc",
        "readfragauxjk",
        "readfragcabs",
        "readfragecp",
        "gtoname",
        "gtoauxname",
        "gtoauxjname",
        "gtoauxcname",
        "gtoauxxname",
        "gtoauxjkname",
        "gtocabsname",
        mode="before",
    )
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

    @field_validator(
        "fragbasis",
        "fragaux",
        "fragauxj",
        "fragauxjk",
        "fragauxc",
        "fragcabs",
        "fragecp",
        mode="before",
    )
    @classmethod
    def frag_fromstring(cls, inp: str | FragBasis, info: FieldValidationInfo) -> FragBasis:
        """

        Parameters
        ----------
        inp: str | FragBasis
        info: FieldValidationInfo

        Returns
        -------
        FragBasis

        """
        if isinstance(inp, str):
            field_to_class = {
                "fragbasis": FragBasis,
                "fragaux": FragAux,
                "fragauxj": FragAuxJ,
                "fragauxjk": FragAuxJK,
                "fragauxc": FragAuxC,
                "fragcabs": FragCabs,
                "fragecp": FragEcp,
            }

            field_name: str = info.field_name  # type: ignore
            if field_name is None:
                raise ValueError("Field name not found")
            frag_class = field_to_class.get(field_name)

            if not frag_class:
                raise TypeError(f"No FragBasis subclass for '{field_name}'")

            return frag_class.from_string(inp)

        else:
            return inp
