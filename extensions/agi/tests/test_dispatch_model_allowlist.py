"""Tests for the fail-closed model allowlist (hypothesis:l4-dispatch-model-allowlist).

The claim under test: `dispatch.py` REFUSES to spawn with an AGI_MODEL the
harness's `allowed_models` does not permit, FAIL-CLOSED — an absent or empty
list refuses EVERY model (it never means "allow everything"), and a `--seat`
override is not an exemption. The refusal is a non-zero exit whose message
names the refused model, the harness and the allowed list, and the dry-run
path reports the refusal the same way the live path does.

The dry run is the ground truth here: it resolves the full effective model
(the same `dispatch_harness["models"]` the live spawn reads) BEFORE any spawn,
so a refusal there is a refusal of the live spawn too.
"""
from __future__ import annotations

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
  - {"tier": 0, "role": "kid", "harness": "pi", "model": "~deepseek/deepseek-v4-flash-latest", "effort": "", "settings": ""}
  - {"tier": 1, "role": "parent", "harness": "pi", "model": "~z-ai/glm-flash-latest", "effort": "", "settings": ""}
---

body
"""

CONFIG_ALLOWED = {
    "harnesses": {
        "pi": {
            "adapter": "pi", "provider": "openrouter",
            "models": {"kid": "~deepseek/deepseek-v4-flash-latest",
                       "parent": "~z-ai/glm-flash-latest"},
            "allowed_models": ["~deepseek/deepseek-v4-flash-latest",
                               "~z-ai/glm-flash-latest"],
        },
    },
    "spawn": {"harness": "pi", "parallel": 1, "max_live": 25},
}


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps(CONFIG_ALLOWED))
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


def _write_config(project: Path, config: dict) -> None:
    (project / ".agi" / "config.json").write_text(json.dumps(config))


def test_allowed_model_still_spawns_and_carries_agi_model(project):
    """P(1): a dispatch with an ALLOWED model still spawns -- the dry-run env
    line carries AGI_MODEL and the run exits 0."""
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    assert "AGI_MODEL=~z-ai/glm-flash-latest" in r.stdout, r.stdout


def test_disallowed_model_refuses_naming_model_harness_and_list(project):
    """P(2): a model not in the list REFUSES with a non-zero exit and a
    message naming model, harness and the allowed list."""
    cfg = dict(CONFIG_ALLOWED)
    cfg["harnesses"]["pi"]["models"]["parent"] = "~some-other/model"
    _write_config(project, cfg)
    # drop the tier-1 parent row so the config fallback model (~some-other/model)
    # is what actually resolves -- the ladder row would otherwise win.
    ladder = (project / ".agi" / "nodes" / ".geometry" / "ladder.md")
    ladder.write_text("""---
current_season: 2
roles:
  - {"tier": 0, "role": "kid", "harness": "pi", "model": "~deepseek/deepseek-v4-flash-latest", "effort": "", "settings": ""}
---

body
""")
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode != 0, r.stdout
    assert "~some-other/model" in r.stderr, r.stderr
    assert "pi" in r.stderr, r.stderr
    assert "~z-ai/glm-flash-latest" in r.stderr, r.stderr
    assert "allowed_models" in r.stderr, r.stderr


def test_seat_override_naming_disallowed_model_refuses(project):
    """P(3): a `--seat` override is NOT an exemption -- a seat row whose model
    is disallowed must refuse exactly like a direct dispatch."""
    seats = project / ".agi" / "nodes" / ".geometry" / "seats.md"
    seats.write_text("---\nseats:\n"
                     "  - {name: rogue, tier: 1, role: parent, "
                     "harness: pi, model: ~some-other/model, "
                     "effort: \"\", settings: \"\"}\n---\n")
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--seat", "rogue", "--target", "hypothesis:x", "--dry-run")
    assert r.returncode != 0, r.stdout
    assert "~some-other/model" in r.stderr, r.stderr
    assert "rogue" in repr(r.stderr) or "pi" in r.stderr, r.stderr


def test_empty_allowed_models_refuses_every_model(project):
    """P(4a): an EMPTY `allowed_models` must refuse -- the gate does not open
    on an empty list."""
    cfg = dict(CONFIG_ALLOWED)
    cfg["harnesses"]["pi"]["allowed_models"] = []
    _write_config(project, cfg)
    r = _run(project, "--harness", "pi", "--tier", "kid",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode != 0, r.stdout
    assert "absent or empty" in r.stderr, r.stderr
    assert "~deepseek/deepseek-v4-flash-latest" in r.stderr, r.stderr


def test_absent_allowed_models_refuses_every_model(project):
    """P(4b): an ABSENT `allowed_models` (key missing entirely) must refuse --
    fail-closed, not fail-open. This is the 'deleted the key' case."""
    cfg = dict(CONFIG_ALLOWED)
    del cfg["harnesses"]["pi"]["allowed_models"]
    _write_config(project, cfg)
    r = _run(project, "--harness", "pi", "--tier", "kid",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode != 0, r.stdout
    assert "absent or empty" in r.stderr, r.stderr
