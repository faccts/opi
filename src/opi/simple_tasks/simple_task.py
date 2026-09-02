import os
import shutil
import typing
import warnings
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, get_type_hints

from pydantic import ConfigDict

from opi.core import Calculator
from opi.input import Input
from opi.input.simple_keywords import (
    SimpleKeyword,
    SimpleKeywordBox,
    Solvent,
)
from opi.input.structures import BaseStructureFile, Structure
from opi.output.core import Output
from opi.simple_tasks.method_settings import MethodSettings
from opi.simple_tasks.settings import Settings


class TaskSettings(Settings):
    """
    Base settings class for task-level keywords (SP, OPT, FREQ, …).

    Subclasses set ``task_keyword`` to the default ``Task`` enum member for
    the calculation type.  Additional task-specific options (convergence
    thresholds, flags, block parameters) are declared as typed fields in the
    subclass.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="forbid"
    )
    task_keyword: typing.Annotated[SimpleKeyword, SimpleKeywordBox] | None = None


_RT = typing.TypeVar("_RT", bound="TaskResults")


class SimpleTask(ABC, typing.Generic[_RT]):
    """
    Abstract base class for all OPI simple tasks.

    Combines a ``TaskSettings`` (what kind of calculation to run) with a
    ``MethodSettings`` (which method/basis/solvent to use) and exposes a
    ``run()`` method that writes the ORCA input, executes the calculation,
    and returns a ``TaskResults`` object.

    Concrete subclasses (``SinglePointTask``, ``OptTask``, …) bind the
    specific settings and results types through ``_task_settings_type`` and
    ``_results_type``.  Each subclass is parameterised with its concrete
    results type (e.g. ``SimpleTask[FreqResults]``) so that ``run``,
    ``restart``, and ``from_string`` all return the exact subtype without
    casts.

    Method family switching via the ``method`` setter automatically migrates
    compatible fields (``basis_set``, ``solvation_model``, ``solvent``) and
    warns about any settings that cannot be transferred.
    """

    _results_type: type[_RT]
    _task_settings: TaskSettings | None = None
    _method_settings: MethodSettings | None = None
    _input_object: Input
    _expert_mode: bool

    def __init__(
        self,
        method: str | SimpleKeyword | None = None,
        basis_set: str | SimpleKeyword | None = None,
        solvation_model: str | SimpleKeyword | None = None,
        solvent: str | Solvent | None = None,
        task_settings: "TaskSettings | dict[str, typing.Any] | None" = None,
        method_settings: "MethodSettings | dict[str, typing.Any] | None" = None,
        input: Input | str | None = None,
    ):
        """
        The various input parameters, both task and method related are set using this function. The most widely used arguments,
        like method and basis set are set using arguments that are defined in the init. If the user wants to add additional settings,
        such as block options like scf maxiter, they can make use of the `task_settings` and `method-settings` arguments, where any additional
        settings will be parsed, validated and then added to the respective `Settings` class.

        There is an additional optional argument `input`, if the user chooses to directly pass the input to the init, the `SimpleTask` class
        will forego any validation of input and simply execute the task using the user-given input data. This is recommended for more experienced
        users that want to add certain simple keywords or block options that are not provided by default.

        Passing `input` puts the task into expert mode: the given input takes precedence over
        everything the settings map to, and no default settings are filled in. Settings are still
        built from any `method`, `basis_set`, `solvation_model`, `solvent`, `task_settings` or
        `method_settings` that are passed alongside `input`, they just lose to it wherever both
        set the same thing. Without `input` the settings take precedence instead, so that they
        are re-applied over any manual edit of `SimpleTask.input`.

        Parameters
        ----------
        method : str or SimpleKeyword, optional
            Shorthand for setting ``method_settings.method``.  Mutually
            exclusive with passing a fully configured ``method_settings``
            object that already has a method.
        basis_set : str or SimpleKeyword, optional
            Shorthand for ``method_settings.basis_set``.
        solvation_model : str or SimpleKeyword, optional
            Shorthand for ``method_settings.solvation_model``.
        solvent : str or Solvent, optional
            Shorthand for ``method_settings.solvent``.
        task_settings : TaskSettings or dict, optional
            Overrides the default task settings.  A plain ``dict`` is
            validated against the concrete ``TaskSettings`` subclass.
        method_settings : MethodSettings or dict, optional
            Pre-built method settings object.  When ``method`` is also given,
            values from the shorthand parameters take precedence over fields
            already present in ``method_settings``.
        input : Input or str, optional
            Ready-made input, either as an ``Input`` object or as a raw ORCA
            keyword string.  Enables expert mode: the input is not validated
            and always takes precedence over the settings.

        Raises
        ------
        ValueError
            If neither ``method`` nor a ``method_settings`` object with a
            method is provided, unless ``input`` is given.
        """
        # > An input passed at init marks expert mode, in which the user is in charge: the given
        # > input wins over the settings and no default settings are filled in.
        self._expert_mode = input is not None

        if isinstance(input, Input):
            self._input_object = input
        elif input is not None:
            # Raw input bypasses the typed settings system entirely — no validation.
            self._input_object = Input()
            self._input_object.add_arbitrary_string(input, pos="top")
        else:
            self._input_object = Input()

        if isinstance(task_settings, dict):
            # The intended TaskSettings type is taken from the type hints of the concrete task.
            self._task_settings = self._get_task_settings_type().model_validate(task_settings)
        elif task_settings is not None:
            # A ready-made TaskSettings object is used as it is.
            self._task_settings = task_settings
        elif not self._expert_mode:
            # None falls back to a default instance so there's always a settings object.
            self._task_settings = self._get_task_settings_type()()
        else:
            # In expert mode the given input carries the task keyword, so no default is added.
            self._task_settings = None

        resolved_method_settings: MethodSettings | None = (
            MethodSettings(**method_settings)
            if isinstance(method_settings, dict)
            else method_settings
        )

        if method is not None:
            # Here the type of MethodSettings class will be resolved depending on which method was selected.
            resolved_type = MethodSettings.resolve_method_settings_type(method)
            # MethodSettings object is created with the basic essential input parameters.
            base_data: dict[str, typing.Any] = {
                k: v
                for k, v in {
                    "method": method,
                    "basis_set": basis_set,
                    "solvation_model": solvation_model,
                    "solvent": solvent,
                }.items()
                if v is not None
            }
            if resolved_method_settings is not None:
                # If there are other options defined over method_settings argument, they will be merged with the existing
                # MethodSettings object here.
                # model_extra captures plugin-defined fields absent from model_fields.
                extra: dict[str, typing.Any] = {
                    **resolved_method_settings.model_dump(exclude_unset=True),
                    **(resolved_method_settings.model_extra or {}),
                }
                # base_data last so shorthand args override method_settings fields.
                self._method_settings = resolved_type(**{**extra, **base_data})
            else:
                # if method_settings argument is None, simple the methodSettings class with the base input parameters will be defined.
                self._method_settings = resolved_type(**base_data)
        elif resolved_method_settings is not None:
            self._method_settings = resolved_method_settings
        elif self._expert_mode:
            # In expert mode the given input carries the method, so none has to be provided.
            self._method_settings = None
        else:
            # raise error if no method is given
            raise ValueError(
                "Either 'method' or a 'method_settings' object with a method must be provided"
            )

    @classmethod
    def _get_task_settings_type(cls) -> type[TaskSettings]:
        """Get the TaskSettings subclass type associated with the SimpleTask initialized."""
        hints = get_type_hints(cls)
        task_setting_type = hints["_task_settings"]

        return typing.cast(type[TaskSettings], task_setting_type)

    @property
    def task_settings(self) -> TaskSettings | None:
        """Task-level settings (keyword, thresholds, flags)."""
        return self._task_settings if self._task_settings else None

    @property
    def method_settings(self) -> MethodSettings | None:
        """Method-level settings (functional, basis set, solvent, …)."""
        return self._method_settings if self._method_settings else None

    @property
    def input(self) -> Input:
        """
        Returns the ``Input`` object for this task, merged from ``task_settings``,
        ``method_settings`` and the input held by the task.

        The merge is re-done on every access, and which side wins depends on how the
        task was built. In expert mode — an ``input`` was passed to the constructor —
        the task's own input is merged last and hence takes precedence over the
        settings. Otherwise the settings are merged last, so that they are re-applied
        over any manual edit of the fields they control.

        Either way, everything the settings do not control (extra keywords, ``ncores``,
        arbitrary strings, …) is preserved across accesses.

        Returns
        -------
        Input
            The task's ``Input`` object, ready for inspection or further
            user customisation before calling ``run()``.
        """
        if self._task_settings is None and self._method_settings is None:
            # > Nothing to merge: the input is used as it is.
            return self._input_object

        settings_input = Input()
        for setting in (self._task_settings, self._method_settings):
            if setting:
                settings_input = settings_input | setting.map_to_input()

        if self._expert_mode:
            self._input_object = settings_input | self._input_object
        else:
            self._input_object = self._input_object | settings_input

        return self._input_object

    @input.setter
    def input(self, value: Input) -> None:
        self._input_object = value

    @property
    def keyword(self) -> SimpleKeyword | None:
        """The primary task keyword (e.g. ``Task.SP``, ``Task.OPT``)."""
        return self._task_settings.task_keyword if self._task_settings else None

    @property
    def method(self) -> SimpleKeyword | None:
        """Active method keyword, or ``None`` if the settings type has no method field."""
        if self._method_settings and hasattr(self._method_settings, "method"):
            return self._method_settings.method
        return None

    @method.setter
    def method(self, new_value: str | SimpleKeyword | None) -> None:
        """
        Change the method, migrating to a different settings type when needed.

        If ``new_value`` belongs to the same method family as the current
        settings, the field is updated in-place. Otherwise a new settings
        object of the correct type is created, carrying over compatible fields
        (``basis_set``, ``solvation_model``, ``solvent``) and warning about
        any fields that are dropped.

        Raises
        ------
        AttributeError
            If the current settings type does not have a ``method`` field.
        """
        if not self._method_settings:
            raise AttributeError("Method settings has not been set.")
        if not hasattr(self._method_settings, "method"):
            raise AttributeError("method is not defined in method_settings object")
        if new_value is None:
            # Set the method to None and skip resolving the type.
            self._method_settings.method = None
            return
        resolved_type = MethodSettings.resolve_method_settings_type(new_value)
        if isinstance(self._method_settings, resolved_type):
            # Add type:ignore since the resolving of string to SimpleKeyword happens in validation of Settings.
            self._method_settings.method = new_value  # type:ignore
        else:
            common_fields: dict[str, Any] = {"method": new_value}
            for field in ("basis_set", "solvation_model", "solvent"):
                if field in resolved_type.model_fields:
                    val = getattr(self._method_settings, field, None)
                    if val is not None:
                        common_fields[field] = val
            dropped = [
                f
                for f, v in self._method_settings.model_dump(exclude_unset=True).items()
                if f not in common_fields and v is not None
            ]
            if dropped:
                warnings.warn(
                    f"Switching method family dropped settings: {', '.join(dropped)}",
                    UserWarning,
                    stacklevel=2,
                )
            self._method_settings = resolved_type(**common_fields)

    @property
    def basis_set(self) -> SimpleKeyword | None:
        """Active basis-set keyword, or ``None`` if the settings type has no basis_set field."""
        if self._method_settings and hasattr(self._method_settings, "basis_set"):
            return self._method_settings.basis_set
        return None

    @basis_set.setter
    def basis_set(self, new_value: str | SimpleKeyword | None) -> None:
        """
        Raises
        ------
        AttributeError
            If the current settings type does not have a ``basis_set`` field.
        """
        if not self._method_settings:
            raise AttributeError("Method settings has not been set.")
        if not hasattr(self._method_settings, "basis_set"):
            raise AttributeError("basis_set is not defined in method_settings object")
        self._method_settings.basis_set = new_value  # type:ignore

    @property
    def solvent(self) -> str | None:
        """Solvent name, or ``None`` if the settings type has no solvent field."""
        if self._method_settings and hasattr(self._method_settings, "solvent"):
            return self._method_settings.solvent
        return None

    @solvent.setter
    def solvent(self, new_value: str | None) -> None:
        """
        Raises
        ------
        AttributeError
            If the current settings type does not have a ``solvent`` field.
        """
        if not self._method_settings:
            raise AttributeError("Method settings has not been set.")
        if not hasattr(self._method_settings, "solvent"):
            raise AttributeError("solvent is not defined in method_settings object")
        self._method_settings.solvent = new_value

    @property
    def solvation_model(self) -> SimpleKeyword | None:
        """Solvation-model keyword, or ``None`` if the settings type has no solvation_model field."""
        if self._method_settings and hasattr(self._method_settings, "solvation_model"):
            return self._method_settings.solvation_model
        return None

    @solvation_model.setter
    def solvation_model(self, new_value: str | SimpleKeyword | None) -> None:
        """
        Raises
        ------
        AttributeError
            If the current settings type does not have a ``solvation_model`` field.
        """
        if not self._method_settings:
            raise AttributeError("Method settings has not been set.")
        if not hasattr(self._method_settings, "solvation_model"):
            raise AttributeError("solvation_model is not defined in method_settings object")
        self._method_settings.solvation_model = new_value  # type:ignore

    @classmethod
    def from_string(
        cls,
        string: str,
    ) -> typing.Self:
        """
        Build a task from a raw ORCA keyword string.

        Bypasses the typed ``TaskSettings``/``MethodSettings`` API and feeds
        keywords directly into the input file. Equivalent to constructing the
        task with ``input=string``.

        Parameters
        ----------
        string : str
            Space-separated ORCA simple keywords (leading ``!`` characters are
            stripped automatically).  Example: ``"B3LYP def2-SVP FREQ"``.

        Returns
        -------
        Self
            A task instance of the concrete subclass, ready for ``run()``.
        """
        inp = Input()
        keywords = string.split()
        for keyword in keywords:
            keyword = keyword.strip("!")
            inp.add_simple_keywords(SimpleKeyword(keyword))

        return cls(input=inp)

    def run(
        self,
        basename: str,
        structure: Structure | BaseStructureFile,
        working_dir: Path | str | os.PathLike[str] = Path("RUN"),
        ncores: int | None = None,
        memory: int | None = None,
        moinp: Path | None = None,
        strict: bool = False,
    ) -> _RT:
        """
        Execute the computational task with the given structure and settings.

        This method prepares the working directory, configures the calculation
        input parameters, and runs the calculation using an external calculator.
        The results are returned as an instance of the configured results type.

        Parameters
        ----------
        basename : str
            Base name for the calculation.
        structure : Structure or BaseStructureFile
            The input structure for the calculation.
        working_dir : pathlib.Path, optional
            Directory in which the calculation will be executed.
            If it exists, it will be removed and recreated. Defaults to "RUN".
        ncores : int, optional
            Number of CPU cores to use for the calculation. Overrides the default
            value in the input object if provided.
        memory : int, optional
            Amount of memory to allocate for the calculation. Overrides the default
            value in the input object if provided.
        moinp : pathlib.Path, optional
            Path to a molecular orbital input file. Overrides the default if provided.
        strict : bool, optional
            Controls whether working directory will be created/overwritten. Defaults to False.

        Returns
        -------
        TaskResults
            An instance of the configured results type containing the results
            of the calculation.
        """
        working_dir = Path(working_dir)

        if strict:
            # Must already exist
            if not working_dir.exists():
                raise ValueError(
                    f"Working directory {working_dir.resolve()} does not exist (strict mode)"
                )

            # Must be empty
            if any(working_dir.iterdir()):
                raise ValueError(
                    f"Working directory {working_dir.resolve()} is not empty (strict mode)"
                )

        else:
            # Non-strict: recreate directory
            if working_dir.exists():
                shutil.rmtree(working_dir)
            working_dir.mkdir()

        inp = self.input

        if ncores is not None:
            inp.ncores = ncores

        if memory is not None:
            inp.memory = memory

        if moinp is not None:
            inp.moinp = moinp

        calc = Calculator(basename, working_dir=working_dir)
        calc.structure = structure
        calc.input = inp

        calc.write_and_run()

        method_family = type(self.method_settings) if self.method_settings else MethodSettings
        return self._results_type(calculator=calc, _method_family=method_family)

    def restart(
        self,
        previous_results: "TaskResults",
        basename: str | None = None,
        structure: Structure | BaseStructureFile | None = None,
        working_dir: Path | None = None,
        ncores: int | None = None,
        memory: int | None = None,
        moinp: Path | None = None,
        use_previous_orbitals: bool = False,
    ) -> _RT:
        """
        Re-run the task, inheriting settings from a previous calculation.

        All parameters default to the values used in ``previous_results`` and
        only need to be supplied when overriding them.  The target working
        directory is wiped and recreated by the underlying ``run()`` call, so
        the previous output files are not preserved unless ``working_dir`` is
        changed.

        Parameters
        ----------
        previous_results : TaskResults
            Results object from the earlier run.  Provides fallback values for
            ``basename``, ``struct``, ``working_dir``, ``ncores``, and
            ``memory``.
        basename : str, optional
            Job name for the new calculation.  Defaults to the basename of the
            previous run.
        structure : Structure or BaseStructureFile, optional
            Input structure.  Defaults to the structure used in the previous
            run.  Raises ``ValueError`` if no structure can be determined.
        working_dir : Path, optional
            Directory in which to run the new calculation.  Defaults to the
            working directory of the previous run (which will be overwritten).
        ncores : int, optional
            Number of CPU cores.  Defaults to the value from the previous run.
        memory : int, optional
            Memory in MB.  Defaults to the value from the previous run.
        moinp : Path, optional
            Explicit path to an MO input file.  Ignored when
            ``use_previous_orbitals=True``.  Defaults to the ``moinp`` of the
            previous run.
        use_previous_orbitals : bool, optional
            If ``True``, passes the ``.gbw`` file from the previous calculation
            as ``moinp`` to seed the SCF guess.  Raises ``FileNotFoundError``
            if the file does not exist.

        Returns
        -------
        TaskResults
            Results of the new calculation, of the same concrete type as this
            task's ``_results_type``.

        Raises
        ------
        ValueError
            If no structure is available from either the argument or the
            previous results.
        FileNotFoundError
            If ``use_previous_orbitals=True`` and the ``.gbw`` file from the
            previous run is missing.
        """
        prev_calc = previous_results.calculator

        basename = basename if basename else prev_calc.basename
        struct = structure if structure else prev_calc.structure
        if struct is None:
            raise ValueError(
                "No structure available for restart: previous calculation had no structure set"
            )
        working_dir = working_dir if working_dir else prev_calc.working_dir
        ncores = ncores if ncores else prev_calc.input.ncores
        memory = memory if memory else prev_calc.input.memory

        if use_previous_orbitals:
            prev_gbw = prev_calc.working_dir / f"{prev_calc.basename}.gbw"
            if not prev_gbw.exists():
                raise FileNotFoundError(f"GBW file not found: {prev_gbw}")
            moinp = prev_gbw
        else:
            moinp = moinp if moinp else prev_calc.input.moinp

        return self.run(basename, struct, working_dir, ncores, memory, moinp)


class TaskResults(ABC):
    """
    Abstract base class for the results returned by a completed task.

    Wraps the ``Calculator`` that ran the job and provides lazy-evaluated
    access to the parsed ``Output``.  Subclasses expose task-specific
    properties (energies, structures, gradients, …) and must implement
    ``primary_property``.
    """

    def __init__(self, calculator: Calculator, _method_family: type[MethodSettings]):
        """
        Parameters
        ----------
        calculator : Calculator
            The calculator that ran the calculation.
        """
        self.calculator = calculator
        self._method_family = _method_family

    @property
    def output(self) -> Output:
        """
        Parsed ORCA output.

        Lazily calls ``get_output()`` and ``parse()`` on the first access so
        that result objects can be created without immediately hitting the
        filesystem.
        """
        if not self.calculator:
            raise ValueError("calculator not set")

        out = self.calculator.get_output()
        out.parse()
        return out

    @property
    def status(self) -> bool:
        """``True`` if the job terminated normally and passes method-specific convergence checks."""
        return self.output.terminated_normally() and self._method_family.check_convergence(
            self.output
        )

    @property
    @abstractmethod
    def primary_property(self) -> Any:
        """The most important result for this task type (energy, structure, …)."""
        pass

    @property
    def final_energy(self) -> float:
        """The final energy of the calculation.

        Raises
        ------
        ValueError
            If the energy is not present in the ORCA output."""
        final_energy = self.output.get_final_energy()

        if final_energy is None:
            raise ValueError("Could not get final energy from ORCA Output")

        return final_energy
