#!/usr/bin/env python3
"""
Tests for error extraction capabilities of OPI from the ORCA output with bad ORCA input.
Covers invalid lines, unknown simple keywords, unknown blocks, and invalid block options.
"""

import pytest

from opi.core import Calculator
from opi.input.blocks import BlockScf
from opi.input.structures import Structure
from opi.output.grepper.patterns import NO_COORDS_ERROR


@pytest.fixture
def calc(tmp_path):
    """Create a calculator object and return it."""
    calc = Calculator(basename="job", working_dir=tmp_path)
    return calc


@pytest.fixture
def calc_water(calc):
    """Create a calculator object with water as structure and return it."""
    calc.structure = Structure.from_smiles("O")
    return calc


@pytest.mark.orca
def test_no_coords(calc):
    """Test error_message for ORCA without coordinates"""
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == NO_COORDS_ERROR.message


@pytest.mark.orca
def test_invalid_line(calc_water):
    """Test error_message for ORCA with an invalid line in the input."""
    # > Add invalid line to input
    invalid_line = "invalid_line"
    calc_water.input.add_arbitrary_string(invalid_line)

    # > write the input and run the calculation
    calc_water.write_and_run()

    # > get the output and check some results
    output = calc_water.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == f"Invalid line starting with: {invalid_line.upper()}"


@pytest.mark.orca
def test_simple_keyword(calc_water):
    """Test error_message for ORCA with duplicate simple keywords."""
    # > Add invalid line to input
    simple_keyword = "! hf hf hf"
    calc_water.input.add_arbitrary_string(simple_keyword)

    # > write the input and run the calculation
    calc_water.write_and_run()

    # > get the output and check some results
    output = calc_water.get_output()
    assert not output.terminated_normally()
    # > Since one HF is duplicate ORCA only prints two instead of three
    assert output.error_message() == "Unknown/duplicate simple keyword(s): HF HF"


@pytest.mark.orca
def test_unknown_block(calc_water):
    """Test error_message for ORCA with an unknown block."""
    # > Add invalid line to input
    unknown_block = "%invalidblock"
    calc_water.input.add_arbitrary_string(unknown_block)

    # > write the input and run the calculation
    calc_water.write_and_run()

    # > get the output and check some results
    output = calc_water.get_output()
    assert not output.terminated_normally()
    # > Remove the % in the beginning and make it upper case
    assert output.error_message() == f"Unknown block: {unknown_block.upper()[1:]}"


@pytest.mark.orca
def test_unknown_block_key(calc_water):
    """Test error_message for ORCA with an unknown block key."""
    # > Add invalid line to input
    scf_block = BlockScf()
    invalid_key = "invalid_key"
    scf_block.add_option(name=invalid_key, val="none")
    calc_water.input.add_blocks(scf_block)

    # > write the input and run the calculation
    calc_water.write_and_run()

    # > get the output and check some results
    output = calc_water.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == f"Unknown block key:  {invalid_key.upper()}"


@pytest.mark.orca
def test_unknown_block_value(calc_water):
    """Test error_message for ORCA with an unknown block value."""

    # > Add invalid line to input
    scf_block = BlockScf()
    invalid_value = "invalid_value"
    scf_block.add_option(name="maxiter", val=invalid_value)
    calc_water.input.add_blocks(scf_block)

    # > write the input and run the calculation
    calc_water.write_and_run()

    # > get the output and check some results
    output = calc_water.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == f"Unknown block value:  {invalid_value.upper()}"
