import shutil
from functools import partialmethod
from pathlib import Path

import pytest

from opi.core import Calculator
from opi.input.blocks import BlockNeb
from opi.input.simple_keywords import Neb
from opi.input.structures import Structure
from opi.output.core import Output
from opi.simple_tasks import NebResults, NebTask, SqmSettings
from opi.simple_tasks.simple_task import SimpleTask

"""
Unit tests for `NebTask`, `NebSettings` and `NebResults`:
- NebSettings maps to `! NEB-CI` and the typed `%neb` fields
- NebTask.add_product() writes the product and sets `%neb Neb_End_XYZFile` for one run only
- NebTask.add_product() rejects a product whose atoms do not match the reactant
- NebTask.run() requires the product as keyword argument and passes it to ORCA
- NebResults reads the minimal energy pathway from a `_MEP_trj.xyz` file of a real ORCA run
  (GFN2-xTB NEB-CI of the ethane rotation, as run by examples/exmp065_neb_simpletask)
- NebResults.status requires normal termination and NEB convergence, but no "SUCCESS"
"""

# > Number of images in the fixture: 8 intermediate images plus both endpoints
N_IMAGES = 10
# > Energies of the images in the fixture, as printed in its comment lines
FIXTURE_ENERGIES = [
    -7.336370676790,
    -7.335053872010,
    -7.333672441410,
    -7.332767249290,
    -7.332302566140,
    -7.332283228120,
    -7.332722897700,
    -7.333629629510,
    -7.335028026410,
    -7.336370669830,
]


@pytest.fixture
def ethane() -> Structure:
    return Structure.from_lists(
        ["C", "C", "H", "H", "H", "H", "H", "H"],
        [
            (-0.766, 0.000, 0.000),
            (0.766, 0.000, 0.000),
            (-1.158, 1.004, -0.137),
            (-1.158, -0.621, -0.801),
            (-1.158, -0.384, 0.938),
            (1.158, 0.579, 0.832),
            (1.158, -1.010, 0.086),
            (1.158, 0.431, -0.918),
        ],
    )


@pytest.fixture
def no_orca(monkeypatch: pytest.MonkeyPatch) -> None:
    """Skip contacting the ORCA binary, on `Calculator` construction and on execution alike."""
    monkeypatch.setattr(
        SimpleTask,
        "make_calculator",
        partialmethod(SimpleTask.make_calculator, version_check=False),
    )
    monkeypatch.setattr(Calculator, "write_and_run", lambda self: True)


def _calculator(working_dir: Path, structure: Structure | None = None) -> Calculator:
    calculator = Calculator("job", working_dir=working_dir, version_check=False)
    if structure is not None:
        calculator.structure = structure
    return calculator


def _results_from_fixture(
    fixtures_dir: Path, tmp_path: Path, structure: Structure | None = None
) -> NebResults:
    shutil.copy(fixtures_dir / "neb" / "job_MEP_trj.xyz", tmp_path / "job_MEP_trj.xyz")
    return NebResults(calculator=_calculator(tmp_path, structure), _method_family=SqmSettings)


# ---------------------------------------------------------------------------
# NebSettings
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.simpletasks
def test_neb_settings_default_keyword() -> None:
    """The task defaults to the climbing-image NEB without any `%neb` block."""
    task = NebTask(method="gfn2-xtb")

    assert Neb.NEB_CI in task.input.simple_keywords
    assert task.input.get_block(BlockNeb) is None


@pytest.mark.unit
@pytest.mark.simpletasks
def test_neb_settings_block_fields() -> None:
    """The typed fields map onto the corresponding options of the `%neb` block."""
    task = NebTask(
        method="gfn2-xtb",
        task_settings={
            "nimages": 6,
            "neb_maxiter": 100,
            "preopt_ends": True,
            "interpolation": "idpp",
        },
    )

    block = task.input.get_block(BlockNeb)
    assert isinstance(block, BlockNeb)
    assert block.nimages == 6
    assert block.maxiter == 100
    assert block.preopt_ends is True
    assert block.interpolation == "idpp"


@pytest.mark.unit
@pytest.mark.simpletasks
def test_neb_task_property_forwarding() -> None:
    """The convenience properties of the task read from and write to its settings."""
    task = NebTask(method="gfn2-xtb")
    task.nimages = 4
    task.neb_maxiter = 50
    task.preopt_ends = False
    task.interpolation = "linear"

    block = task.input.get_block(BlockNeb)
    assert isinstance(block, BlockNeb)
    assert (block.nimages, block.maxiter, block.preopt_ends, block.interpolation) == (
        4,
        50,
        False,
        "linear",
    )


# ---------------------------------------------------------------------------
# NebTask.add_product() / NebTask.run()
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.simpletasks
def test_add_product_sets_end_file(tmp_path: Path, ethane: Structure) -> None:
    """The product is written next to the input and referenced from the `%neb` block."""
    task = NebTask(method="gfn2-xtb", task_settings={"nimages": 6})
    calculator = task.make_calculator("job", ethane, tmp_path, version_check=False)

    product_file = NebTask.add_product(calculator, ethane)

    assert product_file == tmp_path / "job_product.xyz"
    assert len(Structure.from_xyz(product_file)) == len(ethane)
    block = calculator.input.get_block(BlockNeb)
    assert isinstance(block, BlockNeb)
    assert block.neb_end_xyzfile is not None
    assert block.neb_end_xyzfile.file == Path("job_product.xyz")
    # > Settings of the task in the same block are kept
    assert block.nimages == 6
    # > The product does not stick to the task
    task_block = task.input.get_block(BlockNeb)
    assert isinstance(task_block, BlockNeb)
    assert task_block.neb_end_xyzfile is None


