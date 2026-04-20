import os
from typing import List, Tuple, Union

import numpy as np


def read_xyz(data: Union[str, Tuple[List[str], np.ndarray]]) -> Tuple[List[str], np.ndarray]:
    """
    Read geometry from:
    - XYZ file path
    - XYZ block string

    Returns
    -------
    symbols : list[str]
    coords : (N, 3) ndarray
    """

    if isinstance(data, str):
        # Case 1a: a file path
        if os.path.isfile(data):
            with open(data, "r") as f:
                lines = f.readlines()

        # Case 1b: an XYZ block string
        else:
            lines = data.strip().splitlines()

        n_atoms = int(lines[0].strip())
        symbols = []
        coords = []

        for line in lines[2 : 2 + n_atoms]:
            parts = line.split()
            sym = parts[0]
            xyz = [float(x) for x in parts[1:4]]

            symbols.append(sym)
            coords.append(xyz)

        return symbols, np.array(coords, dtype=np.float64)

    else:
        raise TypeError("Input must be: file path or XYZ string")


def _validate_geometries(symA: List[str], symB: List[str]) -> None:
    if len(symA) != len(symB):
        raise ValueError("Geometries have different number of atoms")

    for i, (a, b) in enumerate(zip(symA, symB)):
        if a != b:
            raise ValueError(f"Atom mismatch at index {i}: {a} != {b}")


def kabsch_rmsd(
    ref_xyz: str,
    target_xyz: str,
    *,
    align: bool = True,
) -> float:
    """Compute RMSD between two XYZ geometries.

    Parameters
    ----------
    ref_xyz : str
        Reference geometry.
    target_xyz : str
        Target geometry.
    align : bool, default True
        Whether to perform optimal alignment (Kabsch).

    Returns
    -------
    float
        RMSD (Å)
    """

    symA, A = read_xyz(ref_xyz)
    symB, B = read_xyz(target_xyz)

    _validate_geometries(symA, symB)

    # Center using centroid (simple average)
    A_cent = A - A.mean(axis=0)
    B_cent = B - B.mean(axis=0)

    if not align:
        diff = A_cent - B_cent
        return float(np.sqrt(np.sum(diff**2) / len(A_cent)))

    # Standard Kabsch covariance matrix
    H = B_cent.T @ A_cent

    U, _, Vt = np.linalg.svd(H)

    d = np.linalg.det(Vt.T @ U.T)
    D = np.diag([1.0, 1.0, d])

    R = Vt.T @ D @ U.T

    B_rot = B_cent @ R

    diff = A_cent - B_rot

    rmsd = np.sqrt(np.sum(diff**2) / len(A_cent))

    return float(rmsd)
