"""The two FLIP SUCCESSORS (goal:g7.16.1.11.13.1): turning cron:crons `grid_sync.enabled` false must not stop (1) the 5-minute on-disk evidence demotion (`evidence_gate.py enforce`, which only
`grid.py commit --all` ran) or (2) the town MIRROR push (`refs/heads/<town>/*` -> `refs/agi/<town>/*`). Each is a cron:crons job of its own, `evidence_enforce` and `town_mirror`, independent of grid_sync.

PROVED BY THE REAL RENDERED LINES. The fixture is a project (`<repo>/.agi`, a git repo, a bare origin) whose crons node is a yaml copy of the REAL `.agi/nodes/.geometry/crons.md` with ONE literal flipped
(grid_sync.enabled false) or edited per row. Rendering is the real `crons.render_managed_lines` (and `crons.py show`); the evidence and mirror lines are then RUN with `sh -c` in a bare environment
against fixture graphs / repos. Nothing touches the real crontab, graph or origin. HOME is a sandbox.

v2 (DG1 17:53Z, SM G-4 / G-5): (e) the evidence job KEEPS the suite-lock deferral of the grid path it replaces (verification.suite_lock_holder's own judgement: a LIVE FOREIGN pid in the suite lock = the tick prints `evidence gate deferred: suite lock held by pid N`, rewrites NO node file, rc 0; the next tick runs) and is NOT a committer (no commit, no ref; the demotion is an in-place working-tree edit, a second run changes nothing). test_crons_mirror.py changes with the build (sent with these rows). v3 (DG1 18:21Z, writer-list FIX ROWS): (f) F1 the grid.py migrate verbs REFUSE `--write` by name while grid_sync is retired (no ref moved), dry-run unchanged, grid_sync on = today's; F2 no PLAIN fetch updates refs/grid after the flip: the mail_poll line the node renders (the live cell crons.md:24 and crons.py's built-in) run with grid_sync off leaves local refs/grid unchanged, with grid_sync on it fetches the grid as today (cli.py:4241, the rename verb's `git fetch`, has no row: it needs a full branch-rename fixture; DG1 to rule).

Pinned (contract for the builder; the rows are implementation-agnostic otherwise): the evidence line is the ONLY rendered line naming `evidence_gate.py`, runs `enforce --root <the graph root>`, every 5 minutes,
behind `box: local-town`; each town gets ONE mirror line, byte-for-byte `crons._mirror_push_line` (the shape test_crons_mirror.py pins), every 5 minutes, any box; with grid_sync ON the rendered set is
today's (the node WITHOUT the two jobs and with `mirror_towns: true` on grid_sync) plus the one evidence line; neither job names grid.py; `mirror_towns` is gone from the grid_sync cell; `crons_live: false` removes
every line; a disabled job renders nothing.
Env FLIP_ROOT=<tree> runs a scratch tree (extensions/agi/bin + .agi/nodes/.geometry/crons.md); default: the repo that holds this file.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve()
ROOT = Path(os.environ.get("FLIP_ROOT") or HERE.parents[3])
BIN = ROOT / "extensions" / "agi" / "bin"
NODE = ROOT / ".agi" / "nodes" / ".geometry" / "crons.md"
sys.path.insert(0, str(BIN))

import crons  # noqa: E402

TOWNS = ("core", "local-maxxing")
BOX = "local-town"
EVERY5 = "*/5 * * * *"


def real_fm() -> dict:
    text = NODE.read_text()
    return yaml.safe_load(text.split("---", 2)[1])


def evid(lines):
    return [l for l in lines if "evidence_gate.py" in l]


def mirrors(lines):
    return [l for l in lines if "for-each-ref" in l and "refs/agi/" in l]


def cmd_of(line: str) -> str:
    return line.split(" ", 5)[5]


def sh(cmd: str, cwd: Path, home: Path, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["sh", "-c", cmd], cwd=str(cwd), capture_output=True, text=True,
                          env={"PATH": "/usr/bin:/bin", "HOME": str(home), **(env or {})})


def git(path: Path, *args: str) -> str:
    r = subprocess.run(["git", *args], cwd=path, capture_output=True, text=True,
                       env={"PATH": "/usr/bin:/bin", "HOME": str(path), "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null",
                            "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})
    if r.returncode != 0:
        raise RuntimeError(f"git {args} in {path}: {r.stderr}")
    return r.stdout.strip()


class Fx:
    """A fixture project: <tmp>/repo/.agi (graph, config {}), a git repo with a bare origin, the REAL extensions/ linked in (so {repo_root} and {engine_root} both find the real pieces)."""

    def __init__(self, tmp_path: Path, monkeypatch, edit=None, towns=TOWNS):
        self.home = tmp_path / "home"
        self.home.mkdir()
        monkeypatch.setenv("HOME", str(self.home))
        self.repo = tmp_path / "repo"
        self.graph = self.repo / ".agi"
        (self.graph / "nodes" / ".geometry").mkdir(parents=True)
        (self.graph / "config.json").write_text("{}")
        (self.repo / "extensions").symlink_to(ROOT / "extensions")
        sch = self.graph / "context" / "schemas"
        sch.mkdir(parents=True)
        (sch / "[box].md").write_text((ROOT / ".agi" / "context" / "schemas" / "[box].md").read_text())   # placeholders: {root} {repo_root} {logs} {box} resolve through the real schema
        fm = real_fm()
        if edit:
            edit(fm)
        self.write_node(fm)
        (self.graph / "nodes" / ".geometry" / "ladder.md").write_text(
            "---\ntowns:\n" + "".join(f"  - {t}\n" for t in towns) + "---\n\nladder\n")
        git(self.repo, "init", "-q", "-b", "master")
        git(self.repo, "config", "user.email", "t@t")
        git(self.repo, "config", "user.name", "t")
        git(self.repo, "add", ".agi")
        git(self.repo, "commit", "-q", "-m", "init")
        self.bare = tmp_path / "origin"
        self.bare.mkdir()
        git(self.bare, "init", "-q", "--bare")
        git(self.repo, "remote", "add", "origin", str(self.bare))
        self.log = crons._log_path(self.repo)
        self.log.parent.mkdir(parents=True, exist_ok=True)

    def write_node(self, fm: dict) -> None:
        (self.graph / "nodes" / ".geometry" / "crons.md").write_text("---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n\nBody.\n")

    def render(self, box: str | None = BOX) -> list[str]:
        _, _cfg, repo_root, engine_root, node = crons._resolve(self.graph)
        return crons.render_managed_lines(self.graph, repo_root, engine_root, node, box_name=box)

    def remote(self) -> list[str]:
        r = subprocess.run(["git", "ls-remote", str(self.bare)], capture_output=True, text=True)
        return [l.split("\t")[1] for l in r.stdout.splitlines() if l]

    def remote_map(self) -> dict:
        r = subprocess.run(["git", "ls-remote", str(self.bare)], capture_output=True, text=True)
        return {l.split("\t")[1]: l.split("\t")[0] for l in r.stdout.splitlines() if l}


def flip_off(fm: dict) -> None:
    fm["cadences"]["grid_sync"]["enabled"] = False


def without_the_two(fm: dict) -> None:
    """Today's node: the two successor jobs absent, the mirror flag back on grid_sync."""
    fm["cadences"].pop("evidence_enforce", None)
    fm["cadences"].pop("town_mirror", None)
    fm["cadences"]["grid_sync"]["mirror_towns"] = True


