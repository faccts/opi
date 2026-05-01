from typing import Sequence
from pathlib import Path
import subprocess
from opi.execution.text_stream import open_text_stream_fanout, StreamTargetSpec, pump_text_stream
from dataclasses import dataclass
import threading


@dataclass(frozen=True)
class SubprocessRunResult:
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
    with (
        open_text_stream_fanout(stdout) as stdout_target,
        open_text_stream_fanout(stderr) as stderr_target,
    ):
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE if stdin is not None else None,
            stdout=subprocess.PIPE if stdout_target.active else subprocess.DEVNULL,
            stderr=subprocess.PIPE if stderr_target.active else subprocess.DEVNULL,
            cwd=cwd,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )

        errors: list[BaseException] = []
        threads: list[threading.Thread] = []

        if proc.stdout is not None:
            thread = threading.Thread(
                target=pump_text_stream,
                args=(proc.stdout, stdout_target, errors),
                daemon=True,
            )
            thread.start()
            threads.append(thread)

        if proc.stderr is not None:
            thread = threading.Thread(
                target=pump_text_stream,
                args=(proc.stderr, stderr_target, errors),
                daemon=True,
            )
            thread.start()
            threads.append(thread)

        if proc.stdin is not None:
            try:
                proc.stdin.write(stdin or "")
                proc.stdin.close()
            except BrokenPipeError:
                pass

        try:
            returncode = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            proc.kill()
            proc.wait()

            for thread in threads:
                thread.join()

            raise subprocess.TimeoutExpired(
                cmd=cmd,
                timeout=timeout or 0.0,  # appease the type checker
                output=stdout_target.get_captured(),
                stderr=stderr_target.get_captured(),
            ) from exc

        for thread in threads:
            thread.join()

        if errors:
            raise errors[0]

        return SubprocessRunResult(
            returncode=returncode,
            stdout=stdout_target.get_captured(),
            stderr=stderr_target.get_captured(),
        )
