"""Fixture proof for `season.py rollover --align` (hypothesis:l4-a-town-season-
rollover-is-one-gated-command... ALIGN half, kid SM.104 #1).

Builds a THROWAWAY bare origin + clone under tmp_path (never the live tree):
two towns at cells 1 and 2, a third town whose season-2 trunk ALREADY exists,
a ladder with current_season=2, and a config:posts row per council.

Asserts:
  (1) dry run performs NOTHING (origin refs and town node bytes identical) and
      prints the steps with shas;
  (2) --apply --delete-old on the cell-1 town: new-name sha == old tip, the
      archive ref is verified, the old head is gone, the cell is 2 with one
      season_history entry, the cell-2 town is untouched, origin heads +0, and
      the global season is unchanged;
  (3) a live worktree on the old name keeps its checkout (branch -m applied,
      worktree HEAD unchanged);
  (4) an injected archive mismatch STOPS before the delete, names step 2, and
      no cell changed;
  (5) without --delete-old the old head stays on origin, heads +1, and the
      cell is HELD (unchanged) — the claim's own falsifier inverted;
  (6) an unknown --town is refused by name; an existing new trunk with a
      DIFFERENT sha is refused by name at step 1; a re-run on an aligned town
      is a named SKIP;
  (7) a cut-only run followed by --delete-old RESUMES (never a dead end).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
SRC = Path(__file__).resolve().parents[1] / "src"
CLI = BIN / "season.py"
H = "a" * 32

#: local + origin trunk branches the fixture builds, each with its own commit
BRANCHES = ["maxx/season1/main", "sanc/season2/main",
            "third/season1/main", "third/season2/main"]

TOWNS = [("maxx", 1, "council-maxx", "vision:maxx-v"),
         ("sanc", 2, "council-sanc", "vision:sanc-v"),
         ("third", 1, "council-third", "vision:third-v")]


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)


def _run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(CLI), "--root", str(root), "rollover", *args],
                          capture_output=True, text=True)


def _write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def _fm(path: Path) -> dict:
    sys.path.insert(0, str(SRC))
    from graph_core.persistence import frontmatter  # noqa: E402
    return frontmatter.load_node_file(path).frontmatter


def _heads(repo: Path) -> dict:
    """{ref: sha} for origin's heads."""
    out = _git(repo, "ls-remote", "--heads", "origin").stdout
    return {ln.split()[1]: ln.split()[0] for ln in out.splitlines() if ln.strip()}