# ====
# a: the rendered set
# ====


def test_a1_with_grid_sync_off_the_two_jobs_render_and_no_grid_line_does(tmp_path, monkeypatch):
    """grid_sync.enabled false in a copy of the REAL node: the rendered lines hold exactly ONE evidence line and ONE mirror line per declared town (core, local-maxxing),
    and NO line runs `grid.py` (no `commit --all`, no `push-changed`)."""
    fx = Fx(tmp_path, monkeypatch, flip_off)
    lines = fx.render()
    assert len(evid(lines)) == 1, f"evidence lines: {evid(lines)}"
    assert len(mirrors(lines)) == len(TOWNS), f"mirror lines: {mirrors(lines)}"
    assert [l for l in lines if "grid.py" in l or "push-changed" in l] == [], [l for l in lines if "grid.py" in l]
    for t in TOWNS:
        assert sum(f"refs/heads/{t}/" in l for l in mirrors(lines)) == 1, (t, mirrors(lines))


def test_a2_with_grid_sync_on_the_rendered_set_is_todays_plus_the_two_jobs(tmp_path, monkeypatch):
    """grid_sync true: the lines are exactly the lines of the node WITHOUT the two jobs (today's: grid_sync's `grid.py commit --all` / `push-changed` / apply step, branch_push, mail_poll, ... all unchanged)
    PLUS the one evidence line PLUS one mirror line per town (the mirror moved out of the grid_sync block; its bytes are pinned in a3). Compared as multisets with the per-fixture paths and log hash normalised."""
    import re
    (tmp_path / "n").mkdir()
    (tmp_path / "o").mkdir()
    new = Fx(tmp_path / "n", monkeypatch, None).render()
    old = Fx(tmp_path / "o", monkeypatch, lambda fm: (fm["cadences"].pop("evidence_enforce", None), fm["cadences"].pop("town_mirror", None), fm["cadences"]["grid_sync"].pop("mirror_towns", None))).render()
    ev, mi = evid(new), mirrors(new)
    assert len(ev) == 1 and len(mi) == len(TOWNS), (ev, mi)
    norm = lambda ls: sorted(re.sub(r"agi-crons-repo-[0-9a-f]{8}", "agi-crons-repo-<h>", l.replace(str(tmp_path / "n"), "<T>").replace(str(tmp_path / "o"), "<T>")) for l in ls)
    rest = [l for l in new if l not in ev and l not in mi]
    assert norm(rest) == norm(old), f"the rest of the set is not today's:\nnew-only: {sorted(set(norm(rest)) - set(norm(old)))}\nold-only: {sorted(set(norm(old)) - set(norm(rest)))}"
    assert any("grid.py" in l and "commit --all" in l for l in new) and any("push-changed" in l for l in new), "grid_sync on still runs `grid.py commit --all` and `push-changed`"


