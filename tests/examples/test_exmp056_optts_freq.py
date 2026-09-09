import pytest

from examples.exmp056_optts_freq.job import run_exmp056
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp056_optts_freq(example_input_file, tmp_path) -> None:
    """Ensure OPTTS + NUMFREQ example runs and identifies the structure as a transition state."""
    input_file = example_input_file(run_exmp056)
    structure = Structure.from_xyz(input_file)

    output = run_exmp056(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0

    # Assert all frequencies are present
    frequencies = output.get_frequencies()
    assert isinstance(frequencies, dict)
    assert len(frequencies) > 0

    # Assert exactly one imaginary frequency
    imaginary = output.get_imaginary_frequencies()
    assert isinstance(imaginary, dict)
    assert len(imaginary) == 1

    # Assert structure is identified as a transition state
    assert output.is_pes_transition_state() is True
    assert output.is_pes_minimum() is False
