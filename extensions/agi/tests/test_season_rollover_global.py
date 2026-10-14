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
from tests.veto_cell import write_free_veto  # noqa: E402

BIN = Path(__file__).resolve().parents[1] / "bin"
SRC = Path(__file__).resolve().parents[1] / "src"
CLI = BIN / "season.py"
H = "a" * 32

TOWNS = [("maxx", "council-maxx", "vision:maxx-v"),
         ("sanc", "council-sanc", "vision:sanc-v")]


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)


def _run(root: Path, *args: str, cli: Path = CLI, core_old: bool = True) -> subprocess.CompletedProcess:
    # --global always carries a comparison tip (the judge check refuses without one):
    # the seed commit, whose judge-path blobs every fixture commit shares
    if "--global" in args and "--judge-tip" not in args:
        seed = _git(root.parent, "rev-list", "--max-parents=0", "HEAD").stdout.split()[0]
        args = (*args, "--judge-tip", seed)
    # the core town's OLD tip is GIVEN (goal:g8.2: season.py names no app town): the live trunk, as the runner passes it
    if "--global" in args and core_old and "--core-old" not in args:
        args = (*args, "--core-old", "local-maxxing/season2/main")
    return subprocess.run([sys.executable, str(cli), "--root", str(root), "rollover", *args],
                          capture_output=True, text=True)


def _on_new_trunk(repo: Path) -> None:
    """Run where the cell commits belong: a scratch checkout on the new season trunk."""
    _git(repo, "checkout", "-q", "-B", "season3/main", "master")


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


def _build(tmp_path: Path, towns=TOWNS) -> Path:
    bare, r = tmp_path / "origin.git", tmp_path / "work"
    tmp_path.mkdir(parents=True, exist_ok=True)
    bare.mkdir()
    _git(bare, "init", "-q", "--bare")
    r.mkdir()
    _git(r, "init", "-q", "-b", "master")
    _git(r, "config", "user.email", "t@t")
    _git(r, "config", "user.name", "t")
    _write(r / "README", "hi\n")
    g = r / ".agi"
    _write(g / "config.json", "{}\n")
    write_free_veto(g / "nodes" / ".geometry")
    _write(g / "nodes" / ".geometry" / "ladder.md",
           f"---\nid: ladder:ladder\nmint_id: {H}\ntype: ladder\n"
           "current_season: 2\ntiers: []\ncaps: {}\ncaps_apply_from_season: 2\n"
           "budget_usd_week: 0\nspawn_profiles: []\nread_order: {}\n"
           "director_rotate_at: 0.5\nzoom: numeric\nroles: []\n"
           "season_names: {}\nmantles: {}\n---\n")
    _write(g / "nodes" / ".geometry" / "posts.md",
           "---\nid: config:posts\nmint_id: " + H + "\ntype: config\nposts:\n"
           + "".join(f'  - {{"name": "{c}", "role": "council"}}\n'
                     for _s, c, _v in towns) + "---\n")
    for slug, council, vision in towns:
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
    for name in ["season2/main"] + [f"{s}/season2/main" for s, _c, _v in towns]:
        _git(r, "checkout", "-q", "-B", name, "master")
        _commit(r, name.replace("/", "-"))
        _git(r, "push", "-q", "origin", f"{name}:refs/heads/{name}")
    # master advances past the trunk bases so every fold is a real merge
    _git(r, "checkout", "-q", "master")
    _commit(r, "m1")
    _git(r, "push", "-q", "origin", "master")
    # the town mains at M1
    for slug, _c, _v in towns:
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
    _on_new_trunk(repo)
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


# ---- (4) R1: a head that is an ANCESTOR of the old trunk is still folded by a 2-parent commit ----
def test_fold_onto_an_ancestor_head_is_a_two_parent_commit_never_a_plain_ff(repo: Path, tmp_path: Path):
    g = _graph(repo)
    # master reset back to the trunk base: master is now an ANCESTOR of season2/main
    base = _git(repo, "rev-parse", "season2/main^").stdout.strip()
    _git(repo, "push", "-q", "-f", "origin", f"{base}:refs/heads/master")
    trunk = _remote_sha(repo, "refs/heads/season2/main")
    dry = _run(g, "--global")
    assert dry.returncode == 0, dry.stdout + dry.stderr
    assert "FOLD season2/main -> master (merge --no-ff, head is an ancestor: 2 parents" in dry.stdout
    assert _remote_sha(repo, "refs/heads/master") == base       # the dry path writes nothing
    res = _run(g, "--global", "--apply")                          # cut + fold, no cell
    assert res.returncode == 0, res.stdout + res.stderr
    par = _parents(repo, "refs/heads/master")
    assert len(par) == 2 and par[0] == base and par[1] == trunk   # head = parent 1
    new = _remote_sha(repo, "refs/heads/master")
    assert _git(repo, "rev-parse", f"{new}^{{tree}}").stdout == _git(repo, "rev-parse", f"{trunk}^{{tree}}").stdout