def test_a3_cadence_box_and_the_exact_mirror_shape(tmp_path, monkeypatch):
    """Both jobs run every 5 minutes. The evidence line is box-gated (local-town): on another box, or none, it does NOT render (fail closed); the mirror line is NOT box-gated.
    Each mirror line is byte-for-byte the shape test_crons_mirror.py pins."""
    fx = Fx(tmp_path, monkeypatch, flip_off)
    lines = fx.render(BOX)
    assert f" enforce --root {fx.graph.resolve()} " in evid(lines)[0] and f"cd {fx.graph.resolve()} && " in evid(lines)[0], f"the evidence line enforces on the GRAPH root (not the repo root): {evid(lines)[0]}"
    assert evid(lines)[0].startswith(EVERY5 + " ") and all(l.startswith(EVERY5 + " ") for l in mirrors(lines)), (evid(lines), mirrors(lines))
    for other in ("some-other-box",):
        ls = fx.render(other)
        assert evid(ls) == [], f"box {other!r}: the evidence job edits node files on MAIN and must not render here: {evid(ls)}"
        assert len(mirrors(ls)) == len(TOWNS), f"box {other!r}: the mirror renders on every box"
    for t in TOWNS:
        want = (f"{EVERY5} cd {fx.graph.resolve()} && if git -C {fx.repo.resolve()} for-each-ref --format='%(refname)' refs/heads/{t}/ | grep -q .; then "
                f"git -C {fx.repo.resolve()} push -q origin 'refs/heads/{t}/*:refs/agi/{t}/*' >> {fx.log} 2>&1; fi")
        assert want in lines, f"the {t} mirror line is not today's shape:\nwant {want}\ngot  {[l for l in mirrors(lines) if t in l]}"


def test_a4_the_kill_switch_and_a_disabled_job_remove_the_lines(tmp_path, monkeypatch):
    """crons_live false removes every line (the successors included); enabled false on a successor removes ITS lines only."""
    fx = Fx(tmp_path, monkeypatch, lambda fm: fm.update(crons_live=False))
    assert fx.render() == []
    fx2 = Fx(tmp_path / "a", monkeypatch, lambda fm: fm["cadences"]["evidence_enforce"].update(enabled=False)) if (tmp_path / "a").mkdir() is None else None
    ls = fx2.render()
    assert evid(ls) == [] and len(mirrors(ls)) == len(TOWNS), (evid(ls), mirrors(ls))
    fx3 = Fx(tmp_path / "b", monkeypatch, lambda fm: fm["cadences"]["town_mirror"].update(enabled=False)) if (tmp_path / "b").mkdir() is None else None
    ls = fx3.render()
    assert len(evid(ls)) == 1 and mirrors(ls) == [], (evid(ls), mirrors(ls))


def test_a5_crons_py_show_prints_them_with_grid_sync_off(tmp_path, monkeypatch):
    """The shipped command, not only the function: `crons.py show --root <graph>` (AGI_BOX=local-town, an empty crontab file) lists the evidence line and the mirror lines under `desired:` and no grid.py line."""
    fx = Fx(tmp_path, monkeypatch, flip_off)
    ct = tmp_path / "crontab.txt"
    ct.write_text("")
    r = subprocess.run([sys.executable, str(BIN / "crons.py"), "show", "--root", str(fx.graph), "--crontab-file", str(ct)], cwd=str(tmp_path), capture_output=True, text=True,
                       env={"PATH": "/usr/bin:/bin", "HOME": str(fx.home), "AGI_BOX": BOX})
    assert r.returncode == 0, (r.returncode, r.stdout[-300:], r.stderr[-300:])
    desired = r.stdout.split("desired:\n", 1)[1].split("\n\n", 1)[0]
    assert desired.count("evidence_gate.py") == 1 and desired.count("for-each-ref") == len(TOWNS) and "grid.py" not in desired, desired[-900:]


def test_a6_the_two_jobs_are_cells_of_the_real_node_and_the_flag_moved(tmp_path):
    """The REAL node: `evidence_enforce` (every 5, enabled, box local-town) and `town_mirror` (every 5, enabled) exist; neither cell names grid.py; `mirror_towns` is GONE from the grid_sync cell
    (it moved to town_mirror); grid_sync itself still exists (the flip changes ONE literal later)."""
    fm = real_fm()
    cad = fm["cadences"]
    for name in ("evidence_enforce", "town_mirror"):
        assert name in cad, f"cadences.{name} missing"
        assert cad[name].get("enabled") is True and cad[name].get("every_mins") == 5, (name, cad[name])
        assert "grid.py" not in yaml.safe_dump(cad[name]), (name, cad[name])
    assert cad["evidence_enforce"].get("box") == BOX, cad["evidence_enforce"]
    assert "mirror_towns" not in cad["grid_sync"], cad["grid_sync"]
    assert "grid_sync" in cad


# ====
# b: the rendered evidence line, run
# ====


