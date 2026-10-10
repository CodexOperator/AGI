"""E2b0 (goal:g7.16.1.11.13, node re-cut 6, DG1 ruling E2b0 + belam 10-08 12:4xZ option (b)): the GATE. `grid.py commit` and `grid.py push-changed` write nothing under refs/grid once `crons.py` ITSELF reads cron:crons `cadences.grid_sync.enabled` as False.

`grid_retired(root)` = a lazy `import crons`, then `crons.load_crons_node(<SHARED root>)["jobs"]["grid_sync"]["enabled"] is False` (the shared root is `locations.shared_project_root`, like `ref_ns_for`: a linked worktree carries its own `.agi` that can lag); ANY exception is NOT retired. So the gate is retired ONLY when crons.py reads `grid_sync.enabled` as False: every YAML-1.1 off spelling (`false`, `False`, `FALSE`, `no`, `No`, `off`, `Off`), flow style, a comment, CRLF, indents read not assumed. `crons_live: false`, a `box:` gate and an absent key also drop the job from the applier but leave the gate OPEN (fail-safe). Not retired: true / yes, a missing file / key / job, and everything crons.py refuses (it validates the WHOLE node: an empty / 0 / "false" / `n` value, a tab, a BOM, no closing `---`, an unknown job with no `cmd`, `import yaml` missing) and a DEEPER `enabled: false` (grid_sync.mirror.enabled). Retired, `grid.py commit` and `grid.py push-changed` print `grid: retired (cron:crons grid_sync.enabled false); nothing written` and exit 0; read verbs are not gated.

Every row builds its OWN node in a scratch repo (the live crons.md is only the base of the other cadences), except B8f, which edits the LIVE node. RED on the trunk without the gate: the retired B8 / B8c / B8e / B8f / B8h rows; GREEN without it: the RENDER rows B4 B5 B7 (the cron block loses only grid_sync lines (and, with .13.1 F2, has the mail_poll fetch rewritten by exactly one substitution), renders no grid writer, the pre-switch node is the witness) and every not-retired row. B8: BEHAVIOURAL, retired `grid.py commit --all`, `push-changed`, rotate.py's `_button_down` and closeout `_grid_commit` leave refs/grid byte-identical (and the scratch origin holds none); the same calls with grid_sync ON move it (the witnesses), and every not-retired state moves it too. B8b pins the rotate.py writer FUNCTIONS to {_grid_commit, _button_down, _push} (a fourth is a RED); B9 proves the scanner can see one. B8c: the gate reads the SHARED root. B8d: a deeper `enabled: false` never retires the job. B8e: the switch node as RAW TEXT, one row per shape (every other row writes it through yaml.safe_dump, which can only emit the canonical form), each shape ANCHORED to what `crons.load_crons_node` says about it (an anchor row per shape, so the table is not opinion), each row asserting the verdict AND what the verbs did. B8h (SM residue, DG1 ruling (b); B8h-3 the legacy `grid.py cron install` snap line, DG1 15:18Z): a RETIRED push may publish ONLY tips that already exist locally: rotate's closeout push step and `grid.py sync` (the operator's verb, ungated by design) leave the local refs/grid/* identical, the origin ends equal to local, a second push moves nothing. B8f: the REAL node (the trunk's crons.md with ONLY `grid_sync.enabled` set to false is retired; unflipped is not) and `import yaml` missing AFTER grid loaded (not retired, no exception; the same call a line earlier is True: this row is also what sees a module-level `import crons`, which keeps its binding when `crons` is dropped from sys.modules).

Override the units under test: CRONS_NODE=<crons.md copy> (the base node), GRID_PY=<grid.py copy> (the gate; copied into the scratch engine dir next to the real crons.py), ROTATE_PY=<rotate.py copy> (a new writer).
"""
from __future__ import annotations

import ast
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve()
BIN = HERE.parents[1] / "bin"
REPO = HERE.parents[3]
sys.path.insert(0, str(BIN))

import crons  # noqa: E402
from tests.veto_cell import write_free_veto  # noqa: E402

GRID_PY = Path(os.environ.get("GRID_PY") or BIN / "grid.py")
LIVE_NODE = Path(os.environ.get("CRONS_NODE")
                 or REPO / ".agi" / "nodes" / ".geometry" / "crons.md")
BOX_SCHEMA = REPO / ".agi" / "context" / "schemas" / "[box].md"
BOX = "encryption-town"
MAIL_BOX = "local-town"   # mail_poll stays box-gated to local-town (the hub reader): the rows that read ITS line render the block for that box


def git(repo: Path, *args: str, check: bool = True, env: dict | None = None) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                       env={**os.environ, **(env or {})})
    if check and r.returncode != 0:
        raise RuntimeError(f"git {args}: {r.stderr}")
    return r.stdout.strip()


@pytest.fixture(autouse=True)
def _home(tmp_path, monkeypatch):
    h = tmp_path / "home"
    h.mkdir()
    monkeypatch.setenv("HOME", str(h))
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/dev/null")
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", "/dev/null")
    monkeypatch.delenv("AGI_BOX", raising=False)
    return h


# --- E2b: the switch, over the LIVE node ---


def _live_fm() -> dict:
    return yaml.safe_load(LIVE_NODE.read_text().split("---\n", 2)[1])


NODE_TMPL = """---
id: doc:{n}
mint_id: {m}
type: doc
parents: []
next_edges: []
edited_by: e2b
season: 2
title: node {n}
town: core
---
# doc:{n}

body {n}
"""


def make_project(tmp_path: Path, fm: dict, name: str = "repo", nodes: int = 3) -> Path:
    """G11 layout: root = repo/.agi, repo_root = engine_root = repo; engine bin =
    symlinks to the real modules; `nodes` node files committed on master; an
    `origin` that is a scratch bare repo."""
    repo = tmp_path / name
    repo.mkdir(parents=True)
    git(repo, "init", "-q", "-b", "master")
    git(repo, "config", "user.email", "t@t")
    git(repo, "config", "user.name", "t")
    root = repo / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "nodes" / "doc").mkdir(parents=True)
    (root / "config.json").write_text("{}")
    (root / "nodes" / ".geometry" / "crons.md").write_text(
        "---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n\nBody.\n")
    schema = root / "context" / "schemas" / "[box].md"
    schema.parent.mkdir(parents=True)
    schema.write_text(BOX_SCHEMA.read_text())
    eb = repo / "extensions" / "agi" / "bin"
    eb.mkdir(parents=True)
    for p in BIN.iterdir():
        if p.is_file() and p.name != "grid.py":
            (eb / p.name).symlink_to(p)
    shutil.copy(GRID_PY, eb / "grid.py")   # a real file: sys.path[0] is then the scratch engine dir, where crons.py (a symlink) imports
    if os.environ.get("ROTATE_PY"):   # a candidate rotate.py (a mutant of the push step): a real file beside grid.py
        (eb / "rotate.py").unlink()
        shutil.copy(os.environ["ROTATE_PY"], eb / "rotate.py")
    for i in range(nodes):
        (root / "nodes" / "doc" / f"n{i}.md").write_text(
            NODE_TMPL.format(n=f"n{i}", m=f"{i + 1:032x}"))
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "init")
    bare = tmp_path / f"{name}-origin.git"
    git(tmp_path, "init", "-q", "--bare", str(bare))
    git(repo, "remote", "add", "origin", str(bare))
    return root


