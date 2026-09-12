"""Real-judge opt-in gate (goal:g15).

The real stream-master ModelJudge run is gated on ONE explicit env flag,
AGI_REAL_JUDGE (default OFF), SHARED by both real-judge test modules through
one conftest helper -- never two spellings. A present OPENROUTER_API_KEY alone
spends nothing. These tests prove the gate directly (level3: the keyed
default-suite cost is proved by the gate, not by a live model call).

Invocation of the real measurement is the same one-liner named in both module
docstrings: `AGI_REAL_JUDGE=1 python3 -m pytest <file>`.
"""
import os
from pathlib import Path

from tests.conftest import real_judge_skip


def _read_module(name):
    return (Path(__file__).parent / name).read_text(encoding="utf-8")


def test_key_without_flag_is_off(monkeypatch):
    """A present OPENROUTER_API_KEY alone still spends nothing (default OFF)."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test")
    monkeypatch.delenv("AGI_REAL_JUDGE", raising=False)
    reason = real_judge_skip()
    assert reason is not None
    assert "AGI_REAL_JUDGE" in reason


def test_flag_without_key_is_off(monkeypatch):
    """The flag alone is not enough -- a key is still required."""
    monkeypatch.setenv("AGI_REAL_JUDGE", "1")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    reason = real_judge_skip()
    assert reason is not None
    assert "OPENROUTER_API_KEY" in reason


def test_flag_and_key_is_on(monkeypatch):
    """Only the explicit flag AND a present key turn the real run on."""
    monkeypatch.setenv("AGI_REAL_JUDGE", "1")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test")
    assert real_judge_skip() is None


def test_real_judge_flag_survives_conftest_strip_and_reads_live_env():
    """(c1) PROOF AT SUITE LEVEL, no monkeypatch of the flag, no network.

    A monkeypatch-only test sets the env AFTER conftest's strip, so it cannot
    distinguish "the flag survives the strip" from "monkeypatch re-set it".
    Two legs prove it without that hole:

      * mechanism -- parsed with ``ast``: the strip tuple that pops the
        sender-identity three (AGI_AGENT_ID/AGI_SEAT/AGI_POST) does NOT name
        AGI_REAL_JUDGE, so the opt-in lives past the strip by construction.
      * differential -- a REAL child pytest run (not a plain import) with the
        flag in the ACTUAL child env and no key: flag=1 must skip with the KEY
        reason (proving conftest's pytest_cmdline_main strip ran AND the flag
        survived it, so control reached the key check), flag unset must skip
        with the FLAG reason. A dead flag under the suite short-circuits on
        the FLAG reason in leg A. A monkeypatch test cannot substitute: it
        writes the environment after the strip, so it cannot know the strip
        did not also clear the flag.

    No real key is present, so no judge call and no network.
    """
    import ast
    import subprocess
    import sys

    tree = ast.parse(_read_module("conftest.py"))
    stripped = []
    for node in ast.walk(tree):
        if isinstance(node, ast.For) and isinstance(node.iter, ast.Tuple):
            names = [c.value for c in node.iter.elts
                     if isinstance(c, ast.Constant)
                     and isinstance(c.value, str)]
            if {"AGI_AGENT_ID", "AGI_SEAT", "AGI_POST"} <= set(names):
                stripped = names
    assert "AGI_AGENT_ID" in stripped, "strip tuple parsed from conftest"
    assert "AGI_REAL_JUDGE" not in stripped, \
        "conftest strip must not pop the opt-in flag"

    root = str(Path(__file__).resolve().parents[1])  # extensions/agi
    files = ["tests/test_stream_master_semantic_screen.py",
             "tests/test_stream_master_blind_measure_v2.py"]
    child_cmd = [sys.executable, "-m", "pytest"] + files + ["-q", "-rs"]

    def _output(flag):
        env = dict(os.environ)
        env.pop("OPENROUTER_API_KEY", None)
        if flag:
            env["AGI_REAL_JUDGE"] = "1"
        else:
            env.pop("AGI_REAL_JUDGE", None)
        p = subprocess.run(child_cmd, cwd=root, env=env,
                           capture_output=True, text=True, timeout=180)
        assert p.returncode == 0, p.stdout + p.stderr
        return p.stdout + p.stderr

    key_marker = ("ModelJudge has no OPENROUTER_API_KEY; real semantic "
                  "measurement unavailable in this environment")
    flag_marker = "AGI_REAL_JUDGE not set"

    key_out = _output(flag=True)
    flag_out = _output(flag=False)
    assert flag_marker not in key_out, key_out
    assert key_marker in key_out, \
        "flag set but gate never reached the key check -- dead under suite"
    assert flag_marker in flag_out, flag_out
    assert key_marker not in flag_out, flag_out


def test_both_docstrings_name_the_flag_and_both_skipifs_use_the_gate():
    """Every real-judge module names AGI_REAL_JUDGE and gates via the shared helper."""
    for module in ("test_stream_master_semantic_screen.py",
                   "test_stream_master_blind_measure_v2.py"):
        src = _read_module(module)
        assert "AGI_REAL_JUDGE" in src.split('"""')[1], (
            f"{module} docstring does not name the opt-in flag")
        assert "real_judge_skip" in src, (
            f"{module} does not gate its real-judge class on the shared helper")