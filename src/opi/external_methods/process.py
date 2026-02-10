import subprocess
from enum import Enum
from typing import Any


# Error type definitions
class ProcessAlreadyRunningError(Exception):
    """Raised when start() is called while a process is already running."""


class ProcessStatus(Enum):
    NOT_RUNNING = "not_running"
    RUNNING = "running"
    SOFT_KILLED = "soft_killed"
    HARD_KILLED = "hard_killed"
    ERROR = "error"


class Process:
    """
    Class that runs a process, monitors it and terminates it.
    """

    def __init__(self) -> None:
        """
        Init Process object
        """
        # Variable for storing the process
        self.process: subprocess.Popen[bytes] | None = None

    def start(self, cmd: list[str], pipe: bool = False) -> None:
        """
        Starts a subprocess

        Attributes
        ----------
        cmd: list[str]
            List of arguments to be executed
        pipe: bool, default: False
            Determines whether to hold the channel open for piping input in or not.

        Raises
        ------
        ProcessAlreadyRunningError
            If a process is already running.
        FileNotFoundError
            If the command cannot be found on the system PATH.
        ValueError
            If invalid arguments are passed to `subprocess.Popen`.
        subprocess.SubprocessError
            If an error occurs in the `subprocess` module during process creation.
        OSError
            For operating system related errors when starting the process.
        """
        # Check if process running
        if self.process_is_running():
            raise ProcessAlreadyRunningError

        pipe_kwargs: dict[str, Any] = {}
        if pipe:
            pipe_kwargs["stdin"] = subprocess.PIPE

        try:
            self.process = subprocess.Popen(cmd, **pipe_kwargs)
        except FileNotFoundError as e:
            self.process = None
            raise FileNotFoundError(f"Command not found: {cmd!r}") from e
        except ValueError as e:
            self.process = None
            raise ValueError(f"Invalid Popen arguments for {cmd!r}") from e
        except subprocess.SubprocessError as e:
            self.process = None
            raise subprocess.SubprocessError(f"Subprocess error for {cmd!r}") from e
        except OSError as e:
            self.process = None
            raise OSError(f"OS error while spawning {cmd!r}") from e

    def stop_process(self) -> ProcessStatus:
        """
        Kills the process if its running.

        Returns
        -------
        ProcessStatus
            Indicates how the process was stopped:
        """
        if not self.process_is_running():
            return ProcessStatus.NOT_RUNNING
        if self.process:
            proc = self.process
            proc.terminate()
            try:
                proc.wait(timeout=30)
                return ProcessStatus.SOFT_KILLED
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
                return ProcessStatus.HARD_KILLED
            finally:
                self.process = None
        else:
            return ProcessStatus.ERROR

    def process_is_running(self) -> bool:
        """
        Returns true if the process is running and false if not.

        Returns
        -------
        bool
            True if process is running, otherwise false
        """
        return self.process is not None and self.process.poll() is None
