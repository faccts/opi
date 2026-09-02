import pytest

from examples.exmp003_opt.job import run_exmp003
from opi.input.structures import Structure
from opi.input.structures.atom import Atom
from opi.output.models.json.gbw.gbw_results import GbwResults
from tests.helpers import OutFileExporter


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.json_files
@pytest.mark.out_files
def test_exmp003_opt(
    example_input_file, tmp_path, json_files_exporter, out_file_exporter: OutFileExporter
) -> None:
    """Ensure optimization example runs successfully and produces a final energy and structure."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp003)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp003(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0
    # > Assert that a structure is available
    structure = output.get_structure()
    assert isinstance(structure, Structure), f"Expected Structure, got {type(structure).__name__}"

    # > Assert that the gbw JSON yields the same structure as the property JSON
    from_gbw = output.get_structure_from_gbw()
    assert isinstance(from_gbw, Structure), f"Expected Structure, got {type(from_gbw).__name__}"
    assert [atom.element for atom in from_gbw.atoms] == [atom.element for atom in structure.atoms]
    assert from_gbw.charge == structure.charge
    assert from_gbw.multiplicity == structure.multiplicity
    for gbw_atom, prop_atom in zip(from_gbw.atoms, structure.atoms):
        assert gbw_atom.coordinates.to_list() == pytest.approx(
            prop_atom.coordinates.to_list(), abs=1e-6
        )
    # > wB97X-3c puts an ECP on oxygen, which must not be mistaken for a ghost atom
    assert all(type(atom) is Atom for atom in from_gbw.atoms)

    # optional export of json files
    json_files_exporter.export_jsons_from(tmp_path)

    # optional export of .out fixture
    out_file_exporter.export_from(tmp_path / "job.out")

    # > Recreating the JSON from the binary gbw file must give the same structure again.
    # > Done after the exports so that the committed fixtures stay untouched by it.
    recreated = GbwResults.from_gbw_file(tmp_path / "job.gbw").get_structure()
    assert recreated is not None
    assert recreated.rmsd(from_gbw) == pytest.approx(0.0, abs=1e-6)