def fm_with(grid_sync: bool | None = None, drop_cell: bool = False, live: bool = True) -> dict:
    fm = _live_fm()
    cad = fm["cadences"]
    if grid_sync is not None:
        cad["grid_sync"]["enabled"] = grid_sync
    if drop_cell:
        cad.pop("crons_apply", None)
    fm["crons_live"] = live
    fm.pop("services", None)
    return fm


def render(root: Path, box: str = BOX) -> list[str]:
    _, _, repo_root, engine_root, node = crons._resolve(root)
    return crons.render_managed_lines(root, repo_root, engine_root, node, box_name=box)


GRID_WRITERS = re.compile(r"grid\.py|push-changed|refs/grid|refs/agi/|update-ref")


def refs_grid(repo: Path) -> list[str]:
    return git(repo, "for-each-ref", "--format=%(refname) %(objectname)", "refs/grid").splitlines()


@pytest.fixture
def fakes(tmp_path):
    """A FAKE `crontab` (file table) and `systemctl` first on PATH; the env a
    cron line runs under."""
    fb = tmp_path / "fakebin"
    fb.mkdir()
    table = tmp_path / "crontab.table"
    (fb / "crontab").write_text(
        "#!/bin/sh\n" f"T={table}\n"
        'case "$1" in\n'
        '  -l) if [ -f "$T" ]; then cat "$T"; else echo "no crontab" >&2; exit 1; fi;;\n'
        '  -) cat > "$T";;\n  *) exit 2;;\nesac\n')
    (fb / "systemctl").write_text("#!/bin/sh\nexit 0\n")
    for p in fb.iterdir():
        p.chmod(0o755)
    (Path(os.environ["HOME"]) / "logs").mkdir(exist_ok=True)   # a box that was applied once
    rt = tmp_path / "runtime"
    rt.mkdir()
    (rt / "bus").write_text("")
    return {"PATH": f"{fb}:/usr/bin:/bin", "HOME": os.environ["HOME"], "AGI_BOX": BOX,
            "XDG_RUNTIME_DIR": str(rt), "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_SYSTEM": "/dev/null", "PYTHONPATH": str(BIN)}


def cron_run(line: str, env: dict) -> subprocess.CompletedProcess:
    return subprocess.run(["sh", "-c", line.split(" ", 5)[5]], env=env,
                          capture_output=True, text=True, timeout=120)










#: goal:g7.16.1.11.13.1 F2 (DG1 ruling 19:2xZ): the flip rewrites the mail_poll line's plain fetch to an explicit heads refspec, so no plain fetch updates refs/grid. It is the ONE
#: line the flip may change instead of remove, and by exactly this one substitution.
FETCH_OLD = "fetch -q origin"
FETCH_NEW = "fetch -q origin '+refs/heads/*:refs/remotes/origin/*'"


def switch_pair(tmp_path: Path) -> tuple[list[str], list[str]]:
    """(pre, post): the cron block rendered with grid_sync ON and OFF, the scratch root and the log name normalised."""
    post = render(make_project(tmp_path, fm_with(grid_sync=False), name="post"), MAIL_BOX)
    pre = render(make_project(tmp_path, fm_with(grid_sync=True), name="pre"), MAIL_BOX)
    n = lambda ls, r: [re.sub(r"agi-crons-\S+?\.log", "LOG", l.replace(str(r), "R")) for l in ls]
    return n(pre, tmp_path / "pre"), n(post, tmp_path / "post")


def switch_problems(pre: list[str], post: list[str]) -> list[str]:
    """What the flip did beyond 'remove the grid_sync lines': every removed line names grid.py or refs/agi/, EXCEPT the mail_poll line (it holds `send.py read`), which is not removed
    but REWRITTEN by exactly FETCH_OLD -> FETCH_NEW (once, at the first match); no other line is added, and ON (today's) carries no heads refspec."""
    removed, added = [l for l in pre if l not in post], [l for l in post if l not in pre]
    bad = [f"a pre line already carries the heads refspec: {l}" for l in pre if "refs/remotes/origin" in l]
    if not removed:
        bad.append("the flip removed nothing")
    swapped = [l for l in removed if "send.py read" in l and FETCH_OLD in l and l.replace(FETCH_OLD, FETCH_NEW, 1) in added]
    bad += [f"a removed line names neither grid.py nor refs/agi/ (and is not the mail_poll rewrite): {l}" for l in removed if l not in swapped and not ("grid.py" in l or "refs/agi/" in l)]
    bad += [f"an added line is not the one mail_poll fetch substitution: {l}" for l in added if l not in [s.replace(FETCH_OLD, FETCH_NEW, 1) for s in swapped]]
    bad += [f"{len(swapped)} mail_poll rewrites (at most one)"] if len(swapped) > 1 else []
    return bad


def test_b4_the_switch_removes_only_grid_sync_lines(tmp_path):
    """The cron block loses only grid_sync lines; the ONE other change is the mail_poll fetch, rewritten by exactly FETCH_OLD -> FETCH_NEW (F2). A build without F2 (no rewrite) is GREEN too."""
    pre, post = switch_pair(tmp_path)
    assert switch_problems(pre, post) == []
    assert any("push -q origin" in l for l in post), "branch_push line stays"


def _mail_poll(ls: list[str]) -> str:
    one = [l for l in ls if "send.py read" in l and FETCH_OLD in l.replace(FETCH_NEW, FETCH_OLD)]
    assert len(one) == 1, one
    return one[0]


def _flipped(pre: list[str], rewrite: bool) -> list[str]:
    """A hand-made POST block from the rendered PRE one (build-independent): the grid_sync lines gone, the mail_poll line rewritten by FETCH_OLD -> FETCH_NEW or, without `rewrite`, kept."""
    mp = _mail_poll(pre)
    return [mp.replace(FETCH_OLD, FETCH_NEW, 1) if rewrite and l == mp else l for l in pre if l == mp or not ("grid.py" in l or "refs/agi/" in l)]


