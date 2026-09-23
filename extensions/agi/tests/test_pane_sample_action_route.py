"""goal:g7.31.3.2 — one sample agent action goes through the NAMED CLIs.

The falsifier under test: *a sample agent action for write + send + one
dispatch/workflow run goes through the named CLIs, not a parallel script
(transcript/experiment proof).*

So this module does not import the verbs. It executes ONE sample action
sequence by invoking the four named entry points under `extensions/agi/bin/`
as REAL subprocesses:

  (a) ``write.py``    — `set title` on a node in a scratch tmp project,
                        asserting the file CHANGED and `edited_by` is recorded
  (b) ``send.py``     — ``send <to> <body>`` with a plain, metacharacter-free
                        argv body, asserting the inbox block under the SCRATCH
                        project's `.agi/sessions/inbox/`
  (c) ``dispatch.py`` — ONE ``--dry-run`` route resolution, asserting rc 0 and
                        the `[dry-run] slot=...` line + the built command
  (d) ``workflow.py`` — ONE ``workflow.py run review --harness pi --dry-run``,
                        asserting rc 0 and the `via dispatch.py kids` summary

ISOLATION IS NON-NEGOTIABLE: every subprocess runs with ``cwd=`` the scratch
tmp project (and a scrubbed env — see `_child_env`), so nothing touches this
worktree's live `.agi/`. `--dry-run` is the ONLY safe way to exercise the
dispatch/workflow CLIs in a sample: it resolves everything a live spawn
resolves but mints nothing and spawns nothing (a live `dispatch.py` spawns a
paid agent, and a live `workflow.py run` dispatches one kid per stage).

The workflows registry is reached through a symlink under the scratch project
(`_repo_root` walks up from the project looking for `extensions/agi/workflows`),
so the ONE router — never a parallel invoker — is what runs here.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
REPO = Path(__file__).resolve().parents[3]
WF_DIR = REPO / "extensions" / "agi" / "workflows"

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
            # OpenRouter slugs, not bare aliases: workflow.py's pi path
            # fail-closes on a model outside the provider namespace.
            "models": {"kid": "~deepseek/deepseek-v4-flash-latest",
                       "parent": "~z-ai/glm-flash-latest"},
            "allowed_models": ["deepseek-v4", "glm-flash",
                               "~deepseek/deepseek-v4-flash-latest",
                               "~z-ai/glm-flash-latest"],
        },
    },
    "spawn": {"harness": "pi", "parallel": 1, "max_live": 25},
    "workflows": {"review": {"model": "sonnet", "effort": "low"}},
}

SAMPLE_NODE = (
    '---\n'
    'id: "hypothesis:sample-route"\n'
    'mint_id: cafebabe00000000000000000000abcd\n'
    'type: hypothesis\n'
    'title: "the pre-action title"\n'
    'testable_claim: "c"\n'
    'scaffold_hash: deadbeef\n'
    'status: pending\n'
    '---\n'
    '\n'
    'the sample body\n'
)


@pytest.fixture()
def sample_project(tmp_path: Path) -> Path:
    """A scratch tmp agi project + a symlink to the engine's workflows dir.

    `cwd` for every subprocess is this project. The project is under
    `tmp_path` (outside any git repo), so the shared-sessions resolver is the
    identity and the inbox lands in the scratch `.agi` — never in a live
    inbox.
    """
    proj = tmp_path / "sampleproj"
    graph = proj / ".agi"
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps(CONFIG))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(LADDER)
    (graph / "nodes" / "hypothesis" / "sample-route.md").write_text(SAMPLE_NODE)
    # workflow.py's _repo_root walks up from the project root looking for
    # `extensions/agi/workflows`; the symlink lets the ONE router's manifest
    # resolve while every write still lands in this scratch project.
    (proj / "extensions" / "agi").mkdir(parents=True)
    os.symlink(WF_DIR, proj / "extensions" / "agi" / "workflows")
    return proj


def _child_env() -> dict:
    """A scrubbed env: no AGI_* / PROJECT_ROOT re-rooting inherited from the
    calling agent, so every subprocess resolves the scratch project it was
    given rather than this worktree's live graph."""
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("AGI_")
           and k not in ("PROJECT_ROOT", "AUTORESEARCH_TREE_PROJECT_ROOT")}
    return env


