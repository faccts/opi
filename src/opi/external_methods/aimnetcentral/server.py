#!/usr/bin/env python3
"""
Persistent AIMNetCentral calculator server for ORCA ExtOpt interface.

This server loads the AIMNet2Calculator once on startup and handles
multiple single-point energy/gradient requests via a network socket.

Usage
-----
# Start the server:
python -m opi.external_methods.aimnetcentral.server -b 127.0.0.1:8888 --model aimnet2_2025 --device cuda

# ORCA will call this server repeatedly via its ExtOpt mechanism.
# The server stays alive, avoiding the ~1 second Python cold-start overhead.

Units
-----
- Coordinates received from ORCA are in Angstrom
- Energies returned to ORCA must be in Hartree
- Gradients returned to ORCA must be in Hartree/Bohr
"""
from __future__ import annotations

import argparse
import contextlib
import json
import os
import pickle
import signal
import socket
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from opi.external_methods.interface import ExtoptInterface
from opi.external_methods.process import Process, ProcessAlreadyRunningError

ANGSTROM_TO_BOHR = 1.8897261254578281
EV_TO_HARTREE = 0.03674932217565499
EV_ANGSTROM_TO_HARTREE_BOHR = EV_TO_HARTREE / ANGSTROM_TO_BOHR


@dataclass
class Request:
    type: str  # "sp" for single-point, "shutdown" to terminate server
    ext_input: str = ""  # Path to ORCA ExtOpt input file
    ext_output: str = ""  # Path to ORCA ExtOpt output file
    model: str | None = None
    device: str | None = None
    compile_model: bool = False
    ensemble_member: int = 0
    revision: str | None = None
    token: str | None = None
    charge: float | None = None
    mult: float | None = None
    nb_threshold: int = 120
    needs_coulomb: bool | None = None
    needs_dispersion: bool | None = None
    coulomb_method: str | None = None
    coulomb_cutoff: float = 15.0
    dsf_alpha: float = 0.2
    ewald_accuracy: float = 1.0e-8
    dftd3_cutoff: float | None = None
    dftd3_smoothing_fraction: float | None = None


@dataclass
class Response:
    success: bool
    error: str | None = None
    energy_hartree: float | None = None
    gradient: list[float] | None = None