def test_b4_the_hand_made_flips_are_green_with_and_without_the_fetch_rewrite(tmp_path):
    """Controls for the mutant rows: the rewrite is allowed, not required (a build without F2 stays GREEN; F2's own rows pin the rewrite)."""
    pre, _ = switch_pair(tmp_path)
    assert FETCH_NEW in _mail_poll(_flipped(pre, True)) and switch_problems(pre, _flipped(pre, True)) == []
    assert FETCH_NEW not in _mail_poll(_flipped(pre, False)) and switch_problems(pre, _flipped(pre, False)) == []


@pytest.mark.parametrize("name,edit", [
    ("a different refspec", lambda ls: [l.replace(FETCH_NEW, FETCH_OLD + " '+refs/*:refs/remotes/origin/*'") for l in ls]),
    ("the substitution twice in the line", lambda ls: [l.replace(FETCH_NEW, FETCH_NEW + " " + FETCH_NEW) for l in ls]),
    ("a SECOND line differs (branch_push gains a flag)", lambda ls: [l.replace("push -q origin", "push -q --force origin") if "push -q origin" in l else l for l in ls]),
    ("a second line is ADDED", lambda ls: [*ls, "*/5 * * * * cd R/.agi && echo extra >> LOG 2>&1"]),
    ("the mail_poll line is dropped, not rewritten", lambda ls: [l for l in ls if FETCH_NEW not in l]),
    ("the rewrite also changes the rest of the line", lambda ls: [l.replace("--peek", "--peek --all") if FETCH_NEW in l else l for l in ls]),
])
def test_b4_mutants_a_second_differing_line_or_another_substitution_is_red(tmp_path, name, edit):
    """One edit to the hand-made POST block each: another refspec, the substitution twice, a second line changed, a line added, the mail_poll line dropped, the mail_poll line changed beyond
    the substitution: each is a problem (the row can fail), the un-mutated block is GREEN (row above)."""
    pre, _ = switch_pair(tmp_path)
    post = _flipped(pre, True)
    mutant = edit(post)
    assert mutant != post, name
    assert switch_problems(pre, mutant), name


def test_b5_no_builtin_job_renders_a_grid_writer(tmp_path):
    """crons.py's own renderers, worst case: every KNOWN job except grid_sync on."""
    fm = fm_with(grid_sync=False)
    for j in ("branch_push", "engine_push", "mail_poll", "nudge_sweep"):
        job = fm["cadences"].setdefault(j, {"every_mins": 5})
        job["enabled"] = True
    root = make_project(tmp_path, fm)
    lines = render(root)
    assert len(lines) >= 8, lines
    assert [l for l in lines if GRID_WRITERS.search(l)] == []




def test_b7_the_pre_switch_node_is_the_witness(tmp_path, fakes):
    """The same run with grid_sync ON moves refs/grid (the row can fail)."""
    root = make_project(tmp_path, fm_with(grid_sync=True))
    repo = root.parent
    env = dict(fakes)
    subprocess.run([sys.executable, str(repo / "extensions/agi/bin/grid.py"), "commit", "--all"],
                   cwd=root, env=env, check=True, capture_output=True)
    before = refs_grid(repo)
    n0 = root / "nodes" / "doc" / "n0.md"
    n0.write_text(n0.read_text() + "\nedited after the last snapshot\n")
    git(repo, "commit", "-qam", "edit n0")
    gl = [l for l in render(root) if "grid.py commit" in l]
    assert len(gl) == 1
    cron_run(gl[0], env)
    assert refs_grid(repo) != before




# --- B8: no non-cron writer moves refs/grid once grid_sync is off (behavioural) ---

RUNNER = """
import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import rotate
root = Path(sys.argv[2])
bd = rotate._button_down(root=root, branch_allow=True, legal_branch=None)
gc = rotate._make_closeout_seams(root, {})["grid_commit"]()
print(json.dumps({"button_down": bd, "grid_commit": list(gc)}))
"""
RETIRED = "grid: retired (cron:crons grid_sync.enabled false)"


def set_grid_sync(root: Path, state: str) -> None:
    """state: on | off | missing_file | missing_key | parse_error | null | zero | string_false
    (the last three are MALFORMED `enabled` values: empty, 0, the string "false")."""
    p = root / "nodes" / ".geometry" / "crons.md"
    if state == "missing_file":
        p.unlink()
        return
    if state == "parse_error":
        p.write_text("---\ncadences: [unclosed\n  grid_sync: {\n---\nbody\n")
        return
    fm = yaml.safe_load(p.read_text().split("---\n", 2)[1])
    if state == "missing_key":
        fm["cadences"].pop("grid_sync", None)
    elif state in ("nested_false", "nested_false_no_own"):
        gs = {"every_mins": 5, "mirror": {"enabled": False}}
        if state == "nested_false":
            gs["enabled"] = True
        fm["cadences"]["grid_sync"] = gs
    elif state in ("null", "zero", "string_false"):
        fm["cadences"]["grid_sync"]["enabled"] = {"null": None, "zero": 0, "string_false": "false"}[state]
    else:
        fm["cadences"]["grid_sync"]["enabled"] = state == "on"
    p.write_text("---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n\nBody.\n")


def sh_env(tmp_path: Path) -> dict:
    return {"PATH": "/usr/bin:/bin", "HOME": os.environ["HOME"], "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_SYSTEM": "/dev/null", "PYTHONPATH": str(BIN)}


def grid_py(root: Path, env: dict, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(root.parent / "extensions/agi/bin/grid.py"), *args],
                          cwd=root, env=env, capture_output=True, text=True, timeout=120)


def rotate_writers(root: Path, env: dict) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-c", RUNNER, str(root.parent / "extensions/agi/bin"), str(root)],
                          cwd=root.parent, env=env, capture_output=True, text=True, timeout=180)


def seeded(tmp_path: Path):
    """A project seeded with one grid version per node (grid_sync ON), a node edited after."""
    root = make_project(tmp_path, fm_with(grid_sync=True))
    env = sh_env(tmp_path)
    r = grid_py(root, env, "commit", "--all")
    assert r.returncode == 0, r.stderr
    n0 = root / "nodes" / "doc" / "n0.md"
    n0.write_text(n0.read_text() + "\nedited after the last snapshot\n")
    return root, env