def _run(project: Path, argv: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *argv], cwd=project, env=_child_env(),
        capture_output=True, text=True,
    )


# ── (a) write.py ────────────────────────────────────────────────────────────


def test_write_py_is_the_route_and_the_node_file_changes(sample_project):
    """`write.py` mutates a real node in the scratch project, and the mutation
    is observable on disk: the file changed and `edited_by` records the
    actor. A returncode-0-only assertion would pass on a no-op."""
    node = (sample_project / ".agi" / "nodes" / "hypothesis"
            / "sample-route.md")
    before = node.read_text()

    r = _run(sample_project, [
        str(BIN / "write.py"), "hypothesis:sample-route",
        "set title route sample lands through write.py",
        "--root", str(sample_project), "--actor", "a00-sample",
    ])
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)

    after = node.read_text()
    assert after != before, "write.py reported success but the node is unchanged"
    assert "route sample lands through write.py" in after
    assert "a00-sample" in after, "edited_by did not record the actor"


# ── (b) send.py ─────────────────────────────────────────────────────────────


def test_send_py_is_the_route_and_the_inbox_block_lands(sample_project):
    """`send.py send <to> <body>` with a plain, argv-safe body (no backticks,
    no shell metacharacters) lands a block under the SCRATCH project's
    `.agi/sessions/inbox/`, with `from:` recorded."""
    r = _run(sample_project, [
        str(BIN / "send.py"), "send", "sample-parent",
        "sample body with no backticks or shell metacharacters",
        "--from", "a00-sample",
    ])
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)

    inbox = (sample_project / ".agi" / "sessions" / "inbox"
             / "sample-parent.md")
    assert inbox.is_file(), f"no inbox block at {inbox}"
    text = inbox.read_text()
    assert "sample body with no backticks or shell metacharacters" in text
    assert "from: a00-sample" in text


# ── (c) dispatch.py ─────────────────────────────────────────────────────────


def test_dispatch_py_dry_run_resolves_the_route(sample_project):
    """ONE dispatch route resolution through `dispatch.py --dry-run`: rc 0,
    the `[dry-run] slot=...` line, and the built command string. `--dry-run`
    is the only safe sample: a live dispatch spawns a paid agent."""
    r = _run(sample_project, [
        str(BIN / "dispatch.py"), str(sample_project), "1",
        "--tier", "kid", "--target", "hypothesis:sample-route",
        "--harness", "pi", "--dry-run",
    ])
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
    out = r.stdout
    assert "[dry-run] slot=0" in out, out
    assert "  command: " in out, out
    assert "harness=pi" in out, out
    assert "nothing spawned, nothing written, no budget slot taken" in out, out
    # a dry run leaves no session dir and no node behind
    assert not (sample_project / ".agi" / "sessions").exists(), (
        "a dispatch dry run must not create a session dir")


# ── (d) workflow.py ─────────────────────────────────────────────────────────


def test_workflow_py_dry_run_is_the_one_router(sample_project):
    """ONE run through the ONE workflow router (`goal:g1.14`):
    `workflow.py run review --harness pi --dry-run` resolves every stage
    through `dispatch.py` and says so in its summary line. No parallel
    workflow invoker is written."""
    r = _run(sample_project, [
        str(BIN / "workflow.py"), "run", "review",
        "--harness", "pi", "--dry-run",
    ])
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
    out = r.stdout
    assert "via dispatch.py kids" in out, out
    assert "workflow=review" in out, out
    assert "harness=pi" in out, out
