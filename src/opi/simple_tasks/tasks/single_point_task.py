import typing

from opi.input.simple_keywords import SimpleKeyword, Task
from opi.simple_tasks.simple_task import SimpleTask, TaskResults, TaskSettings


class SinglePointSettings(TaskSettings):
    """Task settings for a single-point energy calculation (``! SP``)."""

    _name: str = "singlepoint"
    task_keyword: typing.Annotated[SimpleKeyword, Task] = Task.SP


class SinglePointResults(TaskResults):
    """Results from a single-point energy calculation."""

    @property
    def primary_property(self) -> float:
        """Alias for ``final_energy``."""
        return float(self.final_energy)


class SinglePointTask(SimpleTask[SinglePointResults]):
    """
    Simple task for single-point energy calculations.

    Configures ORCA with the ``SP`` keyword and returns a
    ``SinglePointResults`` object whose ``final_energy`` attribute holds the
    total energy in Hartree.
    """

    _task_settings: SinglePointSettings
    _results_type = SinglePointResults
