"""A `kind: round` stage's evidence is named, and a seam that cannot run a
round refuses it by name.

hypothesis:a-round-stage-fails-closed-by-name-and-every-inherited-review-
stage-is-gated — falsifiers 3 and 4. Stand-ins only: `subprocess.run` is the
dispatch stand-in, `_round_git_harvest` is the git-range stand-in, and the
claude-code branch is reached through the REAL `run_workflow` with the
manifest loading and the run key faked — nothing spawns a model.
"""
from __future__ import annotations

import io
import json
import subprocess
import sys
from pathlib import Path
from unittest import mock

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BIN))

import workflow as _wf  # noqa: E402

_ROUND_FILES = [
    ".agi/nodes/experiment/a00-abc123-11aa22.md",
    ".agi/nodes/verdict/a00-abc123-99ff00.md",
    ".agi/nodes/hypothesis/some-realm-claim.md",
    ".agi/context/schemas/experiment.md",
]


def _done_record(root):
    (root / "manifest.json").write_text(json.dumps(
        {"agents": [{"id": "a00-test", "status": "done", "branch": "loop/hyp",
                     "base_branch": "main"}]}), encoding="utf-8")


def _real_round_return(tmp_path, files):
    """`_run_round_stage` through the REAL return path: the dispatch stand-in
    prints `spawned`, the record reads done, the harvest returns `files`. Only
    the three process/clock seams are faked."""
    root = tmp_path / ".agi"
    root.mkdir(exist_ok=True)
    _done_record(root)
    with mock.patch.object(
            _wf.subprocess, "run",
            lambda cmd, **kw: subprocess.CompletedProcess(
                cmd, 0, "spawned a00-test\n", "")), \
         mock.patch.object(_wf, "_loc", mock.Mock(
             iteration_dir=lambda _r, _i: root)), \
         mock.patch.object(_wf, "_round_git_harvest",
                           lambda _r, _rec: {"old_tip": "o", "new_tip": "n",
                                             "files": files}), \
         mock.patch("dispatch._branch_has_done_commit",
                    lambda _r, _rec, _a: True), \
         mock.patch.object(_wf.time, "sleep", lambda _s: None):
        return _wf._run_round_stage(
            tmp_path, {}, {"target": "hypothesis:x", "iteration": "L1.01"}, 5)


# ---------- falsifier 3: the round payload names its own findings ----------

def test_round_payload_carries_experiments_and_verdict(tmp_path):
    """FALSIFIER 3 — a review prompt that writes `{experiments}` or
    `{verdict}` must render the round's OWN committed nodes. Before the fix
    the round returned no such keys, `_SafeDict` blanked both, and the review
    stage was asked to judge a round with no evidence in its context — a
    silent blank, indistinguishable from a short answer."""
    rc, value = _real_round_return(tmp_path, _ROUND_FILES)
    assert rc == 0
    assert value["experiments"] == ["a00-abc123-11aa22"]
    assert value["verdict"] == ["a00-abc123-99ff00"]
    # the hypothesis node is NOT one of the two named kinds
    assert "some-realm-claim" not in value["experiments"] + value["verdict"]
    st = {"label": "review-a", "chained_from": "round-parent",
          "prompt": "experiments={experiments} verdict={verdict}"}
    out = _wf.render_stage_prompt(st, {"target": "x"}, prior=value)
    assert "a00-abc123-11aa22" in out and "a00-abc123-99ff00" in out, out
    assert "{experiments}" not in out and "{verdict}" not in out, out


def test_round_payload_names_both_keys_even_when_the_round_is_empty(tmp_path):
    """The blank-vs-missing distinction: a round that committed no nodes of a
    kind hands `[]`, which reads as an EMPTY finding. A round that lacked the
    key rendered `''`, which reads as a stage that said nothing. The
    falsifier is the first; this pins the second away."""
    rc, value = _real_round_return(tmp_path, [])
    assert rc == 0
    assert value["experiments"] == [] and value["verdict"] == []
    st = {"label": "review-a", "chained_from": "round-parent",
          "prompt": "experiments={experiments} verdict={verdict}"}
    out = _wf.render_stage_prompt(st, {"target": "x"}, prior=value)
    assert out == "experiments=[] verdict=[]", out


def test_findings_are_keyed_from_the_committed_range_alone(tmp_path):
    """`_round_findings` reads the harvest's file list and nothing else — no
    config cell, no cwd, no second git call. A path outside the two node dirs
    never leaks into a finding list."""
    assert _wf._round_findings([]) == {"experiments": [], "verdict": []}
    assert _wf._round_findings(["nodes/experiment/x.md", "notes/verdict.md"]) \
        == {"experiments": ["x"], "verdict": []}
    # a node whose stem contains a dot (a hashed mint) still keys on the dir
    assert _wf._round_findings(
        ["a/b/nodes/verdict/h-1.2.3.md"])["verdict"] == ["h-1.2.3"]


