"""Tests for the H4 orphan-verdict gate — bin/evidence_gate.py + both writer paths.

Rule under test: `proved`/`disproved` require `evidence_runs >= 1`;
`pending` and `inconclusive_lean_*` are permitted without evidence.
Violations demote (never discard) the node.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"


def _load(name, filename=None):
    path = BIN / (filename or f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


eg = _load("evidence_gate")
cli = _load("cli")
post_wire = _load("post_wire")


ALL_VERDICTS = [
    "proved",
    "disproved",
    "inconclusive_lean_proved:60",
    "inconclusive_lean_disproved:40",
    "pending",
]


# ---------------------------------------------------------------- pure gate


@pytest.mark.parametrize("verdict", ALL_VERDICTS)
def test_taxonomy_is_valid(verdict):
    assert eg.is_valid_verdict(verdict)


def test_cli_uses_the_shared_taxonomy():
    """One regex, not two — cli.py must not drift from the gate."""
    assert cli.VERDICT_RE is eg.VERDICT_RE


@pytest.mark.parametrize("bad", ["PROVED", "maybe", "inconclusive_lean_proved", "", None])
def test_invalid_verdicts_rejected(bad):
    assert not eg.is_valid_verdict(bad)


@pytest.mark.parametrize("verdict", ["proved", "disproved"])
def test_decisive_without_evidence_is_demoted(verdict):
    res = eg.apply_gate(verdict, 0)
    assert res.demoted
    assert not res.ok
    assert res.verdict == eg.DEMOTION[verdict]
    assert res.original == verdict
    assert res.messages  # loud


@pytest.mark.parametrize("verdict", ["proved", "disproved"])
def test_decisive_with_evidence_passes(verdict):
    res = eg.apply_gate(verdict, 1)
    assert res.ok
    assert res.verdict == verdict
    assert res.messages == []


@pytest.mark.parametrize(
    "verdict", ["pending", "inconclusive_lean_proved:60", "inconclusive_lean_disproved:40"]
)
def test_uncertain_verdicts_permitted_without_evidence(verdict):
    res = eg.apply_gate(verdict, 0)
    assert res.ok
    assert res.verdict == verdict
    assert res.messages == []


def test_bypass_is_loud_and_preserves_verdict():
    res = eg.apply_gate("proved", 0, bypass=True)
    assert res.ok
    assert res.bypassed
    assert res.verdict == "proved"
    assert any("BYPASSED" in m for m in res.messages)


def test_bypass_is_a_noop_when_evidence_exists():
    res = eg.apply_gate("proved", 3, bypass=True)
    assert not res.bypassed and res.ok


@pytest.mark.parametrize(
    "value,expected",
    [
        (None, 0), (0, 0), (2, 2), (-5, 0),
        ([], 0), ([{"run": 1}, {"run": 2}], 2),
        ("3", 3), ("many", 0), ({"a"}, 1), (True, 1),
    ],
)
def test_normalize_evidence_runs(value, expected):
    assert eg.normalize_evidence_runs(value) == expected


def test_stamp_records_demotion():
    fm = eg.stamp({}, eg.apply_gate("proved", 0))
    assert fm["verdict"] == "inconclusive_lean_proved:50"
    assert fm["demoted_from"] == "proved"
    assert fm["demote_reason"]
    assert fm["evidence_runs"] == 0


# ------------------------------------------------------------ cli.py done


@pytest.fixture()
def project(tmp_path, monkeypatch):
    (tmp_path / "agi-tree.config.json").write_text("{}")
    (tmp_path / "nodes" / "experiment").mkdir(parents=True)
    sess = tmp_path / "sessions" / "iter-001" / "a1"
    sess.mkdir(parents=True)
    (sess / "agent.json").write_text(json.dumps({"id": "a1", "status": "running"}))
    monkeypatch.chdir(tmp_path)
    return tmp_path


def _via_subprocess(project, argv):
    return subprocess.run(
        [sys.executable, str(BIN / "cli.py"), *argv],
        cwd=project, capture_output=True, text=True,
    )


def _agent_rec(project):
    return json.loads(
        (project / "sessions" / "iter-001" / "a1" / "agent.json").read_text()
    )


def test_cli_done_demotes_unevidenced_proved(project):
    r = _via_subprocess(project, ["done", "1", "a1", "--verdict", "proved",
                                  "--node-id", "experiment:e1", "--evidence-runs", "0"])
    assert r.returncode == 0, r.stderr          # work preserved, not discarded
    assert "EVIDENCE-GATE DEMOTED" in (r.stdout + r.stderr)
    rec = _agent_rec(project)
    assert rec["verdict"] == "inconclusive_lean_proved:50"
    assert rec["demoted_from"] == "proved"
    node = project / "nodes" / "verdict" / "experiment_e1.md"
    assert "verdict: inconclusive_lean_proved:50" in node.read_text()
    assert "demoted_from: proved" in node.read_text()


def test_cli_done_accepts_evidenced_proved(project):
    r = _via_subprocess(project, ["done", "1", "a1", "--verdict", "proved",
                                  "--node-id", "experiment:e1", "--evidence-runs", "2"])
    assert r.returncode == 0, r.stderr
    assert "DEMOTED" not in r.stdout + r.stderr
    assert _agent_rec(project)["verdict"] == "proved"


def test_cli_done_permits_pending_and_leans_without_evidence(project):
    for verdict in ("pending", "inconclusive_lean_proved:60",
                    "inconclusive_lean_disproved:40"):
        r = _via_subprocess(project, ["done", "1", "a1", "--verdict", verdict,
                                      "--node-id", "experiment:e1"])
        assert r.returncode == 0, r.stderr
        assert "DEMOTED" not in r.stdout + r.stderr
        assert _agent_rec(project)["verdict"] == verdict


def test_cli_done_rejects_invalid_verdict(project):
    r = _via_subprocess(project, ["done", "1", "a1", "--verdict", "definitely"])
    assert r.returncode == 2
    assert "invalid verdict" in r.stderr


def test_cli_done_infers_evidence_from_node_frontmatter(project):
    """A real experiment must not be punished for a missing flag."""
    nf = project / "nodes" / "experiment" / "e1.md"
    nf.write_text(
        "---\nid: experiment:e1\ntype: experiment\n"
        "evidence_runs:\n  - run-a\n  - run-b\n---\n\nran it twice\n"
    )
    r = _via_subprocess(project, ["done", "1", "a1", "--verdict", "proved",
                                  "--node-id", "experiment:e1"])
    assert r.returncode == 0, r.stderr
    assert "DEMOTED" not in r.stdout + r.stderr
    assert "verdict: proved" in nf.read_text()


def test_cli_done_escape_hatch_is_loud(project):
    r = _via_subprocess(project, ["done", "1", "a1", "--verdict", "proved",
                                  "--node-id", "experiment:e1",
                                  "--evidence-runs", "0", "--no-evidence-gate"])
    assert r.returncode == 0, r.stderr
    assert "EVIDENCE-GATE BYPASSED" in (r.stdout + r.stderr)
    assert _agent_rec(project)["verdict"] == "proved"
    assert "evidence_gate: bypassed" in (
        project / "nodes" / "verdict" / "experiment_e1.md").read_text()


# ---------------------------------------------------------- post_wire path


@pytest.fixture()
def wired_project(tmp_path, monkeypatch):
    (tmp_path / "agi-tree.config.json").write_text("{}")
    exp = tmp_path / "nodes" / "experiment"
    exp.mkdir(parents=True)
    (exp / "e1.md").write_text(
        '---\nid: "experiment:e1"\ntype: experiment\n---\n\nbody\n'
    )
    iter_dir = tmp_path / "sessions" / "iter-001"
    iter_dir.mkdir(parents=True)
    monkeypatch.chdir(tmp_path)
    return tmp_path, iter_dir


def _wire(iter_dir, agent):
    (iter_dir / "manifest.json").write_text(json.dumps({"agents": [agent]}))
    import argparse
    return post_wire.cmd_wire(argparse.Namespace(iter_n=1, project_root=None))


def test_post_wire_demotes_unevidenced_proved(wired_project):
    root, iter_dir = wired_project
    _wire(iter_dir, {"id": "a1", "status": "done", "verdict": "proved",
                     "node_id": "experiment:e1", "evidence_runs": 0})
    text = (root / "nodes" / "experiment" / "e1.md").read_text()
    assert "verdict: inconclusive_lean_proved:50" in text
    assert "demoted_from: proved" in text


def test_post_wire_keeps_evidenced_proved(wired_project):
    root, iter_dir = wired_project
    _wire(iter_dir, {"id": "a1", "status": "done", "verdict": "proved",
                     "node_id": "experiment:e1", "evidence_runs": 4})
    text = (root / "nodes" / "experiment" / "e1.md").read_text()
    assert "verdict: proved" in text
    assert "demoted_from" not in text


def test_post_wire_permits_lean_without_evidence(wired_project):
    root, iter_dir = wired_project
    _wire(iter_dir, {"id": "a1", "status": "done",
                     "verdict": "inconclusive_lean_disproved:30",
                     "node_id": "experiment:e1", "evidence_runs": 0})
    text = (root / "nodes" / "experiment" / "e1.md").read_text()
    assert "verdict: inconclusive_lean_disproved:30" in text
    assert "demoted_from" not in text


def test_post_wire_falls_back_to_node_frontmatter_evidence(wired_project):
    root, iter_dir = wired_project
    nf = root / "nodes" / "experiment" / "e1.md"
    nf.write_text('---\nid: "experiment:e1"\ntype: experiment\n'
                  "evidence_runs:\n  - r1\n---\n\nbody\n")
    _wire(iter_dir, {"id": "a1", "status": "done", "verdict": "proved",
                     "node_id": "experiment:e1"})   # no evidence_runs key
    assert "verdict: proved" in nf.read_text()


def test_post_wire_creates_demoted_verdict_node_when_file_missing(wired_project):
    root, iter_dir = wired_project
    _wire(iter_dir, {"id": "a1", "status": "done", "verdict": "proved",
                     "node_id": "hypothesis:ghost", "evidence_runs": 0})
    text = (root / "nodes" / "verdict" / "ghost.md").read_text()
    assert "verdict: inconclusive_lean_proved:50" in text
    assert "demoted_from: proved" in text
