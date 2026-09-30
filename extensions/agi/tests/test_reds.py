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
sys.path.insert(0, str(BIN))
from reds import CLASSES  # noqa: E402  -- ONE source: the gate names the classes
MAIL_HEAD, MAIL_TAIL = "person@ex", "ample.invalid"   # one email, two halves
MAIL = MAIL_HEAD + MAIL_TAIL
#: a commit-identity address the LIVE cell `anonymize.email_allow` admits
#: (example.com). `.invalid` is not admitted, so the gate's own bytes were RED.
WHO = "t@example.com"
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
    _git(repo, "-c", f"user.email={WHO}", "-c", "user.name=t",
         "commit", "-qm", "base")
    return repo


def _commit(repo, msg, *paths):
    _git(repo, "add", "-A", *paths)
    _git(repo, "-c", f"user.email={WHO}", "-c", "user.name=t",
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


# F7 -- fail CLOSED: a present-but-empty or all-unknown cell runs ALL THREE with
# ONE WARN. A gate that disables itself on a typo is the near miss the rule exists
# to prevent (parent probe P1/P2, DG3.51).
@pytest.mark.parametrize("cell", [[], ["nonsense"], ["nonsense", "other"]])
def test_f7_a_cell_naming_no_known_class_runs_all_three_with_one_warn(proj, cell):
    cfg = proj / ".agi" / "config.json"
    (proj / "notes" / "leak.py").write_text(f'TOKEN = "{KEY}"\n')
    (proj / ".agi" / "nodes" / "build" / "two.md").unlink()
    _git(proj, "add", "-A")
    _git(proj, "-c", f"user.email={WHO}", "-c", "user.name=t", "commit", "-qm", "red range")
    base = _git(proj, "rev-parse", "HEAD~1").strip()
    cfg.write_text(json.dumps({"merge_gate": {"red_classes": cell}}))
    _git(proj, "add", "-A")
    _git(proj, "-c", f"user.email={WHO}", "-c", "user.name=t", "commit", "-qm", "cell")
    r = _run(proj, base)
    line = r.stdout.splitlines()[0]
    assert r.returncode == 1, r.stdout + r.stderr
    assert all(c in line for c in CLASSES), line
    assert "RED secrets 1" in r.stdout and "RED node_deletion 1" in r.stdout, r.stdout
    assert r.stderr.count("WARN") == 1, r.stderr


# F7b -- a KNOWN class still narrows when an unknown name rides along, and the
# unknown name is named in ONE WARN rather than silently swallowed.
def test_f7b_a_known_class_narrows_but_an_unknown_name_still_warns(proj):
    cfg = proj / ".agi" / "config.json"
    (proj / "notes" / "leak.py").write_text(f'TOKEN = "{KEY}"\n')
    base = _git(proj, "rev-parse", "HEAD").strip()
    cfg.write_text(json.dumps({"merge_gate": {"red_classes": ["secrets", "nonsense"]}}))
    _commit(proj, "narrow the cell with a typo")
    r = _run(proj, base)
    line = r.stdout.splitlines()[0]
    assert r.returncode == 1, r.stdout + r.stderr
    assert "secrets" in line and "node_deletion" not in line and "broken_link" not in line
    assert r.stderr.count("WARN") == 1 and "nonsense" in r.stderr, r.stderr


# F8 (P13) -- a `parents:` id resolving to NO node is a broken_link: the graph
# edge broken_by_status cannot see. Broken since OLD is still not counted.
def _child(nid, mint, parents):
    lst = "".join(f"  - {p}\n" for p in parents)
    return f"---\nid: {nid}\nmint_id: {mint}\ntype: idea\nparents:\n{lst}---\n\nbody\n"


def test_f8_a_parents_id_with_no_node_is_a_broken_link(proj):
    g = proj / ".agi" / "nodes/idea"
    (g / "old-broken.md").write_text(_child("idea:oldbroken", "d" * 32, ["hypothesis:gone"]))
    _commit(proj, "a node whose parent already resolved nowhere")
    base = _git(proj, "rev-parse", "HEAD").strip()
    (g / "new-broken.md").write_text(_child("idea:newbroken", "e" * 32, ["hypothesis:absent"]))
    _commit(proj, "a node whose parent never existed")
    r = _run(proj, base)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "RED broken_link 1: idea:newbroken->hypothesis:absent" in r.stdout, r.stdout
    assert "idea:oldbroken" not in r.stdout          # broken since OLD
    (g / "new-broken.md").write_text(_child("idea:newbroken", "e" * 32, ["idea:one"]))
    base2 = _git(proj, "rev-parse", "HEAD").strip()
    _commit(proj, "point the parent at a node that exists")
    assert _run(proj, base2).returncode == 0, _run(proj, base2).stdout


# F9 -- a BARE key-shaped value is a RED: no `name =` in front, or glued behind `h/` `a.` `_` `--`.
def test_f9_a_bare_key_shaped_token_on_an_added_line_is_a_secret(proj):
    lines = ["the value is " + KEY, "https://h/" + KEY, "a." + KEY, "_" + KEY, "--" + KEY, "task-usage-report-v2"]
    (proj / "notes" / "bare.txt").write_text("\n".join(lines) + "\n")
    base = _git(proj, "rev-parse", "HEAD").strip()
    _commit(proj, "a bare key-shaped value")
    r = _run(proj, base)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "RED secrets 5" in r.stdout and "bare.txt:6" not in r.stdout, r.stdout
    assert KEY not in r.stdout + r.stderr


# F14 -- rc 2 names a foreign exception by CLASS only: an OSError's path never reaches stderr.
def test_f14_a_foreign_error_is_rc_two_by_class_name_only(proj, monkeypatch, capsys):
    import reds
    monkeypatch.setattr(reds, "_classes", lambda root: (_ for _ in ()).throw(OSError(13, "denied", "/abs/secret/path")))
    assert reds.main(["check", "HEAD", "HEAD", "--root", str(proj / ".agi"), "--repo", str(proj)]) == 2
    err = capsys.readouterr().err
    assert "PermissionError" in err and "/abs/secret" not in err, err


# F10 -- rc 2 is PINNED: a bad rev, and no path byte in the gate's own stderr.
def test_f10_a_bad_rev_is_rc_two_and_never_echoes_a_path(proj):
    r = _run(proj, "HEAD", "no-such-rev")
    assert r.returncode == 2, r.stdout + r.stderr
    assert "Traceback" not in r.stderr, r.stderr
    assert str(proj) not in r.stderr and str(proj.parent) not in r.stderr, r.stderr
    assert "exit" in r.stderr, r.stderr


# F11 -- a MALFORMED config is rc 2 naming the cell file, never a traceback.
def test_f11_a_config_that_does_not_parse_is_rc_two(proj):
    cfg = proj / ".agi" / "config.json"
    base = _git(proj, "rev-parse", "HEAD").strip()
    cfg.write_text("{not json")
    _commit(proj, "break the config")
    r = _run(proj, base)
    assert r.returncode == 2, r.stdout + r.stderr
    assert "config.json" in r.stderr and "Traceback" not in r.stderr, r.stderr


# F12 -- node_deletion fails CLOSED on a resolver that raises, and a mint a
# PRE-EXISTING other node carries is a deletion wearing it as a disguise.
def test_f12_a_raising_resolver_is_rc_two_naming_the_class(proj):
    g = proj / ".agi" / "nodes/idea"
    (g / "one.md").unlink()
    for nm in ("dup1", "dup2"):
        (g / f"{nm}.md").write_text(_node(f"idea:{nm}", "a" * 32, type="idea"))
    _commit(proj, "two live nodes take one mint")
    r = _run(proj, "HEAD~1")
    assert r.returncode == 2, r.stdout + r.stderr
    assert "node_deletion" in r.stderr and "Traceback" not in r.stderr, r.stderr


def test_f12b_a_mint_reused_by_a_pre_existing_node_is_a_deletion(proj):
    g = proj / ".agi" / "nodes"
    (g / "idea/one.md").unlink()
    (g / "build/two.md").write_text(
        _node("build:two", "a" * 32, type="build", payload_ref="notes/payload.md"))
    _commit(proj, "another node takes the deleted node's mint")
    r = _run(proj, "HEAD~1")
    assert r.returncode == 1, r.stdout + r.stderr
    assert "RED node_deletion 1: idea:one" in r.stdout, r.stdout


# F13 -- broken_link counts BOTH halves: a link broken on a DEPRECATED node at
# NEW only is a NEW break, not a retirement to be excluded.
def test_f13_a_link_broken_on_a_deprecated_node_at_new_is_counted(proj):
    g = proj / ".agi" / "nodes/deprecated/idea"
    g.mkdir(parents=True)
    (proj / "notes/old.md").write_text("old payload\n")
    (g / "ret.md").write_text(
        _node("idea:ret", "f" * 32, type="idea", status="deprecated",
              payload_ref="notes/old.md"))
    base = _commit(proj, "a retired node whose payload is still there")
    assert _run(proj, base).returncode == 0, _run(proj, base).stdout
    base = _git(proj, "rev-parse", "HEAD").strip()
    (proj / "notes/old.md").unlink()
    _commit(proj, "the retired node's payload is gone")
    r = _run(proj, base)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "RED broken_link 1: idea:ret->notes/old.md" in r.stdout, r.stdout
