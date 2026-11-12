import math
import re
from textwrap import indent
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo

from opi.input.blocks import BlockABC
from opi.input.blocks.util import InputFilePath
from opi.input.simple_keywords import (
    ORCAKeyword,
)
from opi.utils.element import Element

__all__ = (
    "BasisShell",
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


# > Indentation of the options of a block, as written by `BlockABC.format_orca()`
_BLOCK_INDENT = "    "
# > Indentation of nested lines relative to their parent line
_NESTED_INDENT = "  "


class BasisShell(BaseModel):
    """
    Class to model a contracted shell of basis functions given explicitly in `NewBasis`.

    Attributes
    ----------
    angmom: Literal["s", "p", "d", "f", "g", "h", "i"]
        Angular momentum of the shell
    primitives: list[tuple[float, float]]
        Exponent and contraction coefficient of each primitive Gaussian

    Examples
    --------
    >>> print(BasisShell(angmom="g", primitives=[(0.4203, 1.0)]))
    G 1
      1 0.4203 1.0
    """

    angmom: Literal["s", "p", "d", "f", "g", "h", "i"]
    primitives: list[tuple[float, float]]

    @field_validator("angmom", mode="before")
    @classmethod
    def lowercase_angmom(cls, value: object) -> object:
        """
        ORCA prints the angular momentum in uppercase, so both cases are accepted.

        Parameters
        ----------
        value : object
        """
        return value.lower() if isinstance(value, str) else value

    @field_validator("primitives")
    @classmethod
    def check_primitives(cls, values: list[tuple[float, float]]) -> list[tuple[float, float]]:
        """
        Parameters
        ----------
        values : list[tuple[float, float]]
        """
        if not values:
            raise ValueError("A shell needs at least one primitive")
        for exponent, coefficient in values:
            if not (math.isfinite(exponent) and exponent > 0):
                raise ValueError("All exponents must be positive and finite")
            if not math.isfinite(coefficient):
                raise ValueError("All contraction coefficients must be finite")
        return values

    def __str__(self) -> str:
        lines = [f"{self.angmom.upper()} {len(self.primitives)}"]
        lines += [
            f"{_NESTED_INDENT}{i} {exponent} {coefficient}"
            for i, (exponent, coefficient) in enumerate(self.primitives, start=1)
        ]
        return "\n".join(lines)


class NewBasis(BaseModel):
    """
    Class to model `newgto`, `addgto`, `newauxgto`, `addauxgto`, `newauxjgto`, `addauxjgto`,
    `newauxcgto`, `addauxcgto`, `newauxxgto`, `addauxxgto`, `newauxjkgto`, `addauxjkgto`, and
    `newecp` attributes in `BlockBasis`.

    The basis is either a basis set keyword or, except for `newecp`, a list of explicit shells.

    Attributes
    -----------
    element: `Element`
        Element for which basis is defined
    basis: `ORCAKeyword` | None, default: None
        Basis set keyword to be defined
    shells: list[BasisShell] | None, default: None
        Explicit shells to be defined, in the given order

    Examples
    --------
    Add a g shell to the basis set of bismuth:

    >>> BlockBasis(
    ...     addgto=NewBasis(
    ...         element=Element.BISMUTH, shells=[BasisShell(angmom="g", primitives=[(0.4203, 1.0)])]
    ...     )
    ... )
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    element: Element
    basis: ORCAKeyword | None = None
    shells: list[BasisShell] | None = None

    @model_validator(mode="after")
    def check_basis_or_shells(self) -> Self:
        if (self.basis is None) == (self.shells is None):
            raise ValueError("Exactly one of `basis` and `shells` must be given")
        if self.shells is not None and not self.shells:
            raise ValueError("`shells` must not be empty")
        return self

    def __str__(self) -> str:
        if self.basis is not None:
            return f'{str(self.element)} "{self.basis.format_orca()}" end'
        assert self.shells is not None
        # > The first line follows the name of the option, all others are lines of their own
        lines = [str(self.element)]
        lines += [indent(str(shell), _BLOCK_INDENT + _NESTED_INDENT) for shell in self.shells]
        lines.append(f"{_BLOCK_INDENT}end")
        return "\n".join(lines)


class FragBasis(BaseModel):
    """
    Class to model `fragbasis` attribute in `BlockBasis`.
    Also base class for `FragAux`, `FragAuxJ`, `FragAuxJK`, `FragAuxC`, `FragCabs`, `FragEcp`.

    Attributes
    ----------
    frag : dict[int, ORCAKeyword]
        A dictionary mapping atomic indices to basis set keywords.
    name: str
        Used to identify the class for the ORCA input

    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    frag: dict[int, ORCAKeyword]
    name: str = "fragbasis"

    @field_validator("frag")
    @classmethod
    def check_fragments(cls, values: dict[int, ORCAKeyword]) -> dict[int, ORCAKeyword]:
        """
        Parameters
        ----------
        values : dict[int | ORCAKeyword]
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
            frag_dict[v] = ORCAKeyword(frag_dict[v])

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


class BlockBasis(BlockABC):
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
    basis: ORCAKeyword | None = None
    auxj: ORCAKeyword | None = None
    gtoaux: ORCAKeyword | None = None
    auxbasis: ORCAKeyword | None = None
    aux: ORCAKeyword | None = None
    auxc: ORCAKeyword | None = None  # **
    auxx: ORCAKeyword | None = None  # **
    ecp: ORCAKeyword | None = None
    auxjk: ORCAKeyword | None = None
    cabs: ORCAKeyword | None = None
    gtocabs: ORCAKeyword | None = None
    cabsbasis: ORCAKeyword | None = None
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

    @field_validator("newecp")
    @classmethod
    def check_newecp(cls, value: NewBasis | None) -> NewBasis | None:
        """
        Explicit shells use the syntax of basis sets, which is not valid for ECPs.

        Parameters
        ----------
        value : NewBasis | None
        """
        if value is not None and value.shells is not None:
            raise ValueError("`newecp` only supports an ECP keyword, not explicit shells")
        return value

    def format_orca(self) -> str:
        """
        Method to convert the block into string for the ORCA input file.

        Raises
        ------
        ValueError
            If `newecp` holds explicit shells. These are rejected when the block is created, but
            fields assigned afterwards are not validated.
        """
        self.check_newecp(self.newecp)
        return super().format_orca()

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
    def frag_fromstring(cls, inp: str | FragBasis, info: ValidationInfo) -> FragBasis:
        """

        Parameters
        ----------
        inp: str | FragBasis
        info: ValidationInfo

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
