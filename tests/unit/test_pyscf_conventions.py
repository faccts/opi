import numpy as np
import pytest

from opi.output.models.json.gbw._pyscf_converter import ORCA_TO_PYSCF_SHELLS, AOMap
from opi.output.models.json.gbw.properties.base import SHELL_LETTERS

"""
Consistency checks of the table that relates ORCA's and PySCF's basis functions.

The table itself is checked against ORCA's overlap matrix by the tests in `tests/pyscf_conversion`;
these tests only guard against typos when editing it. They do not require PySCF.
"""


@pytest.mark.unit
def test_shell_conventions_cover_all_shell_letters() -> None:
    """The table must have one entry for each angular momentum supported by ORCA."""
    assert sorted(ORCA_TO_PYSCF_SHELLS) == list(range(len(SHELL_LETTERS)))


@pytest.mark.unit
@pytest.mark.parametrize("ang", range(len(SHELL_LETTERS)))
def test_shell_convention_is_signed_permutation(ang: int) -> None:
    """Each entry must relate the 2l + 1 functions of a shell one to one, up to a sign."""
    convention = ORCA_TO_PYSCF_SHELLS[ang]

    assert sorted(convention.orca_index) == list(range(2 * ang + 1))
    assert len(convention.sign) == 2 * ang + 1
    assert set(convention.sign) <= {"+", "-"}


@pytest.mark.unit
def test_ao_map_round_trip() -> None:
    """Transforming coefficients from ORCA to PySCF and back must reproduce them."""
    # > Shells of all angular momenta, placed in reverse order in PySCF's basis
    angs = list(range(len(SHELL_LETTERS)))
    sizes = [2 * ang + 1 for ang in angs]
    orca_starts = np.cumsum([0, *sizes])[:-1]
    pyscf_starts = np.cumsum([0, *sizes[::-1]])[:-1][::-1]
    ao_map = AOMap.from_shells(
        (ang, int(orca_start), int(pyscf_start))
        for ang, orca_start, pyscf_start in zip(angs, orca_starts, pyscf_starts, strict=True)
    )
    coeff = np.random.default_rng(0).standard_normal((ao_map.n_ao, 5))

    np.testing.assert_array_equal(ao_map.pyscf_to_orca(ao_map.orca_to_pyscf(coeff)), coeff)
    assert not np.array_equal(ao_map.orca_to_pyscf(coeff), coeff)
