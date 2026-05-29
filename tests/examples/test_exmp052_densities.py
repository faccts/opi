import numpy as np
import pytest

from examples.exmp052_densities.job import run_exmp052
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.json_files
def test_exmp052_densities(example_input_file, tmp_path, json_files_exporter) -> None:
    """Ensure SCF density example runs successfully and allows access to densities."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp052)
    structure = Structure.from_xyz(input_file, charge=1)
    structure.set_ls_multiplicity()

    # Run the example in tmp_path
    output = run_exmp052(structure=structure, working_dir=tmp_path)

    # Assert that densities can be obtained

    # scfp
    scfp = output.get_scf_density(recreate_json=True)
    assert isinstance(scfp, np.ndarray)
    assert scfp.dtype == np.float64
    assert scfp.ndim == 2

    # scfr
    scfr = output.get_scf_spin_density(recreate_json=True)
    assert isinstance(scfr, np.ndarray)
    assert scfr.dtype == np.float64
    assert scfr.ndim == 2

    # optional export of json files
    json_files_exporter.export_jsons_from(tmp_path)