def graph_with_verdicts(graph: Path) -> dict:
    n = graph / "nodes"
    (n / "hypothesis").mkdir(parents=True, exist_ok=True)
    (n / "experiment").mkdir(parents=True, exist_ok=True)
    unbacked = n / "hypothesis" / "h-unbacked.md"
    backed = n / "hypothesis" / "h-backed.md"
    exp = n / "experiment" / "e1.md"
    bad = n / "hypothesis" / "h-bad.md"
    unbacked.write_text("---\nid: hypothesis:h-unbacked\nmint_id: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1\ntype: hypothesis\nparents: []\nverdict: proved\n---\nbody\n")
    backed.write_text("---\nid: hypothesis:h-backed\nmint_id: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa2\ntype: hypothesis\nparents: []\nverdict: proved\nevidence_runs:\n  - experiment:e1\n---\nbody\n")
    exp.write_text("---\nid: experiment:e1\nmint_id: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa3\ntype: experiment\nparents:\n  - hypothesis:h-backed\nverdict: pending\n---\nbody\n")
    bad.write_text("---\nid: hypothesis:h-bad\nverdict: proved\n  broken: [unclosed\n---\nbody\n")
    return {"unbacked": unbacked, "backed": backed, "bad": bad, "exp": exp}


def run_evidence(fx: Fx) -> tuple[subprocess.CompletedProcess, dict, dict]:
    """grid_sync OFF fixture; the REAL rendered evidence line, `sh -c`, bare env, on a graph with an unbacked verdict, a backed one and an unparseable node."""
    paths = graph_with_verdicts(fx.graph)
    before = {k: p.read_bytes() for k, p in paths.items()}
    lines = evid(fx.render())
    assert len(lines) == 1, f"no single evidence line: {lines}"
    r = sh(cmd_of(lines[0]), fx.graph, fx.home)
    return r, before, paths


def test_b1_the_rendered_evidence_line_demotes_the_unbacked_verdict_in_place_rc_0(tmp_path, monkeypatch):
    fx = Fx(tmp_path, monkeypatch, flip_off)
    r, before, paths = run_evidence(fx)
    assert r.returncode == 0, (r.returncode, r.stdout[-300:], r.stderr[-300:], fx.log.read_text()[-400:] if fx.log.exists() else "")
    after = paths["unbacked"].read_text()
    assert "verdict: inconclusive_lean_proved" in after and "demoted_from: proved" in after, after
    assert paths["unbacked"].read_bytes() != before["unbacked"]


def test_b2_a_backed_verdict_is_untouched(tmp_path, monkeypatch):
    fx = Fx(tmp_path, monkeypatch, flip_off)
    r, before, paths = run_evidence(fx)
    assert r.returncode == 0
    assert paths["backed"].read_bytes() == before["backed"] and paths["exp"].read_bytes() == before["exp"]
    assert "verdict: proved" in paths["backed"].read_text()


def test_b3_an_unparseable_node_is_reported_in_the_log_and_never_rewritten(tmp_path, monkeypatch):
    fx = Fx(tmp_path, monkeypatch, flip_off)
    r, before, paths = run_evidence(fx)
    assert r.returncode == 0
    assert paths["bad"].read_bytes() == before["bad"], "an unparseable node must not be rewritten"
    log = fx.log.read_text() if fx.log.exists() else ""
    assert "h-bad.md" in log + r.stdout + r.stderr, f"the unparseable node must be REPORTED (log {fx.log}): {(log + r.stdout + r.stderr)[-500:]}"


def test_b4_the_evidence_line_does_not_need_grid_sync_nor_a_clean_cwd(tmp_path, monkeypatch):
    """The same demotion with grid_sync ON, and the line run from an unrelated cwd (`cd <root> &&` is part of the line): independent of the grid_sync block and of where cron starts."""
    fx = Fx(tmp_path, monkeypatch, None)
    paths = graph_with_verdicts(fx.graph)
    other = tmp_path / "elsewhere"
    other.mkdir()
    lines = evid(fx.render())
    assert len(lines) == 1
    r = sh(cmd_of(lines[0]), other, fx.home)
    assert r.returncode == 0 and "demoted_from: proved" in paths["unbacked"].read_text(), (r.returncode, r.stderr[-300:])


# ====
# c: the rendered mirror line, run
# ====


def seed_town_ref(fx: Fx, town: str, name: str = "x") -> str:
    git(fx.repo, "branch", f"{town}/{name}")
    return git(fx.repo, "rev-parse", f"refs/heads/{town}/{name}")


def run_mirrors(fx: Fx) -> list:
    out = []
    for l in mirrors(fx.render()):
        out.append(sh(cmd_of(l), fx.graph, fx.home))
    return out


def test_c1_the_rendered_mirror_line_creates_refs_agi_town_x_on_origin_and_a_second_run_moves_nothing(tmp_path, monkeypatch):
    fx = Fx(tmp_path, monkeypatch, flip_off)
    sha = seed_town_ref(fx, "local-maxxing")
    rs = run_mirrors(fx)
    assert all(r.returncode == 0 for r in rs), [(r.returncode, r.stderr[-200:]) for r in rs]
    m = fx.remote_map()
    assert m.get("refs/agi/local-maxxing/x") == sha, m
    assert not any(k.startswith("refs/agi/core/") for k in m), "a town without refs gets nothing"
    assert not any(k.startswith("refs/heads/") for k in m), f"the mirror never writes refs/heads: {m}"
    again = run_mirrors(fx)
    assert all(r.returncode == 0 for r in again) and fx.remote_map() == m, "a second run must move nothing"


