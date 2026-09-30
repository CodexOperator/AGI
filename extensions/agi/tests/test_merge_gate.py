"""hypothesis:g716107-...-merge-gate-gives-one-word -- `merge_gate.py check BASE TIP`
prints ONE word: merge, or hold by name. One row per falsifier F1-F6 and per corrective
DH.DG3.62 C1-C5. Values are SYNTHETIC; every repo and config is a tmp fixture -- no test
touches the live repo, its history or its report node."""
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
HEADER = "| round | old..new | state | verdict | residues | reds |\n|---|---|---|---|---|---|\n"
sys.path.insert(0, str(BIN))
import merge_gate  # noqa: E402  -- the gate in-process, for the git-verb row

def _git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True, timeout=300).stdout

def _commit(repo, msg, *paths):
    _git(repo, "add", "-A", *paths)
    _git(repo, "-c", f"user.email={WHO}", "-c", "user.name=t", "commit", "-qm", msg)
    return _git(repo, "rev-parse", "HEAD").strip()

def _row(old, new, state="REVIEWED", verdict="accept"):
    return f"| pass/{state[:3]} | {old}..{new} | {state} | {verdict} | 0 | unchecked |"

def _report(repo, *rows):
    g = repo / ".agi"
    (g / "nodes/doc").mkdir(parents=True, exist_ok=True)
    (g / "nodes/doc/council-report.md").write_text(
        "---\nid: doc:council-report\nmint_id: " + "d" * 32 + "\ntype: doc\n---\n\n"
        + HEADER + "\n".join(rows) + "\n")

def _cfg(repo, review=REVIEW):
    (repo / ".agi/config.json").write_text(json.dumps({"merge_gate": {"red_classes": ["secrets"], "review_paths": review}}))

@pytest.fixture
def proj(tmp_path):
    """A tmp repo at `base` with the review-path cell and ONE covering report row."""
    repo = tmp_path / "proj"
    (repo / ".agi").mkdir(parents=True)
    _cfg(repo)
    (repo / "extensions").mkdir()
    (repo / "extensions/keep.py").write_text("x = 1\n")
    _git(tmp_path, "init", "-q", str(repo))
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
    assert p.returncode == 1 and p.stdout.splitlines()[0] == "hold" and sha[:20] in p.stdout

# F2 -- a planted RED (key-shaped, built by concatenation) -> hold naming the class.
def test_f2_planted_red_holds_and_names_the_class(proj):
    repo, base = proj
    (repo / "extensions/leak.py").write_text(f'TOKEN = "{KEY}"\n')
    p = _run(repo, base, _commit(repo, "leak"))
    assert (p.returncode, p.stdout.splitlines()[0]) == (1, "hold")
    assert "secrets" in p.stdout and KEY not in p.stdout

# F3 -- an unreviewed:budget row merges ONLY when --prime-count names its count.
def test_f3_budget_row_needs_the_prime_count(proj):
    repo, base = proj
    _report(repo, _row(base, "HEAD", "unreviewed:budget"))
    _commit(repo, "budget row")
    absent, wrong = _run(repo, base, "HEAD"), _run(repo, base, "HEAD", "--prime-count", "2")
    assert [absent.returncode, wrong.returncode] == [1, 1]   # absent / wrong count -> hold
    assert "2" in wrong.stdout and _run(repo, base, "HEAD", "--prime-count", "1").returncode == 0

# F4 -- a NON-review commit with no row merges; a MERGE commit is never named.
def test_f4_non_review_commit_needs_no_row_and_a_merge_is_never_named(proj):
    repo, base = proj
    (repo / ".agi/nodes/doc/card.md").write_text("---\nid: doc:card\n---\n\ncard\n")
    assert _run(repo, base, _commit(repo, "a card, no round")).returncode == 0
    _git(repo, "checkout", "-q", "-b", "side", base)
    (repo / "extensions/side.py").write_text("z = 3\n")
    side = _commit(repo, "side")
    _git(repo, "checkout", "-q", "master" if (repo / ".git/refs/heads/master").exists() else "main")
    merge = _git(repo, "merge", "--no-ff", "-qm", "merge side", "side").strip() or _git(repo, "rev-parse", "HEAD").strip()
    p = _run(repo, base, merge)
    assert p.returncode == 1 and merge[:20] not in p.stdout   # the MERGE is silent...
    assert side[:20] in p.stdout                              # ...its commit IS named

