"""Tests for the DERIVED model allowlist (hypothesis:l4-a-model-change-is-one-write).

The claim under test: `dispatch.py` allows the model the ladder `roles:` row
resolves — the ALLOWED set is now DERIVED as {every ladder row's model for that
harness} ∪ `harnesses.<h>.allowed_extra` — so a model write on the ladder is ONE
write and is allowed WITHOUT editing the config's allowlist. The gate still
fails CLOSED for a model no row and no extra names (an absent/empty allowed
set refuses every model, a `--seat` override is not an exemption). The config's
legacy `allowed_models` key is a NON-INPUT: carrying it still works (unioned
for one cut-over round) but raises exactly ONE stderr warning; it no longer
has to be edited for a new ladder model to spawn — the four-cells-in-three-files
defect the hypothesis measures.

The dry run is the ground truth: it resolves the full effective model (the same
`dispatch_harness["models"]` the live spawn reads) BEFORE any spawn, so a
refusal there is a refusal of the live spawn too.
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

CONFIG = {
    "harnesses": {
        "pi": {
            "adapter": "pi", "provider": "openrouter",
            "models": {"kid": "~deepseek/deepseek-v4-flash-latest",
                       "parent": "~z-ai/glm-flash-latest"},
            "allowed_extra": ["~z-ai/glm-flash-latest"],
        },
    },
    "spawn": {"harness": "pi", "parallel": 1, "max_live": 25},
}


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps(CONFIG))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(LADDER)
    return tmp_path


def _run(project: Path, *args, env=None) -> subprocess.CompletedProcess:
    base = dict(os.environ)
    # A spawned dispatch re-roots via AGI_TREE_PROJECT_ROOT/AGI_PROJECT_ROOT
    # (child_working_graph); tests target their own tmp_path, so scrub those.
    base.pop("AGI_TREE_PROJECT_ROOT", None)
    base.pop("AGI_PROJECT_ROOT", None)
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


def _write_ladder(project: Path, ladder_text: str) -> None:
    (project / ".agi" / "nodes" / ".geometry" / "ladder.md").write_text(
        ladder_text)


def test_allowed_model_still_spawns_and_carries_agi_model(project):
    """P(1): a dispatch with an ALLOWED model (in a ladder row) still spawns —
    the dry-run env line carries AGI_MODEL and the run exits 0."""
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    assert "AGI_MODEL=~z-ai/glm-flash-latest" in r.stdout, r.stdout


def test_ladder_model_change_is_one_write_no_config_edit(project):
    """P(one-write): a NEW model written ONLY into a ladder row is allowed and
    dispatches WITHOUT any config edit — the allowlist is DERIVED from the
    ladder, so this is the whole "four cells in three files" defect collapsing
    into one write (hypothesis:l4-a-model-change-is-one-write)."""
    _write_ladder(project, """---
current_season: 2
roles:
  - {"tier": 0, "role": "kid", "harness": "pi", "model": "~deepseek/deepseek-v4-flash-latest", "effort": "", "settings": ""}
  - {"tier": 1, "role": "parent", "harness": "pi", "model": "deepseek/deepseek-v4.1-flash", "effort": "", "settings": ""}
---

