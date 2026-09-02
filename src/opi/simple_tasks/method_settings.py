import typing
import warnings
from typing import Any

from pydantic import ConfigDict, model_validator

from opi.input import Input
from opi.input.simple_keywords import (
    AuxBasisSet,
    BasisSet,
    Dft,
    DispersionCorrection,
    ForceField,
    Grid,
    Method,
    SimpleKeyword,
    SolvationModel,
    Solvent,
    Sqm,
    Wft,
)
from opi.input.simple_keywords.dlpno import Dlpno, PNOThresh
from opi.input.simple_keywords.scf import Scf, ScfConvergence, ScfSolver, ScfThreshold
from opi.input.simple_keywords.wft import DLPNOcc
from opi.output.core import Output
from opi.simple_tasks.settings import Settings


class MethodSettings(Settings):
    """
    Base settings class for all computational methods.

    Instantiating ``MethodSettings`` directly dispatches to the appropriate
    subclass (``DFTSettings``, ``SQMSettings``, etc.) based on the ``method``
    keyword via ``__new__``.  Subclasses set ``extra="forbid"`` so that
    unknown fields raise an error at construction time.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True, extra="allow")

    method: typing.Annotated[SimpleKeyword, Method] | None = None
    basis_set: typing.Annotated[SimpleKeyword, BasisSet] | None = None
    solvation_model: typing.Annotated[SimpleKeyword, SolvationModel] | None = None
    solvent: typing.Annotated[str, Solvent] | None = None

    def __new__(cls, /, **data: Any) -> "MethodSettings":
        """
        Dispatch to the correct ``MethodSettings`` subclass.

        When called as ``MethodSettings(method=..., ...)``, inspects ``method``
        and returns an instance of the matching subclass so callers never need
        to import the concrete type.
        """
        if cls is MethodSettings:
            method = data.get("method")
            if method is not None:
                resolved_cls = cls.resolve_method_settings_type(method)
                return super().__new__(resolved_cls)
        return super().__new__(cls)

    @model_validator(mode="before")
    @classmethod
    def _check_valid_fields(cls, data: Any) -> Any:
        """
        Reject unknown fields before Pydantic processes them.

        Subclasses use ``extra="forbid"``, but this pre-validator runs first
        and provides a clearer error message listing both the invalid fields
        and the valid ones.
        """
        if not isinstance(data, dict) or cls is MethodSettings:
            return data
        invalid_fields = set(data) - set(cls.model_fields)
        if invalid_fields:
            field_word = "field" if len(invalid_fields) == 1 else "fields"
            raise ValueError(
                f"Invalid {field_word} for {cls.__name__}: {', '.join(sorted(invalid_fields))}. "
                f"Valid fields: {', '.join(sorted(cls.model_fields))}"
            )
        return data

    @classmethod
    def resolve_method_settings_type(
        cls, method: str | SimpleKeyword
    ) -> typing.Type["MethodSettings"]:
        """
        Return the ``MethodSettings`` subclass that handles ``method``.

        Iterates over the known enum-to-settings mapping and returns the first
        match.

        Parameters
        ----------
        method : str or SimpleKeyword
            Method keyword to look up (e.g. ``"PBE"``, ``"XTB2"``).

        Returns
        -------
        type[MethodSettings]
            Concrete subclass responsible for the given method family.

        Raises
        ------
        ValueError
            If ``method`` is not found in any registered enum.
        """

        enum_to_settings = {
            Dft: DftSettings,
            Sqm: SqmSettings,
            Wft: WftSettings,
            Method: HFSettings,
            ForceField: ForceFieldSettings,
        }
        for enum_class, settings_type in enum_to_settings.items():
            try:
                if enum_class.find_keyword(method):
                    return typing.cast(typing.Type[MethodSettings], settings_type)
            except ValueError:
                if enum_class is Dft and DftSettings._split_dft_disp_keyword(method) is not None:
                    return typing.cast(typing.Type[MethodSettings], settings_type)

        raise ValueError(f"Keyword {method} not found in any of the valid groupings")

    @classmethod
    def check_convergence(cls, output: Output) -> bool:
        """
        Method-family-specific convergence check on top of ``Output.terminated_normally()``.

        Base implementation performs no additional check; subclasses override
        this for methods that need one (e.g. SCF-based methods check
        ``Output.scf_converged()``).

        Parameters
        ----------
        output : Output
            Parsed ORCA output of the completed calculation.

        Returns
        -------
        bool
            ``True`` if this method family's convergence criteria are met.
        """
        return True


class DftSettings(MethodSettings):
    """
    Method settings for DFT calculations.

    Accepts DFT functionals with an optional ``-`` separated dispersion
    correction (e.g. ``"PBE-D3BJ"``), which is split into ``method`` and
    ``disp_correction`` on construction.  Composite "3c" methods silently drop
    ``basis_set`` because they carry their own basis internally.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="forbid"
    )
    _name: str = "dft"
    method: typing.Annotated[SimpleKeyword, Dft] | None = None
    grid: typing.Annotated[SimpleKeyword, Grid] | None = None
    scf_maxiter: typing.Annotated[int, "scf", "maxiter"] | None = None
    scf_threshold: typing.Annotated[SimpleKeyword, ScfThreshold] | None = None
    scf_solver: typing.Annotated[SimpleKeyword, ScfSolver] | None = None
    scf_stab: bool = False
    scf_conv: typing.Annotated[SimpleKeyword, ScfConvergence] | None = None
    disp_correction: typing.Annotated[SimpleKeyword, DispersionCorrection] | None = None

    @model_validator(mode="before")
    @classmethod
    def _split_compound_method(cls, data: Any) -> Any:
        """
        Split a compound ``"Functional-Dispersion"`` ``method`` string into
        separate ``method`` and ``disp_correction`` fields.

        Runs before validation, so by the time ``method`` and
        ``disp_correction`` are validated individually they are already
        single-purpose values. Left untouched if ``method`` is already a valid
        standalone ``Dft`` keyword, since several functionals carry their own
        dispersion correction (or a dash) in their registered name, e.g.
        ``"wb97x-d3bj"`` or ``"r2scan-3c"``.
        """
        if not isinstance(data, dict):
            return data
        method = data.get("method")
        if method is None:
            return data

        method_str = method.keyword if isinstance(method, SimpleKeyword) else method
        if not isinstance(method_str, str):
            return data

        try:
            Dft.find_keyword(method_str)
            return data
        except ValueError:
            pass

        split = cls._split_dft_disp_keyword(method_str)
        if split is None:
            return data

        functional, dispersion = split
        if data.get("disp_correction") is not None:
            raise ValueError(
                f"Conflicting dispersion correction: method {method_str!r} already specifies "
                f"{dispersion!r}, but disp_correction={data['disp_correction']!r} was also given."
            )

        data = dict(data)
        data["method"] = functional
        data["disp_correction"] = dispersion
        return data

    @model_validator(mode="after")
    def cross_validate(self) -> "DftSettings":
        """
        Cross-validation for `DftSettings`.
        If the method keyword contains '3c', the `basis_set` attribute will be set to `None`.

        The `DftSettings` object is then returned.

        Returns
        -------
        DFTSettings
            Cross-validated `DFTSettings` object.

        """
        if (self.method and "3c" in self.method.keyword) and self.basis_set:
            warnings.warn("Basis Set will be ignored due to selection of Method", UserWarning)
            self.basis_set = None

        return self

    def map_to_input(self) -> Input:
        """
        Extend the base mapping with SCF stability analysis.

        Calls the parent ``map_to_input`` for all annotated fields, then
        appends ``SCFSTAB`` when ``scf_stab=True``.

        Returns
        -------
        Input
            Modified ``Input`` object.
        """
        input_object = super().map_to_input()

        if self.scf_stab:
            input_object.add_simple_keywords(Scf.SCFSTAB)

        return input_object

    @classmethod
    def check_convergence(cls, output: Output) -> bool:
        """``True`` if the SCF converged."""
        return output.scf_converged()

    @classmethod
    def _split_dft_disp_keyword(cls, value: str | SimpleKeyword) -> tuple[str, str] | None:
        """
        Split a compound ``"Functional-Dispersion"`` string into its parts.

        Splits on the last ``-`` so functional names that themselves contain a
        dash (e.g. ``"cam-b3lyp"``) are handled correctly.

        Parameters
        ----------
        value: str | SimpleKeyword
            The value to search for.

        Returns
        -------
        tuple[str, str] | None
            ``(functional, dispersion)`` if ``value`` is a valid compound of a
            ``Dft`` keyword and a ``DispersionCorrection`` keyword, ``None``
            otherwise.
        """
        if isinstance(value, SimpleKeyword):
            value = value.keyword

        if "-" not in value:
            return None

        functional, _, dispersion = value.rpartition("-")
        try:
            Dft.find_keyword(functional)
            DispersionCorrection.find_keyword(dispersion)
        except ValueError:
            return None

        return functional, dispersion