class AIMNetCentralServer:
    """Persistent AIMNetCentral calculator server."""

    def __init__(
        self,
        host_id: str = "127.0.0.1",
        port: int = 8888,
    ):
        self._host_id = host_id
        self._port = port
        self._server_socket: socket.socket | None = None
        self._calculator: Any | None = None
        self._calc_config: dict[str, Any] | None = None
        self._running = False
        self._interface = ExtoptInterface()

    def _init_calculator(self, config: dict[str, Any]) -> None:
        """Initialize or update the AIMNet2Calculator with the given config."""
        from aimnet.calculators import AIMNet2Calculator

        # Only reinitialize if config changed
        if self._calc_config == config:
            return

        calc_kwargs = {
            "model": config.get("model", "aimnet2_2025"),
            "nb_threshold": config.get("nb_threshold", 120),
            "needs_coulomb": config.get("needs_coulomb"),
            "needs_dispersion": config.get("needs_dispersion"),
            "device": config.get("device"),
            "compile_model": config.get("compile_model", False),
            "ensemble_member": config.get("ensemble_member", 0),
            "revision": config.get("revision"),
            "token": config.get("token"),
        }

        self._calculator = AIMNet2Calculator(**calc_kwargs)
        self._calc_config = config.copy()

        # Configure LR modules if specified
        coulomb_method = config.get("coulomb_method")
        if coulomb_method is not None:
            self._calculator.set_lrcoulomb_method(
                coulomb_method,
                cutoff=config.get("coulomb_cutoff", 15.0),
                dsf_alpha=config.get("dsf_alpha", 0.2),
                ewald_accuracy=config.get("ewald_accuracy", 1.0e-8),
            )

        dftd3_cutoff = config.get("dftd3_cutoff")
        dftd3_smoothing = config.get("dftd3_smoothing_fraction")
        if dftd3_cutoff is not None or dftd3_smoothing is not None:
            self._calculator.set_dftd3_cutoff(dftd3_cutoff, dftd3_smoothing)

    def _handle_single_point(self, request: Request) -> Response:
        """Handle a single-point calculation request."""
        if self._calculator is None:
            return Response(success=False, error="Calculator not initialized")

        try:
            # Parse ORCA ExtOpt input
            xyz_filename, charge, multiplicity, _ncores, do_gradient, _pc = (
                self._interface.read_extopt_input(Path(request.ext_input))
            )

            # Parse XYZ file
            xyz_path = Path(xyz_filename)
            if not xyz_path.is_absolute():
                xyz_path = (Path(request.ext_input).parent / xyz_path).resolve()
            lines = [line.strip() for line in xyz_path.read_text().splitlines() if line.strip()]
            nat = int(lines[0])
            body = lines[2 : 2 + nat]

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
            numbers = []
            coord = []
            for line in body:
                parts = line.split()
                numbers.append(symbols[parts[0]])
                coord.append([float(x) for x in parts[1:4]])

            numbers = np.asarray(numbers, dtype=np.int64)
            coord = np.asarray(coord, dtype=np.float32)

            # Determine effective charge and multiplicity
            effective_charge = charge if request.charge is None else request.charge
            effective_mult = multiplicity if request.mult is None else request.mult

            # Prepare input data
            data: dict[str, Any] = {
                "coord": coord,
                "numbers": numbers,
                "charge": np.asarray(effective_charge, dtype=np.float32),
            }
            if self._calculator.is_nse:
                data["mult"] = np.asarray(effective_mult, dtype=np.float32)

            # Run calculation
            results = self._calculator(
                data, forces=(do_gradient and not request.ext_output.endswith("no_forces"))
            )

            energy_hartree = float(results["energy"]) * EV_TO_HARTREE
            gradient = None
            if do_gradient and not request.ext_output.endswith("no_forces"):
                if "forces" in results:
                    gradient = (
                        -results["forces"].reshape(-1) * EV_ANGSTROM_TO_HARTREE_BOHR
                    ).tolist()

            # Write ORCA ExtOpt output
            self._interface.write_orca_input(
                Path(request.ext_output), nat=len(numbers), etot=energy_hartree, grad=gradient
            )

            return Response(
                success=True,
                energy_hartree=energy_hartree,
                gradient=gradient,
            )

        except Exception as e:
            return Response(success=False, error=str(e))

    def _handle_shutdown(self) -> Response:
        """Handle server shutdown request."""
        self._running = False
        return Response(success=True)

    def _handle_request(self, request: Request) -> Response:
        """Route request to appropriate handler."""
        if request.type == "sp":
            return self._handle_single_point(request)
        elif request.type == "shutdown":
            return self._handle_shutdown()
        else:
            return Response(success=False, error=f"Unknown request type: {request.type}")

    def start(self, max_wait: float = 10.0) -> bool:
        """Start the server and accept connections."""
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self._host_id, self._port))
        self._server_socket.listen(1)
        self._server_socket.settimeout(1.0)
        self._running = True

        print(f"AIMNetCentral server listening on {self._host_id}:{self._port}")

        while self._running:
            try:
                client_socket, _addr = self._server_socket.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            try:
                # Receive request
                data = client_socket.recv(65536)
                if not data:
                    continue

                request = pickle.loads(data)
                if isinstance(request, dict):
                    request = Request(**request)

                # Handle request
                response = self._handle_request(request)

                # Send response
                response_data = pickle.dumps(asdict(response) if isinstance(response, Response) else response)
                client_socket.sendall(response_data)

            except Exception as e:
                error_response = Response(success=False, error=str(e))
                client_socket.sendall(pickle.dumps(asdict(error_response)))
            finally:
                client_socket.close()

        if self._server_socket:
            self._server_socket.close()
        return True

    def shutdown(self) -> None:
        """Stop the server."""
        self._running = False
        if self._server_socket:
            self._server_socket.close()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="AIMNetCentral persistent server for ORCA")
    p.add_argument("-b", "--bind", default="127.0.0.1:8888", help="Host:port to bind to")
    p.add_argument("--model", default="aimnet2_2025", help="AIMNetCentral model alias")
    p.add_argument("--device", default=None, help="Device (cuda/cpu)")
    p.add_argument("--compile", action="store_true", help="Enable torch.compile")
    p.add_argument("--ensemble-member", type=int, default=0, help="Ensemble member index (0-3)")
    p.add_argument("--revision", default=None, help="Model revision tag")
    p.add_argument("--token", default=None, help="Hugging Face token for private repos")
    p.add_argument("--nb-threshold", type=int, default=120, help="Neighbor list threshold")
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
    p.add_argument("--log", default=None, help="Log file path")
    return p


def main() -> int:
    args = build_parser().parse_args()

    host_id, port_str = args.bind.split(":")
    port = int(port_str)

    stdout_cm = contextlib.nullcontext()
    if args.log:
        stdout_cm = open(args.log, "a")

    with stdout_cm as stdout_handle:
        if stdout_handle is not None and hasattr(stdout_handle, "write"):
            with contextlib.redirect_stdout(stdout_handle), contextlib.redirect_stderr(stdout_handle):
                return _run_server(args, host_id, port)
        return _run_server(args, host_id, port)


def _run_server(args: argparse.Namespace, host_id: str, port: int) -> int:
    calc_config: dict[str, Any] = {
        "model": args.model,
        "device": args.device,
        "compile_model": args.compile,
        "ensemble_member": args.ensemble_member,
        "revision": args.revision,
        "token": args.token,
        "nb_threshold": args.nb_threshold,
        "needs_coulomb": args.needs_coulomb if args.needs_coulomb else (False if args.no_needs_coulomb else None),
        "needs_dispersion": args.needs_dispersion if args.needs_dispersion else (False if args.no_needs_dispersion else None),
        "coulomb_method": args.coulomb_method,
        "coulomb_cutoff": args.coulomb_cutoff,
        "dsf_alpha": args.dsf_alpha,
        "ewald_accuracy": args.ewald_accuracy,
        "dftd3_cutoff": args.dftd3_cutoff,
        "dftd3_smoothing_fraction": args.dftd3_smoothing_fraction,
    }

    server = AIMNetCentralServer(host_id=host_id, port=port)
    server._calc_config = calc_config

    # Handle SIGTERM for graceful shutdown
    def sigterm_handler(signum: int, frame: Any) -> None:
        print("\nReceived SIGTERM, shutting down...")
        server.shutdown()

    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)

    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        server.shutdown()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
