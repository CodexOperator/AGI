"""Tests for the per-invocation memory cap override.

hypothesis:lm-dispatch-memory-override-feeds-agi-batch-scheduling: a
`--memory` GB option on dispatch.py, threaded as
`resolve_memory_cap(cfg, override=args.memory)`, overrides the config value for
that ONE dispatch call only and falls back to `spawn.memory_max` exactly as
today when the flag is absent.

Falsifiers under test:
(a) `--memory 2G` on a real dispatch does not change the spawn record's
    `memory_max` -- here proved at the resolver + dry-run layers;
(b) omitting `--memory` changes behaviour versus today (no-flag regression);
(c) the override mutates `.agi/config.json` on disk -- checked by byte-hashing
    the scratch config before and after a `--memory` run.

The scratch project's config is a fixture under tmp_path; the repo's own
`.agi/config.json` is never written by any test here.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import mem_cap  # noqa: E402

LADDER = """---
current_season: 2
roles:
  - {"tier": 0, "role": "kid", "harness": "pi", "model": "~deepseek/deepseek-v4-flash-latest", "effort": "", "settings": ""}
---

body
"""

CONFIG = {
    "harnesses": {
        "pi": {
            "adapter": "pi", "provider": "openrouter",
            "models": {"kid": "~deepseek/deepseek-v4-flash-latest"},
            "allowed_models": ["~deepseek/deepseek-v4-flash-latest"],
        },
    },
    "spawn": {"harness": "pi", "parallel": 1, "max_live": 25,
              "memory_max": "6G"},
}


# ---- unit: resolver semantics ---------------------------------------------

def test_override_wins_verbatim():
    assert mem_cap.resolve_memory_cap(
        {"spawn": {"memory_max": "6G"}}, override="2G") == "2G"


def test_no_override_is_the_config_value():
    assert mem_cap.resolve_memory_cap(
        {"spawn": {"memory_max": "6G"}}, override=None) == "6G"


def test_override_none_normalises_to_none():
    assert mem_cap.resolve_memory_cap(
        {"spawn": {"memory_max": "6G"}}, override="none") is None


def test_override_does_not_mutate_cfg():
    cfg = {"spawn": {"memory_max": "6G"}}
    mem_cap.resolve_memory_cap(cfg, override="2G")
    assert cfg == {"spawn": {"memory_max": "6G"}}


def test_absent_config_value_still_defaults_to_4g():
    # no-flag regression guard for the pre-existing behaviour
    assert mem_cap.resolve_memory_cap({}) == "4G"
    assert mem_cap.resolve_memory_cap({"spawn": {}}) == "4G"


# ---- dispatch --dry-run: the cap is observable without a spawn -------------

def _project(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps(CONFIG))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(LADDER)
    return tmp_path


def _run(project: Path, *args) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(BIN / "dispatch.py"), str(project), "1", *args],
        capture_output=True, text=True, env=dict(os.environ),
    )


def test_dry_run_memory_flag_prints_the_override(tmp_path):
    project = _project(tmp_path)
    r = _run(project, "--harness", "pi", "--tier", "kid",
             "--target", "hypothesis:x", "--dry-run", "--memory", "2G")
    assert r.returncode == 0, r.stderr
    assert "memory_max=2G" in r.stdout, r.stdout


def test_dry_run_without_the_flag_prints_the_configured_value(tmp_path):
    project = _project(tmp_path)
    r = _run(project, "--harness", "pi", "--tier", "kid",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    assert "memory_max=6G" in r.stdout, r.stdout


def test_memory_override_never_writes_the_config_on_disk(tmp_path):
    project = _project(tmp_path)
    cfg_path = project / ".agi" / "config.json"
    before = hashlib.sha256(cfg_path.read_bytes()).hexdigest()
    r = _run(project, "--harness", "pi", "--tier", "kid",
             "--target", "hypothesis:x", "--dry-run", "--memory", "2G")
    assert r.returncode == 0, r.stderr
    after = hashlib.sha256(cfg_path.read_bytes()).hexdigest()
    assert before == after, "the override mutated .agi/config.json on disk"