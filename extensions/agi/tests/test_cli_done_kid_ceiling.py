"""hypothesis:l4-cli-done-refuses-a-kid-past-2x-its-line-ceiling-without-a-
rebrief-request, conjunct (1) -- `cli.py done` is the enforcement point.

A KID done past 2x its production-line ceiling with no `rebrief_request` on
its node is REFUSED (rc 2, nothing written) and prints the exact write.py
line to file the request. A kid whose node carries `rebrief_request` passes.
Measurement is the kid's OWN uncommitted production diff (`git diff --numstat
HEAD`) because a kid never runs git, so there is no `done:` commit to read.
"""
import argparse
import json
import subprocess
from pathlib import Path


def _load_cli():
    import importlib.util
    bin_dir = Path(__file__).resolve().parents[1] / "bin"
    spec = importlib.util.spec_from_file_location(
        "agi_cli_done_kid_ceiling", bin_dir / "cli.py")
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    return cli


def _git(repo, *a):
    subprocess.run(["git", "-C", str(repo), *a], check=True,
                   capture_output=True)


def _kid_done_project(tmp_path, *, rebrief=False):
    """A git-backed fixture kid tree: .agi graph, a kid experiment node with a
    40-line ceiling (optionally carrying `rebrief_request`), an 81-line
    UNCOMMITTED production file (strictly ABOVE the 2x-40 ceiling, measured
    from HEAD), and a kid-tier agent record. Returns (graph, args)."""
    repo = tmp_path
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    graph = repo / ".agi"
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / "experiment" / "backer.md").write_text(
        "---\nid: experiment:backer\ntype: experiment\nparents:\n"
        "- hypothesis:h1\nmint_id: bb\n---\n\nbody\n")
    fm = ("---\nid: experiment:e1\ntype: experiment\nparents:\n"
          "- hypothesis:h1\nmint_id: aa\nline_ceiling: 40\n")
    if rebrief:
        fm += "rebrief_request: need more lines\n"
    fm += "---\n\n# experiment:e1\n\nbody\n"
    (graph / "nodes" / "experiment" / "e1.md").write_text(fm)
    _git(repo, "add", ".agi")
    _git(repo, "commit", "-qm", "base")
    src = repo / "src"
    src.mkdir()
    (src / "mod.py").write_text("\n".join(f"x = {i}" for i in range(81)) + "\n")
    # stage it so `git diff HEAD` (the brief's measurement verb) sees it -- a
    # kid's work tree has its changes as tracked-modification or nothing;
    # untracked files are the parent/merge's job, not this enforcer's.
    _git(repo, "add", "src/mod.py")
    (graph / "sessions" / "iter-001" / "a00-x").mkdir(parents=True)
    (graph / "sessions" / "iter-001" / "a00-x" / "agent.json").write_text(
        json.dumps({"id": "a00-x", "node_id": "experiment:e1",
                    "parent": "hypothesis:h1",
                    "status": "running", "tier": "kid"}))
    args = argparse.Namespace(
        iter_n=1, agent_id="a00-x", verdict="proved", confidence=0.9,
        node_id="experiment:e1", parent="hypothesis:h1", notes="",
        next_edge=None, evidence_runs=["experiment:backer"],
        no_evidence_gate=False, owns=None, no_spawn_gate=False,
        probes=None, dry_run=False, salvage=False,
    )
    return graph, args


def test_done_refuses_a_kid_past_2x_with_no_rebrief_request(tmp_path,
                                                           monkeypatch, capsys):
    """81 production lines / 40 ceiling, the node carries no rebrief_request ->
   rc 2, NOTHING written (the node keeps its verdict-less frontmatter), and
   the exact write.py line is printed."""
    cli = _load_cli()
    graph, args = _kid_done_project(tmp_path)
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    rc = cli.cmd_done(args)
    assert rc == 2
    err = capsys.readouterr().err
    assert "set rebrief_request 81/40: <why>" in err, err
    node_text = (graph / "nodes" / "experiment" / "e1.md").read_text()
    assert "verdict:" not in node_text, "a refused done wrote a verdict"


def test_done_passes_when_the_rebrief_request_is_on_the_node(tmp_path,
                                                            monkeypatch):
    """80/40 WITH rebrief_request set -> rc 0: the disclosure is on file, so
    the refusal must not fire and the done records normally."""
    cli = _load_cli()
    graph, args = _kid_done_project(tmp_path, rebrief=True)
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    assert cli.cmd_done(args) == 0