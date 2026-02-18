import pytest

from opi.output.core import Output
from opi.output.models.json.property.properties.hirshfeld_population_analysis import (
    HirshfeldPopulationAnalysis,
)
from opi.output.models.json.property.properties.mayer_population_analysis import (
    MayerPopulationAnalysis,
)
from opi.output.models.json.property.properties.population_analysis import (
    ChelpgPopulationAnalysis,
    LoewdinPopulationAnalysis,
    MullikenPopulationAnalysis,
)

"""
Unit tests for Output population analysis poprerty getters

This module contains tests for the getters of population analysis related properties such as:
- Mulliken population analysis data
- Loewdin population analysis data
- ChelPG population analysis data
- Mayer population analysis data
- Hirshfeld population analysis data
- Mbis population analysis data
"""


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["opt"])
def test_get_mulliken(output_object_factory, task: str):
    """Test to check if `Output.get_mulliken()` returns `MullikenPopulationAnalysis` object."""
    output_object = output_object_factory(task)
    for mulliken in output_object.get_mulliken():
        assert isinstance(mulliken, MullikenPopulationAnalysis)


@pytest.mark.unit
@pytest.mark.output
def test_get_mulliken_returns_none(empty_output_object: Output):
    """Test to check if `Output.get_mulliken()` returns `None` when expected."""
    assert not empty_output_object.get_mulliken()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["rama"])
def test_get_loewdin(output_object_factory, task: str):
    """Test to check if `Output.get_loewdin()` returns `LoewdinPopulationAnalysis` object."""
    output_object = output_object_factory(task)
    for loewdin in output_object.get_loewdin():
        assert isinstance(loewdin, LoewdinPopulationAnalysis)


@pytest.mark.unit
@pytest.mark.output
def test_get_loewdin_returns_none(empty_output_object: Output):
    """Test if `Output.get_loewdin()` returns `None` when expected."""
    assert not empty_output_object.get_loewdin()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["pop_analysis"])
def test_get_chelpg(output_object_factory, task: str):
    """Test to check whether `Output.get_chelpg()` returns `ChelpgPopulationAnalysis` object."""
    output_object = output_object_factory(task)
    for chelpg in output_object.get_chelpg():
        assert isinstance(chelpg, ChelpgPopulationAnalysis)


@pytest.mark.unit
@pytest.mark.output
def test_get_chelpg_returns_none(empty_output_object: Output):
    """Test if `Output.get_chelpg()` returns `None` when expected."""
    assert not empty_output_object.get_loewdin()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["nmr"])
def test_get_mayer(output_object_factory, task: str):
    """Test to check whether `Output.get_mayer()` returns `MayerPopulationAnalysis` object."""
    output_object = output_object_factory(task)
    for loewdin in output_object.get_mayer():
        assert isinstance(loewdin, MayerPopulationAnalysis)


@pytest.mark.unit
@pytest.mark.output
def test_get_mayer_returns_none(empty_output_object: Output):
    """Test if `Output.get_mayer()` returns `None` when expected."""
    assert not empty_output_object.get_mayer()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["pop_analysis"])
def test_get_hirshfeld(output_object_factory, task: str):
    """Test if `Output.get_hirshfeld()` returns `HirshfeldPopulationAnalysis` object."""
    output_object = output_object_factory(task)
    for hirshfeld in output_object.get_hirshfeld():
        assert isinstance(hirshfeld, HirshfeldPopulationAnalysis)


@pytest.mark.unit
@pytest.mark.output
def test_get_hirshfeld_returns_none(empty_output_object: Output):
    """Test if `Output.get_hirshfeld()` returns `None` when expected."""
    assert not empty_output_object.get_hirshfeld()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task,length", [("pop_analysis", 3)])
def test_get_hirshfeld_length_of_list(output_object_factory, task: str, length: int):
    """Test if `Output.get_hirshfeld()` returns list of correct length."""
    output_object = output_object_factory(task)
    assert len(output_object.get_hirshfeld()) == length


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["pop_analysis"])
def test_get_mbis_returns_list(output_object_factory, task: str):
    """Test if `Output.get_mbis()` returns list."""
    output_object = output_object_factory(task)
    assert isinstance(output_object.get_mbis(), list)


@pytest.mark.unit
@pytest.mark.output
def test_get_mbis_returns_none(empty_output_object):
    """Test if `Output.get_mbis()` returns `None` when expected."""
    assert not empty_output_object.get_mbis()
