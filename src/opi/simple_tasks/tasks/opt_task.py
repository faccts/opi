import typing

from opi.input import Input
from opi.input.simple_keywords import SimpleKeyword, Task
from opi.input.simple_keywords.opt import Opt, OptThreshold
from opi.input.structures import Structure
from opi.simple_tasks.simple_task import SimpleTask, TaskResults, TaskSettings


class OptSettings(TaskSettings):
    """
    Task settings for geometry optimisations (``! OPT``).

    The ``opt_h``, ``lopt``, and ``optrigid`` flags are translated to the
    corresponding ORCA keywords in ``map_to_input``; combinations of
    ``opt_h`` and ``lopt`` map to ``OPT_H``, ``L_OPT``, or ``L_OPT_H``
    automatically.
    """

    _name: str = "opt"
    task_keyword: typing.Annotated[SimpleKeyword, Task] = Task.OPT
    opt_threshold: typing.Annotated[SimpleKeyword, OptThreshold] | None = None
    optrigid: bool = False
    opt_h: bool = False
    lopt: bool = False
    opt_maxiter: typing.Annotated[int, "geom", "maxiter"] | None = None

    def map_to_input(self) -> Input:
        """
        Extend the base mapping with optimisation-mode keywords.

        Appends ``RIGIDBODYOPT`` when ``optrigid=True``, and selects
        ``OPT_H`` / ``L_OPT`` / ``L_OPT_H`` based on the ``opt_h`` and
        ``lopt`` flags.

        Returns
        -------
        Input
            Modified ``Input`` object.
        """
        input_object = super().map_to_input()

        if self.optrigid:
            input_object.add_simple_keywords(Opt.RIGIDBODYOPT)

        opt_map = {
            (True, True): Opt.L_OPTH,
            (True, False): Opt.OPTH,
            (False, True): Opt.L_OPT,
        }

        keyword = opt_map.get((self.opt_h, self.lopt))
        if keyword:
            input_object.add_simple_keywords(keyword)

        return input_object


class OptResults(TaskResults):
    """Results from a geometry optimisation."""

    @property
    def structure(self) -> Structure:
        """
        Optimised geometry.

        Raises
        ------
        ValueError
            If the structure is not present in the ORCA output.
        """
        structure = self.output.get_structure()
        if structure is None:
            raise ValueError("Could not get structure from ORCA Output")

        return structure

    @property
    def primary_property(self) -> tuple[float, Structure]:
        """``(final_energy, optimised_structure)`` tuple."""
        return self.final_energy, self.structure

    @property
    def status(self) -> bool:
        return (
            self.output.geometry_optimization_converged()
            and self._method_family.check_convergence(self.output)
        )


class OptTask(SimpleTask[OptResults]):
    """
    High-level task for geometry optimisations.

    Exposes convenience properties (``opt_threshold``, ``optrigid``,
    ``opt_h``, ``lopt``, ``opt_maxiter``) that forward to the underlying
    ``OptSettings`` object.  Returns ``OptResults`` with the optimised
    energy and structure.
    """

    _task_settings: OptSettings
    _results_type = OptResults

    @property
    def opt_threshold(self) -> SimpleKeyword | None:
        """Convergence threshold keyword (e.g. ``OptThreshold.TIGHTOPT``)."""
        return self._task_settings.opt_threshold

    @opt_threshold.setter
    def opt_threshold(self, new_value: SimpleKeyword | str) -> None:
        self._task_settings.opt_threshold = new_value  # type:ignore

    @property
    def optrigid(self) -> bool:
        """When ``True``, adds ``RIGIDBODYOPT`` for rigid-body optimisation."""
        return self._task_settings.optrigid

    @optrigid.setter
    def optrigid(self, new_value: bool) -> None:
        self._task_settings.optrigid = new_value

    @property
    def opt_h(self) -> bool:
        """When ``True``, optimises hydrogen positions only (``OPT_H`` / ``L_OPT_H``)."""
        return self._task_settings.opt_h

    @opt_h.setter
    def opt_h(self, new_value: bool) -> None:
        self._task_settings.opt_h = new_value

    @property
    def lopt(self) -> bool:
        """When ``True``, uses loose optimisation criteria (``L_OPT`` / ``L_OPT_H``)."""
        return self._task_settings.lopt

    @lopt.setter
    def lopt(self, new_value: bool) -> None:
        self._task_settings.lopt = new_value

    @property
    def opt_maxiter(self) -> int | None:
        """Maximum number of geometry optimisation steps (``%geom MaxIter``)."""
        return self._task_settings.opt_maxiter

    @opt_maxiter.setter
    def opt_maxiter(self, new_value: int | None) -> None:
        self._task_settings.opt_maxiter = new_value