def test_c2_with_no_town_refs_the_line_is_a_no_op_rc_0(tmp_path, monkeypatch):
    fx = Fx(tmp_path, monkeypatch, flip_off)
    rs = run_mirrors(fx)
    assert len(rs) == len(TOWNS) and all(r.returncode == 0 for r in rs), [(r.returncode, r.stderr[-200:]) for r in rs]
    assert fx.remote() == [], fx.remote()
    assert (not fx.log.exists()) or fx.log.read_text() == "", "the guard runs BEFORE the push: nothing is pushed, nothing is logged"


def test_c3_the_mirror_is_additive_and_never_forces(tmp_path, monkeypatch):
    """origin already holds refs/agi/local-maxxing/x at a commit D that is NOT an ancestor of the local refs/heads/local-maxxing/x: a non-force push is refused and D stays (a `+` refspec would overwrite it)."""
    fx = Fx(tmp_path, monkeypatch, flip_off)
    tree = git(fx.repo, "rev-parse", "HEAD^{tree}")
    d = git(fx.repo, "commit-tree", tree, "-m", "D diverged")
    git(fx.repo, "push", "-q", "origin", f"{d}:refs/agi/local-maxxing/x")
    e = git(fx.repo, "commit-tree", tree, "-m", "E diverged elsewhere")
    git(fx.repo, "update-ref", "refs/heads/local-maxxing/x", e)
    run_mirrors(fx)
    assert fx.remote_map().get("refs/agi/local-maxxing/x") == d, "the mirror must not force over a diverged origin ref"


# ====
# d: independence from grid.py
# ====


def test_d1_neither_rendered_job_runs_grid_py(tmp_path, monkeypatch):
    fx = Fx(tmp_path, monkeypatch, flip_off)
    lines = fx.render()
    for l in evid(lines) + mirrors(lines):
        assert "grid.py" not in l and "commit --all" not in l, l


# ====
# e: the suite-lock deferral (G-4) and "the job is not a committer" (G-4)
# ====


def lock_path(fx: Fx) -> Path:
    import verification  # the tree's own resolver (ONE reader of the lock policy)
    return fx.graph / "sessions" / verification.suite_lock_name(fx.graph)


def test_e1_a_live_foreign_suite_lock_defers_the_rewrite_and_the_next_tick_runs(tmp_path, monkeypatch):
    """The suite lock names a LIVE foreign pid: the rendered evidence line prints `evidence gate deferred: suite lock held by pid N` (into its log), rewrites NO node file, rc 0. Once that pid is gone the SAME line demotes (the next tick runs the gate)."""
    fx = Fx(tmp_path, monkeypatch, flip_off)
    paths = graph_with_verdicts(fx.graph)
    holder = subprocess.Popen(["sleep", "120"])
    try:
        lp = lock_path(fx)
        lp.parent.mkdir(parents=True, exist_ok=True)
        lp.write_text(f"{holder.pid}\n")
        before = {k: p.read_bytes() for k, p in paths.items()}
        line = evid(fx.render())
        assert len(line) == 1, f"no single evidence line: {line}"
        r = sh(cmd_of(line[0]), fx.graph, fx.home)
        log = fx.log.read_text() if fx.log.exists() else ""
        assert r.returncode == 0, (r.returncode, r.stderr[-300:], log[-300:])
        assert f"evidence gate deferred: suite lock held by pid {holder.pid}" in log + r.stdout + r.stderr, f"no deferral message: {(log + r.stdout + r.stderr)[-400:]}"
        assert all(p.read_bytes() == before[k] for k, p in paths.items()), "a node file was rewritten while a live foreign pid held the suite lock"
    finally:
        holder.kill()
        holder.wait()
    r2 = sh(cmd_of(evid(fx.render())[0]), fx.graph, fx.home)
    assert r2.returncode == 0, (r2.returncode, r2.stderr[-300:])
    assert "demoted_from: proved" in paths["unbacked"].read_text(), "the next tick (the holder gone) must run the gate"


def test_e2_a_stale_lock_naming_a_dead_pid_does_not_defer(tmp_path, monkeypatch):
    """A lock file naming a DEAD pid is stale (verification's own judgement): the gate runs, demotes, and prints no deferral."""
    fx = Fx(tmp_path, monkeypatch, flip_off)
    paths = graph_with_verdicts(fx.graph)
    dead = subprocess.Popen(["true"])
    dead.wait()
    lp = lock_path(fx)
    lp.parent.mkdir(parents=True, exist_ok=True)
    lp.write_text(f"{dead.pid}\n")
    r = sh(cmd_of(evid(fx.render())[0]), fx.graph, fx.home)
    log = fx.log.read_text() if fx.log.exists() else ""
    assert r.returncode == 0, (r.returncode, r.stderr[-300:])
    assert "deferred" not in log + r.stdout + r.stderr, (log + r.stdout + r.stderr)[-300:]
    assert "demoted_from: proved" in paths["unbacked"].read_text()