def test_b8_retired_grid_commit_and_push_changed_write_nothing(tmp_path):
    root, env = seeded(tmp_path)
    before = refs_grid(root.parent)
    assert len(before) >= 3
    set_grid_sync(root, "off")
    a = grid_py(root, env, "commit", "--all")
    b = grid_py(root, env, "push-changed")
    assert a.returncode == 0 and b.returncode == 0, (a.stderr, b.stderr)
    assert RETIRED in a.stdout and RETIRED in b.stdout, (a.stdout[-200:], b.stdout[-200:])
    assert refs_grid(root.parent) == before, "grid.py wrote under refs/grid while retired"
    assert git(tmp_path / "repo-origin.git", "for-each-ref", "refs/grid") == ""


def test_b8_retired_rotate_button_down_and_closeout_grid_commit_write_nothing(tmp_path):
    root, env = seeded(tmp_path)
    before = refs_grid(root.parent)
    set_grid_sync(root, "off")
    r = rotate_writers(root, env)
    assert r.returncode == 0, r.stderr[-600:]
    out = json.loads(r.stdout.strip().splitlines()[-1])
    assert not out["button_down"].startswith(("SKIPPED", "FAILED")), out   # the step RAN (a legal branch): grid.py itself refused to write
    assert out["grid_commit"][0] is True, out
    assert refs_grid(root.parent) == before, "rotate.py moved refs/grid while retired"


def test_b8_witness_grid_sync_on_moves_refs_through_every_writer(tmp_path):
    root, env = seeded(tmp_path)
    before = refs_grid(root.parent)
    r = grid_py(root, env, "commit", "--all")
    assert r.returncode == 0 and refs_grid(root.parent) != before, "ON: grid.py commit --all must move a ref"
    root2, env2 = seeded(tmp_path / "second")
    b2 = refs_grid(root2.parent)
    rotate_writers(root2, env2)
    assert refs_grid(root2.parent) != b2, "ON: rotate.py's writers must move a ref (the row can fail)"


@pytest.mark.parametrize("state", ["on", "missing_file", "missing_key", "parse_error", "null", "zero", "string_false"])
def test_b8_the_gate_is_not_over_eager(tmp_path, state):
    """Only an EXPLICIT boolean false retires: true, a missing file, a missing key, a parse error and a
    MALFORMED value (`enabled:` empty, `enabled: 0`, `enabled: "false"`) do not: a malformed cell must
    never silently stop versioning."""
    root, env = seeded(tmp_path)
    before = refs_grid(root.parent)
    set_grid_sync(root, state)
    r = grid_py(root, env, "commit", "--all")
    assert RETIRED not in r.stdout, state
    assert refs_grid(root.parent) != before, f"{state}: not retired, so the edit must be versioned"


def test_b8_read_verbs_are_not_gated(tmp_path):
    root, env = seeded(tmp_path)
    set_grid_sync(root, "off")
    r = grid_py(root, env, "versions", f"{1:032x}")
    assert r.returncode == 0 and r.stdout.strip().isdigit() and int(r.stdout.strip()) >= 1, r.stdout
    miss = grid_py(root, env, "versions", "b" * 32)
    assert miss.returncode == 0 and miss.stdout.strip() == "0", "a missing mint prints 0 and exits 0: why the row above needs a count >= 1"


# --- B8c (RE7): the gate reads the SHARED root, like ref_ns_for ---
# A linked git worktree carries its OWN .agi/nodes/.geometry/crons.md (committed, so it can predate the
# switch). refs/grid is ONE namespace in the common git dir, so the gate is the MAIN checkout's cell
# (locations.shared_project_root), never the worktree's: main false + worktree true = retired; the converse
# (main true + worktree false) is NOT retired. A gate reading the checkout-local file is RED on the first rows.


# (The worktree sits on a season branch grid.py admits, `season2/main`: rotate's `_button_down` runs `grid.py commit --all` with no
# --allow-branch, so on any other branch it writes NOTHING gate or no gate and the rows would be vacuous.)


def linked_worktree(root: Path, tmp_path: Path, name: str = "wt") -> Path:
    """`git worktree add` of the scratch repo (its HEAD still carries the grid_sync cell the project was
    made with); returns the worktree's own .agi (a node edited there so commit --all WOULD move a ref)."""
    repo = root.parent
    wt = tmp_path / name
    git(repo, "worktree", "add", "-q", "-b", "season2/main", str(wt))
    wroot = wt / ".agi"
    assert wroot.is_dir() and wroot != root
    n1 = wroot / "nodes" / "doc" / "n1.md"
    n1.write_text(n1.read_text() + "\nedited in the worktree\n")
    return wroot


def test_b8c_main_retired_worktree_on_commit_and_push_changed_write_nothing(tmp_path):
    root, env = seeded(tmp_path)
    wroot = linked_worktree(root, tmp_path)           # its own cell says grid_sync TRUE
    set_grid_sync(root, "off")                        # MAIN says FALSE
    assert _cell(wroot) is True and _cell(root) is False
    before = refs_grid(root.parent)
    assert len(before) >= 3
    a = grid_py(wroot, env, "commit", "--all")
    b = grid_py(wroot, env, "push-changed")
    assert a.returncode == 0 and b.returncode == 0, (a.stderr, b.stderr)
    assert RETIRED in a.stdout and RETIRED in b.stdout, (a.stdout[-200:], b.stdout[-200:])
    assert refs_grid(root.parent) == before, "grid.py run from a linked worktree wrote refs/grid while MAIN is retired"
    assert git(tmp_path / "repo-origin.git", "for-each-ref", "refs/grid") == ""


def test_b8c_main_retired_worktree_on_rotate_writers_write_nothing(tmp_path):
    root, env = seeded(tmp_path)
    wroot = linked_worktree(root, tmp_path)
    set_grid_sync(root, "off")
    before = refs_grid(root.parent)
    r = rotate_writers(wroot, env)                    # _button_down(root=<worktree .agi>) and the closeout grid_commit
    assert r.returncode == 0, r.stderr[-600:]
    out = json.loads(r.stdout.strip().splitlines()[-1])
    assert not out["button_down"].startswith(("SKIPPED", "FAILED")), out   # the step RAN: grid.py itself refused
    assert out["grid_commit"][0] is True, out
    assert refs_grid(root.parent) == before, "rotate.py run on a linked worktree moved refs/grid while MAIN is retired"