def _build(tmp_path: Path) -> Path:
    bare, r = tmp_path / "origin.git", tmp_path / "work"
    bare.mkdir()
    _git(bare, "init", "-q", "--bare")
    r.mkdir()
    _git(r, "init", "-q", "-b", "master")
    _git(r, "config", "user.email", "t@t")
    _git(r, "config", "user.name", "t")
    _write(r / "README", "hi\n")
    g = r / ".agi"
    _write(g / "config.json", "{}\n")
    _write(g / "nodes" / ".geometry" / "ladder.md",
           f"---\nid: ladder:ladder\nmint_id: {H}\ntype: ladder\ncurrent_season: 2\n---\n")
    _write(g / "nodes" / ".geometry" / "posts.md",
           "---\nid: config:posts\nmint_id: " + H + "\ntype: config\nposts:\n"
           + "".join(f'  - {{"name": "{c}", "role": "council"}}\n'
                     for _s, _m, c, _v in TOWNS) + "---\n")
    for slug, season, council, vision in TOWNS:
        _write(g / "nodes" / "vision" / f"{slug}-v.md",
               f"---\nid: {vision}\nmint_id: {H}\ntype: vision\nseason: 2\n---\n# {vision}\n")
        _write(g / "nodes" / "town" / f"{slug}.md",
               f"---\nid: town:{slug}\nmint_id: {H}\ntype: town\ncouncil: {council}\n"
               f"season: {season}\ntown: core\nvisions:\n  - {vision}\n---\n"
               f"<!-- BODY:BEGIN -->\n# town:{slug}\n")
    # a town-schema that carries the REAL written_by gate
    _write(g / "context" / "schemas" / "[town].md",
           "---\nname: town\nwritten_by: [prime_director, owner]\nfields:\n"
           "  season: {type: int}\n  season_history: {type: list}\n---\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "seed")
    _git(r, "remote", "add", "origin", str(bare))
    _git(r, "push", "-q", "-u", "origin", "master")
    for i, name in enumerate(BRANCHES):
        _git(r, "checkout", "-q", "-B", name, "master")
        _write(r / f"f{i}.txt", name + "\n")
        _git(r, "add", f"f{i}.txt")
        _git(r, "commit", "-qm", name)
        _git(r, "push", "-q", "origin", f"{name}:refs/heads/{name}")
    _git(r, "checkout", "-q", "master")
    return r


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    return _build(tmp_path)


def _graph(repo: Path) -> Path:
    return repo / ".agi"


# ---- (1) dry run performs NOTHING and prints the steps with shas ----------
def test_dry_run_performs_nothing_and_prints_steps(repo: Path):
    g = _graph(repo)
    node = g / "nodes" / "town" / "maxx.md"
    before_refs, before_bytes = _heads(repo), node.read_bytes()
    res = _run(g, "--align", "--town", "maxx")
    assert res.returncode == 0, res.stdout + res.stderr
    assert "1 CUT refs/heads/maxx/season2/main <-" in res.stdout
    assert "2 ARCHIVE refs/agi/archive/maxx/season1/main <-" in res.stdout
    assert "CELL HELD town:maxx stays 1" in res.stdout
    assert "dry-run: nothing changed" in res.stdout
    assert _heads(repo) == before_refs
    assert node.read_bytes() == before_bytes
    # every step's sha is printed (the CUT line carries the old tip's 12 chars)
    old = before_refs["refs/heads/maxx/season1/main"]
    assert old[:12] in res.stdout


# ---- (2) --apply --delete-old: one town aligned, the others untouched ----
def test_apply_delete_old_aligns_one_town(repo: Path):
    g = _graph(repo)
    before = _heads(repo)
    old_sha = before["refs/heads/maxx/season1/main"]
    res = _run(g, "--align", "--town", "maxx", "--apply", "--delete-old", "--actor", "owner")
    assert res.returncode == 0, res.stdout + res.stderr
    after = _heads(repo)
    assert after["refs/heads/maxx/season2/main"] == old_sha   # new name == old tip
    assert "refs/heads/maxx/season1/main" not in after        # old head deleted
    assert len(after) == len(before)                          # heads +0
    arch = _git(repo, "ls-remote", "origin",
                "refs/agi/archive/maxx/season1/main").stdout.split()
    assert arch and arch[0] == old_sha                        # archive verified
    fm = _fm(g / "nodes" / "town" / "maxx.md")
    assert fm["season"] == 2
    assert len(fm["season_history"]) == 1
    assert fm["season_history"][0]["global_season"] == 2
    assert _fm(g / "nodes" / "town" / "sanc.md")["season"] == 2  # untouched
    assert _fm(g / "nodes" / ".geometry" / "ladder.md")["current_season"] == 2
    assert "6 HEADS" in res.stdout


# ---- (3) a live worktree on the old name keeps its checkout --------------
def test_live_worktree_branch_renamed_head_unchanged(repo: Path):
    g = _graph(repo)
    wt = repo.parent / "wt"
    _git(repo, "worktree", "add", "-q", str(wt), "maxx/season1/main")
    head_before = _git(wt, "rev-parse", "HEAD").stdout.strip()
    res = _run(g, "--align", "--town", "maxx", "--apply", "--actor", "owner")
    assert res.returncode == 0, res.stdout + res.stderr
    assert "5 WORKTREE git branch -m maxx/season1/main maxx/season2/main" in res.stdout
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout.split()
    assert "maxx/season2/main" in branches and "maxx/season1/main" not in branches
    assert _git(wt, "rev-parse", "HEAD").stdout.strip() == head_before


# ---- (4) injected archive mismatch stops before the delete, no cell ------
def test_archive_mismatch_stops_before_delete_no_cell(repo: Path):
    g = _graph(repo)
    hook = repo.parent / "origin.git" / "hooks" / "pre-receive"
    hook.write_text("#!/bin/sh\nwhile read o n r; do case \"$r\" in\n"
                    "refs/agi/archive/*) echo 'archive refused'; exit 1;;\nesac; done\nexit 0\n")
    hook.chmod(0o755)
    old_sha = _heads(repo)["refs/heads/maxx/season1/main"]
    res = _run(g, "--align", "--town", "maxx", "--apply", "--delete-old", "--actor", "owner")
    assert res.returncode != 0
    assert "STOP at step 2: archive" in res.stderr
    assert _heads(repo).get("refs/heads/maxx/season1/main") == old_sha  # NOT deleted
    assert _fm(g / "nodes" / "town" / "maxx.md")["season"] == 1         # no cell change
    assert "season_history" not in _fm(g / "nodes" / "town" / "maxx.md")


# ---- (5) without --delete-old the old head stays, heads +1 ---------------
def test_without_delete_old_head_stays_heads_plus_one(repo: Path):
    g = _graph(repo)
    before = _heads(repo)
    old_sha = before["refs/heads/maxx/season1/main"]
    res = _run(g, "--align", "--town", "maxx", "--apply", "--actor", "owner")
    assert res.returncode == 0, res.stdout + res.stderr
    after = _heads(repo)
    assert after["refs/heads/maxx/season1/main"] == old_sha
    assert after["refs/heads/maxx/season2/main"] == old_sha
    assert len(after) == len(before) + 1
    assert "3 DELETE" not in res.stdout
    # A1: the old head is still on origin, so the cell is HELD, not bumped.
    assert _fm(g / "nodes" / "town" / "maxx.md")["season"] == 1
    assert "CELL HELD town:maxx stays 1" in res.stdout
    assert "season_history" not in _fm(g / "nodes" / "town" / "maxx.md")


# ---- (7) A2: a cut-only run is RESUMED, not a dead end -------------------
def test_cut_only_run_is_resumed_by_a_later_delete_old(repo: Path):
    g = _graph(repo)
    first = _run(g, "--align", "--town", "maxx", "--apply", "--actor", "owner")
    assert first.returncode == 0, first.stdout + first.stderr
    assert _fm(g / "nodes" / "town" / "maxx.md")["season"] == 1  # held
    # The old name now exists AND the new name is already at the old tip.
    res = _run(g, "--align", "--town", "maxx", "--apply", "--delete-old",
               "--actor", "owner")
    assert res.returncode == 0, res.stdout + res.stderr
    assert "RESUME" in res.stdout
    after = _heads(repo)
    assert "refs/heads/maxx/season1/main" not in after
    assert _fm(g / "nodes" / "town" / "maxx.md")["season"] == 2


# ---- (6) unknown town, existing new trunk, and the aligned SKIP ----------
def test_unknown_town_refused_by_name(repo: Path):
    res = _run(_graph(repo), "--align", "--town", "nope", "--apply", "--actor", "owner")
    assert res.returncode != 0
    assert "--town 'nope' is not a declared town" in res.stderr


def test_existing_new_trunk_refused_by_name(repo: Path):
    g = _graph(repo)
    res = _run(g, "--align", "--town", "third", "--apply", "--delete-old", "--actor", "owner")
    assert res.returncode != 0
    assert "STOP at step 1: cut" in res.stderr
    assert "refusing to overwrite" in res.stderr
    assert _fm(g / "nodes" / "town" / "third.md")["season"] == 1


def test_aligned_town_is_a_named_skip_on_rerun(repo: Path):
    g = _graph(repo)
    assert _run(g, "--align", "--town", "maxx", "--apply", "--delete-old",
                "--actor", "owner").returncode == 0
    res = _run(g, "--align", "--town", "maxx", "--apply", "--actor", "owner")
    assert res.returncode == 0
    assert "SKIP town:maxx — season 2 already == G" in res.stdout
