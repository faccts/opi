import typing

from opi.input import Input
from opi.input.simple_keywords import Goat, SimpleKeyword
from opi.input.structures import Properties, Structure
from opi.simple_tasks.simple_task import SimpleTask, TaskResults, TaskSettings


class GoatSettings(TaskSettings):
    """
    Task settings for GOAT conformer-ensemble explorations (``! GOAT``).

    The boolean flags ``goat_react``, ``goat_diversity``, and
    ``goat_explore`` enable the corresponding ORCA keywords; ``goat_maxiter``
    controls the maximum number of GOAT iterations via ``%goat MaxIter``.
    """

    _name: str = "goat"
    task_keyword: typing.Annotated[SimpleKeyword, Goat] = Goat.GOAT
    goat_maxiter: typing.Annotated[int, "goat", "maxiter"] | None = None
    goat_react: bool | None = None
    goat_diversity: bool | None = None
    goat_explore: bool | None = None

    def map_to_input(self) -> Input:
        """
        Extend the base mapping with GOAT-specific keywords.

        Appends ``GOAT_REACT``, ``GOAT_DIVERSITY``, or ``GOAT_EXPLORE`` when
        the corresponding flag is ``True``.

        Returns
        -------
        Input
            Modified ``Input`` object.
        """
        input_object = super().map_to_input()

        if self.goat_react:
            input_object.add_simple_keywords(Goat.GOAT_REACT)

        if self.goat_diversity:
            input_object.add_simple_keywords(Goat.GOAT_DIVERSITY)

        if self.goat_explore:
            input_object.add_simple_keywords(Goat.GOAT_EXPLORE)

        return input_object


class GoatResults(TaskResults):
    """Results from a GOAT conformer-ensemble generation."""

    @property
    def structures(self) -> list[Structure]:
        """
        All structures in the final conformer ensemble.

        Raises
        ------
        ValueError
            If the structures could not be obtained from the ORCA Output.
        """
        try:
            structures = Structure.from_trj_xyz(
                self.output.working_dir / f"{self.output.basename}.finalensemble.xyz"
            )
        except (FileNotFoundError, ValueError, EOFError):
            raise ValueError("Could not obtain conformer structures from the ORCA Output")
        return structures

    @property
    def properties(self) -> list[Properties]:
        """
        Per-conformer properties (energies, …) from the final ensemble file.

        Raises
        ------
        ValueError
            If the properties could not be obtained from the ORCA Output.
        """
        try:
            properties = Properties.from_trj_xyz(
                self.output.working_dir / f"{self.output.basename}.finalensemble.xyz", mode="goat"
            )
        except (FileNotFoundError, ValueError, EOFError):
            raise ValueError("Could not obtain conformer energies from the ORCA Output")
        return properties

    @property
    def primary_property(self) -> tuple[list[Structure], list[Properties]]:
        """``(structures, properties)`` tuple for the final conformer ensemble."""
        return self.structures, self.properties


class GoatTask(SimpleTask[GoatResults]):
    """
    Simple task for GOAT conformer-ensemble generation.

    Returns a ``GoatResults`` object containing the ensemble structures and
    their associated properties read from the ``.finalensemble.xyz`` file.
    """

    _task_settings: GoatSettings
    _results_type = GoatResults
