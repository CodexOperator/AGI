"""The committed integration test the falsifier asks for.

`goal:g7.32.2.1.2` — "unit-only is not landed". These cases drive the REAL
CLI (`python3 send.py pane ...` in a subprocess) so the production importer
is on a live path: delete the `magic_pane.deliver(` call in `send.py` and
every case here goes RED, while an in-process unit test of the module alone
would stay green — which is the gap the leaf exists to close.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
SEND = BIN / "send.py"


def _run(tmp_path: Path, *argv: str) -> subprocess.CompletedProcess:
    """Invoke the CLI as a child process inside a throwaway project root."""
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True, exist_ok=True)
    (root / ".agi" / "config.json").write_text(json.dumps({"box": {"name": "t"}}))
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("AGI_") and k not in ("PI_MODEL",)}
    return subprocess.run([sys.executable, str(SEND), *argv],
                          cwd=root, env=env, capture_output=True, text=True)


def test_pane_verb_exists_on_the_cli(tmp_path):
    r = _run(tmp_path, "--help")
    assert "pane" in r.stdout, r.stdout + r.stderr


def test_nudge_transport_lands_in_the_target_seat_inbox(tmp_path):
    r = _run(tmp_path, "pane", "grok", "pi", "hello", "seat",
             "--from", "grok")
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.strip().splitlines()[-1] == "nudge", r.stdout
    inbox = list((tmp_path / "proj" / ".agi" / "sessions").rglob("pi.md"))
    assert inbox, "nudge never reached the target seat: " + r.stdout + r.stderr
    assert "hello seat" in inbox[0].read_text()


def test_native_transport_writes_no_inbox(tmp_path):
    r = _run(tmp_path, "pane", "grok", "grok", "self", "--from", "grok")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "native" in r.stdout
    assert not list((tmp_path / "proj" / ".agi" / "sessions").rglob("pi.md"))


def test_unsupported_pair_refuses_loudly_with_nonzero_exit(tmp_path):
    r = _run(tmp_path, "pane", "claude", "pi", "nope", "--from", "claude")
    assert r.returncode == 1, r.stdout + r.stderr
    assert "refusing" in r.stderr, r.stdout + r.stderr
    assert "unsupported" in r.stdout
    assert not list((tmp_path / "proj" / ".agi" / "sessions").rglob("pi.md"))


def test_pane_requires_source_target_text(tmp_path):
    r = _run(tmp_path, "pane", "grok", "pi", "--from", "grok")
    assert r.returncode == 1
    assert "SOURCE TARGET TEXT" in r.stderr