def test_fold_onto_an_ancestor_head_a_plain_ff_mutant_is_red(repo: Path, tmp_path: Path):
    g = _graph(repo)
    base = _git(repo, "rev-parse", "season2/main^").stdout.strip()
    _git(repo, "push", "-q", "-f", "origin", f"{base}:refs/heads/master")
    mut = _mutant(tmp_path, (', "merge", "--no-ff", "-q", "-m",', ', "merge", "--ff-only", "-q", "-m",'))
    res = _run(g, "--global", "--apply", cli=mut)
    assert res.returncode != 0 and "STOP at step 2: fold" in res.stderr, "MUTANT (a plain ff) must be RED on the 2-parent proof"


# ---- (5) injected archive mismatch stops before the delete, no cell ------
def test_archive_mismatch_stops_before_delete_no_cell(repo: Path):
    g = _graph(repo)
    hook = repo.parent / "origin.git" / "hooks" / "pre-receive"
    hook.write_text("#!/bin/sh\nwhile read o n r; do case \"$r\" in\n"
                    "refs/agi/archive/*) echo 'archive refused'; exit 1;;\nesac; done\nexit 0\n")
    hook.chmod(0o755)
    _git(hook.parent.parent, "config", "core.hooksPath", str(hook.parent))   # a global core.hooksPath would shadow it
    before = _heads(repo)
    _on_new_trunk(repo)
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
    _on_new_trunk(repo)
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
    _on_new_trunk(repo)
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
    _on_new_trunk(repo)
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


# ===========================================================================
# goal:g7.16.1.11.8.1 -- the rollover runner's gates (council 3/3 06:54Z + 18:05Z 10-14)
#   (a) the JUDGE CHECK in code   (b) _cut RESUMEs a new that CONTAINS the old
#   (c) cell commits only in the new season trunk's scratch worktree
#   (d) the core town's OLD tip is the live trunk, never derive_names'
# Every row has a MUTANT: a copy of season.py with ONE line changed, run on the
# same fixture; the row's own assertion must then FAIL (RED).
# ===========================================================================
import importlib.util  # noqa: E402
import shutil  # noqa: E402

JUDGE = ".agi/nodes/.geometry/engine-post.md"
LADDER = ".agi/nodes/.geometry/ladder.md"


def _mutant(tmp_path: Path, *pairs) -> Path:
    """A copy of bin/ with each (old, new) applied ONCE to season.py; returns its season.py."""
    root = tmp_path / "mut" / "extensions" / "agi"
    if not root.exists():
        root.mkdir(parents=True)
        shutil.copytree(BIN, root / "bin")
        (root / "src").symlink_to(SRC)
    f = root / "bin" / "season.py"
    text = f.read_text()
    for old, new in pairs:
        assert text.count(old) == 1, f"mutant anchor not unique ({text.count(old)}): {old!r}"
        text = text.replace(old, new)
    f.write_text(text)
    return f


def _sh(repo: Path, branch: str, base: str, path: str, text: str) -> str:
    """Commit `text` at `path` on a branch cut from `base`; push it; return the sha."""
    _git(repo, "checkout", "-q", "-B", branch, base)
    _write(repo / path, text)
    _git(repo, "add", path)
    _git(repo, "commit", "-qm", f"{branch}: {path}")
    _git(repo, "push", "-q", "-f", "origin", f"{branch}:refs/heads/{branch}")
    sha = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _git(repo, "checkout", "-q", "master")
    return sha


