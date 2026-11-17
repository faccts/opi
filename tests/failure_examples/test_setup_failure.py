#!/usr/bin/env python3
"""
Tests for error extraction capabilities from ORCA output files of calculations that fail
during setup. Covers impossible charge/multiplicity combinations, broken input structures,
missing basis sets, coupled-cluster calculations without virtuals or without electron pairs,
orbitals read in for another geometry, and Open MPI failures.
"""

import pytest

from opi.core import Calculator
from opi.input.simple_keywords import BasisSet, Method, Scf, Wft
from opi.input.structures import Structure
from opi.output.grepper.patterns import (
    MOINP_GEOMETRY_ERROR,
    MPI_SLOTS_ERROR,
    NO_VIRTUALS_ERROR,
)

HELIUM_XYZ = """1

He 0.0 0.0 0.0
"""

# > Two atoms on top of each other
OVERLAPPING_XYZ = """2

O 0.0 0.0 0.0
O 0.0 0.0 0.0
"""

# > def2-SVP is not defined for fermium
FERMIUM_XYZ = """1

Fm 0.0 0.0 0.0
"""

HYDROGEN_XYZ = """2

H 0.0 0.0 0.0
H 0.0 0.0 0.74
"""


@pytest.fixture
def calc(tmp_path):
    """Create a calculator object with a water structure and return it."""
    calc = Calculator(basename="job", working_dir=tmp_path)
    calc.structure = Structure.from_smiles("O")
    return calc


@pytest.mark.orca
def test_no_error_on_success(calc):
    """Test that a successful calculation does not report any error message."""
    calc.input.add_simple_keywords(Method.HF, BasisSet.DEF2_SVP)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert output.terminated_normally()
    assert output.error_messages() == []
    assert output.error_message() == ""


@pytest.mark.orca
def test_impossible_multiplicity(calc):
    """Test error_message for a multiplicity that the number of electrons does not allow."""
    calc.structure.multiplicity = 2
    calc.input.add_simple_keywords(Method.HF, BasisSet.DEF2_SVP)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == (
        "Impossible combination of multiplicity (2) and number of electrons (10)"
    )


@pytest.mark.orca
def test_no_virtuals(tmp_path):
    """Test error_message for a coupled-cluster calculation without virtual orbitals."""
    calc = Calculator(basename="job", working_dir=tmp_path)
    calc.structure = Structure.from_xyz_block(HELIUM_XYZ)
    calc.input.add_simple_keywords(Wft.CCSD_T, BasisSet.STO_3G)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == NO_VIRTUALS_ERROR.message


@pytest.mark.orca
def test_no_pairs(tmp_path):
    """Test error_message for a coupled-cluster calculation with a single electron."""
    calc = Calculator(basename="job", working_dir=tmp_path)
    calc.structure = Structure.from_xyz_block(HELIUM_XYZ, charge=1, multiplicity=2)
    calc.input.add_simple_keywords(Wft.CCSD_T, BasisSet.DEF2_SVP)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == (
        "No electron pairs to correlate: the system has too few electrons "
        "for a correlated calculation"
    )


@pytest.mark.orca
def test_more_processes_than_pairs(tmp_path):
    """Test error_message for a parallel MDCI run with fewer pairs than processes."""
    calc = Calculator(basename="job", working_dir=tmp_path)
    calc.structure = Structure.from_xyz_block(HYDROGEN_XYZ)
    calc.input.ncores = 4
    calc.input.add_simple_keywords(Wft.CCSD_T, BasisSet.DEF2_SVP)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == (
        "Number of processes (4) in the parallel calculation exceeds the number of pairs (1)"
    )


@pytest.mark.orca
def test_moinp_geometry_mismatch(tmp_path):
    """Test error_message for orbitals that were obtained for another geometry."""
    # > obtain orbitals for water ...
    reference = Calculator(basename="ref", working_dir=tmp_path)
    reference.structure = Structure.from_smiles("O")
    reference.input.add_simple_keywords(Method.HF, BasisSet.DEF2_SVP)
    reference.write_and_run()
    assert reference.get_output().terminated_normally()

    # > ... and read them into a calculation on methane
    calc = Calculator(basename="job", working_dir=tmp_path)
    calc.structure = Structure.from_smiles("C")
    calc.input.add_simple_keywords(Method.HF, BasisSet.DEF2_SVP, Scf.MOREAD)
    calc.input.moinp = tmp_path / "ref.gbw"
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == MOINP_GEOMETRY_ERROR.message


@pytest.mark.orca
def test_mpi_not_enough_slots(calc):
    """Test error_message for an Open MPI error, which is only written to the ".err" file."""
    calc.input.ncores = 512
    calc.input.add_simple_keywords(Method.HF, BasisSet.DEF2_SVP)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == MPI_SLOTS_ERROR.message


@pytest.mark.orca
def test_zero_distance(tmp_path):
    """Test error_message for an input structure with two atoms on top of each other."""
    calc = Calculator(basename="job", working_dir=tmp_path)
    calc.structure = Structure.from_xyz_block(OVERLAPPING_XYZ)
    calc.input.add_simple_keywords(Method.HF, BasisSet.DEF2_SVP)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == "Zero distance between atoms 2 and 1 of the input structure"


@pytest.mark.orca
def test_missing_basis_set(tmp_path):
    """Test error_message for an element the requested basis set is not defined for."""
    calc = Calculator(basename="job", working_dir=tmp_path)
    calc.structure = Structure.from_xyz_block(FERMIUM_XYZ)
    calc.input.add_simple_keywords(Method.HF, BasisSet.DEF2_SVP)
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == "No main basis functions on atom 0 (Fm)"


@pytest.mark.orca
def test_error_termination_in_module(calc, tmp_path):
    """Test that an otherwise unknown module failure is reported with the failing module."""
    # > A corrupted GBW file makes the GUESS module fail without any more specific message.
    broken_gbw = tmp_path / "broken.gbw"
    broken_gbw.write_bytes(b"not a gbw file")
    calc.input.add_simple_keywords(Method.HF, BasisSet.DEF2_SVP, Scf.MOREAD)
    calc.input.moinp = broken_gbw
    # > write the input and run the calculation
    calc.write_and_run()

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    assert output.error_message() == "Error in GUESS part of the calculation"
