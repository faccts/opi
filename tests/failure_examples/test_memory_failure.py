#!/usr/bin/env python3
import pytest

from opi.core import Calculator
from opi.input.blocks import BlockMdci
from opi.input.simple_keywords import BasisSet, Scf, Wft
from opi.input.structures import Structure
from opi.output.grepper.patterns import OOM_ERROR, TRIPLES_OOM_ERROR

"""
Contains ORCA examples of memory failures to test OPI´s error handling capabilities.
The functions error_message() will search in the ORCA output file for a respective error string and will compose the
error message we assert here.
"""


@pytest.fixture
def calc(tmp_path):
    """Create a calculator object with a water structure and return it."""
    calc = Calculator(basename="job", working_dir=tmp_path)
    calc.structure = Structure.from_smiles("O")
    return calc


@pytest.mark.orca
def test_scf_mem_fail(calc):
    """Test error_message for SCF memory failure"""
    calc.input.memory = 1
    calc.input.add_simple_keywords(BasisSet.DEF2_QZVPPD)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    print(output.error_message())
    assert not output.terminated_normally()
    assert (
        "Not enough memory available for SCF. Available:           1.0 MB" in output.error_message()
    )


@pytest.mark.orca
def test_mp2_mem_fail(calc):
    """Test error_message for MP2 memory failure"""
    calc.input.memory = 4
    calc.input.add_simple_keywords(Wft.MP2, BasisSet.DEF2_TZVP, Scf.NOITER)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == OOM_ERROR.message


@pytest.mark.orca
def test_cc_mem_fail(calc):
    """Test error_message for CC triples memory failure"""
    calc.input.memory = 1
    calc.input.add_simple_keywords(Wft.CCSD_T, BasisSet.DEF2_SVP, Scf.NOITER)
    calc.input.add_blocks(BlockMdci(maxcore=1))
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == TRIPLES_OOM_ERROR.message