def _judged(repo: Path, text: str = "v2\n") -> str:
    """Every trunk carries the same judge file: the PASS tip's. Returns the global trunk tip."""
    tip = ""
    for name in ["season2/main"] + [f"{s}/season2/main" for s, _c, _v in TOWNS]:
        sha = _sh(repo, name, name, JUDGE, text)
        tip = tip or sha
    return tip


# ---- (a) judge check ------------------------------------------------------
def test_a1_a_fold_carrying_the_comparison_tips_judge_passes_and_the_first_parent_mutant_is_red(repo: Path, tmp_path: Path):
    g, tip = _graph(repo), _judged(repo)
    ok = _run(g, "--global", "--judge-tip", tip)
    assert ok.returncode == 0, ok.stdout + ok.stderr          # the fold stages the judge file vs master, == the PASS tip
    assert f"comparison tip {tip[:12]}" in ok.stdout
    mut = _mutant(tmp_path, ("jd = _blob_diff(_judge_blobs(repo, tree), jb)",
                              "jd = _blob_diff(_judge_blobs(repo, tree), _judge_blobs(repo, htip))"))
    res = _run(g, "--global", "--judge-tip", tip, cli=mut)
    assert res.returncode != 0, "MUTANT (compare to the first parent) must be RED: the clean row wants rc 0 on the FOLD"


def test_a2_a_fold_that_differs_from_the_comparison_tip_is_refused_named_nothing_done(repo: Path):
    g, _tip = _graph(repo), _judged(repo)
    other = _sh(repo, "tip-v3", "master", JUDGE, "v3\n")          # a comparison tip whose judge file is v3
    before = _heads(repo)
    res = _run(g, "--global", "--apply", "--judge-tip", other)
    assert res.returncode == 1
    assert f"[rollover] stages the judge: {JUDGE}" in res.stderr
    assert "nothing performed" in res.stderr
    assert _heads(repo) == before


def test_a3_a_fold_whose_ladder_is_not_the_comparison_tips_is_refused_and_one_that_is_passes(repo: Path, tmp_path: Path):
    g = _graph(repo)
    ladder = (g / "nodes" / ".geometry" / "ladder.md").read_text()
    seed = _git(repo, "rev-list", "--max-parents=0", "HEAD").stdout.split()[0]
    tip = ""
    for name in ["season2/main"] + [f"{s}/season2/main" for s, _c, _v in TOWNS]:        # every trunk: the PASS tip's ladder
        sha = _sh(repo, name, name, LADDER, ladder + "\nseason 2 closes here\n")
        tip = tip or sha
    # the folds take a ladder the SEED comparison tip does not carry -> refused, named, nothing done
    res = _run(g, "--global", "--apply", "--judge-tip", seed)
    assert res.returncode == 1 and f"[rollover] stages the judge: {LADDER}" in res.stderr and "nothing performed" in res.stderr
    mut = _mutant(tmp_path, ("        if a != b:\n            notes.append(f\"[rollover] fold {old} -> {head} carries a {LADDER_PATH}", "        if False:\n            notes.append(f\"[rollover] fold {old} -> {head} carries a {LADDER_PATH}"))
    assert _run(g, "--global", "--judge-tip", seed, cli=mut).returncode == 0, "MUTANT (ladder check dropped) must be RED: it passes the foreign ladder"
    # a DRY run still rehearses every town, then ends rc 1 (the real run would refuse); the rc-0 mutant is RED
    dry = _run(g, "--global", "--judge-tip", seed)
    assert dry.returncode == 1 and "WOULD REFUSE the real run" in dry.stdout and "CUT refs/heads/maxx/season3/main" in dry.stdout
    mut2 = _mutant(tmp_path, ("    return 1 if refused else 0\n", "    return 0\n"))
    assert _run(g, "--global", "--judge-tip", seed, cli=mut2).returncode == 0, "MUTANT (dry run ends rc 0) must be RED"
    # the comparison tip IS the PASS tip: the same ladder differs from the first parent (master) and still passes
    assert _run(g, "--global", "--judge-tip", tip).returncode == 0


def test_a4_no_comparison_tip_is_refused_by_name(repo: Path):
    res = subprocess.run([sys.executable, str(CLI), "--root", str(_graph(repo)), "rollover", "--global"],
                         capture_output=True, text=True)
    assert res.returncode == 1 and "--judge-tip <rev> is required" in res.stderr


