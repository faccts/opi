import os
import typing
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockNeb
from opi.input.blocks.util import InputFilePath
from opi.input.simple_keywords import Neb, ORCAKeyword
from opi.input.structures import Atom, BaseStructureFile, Properties, Structure
from opi.simple_tasks.simple_task import SimpleTask, TaskResults, TaskSettings
from opi.utils.element import Element


class NebSettings(TaskSettings):
    """
    Task settings for climbing-image nudged elastic band calculations (``! NEB-CI``).

    The NEB yields the minimal energy pathway between a reactant and a product structure.
    No transition-state optimization is done afterwards; with the climbing image, the highest
    image of the converged path approximates the saddle point.
    """

    _name: str = "neb"
    task_keyword: typing.Annotated[ORCAKeyword, Neb] = Neb.NEB_CI
    nimages: typing.Annotated[int, "neb", "nimages"] | None = None
    neb_maxiter: typing.Annotated[int, "neb", "maxiter"] | None = None
    preopt_ends: typing.Annotated[bool, "neb", "preopt_ends"] | None = None
    interpolation: (
        typing.Annotated[
            typing.Literal[
                "linear",
                "idpp",
                "xtb",
                "xtbts",
                "xtb0",
                "xtb0ts",
                "xtb1",
                "xtb1ts",
                "xtb2",
                "xtb2ts",
            ],
            "neb",
            "interpolation",
        ]
        | None
    ) = None


class NebResults(TaskResults):
    """
    Results from a nudged elastic band calculation.

    The minimal energy pathway is read from the ``<basename>_MEP_trj.xyz`` file, which holds
    all images of the converged path including both endpoints.
    """

    @property
    def _mep_file(self) -> Path:
        # > Taken from the calculator, since `TaskResults.output` parses all JSON files.
        return self.calculator.working_dir / f"{self.calculator.basename}_MEP_trj.xyz"

    @property
    def structures(self) -> list[Structure]:
        """
        Structures of all images along the minimal energy pathway, from reactant to product.

        Charge and multiplicity are taken from the reactant structure, if it is a ``Structure``.

        Raises
        ------
        ValueError
            If the structures could not be obtained from the ORCA output.
        """
        reactant = self.calculator.structure
        charge, multiplicity = 0, 1
        if isinstance(reactant, Structure):
            charge = reactant.charge if reactant.charge is not None else charge
            if reactant.multiplicity is not None:
                multiplicity = reactant.multiplicity

        try:
            return Structure.from_trj_xyz(self._mep_file, charge=charge, multiplicity=multiplicity)
        except (FileNotFoundError, ValueError, EOFError):
            raise ValueError("Could not obtain the NEB images from the ORCA output")

    @property
    def energies(self) -> list[float]:
        """
        Total energies in Hartree of all images along the minimal energy pathway.

        Raises
        ------
        ValueError
            If the energies could not be obtained from the ORCA output.
        """
        try:
            properties = Properties.from_trj_xyz(self._mep_file, mode="neb")
        except (FileNotFoundError, ValueError, EOFError):
            raise ValueError("Could not obtain the NEB image energies from the ORCA output")

        energies = [p.energy_total for p in properties]
        if any(energy is None for energy in energies):
            raise ValueError("Could not obtain the NEB image energies from the ORCA output")

        return typing.cast(list[float], energies)

    @property
    def primary_property(self) -> tuple[list[Structure], list[float]]:
        """``(structures, energies)`` tuple describing the minimal energy pathway."""
        return self.structures, self.energies

    @property
    def highest_image_index(self) -> int:
        """
        Index of the image with the highest energy along the minimal energy pathway.

        The endpoints are included, so for a path without a barrier this can be the index
        of the reactant or the product.
        """
        energies = self.energies
        return energies.index(max(energies))

    @property
    def highest_energy(self) -> float:
        """Total energy in Hartree of the highest image along the minimal energy pathway."""
        return max(self.energies)

    @property
    def highest_structure(self) -> Structure:
        """Structure of the highest image along the minimal energy pathway."""
        return self.structures[self.highest_image_index]

    @property
    def status(self) -> bool:
        """
        ``True`` if the job terminated normally and the NEB converged.

        The method-specific convergence check of ``TaskResults.status`` is skipped: the SCFs
        of the images are not printed to the main output file, so it would always fail.
        Instead, ORCA itself aborts the NEB if an image does not converge
        (``%neb CheckSCFConv``, on by default).
        """
        output = self.output
        return output.terminated_normally() and output.neb_converged()


def _atom_signature(structure: Structure) -> list[tuple[type, Element | None]]:
    """Type and element of every atom, which reactant and product of a NEB must share."""
    return [(type(a), a.element if isinstance(a, Atom) else None) for a in structure.atoms]