@pytest.mark.unit
@pytest.mark.simpletasks
@pytest.mark.parametrize(
    "elements",
    [
        ["C", "C", "H", "H", "H", "H", "H"],
        ["C", "H", "C", "H", "H", "H", "H", "H"],
    ],
    ids=["atom_count", "atom_order"],
)
def test_add_product_rejects_mismatched_atoms(
    tmp_path: Path, ethane: Structure, elements: list[str]
) -> None:
    """A product with other atoms, or the same atoms in another order, is rejected."""
    product = Structure.from_lists(elements, [(float(i), 0.0, 0.0) for i in range(len(elements))])
    calculator = NebTask(method="gfn2-xtb").make_calculator(
        "job", ethane, tmp_path, version_check=False
    )

    with pytest.raises(ValueError, match="same atoms"):
        NebTask.add_product(calculator, product)
    assert not (tmp_path / "job_product.xyz").exists()


@pytest.mark.unit
@pytest.mark.simpletasks
def test_run_requires_product_as_keyword(tmp_path: Path, ethane: Structure) -> None:
    """The product can only be passed by keyword."""
    task = NebTask(method="gfn2-xtb")

    with pytest.raises(TypeError):
        task.run("job", ethane, ethane)  # type: ignore[misc]


@pytest.mark.unit
@pytest.mark.simpletasks
def test_run_writes_product_into_input(tmp_path: Path, ethane: Structure, no_orca: None) -> None:
    """`run()` hands the product to ORCA, and a second run does not inherit it."""
    task = NebTask(method="gfn2-xtb")
    working_dir = tmp_path / "RUN"

    results = task.run("job", ethane, product=ethane, working_dir=working_dir)

    assert isinstance(results, NebResults)
    assert (working_dir / "job_product.xyz").is_file()
    block = results.calculator.input.get_block(BlockNeb)
    assert isinstance(block, BlockNeb)
    assert block.neb_end_xyzfile is not None
    assert task.input.get_block(BlockNeb) is None


# ---------------------------------------------------------------------------
# NebResults
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.simpletasks
def test_neb_results_pathway(fixtures_dir: Path, tmp_path: Path) -> None:
    """Structures and energies of all images are read from the `_MEP_trj.xyz` file."""
    results = _results_from_fixture(fixtures_dir, tmp_path)

    structures, energies = results.primary_property

    assert len(structures) == N_IMAGES
    assert all(len(structure) == 8 for structure in structures)
    assert energies == pytest.approx(FIXTURE_ENERGIES, abs=1e-12)


@pytest.mark.unit
@pytest.mark.simpletasks
def test_neb_results_highest_image(fixtures_dir: Path, tmp_path: Path) -> None:
    """The highest image is the climbing image in the middle of the ethane rotation."""
    results = _results_from_fixture(fixtures_dir, tmp_path)

    assert results.highest_image_index == 5
    assert results.highest_energy == pytest.approx(-7.332283228120, abs=1e-12)
    assert results.highest_structure.to_xyz_block() == results.structures[5].to_xyz_block()


@pytest.mark.unit
@pytest.mark.simpletasks
def test_neb_results_charge_multiplicity_from_reactant(fixtures_dir: Path, tmp_path: Path) -> None:
    """The images carry the charge and multiplicity of the reactant."""
    reactant = Structure.from_lists(["H"], [(0.0, 0.0, 0.0)], charge=1, multiplicity=3)
    results = _results_from_fixture(fixtures_dir, tmp_path, reactant)

    assert {(s.charge, s.multiplicity) for s in results.structures} == {(1, 3)}


@pytest.mark.unit
@pytest.mark.simpletasks
def test_neb_results_missing_file(tmp_path: Path) -> None:
    """Without a `_MEP_trj.xyz` file, the getters raise a ValueError."""
    results = NebResults(calculator=_calculator(tmp_path), _method_family=SqmSettings)

    with pytest.raises(ValueError):
        _ = results.structures
    with pytest.raises(ValueError):
        _ = results.energies


# ---------------------------------------------------------------------------
# NebResults.status
# ---------------------------------------------------------------------------

# > Sentinels of the health checks, see `test_simpletasks_status.py`. The main output of a
# > NEB-CI run contains no "SUCCESS", since the SCFs of the images are not printed there.
NEB_CONVERGED = "H U R R A Y\n"
TERMINATED_NORMALLY = "****ORCA TERMINATED NORMALLY****\n"


@pytest.mark.unit
@pytest.mark.simpletasks
@pytest.mark.parametrize(
    "content,expected",
    [
        (NEB_CONVERGED + TERMINATED_NORMALLY, True),
        (TERMINATED_NORMALLY, False),
        (NEB_CONVERGED, False),
    ],
    ids=["converged", "neb_not_converged", "not_terminated"],
)
def test_neb_results_status(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, content: str, expected: bool
) -> None:
    """`status` needs normal termination and NEB convergence, but no SCF "SUCCESS"."""
    (tmp_path / "job.out").write_text(content)
    output = Output("job", working_dir=tmp_path, version_check=False)
    monkeypatch.setattr(NebResults, "output", property(lambda self: output))

    results = NebResults(calculator=_calculator(tmp_path), _method_family=SqmSettings)

    assert results.status is expected