def test_e3_the_job_leaves_no_commit_and_no_ref_and_a_second_run_changes_nothing(tmp_path, monkeypatch):
    """SM G-4, THE COMMITTER named: evidence_enforce is a working-tree editor, not a committer. With the nodes tracked: after a run HEAD and EVERY ref (refs/grid included: none is created) are unchanged, the demoted node is modified in the working tree (unstaged, only that one), and a second run changes no byte, no ref, no status."""
    fx = Fx(tmp_path, monkeypatch, flip_off)
    paths = graph_with_verdicts(fx.graph)
    git(fx.repo, "add", "-A")
    git(fx.repo, "commit", "-q", "-m", "nodes")
    head = git(fx.repo, "rev-parse", "HEAD")
    refs = git(fx.repo, "for-each-ref", "--format=%(refname) %(objectname)")
    ncommits = git(fx.repo, "rev-list", "--count", "--all")
    line = cmd_of(evid(fx.render())[0])
    r = sh(line, fx.graph, fx.home)
    assert r.returncode == 0, (r.returncode, r.stderr[-300:])
    assert git(fx.repo, "rev-parse", "HEAD") == head and git(fx.repo, "rev-list", "--count", "--all") == ncommits, "the job made a commit"
    assert git(fx.repo, "for-each-ref", "--format=%(refname) %(objectname)") == refs, "the job moved or created a ref"
    assert "refs/grid" not in git(fx.repo, "for-each-ref", "--format=%(refname)")
    assert git(fx.repo, "diff", "--name-only").split() == [".agi/nodes/hypothesis/h-unbacked.md"], "the demotion must be an unstaged working-tree edit of exactly the unbacked node"
    assert git(fx.repo, "diff", "--cached", "--name-only") == "", "the job staged something"
    snap = {k: p.read_bytes() for k, p in paths.items()}
    status = git(fx.repo, "status", "--porcelain")
    r2 = sh(line, fx.graph, fx.home)
    assert r2.returncode == 0
    assert {k: p.read_bytes() for k, p in paths.items()} == snap, "a second run changed a node file"
    assert git(fx.repo, "status", "--porcelain") == status and git(fx.repo, "rev-parse", "HEAD") == head
    assert git(fx.repo, "for-each-ref", "--format=%(refname) %(objectname)") == refs


# ====
# f: the writer list's FIX ROWS (F1 the migrate verbs, F2 the plain fetch)
# ====

RETIRED_LINE = "grid: retired (cron:crons grid_sync.enabled false); nothing written"


def grid_cmd(fx: Fx, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(BIN / "grid.py"), *args], cwd=str(fx.graph), capture_output=True, text=True, timeout=120,
                          env={"PATH": "/usr/bin:/bin", "HOME": str(fx.home), "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null", "PYTHONPATH": str(BIN)})


def all_refs(repo: Path) -> str:
    return git(repo, "for-each-ref", "--format=%(refname) %(objectname)")


def seed_migrations(fx: Fx) -> dict:
    """Refs the three migrate verbs would move: two grid tips for migrate-trunk, a node-id-keyed ref for migrate-mint-refs (doc:n0 -> its mint ref), a legacy-sanitize ref for migrate-refs (doc:a b)."""
    import grid
    sha = git(fx.repo, "rev-parse", "HEAD")
    nd = fx.graph / "nodes" / "doc"
    nd.mkdir(parents=True, exist_ok=True)
    mint0, mint1 = "0" * 31 + "1", "0" * 31 + "2"
    (nd / "n0.md").write_text(f"---\nid: doc:n0\nmint_id: {mint0}\ntype: doc\nparents: []\n---\nbody\n")
    (nd / "ab.md").write_text(f"---\nid: doc:a b\nmint_id: {mint1}\ntype: doc\nparents: []\n---\nbody\n")
    git(fx.repo, "add", "-A")
    git(fx.repo, "commit", "-q", "-m", "nodes")
    sha = git(fx.repo, "rev-parse", "HEAD")
    refs = {"trunk": ["refs/grid/node/tt-1", "refs/grid/node/tt-2"], "mint_old": grid.node_ref("doc:n0"), "mint_new": grid.mint_node_ref(mint0),
            "leg_old": grid._node_ref_legacy("doc:a b"), "leg_new": grid.node_ref("doc:a b")}
    for r in [*refs["trunk"], refs["mint_old"], refs["leg_old"]]:
        git(fx.repo, "update-ref", r, sha)
    return refs


VERBS = {"migrate-trunk": ["migrate-trunk", "--to", "refs/gridx"], "migrate-mint-refs": ["migrate-mint-refs"], "migrate-refs": ["migrate-refs"]}


@pytest.mark.parametrize("verb", sorted(VERBS))
def test_f1_a_retired_grid_refuses_migrate_write_by_name_and_moves_no_ref(tmp_path, monkeypatch, verb):
    """grid_sync retired: `grid.py <migrate-verb> --write` prints RETIRED_LINE, exits 0 and changes NO ref (the verbs write under refs/grid: update-ref / update-ref -d)."""
    fx = Fx(tmp_path, monkeypatch, flip_off)
    seed_migrations(fx)
    before = all_refs(fx.repo)
    r = grid_cmd(fx, *VERBS[verb], "--write")
    assert r.returncode == 0, (r.returncode, r.stdout[-300:], r.stderr[-300:])
    assert RETIRED_LINE in r.stdout, f"no refusal by name: {r.stdout[-300:]!r}"
    assert all_refs(fx.repo) == before, "a retired grid moved a ref"


