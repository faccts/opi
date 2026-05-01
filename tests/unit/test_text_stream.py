# tests/test_fanout.py

from __future__ import annotations

import io
import subprocess
import sys
import threading
from pathlib import Path

import pytest

from opi.execution.run import SubprocessRunResult, run_subprocess_with_fanout
from opi.execution.text_stream import StreamTargetSpec, TextStreamFanout, open_text_stream_fanout


@pytest.mark.unit
def test_fanout_capture_only():
    """Test fanout captures output when explicitly calling write."""
    target = TextStreamFanout()
    target.add_capture()

    assert target.active is True

    target.write("hello")
    target.write(" world")

    assert target.get_captured() == "hello world"


@pytest.mark.unit
def test_fanout_write_multi():
    """Test fanout can write to multiple targets."""
    target = TextStreamFanout()

    buffer = io.StringIO()
    callback_chunks: list[str] = []

    target.add_capture()
    target.add_stream(buffer)
    target.add_callback(callback_chunks.append)

    target.write("abc")
    target.write("def")

    assert target.get_captured() == "abcdef"
    assert buffer.getvalue() == "abcdef"
    assert callback_chunks == ["abc", "def"]


@pytest.mark.unit
def test_fanout_no_capture():
    """Test that no buffer is captured if not enabled."""
    target = TextStreamFanout()
    buffer = io.StringIO()

    target.add_stream(buffer)
    target.write("not captured")

    assert buffer.getvalue() == "not captured"
    assert target.get_captured() == ""


@pytest.mark.unit
def test_open_text_stream_fanout(
    tmp_path: Path,
):
    """Test open stream is able to write to multiple targets."""
    output_path = tmp_path / "stdout.txt"
    buffer = io.StringIO()
    callback_chunks: list[str] = []

    with open_text_stream_fanout(
        [
            subprocess.PIPE,
            output_path,
            buffer,
            callback_chunks.append,
        ]
    ) as target:
        assert target.active is True

        target.write("line 1\n")
        target.write("line 2\n")

        captured = target.get_captured()

    expected = "line 1\nline 2\n"

    assert captured == expected
    assert output_path.read_text(encoding="utf-8") == expected
    assert buffer.getvalue() == expected
    assert callback_chunks == ["line 1\n", "line 2\n"]


@pytest.mark.unit
def test_subprocess_captures_stdout():
    """Test stdout is captured when running subprocess."""
    result = run_subprocess_with_fanout(
        [
            sys.executable,
            "-c",
            "print('hello from child')",
        ],
        stdout=subprocess.PIPE,
    )

    assert result.returncode == 0
    assert result.stdout == "hello from child\n"
    assert result.stderr == ""


