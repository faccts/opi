import pytest

from opi.output.models.json.property.properties.chem_shift import ChemicalShift
from opi.output.models.json.property.properties.spin_coupling import SpinSpinCoupling

"""
Unit tests for the Output getters of NMR properties

This module contains tests for the getters of:
- Chemical shielding tensors
- Spin-spin coupling constants
"""


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["nmr"])
def test_get_chemical_shift_returns_shieldings(output_object_factory, task: str):
    """Test if `Output.get_chemical_shift()` returns the `ChemicalShift` of every method."""
    output_object = output_object_factory(task)
    shieldings = output_object.get_chemical_shift()

    # > An MP2 calculation reports the SCF shieldings alongside the MP2 ones
    assert [(shift.method, shift.level) for shift in shieldings] == [
        ("SCF", "Relaxed density"),
        ("MP2", "Unrelaxed density"),
        ("MP2", "Relaxed density"),
    ]
    for shift in shieldings:
        assert isinstance(shift, ChemicalShift)
        assert len(shift.siso) == shift.numofnucs
        assert len(shift.saniso) == shift.numofnucs


@pytest.mark.unit
@pytest.mark.output
def test_get_chemical_shift_returns_none(empty_output_object):
    """Test if `Output.get_chemical_shift()` returns None when expected."""
    assert not empty_output_object.get_chemical_shift()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["nmr"])
def test_get_spin_spin_coupling_returns_couplings(output_object_factory, task: str):
    """Test if `Output.get_spin_spin_coupling()` returns the `SpinSpinCoupling`."""
    output_object = output_object_factory(task)
    couplings = output_object.get_spin_spin_coupling()

    for coupling in couplings:
        assert isinstance(coupling, SpinSpinCoupling)
        assert len(coupling.pairsinfo) == coupling.numofnucpairs
        assert len(coupling.pairstotalssciso) == coupling.numofnucpairs


@pytest.mark.unit
@pytest.mark.output
def test_get_spin_spin_coupling_returns_none(empty_output_object):
    """Test if `Output.get_spin_spin_coupling()` returns None when expected."""
    assert not empty_output_object.get_spin_spin_coupling()