def test_b8c_main_on_worktree_off_is_not_retired_commit_versions_the_edit(tmp_path):
    root, env = seeded(tmp_path)
    wroot = linked_worktree(root, tmp_path)
    set_grid_sync(wroot, "off")                       # the worktree's cell says FALSE, MAIN's stays TRUE
    assert _cell(wroot) is False and _cell(root) is True
    before = refs_grid(root.parent)
    a = grid_py(wroot, env, "commit", "--all")
    assert a.returncode == 0 and RETIRED not in a.stdout, a.stdout[-200:]
    assert refs_grid(root.parent) != before, "MAIN is not retired, so the worktree's edit must be versioned"


def test_b8c_main_on_worktree_off_rotate_writers_still_move_refs(tmp_path):
    root, env = seeded(tmp_path)
    wroot = linked_worktree(root, tmp_path)
    set_grid_sync(wroot, "off")
    before = refs_grid(root.parent)
    r = rotate_writers(wroot, env)
    assert r.returncode == 0, r.stderr[-600:]
    assert refs_grid(root.parent) != before, "MAIN is not retired: rotate.py's writers must move a ref (the row can fail)"


def _cell(root: Path):
    fm = yaml.safe_load((root / "nodes" / ".geometry" / "crons.md").read_text().split("---\n", 2)[1])
    return fm["cadences"]["grid_sync"]["enabled"]


# --- B8d: only `cadences.grid_sync.enabled` itself retires the job ---


@pytest.mark.parametrize("state", ["nested_false", "nested_false_no_own"])
def test_b8d_a_deeper_enabled_false_does_not_retire_the_job(tmp_path, state):
    """`grid_sync: {enabled: true, mirror: {enabled: false}}` (and the same with NO `enabled` of its own) is NOT
    retired: the edit is versioned. A gate that accepts an `enabled: false` at any depth under grid_sync would stop
    the whole job because its town-mirror sub-cell is off."""
    root, env = seeded(tmp_path)
    before = refs_grid(root.parent)
    set_grid_sync(root, state)
    cell = yaml.safe_load((root / "nodes" / ".geometry" / "crons.md").read_text().split("---\n", 2)[1])["cadences"]["grid_sync"]
    assert cell["mirror"] == {"enabled": False} and cell.get("enabled") is not False, cell   # the fixture is the shape named
    r = grid_py(root, env, "commit", "--all")
    assert RETIRED not in r.stdout, state
    assert refs_grid(root.parent) != before, f"{state}: only grid_sync.enabled retires; the edit must be versioned"
    p = grid_py(root, env, "push-changed")
    assert RETIRED not in p.stdout, state


# --- B8h: a RETIRED push may publish ONLY tips that already exist locally (SM residue, DG1 ruling (b)) ---

PUSHER = """
import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import rotate
print(json.dumps(list(rotate._make_closeout_seams(Path(sys.argv[2]), {})["push"]())))
"""
# `_push` is a closure inside `_make_closeout_seams`; the seam table hands it out as ["push"], so this row runs the REAL closeout push step
# (origin season2/main, then origin grid.push_spec_for(root), both from MAIN, never forced).


def retired_push_fixture(tmp_path: Path):
    """A seeded project (one grid version per node, an edit after), MAIN with the closeout target branch `season2/main`, then grid_sync OFF."""
    root, env = seeded(tmp_path)
    git(root.parent, "branch", "season2/main")
    set_grid_sync(root, "off")
    write_free_veto(root / "nodes" / ".geometry")   # the push step reads the veto cell STRICT
    return root, env


def push_step(root: Path, env: dict) -> tuple:
    r = subprocess.run([sys.executable, "-c", PUSHER, str(root.parent / "extensions/agi/bin"), str(root)],
                       cwd=root.parent, env=env, capture_output=True, text=True, timeout=180)
    assert r.returncode == 0, r.stderr[-600:]
    return tuple(json.loads(r.stdout.strip().splitlines()[-1]))


def test_b8h_a_retired_push_step_publishes_only_the_tips_that_exist_and_is_idempotent(tmp_path):
    root, env = retired_push_fixture(tmp_path)
    origin = tmp_path / "repo-origin.git"
    before = refs_grid(root.parent)
    assert len(before) >= 3 and git(origin, "for-each-ref", "refs/grid") == ""
    a = grid_py(root, env, "commit", "--all")
    b = grid_py(root, env, "push-changed")
    assert RETIRED in a.stdout and RETIRED in b.stdout, (a.stdout[-200:], b.stdout[-200:])
    assert refs_grid(root.parent) == before, "retired commit --all / push-changed moved a local ref"
    ok1 = push_step(root, env)
    assert ok1[0] is True, ok1
    assert refs_grid(root.parent) == before, "the push step created or moved a local refs/grid ref while retired"
    assert refs_grid(origin) == before, "the archive must arrive whole: origin's refs/grid == the local set"
    ok2 = push_step(root, env)                       # a SECOND push: a plain, non-force, idempotent push
    assert ok2[0] is True, ok2
    assert refs_grid(root.parent) == before and refs_grid(origin) == before, "the second push moved something"


def test_b8h_grid_sync_the_operators_verb_stays_ungated_and_says_so(tmp_path):
    root, env = retired_push_fixture(tmp_path)
    origin = tmp_path / "repo-origin.git"
    before = refs_grid(root.parent)
    r = grid_py(root, env, "sync")
    assert r.returncode == 0 and "Traceback" not in r.stderr and RETIRED not in r.stdout, (r.returncode, r.stdout[-200:], r.stderr[-300:])
    assert refs_grid(root.parent) == before, "sync created or moved a local ref while retired"
    assert refs_grid(origin) == before, "sync is ungated: it publishes the local tips"
    d = subprocess.run([sys.executable, "-c",
                        "import sys; sys.path.insert(0, sys.argv[1]); import grid; print(grid.grid_retired.__doc__ or ''); print(grid.cmd_sync.__doc__ or '')",
                        str(root.parent / "extensions/agi/bin")], cwd=root.parent, env=env, capture_output=True, text=True, timeout=60)
    assert d.returncode == 0, d.stderr[-300:]
    assert re.search(r"(?is)\bsync\b.{0,80}operator|operator.{0,80}\bsync\b", d.stdout), "grid_retired's (or cmd_sync's) docstring must name `grid.py sync` as the operator's verb: " + d.stdout[-300:]


