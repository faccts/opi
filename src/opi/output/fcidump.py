"""Read, create, and write FCIDUMP files"""

import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Self, TypeVar

import numpy as np
from numpy.typing import ArrayLike

K = TypeVar("K")


@dataclass
class Fcidump:
    """
    Reads and stores data from a FCIDUMP file. One and two-electrons integrals are stored as dicts and
    can be accessed as numpy arrays via `hcore_matrix` and `eri_tensor`. Integrals must contain only symmetry-unique
    elements.

    Besides parsing a file with `from_file()`, objects can be created directly from the integral
    dicts (default constructor) or from numpy arrays via `from_arrays()`, and written to a
    FCIDUMP file with `to_file()`.

    Attributes
    --------
    norb: int
        Number of active orbitals.
    nelec: int
        Number of active electrons.
    ms2: int
        Twice the total spin projection, i.e. the difference of alpha and beta electrons.
    orbsym: list[int]
        Symmetry labels of the orbitals.
    isym: int
        Overall symmetry of the electronic structure.
    one_electron: dict[tuple[int, int], float]
        Dictionary that contains the one-electron integrals. Must only contain symmetry-unique elements.
    two_electron: dict[tuple[int, int, int, int], float]
        Dictionary that contains the two-electron integrals. Must only contain symmetry-unique elements.
    orbital_energies: dict[int, float]
        Dictionary that contains the orbital energies, if present in the FCIDUMP file (not in ORCA FCIDUMP).
    e_nuc: float
        Core energy contribution. Contains the contracted energy of the inactive space.
    path: Path
        Path to the FCIDUMP file.
    """

    norb: int
    nelec: int
    ms2: int
    orbsym: list[int]
    isym: int
    one_electron: dict[tuple[int, int], float] = field(default_factory=dict)
    two_electron: dict[tuple[int, int, int, int], float] = field(default_factory=dict)
    orbital_energies: dict[int, float] = field(default_factory=dict)
    e_nuc: float = 0.0
    path: Path = field(default_factory=Path)

    def __post_init__(self) -> None:
        """
        Check that the one- and two-electron integrals contain no symmetry-equivalent keys.

        Raises
        -------
        ValueError
            If symmetry-equivalent keys are present, e.g. (i,j) and (j,i) for one-electron integrals.
        """
        self._validate_integrals()

    def _validate_integrals(self) -> None:
        """
        Check that the one- and two-electron integral dicts hold only symmetry-unique keys.

        Raises
        -------
        ValueError
            If symmetry-equivalent keys are present, e.g. (i,j) and (j,i) for one-electron integrals.
        """
        self._check_no_symmetry_duplicates(self.one_electron, self._canon_1e, "one_electron")
        self._check_no_symmetry_duplicates(self.two_electron, self._canon_2e, "two_electron")

    @cached_property
    def hcore_matrix(self) -> np.ndarray[tuple[int, int], np.dtype[np.float64]]:
        """Return the one-electron integrals as a symmetric (norb, norb) numpy array.

        Raises
        -------
        ValueError
            If a stored key contains an orbital index smaller than 1.
        """
        mat = np.zeros((self.norb, self.norb))
        if not self.one_electron:
            return mat

        # > Pull all stored indices/values into arrays once
        idx = np.array(list(self.one_electron.keys()), dtype=np.int64) - 1  # (n_integrals, 2)
        vals = np.array(list(self.one_electron.values()), dtype=np.float64)  # (n_integrals,)
        if idx.min() < 0:
            raise ValueError(f"{type(self).__name__}: orbital indices in one_electron must be >= 1")

        # > Keys may be stored in either triangle, so sort them into the lower one and
        # > mirror the values to keep the matrix symmetric
        row = np.maximum(idx[:, 0], idx[:, 1])
        col = np.minimum(idx[:, 0], idx[:, 1])
        mat[row, col] = vals
        mat[col, row] = mat[row, col]
        return mat

    @cached_property
    def eri_tensor(self) -> np.ndarray[tuple[int, int, int, int], np.dtype[np.float64]]:
        """Return the two-electron integrals as a (norb, norb, norb, norb) numpy array.

        Uses chemist's notation (ij|kl) with 8-fold permutation symmetry applied.

        Raises
        -------
        ValueError
            If a stored key contains an orbital index smaller than 1.
        """
        tensor = np.zeros((self.norb,) * 4)
        if not self.two_electron:
            return tensor

        # > Pull all stored indices/values into arrays once
        idx = np.array(list(self.two_electron.keys()), dtype=np.int64) - 1  # (n_integrals, 4)
        vals = np.array(list(self.two_electron.values()), dtype=np.float64)  # (n_integrals,)
        if idx.min() < 0:
            raise ValueError(f"{type(self).__name__}: orbital indices in two_electron must be >= 1")
        a, b, c, d = idx[:, 0], idx[:, 1], idx[:, 2], idx[:, 3]

        # > Vectorized assignment for each of the 8 symmetry-equivalent index permutations
        for p, q, r, s in (
            (a, b, c, d),
            (b, a, c, d),
            (a, b, d, c),
            (b, a, d, c),
            (c, d, a, b),
            (d, c, a, b),
            (c, d, b, a),
            (d, c, b, a),
        ):
            tensor[p, q, r, s] = vals
        return tensor

    @classmethod
    def from_arrays(
        cls,
        hcore: ArrayLike,
        eri: ArrayLike,
        nelec: int,
        ms2: int = 0,
        *,
        e_nuc: float = 0.0,
        orbsym: Sequence[int] = (),
        isym: int = 1,
        orbital_energies: Sequence[float] | None = None,
    ) -> Self:
        """
        Create a `Fcidump` object from raw numpy arrays.

        Only the symmetry-unique elements (i >= j for `hcore`, canonical 8-fold permutations for
        `eri`) are stored in the integral dicts.

        Parameters
        ----------
        hcore: ArrayLike
            One-electron integrals as a symmetric (norb, norb) array.
        eri: ArrayLike
            Two-electron integrals as a (norb, norb, norb, norb) array in chemist's notation
            (ij|kl) with 8-fold permutation symmetry.
        nelec: int
            Number of active electrons.
        ms2: int, default: 0
            Twice the total spin projection, i.e. the difference of alpha and beta electrons.
        e_nuc: float, default: 0.0
            Core energy contribution.
        orbsym: Sequence[int], default: ()
            Symmetry labels of the orbitals. Defaults to all orbitals in irrep 1.
        isym: int, default: 1
            Overall symmetry of the electronic structure.
        orbital_energies: Sequence[float] | None, default: None
            Orbital energies. Not part of ORCA-generated FCIDUMP files but supported.

        Raises
        -------
        ValueError
            If the array shapes are inconsistent or the required symmetries are violated.
        """
        hcore = np.asarray(hcore, dtype=np.float64)
        eri = np.asarray(eri, dtype=np.float64)

        if hcore.ndim != 2 or hcore.shape[0] != hcore.shape[1]:
            raise ValueError(f"{cls.__name__}: hcore must be a square matrix, got {hcore.shape}")
        norb = hcore.shape[0]
        if eri.shape != (norb,) * 4:
            raise ValueError(
                f"{cls.__name__}: eri must have shape {(norb,) * 4} to match hcore, got {eri.shape}"
            )
        if not np.allclose(hcore, hcore.T):
            raise ValueError(f"{cls.__name__}: hcore must be symmetric")
        # > These three transpositions generate the full 8-fold permutation group
        for axes in ((1, 0, 2, 3), (0, 1, 3, 2), (2, 3, 0, 1)):
            if not np.allclose(eri, eri.transpose(axes)):
                raise ValueError(f"{cls.__name__}: eri must have 8-fold permutation symmetry")
        if orbsym and len(orbsym) != norb:
            raise ValueError(f"{cls.__name__}: orbsym must contain exactly {norb} entries")

        # > Unique one-electron elements: lower triangle (i >= j)
        i1, j1 = np.tril_indices(norb)
        vals1 = hcore[i1, j1]
        one_electron = {
            (int(i) + 1, int(j) + 1): float(v) for i, j, v in zip(i1, j1, vals1, strict=True)
        }

        # > Unique two-electron elements: i >= j, k >= l and pair index (ij) >= (kl)
        pq, rs = np.tril_indices(i1.size)
        i2, j2, k2, l2 = i1[pq], j1[pq], i1[rs], j1[rs]
        vals2 = eri[i2, j2, k2, l2]
        two_electron = {
            (int(i) + 1, int(j) + 1, int(k) + 1, int(ll) + 1): float(v)
            for i, j, k, ll, v in zip(i2, j2, k2, l2, vals2, strict=True)
        }

        return cls(
            norb=norb,
            nelec=nelec,
            ms2=ms2,
            # > If no orbsym is available we use the total symmetric representation (array of 1)
            orbsym=list(orbsym) if orbsym else [1] * norb,
            isym=isym,
            one_electron=one_electron,
            two_electron=two_electron,
            # > Check against None explicitly: `or` would crash on a multi-element numpy array
            orbital_energies=(
                {i + 1: float(v) for i, v in enumerate(orbital_energies)}
                if orbital_energies is not None
                else {}
            ),
            e_nuc=e_nuc,
        )

    def to_file(self, path: Path | str) -> None:
        """
        Write the stored data to a FCIDUMP file, using the same formatting as ORCA.

        The integrals are written as stored in the dicts, i.e. only the symmetry-unique elements
        provided there end up in the file. `path` is stored in the `path` attribute afterwards.
        Values are written with 15 decimal places (ORCA's format), so magnitudes below ~1e-15
        end up as zero in the file.

        Parameters
        ----------
        path: Path | str
            Path of the FCIDUMP file to write.

        Raises
        -------
        ValueError
            If the object contains no orbitals (`norb` < 1) or a negative header value
            (`nelec`, `ms2`, `isym`), neither of which can be represented in the FCIDUMP format.
        """
        if self.norb < 1:
            raise ValueError(
                f"{type(self).__name__}: cannot write a FCIDUMP file without orbitals "
                f"(norb = {self.norb})"
            )
        if self.nelec < 0 or self.ms2 < 0 or self.isym < 0:
            raise ValueError(
                f"{type(self).__name__}: nelec, ms2, and isym must be non-negative to be "
                f"written to a FCIDUMP file (got nelec = {self.nelec}, ms2 = {self.ms2}, "
                f"isym = {self.isym})"
            )
        path = Path(path)

        lines = [
            f"&FCI NORB={self.norb:>2},NELEC={self.nelec:>2},MS2={self.ms2:>2},",
            " ORBSYM=" + ",".join(str(sym) for sym in self.orbsym) + ",",
            f" ISYM={self.isym:>2},",
            "&END",
        ]
        for (i, j, k, ll), val in sorted(self.two_electron.items()):
            lines.append(f"{val:21.15f}   {i} {j} {k} {ll}")
        for (i, j), val in sorted(self.one_electron.items()):
            lines.append(f"{val:21.15f}   {i} {j} 0 0")
        for i, val in sorted(self.orbital_energies.items()):
            lines.append(f"{val:21.15f}   {i} 0 0 0")
        lines.append(f"{self.e_nuc:21.15f}   0 0 0 0")

        path.write_text("\n".join(lines) + "\n")
        self.path = path

    @classmethod
    def from_file(cls, path: Path | str) -> Self:
        """
        Parse a FCIDUMP file and return the populated `Fcidump` object.
        The FCIDUMP file is documented in the paper:
        Knowles, P. J.; Handy, N. C. A Determinant Based Full Configuration Interaction Program.
        Computer Physics Communications 1989, 54, 75–83. https://doi.org/10.1016/0010-4655(89)90033-7

        Raises
        -------
        ValueError
            If the FCIDUMP file cannot be parsed or contains symmetry-equivalent integrals,
            e.g. both (i,j) and (j,i) for the one-electron integrals.
        FileNotFoundError
            If the FCIDUMP file cannot be found at the given path.
        """
        path = Path(path)

        if not path.is_file():
            raise FileNotFoundError(f"{cls.__name__}: FCIDUMP file not found at {path}")

        text = path.read_text()

        # > Split header and body
        end_match = re.search(r"&END|/", text, re.IGNORECASE)
        if end_match is None:
            raise ValueError(
                f"{cls.__name__}: Could not find header terminator (&END or /) in {path}"
            )
        header = text[: end_match.end()]
        body = text[end_match.end() :]

        # > Parse the header
        dump = cls(
            norb=cls._get_int("NORB", header),
            nelec=cls._get_int("NELEC", header),
            ms2=cls._get_int("MS2", header),
            orbsym=cls._get_int_list("ORBSYM", header),
            isym=cls._get_int("ISYM", header),
            path=Path(path),
        )

        # > Parse the integrals from the body
        for line in body.splitlines():
            parts = line.split()
            if not parts:
                continue
            if len(parts) != 5:
                raise ValueError(f"{cls.__name__}: Could not parse {line} in {path}")
            try:
                val, i, j, k, ll = (
                    float(parts[0]),
                    int(parts[1]),
                    int(parts[2]),
                    int(parts[3]),
                    int(parts[4]),
                )
            except ValueError:
                raise ValueError(f"{cls.__name__}: Could not parse {line} in {path}")
            # > Inactive contribution
            if i == 0 and j == 0 and k == 0 and ll == 0:
                dump.e_nuc = val
            # > Orbital energies (not written by ORCA, but by some other programs)
            elif j == 0 and k == 0 and ll == 0:
                dump.orbital_energies[i] = val
            # > One-electron matrix
            elif k == 0 and ll == 0:
                dump.one_electron[(i, j)] = val
            # > Two-electron tensor
            else:
                dump.two_electron[(i, j, k, ll)] = val

        # > The integrals are filled in after construction, so `__post_init__` could not check them
        dump._validate_integrals()

        return dump

    @classmethod
    def _get_int(cls, key: str, header: str) -> int:
        """Return the positive integer value of the given key."""
        m = re.search(rf"{key}\s*=\s*(\d+)", header, re.IGNORECASE)
        if m is None:
            raise ValueError(f"{cls.__name__}: Could not parse {key}")
        return int(m.group(1))

    @classmethod
    def _get_int_list(cls, key: str, header: str) -> list[int]:
        """Return a list of non-negative integers corresponding to the given key."""
        m = re.search(rf"{key}\s*=\s*([-\d\s,]+)", header, re.IGNORECASE)
        if m is None:
            raise ValueError(f"{cls.__name__}: Could not parse {key}")
        try:
            values = [int(x) for x in re.split(r"[,\s]+", m.group(1).strip()) if x]
        except ValueError:
            raise ValueError(f"{cls.__name__}: Could not parse {key}")
        if not values or any(v < 0 for v in values):
            raise ValueError(f"{cls.__name__}: Could not parse {key}")
        return values

    @staticmethod
    def _canon_1e(key: tuple[int, int]) -> tuple[int, int]:
        """Canonicalize the key of one-electron integrals."""
        p, q = key
        return (p, q) if p <= q else (q, p)

    @staticmethod
    def _canon_2e(key: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        """Canonicalize the key of two-electron integrals."""
        p, q, r, s = key
        pq = (p, q) if p <= q else (q, p)
        rs = (r, s) if r <= s else (s, r)
        return (*pq, *rs) if pq <= rs else (*rs, *pq)

    @classmethod
    def _check_no_symmetry_duplicates(
        cls, integral_dict: dict[K, float], canon: Callable[[K], K], name: str
    ) -> None:
        """Raise a ValueError if symmetry-equivalent keys are present."""
        seen: dict[K, K] = {}
        for key in integral_dict:
            c: K = canon(key)
            if c in seen:
                raise ValueError(
                    f"{cls.__name__}: {name}: symmetry-equivalent keys {seen[c]} and {key} "
                    "both present"
                )
            seen[c] = key
