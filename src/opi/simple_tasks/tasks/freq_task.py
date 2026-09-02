import typing

from opi.input.simple_keywords import SimpleKeyword, Task
from opi.simple_tasks.simple_task import SimpleTask, TaskResults, TaskSettings


class FreqSettings(TaskSettings):
    """Task settings for frequency calculations (``! FREQ``)."""

    _name: str = "freq"
    task_keyword: typing.Annotated[SimpleKeyword, Task] = Task.FREQ


class FreqResults(TaskResults):
    """Results from a harmonic frequency calculation."""

    @property
    def status(self) -> bool:
        """``True`` if the job terminated normally (SCF convergence not re-checked)."""
        return self.output.terminated_normally()

    @property
    def free_energy_delta(self) -> float:
        """
        Thermal free-energy correction (ΔG) in Hartree.

        Raises
        ------
        ValueError
            If the free-energy correction is not present in the ORCA output.
        """
        free_energy_delta = self.output.get_free_energy_delta()

        if free_energy_delta is None:
            raise ValueError("Could not get free energy delta from ORCA output")

        return free_energy_delta

    @property
    def primary_property(self) -> float:
        """Alias for ``free_energy_delta``."""
        return float(self.free_energy_delta)


class FreqTask(SimpleTask[FreqResults]):
    """
    Task for harmonic frequency calculations.

    Returns a ``FreqResults`` object.  ``status`` is ``True`` when the job
    terminated normally (SCF convergence is not checked separately because
    frequency jobs always follow an SCF step).
    """

    _task_settings: FreqSettings
    _results_type = FreqResults
