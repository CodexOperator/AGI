"""The workflow template seam carries no hardcoded checkout path (.json half).

goal:g7.33.14.1 -- the 7 stale `extensions/agi/workflows/*.json` manifests
used to name `/home/ubuntu/work/agi` in their stage prompts, so a run started
in another box (or a git worktree) was pointed at the main checkout. The
RUNNER already injects the resolved root as `{project_root}`
(workflow.py `run_workflow` `args.setdefault("project_root", str(repo))`), and
`render_stage_prompt` falls back to the cwd's project root when a direct caller
passes none. This file locks that migration: every one of the 7 manifests
renders its root from the injected value, and the fallback still yields a real
directory.

It mirrors the existing guard for `research-review` in
`test_workflow.py` (R1) and extends it over the 7 migrated manifests.
"""
from __future__ import annotations

import json
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
REPO = Path(__file__).resolve().parents[3]
WF = REPO / "extensions" / "agi" / "workflows"

import sys  # noqa: E402

sys.path.insert(0, str(BIN))

import workflow  # noqa: E402
from workflow import render_stage_prompt  # noqa: E402

MIGRATED = [
    "review",
    "drafting",
    "prime-open-questions",
    "desktop-check",
    "recovery-survey",
    "g15-close-triage",
    "merge-up-review",
]

STALE = "/home/ubuntu/work/agi"


def _stages(name: str) -> list[dict]:
    """Every stage dict of a manifest, including nested chains/routines."""
    manifest = json.loads((WF / f"{name}.json").read_text(encoding="utf-8"))
    out: list[dict] = []

    def walk(node):
        if isinstance(node, dict):
            if isinstance(node.get("prompt"), str):
                out.append(node)
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(manifest)
    return out


def test_every_migrated_manifest_declares_a_stage_prompt():
    for name in MIGRATED:
        assert _stages(name), name


def test_no_migrated_manifest_carries_the_stale_literal():
    for name in MIGRATED:
        raw = (WF / f"{name}.json").read_text(encoding="utf-8")
        assert STALE not in raw, name


def test_migrated_stages_render_the_injected_project_root():
    """Every stage of every migrated manifest renders with NO stale literal
    and the injected value lands wherever the prompt references it."""
    worktree = "/tmp/fake-worktree"
    used = 0
    for name in MIGRATED:
        for st in _stages(name):
            out = render_stage_prompt(st, {"project_root": worktree})
            assert STALE not in out, (name, st.get("label"), out[:200])
            assert "cd  &&" not in out, (name, st.get("label"))
            if "{project_root}" in st["prompt"]:
                used += 1
                assert worktree in out, (name, st.get("label"), out[:200])
    # 12 stale literals lived in 10 stages (desktop-check and merge-up-review
    # name the root twice each), so 10 referencing stages is the full set.
    assert used == 10, used


def test_manifest_loads_through_the_runner_resolver():
    """The manifest still parses the way the runner parses it (a broken
    JSON edit fails here, not inside a pi run)."""
    for name in MIGRATED:
        m = workflow._load_manifest(REPO, name)
        assert m.get("stages"), name


def test_fallback_without_args_yields_a_real_existing_dir():
    """A direct caller that passes no project_root still gets a REAL path,
    never an empty `cd  &&` -- resolved from the cwd's project root."""
    st = {"label": "probe", "prompt": "cd {project_root} && true"}
    out = render_stage_prompt(st, {})
    resolved = out[len("cd "):-len(" && true")]
    assert resolved, out
    p = Path(resolved)
    assert p.is_dir(), resolved
    assert (p / ".agi").is_dir(), resolved