body
""")
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    assert "AGI_MODEL=deepseek/deepseek-v4.1-flash" in r.stdout, r.stdout
    assert "--model deepseek/deepseek-v4.1-flash" in r.stdout, r.stdout


def test_model_in_no_row_and_no_extra_is_refused(project):
    """P(2): a model in neither a ladder row nor `allowed_extra` REFUSES with a
    non-zero exit and a message naming model, harness and the derived list."""
    # Parent model comes from a SEAT row naming a model no ladder row and no
    # allowed_extra admits — the seat is not an exemption.
    seats = project / ".agi" / "nodes" / ".geometry" / "seats.md"
    seats.write_text("---\nseats:\n"
                     "  - {name: rogue, tier: 1, role: parent, "
                     "harness: pi, model: ~some-other/model, "
                     "effort: \"\", settings: \"\"}\n---\n")
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--seat", "rogue", "--target", "hypothesis:x", "--dry-run")
    assert r.returncode != 0, r.stdout
    assert "~some-other/model" in r.stderr, r.stderr
    assert "pi" in r.stderr, r.stderr


def test_extra_census_admits_a_model_outside_ladder_rows(project):
    """P(extra): `harnesses.<h>.allowed_extra` adds to the derived census, so a
    model the ladder does not row (e.g. a director not yet on the ladder) is
    still spawnable."""
    _write_config(project, dict(
        CONFIG,
        harnesses={"pi": {
            "adapter": "pi", "provider": "openrouter",
            "models": {"director": "~z-ai/glm-flash-latest"},
            "allowed_extra": ["~z-ai/glm-flash-latest"],
        }}) )
    seats = project / ".agi" / "nodes" / ".geometry" / "seats.md"
    seats.write_text("---\nseats:\n"
                     "  - {name: dd, tier: 0, role: director, harness: pi, "
                     "model: ~z-ai/glm-flash-latest, effort: \"\", "
                     "settings: \"\"}\n---\n")
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--seat", "dd", "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    assert "AGI_MODEL=~z-ai/glm-flash-latest" in r.stdout, r.stdout


def test_legacy_allowed_models_is_warned_but_does_not_govern(project):
    """P(legacy): a config that still carries the deprecated `allowed_models`
    key gets ONE stderr warning; the derived ladder census governs — so a NEW
    ladder model that the config list does NOT name is still allowed."""
    _write_config(project, dict(
        CONFIG,
        harnesses={"pi": {
            "adapter": "pi", "provider": "openrouter",
            "models": {"kid": "~deepseek/deepseek-v4-flash-latest",
                       "parent": "~z-ai/glm-flash-latest"},
            # stale census: does NOT include the new parent model below
            "allowed_models": ["~deepseek/deepseek-v4-flash-latest",
                               "~z-ai/glm-flash-latest"],
        } }) )
    _write_ladder(project, """---
current_season: 2
roles:
  - {"tier": 0, "role": "kid", "harness": "pi", "model": "~deepseek/deepseek-v4-flash-latest", "effort": "", "settings": ""}
  - {"tier": 1, "role": "parent", "harness": "pi", "model": "deepseek/deepseek-v4.1-flash", "effort": "", "settings": ""}
---

body
""")
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    assert "AGI_MODEL=deepseek/deepseek-v4.1-flash" in r.stdout, r.stdout
    # the legacy allowlist key is warned (non-input), it does not govern
    assert "allowed_models is legacy" in r.stderr, r.stderr
    # exactly ONE non-input warning for the model cells names the ladder row
    assert r.stderr.count("NON-INPUTS") == 1, r.stderr


def test_empty_derived_census_refuses_every_model(project):
    """P(4a): an EMPTY derived census must refuse — the gate does not open on
    an empty set. Build a harness with no ladder row, no allowed_extra (and a
    config fallback model) so the derived set is empty."""
    _write_ladder(project, """---
current_season: 2
roles: []
---

body
""")
    _write_config(project, dict(
        CONFIG,
        harnesses={"pi": {
            "adapter": "pi", "provider": "openrouter",
            "models": {"kid": "~deepseek/deepseek-v4-flash-latest"},
            "allowed_extra": [],
        } }) )
    r = _run(project, "--harness", "pi", "--tier", "kid",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode != 0, r.stdout
    assert "absent or empty" in r.stderr, r.stderr
    assert "~deepseek/deepseek-v4-flash-latest" in r.stderr, r.stderr


def test_absent_allowed_models_key_no_longer_refuses(project):
    """P(4b): the ABSENT legacy `allowed_models` key is no longer a refusal —
    the derived census (ladder rows + allowed_extra) governs. The old
    "deleted the key" case is now a NON-INPUT, not a gate opening."""
    cfg = dict(CONFIG)
    del cfg["harnesses"]["pi"]["allowed_extra"]  # keep config minimal
    _write_config(project, cfg)
    r = _run(project, "--harness", "pi", "--tier", "kid",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    assert "AGI_MODEL=~deepseek/deepseek-v4-flash-latest" in r.stdout, r.stdout