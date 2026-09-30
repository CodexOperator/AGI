"""hypothesis:g716103 — `reds.py check OLD NEW`: the ONE mechanical RED check
over a commit range, before any model.

One row per falsifier (F1-F6). Every value is SYNTHETIC and built by string
concatenation, so no test file carries a key-shaped literal; every repo and
config is a tmp fixture — no test reads or writes the live repo's history.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
CLASSES = ["secrets", "node_deletion", "broken_link"]
MAIL_HEAD, MAIL_TAIL = "person@ex", "ample.invalid"   # one email, two halves
MAIL = MAIL_HEAD + MAIL_TAIL
KEY = "sk-" + "SYNTHETIC" + "0123456789abcdef"      # shape only, never a real key


def _git(repo, *args):
    p = subprocess.run(["git", "-C", str(repo), *args], check=True,
                       capture_output=True, text=True)
    return p.stdout


def _node(nid, mint, **fm):
    head = "\n".join(f"{k}: {v}" for k, v in fm.items())
    return f"---\nid: {nid}\nmint_id: {mint}\n{head}\n---\n\nbody of {nid}\n"


@pytest.fixture
def proj(tmp_path):
    """A tmp project repo at commit `base`: two linked nodes, one already broken."""
    repo = tmp_path / "proj"
    g = repo / ".agi"
    for d in ("nodes/idea", "nodes/build"):
        (g / d).mkdir(parents=True, exist_ok=True)
    (repo / "notes").mkdir(parents=True, exist_ok=True)
    (g / "config.json").write_text(json.dumps({"merge_gate": {"red_classes": CLASSES}}))
    (g / "nodes/idea/one.md").write_text(_node("idea:one", "a" * 32, type="idea", status="live"))
    (g / "nodes/build/two.md").write_text(
        _node("build:two", "b" * 32, type="build", payload_ref="notes/payload.md"))
    (g / "nodes/idea/stale.md").write_text(
        _node("idea:stale", "c" * 32, type="idea", payload_ref="notes/never.md"))
    (repo / "notes/payload.md").write_text("payload\n")
    _git(repo.parent, "init", "-q", str(repo))
    _git(repo, "add", "-A")
    _git(repo, "-c", "user.email=t@example.invalid", "-c", "user.name=t",
         "commit", "-qm", "base")
    return repo


def _commit(repo, msg):
    _git(repo, "add", "-A")
    _git(repo, "-c", "user.email=t@example.invalid", "-c", "user.name=t",
         "commit", "-qm", msg)
    return _git(repo, "rev-parse", "HEAD").strip()


def _run(repo, old="HEAD", new="HEAD", root=None, env=None):
    return subprocess.run(
        [sys.executable, str(BIN / "reds.py"), "check", old, new,
         "--root", str(root or repo / ".agi"), "--repo", str(repo)],
        capture_output=True, text=True, env=env)


# F1 -- a key-shaped value on an ADDED line: rc 1, one secrets name, no bytes.
def test_f1_key_shaped_added_line_is_one_secret_and_never_prints_it(proj):
    base = _git(proj, "rev-parse", "HEAD").strip()
    (proj / "notes" / "leak.py").write_text(f'TOKEN = "{KEY}"\n')
    _commit(proj, "leak")
    r = _run(proj, base)
    assert r.returncode == 1, r.stderr
    assert "RED secrets 1" in r.stdout
    assert "leak.py" in r.stdout
    assert KEY not in r.stdout and KEY not in r.stderr
    assert "SYNTHETIC" not in r.stdout


# F2 -- a retire-move is NOT a deletion; a plain removal IS, named by node id.
def test_f2_move_to_deprecated_is_not_a_deletion_but_a_removal_is(proj):
    g = proj / ".agi"
    (g / "nodes/deprecated/idea").mkdir(parents=True)
    _git(proj, "mv", ".agi/nodes/idea/one.md", ".agi/nodes/deprecated/idea/one.md")
    base = _git(proj, "rev-parse", "HEAD").strip()
    _commit(proj, "move")
    r = _run(proj, base)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "RED node_deletion" not in r.stdout

    base = _git(proj, "rev-parse", "HEAD").strip()
    (g / "nodes/build/two.md").unlink()
    _commit(proj, "delete")
    r = _run(proj, base)
    assert r.returncode == 1, r.stdout
    assert "RED node_deletion 1: build:two" in r.stdout


# F3 -- a link broken at NEW is one; a link already broken at OLD is not.
def test_f3_new_broken_link_is_one_and_the_old_one_is_not_counted(proj):
    """`notes/fresh.md` exists at OLD; a commit deletes it. `idea:stale`'s link
    was already broken at base, so it is not a NEW break."""
    node = proj / ".agi" / "nodes/build/two.md"
    base = _git(proj, "rev-parse", "HEAD").strip()
    (proj / "notes/fresh.md").write_text("fresh\n")
    node.write_text(_node("build:two", "b" * 32, type="build", payload_ref="notes/fresh.md"))
    _commit(proj, "link a file that is there")
    assert _run(proj, base).returncode == 0, "a resolvable link is not a RED"

    base = _git(proj, "rev-parse", "HEAD").strip()
    (proj / "notes/fresh.md").unlink()
    _commit(proj, "delete the file the link names")
    r = _run(proj, base)
    assert r.returncode == 1, r.stdout
    assert "RED broken_link 1: build:two->notes/fresh.md" in r.stdout
    assert "idea:stale" not in r.stdout          # broken since base


# F4 -- an email split across two ADDED lines is not one (goal:g7.33.19 row 36).
def test_f4_email_split_across_lines_is_clean_and_one_line_is_not(proj):
    p = proj / "notes"
    p.joinpath("split.txt").write_text(f"a: {MAIL_HEAD}\nb: {MAIL_TAIL}\n")
    base = _git(proj, "rev-parse", "HEAD").strip()
    _commit(proj, "split")
    r = _run(proj, base)
    assert "RED secrets" not in r.stdout, r.stdout
    assert r.returncode == 0, r.stdout

    p.joinpath("whole.txt").write_text(f"a: {MAIL}\n")
    base = _git(proj, "rev-parse", "HEAD").strip()
    _commit(proj, "whole")
    r = _run(proj, base)
    assert r.returncode == 1 and "RED secrets 1" in r.stdout, r.stdout


# F5 -- the cell absent = all three + ONE WARN; a 2-class cell skips the third.
def test_f5_absent_cell_runs_all_three_with_one_warn_and_a_two_cell_skips_one(proj):
    cfg = proj / ".agi" / "config.json"
    base = _git(proj, "rev-parse", "HEAD").strip()
    cfg.write_text(json.dumps({"merge_gate": {"red_classes": ["secrets"]}}))
    _commit(proj, "narrow the cell")
    r = _run(proj, base)
    assert "secrets" in r.stdout.splitlines()[0]
    assert "node_deletion" not in r.stdout.splitlines()[0]
    assert "WARN" not in r.stderr

    base = _git(proj, "rev-parse", "HEAD").strip()
    cfg.write_text(json.dumps({}))
    _commit(proj, "drop the cell")
    r = _run(proj, base)
    line = r.stdout.splitlines()[0]
    assert all(c in line for c in CLASSES), line
    assert r.stderr.count("WARN") == 1, r.stderr


# F6 -- no model: fake `pi` and `claude` on PATH are never called.
def test_f6_no_model_is_started(proj, tmp_path):
    fake = tmp_path / "fakebin"
    fake.mkdir()
    record = tmp_path / "called.txt"
    for name in ("pi", "claude"):
        f = fake / name
        f.write_text(f'#!/bin/sh\necho {name} >> {record}\n')
        f.chmod(0o755)
    env = dict(os.environ, PATH=f"{fake}{os.pathsep}{os.environ['PATH']}")
    (proj / "notes" / "x.md").write_text("plain\n")
    base = _git(proj, "rev-parse", "HEAD").strip()
    _commit(proj, "no model here")
    r = _run(proj, base, env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    assert not record.exists(), "a model command ran"