# ---------- falsifier 4: a seam that cannot run a round refuses it --------

def _round_manifest(tmp_path):
    wf = tmp_path / "extensions" / "agi" / "workflows"
    wf.mkdir(parents=True)
    (wf / "base.json").write_text(json.dumps({
        "name": "base", "type": "review", "harness": "pi-free",
        "script": "agi-base.js",
        "stages": [{"label": "review-a", "role": "kid",
                    "model_hint": "claude-sonnet-5", "prompt": "review {target}",
                    "schema": {"type": "object",
                               "properties": {"ok": {"type": "boolean"}},
                               "required": ["ok"]}}],
    }), encoding="utf-8")
    (wf / "round.json").write_text(json.dumps({
        "name": "round", "extends": "base", "script": "agi-round.js",
        "prelude": [{"kind": "round", "label": "round-parent", "timeout_s": 1}],
        "stages": [],
    }), encoding="utf-8")
    return _wf._load_manifest(tmp_path, "round")


_CLAUDE_CFG = {"workflows": {"round": {"type": "review"}},
               "harnesses": {"claude-code": {
                   "adapter": "claude_code",
                   "models": {"kid": "claude-sonnet-5",
                              "parent": "claude-opus-5"},
                   "allowed_models": ["claude-sonnet-5", "claude-opus-5"]}}}


@pytest.mark.parametrize("dry_run", [False, True])
@pytest.mark.parametrize("seam", [True, False],
                         ids=["native-session", "headless"])
def test_claude_code_seam_refuses_a_round_stage_by_name(
        tmp_path, monkeypatch, capsys, seam, dry_run):
    """FALSIFIER 4 — the claude-code seam given a `kind: round` stage. It
    cannot dispatch a detached parent (only the pi path's `_run_round_stage`
    does), so it must REFUSE BY NAME. Measured before the fix: it printed the
    Workflow call, marked `round-parent resolved` and returned 0 — a run that
    spawned no parent reported every stage satisfied. Both seam branches and
    `--dry-run` are covered, so the dry run cannot promise a run the live
    path refuses."""
    manifest = _round_manifest(tmp_path)
    assert [s.get("kind") for s in manifest["stages"]] == ["round", None]
    monkeypatch.setattr(_wf, "_load_manifest", lambda r, k: manifest)
    monkeypatch.setattr(_wf, "_load_config", lambda r: _CLAUDE_CFG)
    monkeypatch.setattr(_wf, "_repo_root", lambda r: REPO)
    monkeypatch.setattr(_wf, "_mint_run_key", lambda *a: "probe-1")
    monkeypatch.setattr(_wf, "_track_run", lambda *a, **k: None)
    monkeypatch.setattr(_wf, "_claude_code_seam_present",
                        lambda env=None: seam)
    buf = io.StringIO()
    rc = _wf.run_workflow(REPO / ".agi", "round", "claude-code",
                          {"target": "hypothesis:x", "iteration": "L1.01"},
                          dry_run, out=buf)
    err = capsys.readouterr().err
    assert rc == 6, (rc, buf.getvalue(), err)
    assert "round-parent" in err and "kind=round" in err, err
    # it refused: no Workflow call handed back, nothing marked resolved
    assert "Workflow(" not in buf.getvalue(), buf.getvalue()
    assert "resolved" not in buf.getvalue(), buf.getvalue()


def test_the_refusal_does_not_touch_a_round_free_workflow(
        tmp_path, monkeypatch):
    """The same refusal must NOT fire for a manifest with no round stage —
    the claude-code branch keeps its two real routes (native tool call /
    headless notice) for a workflow it can actually describe."""
    wf = tmp_path / "extensions" / "agi" / "workflows"
    wf.mkdir(parents=True)
    (wf / "plain.json").write_text(json.dumps({
        "name": "plain", "type": "review", "harness": "pi-free",
        "script": "agi-plain.js",
        "stages": [{"label": "review-a", "role": "kid",
                    "model_hint": "claude-sonnet-5", "prompt": "review {target}"}],
    }), encoding="utf-8")
    manifest = _wf._load_manifest(tmp_path, "plain")
    monkeypatch.setattr(_wf, "_load_manifest", lambda r, k: manifest)
    monkeypatch.setattr(_wf, "_load_config", lambda r: _CLAUDE_CFG)
    monkeypatch.setattr(_wf, "_repo_root", lambda r: REPO)
    monkeypatch.setattr(_wf, "_mint_run_key", lambda *a: "probe-1")
    monkeypatch.setattr(_wf, "_track_run", lambda *a, **k: None)
    monkeypatch.setattr(_wf, "_claude_code_seam_present", lambda env=None: True)
    buf = io.StringIO()
    rc = _wf.run_workflow(REPO / ".agi", "plain", "claude-code",
                          {"target": "hypothesis:x"}, False, out=buf)
    assert rc == 0, buf.getvalue()
    assert 'Workflow({"name": "agi-plain"' in buf.getvalue(), buf.getvalue()
