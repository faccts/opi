#!/usr/bin/env python3
"""
Tests for error extraction capabilities of OPI.
Covers SCF, coupled-cluster, geometry optimization, and CP-SCF convergence failures.
"""

import pytest

from opi.core import Calculator
from opi.input.blocks import BlockGeom, BlockMdci, BlockMethod, BlockScf
from opi.input.simple_keywords import AuxBasisSet, Task, Wft
from opi.input.structures import Structure
from opi.output.grepper.patterns import (
    CC_NOT_CONVERGED_ERROR,
    CPSCF_NOT_CONVERGED_ERROR,
    OPT_NOT_CONVERGED_ERROR,
    SCF_NOT_CONVERGED_ERROR,
)


@pytest.fixture
def calc(tmp_path):
    """Create a calculator object with a water structure and return it."""
    calc = Calculator(basename="job", working_dir=tmp_path)
    calc.structure = Structure.from_smiles("O")
    return calc


@pytest.mark.orca
def test_scf_conv_fail(calc):
    """Test error_message for SCF not converging"""
    calc.input.add_blocks(BlockScf(maxiter=1))
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == SCF_NOT_CONVERGED_ERROR.message


@pytest.mark.orca
def test_cc_conv_fail(calc):
    """Test error_message for CC not converging"""
    calc.input.add_blocks(BlockMdci(maxiter=1))
    calc.input.add_simple_keywords(Wft.CCSD_T)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == CC_NOT_CONVERGED_ERROR.message


@pytest.mark.orca
def test_dlpno_cc_conv_fail(calc):
    """Test error_message for DLPNO-CC not converging"""
    calc.input.add_blocks(BlockMdci(maxiter=1))
    calc.input.add_simple_keywords(Wft.DLPNO_CCSD_T, AuxBasisSet.AUTOAUX)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == CC_NOT_CONVERGED_ERROR.message


@pytest.mark.orca
def test_opt_conv_fail(calc):
    """Test error_message for geometry optimization not converging"""
    calc.input.add_blocks(BlockGeom(maxiter=1))
    calc.input.add_simple_keywords(Task.OPT)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    # > Note that ORCA still terminates normally
    assert output.terminated_normally()
    assert output.error_message() == OPT_NOT_CONVERGED_ERROR.message


@pytest.mark.orca
def test_cpscf_conv_fail(calc):
    """Test error_message for CP-SCF not converging"""
    calc.input.add_blocks(BlockMethod(z_maxiter=1))
    calc.input.add_simple_keywords(Task.FREQ)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == CPSCF_NOT_CONVERGED_ERROR.message
