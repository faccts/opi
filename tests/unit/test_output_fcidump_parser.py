from pathlib import Path

import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from opi.output.fcidump import Fcidump


@pytest.mark.unit
@pytest.mark.output
def test_parse_fcidump_header(tmp_path: Path) -> None:
    fcidump_text = """
         &FCI
          NORB= 2, NELEC= 2, MS2= 0,
          ORBSYM=1,1,
          ISYM=0,
         /
          0.5000000000  1  1  1  1
          0.1000000000  2  1  1  1
          0.2000000000  2  2  1  1
          0.3000000000  2  2  2  2
         -0.1234567890  1  1  0  0
          0.0987654321  2  1  0  0
          0.0500000000  2  2  0  0
         -1.2345678901  0  0  0  0
    """
    fci_file = tmp_path / "test.fcidump"
    fci_file.write_text(fcidump_text)

    dump = Fcidump.from_file(fci_file)

    assert dump.norb == 2
    assert dump.nelec == 2
    assert dump.ms2 == 0
    assert dump.orbsym == [1, 1]
    assert dump.isym == 0
    assert pytest.approx(dump.e_nuc) == -1.2345678901


@pytest.mark.unit
@pytest.mark.output
def test_get_int() -> None:
    """`_get_int()` extracts integer header values, tolerating whitespace and mixed-case keys."""
    header = "&FCI\n NORB= 12, NELEC=8,\n ms2 = 0,\n/"

    assert Fcidump._get_int("NORB", header) == 12
    assert Fcidump._get_int("NELEC", header) == 8
    # key matching is case-insensitive
    assert Fcidump._get_int("MS2", header) == 0


@pytest.mark.unit
@pytest.mark.output
def test_get_int_missing_key_raises() -> None:
    """`_get_int()` raises a ValueError naming the key when it is absent from the header."""
    with pytest.raises(ValueError, match="ISYM"):
        Fcidump._get_int("ISYM", "&FCI\n NORB= 2,\n/")


@pytest.mark.unit
@pytest.mark.output
def test_get_int_negative_value_raises() -> None:
    """`_get_int()` only accepts non-negative integers, so a negative value raises a ValueError."""
    with pytest.raises(ValueError, match="MS2"):
        Fcidump._get_int("MS2", "&FCI\n MS2= -2,\n/")


@pytest.mark.unit
@pytest.mark.output
def test_get_int_list() -> None:
    """`_get_int_list()` parses comma-separated integers, tolerating whitespace and mixed case."""
    assert Fcidump._get_int_list("ORBSYM", "ORBSYM=1,1,2,1,") == [1, 1, 2, 1]
    # tolerates whitespace around the separators and is case-insensitive
    assert Fcidump._get_int_list("ORBSYM", "orbsym = 1 , 2 , 3,") == [1, 2, 3]
    # a single-entry list (norb=1) must parse as well
    assert Fcidump._get_int_list("ORBSYM", "ORBSYM=1,") == [1]


@pytest.mark.unit
@pytest.mark.output
def test_get_int_list_missing_key_raises() -> None:
    """`_get_int_list()` raises a ValueError naming the key when it is absent from the header."""
    with pytest.raises(ValueError, match="ORBSYM"):
        Fcidump._get_int_list("ORBSYM", "&FCI\n NORB= 2,\n/")


@pytest.mark.unit
@pytest.mark.output
def test_get_int_list_negative_value_raises() -> None:
    """`_get_int_list()` only accepts non-negative integers, so a negative entry raises a ValueError."""
    with pytest.raises(ValueError, match="ORBSYM"):
        Fcidump._get_int_list("ORBSYM", "ORBSYM=-1,1,")


@pytest.mark.unit
@pytest.mark.output
def test_hcore_matrix_shape_and_symmetry() -> None:
    dump = Fcidump(
        norb=2,
        nelec=2,
        ms2=0,
        orbsym=[1, 1],
        isym=0,
        one_electron={(1, 1): -0.5, (2, 1): 0.1, (2, 2): -0.3},
    )
    mat = dump.hcore_matrix

    assert mat.shape == (2, 2)
    assert pytest.approx(mat[0, 0]) == -0.5
    assert pytest.approx(mat[1, 1]) == -0.3
    # off-diagonal must be symmetric
    assert pytest.approx(mat[1, 0]) == 0.1
    assert pytest.approx(mat[0, 1]) == 0.1


