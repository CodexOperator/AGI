"""Tests for dispatch.py's LOW-DOX stdout (hypothesis:l4-dispatch-echoes-less-
than-it-knows).

The claim under test: dispatch's console output is reduced to a reader's
contract. Two surfaces are locked here:

1. `--dry-run` (the cheapest spawn-shaped path, and the one that runs in
   CI/suites) must NEVER echo a key-shaped string or any env value that looks
   like a secret -- whether named like one (OPENROUTER_API_KEY, *_TOKEN, ...)
   or shaped like one (sk-, sk-or-v1-). The dry-report shows a fixed allowlist
   of non-secret metadata (AGI_TIER/AGI_MODEL/AGI_AGENT_ID/...); a real-shaped
   fake key in the caller's env must not surface.

2. The redaction helpers (`_redact_env_map`, `_looks_like_secret`,
   `_redact_secret_value`) that build spawn.json for a debugger: redaction by
   BOTH name pattern and value shape, values reduced to "...last4" (never the
   value, a prefix, or a doxable fragment), and the real env untouched (the
   function returns a copy).

No envfile.py changes here; there was no forbidden-pattern helper to import,
so the name/value patterns are copied into this test verbatim from the
hypothesis's HARD RULES (name: KEY, TOKEN, SECRET, PASSWORD; value: sk-,
sk-or-v1-).
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"

LADDER = """---
current_season: 2
roles:
  - {"tier": 1, "role": "parent", "harness": "pi", "model": "~z-ai/glm-flash-latest", "effort": "", "settings": ""}
  - {"tier": 0, "role": "kid", "harness": "pi", "model": "~deepseek/deepseek-v4-flash-latest", "effort": "", "settings": ""}
---

body
"""

CONFIG = {
    "harnesses": {
        "pi": {
            "adapter": "pi", "provider": "openrouter",
            "models": {"kid": "deepseek-v4", "parent": "glm-flash"},
            "allowed_models": ["deepseek-v4", "glm-flash",
                               "~deepseek/deepseek-v4-flash-latest",
                               "~z-ai/glm-flash-latest"],
        },
        "claude-code": {
            "adapter": "claude_code",
            "models": {"kid": "claude-sonnet-5", "parent": "claude-opus-5"},
            "allowed_models": ["claude-sonnet-5", "claude-opus-5"],
        },
    },
    "spawn": {"harness": "pi", "parallel": 1, "max_live": 25},
}


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    """A scratch agi project: `.agi/` with a config and a ladder roles table."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps(CONFIG))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(LADDER)
    return tmp_path


def _run(project: Path, *args, env=None) -> subprocess.CompletedProcess:
    base = dict(os.environ)
    if env:
        for k, v in env.items():
            if v is None:
                base.pop(k, None)
            else:
                base[k] = v
    return subprocess.run(
        [sys.executable, str(BIN / "dispatch.py"), str(project), "1", *args],
        capture_output=True, text=True, env=base,
    )


# A value-shaped fake key, indistinguishable from a real OpenRouter key by
# anything other than the provider's own accounting.
FAKE_KEY = "sk-or-v1-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbb"


# --- dry-run stdout must stay secret-free ---------------------------------


@pytest.mark.parametrize("tier", ["kid", "parent"])
def test_dry_run_stdout_carries_no_environment_key_value(project, tier):
    """hypothesis (a): `--dry-run` with a real-shaped fake runtime key in the
    caller's env must not echo the key VALUE, its prefix, or any fragment of
    it on stdout. The dry-report's env line is an allowlist of non-secret
    metadata, never a dump of the caller's environment."""
    r = _run(project, "--harness", "pi", "--tier", tier,
             "--target", "hypothesis:x", "--dry-run",
             env={"OPENROUTER_API_KEY": FAKE_KEY})
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert FAKE_KEY not in out
    assert "sk-or-v1-" not in out
    # the value as a whole and any prefix length
    assert "sk-or-v1-aaaaaaaa" not in out


@pytest.mark.parametrize("tier", ["kid", "parent"])
def test_dry_run_stdout_carries_no_name_shaped_secret(project, tier):
    """A key-shaped NAME (not just a value-shaped one) must also be safe: a
    *_TOKEN/_SECRET/_PASSWORD var in the caller's env is not in the dry-report
    allowlist, so neither its name nor value may surface."""
    for var in ("MY_ACCESS_TOKEN", "FOO_SECRET", "DB_PASSWORD"):
        val = "supersecretvalue-" + var.lower()
        r = _run(project, "--harness", "pi", "--tier", tier,
                 "--target", "hypothesis:x", "--dry-run",
                 env={var: val})
        assert r.returncode == 0, r.stderr
        assert val not in r.stdout
        assert var + "=" not in r.stdout


def test_dry_run_stdout_still_carries_the_reader_contract(project):
    """The reader's contract survives the low-dox pass: the dry-report env
    line still carries the non-secret metadata a parent polls on (identity,
    seat, tier), and the brief is summarized, not printed wholesale."""
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "AGI_AGENT_ID=" in out
    assert "AGI_TIER=parent" in out
    assert "first 20:" in out  # brief summarized, not dumped
    assert "harness=pi" in out


# --- the spawn.json redaction helpers -------------------------------------


def _load_dispatch():
    spec = importlib.util.spec_from_file_location("dispatch", BIN / "dispatch.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["dispatch"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_redact_env_map_redacts_by_name_and_value_shape():
    dispatch = _load_dispatch()
    redacted = dispatch._redact_env_map({
        "OPENROUTER_API_KEY": FAKE_KEY,           # name pattern
        "MY_ACCESS_TOKEN": "1234567890abcdef",    # name pattern (TOKEN)
        "UNNAMED_SHAPED": "sk-abcdefghijkl",      # value shape only
        "AGI_MODEL": "glm-flash",                 # not secret
        "PLAIN_PATH": "/home/user/some/thing",    # not secret
    })
    assert redacted["OPENROUTER_API_KEY"] == "...abbb", redacted
    assert redacted["MY_ACCESS_TOKEN"] == "...cdef", redacted
    assert redacted["UNNAMED_SHAPED"] == "...ijkl", redacted
    # non-secrets survive verbatim
    assert redacted["AGI_MODEL"] == "glm-flash"
    assert redacted["PLAIN_PATH"] == "/home/user/some/thing"
    # NO secret value, prefix, or substantial fragment survives anywhere
    dump = json.dumps(redacted)
    assert FAKE_KEY not in dump
    assert "sk-or-v1-" not in dump
    assert "sk-abcdefghijkl" not in dump
    assert dump.count("...") >= 3


def test_redact_secret_value_never_carries_a_doxable_prefix():
    dispatch = _load_dispatch()
    assert dispatch._redact_secret_value("abcdefghij") == "...ghij"
    assert dispatch._redact_secret_value("abcd") == "<redacted>"  # too short to fragment safely


def test_looks_like_secret_name_and_shape():
    dispatch = _load_dispatch()
    # name pattern
    assert dispatch._looks_like_secret("OPENROUTER_API_KEY", "not-a-real-key")
    assert dispatch._looks_like_secret("AUTH_TOKEN", "x")
    assert dispatch._looks_like_secret("DB_PASSWORD", "x")
    # value shape, regardless of name
    assert dispatch._looks_like_secret("UNNAMED", "sk-or-v1-anything")
    assert dispatch._looks_like_secret("UNNAMED", "sk-anything")
    # neither
    assert not dispatch._looks_like_secret("AGI_MODEL", "glm-flash")
    assert not dispatch._looks_like_secret("AGI_SEAT", "liaison")