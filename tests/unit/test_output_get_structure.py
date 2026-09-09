import pytest

from opi.input.structures import Structure
from opi.output.core import Output

"""
Unit tests for Output structure getters.

This module contains tests for structure-related getters for attributes such as:
- Gradients at either default or specified index
- Structure data with or without fragments
"""


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["mp2"])
def test_get_gradient_default_index(output_object_factory, task: str):
    """Test to check if `Output.get_gradient()` returns None when expected."""
    output_object = output_object_factory(task)
    assert not output_object.get_gradient()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "task, index",
    [("opt", 0), ("opt", 1)],
)
def test_get_gradient_with_index(output_object_factory, task: str, index: int):
    """Test to check if `Output.get_gradient()` returns expected values when given index."""
    output_object = output_object_factory(task)
    assert isinstance(output_object.get_gradient(index=index), list)


@pytest.mark.unit
@pytest.mark.output
def test_get_gradient_returns_none(empty_output_object: Output):
    """Test if `Output.get_gradient()` returns `None` when expected."""
    assert not empty_output_object.get_gradient()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["opt", "led"])
def test_get_structure_no_fragments(output_object_factory, task: str):
    """Test to check if `Output.get_structure()` returns `Structure` object."""
    output_object = output_object_factory(task)
    assert isinstance(output_object.get_structure(), Structure)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led"])
def test_get_structure_with_fragments(output_object_factory, task: str):
    """Test to check if `Output.get_structure()` returns `Structure` object with fragment ids when `with_fragments=True`."""
    output_object = output_object_factory(task)
    structure = output_object.get_structure(with_fragments=True)
    for atom in structure.atoms:
        assert atom.fragment_id


@pytest.mark.unit
@pytest.mark.output
def test_get_structure_returns_none(empty_output_object: Output):
    """Test if `Output.get_structure()` returns `None` when expected."""
    assert not empty_output_object.get_structure()


@pytest.mark.unit
@pytest.mark.output
def test_get_structure_fallback(output_no_json):
    """Test that `get_structure()` falls back to grepping the .out file when no JSON is present."""
    structure = output_no_json.get_structure()
    assert isinstance(structure, Structure)
    assert len(structure.atoms) == 3


@pytest.mark.unit
@pytest.mark.output
def test_get_structure_fallback_index(output_no_json):
    """Test that grepper fallback respects the index argument and returns different geometries."""
    s0 = output_no_json.get_structure(index=0)
    s_last = output_no_json.get_structure(index=-1)
    assert isinstance(s0, Structure)
    assert isinstance(s_last, Structure)
    assert s0.atoms[0].coordinates != s_last.atoms[0].coordinates


@pytest.mark.unit
@pytest.mark.output
def test_get_structure_no_fallback(output_no_json):
    """Test that `get_structure(fallback=False)` returns None when no JSON is present."""
    assert output_no_json.get_structure(fallback=False) is None


@pytest.mark.unit
@pytest.mark.output
def test_get_gradient_fallback(output_no_json):
    """Test that `get_gradient()` falls back to grepping the .out file when no JSON is present."""
    gradient = output_no_json.get_gradient(index=0)
    assert isinstance(gradient, list)
    assert len(gradient) == 9  # 3 atoms * 3 components


@pytest.mark.unit
@pytest.mark.output
def test_get_gradient_no_fallback(output_no_json):
    """Test that `get_gradient(fallback=False)` returns None when no JSON is present."""
    assert output_no_json.get_gradient(index=0, fallback=False) is None
