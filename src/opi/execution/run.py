import os
import signal
import subprocess
import threading
from dataclasses import dataclass
from pathlib import Path
from types import FrameType
from typing import Sequence, Callable, Any

from opi.execution.text_stream import StreamTargetSpec, open_text_stream_fanout, pump_text_stream

# > Signals that we need register a specific handler for, to forward them to the ORCA process.
SIGNALS_TO_FORWARD = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)


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

    def check_returncode(self) -> None:
        """Raise RuntimeError exit code is non-zero."""
        if not self.returncode_ok():
            raise RuntimeError(
                f"Command failed with exit code: {self.returncode}"
            )  # > change to OpiExecutionError when PR #224 merged

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
        Optional string to send to the stdin of the subprocess, by default None
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
    Exception
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
            # > if stdout is active pipe output otherwise send to devnull
            stdout=subprocess.PIPE if stdout_target.active else subprocess.DEVNULL,
            # > if stderr is active pipe output otherwise send to devnull
            stderr=subprocess.PIPE if stderr_target.active else subprocess.DEVNULL,
            cwd=cwd,
            text=True,  # > Force text mode so that `stdout` and `stderr` are `IO[str]` streams.
            encoding="utf-8",
            errors="replace",  # > Replace invalid bytes/chars with a replacement marker,
            # > Creating process in new session, so that we can later kill the entire process tree
            # > to avoid orphans
            start_new_session=True
        )
        # > Registering signal handler
        for sig in SIGNALS_TO_FORWARD:
            signal.signal(sig, _signal_handler(proc.pid))

        errors: list[Exception] = []  # > List used for write error accumulations
        threads: list[threading.Thread] = []  # > List to accumulate active write threads

        try:
            # > Check if stdout target is active and proc.stdout is a readable stream
            if stdout_target.active and proc.stdout is not None:
                # > Create stdout write thread
                thread = threading.Thread(
                    target=pump_text_stream,
                    args=(proc.stdout, stdout_target, errors),
                    daemon=True,
                )
                thread.start()
                threads.append(thread)

            # > Check if stderr target is active and proc.stdout is a readable stream
            if stderr_target.active and proc.stderr is not None:
                # > Create stderr write thread
                thread = threading.Thread(
                    target=pump_text_stream,
                    args=(proc.stderr, stderr_target, errors),
                    daemon=True,
                )
                thread.start()
                threads.append(thread)

            # > Create thread that writes to STDIN to avoid blocking
            if stdin is not None and proc.stdin is not None:
                thread = threading.Thread(
                    target=pump_text_stream,
                    args=(stdin, proc.stdin, errors),
                    daemon=True,
                )
                thread.start()
                threads.append(thread)

            try:
                # > Wait for the process to exit
                returncode = proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired as exc:
                # > First try a soft kill
                proc.terminate()
                try:
                    # > Wait 1min for cleanup
                    proc.wait(timeout=60)
                except subprocess.TimeoutExpired:
                    # > Kill the entire process tree with no mercy
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                    # > Adding another timeout just as precaution, as processes that wait for I/O might
                    # > be in deepsleep and cannot be killed.
                    try:
                        # > Wait 5 seconds minute. Killing should usually only take microseconds.
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        pass

                # > Join all active threads
                for thread in threads:
                    # > The timeout does not actually kill the thread if exceeded, but it makes sure
                    # > that `join()` does not block.
                    # >> I'm not aware of any way to kill threads, aside from terminating the parent process.
                    # >>> If the thread exceeds the timeout, STDOUT and STDERR captures will
                    # >>> mostly likely be incomplete.
                    thread.join(timeout=timeout)

                raise subprocess.TimeoutExpired(
                    cmd=cmd,
                    timeout=timeout or 0.0,  # > appease the type checker
                    output=stdout_target.get_captured(),
                    stderr=stderr_target.get_captured(),
                ) from exc

            # > Join active writer threads once the subprocess exits normally.
            for thread in threads:
                # > The timeout does not actually kill thread if it's exceed, but it makes sure
                # > that `join()` does not block.
                # >> I'm not aware of any way to kill threads, aside from terminating the parent process.
                thread.join(timeout=timeout)

            # > If any errors occurred in the writer threads then re-raise all of them.
            if errors:
                raise ExceptionGroup("ORCA execution", errors)

            return SubprocessRunResult(
                returncode=returncode,
                stdout=stdout_target.get_captured(),
                stderr=stderr_target.get_captured(),
            )
        finally:
            # > Restarting default signal handling again
            for sig in SIGNALS_TO_FORWARD:
                signal.signal(sig, signal.SIG_DFL)


def _signal_handler(pid: int, /) -> Callable[[int, FrameType | None], Any | int | signal.Handlers | None]:
    """
    Signal handler that forwards signals to the ORCA process group.
    This is necessary as the ORCA process is started in a separate session.

    Parameters
    ----------
    pid : int
        Process ID of the ORCA process.
    """

    def handler(signum: int, __: FrameType | None) -> Any | int | signal.Handlers | None:
        os.killpg(os.getpgid(pid), signum)

    return handler