@pytest.mark.parametrize("verb", sorted(VERBS))
def test_f1_dry_run_is_unchanged_while_retired(tmp_path, monkeypatch, verb):
    """The dry run (the default) still REPORTS while retired: its usual summary (`(dry-run)`), no refusal line, rc 0, no ref changed."""
    fx = Fx(tmp_path, monkeypatch, flip_off)
    seed_migrations(fx)
    before = all_refs(fx.repo)
    r = grid_cmd(fx, *VERBS[verb])
    assert r.returncode == 0, (r.returncode, r.stdout[-300:], r.stderr[-300:])
    assert "dry-run" in r.stdout and RETIRED_LINE not in r.stdout, r.stdout[-300:]
    assert all_refs(fx.repo) == before


def test_f1_grid_sync_on_is_todays_behaviour_the_verbs_move_refs(tmp_path, monkeypatch):
    """The control: grid_sync ON, `--write` MOVES the seeded refs (so the refusals above are the gate, not an empty fixture): migrate-trunk to refs/gridx, migrate-mint-refs to the mint ref, migrate-refs to the injective name."""
    fx = Fx(tmp_path, monkeypatch, None)
    refs = seed_migrations(fx)
    for verb in sorted(VERBS):
        r = grid_cmd(fx, *VERBS[verb], "--write")
        assert r.returncode == 0 and RETIRED_LINE not in r.stdout, (verb, r.returncode, r.stdout[-300:], r.stderr[-300:])
    have = set(git(fx.repo, "for-each-ref", "--format=%(refname)").splitlines())
    gx = lambda r: r.replace("refs/grid/", "refs/gridx/", 1)   # migrate-trunk ran last and moved everything under refs/grid/node/ (including what the other two verbs just produced)
    want = {gx(r) for r in [*refs["trunk"], refs["mint_new"], refs["leg_new"]]}
    assert want <= have, (sorted(want - have), sorted(have))
    assert not [r for r in have if r.startswith("refs/grid/")], sorted(have)


def mail_poll_line(fx: Fx) -> str:
    ls = [l for l in fx.render() if " fetch " in l and "origin" in l]
    assert len(ls) == 1, f"mail_poll's fetch line: {ls}"
    return ls[0]


def run_fetch_line(fx: Fx, tmp_path: Path) -> subprocess.CompletedProcess:
    """The rendered mail_poll line, `sh -c`, bare env; python3 is a no-op shim so only the FETCH part is real (the send.py / rotate.py halves are not under test)."""
    shim = tmp_path / "shim"
    shim.mkdir(exist_ok=True)
    (shim / "python3").write_text("#!/bin/sh\nexit 0\n")
    (shim / "python3").chmod(0o755)
    return subprocess.run(["sh", "-c", cmd_of(mail_poll_line(fx))], cwd=str(fx.graph), capture_output=True, text=True, timeout=120,
                          env={"PATH": f"{shim}:/usr/bin:/bin", "HOME": str(fx.home), "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"})


def origin_with_new_grid_tip(fx: Fx) -> str:
    tree = git(fx.repo, "rev-parse", "HEAD^{tree}")
    sha = git(fx.repo, "commit-tree", tree, "-m", "a NEW grid tip on origin")
    git(fx.repo, "push", "-q", "origin", f"{sha}:refs/grid/node/zz")   # BEFORE the refspec below: a push also updates a local ref its tracking refspec matches
    git(fx.repo, "config", "--add", "remote.origin.fetch", "+refs/grid/*:refs/grid/*")   # what `grid.py init` configures (grid.py:881): a plain fetch would write refs/grid
    return sha


def local_grid_refs(fx: Fx) -> str:
    return git(fx.repo, "for-each-ref", "--format=%(refname) %(objectname)", "refs/grid")


def test_f2_after_the_flip_the_rendered_mail_poll_line_does_not_update_refs_grid(tmp_path, monkeypatch):
    """The EFFECT: a bare origin carries a NEW refs/grid tip and the clone's remote.origin.fetch carries the forced grid refspec; with grid_sync OFF the mail_poll line the node renders (the live cell, crons.md:24) is run: local refs/grid is unchanged (nothing there before, nothing after). The build may rewrite the line's fetch to an explicit heads refspec; unsetting the grid refspec in config does not satisfy THIS row (the line itself must be grid-safe)."""
    fx = Fx(tmp_path, monkeypatch, flip_off)
    origin_with_new_grid_tip(fx)
    before = local_grid_refs(fx)
    r = run_fetch_line(fx, tmp_path)
    assert r.returncode == 0, (r.returncode, r.stdout[-300:], r.stderr[-300:])
    assert local_grid_refs(fx) == before == "", f"a plain fetch moved refs/grid after the flip: {local_grid_refs(fx)}"


def test_f2_the_fetch_still_happens_after_the_flip_heads_arrive(tmp_path, monkeypatch):
    """Non-vacuity: the flipped line still FETCHES (a new branch on origin arrives under refs/remotes/origin/): the mail_poll consumer keeps working, only the grid namespace stops."""
    fx = Fx(tmp_path, monkeypatch, flip_off)
    tree = git(fx.repo, "rev-parse", "HEAD^{tree}")
    sha = git(fx.repo, "commit-tree", tree, "-m", "a new branch")
    git(fx.repo, "push", "-q", "origin", f"{sha}:refs/heads/newbranch")
    r = run_fetch_line(fx, tmp_path)
    assert r.returncode == 0, (r.returncode, r.stderr[-300:])
    assert git(fx.repo, "rev-parse", "refs/remotes/origin/newbranch") == sha


