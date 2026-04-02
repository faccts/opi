#!/usr/bin/env python3
import pytest

from opi.core import Calculator
from opi.input.blocks import BlockGeom, BlockMdci, BlockMethod, BlockScf
from opi.input.simple_keywords import AuxBasisSet, Task, Wft
from opi.input.structures import Structure

"""
Contains ORCA examples of convergence failures to test OPI´s error handling capabilities.
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
def test_scf_fail(calc):
    """Test error_message for SCF failure"""
    calc.input.add_blocks(BlockScf(maxiter=1))
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == "SCF did not converge"


def test_cc_fail(calc):
    """Test error_message for CC not converging"""
    calc.input.add_blocks(BlockMdci(maxiter=1))
    calc.input.add_simple_keywords(Wft.CCSD_T)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == "Coupled-Cluster did not converge"


def test_dlpno_cc_fail(calc):
    """Test error_message for DLPNO-CC not converging"""
    calc.input.add_blocks(BlockMdci(maxiter=1))
    calc.input.add_simple_keywords(Wft.DLPNO_CCSD_T, AuxBasisSet.AUTOAUX)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == "Coupled-Cluster did not converge"


def test_opt_fail(calc):
    """Test error_message for optimization not converging"""
    calc.input.add_blocks(BlockGeom(maxiter=1))
    calc.input.add_simple_keywords(Task.OPT)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert output.terminated_normally()
    assert output.error_message() == "Geometry optimization did not converge"


def test_cpscf_fail(calc):
    """Test error_message for CP-SCF not converging"""
    calc.input.add_blocks(BlockMethod(z_maxiter=1))
    calc.input.add_simple_keywords(Task.FREQ)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == "CP-SCF did not converge"