def _season_module(*pairs):
    src = CLI.read_text()
    for old, new in pairs:
        assert src.count(old) == 1, old
        src = src.replace(old, new)
    spec = importlib.util.spec_from_file_location("season_under_test", CLI)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(BIN)); sys.path.insert(0, str(SRC))
    sys.modules["season_under_test"] = mod            # the dataclasses in season.py look their module up
    exec(compile(src, str(CLI), "exec"), mod.__dict__)
    return mod


def test_a5_a_cell_commit_staging_the_judge_or_the_ladder_beside_a_node_is_refused(tmp_path: Path):
    r = tmp_path / "c"; r.mkdir()
    _git(r, "init", "-q", "-b", "x"); _git(r, "config", "user.email", "t@t"); _git(r, "config", "user.name", "t")
    for rel in (JUDGE, LADDER, ".agi/nodes/town/a.md"):
        _write(r / rel, "0\n")
    _git(r, "add", "-A"); _git(r, "commit", "-qm", "seed")
    tip = _git(r, "rev-parse", "HEAD").stdout.strip()

    def commit_with(*rels):
        h0 = _git(r, "rev-parse", "HEAD").stdout.strip()
        for rel in rels:
            _write(r / rel, _git(r, "rev-list", "--count", "HEAD").stdout)
        _git(r, "add", "-A"); _git(r, "commit", "-qm", "cell")
        return h0

    def verdict(mod, cell, h0):
        return mod._check_cell_commit(r, h0, cell, mod._judge_blobs(r, tip))

    clean, bad = _season_module(), _season_module(("    if LADDER_PATH in names and names != [LADDER_PATH]:", "    if False:"))
    h0 = commit_with(LADDER)                                   # the bump: ladder.md ALONE
    assert verdict(clean, "ladder:ladder", h0) == ""
    h0 = commit_with(LADDER, ".agi/nodes/town/a.md")          # ladder.md + a node
    assert "ladder.md moves alone" in verdict(clean, "town:a", h0)
    assert verdict(bad, "town:a", h0) == "", "MUTANT (beside-check dropped) must be RED"
    h0 = commit_with(".agi/nodes/town/a.md")                  # a town cell on the ladder row
    assert "not ladder.md alone" in verdict(clean, "ladder:ladder", h0)
    h0 = commit_with(JUDGE)                                    # a judge path
    assert "[rollover] stages the judge: " + JUDGE in verdict(clean, "town:a", h0)


# ---- (b) _cut RESUME on an ancestor ---------------------------------------
def test_b1_old_equals_new_resumes_and_a_new_containing_old_resumes_with_the_extras_listed(repo: Path, tmp_path: Path):
    g = _graph(repo)
    first = _run(g, "--global", "--apply", "--actor", "owner")             # cut-only: new == old
    assert first.returncode == 0
    again = _run(g, "--global", "--apply", "--actor", "owner")
    assert again.returncode == 0 and "RESUME: new name already at old tip" in again.stdout
    old = _remote_sha(repo, "refs/heads/season2/main")
    extra = _sh(repo, "season3/main", old, "extra.txt", "x\n")  # new = old + 1 extra commit
    before = _heads(repo)
    res = _run(g, "--global", "--judge-tip", "master")
    assert res.returncode == 0, res.stdout + res.stderr
    assert "CONTAINS the old tip" in res.stdout and "1 extra commit(s), 0 judge-path diff" in res.stdout
    assert extra[:7] in res.stdout and "season3/main: extra.txt" in res.stdout   # old..new subjects listed
    assert _heads(repo) == before and _remote_sha(repo, "refs/heads/season2/main") == old


def test_b2_a_new_that_contains_old_but_changes_a_judge_path_is_refused(repo: Path):
    g = _graph(repo)
    assert _run(g, "--global", "--apply", "--actor", "owner").returncode == 0
    _sh(repo, "season3/main", _remote_sha(repo, "refs/heads/season3/main"), JUDGE, "tampered\n")
    res = _run(g, "--global", "--judge-tip", "master")
    assert res.returncode == 1 and f"[rollover] stages the judge: {JUDGE}" in res.stderr
    assert "STOP at step 1: cut" in res.stderr


