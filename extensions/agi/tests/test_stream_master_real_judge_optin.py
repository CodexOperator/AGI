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


def test_both_docstrings_name_the_flag_and_both_skipifs_use_the_gate():
    """Every real-judge module names AGI_REAL_JUDGE and gates via the shared helper."""
    for module in ("test_stream_master_semantic_screen.py",
                   "test_stream_master_blind_measure_v2.py"):
        src = _read_module(module)
        assert "AGI_REAL_JUDGE" in src.split('"""')[1], (
            f"{module} docstring does not name the opt-in flag")
        assert "real_judge_skip" in src, (
            f"{module} does not gate its real-judge class on the shared helper")