@pytest.mark.unit
@pytest.mark.output
def test_eri_tensor_empty_two_electron() -> None:
    """Without two-electron integrals, eri_tensor must be all-zero instead of raising."""
    dump = Fcidump(norb=2, nelec=2, ms2=0, orbsym=[1, 1], isym=0)

    assert dump.eri_tensor.shape == (2, 2, 2, 2)
    assert not dump.eri_tensor.any()


@pytest.mark.unit
@pytest.mark.output
def test_eri_tensor_shape_and_symmetry() -> None:
    dump = Fcidump(
        norb=2,
        nelec=2,
        ms2=0,
        orbsym=[1, 1],
        isym=0,
        two_electron={(1, 1, 1, 1): 0.5, (2, 1, 1, 1): 0.1, (2, 2, 1, 1): 0.2, (2, 2, 2, 2): 0.3},
    )
    tensor = dump.eri_tensor

    assert tensor.shape == (2, 2, 2, 2)
    assert pytest.approx(tensor[0, 0, 0, 0]) == 0.5
    assert pytest.approx(tensor[1, 1, 1, 1]) == 0.3
    # check 8-fold symmetry for (2,1,1,1) -> index (1,0,0,0)
    val = 0.1
    assert pytest.approx(tensor[1, 0, 0, 0]) == val  # (ij|kl)
    assert pytest.approx(tensor[0, 1, 0, 0]) == val  # (ji|kl)
    assert pytest.approx(tensor[0, 0, 1, 0]) == val  # (kl|ij)
    assert pytest.approx(tensor[0, 0, 0, 1]) == val  # (lk|ij)


@pytest.mark.unit
@pytest.mark.output
def test_from_arrays_roundtrip() -> None:
    """`from_arrays()` stores only canonical elements and reproduces the input arrays."""
    hcore = np.array([[-0.5, 0.1], [0.1, -0.3]])
    eri = np.zeros((2, 2, 2, 2))
    for idx, val in (((0, 0, 0, 0), 0.5), ((1, 0, 0, 0), 0.1), ((1, 1, 1, 1), 0.3)):
        i, j, k, ll = idx
        for p, q, r, s in (
            (i, j, k, ll),
            (j, i, k, ll),
            (i, j, ll, k),
            (j, i, ll, k),
            (k, ll, i, j),
            (ll, k, i, j),
            (k, ll, j, i),
            (ll, k, j, i),
        ):
            eri[p, q, r, s] = val

    dump = Fcidump.from_arrays(hcore, eri, nelec=2, e_nuc=-1.5)

    assert dump.norb == 2
    assert dump.orbsym == [1, 1]
    # all canonical representatives are stored, including zeros
    assert dump.one_electron == {(1, 1): -0.5, (2, 1): 0.1, (2, 2): -0.3}
    assert dump.two_electron == {
        (1, 1, 1, 1): 0.5,
        (2, 1, 1, 1): 0.1,
        (2, 1, 2, 1): 0.0,
        (2, 2, 1, 1): 0.0,
        (2, 2, 2, 1): 0.0,
        (2, 2, 2, 2): 0.3,
    }
    # reconstruction from the dicts must give back the input arrays
    assert np.allclose(dump.hcore_matrix, hcore)
    assert np.allclose(dump.eri_tensor, eri)


@pytest.mark.unit
@pytest.mark.output
def test_from_arrays_asymmetric_raises() -> None:
    """`from_arrays()` rejects a non-symmetric hcore matrix."""
    hcore = np.array([[-0.5, 0.1], [0.2, -0.3]])
    eri = np.zeros((2, 2, 2, 2))

    with pytest.raises(ValueError, match="symmetric"):
        Fcidump.from_arrays(hcore, eri, nelec=2)


@pytest.mark.unit
@pytest.mark.output
@given(
    norb=st.integers(min_value=2, max_value=8),
    data=st.data(),
)
def test_hcore_matrix_transposed_keys(norb: int, data: st.DataObject) -> None:
    """Initializing hcore with symmetry equivalent keys, (i,j) and (j,i), should raise a ValueError."""
    # > Pick a subset of upper-triangle index pairs (1-based, i <= j) to populate.
    pairs = [(i, j) for i in range(1, norb + 1) for j in range(i, norb + 1)]
    one_electron: dict[tuple[int, int], float] = {}
    finite = st.floats(min_value=-10, max_value=10, allow_nan=False, allow_infinity=False)
    for i, j in pairs:
        one_electron[(i, j)] = data.draw(finite)
        if i != j:
            # > Store a transposed key too - Could be any value
            one_electron[(j, i)] = data.draw(finite)

    # > Raise a value error due to symmetry-equivalent keys
    with pytest.raises(ValueError, match="symmetry-equivalent keys"):
        Fcidump(
            norb=norb,
            nelec=2,
            ms2=0,
            orbsym=[1] * norb,
            isym=0,
            one_electron=one_electron,
        )