def test_f2_grid_sync_on_the_grid_is_fetched_as_today(tmp_path, monkeypatch):
    """grid_sync ON = today's: the same line fetches the grid tip into local refs/grid."""
    fx = Fx(tmp_path, monkeypatch, None)
    sha = origin_with_new_grid_tip(fx)
    r = run_fetch_line(fx, tmp_path)
    assert r.returncode == 0, (r.returncode, r.stderr[-300:])
    assert local_grid_refs(fx) == f"refs/grid/node/zz {sha}", local_grid_refs(fx)


# ====
# g: the OLD flag `grid_sync.mirror_towns` (DG1 21:4xZ, SM's gate): refused BY NAME, and a node crons.py refuses never retires the grid SILENTLY
# ====

NOT_RETIRED = "grid: crons node invalid ({}); grid NOT retired"


def with_old_flag(value, enabled=None):
    def edit(fm: dict) -> None:
        fm["cadences"]["grid_sync"]["mirror_towns"] = value
        if enabled is not None:
            fm["cadences"]["grid_sync"]["enabled"] = enabled
    return edit


def refusal_text(fx: Fx) -> str:
    with pytest.raises(crons.CronsError) as e:
        crons.load_crons_node(fx.graph)
    return str(e.value)


@pytest.mark.parametrize("value", [True, False])
def test_g1_a_node_still_carrying_the_old_mirror_towns_flag_is_refused_by_name(tmp_path, monkeypatch, value):
    """`cadences.grid_sync.mirror_towns` (either value) moved to the `town_mirror` job: load_crons_node refuses the node, and the text NAMES both the old flag and the new job (so the operator
    sees what to do). Control: the same node without the flag loads."""
    fx = Fx(tmp_path, monkeypatch, with_old_flag(value))
    text = refusal_text(fx)
    assert "mirror_towns" in text and "town_mirror" in text, text
    (tmp_path / "ok").mkdir()
    ok = Fx(tmp_path / "ok", monkeypatch, None)
    assert "mirror_towns" not in crons.load_crons_node(ok.graph)["jobs"]["grid_sync"]


@pytest.mark.parametrize("enabled", [None, False, True])
def test_g2_grid_retired_on_a_refused_node_is_false_and_prints_one_named_line_per_call(tmp_path, monkeypatch, capsys, enabled):
    """grid_retired() on a node crons.py REFUSES keeps the fail-safe value False (the grid keeps working) but is no longer silent: ONE stderr line per call, exactly
    `grid: crons node invalid (<the CronsError text>); grid NOT retired`, nothing on stdout. With `enabled: false` ALSO set (the flip done on an invalid node) it is STILL False: an invalid node never retires the grid."""
    import grid
    fx = Fx(tmp_path, monkeypatch, with_old_flag(True, enabled))
    want = NOT_RETIRED.format(refusal_text(fx))
    capsys.readouterr()
    assert grid.grid_retired(fx.graph) is False
    first = capsys.readouterr()
    assert first.err.splitlines() == [want] and first.out == "", (first.err, first.out)
    assert grid.grid_retired(fx.graph) is False
    second = capsys.readouterr()
    assert second.err.splitlines() == [want], f"one line PER call: {second.err!r}"


def test_g3_a_valid_node_is_silent_on_or_off(tmp_path, monkeypatch, capsys):
    """Control for g2: a node crons.py accepts prints NOTHING on stderr from grid_retired(): ON -> False, flipped OFF -> True."""
    import grid
    (tmp_path / "off").mkdir()
    on = Fx(tmp_path, monkeypatch, None)
    off = Fx(tmp_path / "off", monkeypatch, flip_off)
    capsys.readouterr()
    assert grid.grid_retired(on.graph) is False
    assert grid.grid_retired(off.graph) is True
    assert capsys.readouterr().err == ""


def test_g4_the_grid_keeps_working_on_a_refused_node_and_names_it_on_stderr(tmp_path, monkeypatch):
    """The CLI: `grid.py commit --all` on a refused node (even with `enabled: false` set) is NOT retired: rc 0, no RETIRED_LINE, refs/grid written, and stderr carries the named line ONCE."""
    fx = Fx(tmp_path, monkeypatch, with_old_flag(True, False))
    seed_migrations(fx)
    import re
    assert "mirror_towns" in refusal_text(fx)
    before = git(fx.repo, "for-each-ref", "--format=%(refname) %(objectname)", "refs/grid")
    r = grid_cmd(fx, "commit", "--all")
    assert r.returncode == 0 and RETIRED_LINE not in r.stdout, (r.returncode, r.stdout[-300:], r.stderr[-300:])
    named = [l for l in r.stderr.splitlines() if re.fullmatch(r"grid: crons node invalid \(.*mirror_towns.*\); grid NOT retired", l)]
    assert len(named) == 1, (named, r.stderr[-500:])
    assert git(fx.repo, "for-each-ref", "--format=%(refname) %(objectname)", "refs/grid") != before, "the grid did not write: it was treated as retired"
