from opi.input.simple_keywords.approximation import Approximation
from opi.input.simple_keywords.atomic_charge import AtomicCharge
from opi.input.simple_keywords.aux_basis_set import AuxBasisSet
from opi.input.simple_keywords.avas import Avas
from opi.input.simple_keywords.base import ORCAKeyword
from opi.input.simple_keywords.basis_set import BasisSet
from opi.input.simple_keywords.basisoption import BasisOption
from opi.input.simple_keywords.dft import Dft
from opi.input.simple_keywords.dispersion_correction import DispersionCorrection
from opi.input.simple_keywords.dlpno import Dlpno
from opi.input.simple_keywords.docker import Docker
from opi.input.simple_keywords.ecp import Ecp
from opi.input.simple_keywords.esd import Esd
from opi.input.simple_keywords.external_tools import ExternalTools
from opi.input.simple_keywords.force_field import ForceField
from opi.input.simple_keywords.gcp import Gcp
from opi.input.simple_keywords.goat import Goat
from opi.input.simple_keywords.grid import Grid
from opi.input.simple_keywords.method import Method
from opi.input.simple_keywords.miscellaneous import Miscellaneous
from opi.input.simple_keywords.neb import Neb
from opi.input.simple_keywords.opt import Opt
from opi.input.simple_keywords.output_control import OutputControl
from opi.input.simple_keywords.property import Property
from opi.input.simple_keywords.qmmm import Qmmm
from opi.input.simple_keywords.relativistic_correction import RelativisticCorrection
from opi.input.simple_keywords.scf import Scf
from opi.input.simple_keywords.shell_type import ShellType
from opi.input.simple_keywords.solvation import Solvation
from opi.input.simple_keywords.solvation_model import SolvationModel
from opi.input.simple_keywords.sqm import Sqm
from opi.input.simple_keywords.task import Task
from opi.input.simple_keywords.wft import Wft

__all__ = ("SimpleKeyword",)


class SimpleKeyword(
    Approximation,
    AtomicCharge,
    AuxBasisSet,
    Avas,
    BasisSet,
    BasisOption,
    Dft,
    DispersionCorrection,
    Dlpno,
    Docker,
    Ecp,
    Esd,
    ExternalTools,
    ForceField,
    Gcp,
    Goat,
    Grid,
    Method,
    Miscellaneous,
    Neb,
    Opt,
    OutputControl,
    Property,
    Qmmm,
    RelativisticCorrection,
    Scf,
    ShellType,
    Solvation,
    SolvationModel,
    Sqm,
    Task,
    Wft,
):
    """
    Collection of all implemented ORCA simple keywords.

    Inherits the members of every ``SimpleKeywordBox`` group, so any keyword can be
    accessed as an attribute (e.g. ``SimpleKeyword.TIGHTSCF``) or looked up across all
    groups with ``SimpleKeyword.find_keyword()``. ``LibXC`` is not included, since its
    attribute names clash with those of ``Dft``; use ``LibXC`` directly instead.

    Calling ``SimpleKeyword("keyword")`` creates an ``ORCAKeyword`` for an ad-hoc
    keyword that is not implemented in any group.
    """

    def __new__(cls, keyword: str, alias: str | list[str] | None = None) -> ORCAKeyword:  # type: ignore[misc]
        """
        Create an ``ORCAKeyword`` from a raw string.

        Parameters
        ----------
        keyword : str
            Keyword string for the ORCA input line.
        alias : str | list[str], optional
            Alternative lookup name for ``SimpleKeywordBox.from_string``.

        Returns
        -------
        ORCAKeyword
            The newly created keyword.
        """
        # > Kept for backwards compatibility, `SimpleKeyword` used to be the keyword class itself
        return ORCAKeyword(keyword, alias)
