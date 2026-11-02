import pytest

from opi.core import Calculator

"""
This module contains tests for the `ncores` and `memory` properties of the `Input` class.
"""


@pytest.fixture
def empty_calc():
    """An empty instance of `Calculator`."""
    empty_calc = Calculator("test", version_check=False)
    return empty_calc


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize("ncores", [0, 4, None])
def test_ncores_valid(empty_calc: Calculator, ncores: int | None):
    """Test for `Input.ncores` setter with valid values."""
    empty_calc.input.ncores = ncores
    assert empty_calc.input.ncores == ncores


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize("ncores", ["4", 4.0, [4]])
def test_ncores_wrong_type(empty_calc: Calculator, ncores: object):
    """Test for `Input.ncores` setter with values of the wrong type."""
    with pytest.raises(TypeError):
        empty_calc.input.ncores = ncores


@pytest.mark.unit
@pytest.mark.input
def test_ncores_negative(empty_calc: Calculator):
    """Test for `Input.ncores` setter with an invalid negative value."""
    with pytest.raises(ValueError):
        empty_calc.input.ncores = -1


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize("memory", [0, 4000, None])
def test_memory_valid(empty_calc: Calculator, memory: int | None):
    """Test for `Input.memory` setter with valid values."""
    empty_calc.input.memory = memory
    assert empty_calc.input.memory == memory


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize("memory", ["4000", 4000.0, [4000]])
def test_memory_wrong_type(empty_calc: Calculator, memory: object):
    """Test for `Input.memory` setter with values of the wrong type."""
    with pytest.raises(TypeError):
        empty_calc.input.memory = memory


@pytest.mark.unit
@pytest.mark.input
def test_memory_negative(empty_calc: Calculator):
    """Test for `Input.memory` setter with an invalid negative value."""
    with pytest.raises(ValueError):
        empty_calc.input.memory = -1
