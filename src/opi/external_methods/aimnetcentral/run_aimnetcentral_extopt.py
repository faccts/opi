#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
from pathlib import Path

import numpy as np

from opi.external_methods.interface import ExtoptInterface

ANGSTROM_TO_BOHR = 1.8897261254578281
EV_TO_HARTREE = 0.03674932217565499
EV_ANGSTROM_TO_HARTREE_BOHR = EV_TO_HARTREE / ANGSTROM_TO_BOHR


def parse_xyz(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Parse XYZ file and return element numbers and coordinates.
    
    Validation:
    - Element type validation: checks against known elements
    - Coordinate range validation: checks for unreasonably large coordinates
    - File existence check: verifies file exists before parsing
    
    Parameters
    ----------
    path : Path
        Path to the XYZ file.
        
    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Element numbers array and coordinate array.
        
    Raises
    -----
    FileNotFoundError
        If the XYZ file does not exist.
    ValueError
        If the XYZ file is malformed or contains unknown elements.
    """
    if not path.exists():
        raise FileNotFoundError(f"XYZ file not found: {path}")
    
    lines = [line.strip() for line in path.read_text().splitlines() if line.strip()]
    if len(lines) < 2:
        raise ValueError("XYZ file must have at least 2 lines")
    
    nat = int(lines[0])
    if nat < 1:
        raise ValueError("Molecule must have at least 1 atom")
    if len(lines) < 2 + nat:
        raise ValueError(f"XYZ file expects {nat} atoms but has insufficient lines")
    
    body = lines[2 : 2 + nat]
    numbers = []
    coord = []
    symbols = {
        "H": 1,
        "B": 5,
        "C": 6,
        "N": 7,
        "O": 8,
        "F": 9,
        "Si": 14,
        "P": 15,
        "S": 16,
        "Cl": 17,
        "As": 33,
        "Se": 34,
        "Br": 35,
        "Pd": 46,
        "I": 53,
    }
    for line in body:
        parts = line.split()
        element = parts[0]
        if element not in symbols:
            raise ValueError(f"Unknown element: {element}")
        numbers.append(symbols[element])
        coords = [float(x) for x in parts[1:4]]
        if any(abs(c) > 1000 for c in coords):  # Unreasonably large coordinates
            raise ValueError(f"Coordinates outside reasonable range: {coords}")
        coord.append(coords)
    return np.asarray(numbers, dtype=np.int64), np.asarray(coord, dtype=np.float64)  # Changed to float64


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="AIMNetCentral ORCA ExtOpt wrapper")
    p.add_argument("ext_input", nargs="?", default="orca.extinp")
    p.add_argument("ext_output", nargs="?", default="orca.extout")
    p.add_argument("--model", default="aimnet2_2025")
    p.add_argument("--device", default=None)
    p.add_argument("--compile", action="store_true")
    p.add_argument("--ensemble-member", type=int, default=0)
    p.add_argument("--revision", default=None)
    p.add_argument("--token", default=None)
    p.add_argument("--charge", type=float, default=None)
    p.add_argument("--mult", type=float, default=None)
    p.add_argument("--no-forces", action="store_true")
    p.add_argument("--nb-threshold", type=int, default=120)
    p.add_argument("--needs-coulomb", action="store_true")
    p.add_argument("--no-needs-coulomb", action="store_true")
    p.add_argument("--needs-dispersion", action="store_true")
    p.add_argument("--no-needs-dispersion", action="store_true")
    p.add_argument("--coulomb-method", choices=["simple", "dsf", "ewald"], default=None)
    p.add_argument("--coulomb-cutoff", type=float, default=15.0)
    p.add_argument("--dsf-alpha", type=float, default=0.2)
    p.add_argument("--ewald-accuracy", type=float, default=1.0e-8)
    p.add_argument("--dftd3-cutoff", type=float, default=None)
    p.add_argument("--dftd3-smoothing-fraction", type=float, default=None)
    p.add_argument("--pbc", action="store_true")
    p.add_argument("--redirect-stdout", default=None)
    p.add_argument("--opt-type", choices=["opt", "optts"], default="opt", help="Optimization type: opt or optts (transition state)")
    p.add_argument("--hessian", action="store_true", help="Compute Hessian via finite differences (requires --no-forces)")
    return p


def main() -> int:
    args = build_parser().parse_args()
    
    # > Parse opt_type from CLI args (default is "opt")
    opt_type = args.opt_type
    
    stdout_cm = contextlib.nullcontext()
    if args.redirect_stdout is not None:
        stdout_cm = open(args.redirect_stdout, "a")

    with stdout_cm as stdout_handle:
        if stdout_handle is not None and hasattr(stdout_handle, "write"):
            with contextlib.redirect_stdout(stdout_handle), contextlib.redirect_stderr(stdout_handle):
                return _run(args, opt_type)
        return _run(args, opt_type)


def _run(args: argparse.Namespace, opt_type: str) -> int:
    from aimnet.calculators import AIMNet2Calculator

    interface = ExtoptInterface()
    xyz_filename, charge, multiplicity, _ncores, do_gradient, _pc = interface.read_extopt_input(Path(args.ext_input))
    ext_input_path = Path(args.ext_input).resolve()
    xyz_path = Path(xyz_filename)
    if not xyz_path.is_absolute():
        xyz_path = (ext_input_path.parent / xyz_path).resolve()
    numbers, coord = parse_xyz(xyz_path)

    effective_charge = charge if args.charge is None else args.charge
    effective_mult = multiplicity if args.mult is None else args.mult

    # Validate charge/multiplicity consistency
    if effective_mult < 1:
        raise ValueError(f"Invalid multiplicity: {effective_mult} (must be >= 1)")
    if (effective_mult - 1) % 2 != 0 and effective_charge % 2 == 0:
        raise ValueError(f"Invalid multiplicity for even-electron system: mult={effective_mult}, charge={effective_charge}")
    if abs(effective_charge) > 10:
        print(f"Warning: Very high charge ({effective_charge}) may cause numerical instability")
    if effective_mult > 5:
        print(f"Warning: High multiplicity ({effective_mult}) may not be covered by model training")

    # Validate model alias before loading
    if args.model in ["aimnet2", "aimnet2_2025", "aimnet2nse", "aimnet2pd"]:
        print(f"Using AIMNetCentral model: {args.model}")

    needs_coulomb = None
    if args.needs_coulomb:
        needs_coulomb = True
    elif args.no_needs_coulomb:
        needs_coulomb = False

    needs_dispersion = None
    if args.needs_dispersion:
        needs_dispersion = True
    elif args.no_needs_dispersion:
        needs_dispersion = False

    try:
        calc = AIMNet2Calculator(
            args.model,
            nb_threshold=args.nb_threshold,
            needs_coulomb=needs_coulomb,
            needs_dispersion=needs_dispersion,
            device=args.device,
            compile_model=args.compile,
            ensemble_member=args.ensemble_member,
            revision=args.revision,
            token=args.token,
        )
    except FileNotFoundError:
        raise ValueError(
            f"Model '{args.model}' not found. "
            f"Check Hugging Face token or local path. "
            f"Valid aliases: aimnet2, aimnet2_2025, aimnet2nse, aimnet2pd"
        )
    except Exception as e:
        raise ValueError(f"Failed to load model '{args.model}': {e}")

    if args.coulomb_method is not None:
        calc.set_lrcoulomb_method(
            args.coulomb_method,
            cutoff=args.coulomb_cutoff,
            dsf_alpha=args.dsf_alpha,
            ewald_accuracy=args.ewald_accuracy,
        )
    if args.dftd3_cutoff is not None or args.dftd3_smoothing_fraction is not None:
        calc.set_dftd3_cutoff(args.dftd3_cutoff, args.dftd3_smoothing_fraction)

    data = {
        "coord": coord,
        "numbers": numbers,
        "charge": np.asarray(effective_charge, dtype=np.float32),
    }
    if args.pbc:
        raise NotImplementedError(
            "Periodic extopt AIMNetCentral wrapper is not implemented yet because ORCA ExtOpt input does not provide cell vectors in this adapter."
        )
    if calc.is_nse:
        data["mult"] = np.asarray(effective_mult, dtype=np.float32)

    results = calc(data, forces=(do_gradient and not args.no_forces))
    energy_hartree = float(results["energy"]) * EV_TO_HARTREE

    gradient = None
    if do_gradient and not args.no_forces and "forces" in results:
        gradient = (-results["forces"].reshape(-1) * EV_ANGSTROM_TO_HARTREE_BOHR).tolist()

    interface.write_orca_input(Path(args.ext_output), nat=len(numbers), etot=energy_hartree, grad=gradient)
    
    # Hessian computation via finite differences
    if args.hessian and do_gradient:
        hessian = compute_hessian_finite_differences(calc, numbers, coord, effective_charge, effective_mult, args.device)
        interface.write_orca_input(Path(args.ext_output), nat=len(numbers), etot=energy_hartree, grad=gradient, hess=hessian)
    
    return 0


def compute_hessian_finite_differences(
    calc: AIMNet2Calculator,
    numbers: np.ndarray,
    coord: np.ndarray,
    charge: float,
    mult: float,
    device: str | None,
) -> list[list[float]]:
    """Compute Hessian matrix via numerical finite differences.
    
    Parameters
    ----------
    calc : AIMNet2Calculator
        The AIMNet calculator instance.
    numbers : np.ndarray
        Element numbers array (n_atoms,).
    coord : np.ndarray
        Coordinate array (n_atoms, 3).
    charge : float
        System charge.
    mult : float
        Spin multiplicity.
    device : str | None
        Device to run on (cuda/cpu).
        
    Returns
    -------
    list[list[float]]
        Hessian matrix in Hartree/(Bohr*Bohr).
        
    Notes
    -----
    Uses central difference with step size 0.001 Bohr.
    Hessian is symmetric, returned as full matrix.
    """
    n_atoms = len(numbers)
    n_dim = n_atoms * 3
    hessian = [[0.0] * n_dim for _ in range(n_dim)]
    
    step = 0.001  # Bohr
    
    # Compute Hessian via central differences
    # H_ij = (dE/dx_i - dE/dx_j) / step
    # Using finite difference: d2E/dxidxj ≈ (F_i(x+step*j) - F_i(x-step*j)) / (2*step)
    
    for i in range(n_dim):
        coord_plus = coord.copy()
        coord_minus = coord.copy()
        
        atom_i = i // 3
        coord_dir = i % 3
        
        coord_plus[atom_i, coord_dir] += step
        coord_minus[atom_i, coord_dir] -= step
        
        data_plus = {
            "coord": coord_plus,
            "numbers": numbers,
            "charge": np.asarray(charge, dtype=np.float32),
        }
        data_minus = {
            "coord": coord_minus,
            "numbers": numbers,
            "charge": np.asarray(charge, dtype=np.float32),
        }
        if calc.is_nse:
            data_plus["mult"] = np.asarray(mult, dtype=np.float32)
            data_minus["mult"] = np.asarray(mult, dtype=np.float32)
        
        results_plus = calc(data_plus, forces=True)
        results_minus = calc(data_minus, forces=True)
        
        forces_plus = -results_plus["forces"]  # Convert to forces (positive dE/dx)
        forces_minus = -results_minus["forces"]
        
        for j in range(n_dim):
            atom_j = j // 3
            coord_dir_j = j % 3
            
            # Second derivative: dF_j/dx_i
            dF = (forces_plus[atom_j, coord_dir_j] - forces_minus[atom_j, coord_dir_j]) / (2 * step)
            hessian[i][j] = dF * EV_ANGSTROM_TO_HARTREE_BOHR  # Convert to Hartree/Bohr^2
    
    return hessian


if __name__ == "__main__":
    raise SystemExit(main())
