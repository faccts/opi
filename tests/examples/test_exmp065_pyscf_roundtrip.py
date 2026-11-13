# ruff: noqa: E402
import re

import pytest

# > example65 requires PySCF, which is not installed by default
# > skip test if PySCF is not available
pytest.importorskip("pyscf", reason="PySCF not installed")
pytestmark = pytest.mark.pyscf

from examples.exmp065_pyscf_roundtrip.job import run_exmp065
from opi.input.structures import Structure
from opi.output.core import Output


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.json_files
def test_exmp065_pyscf_roundtrip(example_input_file, tmp_path, json_files_exporter) -> None:
    """Ensure a heavy-element wavefunction survives the round trip ORCA -> PySCF -> ORCA."""
    input_file = example_input_file(run_exmp065)
    structure = Structure.from_xyz(input_file)

    output = run_exmp065(structure=structure, working_dir=tmp_path)

    reference = Output("job", working_dir=tmp_path, parse=True)
    e_reference = reference.get_final_energy()
    assert e_reference < 0

    # Assert PySCF reproduces ORCA's energy from ORCA's orbitals (basis set, ECP, AO order)
    mf = reference.results_gbw[0].to_pyscf()
    assert mf.mol.atom_nelec_core(0) == 60
    # > def2-TZVP is augmented by g and h functions
    assert max(mf.mol.bas_angular(i) for i in range(mf.mol.nbas)) == 5
    assert mf.energy_tot() == pytest.approx(e_reference, abs=1e-6)

    # Assert ORCA took the guess from PySCF's orbitals and converged immediately
    outfile_text = output.get_outfile().read_text()
    assert "INITIAL GUESS: MOREAD" in outfile_text
    cycles = re.search(r"SCF CONVERGED AFTER\s+(\d+)\s+CYCLES", outfile_text)
    assert cycles is not None
    assert int(cycles.group(1)) <= 3
    assert output.get_final_energy() == pytest.approx(e_reference, abs=1e-6)

    # optional export of json files (only those of the first calculation, the MORead calculation
    # runs in a subfolder)
    json_files_exporter.export_jsons_from(tmp_path)
