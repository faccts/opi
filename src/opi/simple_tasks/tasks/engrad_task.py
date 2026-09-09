import typing

from opi.input.simple_keywords import SimpleKeyword, Task
from opi.simple_tasks.simple_task import SimpleTask, TaskResults, TaskSettings


class EngradSettings(TaskSettings):
    """Task settings for energy + gradient calculations (``! ENGRAD``)."""

    _name: str = "engrad"
    task_keyword: typing.Annotated[SimpleKeyword, Task] = Task.ENGRAD


class EngradResults(TaskResults):
    """Results from an energy + gradient calculation."""

    @property
    def gradient(self) -> list[float]:
        """
        Cartesian gradient vector in Hartree/Bohr (flattened, atom-major order).

        Raises
        ------
        ValueError
            If the gradient is not present in the ORCA output.
        """
        gradient = self.output.get_gradient()

        if gradient is None:
            raise ValueError("Could not get gradient from ORCA Output")

        return gradient

    @property
    def primary_property(self) -> tuple[float, list[float]]:
        """``(final_energy, gradient)`` tuple."""
        return self.final_energy, self.gradient


class EngradTask(SimpleTask[EngradResults]):
    """
    Simple task for single-point energy and gradient calculations.

    Returns an ``EngradResults`` object containing the total energy and
    the Cartesian gradient vector.
    """

    _task_settings: EngradSettings
    _results_type = EngradResults
