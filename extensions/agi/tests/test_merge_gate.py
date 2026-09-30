"""hypothesis:g716107-...-merge-gate-gives-one-word -- `merge_gate.py check BASE TIP`
prints ONE word from the council report: merge, or hold by name.

One row per falsifier (F1-F6). Every value is SYNTHETIC and built by string
concatenation; every repo and config is a tmp fixture -- no test reads or writes
the live repo, its history or its report node.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
WHO = "t@example.com"
KEY = "sk-" + "SYNTHETIC" + "0123456789abcdef"      # shape only, never a real key
REVIEW = ["extensions/", "skills/", "src/"]


def _git(repo, *args):
    p = subprocess.run(["git", "-C", str(repo), *args], check=True,
                       capture_output=True, text=True, timeout=300)
    return p.stdout


def _commit(repo, msg, *paths):
    _git(repo, "add", "-A", *paths)
    _git(repo, "-c", f"user.email={WHO}", "-c", "user.name=t", "commit", "-qm", msg)
    return _git(repo, "rev-parse", "HEAD").strip()


def _row(old, new, state="REVIEWED"):
    return f"| pass/{state[:3]} | {old}..{new} | {state} | accept | 0 | unchecked |"


def _report(repo, *rows):
    g = repo / ".agi"
    (g / "nodes/doc").mkdir(parents=True, exist_ok=True)
    (g / "nodes/doc/council-report.md").write_text(
        "---\nid: doc:council-report\nmint_id: " + "d" * 32 + "\ntype: doc\n---\n\n"
        "| round | old..new | state | verdict | residues | reds |\n|---|---|---|---|---|---|\n"
        + "\n".join(rows) + "\n")


@pytest.fixture
def proj(tmp_path):
    """A tmp repo at `base` with the review-path cell and ONE covering report row."""
    repo = tmp_path / "proj"
    g = repo / ".agi"
    (g / "nodes/doc").mkdir(parents=True)
    (g / "nodes/doc/council-report.md").write_text(
        "---\nid: doc:council-report\nmint_id: " + "d" * 32 + "\ntype: doc\n---\n\nno rows yet\n")
    (g / "config.json").write_text(json.dumps(
        {"merge_gate": {"red_classes": ["secrets"], "review_paths": REVIEW}}))
    (repo / "extensions").mkdir()
    (repo / "extensions/keep.py").write_text("x = 1\n")
    _git(tmp_path, "init", "-q", str(repo))
    _git(repo, "add", "-A")
    base = _commit(repo, "base")
    _report(repo, _row(base, base))          # the round that reviewed `base` itself
    _commit(repo, "report row")
    return repo, base


def _run(repo, base="HEAD~1", tip="HEAD", *extra):
    return subprocess.run([sys.executable, str(BIN / "merge_gate.py"), "check", base, tip,
                           "--root", str(repo / ".agi"), "--repo", str(repo), *extra],
                          capture_output=True, text=True, timeout=900)


# F1 -- a commit touching a review path with NO covering row -> hold, named by sha.
def test_f1_uncovered_review_path_commit_holds_and_is_named(proj):
    repo, base = proj
    (repo / "extensions/new.py").write_text("y = 2\n")
    sha = _commit(repo, "engine delta")      # AFTER the only row's new rev: uncovered
    p = _run(repo, base, sha)
    assert p.returncode == 1
    assert p.stdout.splitlines()[0] == "hold"
    assert sha[:20] in p.stdout
    assert base not in p.stdout.splitlines()[0]


# F2 -- a planted RED (key-shaped, built by concatenation) -> hold naming the class.
def test_f2_planted_red_holds_and_names_the_class(proj):
    repo, base = proj
    (repo / "extensions/leak.py").write_text(f'TOKEN = "{KEY}"\n')
    sha = _commit(repo, "leak")
    p = _run(repo, base, sha)
    assert p.returncode == 1 and p.stdout.splitlines()[0] == "hold"
    assert "secrets" in p.stdout and KEY not in p.stdout


# F3 -- an unreviewed:budget row merges ONLY when --prime-count names its count.
def test_f3_budget_row_needs_the_prime_count(proj):
    repo, base = proj
    _report(repo, _row(base, "HEAD", "unreviewed:budget"))
    _commit(repo, "budget row")
    assert _run(repo, base, "HEAD").returncode == 1        # absent -> hold
    wrong = _run(repo, base, "HEAD", "--prime-count", "2")
    assert wrong.returncode == 1 and "2" in wrong.stdout    # wrong count -> hold
    assert _run(repo, base, "HEAD", "--prime-count", "1").returncode == 0


# F4 -- a NON-review commit with no row merges; a MERGE commit is never named.
def test_f4_non_review_commit_needs_no_row_and_a_merge_is_never_named(proj):
    repo, base = proj
    (repo / ".agi/nodes/doc/card.md").parent.mkdir(parents=True, exist_ok=True)
    (repo / ".agi/nodes/doc/card.md").write_text("---\nid: doc:card\n---\n\ncard\n")
    sha = _commit(repo, "a card, no round")
    p = _run(repo, base, sha)
    assert p.returncode == 0 and p.stdout.splitlines()[0] == "merge"
    _git(repo, "checkout", "-q", "-b", "side", base)
    (repo / "extensions/side.py").write_text("z = 3\n")
    side = _commit(repo, "side")
    _git(repo, "checkout", "-q", "master" if (repo / ".git/refs/heads/master").exists()
          else "main")
    merge = _git(repo, "merge", "--no-ff", "-qm", "merge side", "side").strip() or \
        _git(repo, "rev-parse", "HEAD").strip()
    p = _run(repo, base, merge)
    assert p.returncode == 1 and merge[:20] not in p.stdout   # the MERGE is silent...
    assert side[:20] in p.stdout                              # ...its commit IS named


# F5 -- a bad rev, an unreadable report and an absent cell -> rc 2, one line, no traceback.
def test_f5_cannot_answer_is_rc_two_on_one_line(proj):
    repo, base = proj
    for args in (["check", "no-such-rev", "HEAD"], ["check", base, "no-such-rev"]):
        p = subprocess.run([sys.executable, str(BIN / "merge_gate.py"), *args,
                            "--root", str(repo / ".agi"), "--repo", str(repo)],
                           capture_output=True, text=True, timeout=300)
        assert p.returncode == 2 and "Traceback" not in p.stderr
    cfg = repo / ".agi/config.json"
    cfg.write_text(json.dumps({"merge_gate": {"red_classes": ["secrets"]}}))
    p = _run(repo, base, "HEAD")
    assert p.returncode == 2 and "review_paths" in p.stderr and "Traceback" not in p.stderr
    assert str(repo) not in p.stderr
    cfg.write_text(json.dumps({"merge_gate": {"red_classes": ["secrets"],
                                               "review_paths": REVIEW}}))
    (repo / ".agi/nodes/doc/council-report.md").write_text("---\nid: doc:council-report\n---\n\nno rows\n")
    _commit(repo, "empty report")
    p = _run(repo, base, "HEAD")
    assert p.returncode == 2 and "Traceback" not in p.stderr


# F6 -- the skill's section 2 retires steps 2, 3, 4 and 6 BY NAME; 0, 1, 5, 7 stay.
def test_f6_skill_section_two_retires_the_prime_hand_steps():
    text = (BIN.parents[2] / "skills/agi-merge-pass/SKILL.md").read_text(encoding="utf-8")
    section = text.split("## 2 · PASS", 1)[1].split("## 3 ·", 1)[0]
    assert "retired by goal:g7.16.1.10.7" in section
    for line in section.splitlines():
        if re.match(r"\s*[2346] ", line):
            assert "retired by goal:g7.16.1.10.7" in line, line
    for step in ("0", "1", "5", "7"):
        assert any(re.match(rf"\s*{step}[a-z]? \S", ln) and "retired" not in ln
                   for ln in section.splitlines()), step
    assert "merge_gate.py check" in section