def test_b3_a_diverged_new_is_refused_by_name_and_the_no_ancestry_mutant_is_red(repo: Path, tmp_path: Path):
    g = _graph(repo)
    _sh(repo, "season3/main", "master", "elsewhere.txt", "e\n")           # not a descendant of season2/main
    res = _run(g, "--global", "--judge-tip", "master")
    assert res.returncode == 1 and "DIVERGED" in res.stderr and "STOP at step 1: cut" in res.stderr
    mut = _mutant(tmp_path, ("        if _is_anc(repo, sha, nsha):\n            jd =", "        if True:\n            jd ="))
    again = _run(g, "--global", "--judge-tip", "master", cli=mut)
    assert again.returncode == 0 and "CONTAINS the old tip" in again.stdout, "MUTANT (no ancestry test) must be RED: it RESUMEs a diverged line"


# ---- (c) cell commits only in the new trunk's scratch worktree -------------
def test_c1_a_run_that_writes_cells_on_any_other_branch_is_refused_by_name(repo: Path, tmp_path: Path):
    g = _graph(repo)                                  # checked out on master
    before, ladder = _heads(repo), (g / "nodes" / ".geometry" / "ladder.md").read_bytes()
    res = _run(g, "--global", "--apply", "--delete-old", "--actor", "owner")
    assert res.returncode == 1
    assert "[rollover] cell commits land on the branch checked out" in res.stderr and "on season3/main" in res.stderr
    assert _heads(repo) == before and (g / "nodes" / ".geometry" / "ladder.md").read_bytes() == ladder
    mut = _mutant(tmp_path, ("    if delete_old and cur_branch != want_branch:", "    if False:"))
    assert _run(g, "--global", "--apply", "--delete-old", "--actor", "owner", cli=mut).returncode == 0, \
        "MUTANT (branch check dropped) must be RED: it writes the cells on master"


def test_c2_the_dry_run_names_the_branch_each_cell_commit_lands_on(repo: Path):
    res = _run(_graph(repo), "--global")
    assert res.returncode == 0
    assert "cell commits land on branch master (expected season3/main; this run writes no cell" in res.stdout


# ---- (d) the core town's old tip ------------------------------------------
def _core(tmp_path: Path):
    towns = [("core", "council-core", "vision:core-v")]
    r = _build(tmp_path, towns)
    live = _sh(r, "local-maxxing/season2/main", "season2/main", "live.txt", "l\n")
    # core/season3/main is an ANCESTOR of the live trunk (the live lineage); core/season2/main (the 10-04 line) DIVERGED
    _git(r, "push", "-q", "-f", "origin", f"{_remote_sha(r, 'refs/heads/season2/main')}:refs/heads/core/season3/main")
    return r, live


def test_d1_the_core_old_tip_is_the_live_trunk_a_dead_line_is_refused_and_derive_names_is_red(tmp_path: Path):
    r, live = _core(tmp_path)
    g = _graph(r)
    ok = _run(g, "--global")
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert "core town: OLD TIP = the live trunk origin/local-maxxing/season2/main" in ok.stdout
    assert "BEHIND the live trunk" in ok.stdout and "FAST-FORWARD" in ok.stdout
    dead = _run(g, "--global", "--core-old", "core/season2/main")
    assert dead.returncode == 1 and "DIVERGED" in dead.stderr and "STOP at step 1: cut" in dead.stderr
    mut = _mutant(r.parent, ('old = core_old if slug == CORE_TOWN else branches.derive_names(slug, g)["town_season_main"]',
                             'old = branches.derive_names(slug, g)["town_season_main"]'))
    red = _run(g, "--global", cli=mut)
    assert red.returncode == 1, "MUTANT (old taken from derive_names) must be RED: " + red.stdout


def test_g82_core_old_is_given_never_defaulted_to_a_town_name_and_the_defaulting_mutant_is_red(tmp_path: Path):
    r, live = _core(tmp_path)
    g = _graph(r)
    before = _heads(r)
    red = _run(g, "--global", "--apply", core_old=False)
    assert red.returncode == 1 and "--core-old <origin branch> is required" in red.stderr, red.stdout + red.stderr
    assert _heads(r) == before                                            # nothing pushed
    assert _run(g, "--global").returncode == 0                            # given: the same fixture runs
    src = (BIN / "season.py").read_text()
    assert "local-maxxing" not in src                                      # no literal app-town name in the script
    mut = _mutant(r.parent, ('core_old = (getattr(args, "core_old", "") or "").strip()\n',
                             'core_old = (getattr(args, "core_old", "") or "").strip() or "local-maxxing/season2/main"\n'))
    ok = _run(g, "--global", cli=mut, core_old=False)
    assert ok.returncode == 0, "MUTANT (a literal default) must NOT refuse, so the clean row's refusal is what pins it: " + ok.stderr


