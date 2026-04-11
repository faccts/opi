#!/usr/bin/env python3
"""
Client wrapper for the AIMNetCentral persistent server.

This module provides functions to start the server and make requests to it.

Usage
-----
# Start server and make a request:
from opi.external_methods.aimnetcentral.client import (
    start_server,
    make_single_point_request,
    shutdown_server,
)

server = start_server(
    model="aimnet2_2025",
    device="cuda",
    host="127.0.0.1",
    port=8888,
)

response = make_single_point_request(
    server,
    ext_input="orca.extinp",
    ext_output="orca.extout",
)

shutdown_server(server)

# Or use the one-shot API:
from opi.external_methods.aimnetcentral.client import run_with_server

run_with_server(
    ext_input="orca.extinp",
    ext_output="orca.extout",
    model="aimnet2_2025",
    device="cuda",
)
"""
from __future__ import annotations

import pickle
import socket
import subprocess
import sys
import time
from typing import Any

from opi.external_methods.process import Process, ProcessAlreadyRunningError


class AIMNetCentralClient:
    """Client for the AIMNetCentral persistent server."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8888):
        self._host = host
        self._port = port
        self._process: Process | None = None

    def start(self, **kwargs: Any) -> bool:
        """Start the server process with the given configuration."""
        cmd = [
            sys.executable,
            "-m",
            "opi.external_methods.aimnetcentral.server",
            f"-b {self._host}:{self._port}",
        ]

        for key, value in kwargs.items():
            if key == "model":
                cmd += ["--model", str(value)]
            elif key == "device":
                cmd += ["--device", str(value)]
            elif key == "compile_model":
                if value:
                    cmd.append("--compile")
            elif key == "ensemble_member":
                cmd += ["--ensemble-member", str(value)]
            elif key == "revision":
                cmd += ["--revision", str(value)]
            elif key == "token":
                cmd += ["--token", str(value)]
            elif key == "nb_threshold":
                cmd += ["--nb-threshold", str(value)]
            elif key == "needs_coulomb":
                if value is True:
                    cmd.append("--needs-coulomb")
                elif value is False:
                    cmd.append("--no-needs-coulomb")
            elif key == "needs_dispersion":
                if value is True:
                    cmd.append("--needs-dispersion")
                elif value is False:
                    cmd.append("--no-needs-dispersion")
            elif key == "coulomb_method":
                cmd += ["--coulomb-method", str(value)]
            elif key == "coulomb_cutoff":
                cmd += ["--coulomb-cutoff", str(value)]
            elif key == "dsf_alpha":
                cmd += ["--dsf-alpha", str(value)]
            elif key == "ewald_accuracy":
                cmd += ["--ewald-accuracy", str(value)]
            elif key == "dftd3_cutoff":
                cmd += ["--dftd3-cutoff", str(value)]
            elif key == "dftd3_smoothing_fraction":
                cmd += ["--dftd3-smoothing-fraction", str(value)]

        self._process = Process()
        try:
            self._process.start(cmd)
        except Exception as e:
            self._process = None
            raise e

        # Wait for server to be ready
        return self._wait_for_ready()

    def shutdown(self) -> bool:
        """Send shutdown request and wait for server to exit."""
        if not self.is_running():
            return True

        try:
            self._send_request({"type": "shutdown"})
        except Exception:
            pass

        if self._process:
            self._process.stop_process()
        self._process = None
        return True

    def is_running(self) -> bool:
        """Check if server process is running."""
        if self._process is None:
            return False
        return self._process.process_is_running()

    def _wait_for_ready(self, timeout: float = 5.0) -> bool:
        """Wait for server socket to become available."""
        end = time.time() + timeout
        while time.time() < end:
            try:
                with socket.socket() as s:
                    s.settimeout(0.25)
                    s.connect((self._host, self._port))
                    return True
            except OSError:
                time.sleep(0.1)
        return False

    def _send_request(self, request: dict | Any) -> dict:
        """Send a request and receive the response."""
        with socket.socket() as s:
            s.settimeout(10.0)
            s.connect((self._host, self._port))
            s.sendall(pickle.dumps(request))
            data = s.recv(65536)
            return pickle.loads(data)


def start_server(**kwargs: Any) -> AIMNetCentralClient:
    """Start the AIMNetCentral server with the given configuration."""
    client = AIMNetCentralClient()
    client.start(**kwargs)
    return client


def shutdown_server(client: AIMNetCentralClient) -> None:
    """Shutdown the AIMNetCentral server."""
    client.shutdown()


def make_single_point_request(
    client: AIMNetCentralClient,
    ext_input: str,
    ext_output: str,
    **kwargs: Any,
) -> dict:
    """Make a single-point calculation request to the server."""
    request: dict[str, Any] = {
        "type": "sp",
        "ext_input": ext_input,
        "ext_output": ext_output,
    }
    request.update(kwargs)
    return client._send_request(request)


def run_with_server(**kwargs: Any) -> dict:
    """Run a single calculation with a temporary server."""
    client = AIMNetCentralClient()
    try:
        client.start(**kwargs)
        response = make_single_point_request(client, kwargs.get("ext_input", "orca.extinp"), kwargs.get("ext_output", "orca.extout"))
        return response
    finally:
        client.shutdown()


def run_with_server_batch(
    client: AIMNetCentralClient,
    requests: list[dict],
) -> list[dict]:
    """Run multiple calculations with a persistent server."""
    responses: list[dict] = []
    for req in requests:
        req.setdefault("type", "sp")
        responses.append(client._send_request(req))
    return responses
