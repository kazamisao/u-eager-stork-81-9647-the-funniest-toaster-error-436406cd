"""Tests for main.py: the program must write one short toaster error line.

Gate (from the kit): /output/entry.txt must be UTF-8 text of 1 to 120
characters, not only white space, on a single line.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent


def run_main(out_dir: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["MAKEFUN_OUTPUT_DIR"] = str(out_dir)
    return subprocess.run(
        [sys.executable, str(REPO / "main.py")],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_writes_one_valid_line():
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        proc = run_main(out_dir)
        assert proc.returncode == 0, f"main.py failed: {proc.stderr}"
        entry = out_dir / "entry.txt"
        assert entry.exists(), "entry.txt was not written"
        raw = entry.read_bytes()
        text = raw.decode("utf-8")  # must be valid UTF-8
        assert "\r" not in text, "no carriage returns allowed"
        line = text.strip()
        assert line, "entry must not be only white space"
        assert "\n" not in line, "entry must be a single line"
        assert 1 <= len(line) <= 120, f"entry is {len(line)} chars, must be 1-120"
        print(f"entry ({len(line)} chars): {line}")


def test_deterministic_two_runs():
    with tempfile.TemporaryDirectory() as tmp:
        first = Path(tmp) / "a"
        second = Path(tmp) / "b"
        first.mkdir()
        second.mkdir()
        assert run_main(first).returncode == 0
        assert run_main(second).returncode == 0
        assert (first / "entry.txt").read_bytes() == (second / "entry.txt").read_bytes()