class NebTask(SimpleTask[NebResults]):
    """
    Simple task for finding the minimal energy pathway with the nudged elastic band method.

    The calculation is double-ended: next to the reactant, ``NebTask.run()`` requires the
    product structure. No transition-state optimization follows the NEB. Exposes convenience
    properties (``nimages``, ``neb_maxiter``, ``preopt_ends``, ``interpolation``) that forward
    to the underlying ``NebSettings`` object.
    """

    _task_settings: NebSettings
    _results_type = NebResults

    @property
    def nimages(self) -> int | None:
        """Number of images between the endpoints (``%neb NImages``)."""
        return self._task_settings.nimages

    @nimages.setter
    def nimages(self, new_value: int | None) -> None:
        self._task_settings.nimages = new_value

    @property
    def neb_maxiter(self) -> int | None:
        """Maximum number of NEB iterations (``%neb MaxIter``)."""
        return self._task_settings.neb_maxiter

    @neb_maxiter.setter
    def neb_maxiter(self, new_value: int | None) -> None:
        self._task_settings.neb_maxiter = new_value

    @property
    def preopt_ends(self) -> bool | None:
        """Whether reactant and product are optimized before the NEB (``%neb PreOpt_Ends``)."""
        return self._task_settings.preopt_ends

    @preopt_ends.setter
    def preopt_ends(self, new_value: bool | None) -> None:
        self._task_settings.preopt_ends = new_value

    @property
    def interpolation(self) -> str | None:
        """Method to generate the initial path (``%neb Interpolation``)."""
        return self._task_settings.interpolation

    @interpolation.setter
    def interpolation(self, new_value: str | None) -> None:
        self._task_settings.interpolation = new_value  # type:ignore

    @staticmethod
    def add_product(calculator: Calculator, product: Structure) -> Path:
        """
        Write the product structure into the working directory of ``calculator`` and point
        ``%neb Neb_End_XYZFile`` of its input to it.

        Only the input of ``calculator`` is changed, so the product does not stick to the task.
        Any product already set in that input is replaced.

        Parameters
        ----------
        calculator : Calculator
            The calculator of the NEB run, as built by ``SimpleTask.make_calculator()``.
        product : Structure
            The product structure. Its atoms must match those of the reactant in number,
            element and order.

        Returns
        -------
        Path
            The written product XYZ file.

        Raises
        ------
        ValueError
            If the atoms of the product do not match those of the reactant.
        """
        reactant = calculator.structure
        if isinstance(reactant, Structure):
            if _atom_signature(reactant) != _atom_signature(product):
                raise ValueError(
                    "Reactant and product must contain the same atoms in the same order."
                )

        product_file = calculator.working_dir / f"{calculator.basename}_product.xyz"
        product_file.write_text(product.to_xyz_block())

        block = typing.cast(BlockNeb, calculator.input.get_block(BlockNeb, create_missing=True))
        block.neb_end_xyzfile = InputFilePath(file=Path(product_file.name))

        return product_file

    def run(  # type: ignore[override]
        self,
        basename: str,
        structure: Structure | BaseStructureFile,
        *,
        product: Structure,
        working_dir: Path | str | os.PathLike[str] = Path("RUN"),
        ncores: int | None = None,
        memory: int | None = None,
        moinp: Path | None = None,
        strict: bool = False,
    ) -> NebResults:
        """
        Run the NEB between the reactant ``structure`` and ``product``.

        Works like ``SimpleTask.run()``, but additionally hands the product to the calculation
        through ``NebTask.add_product()`` before ORCA is executed.

        Parameters
        ----------
        basename : str
            Base name for the calculation.
        structure : Structure or BaseStructureFile
            The reactant structure.
        product : Structure
            The product structure. Its atoms must match those of the reactant in number,
            element and order.
        working_dir : pathlib.Path or str or os.PathLike, optional
            Directory in which the calculation will be executed. Defaults to "RUN".
        ncores : int, optional
            Number of CPU cores to use. Overrides the value held by the task's input.
        memory : int, optional
            Amount of memory to allocate. Overrides the value held by the task's input.
        moinp : pathlib.Path, optional
            Path to a molecular orbital input file. Overrides the value held by the task's input.
        strict : bool, optional
            If True, ``working_dir`` must already exist and be empty. If False (the default),
            ``working_dir`` is deleted and recreated, so any existing content is lost.

        Returns
        -------
        NebResults
            The minimal energy pathway and its highest image.

        Raises
        ------
        ValueError
            If the atoms of the product do not match those of the reactant.
        """
        working_dir = self.prepare_working_dir(working_dir, strict=strict)
        calculator = self.make_calculator(basename, structure, working_dir, ncores, memory, moinp)
        self.add_product(calculator, product)
        self.execute(calculator)

        return self.make_results(calculator)