class SqmSettings(MethodSettings):
    """
    Method settings for semi-empirical (SQM) calculations.

    Supports the same SCF control knobs as ``DFTSettings`` (``scf_maxiter``,
    ``scf_threshold``, ``scf_solver``, ``scf_stab``, ``scf_conv``).
    No basis set field — SQM methods carry their own parametrisation.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="forbid"
    )
    _name: str = "sqm"
    method: typing.Annotated[SimpleKeyword, Sqm]
    scf_maxiter: typing.Annotated[int, "scf", "maxiter"] | None = None
    scf_threshold: typing.Annotated[SimpleKeyword, ScfThreshold] | None = None
    scf_solver: typing.Annotated[SimpleKeyword, ScfSolver] | None = None
    scf_stab: bool = False
    scf_conv: typing.Annotated[SimpleKeyword, ScfConvergence] | None = None

    def map_to_input(self) -> Input:
        """
        Extend the base mapping with SCF stability analysis.

        Returns
        -------
        Input
            Modified ``Input`` object.
        """
        input_object = super().map_to_input()

        if self.scf_stab:
            input_object.add_simple_keywords(Scf.SCFSTAB)

        return input_object

    @classmethod
    def check_convergence(cls, output: Output) -> bool:
        """``True`` if the SCF converged."""
        return output.scf_converged()


class WftSettings(MethodSettings):
    """
    Method settings for wave-function theory (WFT) calculations.

    Covers correlated methods such as MP2, CCSD, CCSD(T), etc.  Basis set
    and solvation are inherited from ``MethodSettings``.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="forbid"
    )
    _name: str = "wft"
    method: typing.Annotated[SimpleKeyword, Wft]

    @classmethod
    def check_convergence(cls, output: Output) -> bool:
        """``True`` if the SCF converged."""
        return output.scf_converged()


