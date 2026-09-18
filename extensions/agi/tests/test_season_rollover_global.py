"""Fixture proof for `season.py rollover --global` (hypothesis:l4-a-town-season-
rollover-is-one-gated-command... ROLLOVER half, kid SM.104 #2).

A THROWAWAY bare origin under tmp_path (never the live tree): the global trunk
`season2/main` plus a `<t>/main` and a `<t>/season2/main` for two towns, all
built so every fold is a real (non-fast-forward) merge. master advanced past
the trunk bases on purpose.

Asserts:
  (1) --global dry performs NOTHING and prints the steps with shas;
  (2) --global --apply --delete-old: every trunk cut to season3, every fold a
      two-parent merge commit into master / <t>/main, archives verified, old
      heads gone, every cell 3, heads +0;
  (3) --global --apply without --delete-old: heads + trunks, NO cell bumped;
  (4) a fold that would fast-forward is REFUSED by name;
  (5) injected archive mismatch STOPS before the delete, names the step, no
      cell changed;
  (6) --global --town t refused by name; bare rollover --town refused by name;
      a cut-only run is RESUMED by a later --delete-old.
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

TOWNS = [("maxx", "council-maxx", "vision:maxx-v"),
         ("sanc", "council-sanc", "vision:sanc-v")]


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
    out = _git(repo, "ls-remote", "--heads", "origin").stdout
    return {ln.split()[1]: ln.split()[0] for ln in out.splitlines() if ln.strip()}


def _remote_sha(repo: Path, ref: str) -> str:
    line = _git(repo, "ls-remote", "origin", ref).stdout.strip()
    return line.split()[0] if line else ""


def _parents(repo: Path, ref: str) -> list:
    sha = _remote_sha(repo, ref)
    return _git(repo, "rev-list", "--parents", "-n1", sha).stdout.split()[1:]


def _commit(repo: Path, name: str) -> None:
    _write(repo / name, name + "\n")
    _git(repo, "add", name)
    _git(repo, "commit", "-qm", name)


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
           f"---\nid: ladder:ladder\nmint_id: {H}\ntype: ladder\n"
           "current_season: 2\ntiers: []\ncaps: {}\ncaps_apply_from_season: 2\n"
           "budget_usd_week: 0\nspawn_profiles: []\nread_order: {}\n"
           "director_rotate_at: 0.5\nzoom: numeric\nroles: []\n"
           "season_names: {}\nmantles: {}\n---\n")
    _write(g / "nodes" / ".geometry" / "posts.md",
           "---\nid: config:posts\nmint_id: " + H + "\ntype: config\nposts:\n"
           + "".join(f'  - {{"name": "{c}", "role": "council"}}\n'
                     for _s, c, _v in TOWNS) + "---\n")
    for slug, council, vision in TOWNS:
        _write(g / "nodes" / "vision" / f"{slug}-v.md",
               f"---\nid: {vision}\nmint_id: {H}\ntype: vision\nseason: 2\n---\n# {vision}\n")
        _write(g / "nodes" / "town" / f"{slug}.md",
               f"---\nid: town:{slug}\nmint_id: {H}\ntype: town\ncouncil: {council}\n"
               f"season: 2\ntown: core\nvisions:\n  - {vision}\n---\n"
               f"<!-- BODY:BEGIN -->\n# town:{slug}\n")
    _write(g / "context" / "schemas" / "[town].md",
           "---\nname: town\nwritten_by: [prime_director, owner]\nfields:\n"
           "  season: {type: int}\n  season_history: {type: list}\n---\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "seed")
    _git(r, "remote", "add", "origin", str(bare))
    _git(r, "push", "-q", "-u", "origin", "master")
    # the global trunk at M0, then the town trunks at M0
    for name in ["season2/main"] + [f"{s}/season2/main" for s, _c, _v in TOWNS]:
        _git(r, "checkout", "-q", "-B", name, "master")
        _commit(r, name.replace("/", "-"))
        _git(r, "push", "-q", "origin", f"{name}:refs/heads/{name}")
    # master advances past the trunk bases so every fold is a real merge
    _git(r, "checkout", "-q", "master")
    _commit(r, "m1")
    _git(r, "push", "-q", "origin", "master")
    # the town mains at M1
    for slug, _c, _v in TOWNS:
        _git(r, "checkout", "-q", "-B", f"{slug}/main", "master")
        _commit(r, slug + "-main")
        _git(r, "push", "-q", "origin", f"{slug}/main:refs/heads/{slug}/main")
    _git(r, "checkout", "-q", "master")
    return r


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    return _build(tmp_path)


def _graph(repo: Path) -> Path:
    return repo / ".agi"


# ---- (1) dry run performs NOTHING and prints the steps with shas ----------
def test_global_dry_performs_nothing(repo: Path):
    g = _graph(repo)
    before, nbytes = _heads(repo), (g / "nodes" / "town" / "maxx.md").read_bytes()
    res = _run(g, "--global")
    assert res.returncode == 0, res.stdout + res.stderr
    assert "CUT refs/heads/season3/main <-" in res.stdout
    assert "FOLD season2/main -> master" in res.stdout
    assert "ARCHIVE refs/agi/archive/season2/main <-" in res.stdout
    assert "CELL HELD ladder:ladder stays 2" in res.stdout
    assert "CUT refs/heads/maxx/season3/main <-" in res.stdout
    assert "6 HEADS" in res.stdout
    assert _heads(repo) == before
    assert (g / "nodes" / "town" / "maxx.md").read_bytes() == nbytes
    assert before["refs/heads/season2/main"][:12] in res.stdout


# ---- (2) --apply --delete-old: everything rolls, heads +0 -----------------
def test_global_apply_delete_old_rolls_everything(repo: Path):
    g = _graph(repo)
    before = _heads(repo)
    old = {"season2/main": before["refs/heads/season2/main"],
           "maxx/season2/main": before["refs/heads/maxx/season2/main"],
           "sanc/season2/main": before["refs/heads/sanc/season2/main"]}
    res = _run(g, "--global", "--apply", "--delete-old", "--actor", "owner")
    assert res.returncode == 0, res.stdout + res.stderr
    after = _heads(repo)
    for old_name, sha in old.items():
        new_name = old_name.replace("season2", "season3")
        assert after[f"refs/heads/{new_name}"] == sha          # new == old tip
        assert f"refs/heads/{old_name}" not in after           # old head gone
        assert _remote_sha(repo, f"refs/agi/archive/{old_name}") == sha
    assert len(after) == len(before)                       # heads +0
    for head in ("refs/heads/master", "refs/heads/maxx/main", "refs/heads/sanc/main"):
        assert len(_parents(repo, head)) == 2              # two-parent merge commit
    assert _fm(g / "nodes" / ".geometry" / "ladder.md")["current_season"] == 3
    for slug, _c, _v in TOWNS:
        fm = _fm(g / "nodes" / "town" / f"{slug}.md")
        assert fm["season"] == 3 and len(fm["season_history"]) == 1
        assert fm["season_history"][0]["global_season"] == 3


# ---- (3) without --delete-old: heads +trunks, no cell bumped -------------
def test_global_without_delete_old_holds_every_cell(repo: Path):
    g = _graph(repo)
    before = _heads(repo)
    res = _run(g, "--global", "--apply", "--actor", "owner")
    assert res.returncode == 0, res.stdout + res.stderr
    after = _heads(repo)
    assert len(after) == len(before) + 3
    assert "DELETE" not in res.stdout
    assert "CELL HELD" in res.stdout
    assert _fm(g / "nodes" / ".geometry" / "ladder.md")["current_season"] == 2
    for slug, _c, _v in TOWNS:
        assert _fm(g / "nodes" / "town" / f"{slug}.md")["season"] == 2


# ---- (4) a fold that would fast-forward is REFUSED by name ---------------
def test_fold_that_would_fast_forward_is_refused(repo: Path):
    g = _graph(repo)
    # master reset back to the trunk base: master is now an ANCESTOR of
    # season2/main, so the FIRST fold (the global trunk) can only fast-forward.
    base = _git(repo, "rev-parse", "season2/main^").stdout.strip()
    _git(repo, "push", "-q", "-f", "origin", f"{base}:refs/heads/master")
    before = _heads(repo)
    res = _run(g, "--global", "--actor", "owner")   # dry: nothing performed
    assert res.returncode != 0
    assert "would fast-forward, refused by name" in res.stderr
    assert "master" in res.stderr
    assert _heads(repo) == before                          # dry-stop, nothing done


# ---- (5) injected archive mismatch stops before the delete, no cell ------
def test_archive_mismatch_stops_before_delete_no_cell(repo: Path):
    g = _graph(repo)
    hook = repo.parent / "origin.git" / "hooks" / "pre-receive"
    hook.write_text("#!/bin/sh\nwhile read o n r; do case \"$r\" in\n"
                    "refs/agi/archive/*) echo 'archive refused'; exit 1;;\nesac; done\nexit 0\n")
    hook.chmod(0o755)
    before = _heads(repo)
    res = _run(g, "--global", "--apply", "--delete-old", "--actor", "owner")
    assert res.returncode != 0
    assert "STOP at step 3: archive" in res.stderr
    after = _heads(repo)
    assert after["refs/heads/season2/main"] == before["refs/heads/season2/main"]
    assert _fm(g / "nodes" / ".geometry" / "ladder.md")["current_season"] == 2
    for slug, _c, _v in TOWNS:
        assert _fm(g / "nodes" / "town" / f"{slug}.md")["season"] == 2


# ---- (6) town refusals, and the cut-only RESUME --------------------------
def test_global_with_town_refused_by_name(repo: Path):
    g = _graph(repo)
    res = _run(g, "--global", "--town", "maxx", "--apply", "--actor", "owner")
    assert res.returncode != 0
    assert "a town never rolls alone" in res.stderr


def test_bare_rollover_with_town_refused_by_name(repo: Path):
    res = _run(_graph(repo), "--town", "maxx", "--dry-run")
    assert res.returncode != 0
    assert "a town never rolls alone" in res.stderr


def test_cut_only_run_is_resumed_by_a_later_delete_old(repo: Path):
    g = _graph(repo)
    first = _run(g, "--global", "--apply", "--actor", "owner")
    assert first.returncode == 0, first.stdout + first.stderr
    assert _fm(g / "nodes" / ".geometry" / "ladder.md")["current_season"] == 2
    res = _run(g, "--global", "--apply", "--delete-old", "--actor", "owner")
    assert res.returncode == 0, res.stdout + res.stderr
    assert "RESUME" in res.stdout
    after = _heads(repo)
    assert "refs/heads/season2/main" not in after
    assert _fm(g / "nodes" / ".geometry" / "ladder.md")["current_season"] == 3
    for slug, _c, _v in TOWNS:
        assert _fm(g / "nodes" / "town" / f"{slug}.md")["season"] == 3


# ---- (7) a partial rollover bumps NO cell anywhere (SM.106 residue fix) ---
def test_partial_cut_refusal_bumps_no_cell(repo: Path):
    """SM.104 residue: with one town's CUT forced to refuse, the OLD bug wrote
    the ladder and town cells inside the per-trunk loop. The fix defers every
    cell write to a second pass, so a failure anywhere leaves every cell at G."""
    g = _graph(repo)
    # a conflicting sanc/season3/main at a DIFFERENT sha forces that CUT to refuse
    _git(repo, "checkout", "-q", "master")
    _commit(repo, "conflict")
    _git(repo, "push", "-q", "origin", "master:refs/heads/sanc/season3/main")
    res = _run(g, "--global", "--apply", "--delete-old", "--actor", "owner")
    assert res.returncode != 0
    assert "STOP at step 1: cut" in res.stderr
    # no cell anywhere changed: ladder and every town stay at G
    assert _fm(g / "nodes" / ".geometry" / "ladder.md")["current_season"] == 2
    for slug, _c, _v in TOWNS:
        assert _fm(g / "nodes" / "town" / f"{slug}.md")["season"] == 2


# ---- (7b) SM.106b: no-delete mode writes no cell, so no admission is owed --
def test_global_default_actor_without_delete_old_performs(repo: Path):
    """SM.106 residue (a00-4323cedc): the pre-flight was gated on `apply`
    ALONE. Cells are written ONLY with --delete-old; without it every cell is
    HELD, no write.py call happens, and no admission is needed. Gating the
    pre-flight on `apply and delete_old` restores the documented no-delete
    mode for the DEFAULT actor: rc 0, heads +3, cells stay at G."""
    g = _graph(repo)
    before = _heads(repo)
    res = _run(g, "--global", "--apply")          # no --delete-old, no --actor
    assert res.returncode == 0, res.stdout + res.stderr
    after = _heads(repo)
    assert len(after) == len(before) + 3
    assert "CELL HELD" in res.stdout
    assert _fm(g / "nodes" / ".geometry" / "ladder.md")["current_season"] == 2
    for slug, _c, _v in TOWNS:
        assert _fm(g / "nodes" / "town" / f"{slug}.md")["season"] == 2


# ---- (8) SM.106 auth defect: the DEFAULT actor refuses before any step ---
def test_global_default_actor_refuses_before_any_step(repo: Path):
    """SM.106 auth defect: the documented command with NO --actor defaults to
    `season.py`, which is not admitted for town cells (written_by
    [prime_director, owner]). The pre-fix code performed all five steps,
    pushed every origin ref, and only then had write.py refuse the FIRST town
    cell -- leaving ladder=G+1 and towns=G. PASS 0 must now refuse by name
    with NOTHING performed: every origin ref and every node byte unchanged,
    and the ladder and every town cell still agreeing at G."""
    g = _graph(repo)
    before = _heads(repo)
    paths = [g / "nodes" / ".geometry" / "ladder.md"] + [
        g / "nodes" / "town" / f"{slug}.md" for slug, _c, _v in TOWNS]
    nbytes = {p: p.read_bytes() for p in paths}
    res = _run(g, "--global", "--apply", "--delete-old")  # NO --actor
    assert res.returncode != 0
    assert "REFUSED" in res.stderr and "not admitted" in res.stderr
    assert "nothing performed" in res.stderr
    assert _heads(repo) == before                     # no origin push happened
    for p, b in nbytes.items():
        assert p.read_bytes() == b                    # no node byte changed
    # the ladder and every town cell AGREE at G
    assert _fm(g / "nodes" / ".geometry" / "ladder.md")["current_season"] == 2
    for slug, _c, _v in TOWNS:
        assert _fm(g / "nodes" / "town" / f"{slug}.md")["season"] == 2
