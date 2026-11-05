import pytest

from opi.output.models.json.property.properties.spectrum import AbsorptionSpectrum, EcdSpectrum

"""
Unit tests for the column properties of the `AbsorptionSpectrum` and `EcdSpectrum` models

The rows are taken from a full TD-DFT calculation (CAM-B3LYP/def2-TZVP) of the degenerate
1E1u state of benzene, in which the transition dipole moment lies along x.
"""

ABSORPTION_ROW = [
    7.174372,
    57865.220208,
    172.81538,
    0.605396,
    3.444271,
    -1.855875,
    0.0,
    -0.000662,
    0.0,
    1e-06,
    0.0,
]
ECD_ROW = [7.174372, 57865.220208, 172.81538, 0.002056, 2e-06, 0.1, 6e-06, 0.2, -1e-06, 0.3]


@pytest.mark.unit
@pytest.mark.output
def test_absorption_spectrum_columns():
    """Test that the properties of `AbsorptionSpectrum` return the correct columns."""
    spectrum = AbsorptionSpectrum.model_validate(
        {"representation": "Length", "ntrans": 2, "excitationenergies": [ABSORPTION_ROW] * 2}
    )

    assert spectrum.energies_ev == [7.174372] * 2
    assert spectrum.energies_cm == [57865.220208] * 2
    assert spectrum.wavelengths_nm == [172.81538] * 2
    assert spectrum.oscillator_strengths == [0.605396] * 2
    assert spectrum.transition_moments_squared == [3.444271] * 2
    assert spectrum.transition_moments == [(-1.855875 + 0j, -0.000662 + 0j, 1e-06 + 0j)] * 2


@pytest.mark.unit
@pytest.mark.output
def test_ecd_spectrum_columns():
    """Test that the properties of `EcdSpectrum` return the correct columns."""
    spectrum = EcdSpectrum.model_validate(
        {"representation": "Length", "ntrans": 1, "excitationenergies": [ECD_ROW]}
    )

    assert spectrum.energies_ev == [7.174372]
    assert spectrum.wavelengths_nm == [172.81538]
    assert spectrum.rotatory_strengths == [0.002056]
    assert spectrum.magnetic_transition_moments == [(2e-06 + 0.1j, 6e-06 + 0.2j, -1e-06 + 0.3j)]


@pytest.mark.unit
@pytest.mark.output
def test_spectrum_columns_none():
    """Test that the properties return None if the output contains no excitation energies."""
    absorption = AbsorptionSpectrum.model_validate({})
    ecd = EcdSpectrum.model_validate({})

    assert absorption.energies_ev is None
    assert absorption.oscillator_strengths is None
    assert absorption.transition_moments is None
    assert ecd.rotatory_strengths is None
    assert ecd.magnetic_transition_moments is None


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["uvvis", "roci"])
def test_absorption_spectrum_consistent(output_object_factory, task: str):
    """Test that the squared transition moments match the parsed transition moments."""
    output_object = output_object_factory(task)
    for spectrum in output_object.get_absorption_spectrum():
        assert isinstance(spectrum, AbsorptionSpectrum)
        assert len(spectrum.oscillator_strengths) == spectrum.ntrans
        for moment, squared in zip(
            spectrum.transition_moments, spectrum.transition_moments_squared
        ):
            assert sum(abs(component) ** 2 for component in moment) == pytest.approx(
                squared, abs=1e-6
            )