def snap_halves(root: Path, env: dict, log: Path) -> tuple[str, str]:
    """The legacy `cron_lines` snap line, rendered by grid.cron_lines in the scratch project, split at its `&&`s into its two halves:
    (cd REPO && python3 grid.py commit --all --prefix 'cron: ' >> LOG 2>&1,  cd REPO && git push -q origin 'PUSH_SPEC' >> LOG 2>&1)."""
    r = subprocess.run([sys.executable, "-c",
                        "import json, sys; from pathlib import Path; sys.path.insert(0, sys.argv[1]); import grid; "
                        "print(json.dumps(grid.cron_lines(Path(sys.argv[2]), 'master', 5, Path(sys.argv[3]))))",
                        str(root.parent / "extensions/agi/bin"), str(root), str(log)],
                       cwd=root.parent, env=env, capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[-400:]
    snap = json.loads(r.stdout.strip().splitlines()[-1])[0]
    cmd = snap.split(" ", 5)[5]                        # the five cron time fields off
    parts = cmd.split(" && ")
    assert len(parts) == 3 and parts[0].startswith("cd ") and "commit --all --prefix 'cron: '" in parts[1] and parts[2].startswith("git push -q origin"), parts
    return parts[0] + " && " + parts[1], parts[0] + " && " + parts[2]


def test_b8h_the_legacy_cron_lines_snap_line_is_exempt_republishes_only_existing_tips_and_is_named(tmp_path):
    """B8h-3 (DG1 15:18Z): the OLD `grid.py cron install` snap line (grid.cron_lines) is not the cron:crons job, so it is not gated by it: retired, its commit
    half (`grid.py commit --all --prefix 'cron: '`) exits 0 writing no ref, its push half republishes ONLY the tips that already exist (local refs/grid/*
    identical before and after, origin == local, a second run moves nothing), and grid_retired's docstring names `cron_lines` (within 120 chars of 'exempt')."""
    root, env = retired_push_fixture(tmp_path)
    origin = tmp_path / "repo-origin.git"
    log = tmp_path / "snap.log"
    commit_half, push_half = snap_halves(root, env, log)
    before = refs_grid(root.parent)
    assert len(before) >= 3 and git(origin, "for-each-ref", "refs/grid") == ""
    sh = lambda c: subprocess.run(["sh", "-c", c], cwd=root.parent, env=env, capture_output=True, text=True, timeout=120)
    a = sh(commit_half)
    assert a.returncode == 0, (a.returncode, a.stdout[-200:], a.stderr[-300:], log.read_text()[-300:] if log.exists() else "")
    assert refs_grid(root.parent) == before, "the snap line's retired commit half wrote or moved a local refs/grid ref"
    assert RETIRED in log.read_text(), log.read_text()[-300:]
    b = sh(push_half)
    assert b.returncode == 0, (b.returncode, b.stderr[-300:], log.read_text()[-300:])
    assert refs_grid(root.parent) == before and refs_grid(origin) == before, "the push half must republish exactly the existing tips"
    c = sh(commit_half + " && " + push_half.split(" && ", 1)[1])        # the whole line again: nothing moves
    assert c.returncode == 0 and refs_grid(root.parent) == before and refs_grid(origin) == before, (c.returncode, c.stderr[-300:])
    d = subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, sys.argv[1]); import grid; print(grid.grid_retired.__doc__ or '')",
                        str(root.parent / "extensions/agi/bin")], cwd=root.parent, env=env, capture_output=True, text=True, timeout=60)
    assert d.returncode == 0, d.stderr[-300:]
    assert re.search(r"(?is)cron_lines.{0,120}exempt|exempt.{0,120}cron_lines", d.stdout), "grid_retired's docstring must name `cron_lines` as exempt: " + d.stdout[-400:]


# --- B8e: the switch node as RAW TEXT, one row per shape, anchored to crons.load_crons_node ---


def doc(*cad: str, head: str = "crons_live: true") -> str:
    return "---\n" + head + "\ncadences:\n" + "\n".join(cad) + "\n---\n\nBody.\n"


