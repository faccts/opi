"""Parse a potential FCIDUMP file"""

import re
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Self

import numpy as np


@dataclass
class Fcidump:
    """
    Reads and stores data from a FCIDUMP file. One and two-electrons integrals are stored as dicts and can be
    accessed as numpy arrays via `hcore_matrix` and `eri_tensor`.

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
        Dictionary that contains the one-electron integrals.
    two_electron: dict[tuple[int, int, int, int], float]
        Dictionary that contains the two-electron integrals.
    orbital_energies: dict[int, float]
        Dictionary that contains the orbital energies, if present in the FCIDUMP file.
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

    @cached_property
    def hcore_matrix(self) -> np.ndarray[tuple[int, int], np.dtype[np.float64]]:
        """Return the one-electron integrals as a symmetric (norb, norb) numpy array."""
        mat = np.zeros((self.norb, self.norb))
        for (i, j), val in self.one_electron.items():
            mat[i - 1, j - 1] = val
            mat[j - 1, i - 1] = val
        return mat

    @cached_property
    def eri_tensor(self) -> np.ndarray[tuple[int, int, int, int], np.dtype[np.float64]]:
        """Return the two-electron integrals as a (norb, norb, norb, norb) numpy array.

        Uses chemist's notation (ij|kl) with 8-fold permutation symmetry applied.
        """
        tensor = np.zeros((self.norb,) * 4)
        if not self.two_electron:
            return tensor

        # > Pull all stored indices/values into arrays once
        idx = np.array(list(self.two_electron.keys()), dtype=np.int64) - 1  # (n_integrals, 4)
        vals = np.array(list(self.two_electron.values()), dtype=np.float64)  # (n_integrals,)
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
    def from_file(cls, path: Path | str) -> Self:
        """
        Parse a FCIDUMP file and return the populated `Fcidump` object.
        The FCIDUMP file is documented in the paper:
        Knowles, P. J.; Handy, N. C. A Determinant Based Full Configuration Interaction Program.
        Computer Physics Communications 1989, 54, 75–83. https://doi.org/10.1016/0010-4655(89)90033-7

        Raises
        -------
        ValueError
            If the FCIDUMP file cannot be parsed.
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
