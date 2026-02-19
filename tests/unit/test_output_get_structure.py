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
