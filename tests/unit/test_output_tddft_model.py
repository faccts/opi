import pytest

from opi.output.models.json.gbw.properties.tddft import TdDft

"""
Unit tests for the `TdDft` gbw model

The committed JSON fixtures only cover a TDA calculation, which reports the amplitudes as `X`.
A full TD-DFT (RPA) calculation instead reports `X+Y` and `X-Y`, which is covered here.
"""


@pytest.mark.unit
@pytest.mark.output
def test_tddft_full_amplitudes():
    """Test that the `X+Y` and `X-Y` amplitudes of a full TD-DFT calculation are loaded."""
    td_dft = TdDft.model_validate(
        {
            "energy": 0.1437943154447575,
            "iroot": 1,
            "irrep": "A",
            "multiplicity": 1,
            "tda": "OFF",
            "orbwin": [1, 2, 3, 4],
            # > A row holding a single value is written as a plain number by ORCA
            "x+y": [0.0, [0.1, 0.2], [0.3, 0.4]],
            "x-y": [[0.5, 0.6], [0.7, 0.8]],
        }
    )

    assert td_dft.tda == "OFF"
    assert td_dft.irrep == "A"
    assert td_dft.multiplicity == 1
    assert td_dft.energy == pytest.approx(0.1437943154447575)
    assert td_dft.xy == [[0.0], [0.1, 0.2], [0.3, 0.4]]
    assert td_dft.x_minus_y == [[0.5, 0.6], [0.7, 0.8]]
    assert td_dft.x is None


@pytest.mark.unit
@pytest.mark.output
def test_tddft_tda_amplitudes():
    """Test that the `X` amplitudes of a TDA calculation are loaded."""
    td_dft = TdDft.model_validate({"tda": "ON", "x": [0.0, [0.1, 0.2]]})

    assert td_dft.x == [[0.0], [0.1, 0.2]]
    assert td_dft.xy is None
    assert td_dft.x_minus_y is None