# F5 -- a bad rev, an unreadable report and an absent cell -> rc 2, one line, no traceback.
def test_f5_cannot_answer_is_rc_two_on_one_line(proj):
    repo, base = proj
    for revs in (("no-such-rev", "HEAD"), (base, "no-such-rev")):
        p = _run(repo, *revs)
        assert p.returncode == 2 and "Traceback" not in p.stderr
    (repo / ".agi/config.json").write_text(json.dumps({"merge_gate": {"red_classes": ["secrets"]}}))
    p = _run(repo, base, "HEAD")
    assert p.returncode == 2 and "review_paths" in p.stderr and str(repo) not in p.stderr
    _cfg(repo)
    (repo / ".agi/nodes/doc/council-report.md").write_text("---\nid: doc:council-report\n---\n\nno rows\n")
    p = _run(repo, base, _commit(repo, "empty report"))
    assert p.returncode == 2 and "Traceback" not in p.stderr

# F6 + fix 8 -- section 2 retires steps 2, 3, 4, 6 BY NAME, continuation line included.
def test_f6_skill_section_two_retires_the_prime_hand_steps():
    text = (BIN.parents[2] / "skills/agi-merge-pass/SKILL.md").read_text(encoding="utf-8")
    section = text.split("## 2 · PASS", 1)[1].split("## 3 ·", 1)[0]
    assert "retired by goal:g7.16.1.10.7" in section
    assert all("retired by goal:g7.16.1.10.7" in ln for ln in section.splitlines()
               if re.match(r"\s*[2346] ", ln)), section
    for step in ("0", "1", "5", "7"):
        assert any(re.match(rf"\s*{step}[a-z]? \S", ln) and "retired" not in ln for ln in section.splitlines()), step
    assert "merge_gate.py check" in section
    assert any("retired" in ln for ln in section.splitlines()    # fix 8: no live tail
               if ".agi/nodes/.geometry paths" in ln)

# C1 -- a row whose tip MERGED the trunk covers only its own first-parent chain.
def test_c1_trunk_commit_merged_into_the_row_stays_uncovered(proj):
    repo, base = proj
    (repo / "extensions/trunk.py").write_text("t = 1\n")
    trunk = _commit(repo, "trunk delta")          # a review-path commit on the trunk
    _git(repo, "checkout", "-q", "-b", "loop", base)
    (repo / ".agi/nodes/doc").mkdir(parents=True, exist_ok=True)
    (repo / ".agi/nodes/doc/card.md").write_text("---\nid: doc:card\n---\n\nloop\n")
    _commit(repo, "loop card")
    _git(repo, "merge", "--no-ff", "-qm", "merge trunk", trunk)
    _report(repo, _row(base, "HEAD"))             # the row accepts the MERGED range
    p = _run(repo, base, "HEAD")
    assert p.returncode == 1 and trunk[:20] in p.stdout

# C2 -- a row covers ONLY when its verdict starts with `accept`.
def test_c2_verdict_column_decides_coverage(proj):
    repo, base = proj
    (repo / "extensions/new.py").write_text("y = 2\n")
    sha = _commit(repo, "engine delta")
    _report(repo, _row(base, "HEAD"), _row(base, sha, "REJECTED", "reject"))
    p = _run(repo, base, sha)
    assert p.returncode == 1 and "pass/REJ" in p.stdout and "reject" in p.stdout
    _report(repo, _row(base, "HEAD"), _row(base, sha, "REVIEWED", "accept_with_residue"))
    assert _run(repo, base, sha).returncode == 0

# C3 -- a FILE-shaped review_paths entry matches the file itself, not nothing.
def test_c3_file_shaped_review_path_entry_is_not_fail_open(proj):
    repo, base = proj
    _cfg(repo, [".agi/config.json"])               # a FILE-shaped entry, not a dir
    sha = _commit(repo, "cell edit", ".agi/config.json")
    p = _run(repo, base, sha)
    assert p.returncode == 1 and sha[:20] in p.stdout

# C4 -- the uncovered list caps at 20 shas and counts the rest on ONE line.
def test_c4_uncovered_list_is_capped_and_counted(proj):
    repo, base = proj
    for i in range(25):
        (repo / f"extensions/f{i}.py").write_text(f"v = {i}\n")
        _commit(repo, f"delta {i}")
    p = _run(repo, base, "HEAD")
    assert p.returncode == 1
    assert sum("uncovered review-path commit" in ln for ln in p.stdout.splitlines()) == 20
    assert "... 5 more (total 25)" in p.stdout

# C5 -- ONE `git log` walk over the range; never one `git show` per commit.
def test_c5_one_walk_and_no_git_show(proj, monkeypatch):
    repo, base = proj
    for i in range(3):
        (repo / f"extensions/g{i}.py").write_text(f"w = {i}\n")
        _commit(repo, f"delta {i}")
    seen, real = [], subprocess.run

    def spy(cmd, *a, **kw):
        if cmd and cmd[0] == "git" and len(cmd) > 3:
            seen.append(cmd[3])
        return real(cmd, *a, **kw)

    monkeypatch.setattr(subprocess, "run", spy)
    assert merge_gate.main(["check", base, "HEAD", "--root", str(repo / ".agi"),
                            "--repo", str(repo)]) == 1
    assert "show" not in seen and seen.count("log") == 1