@pytest.mark.unit
def test_subprocess_captures_stdout_and_stderr():
    """Test both stdout and stderr are captured when running subprocess."""
    code = "import sys\nprint('stdout text')\nprint('stderr text', file=sys.stderr)\n"

    result = run_subprocess_with_fanout(
        [sys.executable, "-c", code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 0
    assert result.stdout == "stdout text\n"
    assert result.stderr == "stderr text\n"


@pytest.mark.unit
def test_subprocess_fanout_multi(tmp_path: Path):
    """Test subprocess output fans out to multiple target streams"""
    output_path = tmp_path / "child.out"
    buffer = io.StringIO()
    callback_chunks: list[str] = []

    code = "print('alpha')\nprint('beta')\n"

    result = run_subprocess_with_fanout(
        [sys.executable, "-c", code],
        stdout=[
            subprocess.PIPE,
            output_path,
            buffer,
            callback_chunks.append,
        ],
    )

    expected = "alpha\nbeta\n"

    assert result.returncode == 0
    assert result.stdout == expected
    assert output_path.read_text(encoding="utf-8") == expected
    assert buffer.getvalue() == expected
    assert "".join(callback_chunks) == expected


@pytest.mark.unit
def test_subprocess_accepts_stdin():
    """Check subprocess can accept input from stdin"""
    code = "import sys\ndata = sys.stdin.read()\nprint(data.upper(), end='')\n"

    result = run_subprocess_with_fanout(
        [sys.executable, "-c", code],
        stdin="hello subprocess",
        stdout=subprocess.PIPE,
    )

    assert result.returncode == 0
    assert result.stdout == "HELLO SUBPROCESS"


@pytest.mark.unit
def test_subprocess_streams_before_process_exits():
    """
    Test subprocess streams output during execution.

    Ensures that we are able to capture output before the process exits.

    1. Child process prints 'started' and flushes.
    2. Child process sleeps for 1s.
    3. Child process prints 'finished' and exits.

    We run a separate thread from the parent process which uses a threading.Event
    with a timeout of 0.5s. As the child process is waiting for 1s we should recieve
    the 'started' signle while the subprocess is still sleeping.
    """
    saw_started = threading.Event()
    runner_finished = threading.Event()

    callback_chunks: list[str] = []

    def on_stdout(chunk: str):
        callback_chunks.append(chunk)
        if "started" in chunk:
            saw_started.set()

    code = (
        "import sys, time\n"
        "print('started', flush=True)\n"
        "time.sleep(1.0)\n"
        "print('finished', flush=True)\n"
    )

    result_holder: dict[str, SubprocessRunResult] = {}

    def run():
        result_holder["result"] = run_subprocess_with_fanout(
            [sys.executable, "-c", code],
            stdout=[subprocess.PIPE, on_stdout],
            timeout=5.0,
        )
        runner_finished.set()

    thread = threading.Thread(target=run)
    thread.start()

    assert saw_started.wait(timeout=0.5), "stdout was not streamed before the process finished"

    assert not runner_finished.is_set(), (
        "runner finished too early; test did not prove live streaming"
    )

    thread.join(timeout=5.0)

    assert runner_finished.is_set()
    assert result_holder["result"].returncode == 0
    assert result_holder["result"].stdout == "started\nfinished\n"
    assert "".join(callback_chunks) == "started\nfinished\n"


@pytest.mark.unit
def test_subprocess_streams_stderr_before_process_exits():
    """Same logic as the stdout streaming test with stderr."""
    saw_warning = threading.Event()
    runner_finished = threading.Event()

    stderr_chunks: list[str] = []

    def on_stderr(chunk: str):
        stderr_chunks.append(chunk)
        if "warning" in chunk:
            saw_warning.set()

    code = (
        "import sys, time\n"
        "print('warning', file=sys.stderr, flush=True)\n"
        "time.sleep(1.0)\n"
        "print('done', file=sys.stderr, flush=True)\n"
    )

    result_holder: dict[str, SubprocessRunResult] = {}

    def run():
        result_holder["result"] = run_subprocess_with_fanout(
            [sys.executable, "-c", code],
            stderr=[subprocess.PIPE, on_stderr],
            timeout=5.0,
        )
        runner_finished.set()

    thread = threading.Thread(target=run)
    thread.start()

    assert saw_warning.wait(timeout=0.5)
    assert not runner_finished.is_set()

    thread.join(timeout=5.0)

    assert runner_finished.is_set()
    assert result_holder["result"].returncode == 0
    assert result_holder["result"].stderr == "warning\ndone\n"
    assert "".join(stderr_chunks) == "warning\ndone\n"


@pytest.mark.unit
def test_subprocess_raises_timeout_expired():
    """Test subprocess fanout raises subprocess.TimeoutExpired"""
    code = "import time\ntime.sleep(10)\n"

    with pytest.raises(subprocess.TimeoutExpired):
        run_subprocess_with_fanout(
            [sys.executable, "-c", code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=0.2,
        )


@pytest.mark.unit
@pytest.mark.parametrize(
    ("stdout", "stderr"),
    [
        ((True,), ()),
        (subprocess.DEVNULL, ()),
        ((), (True,)),
        ((), subprocess.DEVNULL),
    ],
)
def test_invalid_stream_targets(stdout: StreamTargetSpec, stderr: StreamTargetSpec):
    """Test that TypeError is raised for invalide stream types"""
    with pytest.raises(TypeError):
        run_subprocess_with_fanout(
            [sys.executable, "-c", "pass"],
            stdout=stdout,
            stderr=stderr,
        )