class HFSettings(MethodSettings):
    """
    Method settings for Hartree-Fock calculations.

    Basis set and solvation are inherited from ``MethodSettings``.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="forbid"
    )
    _name: str = "hf"
    method: typing.Annotated[SimpleKeyword, Method]

    @classmethod
    def check_convergence(cls, output: Output) -> bool:
        """``True`` if the SCF converged."""
        return output.scf_converged()


class ForceFieldSettings(MethodSettings):
    """
    Method settings for force-field calculations.

    ``basis_set`` is silently dropped because force fields do not use a
    quantum-mechanical basis.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="forbid"
    )
    _name: str = "forcefield"
    method: typing.Annotated[SimpleKeyword, ForceField]

    @model_validator(mode="after")
    def cross_validate(self) -> "ForceFieldSettings":
        if self.basis_set:
            warnings.warn(
                "Basis Set will be ignored due to selection of Force Field method", UserWarning
            )
            self.basis_set = None

        return self


class DlpnoCcSettings(MethodSettings):
    """
    Method settings for DLPNO coupled-cluster calculations.

    Exposes DLPNO-specific thresholds (``pno_thresh``, ``dlpno_t_cut_do``,
    ``dlono_t_cut_pno``) and enables LED analysis via ``dlpno_led=True``.
    SCF control knobs are also available.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="forbid"
    )
    _name: str = "dlpnocc"
    method: typing.Annotated[SimpleKeyword, DLPNOcc] | None = None
    aux_basis: typing.Annotated[SimpleKeyword, AuxBasisSet] | None = None
    pno_thresh: typing.Annotated[SimpleKeyword, PNOThresh] | None = None
    dlpno_led: bool | None = None
    dlpno_t_cut_do: typing.Annotated[float, "mdci", "tcutdo"] | None = None
    dlpno_t_cut_pno: typing.Annotated[float, "mdci", "tcutpno"] | None = None
    scf_maxiter: typing.Annotated[int, "scf", "maxiter"] | None = None
    scf_threshold: typing.Annotated[SimpleKeyword, ScfThreshold] | None = None
    scf_solver: typing.Annotated[SimpleKeyword, ScfSolver] | None = None
    scf_stab: bool = False
    scf_conv: typing.Annotated[SimpleKeyword, ScfConvergence] | None = None

    def map_to_input(self) -> Input:
        """
        Extend the base mapping with DLPNO-specific keywords.

        Appends ``SCFSTAB`` when ``scf_stab=True`` and ``LED`` when
        ``dlpno_led=True``, in addition to the standard field-annotation
        mapping performed by the parent.

        Returns
        -------
        Input
            Modified ``Input`` object.
        """
        input_object = super().map_to_input()

        if self.scf_stab:
            input_object.add_simple_keywords(Scf.SCFSTAB)

        if self.dlpno_led:
            input_object.add_simple_keywords(Dlpno.LED)

        return input_object

    @classmethod
    def check_convergence(cls, output: Output) -> bool:
        """``True`` if the SCF converged."""
        return output.scf_converged()