# ---- R2/R3 (council 18:40Z): the core fold STOPs unless named; the BEHIND cut fast-forwards in the run ----
def _core_conflict(tmp_path: Path):
    r, live = _core(tmp_path)
    live = _sh(r, "local-maxxing/season2/main", live, "conflict.txt", "b\n")
    _sh(r, "core/main", "core/main", "conflict.txt", "a\n")        # core/main and the live trunk disagree on one file
    return r, live


def test_r2_an_unnamed_conflicting_fold_stops_a_named_one_is_skipped_and_the_proceeding_mutant_is_red(tmp_path: Path):
    r, live = _core_conflict(tmp_path)
    g = _graph(r)
    before, core_main = _heads(r), _remote_sha(r, "refs/heads/core/main")
    dry = _run(g, "--global")
    assert dry.returncode == 1 and "[rollover] fold local-maxxing/season2/main -> core/main does not merge cleanly: conflict.txt" in dry.stderr
    assert "--skip-fold core" in dry.stderr
    refused = _run(g, "--global", "--apply")
    assert refused.returncode == 1 and "nothing performed" in refused.stderr
    assert _heads(r) == before                                            # nothing pushed
    unknown = _run(g, "--global", "--skip-fold", "nope")
    assert unknown.returncode == 1 and "--skip-fold names nope: not a declared town" in unknown.stderr
    ok = _run(g, "--global", "--apply", "--skip-fold", "core")
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert "SKIPPED (--skip-fold core, owner-given): conflict.txt; nothing pushed for core/main" in ok.stdout
    assert _remote_sha(r, "refs/heads/core/main") == core_main            # core/main untouched
    mut = _mutant(tmp_path, ('notes.append(f"[rollover] fold {old} -> {head} does not merge cleanly: {why} (name it with --skip-fold {slug} to skip it, owner-given)")', 'pass'))
    r2, _ = _core_conflict(tmp_path / "m")
    b2 = _heads(r2)
    res = _run(_graph(r2), "--global", "--apply", cli=mut)
    assert not (res.returncode == 1 and _heads(r2) == b2), "MUTANT (an unnamed conflicting fold proceeds) must be RED: the row wants nothing pushed"


def test_r3_the_behind_core_cut_fast_forwards_in_the_run_and_the_resume_without_it_is_red(tmp_path: Path):
    r, live = _core(tmp_path)
    g = _graph(r)
    assert not _git(r, "merge-base", "--is-ancestor", live, _remote_sha(r, "refs/heads/core/season3/main")).returncode == 0
    dry = _run(g, "--global")
    assert dry.returncode == 0 and "FAST-FORWARD: origin/core/season3/main" in dry.stdout
    assert _git(r, "merge-base", "--is-ancestor", live, _remote_sha(r, "refs/heads/core/season3/main")).returncode != 0   # dry: untouched
    ok = _run(g, "--global", "--apply")
    assert ok.returncode == 0, ok.stdout + ok.stderr
    new = _remote_sha(r, "refs/heads/core/season3/main")
    assert new == live and _git(r, "merge-base", "--is-ancestor", live, new).returncode == 0   # contains the old tip
    for k, pair in enumerate((('ok, detail, _ = branches.mirror_and_prove(repo, R + new, tip=sha, label="cut-ff")', 'ok, detail = True, ""'),
                              ('ok, detail, _ = branches.mirror_and_prove(repo, R + new, tip=sha, label="cut-ff")', 'ok, detail = True, ""'))):
        r2, live2 = _core(tmp_path / f"m{k}")
        extra = (('if st2 != "present" or not (got == sha or _is_anc(repo, sha, got)):', "if False:"),) if k else ()
        res = _run(_graph(r2), "--global", "--apply", cli=_mutant(tmp_path / f"m{k}", pair, *extra))
        new2 = _remote_sha(r2, "refs/heads/core/season3/main")
        held = res.returncode == 0 and _git(r2, "merge-base", "--is-ancestor", live2, new2).returncode == 0
        assert not held, f"MUTANT {k} (RESUME on BEHIND without the ff) must be RED: the row wants core/season3/main to contain the old tip"
        if not k:
            assert res.returncode == 1 and "does not contain the old tip" in res.stderr    # the post-check alone catches it


