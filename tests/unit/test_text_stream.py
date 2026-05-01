# tests/test_fanout.py

from __future__ import annotations

import io
import subprocess
import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import pytest

from opi.execution.run import run_subprocess_with_fanout, SubprocessRunResult
from opi.execution.text_stream import TextStreamFanout, open_text_stream_fanout, pump_text_stream


@pytest.mark.unit
def test_fanout_capture_only() -> None:
    target = TextStreamFanout()
    target.add_capture()

    assert target.active is True

    target.write("hello")
    target.write(" world")

    assert target.get_captured() == "hello world"


@pytest.mark.unit
def test_fanout_write_to_io_callback_and_capture() -> None:
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
def test_fanout_returns_none_when_capture_not_enabled() -> None:
    target = TextStreamFanout()
    buffer = io.StringIO()

    target.add_stream(buffer)
    target.write("not captured")

    assert buffer.getvalue() == "not captured"
    assert target.get_captured() == ""


@pytest.mark.unit
def test_open_multi_text_io_supports_path_io_callback_and_capture(
    tmp_path: Path,
) -> None:
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
def test_popen_captures_stdout() -> None:
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
def test_popen_captures_stdout_and_stderr_separately() -> None:
    code = "import sys\n" "print('stdout text')\n" "print('stderr text', file=sys.stderr)\n"

    result = run_subprocess_with_fanout(
        [sys.executable, "-c", code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 0
    assert result.stdout == "stdout text\n"
    assert result.stderr == "stderr text\n"


@pytest.mark.unit
def test_popen_fans_out_stdout_to_capture_file_io_and_callback(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "child.out"
    buffer = io.StringIO()
    callback_chunks: list[str] = []

    code = "print('alpha')\n" "print('beta')\n"

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
def test_popen_accepts_stdin_str() -> None:
    code = "import sys\n" "data = sys.stdin.read()\n" "print(data.upper(), end='')\n"

    result = run_subprocess_with_fanout(
        [sys.executable, "-c", code],
        stdin="hello subprocess",
        stdout=subprocess.PIPE,
    )

    assert result.returncode == 0
    assert result.stdout == "HELLO SUBPROCESS"


@pytest.mark.unit
def test_popen_streams_before_process_exits() -> None:
    """
    This is the important streaming test.

    The child prints 'started', flushes, then sleeps before printing 'finished'.

    We run the parent-side runner in a thread. The callback should receive
    'started' while the subprocess is still sleeping, before the runner returns.

    If this fails, your pump is probably buffering until EOF.
    """
    saw_started = threading.Event()
    runner_finished = threading.Event()

    callback_chunks: list[str] = []

    def on_stdout(chunk: str) -> None:
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

    def run() -> None:
        result_holder["result"] = run_subprocess_with_fanout(
            [sys.executable, "-c", code],
            stdout=[subprocess.PIPE, on_stdout],
            timeout=5.0,
        )
        runner_finished.set()

    thread = threading.Thread(target=run)
    thread.start()

    assert saw_started.wait(timeout=0.5), "stdout was not streamed before the process finished"

    assert (
        not runner_finished.is_set()
    ), "runner finished too early; test did not prove live streaming"

    thread.join(timeout=5.0)

    assert runner_finished.is_set()
    assert result_holder["result"].returncode == 0
    assert result_holder["result"].stdout == "started\nfinished\n"
    assert "".join(callback_chunks) == "started\nfinished\n"


@pytest.mark.unit
def test_popen_streams_stderr_before_process_exits() -> None:
    saw_warning = threading.Event()
    runner_finished = threading.Event()

    stderr_chunks: list[str] = []

    def on_stderr(chunk: str) -> None:
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

    def run() -> None:
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
def test_popen_raises_timeout_expired() -> None:
    code = "import time\n" "time.sleep(10)\n"

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
def test_invalid_stream_targets(stdout, stderr) -> None:
    with pytest.raises(TypeError):
        run_subprocess_with_fanout(
            [sys.executable, "-c", "pass"],
            stdout=stdout,
            stderr=stderr,
        )
