import socket
import subprocess
import sys
import time
from enum import Enum
from multiprocessing.connection import Client
from typing import Any

from opi.external_methods.process import Process, ProcessAlreadyRunningError


class ServerStatus(Enum):
    RUNNING = "running"
    PORT_IN_USE = "port_in_use"
    ALREADY_RUNNING = "already_running"
    EXEC_NOT_FOUND = "exec_not_found"
    INVALID_ARGS = "invalid_args"
    SUBPROCESS_ERROR = "subprocess_error"
    OS_ERROR = "os_error"
    BOOT_TIMEOUT = "boot_timeout"


class OpiServer:
    """
    Class for running a server from a file using a network socket.
    """

    def __init__(self, serverpath: str, host_id: str = "127.0.0.1", port: int = 8888):
        """
        Initialize server object with default values.

        Attributes
        ----------
        serverpath: str
            Path to the server script
        host_id: str, default: 127.0.0.1 (for local server only)
            IP to bind server to.
            Can be changed, if someone wants, e.g., a network server.
        port: int, default: 8888
            Port for the server
        """
        self.process = Process()  # Process starting the server
        self.serverpath = serverpath
        self._host_id = host_id
        self._port = port

    def set_id_and_port(self, host_id: str, port: int) -> None:
        """
        Change the host_id and port.

        Attributes
        ----------
        host_id: str
            host_id ID.
        port: int
            Port to use.
        """
        self._host_id = host_id
        self._port = port

    def _wait_for_port(self, host: str, port: int, timeout: float = 10.0) -> bool:
        """
        Waits a little and checks if the server is reachable within the required time

        Parameters
        host: str
            Host ID
        port: str
            Port of server
        timeout:
            float, default: 5.0 (sec)
        """
        end = time.time() + timeout
        while time.time() < end:
            with socket.socket() as s:
                s.settimeout(0.25)
                try:
                    s.connect((host, port))
                    return True
                except OSError:
                    time.sleep(0.1)
        return False

    def start_server(
        self,
        cmd_arguments: str | None = None,
        exe: str = sys.executable,
        max_boot_time: float = 20.0,
    ) -> ServerStatus:
        """
        Starts the Server from script
        Passes self._host_id and self._port as command-line arguments to the server script.

        Parameters
        ----------
        cmd_arguments: str | None, default: None
            cmd arguments that should be passed to the server
        exe: str, default: sys.executable
            Executable to use for starting the server
        max_boot_time: float, default: 5.0 (sec)
            Maximum time in sec to wait till server is booted

        Returns
        -------
        ServerStatus: Indicates if server is running or the type of error
        """
        # First check, whether server.port is free
        if self.server_port_in_use():
            return ServerStatus.PORT_IN_USE
        else:
            # Start server by running a python process
            # Therefore, first set up the command line call for the server script
            # Build the command list:
            # ["python", server_script] + -b ID:port + optional args
            cmd = [exe, self.serverpath]
            cmd.append("-b")
            cmd.append(f"{self._host_id}:{self._port}")
            if cmd_arguments:
                cmd.append(cmd_arguments)
            # Start the server
            try:
                self.process.start(cmd)
            except ProcessAlreadyRunningError:
                return ServerStatus.ALREADY_RUNNING
            except FileNotFoundError:
                return ServerStatus.EXEC_NOT_FOUND
            except ValueError:
                return ServerStatus.INVALID_ARGS
            except subprocess.SubprocessError:
                return ServerStatus.SUBPROCESS_ERROR
            except OSError:
                return ServerStatus.OS_ERROR

        # Wait until the port is reachable
        if not self._wait_for_port(self._host_id, self._port, timeout=max_boot_time):
            # best effort cleanup
            try:
                self.process.stop_process()
            finally:
                pass
            return ServerStatus.BOOT_TIMEOUT

        return ServerStatus.RUNNING

    def kill_server(self) -> None:
        """
        Terminates the server if running
        """
        self.process.stop_process()

    def server_port_in_use(self) -> bool:
        """
        Checks whether self._port is already in use.

        Returns
        -------
        bool
            True if the port is in use (something is listening), False otherwise.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Quick fail if not open
            result = sock.connect_ex((self._host_id, self._port))
            return result == 0  # Port is in use if connect_ex returns 0


class CalcServer:
    """
    Class for running an OpiServer and load a calculator via pickle
    """

    def __init__(
        self,
        serverpath: str,
        calculator: Any = None,
        host_id: str = "127.0.0.1",
        port: int = 8888,
    ):
        """
        Initialize server object with default values.

        Attributes
        ----------
        serverpath: str
            Path to the server script
        calculator: Any, default: None
            Anything that can be send to the server via pickle
            Intended here to be calculator
        host_id: str, default: 127.0.0.1 (for local server only)
            IP to bind server to
            Can be changed, if someone wants, e.g., a network server
        port: int, default: 8888
            Port for the server
        """
        # Server values are set one time at the beginning and not changed
        # If a new server should be set up, a new CalcServer instance must be initialized
        self.server = OpiServer(serverpath=serverpath, host_id=host_id, port=port)
        self._calculator = calculator

    @property
    def calculator(self) -> Any:
        return self._calculator

    @calculator.setter
    def calculator(self, calc: Any) -> None:
        self._calculator = calc

    def set_id_and_port(self, host_id: str, port: int) -> bool:
        """
        Change the host_id and port if server not running.

        Attributes
        ----------
        host_id: str
            host_id ID.
        port: int
            Port to use.

        Return
        bool: Whether setup was successfully or not
        """
        if not self.server.server_port_in_use():
            self.server.set_id_and_port(host_id=host_id, port=port)
            return True
        else:
            return False

    def load_calculator(self) -> None:
        """
        Send the calculator to the server via pickle. Return response.
        """
        # Open a connection to server
        address = (self.server._host_id, self.server._port)
        with Client(address) as conn:
            conn.send({"type": "setup_calculator", "calculator": self._calculator})

    def start_server(self, exe: str = sys.executable) -> ServerStatus:
        """
        Start the server.

        Parameters
        ----------
        exe: str, default=sys.executable
            Executable to use for starting the server

        Returns
        -------
        bool: True if server started correctly
        """
        return self.server.start_server(exe=exe)

    def kill_server(self) -> None:
        """
        Kill the server.
        """
        self.server.kill_server()