# ---- R4: a step-5 refusal leaves origin half-rolled and prints the way back -----------------
def test_r4_a_step_5_stop_prints_the_recovery_and_the_plain_stop_mutant_is_red(repo: Path, tmp_path: Path):
    g = _graph(repo)
    hooks = repo / ".git" / "hooks"
    hooks.mkdir(exist_ok=True)
    (hooks / "pre-commit").write_text("#!/bin/sh\ngit diff --cached --name-only | grep -q 'town/sanc.md' && { echo 'sanc cell refused'; exit 1; }\nexit 0\n")
    (hooks / "pre-commit").chmod(0o755)
    _git(repo, "config", "core.hooksPath", str(hooks))
    _on_new_trunk(repo)
    res = _run(g, "--global", "--apply", "--delete-old", "--actor", "owner")
    assert res.returncode == 1 and "STOP at step 5: cell" in res.stderr, res.stdout + res.stderr
    assert "[rollover] RECOVERY: origin is HALF-ROLLED" in res.stderr
    for old in ("season2/main", "maxx/season2/main", "sanc/season2/main"):
        assert f"git push origin refs/agi/archive/{old}:refs/heads/{old}" in res.stderr
        assert f"refs/heads/{old}" not in _heads(repo)                          # really half-rolled: deleted ...
        assert _remote_sha(repo, f"refs/agi/archive/{old}")                      # ... and restorable
    mut = _mutant(tmp_path, ('return _stop5(repo, restore, h0, cur_branch, f"write.py refused for {cell_id}")', 'return _stop(5, "cell", f"write.py refused for {cell_id}")'))
    repo2 = _build(tmp_path / "m")
    (repo2 / ".git" / "hooks").mkdir(exist_ok=True)
    (repo2 / ".git" / "hooks" / "pre-commit").write_text((hooks / "pre-commit").read_text())
    (repo2 / ".git" / "hooks" / "pre-commit").chmod(0o755)
    _git(repo2, "config", "core.hooksPath", str(repo2 / ".git" / "hooks"))
    _on_new_trunk(repo2)
    red = _run(_graph(repo2), "--global", "--apply", "--delete-old", "--actor", "owner", cli=mut)
    assert "RECOVERY" not in red.stderr, "MUTANT (a plain stop) must be RED: the row wants the RECOVERY lines"


# ---- council 23:46Z 10-14 (1)-(4): the run's REAL town set and argv; two trunks can claim ONE old branch ----
REAL = [(slug, f"council-{slug}", f"vision:{slug}-v")
        for slug in ("core", "local-maxxing", "sanctuary", "streaming-suite", "web-app-suite")]


def _real(tmp_path: Path):
    """The real towns; core/season3/main BEHIND the live trunk; core_old (the live trunk) is local-maxxing's own derived old."""
    r = _build(tmp_path, REAL)
    live = _sh(r, "local-maxxing/season2/main", "season2/main", "live.txt", "l\n")
    _git(r, "push", "-q", "-f", "origin", f"{_remote_sha(r, 'refs/heads/season2/main')}:refs/heads/core/season3/main")
    return r, live


def _lines(text: str, needle: str) -> int:
    return sum(1 for ln in text.splitlines() if needle in ln)