GS = "  grid_sync:"
SIB = ["  branch_push:", "    schedule: 7 * * * *", "    enabled: true"]   # a sibling crons.py validates (an enabled job needs a schedule)
WHOLE = "---\ncrons_live: true\n{}\n---\n\nBody.\n"
SHAPES = {   # name: (raw crons.md text, retired?)  retired == crons.py reads grid_sync.enabled as False
    # the canonical form, its comment / spacing / CRLF forms and the sibling that must not matter
    "plain": (doc(GS, "    every_mins: 5", "    enabled: false", *SIB), True),
    "trailing-comment": (doc(GS, "    enabled: false # x"), True),
    "two-spaces-after-colon": (doc(GS, "    enabled:  false"), True),
    "trailing-spaces": (doc(GS, "    enabled: false   "), True),
    "crlf-line-endings": (doc(GS, "    every_mins: 5", "    enabled: false", *SIB).replace("\n", "\r\n"), True),
    "spaces-only-line": (doc(GS, "    enabled: false", "      "), True),
    "dash-space-first-line": (doc(GS, "    enabled: false").replace("---\n", "--- \n", 1), True),
    "dash-tab-first-line": (doc(GS, "    enabled: false").replace("---\n", "---\t\n", 1), True),   # PyYAML ignores it; the old line scanner did not
    # RE-b6: the YAML 1.1 off spellings are OFF (the applier drops the job): retired
    "False": (doc(GS, "    enabled: False"), True),
    "FALSE": (doc(GS, "    enabled: FALSE"), True),
    "no": (doc(GS, "    enabled: no"), True),
    "No": (doc(GS, "    enabled: No"), True),
    "off": (doc(GS, "    enabled: off"), True),
    "Off": (doc(GS, "    enabled: Off"), True),
    "flow-style": (doc("  grid_sync: {enabled: false}", *SIB), True),
    "crons_live-false": (doc(GS, "    enabled: false", head="crons_live: false"), True),   # the cell itself is what counts
    # the indents are READ by the parser, never assumed
    "cadences-children-at-4": (WHOLE.format("cadences:\n    grid_sync:\n        enabled: false"), True),
    "grid-sync-children-at-3": (doc(GS, "   enabled: false"), True),
    # duplicates: the LAST key wins (PyYAML, as crons.py)
    "duplicate-true-then-false": (doc(GS, "    every_mins: 5", "    enabled: true", "    enabled: false"), True),
    "duplicate-grid-sync-block-false-last": (doc(GS, "    every_mins: 5", GS, "    enabled: false"), True),
    "duplicate-false-then-true": (doc(GS, "    every_mins: 5", "    enabled: false", "    enabled: true"), False),
    "duplicate-grid-sync-block-without-enabled": (doc(GS, "    enabled: false", GS, "    every_mins: 5"), False),
    # RE-b6 (2): after a false block, a LATER declaration of the job (or of `cadences:`) wins and reads on / absent: NOT retired
    "after-false-grid-sync-flow-true": (doc(GS, "    enabled: false", "  grid_sync: {enabled: true}"), False),
    "after-false-grid-sync-flow-true-with-cadence": (doc(GS, "    enabled: false", "  grid_sync: {enabled: true, every_mins: 5}"), False),
    "after-false-grid-sync-null": (doc(GS, "    enabled: false", "  grid_sync: ~"), False),
    "after-false-cadences-empty": (WHOLE.format("cadences:\n  grid_sync:\n    enabled: false\ncadences: {}"), False),
    "after-false-cadences-flow-true": (WHOLE.format("cadences:\n  grid_sync:\n    enabled: false\ncadences: {grid_sync: {enabled: true}}"), False),
    "after-false-cadences-flow-true-with-cadence": (WHOLE.format("cadences:\n  grid_sync:\n    enabled: false\ncadences: {grid_sync: {enabled: true, every_mins: 5}}"), False),
    "after-false-quoted-key-redeclared": (doc(GS, "    enabled: false", '  "grid_sync":', "    every_mins: 5", "    enabled: true"), False),
    "after-false-space-before-colon-redeclared": (doc(GS, "    enabled: false", "  grid_sync :", "    every_mins: 5", "    enabled: true"), False),
    "second-cadences-block-without-grid-sync": (WHOLE.format("cadences:\n  grid_sync:\n    enabled: false\ncadences:\n  branch_push:\n    schedule: 7 * * * *"), False),
    # on / yes / absent
    "true": (doc(GS, "    every_mins: 5", "    enabled: true"), False),
    "yes": (doc(GS, "    every_mins: 5", "    enabled: yes"), False),
    "flow-style-true": (doc("  grid_sync: {enabled: true, every_mins: 5}"), False),
    "missing-grid-sync": (doc(*SIB), False),
    "cadences-null": (WHOLE.format("cadences:"), False),
    "not-top-level-cadences": (WHOLE.format("other:\n  cadences:\n    grid_sync:\n      enabled: false"), False),
    "crons_live-false-grid-sync-on": (doc(GS, "    every_mins: 5", "    enabled: true", head="crons_live: false"), False),   # crons_live false drops the job in the applier, the gate stays OPEN
    "box-gated-grid-sync-on": (doc(GS, "    every_mins: 5", "    enabled: true", "    box: some-other-box", '    why_box: "a gated job says why"'), False),   # a box gate drops the job on this box, the gate stays OPEN
    "sibling-job-false-after": (doc(GS, "    every_mins: 5", "    enabled: true", "  branch_push:", "    schedule: 7 * * * *", "    enabled: false"), False),
    "sibling-job-false-before": (doc("  branch_push:", "    schedule: 7 * * * *", "    enabled: false", GS, "    every_mins: 5", "    enabled: true"), False),
    "mirror-nested-false": (doc(GS, "    every_mins: 5", "    enabled: true", "    mirror:", "      enabled: false"), False),
    "mirror-nested-false-no-own-enabled": (doc(GS, "    every_mins: 5", "    mirror:", "      enabled: false"), False),
    # crons.py REFUSES the whole node (any exception = NOT retired): a malformed cell, a spelling YAML does not call a bool, a node it cannot validate elsewhere
    "null": (doc(GS, "    every_mins: 5", "    enabled: ~"), False),
    "empty": (doc(GS, "    every_mins: 5", "    enabled:"), False),
    "zero": (doc(GS, "    every_mins: 5", "    enabled: 0"), False),
    "quoted-false": (doc(GS, "    every_mins: 5", '    enabled: "false"'), False),
    "single-letter-n": (doc(GS, "    enabled: n"), False),
    "no-space-after-colon": (doc(GS, "    enabled:false"), False),
    "hash-without-space": (doc(GS, "    enabled: false#x"), False),
    "list-item": (doc(GS, "    - enabled: false"), False),
    "block-scalar-body": (doc("  grid_sync: |", "    enabled: false"), False),
    "tab-indent": (doc(GS, "\tenabled: false"), False),
    "tab-after-colon": (doc(GS, "    enabled:\tfalse"), False),
    "space-then-tab-before-false": (doc(GS, "    enabled: \tfalse"), False),
    "nbsp-after-colon": (doc(GS, "    enabled: false"), False),
    "trailing-nbsp": (doc(GS, "    enabled: false "), False),
    "trailing-tab": (doc(GS, "    enabled: false\t"), False),
    "tab-only-line": (doc(GS, "    enabled: false", "\t"), False),
    "nbsp-only-line": (doc(GS, "    enabled: false", " "), False),
    "dash-nbsp-first-line": (doc(GS, "    enabled: false").replace("---\n", "--- \n", 1), False),
    "bom-file": ("﻿" + doc(GS, "    enabled: false"), False),
    "leading-blank-line": ("\n" + doc(GS, "    enabled: false"), False),
    "no-closing-dashes": ("---\ncrons_live: true\ncadences:\n  grid_sync:\n    enabled: false\n", False),
    "no-crons_live": ("---\ncadences:\n  grid_sync:\n    enabled: false\n---\n\nBody.\n", False),
    "crons_live-quoted": (doc(GS, "    enabled: false", head="crons_live: 'true'"), False),
    "unknown-job-without-cmd": (doc(GS, "    enabled: false", "  mystery:", "    every_mins: 5"), False),
}


@pytest.mark.parametrize("shape", sorted(SHAPES))
def test_b8e_raw_text_shape(tmp_path, shape):
    text, retired = SHAPES[shape]
    root, env = seeded(tmp_path)
    (root / "nodes" / ".geometry" / "crons.md").write_bytes(text.encode())
    before = refs_grid(root.parent)
    a = grid_py(root, env, "commit", "--all")
    b = grid_py(root, env, "push-changed")
    assert a.returncode == 0 and b.returncode == 0, (a.stderr[-300:], b.stderr[-300:])
    assert "Traceback" not in a.stderr + b.stderr, (a.stderr[-300:], b.stderr[-300:])
    if retired:
        assert RETIRED in a.stdout and RETIRED in b.stdout, (shape, a.stdout[-200:], b.stdout[-200:])
        assert refs_grid(root.parent) == before, f"{shape}: retired, yet refs/grid moved"
        assert git(tmp_path / "repo-origin.git", "for-each-ref", "refs/grid") == ""
    else:
        assert RETIRED not in a.stdout and RETIRED not in b.stdout, (shape, a.stdout[-200:], b.stdout[-200:])
        assert refs_grid(root.parent) != before, f"{shape}: NOT retired, so the edit must be versioned"