@pytest.mark.unit
@pytest.mark.output
# > The seven non-identity elements of the 8-fold permutation group of (12|34)
@pytest.mark.parametrize(
    "equivalent",
    [
        (2, 1, 3, 4),
        (1, 2, 4, 3),
        (2, 1, 4, 3),
        (3, 4, 1, 2),
        (4, 3, 1, 2),
        (3, 4, 2, 1),
        (4, 3, 2, 1),
    ],
)
def test_eri_symmetry_equivalent_keys_raise(equivalent: tuple[int, int, int, int]) -> None:
    """Any two keys related by the 8-fold permutation symmetry must raise a ValueError."""
    two_electron = {(1, 2, 3, 4): 0.1, equivalent: 0.2}

    with pytest.raises(ValueError, match="two_electron: symmetry-equivalent keys"):
        Fcidump(norb=4, nelec=2, ms2=0, orbsym=[1] * 4, isym=0, two_electron=two_electron)


@pytest.mark.unit
@pytest.mark.output
def test_from_file_symmetry_equivalent_keys_raise(tmp_path: Path) -> None:
    """Duplicates are also rejected when parsed from a file, where the dicts are filled in after construction."""
    fci_file = tmp_path / "duplicates.fcidump"
    fci_file.write_text(
        "&FCI NORB= 2,NELEC= 2,MS2= 0,\n"
        " ORBSYM=1,1,\n"
        " ISYM= 1,\n"
        "&END\n"
        "  0.500000000000000   1 1 1 1\n"
        "  1.000000000000000   1 2 0 0\n"
        "  2.000000000000000   2 1 0 0\n"
        "  0.000000000000000   0 0 0 0\n"
    )

    with pytest.raises(ValueError, match="one_electron: symmetry-equivalent keys"):
        Fcidump.from_file(fci_file)


@pytest.mark.unit
@pytest.mark.output
def test_hcore_matrix_zero_index_raises() -> None:
    """An orbital index of 0 (1-based convention) must raise a ValueError instead of wrapping around."""
    dump = Fcidump(norb=2, nelec=2, ms2=0, orbsym=[1, 1], isym=0, one_electron={(0, 1): 0.5})

    with pytest.raises(ValueError, match="one_electron"):
        dump.hcore_matrix


@pytest.mark.unit
@pytest.mark.output
def test_hcore_matrix_negative_index_raises() -> None:
    """An orbital index that is negative must raise a ValueError instead of wrapping around."""
    dump = Fcidump(norb=2, nelec=2, ms2=0, orbsym=[1, 1], isym=0, one_electron={(-1, 1): 0.5})

    with pytest.raises(ValueError, match="one_electron"):
        dump.hcore_matrix


@pytest.mark.unit
@pytest.mark.output
def test_to_file_roundtrip(tmp_path: Path) -> None:
    """A written FCIDUMP file must parse back into an equivalent object."""
    dump = Fcidump(
        norb=2,
        nelec=2,
        ms2=0,
        orbsym=[1, 1],
        isym=1,
        one_electron={(1, 1): -1.259550439370290, (2, 1): 0.000063953470416},
        two_electron={(1, 1, 1, 1): 0.764178936345604, (2, 1, 1, 1): -0.000062078881437},
        e_nuc=-74.204378402010107,
    )
    fci_file = tmp_path / "written.fcidump"
    dump.to_file(fci_file)

    assert dump.path == fci_file

    # negative header values would be unreadable by from_file and must be rejected
    dump.ms2 = -2
    with pytest.raises(ValueError, match="ms2"):
        dump.to_file(tmp_path / "invalid.fcidump")
    dump.ms2 = 0

    reread = Fcidump.from_file(fci_file)
    assert reread.norb == dump.norb
    assert reread.nelec == dump.nelec
    assert reread.ms2 == dump.ms2
    assert reread.orbsym == dump.orbsym
    assert reread.isym == dump.isym
    assert reread.one_electron == pytest.approx(dump.one_electron)
    assert reread.two_electron == pytest.approx(dump.two_electron)
    assert reread.e_nuc == pytest.approx(dump.e_nuc)