def test_real_towns_and_argv_two_trunks_one_old_branch_roll_with_one_archive_one_delete_and_the_ungrouped_mutant_is_red(tmp_path: Path):
    r, live = _real(tmp_path)
    g = _graph(r)
    argv = ("--global", "--delete-old", "--actor", "owner", "--skip-fold", "core")
    before = _heads(r)
    _on_new_trunk(r)
    dry = _run(g, *argv)                                                    # (4) the DRY names the shared old, ONCE, and pushes nothing
    assert dry.returncode == 0, dry.stdout + dry.stderr
    assert _lines(dry.stdout, "ARCHIVE refs/agi/archive/local-maxxing/season2/main") == 1
    assert _lines(dry.stdout, "DELETE origin/local-maxxing/season2/main") == 1
    assert "shared by town:core, town:local-maxxing: ONE archive, ONE delete" in dry.stdout
    assert _heads(r) == before
    ok = _run(g, *argv, "--apply")                                          # (2) the real run
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert _lines(ok.stdout, "ARCHIVE refs/agi/archive/local-maxxing/season2/main") == 1
    assert _lines(ok.stdout, "DELETE origin/local-maxxing/season2/main") == 1
    after = _heads(r)
    assert after["refs/heads/local-maxxing/season3/main"] == live and after["refs/heads/core/season3/main"] == live
    assert "refs/heads/local-maxxing/season2/main" not in after and "refs/heads/season2/main" not in after
    assert _remote_sha(r, "refs/agi/archive/local-maxxing/season2/main") == live
    assert _fm(g / "nodes" / ".geometry" / "ladder.md")["current_season"] == 3
    for slug, _c, _v in REAL:
        assert _fm(g / "nodes" / "town" / f"{slug}.md")["season"] == 3
    mut = _mutant(tmp_path / "m0", ('groups.setdefault(e["old"], []).append(e)', 'groups.setdefault(e["cell_id"], []).append(e)'))
    r2, _l2 = _real(tmp_path / "m0")
    _on_new_trunk(r2)
    red = _run(_graph(r2), *argv, "--apply", cli=mut)
    assert _lines(red.stdout, "ARCHIVE refs/agi/archive/local-maxxing/season2/main") != 1, "MUTANT (no grouping by the old branch) must be RED: the row wants ONE archive line"


def test_a_stop_after_the_first_delete_prints_the_recovery_in_pass_1_and_the_plain_stop_mutant_is_red(tmp_path: Path):
    def refused(base: Path):
        r, _live = _real(base)
        hook = r.parent / "origin.git" / "hooks" / "pre-receive"
        hook.write_text("#!/bin/sh\nwhile read o n r; do case \"$r\" in\n"
                        "refs/heads/sanctuary/season2/main) case \"$n\" in 0000000*) echo 'delete refused'; exit 1;; esac;;\nesac; done\nexit 0\n")
        hook.chmod(0o755)
        _git(hook.parent.parent, "config", "core.hooksPath", str(hook.parent))
        _on_new_trunk(r)
        return r
    r = refused(tmp_path)
    res = _run(_graph(r), "--global", "--delete-old", "--actor", "owner", "--skip-fold", "core", "--apply")
    assert res.returncode == 1 and "STOP at step 4: delete" in res.stderr, res.stdout + res.stderr
    assert "[rollover] RECOVERY: origin is HALF-ROLLED" in res.stderr
    for old in ("season2/main", "local-maxxing/season2/main"):                # deleted before the stop: restorable by the printed line
        assert f"git push origin refs/agi/archive/{old}:refs/heads/{old}" in res.stderr
        assert f"refs/heads/{old}" not in _heads(r)
    assert "refs/heads/sanctuary/season2/main" in _heads(r)                   # the refused one is still there
    assert "restore sanctuary/season2/main" not in res.stderr
    mut = _mutant(tmp_path / "m0", ("                if restore: _recovery(repo, restore, h0, cur_branch)\n", "                pass\n"))
    r2 = refused(tmp_path / "m0")
    red = _run(_graph(r2), "--global", "--delete-old", "--actor", "owner", "--skip-fold", "core", "--apply", cli=mut)
    assert "RECOVERY" not in red.stderr, "MUTANT (a plain stop in pass 1) must be RED: the row wants the RECOVERY lines"


# ---- (iv) every town cell is at the global season before --global --------------------------
def test_iv_a_town_cell_behind_the_global_season_is_refused_before_anything_and_the_mutant_is_red(repo: Path, tmp_path: Path):
    g = _graph(repo)
    maxx = g / "nodes" / "town" / "maxx.md"
    maxx.write_text(maxx.read_text().replace("season: 2", "season: 1"))
    before = _heads(repo)
    res = _run(g, "--global", "--apply")
    assert res.returncode == 1 and "town(s) maxx not at global season 2 — align first" in res.stderr
    assert _heads(repo) == before
    mut = _mutant(tmp_path, ("    if misaligned:\n", "    if False:\n"))
    red = _run(g, "--global", cli=mut)
    assert not (red.returncode == 1 and "align first" in red.stderr), "MUTANT (alignment check dropped) must be RED"