def crons_says(tmp_path: Path, text: str) -> bool:
    """What the applier itself concludes: `load_crons_node(...)["jobs"]["grid_sync"]["enabled"] is False`; any error = False."""
    p = tmp_path / "anchor" / "nodes" / ".geometry"
    p.mkdir(parents=True, exist_ok=True)
    (p / "crons.md").write_bytes(text.encode())
    try:
        return crons.load_crons_node(tmp_path / "anchor")["jobs"]["grid_sync"]["enabled"] is False
    except Exception:
        return False


@pytest.mark.parametrize("shape", sorted(SHAPES))
def test_b8e_the_table_is_crons_anchored(tmp_path, shape):
    """The expectations are not opinion: `crons.load_crons_node` reads `grid_sync.enabled` as False exactly where the table says retired."""
    text, retired = SHAPES[shape]
    assert crons_says(tmp_path, text) is retired, shape


def test_b8e_the_table_has_both_verdicts_in_depth():
    """A table of all-N (or all-Y) shapes would pass a gate that is constant: both sides are well populated."""
    assert sum(1 for _, r in SHAPES.values() if r) >= 20 and sum(1 for _, r in SHAPES.values() if not r) >= 30


# --- B8f: the REAL node, and `import yaml` missing ---


def test_b8f_the_real_node_with_only_grid_sync_off_is_retired_unflipped_is_not(tmp_path):
    """The flip's own acceptance: the trunk's live crons.md (crons.py must read it) with ONLY `grid_sync.enabled: false` set."""
    live = LIVE_NODE.read_text()
    m = re.search(r"^(  grid_sync:\n(?:    .*\n)*?    enabled: )true$", live, re.M)
    assert m, "the live node no longer spells `grid_sync:` ... `enabled: true` on its own line: re-pin this row"
    flipped = live[:m.start()] + m[1] + "false" + live[m.end():]
    assert len(live.splitlines()) == len(flipped.splitlines()) and [a for a, b in zip(live.splitlines(), flipped.splitlines()) if a != b] == [m[0].splitlines()[-1]], "exactly one line differs"
    assert crons_says(tmp_path / "live", live) is False and crons_says(tmp_path / "flip", flipped) is True, "crons.py must read today's node (a refusal makes the flip impossible)"
    for text, retired in ((flipped, True), (live, False)):
        root, env = seeded(tmp_path / ("flip" if retired else "live"))
        before = refs_grid(root.parent)
        (root / "nodes" / ".geometry" / "crons.md").write_text(text)
        a = grid_py(root, env, "commit", "--all")
        b = grid_py(root, env, "push-changed")
        assert a.returncode == 0 and b.returncode == 0 and "Traceback" not in a.stderr + b.stderr, (a.stderr[-300:], b.stderr[-300:])
        assert (RETIRED in a.stdout and RETIRED in b.stdout) is retired, (retired, a.stdout[-200:])
        assert (refs_grid(root.parent) == before) is retired, f"retired={retired}: refs/grid {'moved' if retired else 'did not move'}"


YAML_GONE = """
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import grid
root = Path(sys.argv[2])
witness = grid.grid_retired(root)                # yaml present: the node says OFF, so the same call is True (the row can fail)
sys.modules.pop("crons", None)
sys.modules["yaml"] = None                       # an interpreter without PyYAML: `import yaml` raises inside crons
print(witness, grid.grid_retired(root))
"""


def test_b8f_import_yaml_missing_is_not_retired_and_no_traceback(tmp_path):
    """`sys.modules['yaml'] = None` while the gate runs (grid.py itself imports yaml elsewhere, so the cell is blanked AFTER grid loaded): the
    gate cannot read the cell, so it answers False (not retired, no exception escapes), where the same call a line earlier answered True."""
    root, env = seeded(tmp_path)
    set_grid_sync(root, "off")
    r = subprocess.run([sys.executable, "-c", YAML_GONE, str(root.parent / "extensions/agi/bin"), str(root)],
                       cwd=root.parent, env=env, capture_output=True, text=True, timeout=60)
    assert r.returncode == 0 and "Traceback" not in r.stderr, (r.returncode, r.stderr[-500:])
    assert r.stdout.split() == ["True", "False"], (r.stdout, "witness True with yaml, False without")


# --- B8b: the rotate.py writer FUNCTIONS are the three named ones ---

ROTATE_PY = Path(os.environ.get("ROTATE_PY") or BIN / "rotate.py")
ALLOWED_ROTATE_WRITERS = {"_grid_commit", "_button_down", "_push"}


def grid_writers(src: str) -> set[str]:
    """Functions (nested ones included, each judged on its OWN statements) that run
    `grid.py commit` (the strings 'grid.py', 'commit' and '--all' in one function) or hand a
    `grid_spec` to a call (the refs/grid push)."""
    out = set()
    for fn in ast.walk(ast.parse(src)):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        consts, names = set(), set()
        stack = [n for n in fn.body if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        while stack:
            n = stack.pop()
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                consts.add(n.value)
            if isinstance(n, ast.Name):
                names.add(n.id)
            for c in ast.iter_child_nodes(n):
                if not isinstance(c, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                    stack.append(c)
        if ("grid.py" in consts and "commit" in consts) or "grid_spec" in names:
            out.add(fn.name)
    return out


def test_b8b_rotate_py_has_no_fourth_refs_grid_writer():
    found = grid_writers(ROTATE_PY.read_text())
    assert found == ALLOWED_ROTATE_WRITERS, (
        f"rotate.py grid writers {sorted(found)}, named {sorted(ALLOWED_ROTATE_WRITERS)}: "
        f"extra {sorted(found - ALLOWED_ROTATE_WRITERS)}, missing {sorted(ALLOWED_ROTATE_WRITERS - found)}")


SYNTH = """
def _grid_commit():
    run([py, p.with_name("grid.py"), "commit", "--all"])
def outer():
    def _push():
        git("push", "origin", grid_spec)
def reader():
    run([py, p.with_name("grid.py"), "versions", "x"])
def other():
    return 1
"""


def test_b9_the_scanner_names_the_writers_sees_a_fourth_and_ignores_a_reader():
    assert grid_writers(SYNTH) == {"_grid_commit", "_push"}
    fourth = SYNTH + "\ndef _sneaky():\n    run([py, p.with_name('grid.py'), 'commit', '--all'])\n"
    assert grid_writers(fourth) == {"_grid_commit", "_push", "_sneaky"}
    pushing = SYNTH + "\ndef sneaky():\n    git('push', 'origin', grid_spec)\n"
    assert "sneaky" in grid_writers(pushing)
