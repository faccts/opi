from typing import Sequence
from pathlib import Path
import subprocess
from opi.execution.text_stream import open_text_stream_fanout, StreamTargetSpec, pump_text_stream
from dataclasses import dataclass
import threading


@dataclass(frozen=True)
class SubprocessRunResult:
    """
    Dataclass capturing information from the result of a subprocess.

    Attributes
    ----------
    returncode: int
        Exit code of the subprocess, non-zero signifies and error occurred.
    stdout: str
        Captured stdout from the subprocess, will be an empty string if
        capture stdout is not configured.
    stderr: str
        Captured stderr from the subprocess, will be an empty string if
        capture stderr is not configured.
    """

    returncode: int
    stdout: str
    stderr: str

    def returncode_ok(self) -> bool:
        """Check for zero exit code"""
        return self.returncode == 0

    def check_returncode(self):
        """Raise RuntimeError exit code is non-zero."""
        if not self.returncode_ok():
            raise RuntimeError(
                f"Command failed with exit code: {self.returncode}"
            )  # change to OpiExecutionError when PR #224 merged

    def get_signal(self) -> int | None:
        """Check and return IPC signals."""
        if self.returncode < 0:
            return abs(self.returncode)
        else:
            return None


def run_subprocess_with_fanout(
    cmd: Sequence[str],
    *,
    stdin: str | None = None,
    stdout: StreamTargetSpec = (),
    stderr: StreamTargetSpec = (),
    timeout: float | None = None,
    cwd: Path | None = None,
) -> SubprocessRunResult:
    """
    Run a subprocess outputting to multiple stdout and stderr target streams.

    Parameters
    ----------
    cmd : Sequence[str]
        Sequence of program arguments, e.g. ["orca", "job.inp"]
    stdin : str | None, optional
        Optional string to send to the stdin of the sbuprocess, by default None
    stdout : StreamTargetSpec, optional
        Single or multiple stream targets to pipe stdout to, by default ()
    stderr : StreamTargetSpec, optional
        Single or multiple stream targets to pipe stderr to, by default ()
    timeout : float | None, optional
        Optional timeout value in seconds, by default None
    cwd : Path | None, optional
        Optional working directory of the subprocess, by default None

    Returns
    -------
    SubprocessRunResult
        Result of the subprocess with returncode and optional captured stdout and stderr.

    Raises
    ------
    subprocess.TimeoutExpired
        Raised if a timeout is set and the process times out.
    BaseException
        After the process has finished, the first error accumulated from
        a failed write is raised.
    """
    with (
        open_text_stream_fanout(stdout) as stdout_target,
        open_text_stream_fanout(stderr) as stderr_target,
    ):
        # > Open new subprocess for the ORCA command.
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE if stdin is not None else None,
            # if stdout is active pipe output otherwise send to devnull
            stdout=subprocess.PIPE if stdout_target.active else subprocess.DEVNULL,
            # if stderr is active pipe output otherwise send to devnull
            stderr=subprocess.PIPE if stderr_target.active else subprocess.DEVNULL,
            cwd=cwd,
            text=True,  # Force text mode so that `stdout` and `stderr` are `IO[str]` streams.
            encoding="utf-8",
            errors="replace",  # Replace invalid bytes/chars with a replacement marker
            bufsize=1,  # buffer a single line at a time, TODO: should this be configurable?
        )

        errors: list[BaseException] = []  # List used for write error accumulations
        threads: list[threading.Thread] = []  # List to accumulate active write threads

        # > Check if stdout target is active and proc.stdout is a readable stream
        if stdout_target.active and proc.stdout is not None:
            # Create stdout write thread
            thread = threading.Thread(
                target=pump_text_stream,
                args=(proc.stdout, stdout_target, errors),
                daemon=True,
            )
            thread.start()
            threads.append(thread)

        # > Check if stderr target is active and proc.stdout is a readable stream
        if stderr_target.active and proc.stderr is not None:
            # Create stderr write thread
            thread = threading.Thread(
                target=pump_text_stream,
                args=(proc.stderr, stderr_target, errors),
                daemon=True,
            )
            thread.start()
            threads.append(thread)

        if stdin is not None and proc.stdin is not None:
            # Optionally pipe `stdin` to `proc.stdin`
            try:
                proc.stdin.write(stdin)
                proc.stdin.close()
            except BrokenPipeError:
                pass

        try:
            # Wait for the process to exit
            returncode = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            # Make sure the process has exitted
            proc.kill()
            proc.wait()

            # Join all active threads
            for thread in threads:
                thread.join()  # TODO: should we set a timeout?

            raise subprocess.TimeoutExpired(
                cmd=cmd,
                timeout=timeout or 0.0,  # appease the type checker
                output=stdout_target.get_captured(),
                stderr=stderr_target.get_captured(),
            ) from exc

        # Join active writer threads once the subprocess exits normally.
        for thread in threads:
            thread.join()

        # If any errors occurred in the writer threads then re-raise the first error.
        if errors:
            # TODO: should we configure whether to silence this error?
            raise errors[0]

        return SubprocessRunResult(
            returncode=returncode,
            stdout=stdout_target.get_captured(),
            stderr=stderr_target.get_captured(),
        )
