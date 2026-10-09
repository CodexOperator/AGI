"""D3 falsifier lane (goal:g7.16.1.11.22, doc:rse-d3-legacy v2; DG2 writes the lane FIRST, DG5 builds `extensions/agi/bin/legacy.py` and the viewport suffix).

A node's legacy mark is COMPUTED from the bytes: the node FILE's own first-parent git history (renames followed, so a retire move keeps it) plus D1's `nest.members()` / `nest.fm()`. Never a front-matter field, never a grid ref. HERMETIC: scratch git repos only (empty HOME, no GIT_CONFIG), never the box's MAIN.

PINNED INTERFACE (DG5 may counter-propose; the rows are then re-cut):
  legacy.mark(rev, season, path) -> "legacy" | "-" | "?"        the doc's function byte for byte ("?" = no history for the path at rev; `season` is a str)
  legacy.label(rev, season, path) -> "" | "[legacy]" | "[legacy ⊃k]" | "[⊃k]"      the string viewport prints; k = |members(N)| - 1 (a retired member still counts)
  Both run git in the CURRENT DIRECTORY (the tests chdir into the scratch repo); `path` is the node file's path AT rev.
  viewport.py (CLI, `--project <repo>/.agi`, run with cwd = the repo) marks every node line of `--emit human` and `--emit llm` with the SAME label string, computed at HEAD with
  season = `current_season` of `.agi/nodes/.geometry/ladder.md` at HEAD; `--verify` still exits 0.

The four shapes: `[legacy]` (k = 0, not graphed since the entry) · `[legacy ⊃k]` (k > 0, not graphed) · `[⊃k]` (k > 0, graphed) · none (k = 0, graphed). ENTRY = the NEWEST of the path's first commit, the commit that ADDS `nest:`, and the commit after which `season:` equals the current season; GRAPHED = a commit above the entry after which `parents:` GAIN a `goal:` id absent at the entry (or, when the entry is the first commit, the node was minted with a goal parent). "Gain", not "includes".

Rows: l2-* the doc's 11-case table (each case judged AT its commit) + carry / retire-move / hand-set-field cases · l1-* the mark equals v1's grid-ref shell rule (quoted from the doc's first version) for every node that has a grid ref · neg-* no `^legacy:` field in any node file, no `refs/grid` in legacy.py (+ witnesses that the greps can hit) · l3-* the viewport CLI. Env: LEGACY_BIN=<dir holding legacy.py, nest.py, viewport.py and the rest of bin> (default: this tree's extensions/agi/bin); mutants are such dirs.

v2 (DG1 17:55Z, DG5's survivors M1 / M2 and the --verify ruling): l4-* the per-user CACHE (${XDG_CACHE_HOME:-~/.cache}/agi/legacy.tsv) is invalidated by a NEW COMMIT on a node (l4-a) and by a new SEASON with no commit on any node (l4-b); an unwritable HOME / cache path still renders the mark (l4-c); `viewport.py --verify` fails when ONE of the two views drops or alters the mark and passes on the clean tree (l4-d: a patched renderer in a scratch copy of the bin dir; env LEGACY_BIN points the lane at the code under test).
"""
from __future__ import annotations

import importlib.util
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve()
BIN = Path(os.environ.get("LEGACY_BIN") or HERE.parents[1] / "bin")
LEGACY = BIN / "legacy.py"
VIEWPORT = BIN / "viewport.py"
MARK_RE = re.compile(r"\[(?:legacy(?: ⊃\d+)?|⊃\d+)\]")


def mint(i: int) -> str:
    return f"{i:032x}"


def node_text(nid: str, typ: str, i: int, parents: list[str], **extra) -> str:
    ps = "parents: []" if not parents else "parents:\n" + "\n".join(f"  - {p}" for p in parents)
    ex = "".join(f"{k}: {v}\n" for k, v in extra.items())
    return f"---\nid: {nid}\nmint_id: {mint(i)}\ntype: {typ}\n{ps}\n{ex}---\nbody\n"


@pytest.fixture(autouse=True)
def _home(tmp_path, monkeypatch):
    h = tmp_path / "home"
    h.mkdir()
    monkeypatch.setenv("HOME", str(h))
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg-cache"))   # legacy.cache_path() prefers it: without this an in-process row writes the USER's real ${XDG_CACHE_HOME}/agi/legacy.v1.tsv
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/dev/null")
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", "/dev/null")
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        monkeypatch.delenv(k, raising=False)


class Repo:
    """A scratch repo whose commits are made one at a time, each returning its sha."""

    def __init__(self, tmp_path: Path, name: str):
        self.dir = tmp_path / name
        self.dir.mkdir(parents=True)
        self.n = 0
        self.g("init", "-q", "-b", "trunk")
        (self.dir / ".agi").mkdir()
        (self.dir / ".agi" / "config.json").write_text("{}")

    def g(self, *a, inp=None, env=None) -> str:
        r = subprocess.run(["git", "-C", str(self.dir), *a], capture_output=True, text=True, input=inp,
                           env={**os.environ, **(env or {})})
        if r.returncode != 0:
            raise RuntimeError(f"git {a}: {r.stderr}")
        return r.stdout.strip()

    def write(self, rel: str, text: str) -> None:
        p = self.dir / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def commit(self, msg: str, *paths: str, staged: bool = False) -> str:
        self.n += 1
        when = f"2026-01-{self.n % 28 + 1:02d}T{self.n // 28:02d}:00:00Z"
        env = {"GIT_COMMITTER_DATE": when, "GIT_AUTHOR_DATE": when, "GIT_COMMITTER_NAME": "t",
               "GIT_COMMITTER_EMAIL": "t@t", "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t"}
        if not staged:
            self.g("add", "-A", "--", *(paths or (".",)))
        self.g("commit", "-q", "-m", msg, env=env)
        return self.g("rev-parse", "HEAD")

    def edit(self, rel: str, text: str, msg: str) -> str:
        self.write(rel, text)
        return self.commit(msg, rel)

    def mv(self, a: str, b: str, msg: str) -> str:
        (self.dir / b).parent.mkdir(parents=True, exist_ok=True)
        self.g("mv", a, b)
        return self.commit(msg, staged=True)


def load_legacy():
    assert LEGACY.exists(), f"{LEGACY} does not exist yet (the build is DG5's)"
    sys.path.insert(0, str(BIN))
    spec = importlib.util.spec_from_file_location("legacy_under_test", LEGACY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ====================================================================================================
# l2: the doc's 11-case table (judged at each case's own commit) -- ENTRY, gain-not-include, minted-through-a-goal, nest, retire move, members()
# ====================================================================================================

B = ".agi/nodes/build"
G = ".agi/nodes/goal"

def build_table(tmp_path: Path) -> tuple[Repo, list]:
    r = Repo(tmp_path, "table")
    cs = []

    def case(name, sha, season, path, expect, why):
        cs.append((name, sha, season, path, expect, why))

    x = lambda ps, **kw: node_text("build:x", "build", 1, ps, **kw)
    case("C1", r.edit(f"{B}/x.md", x(["mvp:engine-bin"], season=2), "C1"), "2", f"{B}/x.md", "[legacy]", "a scanned node, never graphed")
    case("C2", r.edit(f"{B}/x.md", x(["mvp:engine-bin", "goal:g9"], season=2), "C2"), "2", f"{B}/x.md", "", "a goal parent GAINED above the entry: graphed, k = 0 = no mark")
    case("C3", r.edit(f"{B}/y.md", node_text("build:y", "build", 2, ["goal:g9", "mvp:engine-bin"], season=2), "C3"), "2", f"{B}/y.md", "",
         "minted THROUGH a goal (the entry is the first commit): graphed from its first commit")
    case("C4", r.edit(f"{B}/x.md", x(["mvp:engine-bin", "goal:g9"], season=3), "C4"), "3", f"{B}/x.md", "[legacy]",
         "the season carry is a new ENTRY: x keeps its season-2 goal parent, which is 'include', not 'gain'")
    case("C5", r.edit(f"{B}/x.md", x(["mvp:engine-bin", "goal:g9"], season=3, note="typo"), "C5"), "3", f"{B}/x.md", "[legacy]", "an unrelated edit does not graph")
    case("C6", r.edit(f"{B}/x.md", x(["mvp:engine-bin", "goal:g9", "goal:s3a"], season=3, note="typo"), "C6"), "3", f"{B}/x.md", "", "a goal parent gained after the carry")
    r.write(f"{G}/a.md", node_text("goal:a", "goal", 3, ["goal:root"], season=3)); r.commit("goal a", f"{G}/a.md")
    r.write(f"{G}/b.md", node_text("goal:b", "goal", 4, ["goal:a"], season=3)); r.commit("goal b", f"{G}/b.md")
    r.write(f"{B}/z.md", node_text("build:z", "build", 5, ["goal:a"], season=3)); r.commit("build z", f"{B}/z.md")
    a = lambda ps, **kw: node_text("goal:a", "goal", 3, ps, **kw)
    case("C7", r.edit(f"{G}/a.md", a(["goal:root"], season=3, nest="subtree"), "C7"), "3", f"{G}/a.md", "[legacy ⊃2]",
         "the commit that ADDS nest: is the entry; contains b and z")
    case("C8", r.edit(f"{G}/a.md", a(["goal:root", "goal:s3b"], season=3, nest="subtree"), "C8"), "3", f"{G}/a.md", "[⊃2]", "a goal gained after the nest: contains 2 AND worked on")
    case("C9", r.mv(f"{B}/z.md", ".agi/nodes/deprecated/build/z.md", "C9"), "3", f"{G}/a.md", "[⊃2]",
         "a RETIRED member still counts in k (it is still a file)")
    r.write(f"{G}/c.md", node_text("goal:c", "goal", 6, ["goal:b"], season=3))
    case("C10", r.commit("C10", f"{G}/c.md"), "3", f"{G}/a.md", "[⊃3]", "the subtree descends to a grandchild")
    r.write(f"{G}/b.md", node_text("goal:b", "goal", 4, ["goal:a"], season=3, nest="[doc:q]"))
    r.write(".agi/nodes/doc/q.md", node_text("doc:q", "doc", 7, ["goal:zz"], season=3))
    case("C11", r.commit("C11", f"{G}/b.md", ".agi/nodes/doc/q.md"), "3", f"{G}/a.md", "[⊃3]",
         "b carries its own nest: the descent stops at b and b expands its list: a b z q (c is no longer reached)")
    return r, cs


@pytest.mark.parametrize("cid", [f"C{i}" for i in range(1, 12)])
def test_l2_the_doc_table_each_case_judged_at_its_own_commit(tmp_path, monkeypatch, cid):
    """The 11 scratch cases of doc:rse-d3-legacy v2 (inputs -> expected), one commit per row; the mark of the named node AT that commit's sha. The label
    AND the doc's `mark` (legacy | -) are both pinned: `mark` is `legacy` exactly when the label starts with `[legacy`."""
    repo, cases = build_table(tmp_path)
    name, sha, season, path, expect, why = next(c for c in cases if c[0] == cid)
    monkeypatch.chdir(repo.dir)
    L = load_legacy()
    got = L.label(sha, season, path)
    assert got == expect, f"{cid} ({why}): label {got!r}, want {expect!r}"
    assert L.mark(sha, season, path) == ("legacy" if expect.startswith("[legacy") else "-"), (cid, L.mark(sha, season, path))


def test_l2_a_member_graphed_later_does_not_clear_its_containers_mark(tmp_path, monkeypatch):
    """Container a (nest: subtree, entry = the collapse) holds b and z. Member b then GAINS a goal parent (a commit on b's file only), and z is edited: a still
    reads `[legacy ⊃2]`, b reads none. The rule reads only the container's own file."""
    repo = Repo(tmp_path, "member")
    repo.write(f"{G}/a.md", node_text("goal:a", "goal", 3, ["goal:root"], season=3)); repo.commit("a", f"{G}/a.md")
    repo.write(f"{G}/b.md", node_text("goal:b", "goal", 4, ["goal:a"], season=3)); repo.commit("b", f"{G}/b.md")
    repo.write(f"{B}/z.md", node_text("build:z", "build", 5, ["goal:a"], season=3)); repo.commit("z", f"{B}/z.md")
    repo.edit(f"{G}/a.md", node_text("goal:a", "goal", 3, ["goal:root"], season=3, nest="subtree"), "collapse a")
    repo.edit(f"{G}/b.md", node_text("goal:b", "goal", 4, ["goal:a", "goal:g5"], season=3), "b gains a goal")
    sha = repo.edit(f"{B}/z.md", node_text("build:z", "build", 5, ["goal:a"], season=3, note="edited"), "z edited")
    monkeypatch.chdir(repo.dir)
    L = load_legacy()
    got = (L.label(sha, "3", f"{G}/a.md"), L.label(sha, "3", f"{G}/b.md"))
    assert got == ("[legacy ⊃2]", ""), got


def test_l2_a_carried_node_with_a_season_2_goal_reads_legacy_until_a_NEW_goal_is_gained(tmp_path, monkeypatch):
    """w is minted through goal:g9 in season 2 (graphed), the season-3 carry (ONE one-node commit setting season:) makes it `[legacy]`, an unrelated edit keeps it,
    a NEW goal parent graphs it again. ('parents include a goal' would read the first unrelated edit as graphed.)"""
    repo = Repo(tmp_path, "carry")
    w = lambda ps, **kw: node_text("build:w", "build", 1, ps, **kw)
    p = f"{B}/w.md"
    s1 = repo.edit(p, w(["goal:g9", "mvp:e"], season=2), "minted through a goal")
    s2 = repo.edit(p, w(["goal:g9", "mvp:e"], season=3), "carry s2->s3")
    s3 = repo.edit(p, w(["goal:g9", "mvp:e"], season=3, note="x"), "unrelated edit")
    s4 = repo.edit(p, w(["goal:g9", "goal:g10", "mvp:e"], season=3, note="x"), "gains goal:g10")
    monkeypatch.chdir(repo.dir)
    L = load_legacy()
    got = [L.label(s1, "2", p), L.label(s2, "3", p), L.label(s3, "3", p), L.label(s4, "3", p)]
    assert got == ["", "[legacy]", "[legacy]", ""], got


def test_l2_a_goal_gained_then_dropped_on_a_merged_branch_does_not_graph_the_node(tmp_path, monkeypatch):
    """The mark reads FIRST-PARENT history (legacy.py:17, doc:rse-d3-legacy x3). w is minted in season 3 with no goal parent; a side branch GAINS goal:g9 then DROPS it
    again (and edits w's `omega`), trunk edits w's `alpha`, and the branch is merged --no-ff. The merge differs from BOTH parents (git cannot simplify the side branch away),
    so only --first-parent keeps the branch's own commits out of the walk: w reads `legacy`. Without it the gain commit joins the walk and w reads `-` (graphed)."""
    repo = Repo(tmp_path, "merge")
    p = f"{B}/w.md"
    w = lambda ps, **kw: node_text("build:w", "build", 1, ps, **kw)
    ex = lambda alpha, omega: dict(alpha=alpha, m1="m", m2="m", m3="m", omega=omega)
    base = repo.edit(p, w(["mvp:e"], season=3, **ex(1, 1)), "minted, no goal parent")
    repo.g("checkout", "-q", "-b", "side")
    gain = repo.edit(p, w(["mvp:e", "goal:g9"], season=3, **ex(1, 1)), "side: gains goal:g9")
    repo.edit(p, w(["mvp:e"], season=3, **ex(1, 2)), "side: drops goal:g9, edits omega")
    repo.g("checkout", "-q", "trunk")
    repo.edit(p, w(["mvp:e"], season=3, **ex(2, 1)), "trunk: edits alpha")
    env = {"GIT_COMMITTER_DATE": "2026-02-01T00:00:00Z", "GIT_AUTHOR_DATE": "2026-02-01T00:00:00Z", "GIT_COMMITTER_NAME": "t",
           "GIT_COMMITTER_EMAIL": "t@t", "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t"}
    repo.g("merge", "-q", "--no-ff", "-m", "merge side", "side", env=env)
    sha = repo.g("rev-parse", "HEAD")
    assert len(repo.g("rev-list", "--parents", "-n1", sha).split()) == 3, "the fixture must end in a real two-parent merge"
    assert gain in repo.g("log", "--format=%H", sha, "--", p).split(), "the fixture must be a topology where the branch's gain commit is on the walk without --first-parent"
    monkeypatch.chdir(repo.dir)
    L = load_legacy()
    got = (L.mark(sha, "3", p), L.label(sha, "3", p))
    assert got == ("legacy", "[legacy]"), got
    assert base != sha


@pytest.mark.parametrize("order", ["nest-then-carry", "carry-then-nest"])
def test_l2_the_entry_is_the_NEWEST_of_the_nest_commit_and_the_season_carry(tmp_path, monkeypatch, order):
    """A container d with one member m. nest-then-carry: minted (season 2), `nest:` added, a goal GAINED, then the season-3 carry: the carry is the newest entry, so the
    gain before it is history -> `[legacy ⊃1]`. carry-then-nest: minted (2), carried (3), a goal gained, then `nest:` added: the nest is the newest entry -> `[legacy ⊃1]`.
    (An entry that keeps the FIRST match instead of the newest reads `[⊃1]` in both.)"""
    repo = Repo(tmp_path, order)
    repo.write(f"{G}/m.md", node_text("goal:m", "goal", 2, ["goal:d"], season=2)); 
    d = lambda ps, **kw: node_text("goal:d", "goal", 1, ps, **kw)
    p = f"{G}/d.md"
    repo.write(p, d(["goal:root"], season=2)); repo.commit("d and m", p, f"{G}/m.md")
    if order == "nest-then-carry":
        repo.edit(p, d(["goal:root"], season=2, nest="subtree"), "nest")
        repo.edit(p, d(["goal:root", "goal:g1"], season=2, nest="subtree"), "gain")
        sha = repo.edit(p, d(["goal:root", "goal:g1"], season=3, nest="subtree"), "carry")
    else:
        repo.edit(p, d(["goal:root"], season=3), "carry")
        repo.edit(p, d(["goal:root", "goal:g1"], season=3), "gain")
        sha = repo.edit(p, d(["goal:root", "goal:g1"], season=3, nest="subtree"), "nest")
    monkeypatch.chdir(repo.dir)
    assert load_legacy().label(sha, "3", p) == "[legacy ⊃1]", load_legacy().label(sha, "3", p)


def test_l2_a_retire_move_keeps_the_history_so_the_carry_entry_survives_it(tmp_path, monkeypatch):
    """v is minted through a goal (season 2), carried to season 3, then RETIRED by `git mv` to deprecated/: the mark at the new path is still `[legacy]`
    (the history is followed through the rename; with only the move commit visible the first-commit-with-a-goal reading would say graphed)."""
    repo = Repo(tmp_path, "move")
    v = lambda **kw: node_text("build:v", "build", 1, ["goal:g9", "mvp:e"], **kw)
    p, q = f"{B}/v.md", ".agi/nodes/deprecated/build/v.md"
    repo.edit(p, v(season=2), "minted")
    repo.edit(p, v(season=3), "carry")
    sha = repo.mv(p, q, "retire")
    monkeypatch.chdir(repo.dir)
    L = load_legacy()
    assert L.label(sha, "3", q) == "[legacy]" and L.mark(sha, "3", q) == "legacy", (L.label(sha, "3", q), L.mark(sha, "3", q))


def test_l2_the_mark_is_never_read_from_a_front_matter_field(tmp_path, monkeypatch):
    """A hand-set `legacy:` cell must not matter: h1 (never graphed) carries `legacy: graphed`, h2 (graphed) carries `legacy: true`; the marks follow the bytes of the history."""
    repo = Repo(tmp_path, "field")
    repo.write(f"{B}/h1.md", node_text("build:h1", "build", 1, ["mvp:e"], season=2, legacy="graphed"))
    repo.write(f"{B}/h2.md", node_text("build:h2", "build", 2, ["goal:g9", "mvp:e"], season=2, legacy="true"))
    sha = repo.commit("two nodes with a hand-set legacy cell", f"{B}/h1.md", f"{B}/h2.md")
    monkeypatch.chdir(repo.dir)
    L = load_legacy()
    assert (L.label(sha, "2", f"{B}/h1.md"), L.label(sha, "2", f"{B}/h2.md")) == ("[legacy]", ""), (L.label(sha, "2", f"{B}/h1.md"), L.label(sha, "2", f"{B}/h2.md"))


def test_l2_a_path_with_no_history_is_a_question_mark(tmp_path, monkeypatch):
    repo = Repo(tmp_path, "nohist")
    sha = repo.edit(f"{B}/x.md", node_text("build:x", "build", 1, ["mvp:e"], season=2), "x")
    monkeypatch.chdir(repo.dir)
    assert load_legacy().mark(sha, "2", f"{B}/nope.md") == "?"


# ====================================================================================================
# l1: the mark equals v1's grid-ref rule for every build node that has a grid ref
# ====================================================================================================

V1 = r"""legacy(){ k=$(git ls-tree -r -d --name-only $1|grep -cE '(^|/)nest/[^/]+$');g=0
 for c in $(git rev-list --first-parent $1);do s=$(git log -1 --format=%s $c);case $s in "nest "*|"carry "*)break;;esac
  git log -1 --format=%b $c|grep -q '^Parent-Mint-Id: [^ ]* goal:'&&{ g=1;break;};done
 [ $g = 1 ]&&m=||m=legacy;[ $k -gt 0 ]&&m="${m:+$m }⊃$k";echo "${m:--}";}"""


def grid_version(repo: Repo, i: int, text: str, parents: list[str], n: int) -> None:
    """One grid.py-shaped version of node i: tree = node.md, body = a `Parent-Mint-Id: <mint> <parent id>` line per parent, on refs/grid/node/<mint>."""
    blob = repo.g("hash-object", "-w", "--stdin", inp=text)
    tree = repo.g("mktree", inp=f"100644 blob {blob}\tnode.md\n")
    ref = f"refs/grid/node/{mint(i)}"
    prev = repo.g("rev-parse", "-q", "--verify", ref) if subprocess.run(["git", "-C", str(repo.dir), "rev-parse", "-q", "--verify", ref], capture_output=True).returncode == 0 else ""
    body = "\n".join(f"Parent-Mint-Id: {mint(900 + k)} {p}" for k, p in enumerate(parents))
    when = f"2026-02-{n % 28 + 1:02d}T00:00:00Z"
    env = {"GIT_COMMITTER_DATE": when, "GIT_AUTHOR_DATE": when, "GIT_COMMITTER_NAME": "g", "GIT_COMMITTER_EMAIL": "g@g", "GIT_AUTHOR_NAME": "g", "GIT_AUTHOR_EMAIL": "g@g"}
    c = repo.g("commit-tree", tree, *(["-p", prev] if prev else []), "-m", f"v{n}", "-m", body, env=env)
    repo.g("update-ref", ref, c)


def build_l1(tmp_path: Path):
    r = Repo(tmp_path, "l1")
    ver: dict = {}

    def put(i, nid, parents, path, **kw):
        t = node_text(nid, "build", i, parents, **kw)
        ver[i] = ver.get(i, 0) + 1
        r.edit(path, t, f"{nid} v{ver[i]}")
        if i != 6:                                            # n6 has NO grid ref
            grid_version(r, i, t, parents, ver[i])

    P = lambda n: f"{B}/n{n}.md"
    put(1, "build:n1", ["mvp:e"], P(1))                                                   # scanned, never graphed
    put(2, "build:n2", ["mvp:e"], P(2)); put(2, "build:n2", ["mvp:e", "goal:g9"], P(2))   # a goal-made version later
    put(3, "build:n3", ["goal:g9", "mvp:e"], P(3))                                        # minted through a goal
    put(4, "build:n4", ["mvp:e"], P(4)); put(4, "build:n4", ["mvp:e"], P(4), note="a"); put(4, "build:n4", ["mvp:e"], P(4), note="b")   # edits only
    put(5, "build:n5", ["mvp:e"], P(5)); put(5, "build:n5", ["mvp:e", "goal:g8"], P(5))
    r.mv(P(5), ".agi/nodes/deprecated/build/n5.md", "retire n5")                          # a retire MOVE: the file history must be followed, the grid ref persists
    put(6, "build:n6", ["goal:g9", "mvp:e"], P(6))                                        # graphed, no ref
    return r, {1: P(1), 2: P(2), 3: P(3), 4: P(4), 5: ".agi/nodes/deprecated/build/n5.md", 6: P(6)}


def test_l1_the_mark_equals_v1s_grid_ref_rule_for_every_node_with_a_grid_ref(tmp_path, monkeypatch):
    """v1's rule (the doc's first version, quoted) run with `sh` over refs/grid/node/<mint> vs `legacy.mark` over the file history: equal for n1..n5 (a scan, a
    goal-made version, minted through a goal, edits only, a goal-made version then a retire MOVE). The fixture holds both outcomes; n6 has no ref and still gets its own mark."""
    repo, paths = build_l1(tmp_path)
    monkeypatch.chdir(repo.dir)
    L = load_legacy()
    v1, v2 = {}, {}
    for i in range(1, 6):
        v1[i] = subprocess.run(["sh", "-c", f"{V1}\nlegacy refs/grid/node/{mint(i)}"], cwd=repo.dir, capture_output=True, text=True).stdout.strip()
        v2[i] = L.mark("HEAD", "2", paths[i])
    assert set(v1.values()) == {"legacy", "-"}, f"the fixture must hold both outcomes: {v1}"
    assert v1 == v2, f"v1 (grid) vs the file-history rule: {v1} vs {v2}"
    assert L.mark("HEAD", "2", paths[6]) == "-"


@pytest.mark.skipif(not os.environ.get("D3_TRUNK"), reason="set D3_TRUNK=<repo> (and D3_TRUNK_REV=<commit>, default HEAD) to compare against every build node with a grid ref in a real checkout (about 2 min for 300 nodes)")
def test_l1_on_the_trunk_every_build_node_with_a_grid_ref_reads_the_same_mark(monkeypatch):
    """v1 reads the node's NEWEST grid ref (the live town-scoped refs/grid/<town>/node/<mint>, not the frozen legacy refs/grid/node/<mint>); the doc measured 297/297 at its
    own commit 06ee5a73e6. The grid keeps moving only while grid sync runs, so judge at D3_TRUNK_REV (the grid's freeze is E2), not at a later HEAD."""
    root = Path(os.environ["D3_TRUNK"])
    rev = os.environ.get("D3_TRUNK_REV", "HEAD")
    monkeypatch.chdir(root)
    L = load_legacy()
    import nest
    nodes = {k: v for k, v in nest.graph(rev).items() if v[1].get("type") == "build"}
    bad, n = [], 0
    for nid, (p, d) in sorted(nodes.items()):
        mi = d.get("mint_id")
        refs = subprocess.run(["git", "for-each-ref", "--sort=-committerdate", "--format=%(refname)", f"refs/grid/*/node/{mi}", f"refs/grid/node/{mi}"], capture_output=True, text=True).stdout.split()
        if not refs:
            continue
        n += 1
        v1 = subprocess.run(["sh", "-c", f"{V1}\nlegacy {refs[0]}"], capture_output=True, text=True).stdout.strip()
        if v1 != L.mark(rev, "2", p):
            bad.append((nid, v1))
    assert n > 0 and bad == [], f"{len(bad)} of {n} build nodes with a grid ref disagree: {bad[:5]}"


# ====================================================================================================
# neg: the mark is never a field, the rule reads no grid ref
# ====================================================================================================


def grep_field(repo_dir: Path) -> list[str]:
    r = subprocess.run(["git", "-C", str(repo_dir), "grep", "-n", "-E", "^legacy:", "--", ".agi/nodes/*/*.md"], capture_output=True, text=True)
    return r.stdout.splitlines()


def grid_lines(p: Path) -> list[str]:
    return [l for l in p.read_text().splitlines() if "refs/grid" in l]


def test_neg_no_node_file_carries_a_legacy_front_matter_field(tmp_path):
    """`git grep -n -E '^legacy:' -- '.agi/nodes/*/*.md'` has 0 hits in this tree; witness: the same grep hits a scratch repo whose node carries the cell."""
    w = Repo(tmp_path, "witness")
    w.edit(f"{B}/h.md", node_text("build:h", "build", 1, ["mvp:e"], legacy="true"), "a node with the cell")
    assert len(grep_field(w.dir)) == 1, "the grep must be able to hit"
    top = os.environ.get("D3_REPO") or subprocess.run(["git", "-C", str(HERE.parent), "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    assert top, "run inside the repo"
    assert grep_field(Path(top)) == [], grep_field(Path(top))[:5]


def test_neg_the_rule_reads_no_grid_ref(tmp_path):
    """`git grep -n 'refs/grid' -- extensions/agi/bin/legacy.py` is 0 hits (the file is read directly so an untracked file is judged too); witness: the same check hits a file that does."""
    w = tmp_path / "w.py"
    w.write_text("x = 'refs/grid/node/'\n")
    assert len(grid_lines(w)) == 1, "the check must be able to hit"
    assert LEGACY.exists(), f"{LEGACY} does not exist yet"
    assert grid_lines(LEGACY) == [], grid_lines(LEGACY)


# ====================================================================================================
# l3: the viewport CLI -- one render, two readers (goal:g2.19)
# ====================================================================================================

EXPECT = {  # node id -> (title, label at the season-3 tip)
    "goal:root": ("T-root", "[legacy]"),
    "goal:a": ("T-a", "[legacy ⊃2]"),
    "goal:b": ("T-b", ""),
    "goal:g2": ("T-g2", ""),
    "build:x": ("T-x", ""),
    "build:z": ("T-z", "[legacy]"),
}


def build_v(tmp_path: Path) -> Repo:
    """A season-3 tip: everything minted in season 2, ladder says current_season 3; a one-node carry commit per node; goal:a collapsed (nest: subtree);
    member b and build:x then gain goal:g2 (minted in season 3); member z is RETIRED by a move."""
    r = Repo(tmp_path, "vp")
    spec = [("goal:root", "goal", 1, []), ("goal:a", "goal", 2, ["goal:root"]), ("goal:b", "goal", 3, ["goal:a"]),
            ("build:z", "build", 4, ["goal:a"]), ("build:x", "build", 5, ["goal:root"])]
    pth = lambda nid: f".agi/nodes/{nid.split(':')[0]}/{nid.split(':')[1]}.md"
    txt = {nid: dict(typ=typ, i=i, ps=ps) for nid, typ, i, ps in spec}

    def w(nid, season, **kw):
        s = txt[nid]
        r.write(pth(nid), node_text(nid, s["typ"], s["i"], s["ps"], title=f'"T-{nid.split(":")[1]}"', season=season, **kw))

    r.write(".agi/nodes/.geometry/ladder.md", node_text("config:ladder", "config", 20, [], current_season=2))
    for nid, *_ in spec:
        w(nid, 2)
    r.commit("season 2 tip")
    r.edit(".agi/nodes/.geometry/ladder.md", node_text("config:ladder", "config", 20, [], current_season=3), "ladder: season 3")
    for nid, *_ in spec:                                                       # D2's carry: ONE one-node commit per node
        w(nid, 3)
        r.commit(f"carry {nid}", pth(nid))
    w("goal:a", 3, nest="subtree"); r.commit("collapse goal:a", pth("goal:a"))
    r.write(".agi/nodes/goal/g2.md", node_text("goal:g2", "goal", 6, ["goal:root"], title='"T-g2"', season=3))
    r.commit("goal:g2 minted in season 3", ".agi/nodes/goal/g2.md")
    txt["goal:b"]["ps"] = ["goal:a", "goal:g2"]; w("goal:b", 3); r.commit("b gains goal:g2", pth("goal:b"))
    txt["build:x"]["ps"] = ["goal:root", "goal:g2"]; w("build:x", 3); r.commit("x gains goal:g2", pth("build:x"))
    r.mv(pth("build:z"), ".agi/nodes/deprecated/build/z.md", "retire z")
    return r


def vp(repo: Repo, *args: str) -> subprocess.CompletedProcess:
    assert VIEWPORT.exists(), f"{VIEWPORT} does not exist"
    return subprocess.run([sys.executable, str(VIEWPORT), "--project", str(repo.dir / ".agi"), *args], cwd=repo.dir, capture_output=True, text=True,
                          timeout=180, env={"PATH": "/usr/bin:/bin", "HOME": os.environ["HOME"], "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"})


def line_of(out: str, needle: str) -> str:
    hits = [l for l in out.splitlines() if needle in l]
    assert len(hits) == 1, f"{needle!r}: {len(hits)} lines in {out[-400:]}"
    return hits[0]


def test_l3_verify_exits_0_with_the_mark_on(tmp_path):
    """`viewport.py --verify` exits 0 (PASS) on the season-3 tip fixture AND the mark is really on (not vacuous): `--emit llm` shows the three mark shapes."""
    repo = build_v(tmp_path)
    r = vp(repo, "--verify")
    assert r.returncode == 0 and "PASS" in r.stdout, (r.returncode, r.stdout[-300:], r.stderr[-300:])
    shown = set(MARK_RE.findall(vp(repo, "--emit", "llm").stdout))
    assert {"[legacy]", "[legacy ⊃2]"} <= shown, shown


@pytest.mark.parametrize("nid", list(EXPECT))
def test_l3_the_terminal_and_the_llm_view_print_the_same_mark_string(tmp_path, nid):
    """Per node: the label of the season-3 tip (hand-computed in EXPECT: a carried and collapsed container `[legacy ⊃2]`, a carried untouched node `[legacy]`
    even after a member's / its own retire, a node that gained goal:g2 none) appears on the node's line in `--emit human` AND `--emit llm`, byte for byte;
    a node whose label is none carries no mark in either view."""
    title, want = EXPECT[nid]
    repo = build_v(tmp_path)
    human = line_of(vp(repo, "--emit", "human").stdout, title)
    llm = line_of(vp(repo, "--emit", "llm").stdout, f"`{nid}`")
    hm, lm = MARK_RE.findall(human), MARK_RE.findall(llm)
    assert hm == lm == ([want] if want else []), f"{nid}: human {hm}, llm {lm}, want {[want] if want else []}\n{human!r}\n{llm!r}"


# ====================================================================================================
# l4: the cache is keyed by (path, season, the path's newest commit); an unwritable cache never hides the mark; --verify compares the marks
# ====================================================================================================


def vp2(repo: Repo, *args: str, home: Path | None = None, bin_dir: Path | None = None) -> subprocess.CompletedProcess:
    viewport = (bin_dir or BIN) / "viewport.py"
    assert viewport.exists(), f"{viewport} does not exist"
    return subprocess.run([sys.executable, str(viewport), "--project", str(repo.dir / ".agi"), *args], cwd=repo.dir, capture_output=True, text=True, timeout=180,
                          env={"PATH": "/usr/bin:/bin", "HOME": str(home or os.environ["HOME"]), "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"})


def mark_on(out: str, nid: str) -> list[str]:
    """The mark strings on the llm view's line of `nid` (a list: [] = none)."""
    return MARK_RE.findall(line_of(out, f"`{nid}`"))


def test_l4a_a_new_commit_on_a_node_invalidates_its_cached_mark(tmp_path):
    """ONE HOME, two runs, a commit between: goal:a (carried, collapsed, 2 members) reads `[legacy ⊃2]`; a commit that gains goal:g2 as a PARENT of goal:a makes the SAME node
    read `[⊃2]` (graphed since the entry) on the second run. A cache hit that ignores the path's newest-commit key keeps the stale `[legacy ⊃2]` (DG5's M1)."""
    repo = build_v(tmp_path)
    first = vp2(repo, "--emit", "llm")
    assert first.returncode == 0, first.stderr[-300:]
    assert mark_on(first.stdout, "goal:a") == ["[legacy ⊃2]"], first.stdout[-400:]
    repo.edit(".agi/nodes/goal/a.md", node_text("goal:a", "goal", 2, ["goal:root", "goal:g2"], title='"T-a"', season=3, nest="subtree"), "a gains goal:g2")
    second = vp2(repo, "--emit", "llm")
    assert second.returncode == 0, second.stderr[-300:]
    assert mark_on(second.stdout, "goal:a") == ["[⊃2]"], f"stale cache: {mark_on(second.stdout, 'goal:a')} (want [⊃2])"
    third = vp2(repo, "--emit", "llm")
    assert mark_on(third.stdout, "goal:a") == ["[⊃2]"], "a third run over the warm cache must read the same"


def build_season_fx(tmp_path: Path) -> Repo:
    """build:q is minted in season 2, GAINS goal:g1 in season 2, is carried to season 3 by a one-node commit and never touched again: at current_season 3 its entry is the carry
    commit and it gained nothing above it = `[legacy]`; at current_season 4 NO node has a season-4 commit, so its entry is its FIRST commit and the gain of goal:g1 is above it = graphed, no mark."""
    r = Repo(tmp_path, "sx")
    ladder = lambda n: node_text("config:ladder", "config", 20, [], current_season=n)
    q = lambda ps, season: node_text("build:q", "build", 5, ps, title='"T-q"', season=season)
    r.write(".agi/nodes/.geometry/ladder.md", ladder(2))
    r.write(".agi/nodes/goal/root.md", node_text("goal:root", "goal", 1, [], title='"T-root"', season=2))
    r.write(".agi/nodes/goal/g1.md", node_text("goal:g1", "goal", 2, ["goal:root"], title='"T-g1"', season=2))
    r.write(".agi/nodes/build/q.md", q(["goal:root"], 2))
    r.commit("season 2 tip")
    r.edit(".agi/nodes/build/q.md", q(["goal:root", "goal:g1"], 2), "q gains goal:g1 (season 2)")
    r.edit(".agi/nodes/.geometry/ladder.md", ladder(3), "ladder: season 3")
    for nid, typ, i, ps in (("goal:root", "goal", 1, []), ("goal:g1", "goal", 2, ["goal:root"])):
        r.edit(f".agi/nodes/goal/{nid.split(':')[1]}.md", node_text(nid, typ, i, ps, title=f'"T-{nid.split(":")[1]}"', season=3), f"carry {nid}")
    r.edit(".agi/nodes/build/q.md", q(["goal:root", "goal:g1"], 3), "carry build:q")
    return r


def test_l4b_a_new_season_with_no_node_commit_invalidates_the_cached_mark(tmp_path):
    """ONE HOME, two runs; the ONLY commit between them edits ladder.md (current_season 3 -> 4), so every node path keeps its newest commit: build:q reads `[legacy]` at season 3 and NO
    mark at season 4 (its entry falls back to its first commit; the goal:g1 gain is above it). A cache key that ignores the season returns the stale `[legacy]` (DG5's M2)."""
    repo = build_season_fx(tmp_path)
    first = vp2(repo, "--emit", "llm")
    assert first.returncode == 0, first.stderr[-300:]
    assert mark_on(first.stdout, "build:q") == ["[legacy]"], first.stdout[-500:]
    repo.edit(".agi/nodes/.geometry/ladder.md", node_text("config:ladder", "config", 20, [], current_season=4), "ladder: season 4")
    second = vp2(repo, "--emit", "llm")
    assert second.returncode == 0, second.stderr[-300:]
    assert mark_on(second.stdout, "build:q") == [], f"stale cache across a season: {mark_on(second.stdout, 'build:q')} (want none)"


def test_l4c_an_unwritable_home_still_renders_the_mark(tmp_path):
    """The cache is an optimisation: HOME read-only (no ~/.cache can be created) -> rc 0 and the marks are all on, as on a writable HOME."""
    repo = build_v(tmp_path)
    ro = tmp_path / "ro-home"
    ro.mkdir()
    ro.chmod(0o500)
    try:
        r = vp2(repo, "--emit", "llm", home=ro)
    finally:
        ro.chmod(0o700)
    assert r.returncode == 0, (r.returncode, r.stderr[-300:])
    assert mark_on(r.stdout, "goal:a") == ["[legacy ⊃2]"] and mark_on(r.stdout, "build:z") == ["[legacy]"] and mark_on(r.stdout, "goal:b") == [], r.stdout[-500:]
    assert "Traceback" not in r.stderr, r.stderr[-300:]


def test_l4c2_a_cache_path_that_is_a_file_still_renders_the_mark(tmp_path):
    """HOME/.cache is a regular FILE (makedirs fails): rc 0, all marks on, no traceback."""
    repo = build_v(tmp_path)
    h = tmp_path / "file-home"
    h.mkdir()
    (h / ".cache").write_text("not a directory")
    r = vp2(repo, "--emit", "llm", home=h)
    assert r.returncode == 0, (r.returncode, r.stderr[-300:])
    assert mark_on(r.stdout, "goal:a") == ["[legacy ⊃2]" ] and mark_on(r.stdout, "build:z") == ["[legacy]"], r.stdout[-500:]
    assert "Traceback" not in r.stderr, r.stderr[-300:]


def scratch_bin(tmp_path: Path, name: str, old: str, new: str, nth: int = 1) -> Path:
    """A scratch copy of the bin dir under test: every entry a symlink except viewport.py, a patched copy (the nth occurrence of `old` replaced by `new`)."""
    d = tmp_path / name
    d.mkdir()
    for e in BIN.iterdir():
        if e.name in ("viewport.py", "__pycache__"):
            continue
        (d / e.name).symlink_to(e)
    src = (BIN / "viewport.py").read_text()
    if old:
        assert src.count(old) >= nth, f"{old!r} occurs {src.count(old)} time(s) in viewport.py (need >= {nth}): the lane's patch point moved"
        parts = src.split(old)
        src = old.join(parts[:nth]) + new + old.join(parts[nth:])
    (d / "viewport.py").write_text(src)
    return d


LG = 'lg = f" {f.legacy}" if f.legacy else ""'


def test_l4d_verify_exits_0_on_a_clean_scratch_copy(tmp_path):
    """The control for the patched rows: an UNPATCHED scratch copy of the bin dir passes --verify (so a non-zero below is the patch, not the copy)."""
    repo = build_v(tmp_path)
    d = scratch_bin(tmp_path, "bin_clean", "", "")
    r = vp2(repo, "--verify", bin_dir=d)
    assert r.returncode == 0 and "PASS" in r.stdout, (r.returncode, r.stdout[-300:], r.stderr[-300:])


@pytest.mark.parametrize("which,nth,new", [
    ("the human view drops the mark", 1, 'lg = ""'),
    ("the llm view drops the mark", 2, 'lg = ""'),
    ("the llm view alters the mark", 2, 'lg = f" {f.legacy.replace(\'legacy\', \'old\')}" if f.legacy else ""'),
    ("the human view alters the mark", 1, 'lg = f" {f.legacy.replace(\'⊃\', \'+\')}" if f.legacy else ""'),
])
def test_l4d_verify_fails_when_one_view_drops_or_alters_the_mark(tmp_path, which, nth, new):
    """goal:g2.19 'one render, two readers': a renderer that drops or alters the legacy mark in ONE of the two views makes `viewport.py --verify` exit non-zero (and not print PASS)."""
    repo = build_v(tmp_path)
    d = scratch_bin(tmp_path, "bin_patched", LG, new, nth)
    r = vp2(repo, "--verify", bin_dir=d)
    assert r.returncode != 0 and "PASS" not in r.stdout, f"{which}: --verify still passes: rc {r.returncode} {r.stdout[-300:]}"
    # and the patched view really differs from the clean one (the patch is live, not vacuous)
    clean = vp2(repo, "--emit", "llm" if nth == 2 else "human")
    patched = vp2(repo, "--emit", "llm" if nth == 2 else "human", bin_dir=d)
    assert MARK_RE.findall(clean.stdout) != MARK_RE.findall(patched.stdout), f"{which}: the patch changed nothing in the view"


def build_decoy(tmp_path: Path) -> Repo:
    """build_v + two retitled nodes whose TITLE reads like a mark: goal:b (true mark: none) is 'T-b [legacy] [legacy ⊃9] trap' and goal:a (true mark `[legacy ⊃2]`) is 'T-a [legacy ⊃2]'."""
    repo = build_v(tmp_path)
    repo.edit(".agi/nodes/goal/b.md", node_text("goal:b", "goal", 3, ["goal:a", "goal:g2"], title='"T-b [legacy] [legacy ⊃9] trap"', season=3), "retitle goal:b with a decoy")
    repo.edit(".agi/nodes/goal/a.md", node_text("goal:a", "goal", 2, ["goal:root"], title='"T-a [legacy ⊃2]"', season=3, nest="subtree"), "retitle goal:a with its own mark")
    return repo


def test_l4e_a_title_that_reads_like_a_mark_does_not_fail_the_clean_verify(tmp_path):
    """The compare reads the mark OUT OF the line, so it must cut the title first: with the decoy titles `--verify` still exits 0 (PASS) on the clean tree, the decoys are really on the llm lines, and goal:a's true mark is the one AFTER its title."""
    repo = build_decoy(tmp_path)
    r = vp2(repo, "--verify")
    assert r.returncode == 0 and "PASS" in r.stdout, (r.returncode, r.stdout[-300:], r.stderr[-300:])
    llm = vp2(repo, "--emit", "llm").stdout
    assert "trap" in line_of(llm, "`goal:b`") and "[legacy ⊃9]" in line_of(llm, "`goal:b`"), "the decoy title is not in the view: the row is vacuous"
    assert line_of(llm, "`goal:a`").count("[legacy ⊃2]") == 2, line_of(llm, "`goal:a`")


@pytest.mark.parametrize("which,nth", [("the llm view", 2), ("the human view", 1)])
def test_l4e_a_decoy_title_does_not_mask_a_really_dropped_mark(tmp_path, which, nth):
    """goal:a's TITLE carries the same string as its true mark: when one renderer drops the true mark the line still holds that string (from the title), so a compare that reads the whole line passes. `--verify` must still exit non-zero."""
    repo = build_decoy(tmp_path)
    d = scratch_bin(tmp_path, "bin_decoy", LG, 'lg = ""', nth)
    r = vp2(repo, "--verify", bin_dir=d)
    assert r.returncode != 0 and "PASS" not in r.stdout, f"{which}: a dropped mark hid behind the decoy title: rc {r.returncode} {r.stdout[-300:]}"


# ====================================================================================================
# v3 (DG1 19:4xZ order, SM's mur residues; DG5's contract 19:31Z, ruled by DG1 19:32Z): d1-* the NO-HISTORY class · d2-* the per-keypress stamp memo ·
# d3-* the hierarchy layer at top>0 · d4-* the cache RULE VERSION. The contract the rows pin:
#   viewport._with_legacy(frames, root, top=0, height=None, hier=0) memoises in the module dict viewport._LEGACY_MEMO, key = (str(root), top, height, hier, the window's node ids);
#   a second call with an equal key runs NO subprocess and returns equal frames; the stamp window is frames[max(0, top - hier) : top + height] (hier = the human pane's lines above the frames).
#   legacy.cache_path() ends in legacy.v1.tsv (rows `path TAB season TAB last-commit TAB mark`); a legacy.tsv beside it is never read nor rewritten.
# NOT pinned (DG1 19:32Z): the memo key has no HEAD, so a commit made while a viewport is open shows after a scroll to a window with different node ids.
# ====================================================================================================

ORDER = list(EXPECT)                                    # goal:root, goal:a, goal:b, goal:g2, build:x, build:z  (the hand-made frame order of the d2 / d3a rows)
A_PATH = ".agi/nodes/goal/a.md"
GOALS = ".agi/nodes/goal"


def test_d1a_a_path_with_no_history_reads_a_question_mark_and_an_empty_label(tmp_path, monkeypatch):
    """legacy.py:44: mark() on a path with NO history at rev is '?' and label() renders it as '' (never '[legacy]'); a path WITH history beside it is not '?'."""
    repo = Repo(tmp_path, "nohist2")
    sha = repo.edit(f"{B}/x.md", node_text("build:x", "build", 1, ["mvp:e"], season=2), "x")
    monkeypatch.chdir(repo.dir)
    L = load_legacy()
    nope = f"{B}/nope.md"
    assert L.mark(sha, "2", nope) == "?"
    assert L.label(sha, "2", nope) == "" and L.label(sha, "2", nope, {}) == "", (L.label(sha, "2", nope), L.label(sha, "2", nope, {}))
    assert L.mark(sha, "2", f"{B}/x.md") != "?" and L.label(sha, "2", f"{B}/x.md") == "[legacy]"


def test_d1b_labels_omits_a_path_that_has_no_history(tmp_path, monkeypatch):
    """legacy.py:85 `if p not in last: continue`: a node file WRITTEN BUT NEVER COMMITTED (and a path git has never seen) is OMITTED from labels() (no key, not a computed blank),
    while a committed node beside it keeps its label."""
    repo = build_v(tmp_path)
    monkeypatch.chdir(repo.dir)
    L = load_legacy()
    import nest
    nodes = nest.graph("HEAD")
    ghost = f"{GOALS}/uncommitted.md"
    (repo.dir / ghost).write_text(node_text("goal:uncommitted", "goal", 40, ["goal:root"], title='"T-ghost"', season=3))
    out = L.labels("HEAD", "3", [nodes["goal:a"][0], ghost, f"{GOALS}/never-existed.md"], nodes)
    assert out == {nodes["goal:a"][0]: "[legacy ⊃2]"}, out


def test_d1c_an_uncommitted_node_file_carries_no_mark_in_either_view(tmp_path):
    """The viewport with a node file written but never committed: its line is in BOTH `--emit human` and `--emit llm` (not vacuous) and carries NO mark in either; the committed
    nodes keep theirs; --verify exits 0."""
    repo = build_v(tmp_path)
    repo.write(f"{GOALS}/g9.md", node_text("goal:g9", "goal", 41, ["goal:root"], title='"T-g9"', season=3))
    human, llm = vp(repo, "--emit", "human"), vp(repo, "--emit", "llm")
    assert human.returncode == 0 and llm.returncode == 0, (human.stderr[-300:], llm.stderr[-300:])
    assert MARK_RE.findall(line_of(human.stdout, "T-g9")) == [] and MARK_RE.findall(line_of(llm.stdout, "`goal:g9`")) == [], (line_of(human.stdout, "T-g9"), line_of(llm.stdout, "`goal:g9`"))
    assert MARK_RE.findall(line_of(llm.stdout, "`goal:a`")) == ["[legacy ⊃2]"]
    v = vp(repo, "--verify")
    assert v.returncode == 0 and "PASS" in v.stdout, (v.returncode, v.stdout[-300:], v.stderr[-300:])


# ---- d2: the per-keypress stamp memo (in-process: viewport.py is imported from BIN) ----

@pytest.fixture
def vpmod():
    sys.path.insert(0, str(BIN))
    import viewport
    memo = getattr(viewport, "_LEGACY_MEMO", None)
    for d in (memo, viewport._LEGACY_GRAPH):
        if d is not None:
            d.clear()
    yield viewport
    for d in (getattr(viewport, "_LEGACY_MEMO", None), viewport._LEGACY_GRAPH):
        if d is not None:
            d.clear()


class GitCount:
    """Counts every child process (subprocess.run builds a Popen, so patching Popen sees run AND Popen users in viewport, legacy and nest)."""

    def __init__(self, monkeypatch):
        self.calls: list = []
        real = subprocess.Popen
        calls = self.calls

        def counted(*a, **k):                                 # a function, not a subclass: a conftest may already have wrapped Popen
            calls.append(a[0] if a else k.get("args"))
            return real(*a, **k)

        monkeypatch.setattr(subprocess, "Popen", counted)


def fr(v, nid: str, title: str = ""):
    return v.Frame(node_id=nid, type=nid.split(":")[0], depth=0, kind="leaf", title=title or nid, verdict="", damaged="", agents=())


def stamp(v, frames, root, top, h, hier=0):
    return v._with_legacy(frames, root, top, h, **({"hier": hier} if hier else {}))


def window(top: int, h: int, hier: int, n: int) -> range:
    return range(max(0, top - hier), min(n, top + h))


def test_d2a_a_second_call_with_an_equal_key_runs_no_subprocess_and_returns_equal_frames(tmp_path, monkeypatch, vpmod):
    """The interactive loop redraws per key: the SAME window must not walk git again (1.3-1.6 s per scroll step). First call: git runs (not vacuous) and the marks are right;
    second identical call: 0 child processes, frames EQUAL to the first call's."""
    repo = build_v(tmp_path)
    root = repo.dir / ".agi"
    frames = [fr(vpmod, nid) for nid in ORDER]
    g = GitCount(monkeypatch)
    first = stamp(vpmod, frames, root, 0, 6)
    n1 = len(g.calls)
    assert n1 > 0, "the first call must run git: the count is not vacuous"
    assert [f.legacy for f in first] == [EXPECT[nid][1] for nid in ORDER], [f.legacy for f in first]
    second = stamp(vpmod, frames, root, 0, 6)
    assert len(g.calls) == n1, f"a second equal call ran {len(g.calls) - n1} child process(es): {g.calls[n1:][:3]}"
    assert second == first


@pytest.mark.parametrize("part", ["top", "height", "hier", "one window id", "root"])
def test_d2b_a_changed_key_part_recomputes(tmp_path, monkeypatch, vpmod, part):
    """Each part of the key (root, top, height, hier, ONE node id in the window) changed alone, after a warm call, runs git again and stamps the NEW window right. The frames of
    the top / height / hier cases repeat ONE node, so the window's node ids are equal across the two calls and only that one part differs."""
    repo = build_v(tmp_path)
    root = repo.dir / ".agi"
    same = [fr(vpmod, "goal:a")] * 10
    mixed = [fr(vpmod, nid) for nid in ORDER]
    mixed2 = [*mixed[:2], fr(vpmod, "goal:g2"), *mixed[3:]]
    cases = {  # part -> (frames1, args1, frames2, args2, root2)   args = (top, height, hier)
        "top": (same, (2, 3, 0), same, (3, 3, 0), root),
        "height": (same, (8, 3, 0), same, (8, 4, 0), root),
        "hier": (same, (1, 2, 3), same, (1, 2, 5), root),
        "one window id": (mixed, (0, 6, 0), mixed2, (0, 6, 0), root),
        "root": (mixed, (0, 6, 0), mixed, (0, 6, 0), build_v(tmp_path / "two").dir / ".agi"),
    }
    f1, a1, f2, a2, root2 = cases[part]
    stamp(vpmod, f1, root, *a1[:2], hier=a1[2])
    g = GitCount(monkeypatch)
    out = stamp(vpmod, f2, root2, a2[0], a2[1], hier=a2[2])
    assert len(g.calls) > 0, f"{part}: the changed key was served from the memo (0 child processes)"
    win = window(*a2, len(f2))                       # the stamp is keyed by node id, so a REPEATED id is stamped outside the window too: judge the window only
    got = [out[i].legacy for i in win]
    assert win and got == [EXPECT[f2[i].node_id][1] for i in win], (part, got)


def test_d2c_clearing_the_memo_resets_it(tmp_path, monkeypatch, vpmod):
    """viewport._LEGACY_MEMO exists (a dict), a warm call fills it, .clear() empties it, and the same call then runs git again."""
    repo = build_v(tmp_path)
    root = repo.dir / ".agi"
    frames = [fr(vpmod, nid) for nid in ORDER]
    stamp(vpmod, frames, root, 0, 6)
    memo = getattr(vpmod, "_LEGACY_MEMO", None)
    assert isinstance(memo, dict) and len(memo) >= 1, memo
    g = GitCount(monkeypatch)
    stamp(vpmod, frames, root, 0, 6)
    assert len(g.calls) == 0, "warm: served from the memo"
    memo.clear()
    stamp(vpmod, frames, root, 0, 6)
    assert len(g.calls) > 0, "after _LEGACY_MEMO.clear() the call must recompute"


# ---- d3: the hierarchy layer at top > 0 ----

def test_d3a_the_stamp_window_is_the_union_of_what_the_human_pane_shows_and_what_llm_shows(tmp_path, vpmod):
    """With `hier` lines above the frames the human pane (layer hierarchy) shows frames[top-hier : top+h-hier] and `--emit llm` shows frames[top : top+h]; the stamp covers
    frames[max(0, top-hier) : top+h] and NOTHING else (a frame outside both windows is not walked: its mark stays ''). Second case: hier > top clamps the start to 0."""
    repo = build_v(tmp_path)
    root = repo.dir / ".agi"
    for top, h, hier in ((3, 2, 2), (1, 2, 3)):
        vpmod._LEGACY_MEMO.clear() if hasattr(vpmod, "_LEGACY_MEMO") else None
        frames = [fr(vpmod, nid) for nid in ORDER]
        out = stamp(vpmod, frames, root, top, h, hier=hier)
        win = window(top, h, hier, len(frames))
        want = [EXPECT[f.node_id][1] if i in win else "" for i, f in enumerate(frames)]
        assert [f.legacy for f in out] == want, ((top, h, hier), [f.legacy for f in out], want)
        assert any(w for w in want) and any(EXPECT[ORDER[i]][1] and i not in win for i in range(len(ORDER))), "the case must have a marked frame inside AND outside the window"


POSTS = """---
id: config:posts
mint_id: {m}
type: config
parents: []
posts:
  - name: dg-a
    role: director
    tier: 2
    owning_goal: goal:root
  - name: dg-b
    role: parent
    tier: 3
    personality_ref: goal:a
  - name: dg-c
    role: kid
    tier: 1
---
body
"""


def add_posts(repo: Repo) -> None:
    """Three seats (two anchored, one not): the hierarchy layer is then 4 lines (the header + 3) above the frames in the human pane."""
    repo.write(".agi/nodes/.geometry/posts.md", POSTS.format(m=mint(30)))
    repo.commit("posts", ".agi/nodes/.geometry/posts.md")


def frame_marks(out: str, view: str) -> dict:
    """{node id: [marks on its line]} for the frame lines SHOWN in a view of EXPECT's nodes (human: the `~ `-prefixed lines of the hierarchy layer, found by title; llm: `id` lines)."""
    shown = {}
    for nid, (title, _) in EXPECT.items():
        if view == "llm":
            hits = [l for l in out.splitlines() if l.lstrip().startswith("- ") and f"`{nid}`" in l]
        else:
            hits = [l for l in out.splitlines() if l.startswith("~ ") and re.search(rf"\b{re.escape(title)}\b", l)]
        if hits:
            assert len(hits) == 1, (nid, hits)
            shown[nid] = MARK_RE.findall(hits[0])
    return shown


def test_d3b_the_cli_hierarchy_layer_at_top_5_prints_the_true_label_on_every_frame_either_view_shows(tmp_path):
    """`viewport.py --live --layer hierarchy --top 5 --height 3`: the human pane shows frames 1..3 (4 hierarchy lines come first), `--emit llm` shows frames 5..7. EVERY frame either
    view shows carries its true label (EXPECT), the human pane's goal:root (a marked frame in the shifted-in part) included, and the llm slice carries the same label wherever the two overlap."""
    repo = build_v(tmp_path)
    add_posts(repo)
    outs = {}
    for view in ("human", "llm"):
        r = vp(repo, "--live", "--layer", "hierarchy", "--emit", view, "--top", "5", "--height", "3")
        assert r.returncode == 0, (view, r.returncode, r.stderr[-300:])
        outs[view] = frame_marks(r.stdout, view)
    assert "goal:root" in outs["human"] and "build:z" in outs["llm"], f"the fixture must show a marked frame in each view: {outs}"
    for view, shown in outs.items():
        for nid, marks in shown.items():
            want = EXPECT[nid][1]
            assert marks == ([want] if want else []), f"{view} view: {nid} reads {marks}, want {[want] if want else []}"
    for nid in set(outs["human"]) & set(outs["llm"]):
        assert outs["human"][nid] == outs["llm"][nid], nid


def test_d3c_the_graph_layer_at_top_5_is_unchanged_control(tmp_path):
    """Control (GREEN before and after the re-cut): in the graph layer the human pane and `--emit llm` show the SAME frames 5..7 and print the same true labels."""
    repo = build_v(tmp_path)
    add_posts(repo)
    outs = {}
    for view in ("human", "llm"):
        r = vp(repo, "--live", "--layer", "graph", "--emit", view, "--top", "5", "--height", "3")
        assert r.returncode == 0, (view, r.stderr[-300:])
        txt = r.stdout
        if view == "human":                                          # graph layer: the frame lines are un-prefixed; pick them by title
            shown = {}
            for nid, (title, _) in EXPECT.items():
                hits = [l for l in txt.splitlines() if not l.startswith("~ ") and re.search(rf"^\s*\S+ [A-Za-z?] {re.escape(title)}\b", l)]
                if hits:
                    shown[nid] = MARK_RE.findall(hits[0])
            outs[view] = shown
        else:
            outs[view] = frame_marks(txt, view)
    assert outs["human"] == outs["llm"] and "build:z" in outs["llm"], outs
    for nid, marks in outs["llm"].items():
        assert marks == ([EXPECT[nid][1]] if EXPECT[nid][1] else []), (nid, marks)


# ---- d4: the cache carries a RULE VERSION (legacy.v1.tsv) ----

def cache_dir(home: Path) -> Path:
    return home / ".cache" / "agi"


def seed(home: Path, name: str, rows: list) -> str:
    d = cache_dir(home)
    d.mkdir(parents=True, exist_ok=True)
    text = "".join("\t".join(r) + "\n" for r in rows)
    (d / name).write_text(text)
    return text


def test_d4a_the_cache_file_is_named_legacy_v1_tsv(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    assert Path(load_legacy().cache_path()) == tmp_path / "xdg" / "agi" / "legacy.v1.tsv"


def test_d4b_a_planted_row_in_the_old_legacy_tsv_is_ignored_and_the_file_is_not_rewritten(tmp_path):
    """goal:a's true mark is `legacy` (label `[legacy ⊃2]`). A WRONG row (`-` = graphed, label `[⊃2]`) for goal:a at season 3 and its REAL newest commit is planted in the OLD name
    legacy.tsv: the mark is recomputed (the old file is from the rule before the version), and the old file stays byte for byte."""
    repo = build_v(tmp_path)
    home = tmp_path / "h4b"
    home.mkdir()
    sha = repo.g("log", "-1", "--format=%H", "--", A_PATH)
    old = seed(home, "legacy.tsv", [(A_PATH, "3", sha, "-")])
    r = vp2(repo, "--emit", "llm", home=home)
    assert r.returncode == 0, r.stderr[-300:]
    assert mark_on(r.stdout, "goal:a") == ["[legacy ⊃2]"], f"the planted legacy.tsv row was served: {mark_on(r.stdout, 'goal:a')}"
    assert (cache_dir(home) / "legacy.tsv").read_text() == old, "legacy.tsv was rewritten"


def test_d4c_a_matching_row_in_legacy_v1_tsv_is_served_control(tmp_path):
    """Control (the cache still works): the SAME wrong row planted in legacy.v1.tsv, matching goal:a's newest commit, IS served: the label reads `[⊃2]`."""
    repo = build_v(tmp_path)
    home = tmp_path / "h4c"
    home.mkdir()
    sha = repo.g("log", "-1", "--format=%H", "--", A_PATH)
    seed(home, "legacy.v1.tsv", [(A_PATH, "3", sha, "-")])
    r = vp2(repo, "--emit", "llm", home=home)
    assert r.returncode == 0, r.stderr[-300:]
    assert mark_on(r.stdout, "goal:a") == ["[⊃2]"], f"a matching legacy.v1.tsv row was not served: {mark_on(r.stdout, 'goal:a')}"


def test_d4d_a_run_writes_legacy_v1_tsv_in_four_columns_and_no_legacy_tsv(tmp_path):
    repo = build_v(tmp_path)
    home = tmp_path / "h4d"
    home.mkdir()
    r = vp2(repo, "--emit", "llm", home=home)
    assert r.returncode == 0, r.stderr[-300:]
    sha = repo.g("log", "-1", "--format=%H", "--", A_PATH)
    rows = [l.split("\t") for l in (cache_dir(home) / "legacy.v1.tsv").read_text().splitlines()]
    assert rows and all(len(c) == 4 for c in rows), rows
    assert [A_PATH, "3", sha, "legacy"] in rows, rows
    assert not (cache_dir(home) / "legacy.tsv").exists(), "a run created the old-name file"


# ---- d4e / d4f: the DOC (doc:rse-d3-legacy) documents the versioned cache (DG1 19:5xZ, the doc line 1e41179fe7). Env D3_REPO=<repo> reads the doc from another tree. ----

DOC_REL = ".agi/nodes/doc/rse-d3-legacy.md"


def cache_doc_line() -> str:
    top = os.environ.get("D3_REPO") or subprocess.run(["git", "-C", str(HERE.parent), "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    assert top, "run inside the repo"
    text = (Path(top) / DOC_REL).read_text()
    hits = [l for l in text.splitlines() if "a per-user cache file" in l]
    assert len(hits) == 1, f"{DOC_REL}: {len(hits)} lines name the per-user cache file"
    return hits[0]


def test_d4e_the_doc_documents_legacy_v1_tsv_and_the_four_column_row():
    """The doc's cache line: names the file `agi/legacy.v1.tsv`; documents the row as exactly FOUR columns in the order path, season, last-commit, mark (a code span of 4 fields joined
    by ` TAB `); says an old-name file is never read; and no longer names `agi/legacy.tsv` as the cache (the old name appears only after the words 'old-name')."""
    line = cache_doc_line()
    assert "agi/legacy.v1.tsv" in line, line[-400:]
    spans = [s for s in re.findall(r"`([^`]*)`", line) if " TAB " in s]
    assert len(spans) == 1, spans
    cols = spans[0].split(" TAB ")
    assert len(cols) == 4 and cols[:3] == ["path", "season", "last-commit"] and cols[3].startswith("legacy"), cols
    assert "agi/legacy.tsv" not in line, "the doc still names agi/legacy.tsv as the cache"
    assert "never read" in line, "the doc must say an old-name cache file is never read"
    for m in re.finditer(r"legacy\.tsv", line):
        assert "old-name" in line[:m.start()], f"legacy.tsv named before the old-name sentence: {line[max(0, m.start() - 60):m.end()]}"


def test_d4f_the_doc_names_the_file_the_code_uses(monkeypatch, tmp_path):
    """The doc and legacy.cache_path() agree on the cache file's name (the rule version in the name is one fact, not two)."""
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    name = Path(load_legacy().cache_path()).name
    assert f"agi/{name}" in cache_doc_line(), (name, cache_doc_line()[-300:])


# ---- i: the INTERACTIVE loop (SM's pre-gate survivor: interactive()'s hier forced to 0 stayed green, the loop had no row). A STUB curses drives the REAL viewport.main() -> interactive()
# in a child process (so a mutated copy of viewport.py can be run the same way): a scripted key list, a fixed 40 x 250 screen, every redraw's text and the child processes it started recorded. ----

RUNNER = r'''
import io, json, subprocess, sys, types
bin_dir, project, keys, layer = sys.argv[1:5]
sys.path.insert(0, bin_dir)
calls = []
real_popen = subprocess.Popen
def counted(*a, **k):
    calls.append(list(a[0]) if a and not isinstance(a[0], str) else (a[0] if a else k.get("args")))
    return real_popen(*a, **k)
subprocess.Popen = counted
cur = types.ModuleType("curses")
cur.error = type("error", (Exception,), {})
cur.A_REVERSE = 1
for n, v in dict(KEY_DOWN=258, KEY_UP=259, KEY_LEFT=260, KEY_RIGHT=261, KEY_NPAGE=338, KEY_PPAGE=339).items():
    setattr(cur, n, v)
cur.curs_set = lambda n: None
draws = []
class Scr:
    def __init__(s):
        s.cur, s.keys, s.mark = [], [ord(c) for c in keys], 0
    def getmaxyx(s): return (40, 250)
    def nodelay(s, f): pass
    def erase(s): s.cur = []
    def addstr(s, y, x, text, attr=None): s.cur.append(text)
    def refresh(s): pass
    def getch(s):
        new = calls[s.mark:]
        draws.append({"lines": s.cur, "calls": len(new), "argv": [" ".join(map(str, c)) if isinstance(c, (list, tuple)) else str(c) for c in new]})
        s.mark = len(calls)
        return s.keys.pop(0)
cur.wrapper = lambda fn: fn(Scr())
sys.modules["curses"] = cur
class TTY(io.StringIO):
    def isatty(self): return True
real_out = sys.stdout
sys.stdout = TTY()
sys.argv = ["viewport.py", "--project", project, "--live", "--layer", layer]
import viewport
rc = viewport.main()
real_out.write(json.dumps({"rc": rc, "draws": draws}))
'''


def run_interactive(tmp_path: Path, repo: Repo, keys: str, bin_dir: Path | None = None, layer: str = "hierarchy") -> dict:
    """Drive the interactive viewport with the scripted `keys` (j = down, l = right, q = quit) on `repo`; {"rc", "draws": [{"lines", "calls", "git"}]} (one entry per redraw)."""
    import json
    runner = tmp_path / "runner.py"
    runner.write_text(RUNNER)
    r = subprocess.run([sys.executable, str(runner), str(bin_dir or BIN), str(repo.dir / ".agi"), keys, layer], cwd=repo.dir, capture_output=True, text=True, timeout=180,
                       env={"PATH": "/usr/bin:/bin", "HOME": os.environ["HOME"], "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"})
    assert r.returncode == 0, (r.returncode, r.stdout[-300:], r.stderr[-600:])
    out = json.loads(r.stdout)
    assert out["rc"] == 0 and len(out["draws"]) == len(keys), (out["rc"], len(out["draws"]), keys, r.stderr[-300:])
    return out


def check_hierarchy_marks(out: dict) -> None:
    """The LAST redraw of 'jjjq' (top 3, hierarchy layer, 4 hierarchy lines above the frames): every frame the pane shows carries its true label, goal:root (index 2, above `top`) included."""
    shown = frame_marks("\n".join(out["draws"][-1]["lines"]), "human")
    assert "goal:root" in shown and "build:z" in shown, f"the pane must show goal:root and build:z: {shown}"
    for nid, marks in shown.items():
        want = EXPECT[nid][1]
        assert marks == ([want] if want else []), f"interactive pane: {nid} reads {marks}, want {[want] if want else []}"


def check_equal_window_runs_no_git(out: dict) -> None:
    """Keys 'jlq': redraw 1 scrolls (top 0 -> 1: the stamp runs git, not vacuous), redraw 2 only pans (left += 4, the SAME window): the stamp runs NO child process. The loop's own
    five `git rev-parse --git-dir --git-common-dir` per redraw (not the stamp's: they run on every redraw, memo or not) are set aside by their exact shape."""
    stamp = lambda i: [a for a in out["draws"][i]["argv"] if not a.endswith("rev-parse --git-dir --git-common-dir")]
    assert stamp(1), f"the scrolled redraw must run the stamp's git (not vacuous): {out['draws'][1]['argv']}"
    assert stamp(2) == [], f"a redraw of an equal window ran child processes for the stamp: {stamp(2)}"


def test_i1_the_interactive_hierarchy_layer_at_top_3_draws_the_true_mark_on_every_frame_its_pane_shows(tmp_path):
    repo = build_v(tmp_path)
    add_posts(repo)
    check_hierarchy_marks(run_interactive(tmp_path, repo, "jjjq"))


def test_i2_a_redraw_of_an_equal_window_runs_no_git(tmp_path):
    repo = build_v(tmp_path)
    add_posts(repo)
    check_equal_window_runs_no_git(run_interactive(tmp_path, repo, "jlq"))


def test_i3_the_graph_layer_control_draws_the_true_marks(tmp_path):
    """Control (GREEN before and after): the interactive GRAPH layer at top 3 prints the true label on every frame its pane shows."""
    repo = build_v(tmp_path)
    add_posts(repo)
    out = run_interactive(tmp_path, repo, "jjjq", layer="graph")
    txt = out["draws"][-1]["lines"]
    shown = {}
    for nid, (title, _) in EXPECT.items():
        hits = [l for l in txt if not l.startswith("~ ") and re.search(rf"^\s*\S+ [A-Za-z?] {re.escape(title)}\b", l)]
        if hits:
            shown[nid] = MARK_RE.findall(hits[0])
    assert len(shown) >= 2, shown
    for nid, marks in shown.items():
        assert marks == ([EXPECT[nid][1]] if EXPECT[nid][1] else []), (nid, marks)


def scratch_bin_multi(tmp_path: Path, name: str, patches: list) -> Path:
    """A scratch copy of the bin dir under test: viewport.py patched by every (old, new) pair (each `old` must occur exactly once), the rest symlinked."""
    d = tmp_path / name
    d.mkdir()
    for e in BIN.iterdir():
        if e.name not in ("viewport.py", "__pycache__"):
            (d / e.name).symlink_to(e)
    src = (BIN / "viewport.py").read_text()
    for old, new in patches:
        assert src.count(old) == 1, f"{old[:70]!r} occurs {src.count(old)} time(s) in viewport.py: the lane's patch point moved"
        src = src.replace(old, new)
    (d / "viewport.py").write_text(src)
    return d


I_HIER = 'len(hierarchy_lines(anchors)) if (anchors is not None and layer == "hierarchy") else 0)'
I_CALL = f"frames = _with_legacy(frames, root, top, h,\n                                  {I_HIER}"
I_STREAM = "frames = frame_stream(g, fm_by_id, anchor, depth, agents)\n"


@pytest.mark.parametrize("name,patches", [
    ("hier forced to 0 in interactive() (SM's survivor)", [(I_HIER, "0)")]),
    ("interactive() does not pass hier", [(I_CALL, "frames = _with_legacy(frames, root, top, h)")]),
    ("interactive() stamps BEFORE the anchors (hier 0, the later stamp gone)", [(I_STREAM, "frames = _with_legacy(frame_stream(g, fm_by_id, anchor, depth, agents), root, top, h, 0)\n"), (I_CALL, "pass")]),
])
def test_i4_mutants_of_the_real_viewport_make_the_hierarchy_mark_row_red(tmp_path, name, patches):
    """One edit each to the REAL viewport.py (a scratch copy): the interactive hierarchy pane then leaves a frame above `top` unstamped, and row i1's check fails."""
    repo = build_v(tmp_path)
    add_posts(repo)
    d = scratch_bin_multi(tmp_path, "bin_i", patches)
    out = run_interactive(tmp_path, repo, "jjjq", bin_dir=d)
    with pytest.raises(AssertionError):
        check_hierarchy_marks(out)


def test_i5_a_mutant_that_forgets_the_memo_each_redraw_makes_the_equal_window_row_red(tmp_path):
    """interactive() clears _LEGACY_MEMO before every stamp: the pan-only redraw runs git again, and row i2's check fails."""
    repo = build_v(tmp_path)
    add_posts(repo)
    d = scratch_bin_multi(tmp_path, "bin_i2", [("            frames = _with_legacy(frames, root, top, h,\n", "            _LEGACY_MEMO.clear()\n            frames = _with_legacy(frames, root, top, h,\n")])
    out = run_interactive(tmp_path, repo, "jlq", bin_dir=d)
    with pytest.raises(AssertionError):
        check_equal_window_runs_no_git(out)


# ---- x: the lane never writes a user's REAL cache (DG1 21:4xZ, SM's gate: with XDG_CACHE_HOME set in the environment the in-process rows wrote ${XDG_CACHE_HOME}/agi/legacy.v1.tsv) ----

FIXTURE_LINE = '    monkeypatch.setenv("XDG_CACHE' + '_HOME", str(tmp_path / "xdg-cache"))'   # built in two parts so this definition is not a second copy of the line


def nested_pytest(tmp_path: Path, test_file: Path, decoy: Path, *extra: str) -> subprocess.CompletedProcess:
    """pytest on `test_file` in a CHILD process whose environment carries XDG_CACHE_HOME=<decoy> (the box of a user who has one set)."""
    tmpdir = tmp_path / "nested-tmp"
    tmpdir.mkdir(exist_ok=True)
    env = {**os.environ, "XDG_CACHE_HOME": str(decoy), "LEGACY_BIN": str(BIN), "TMPDIR": str(tmpdir)}
    return subprocess.run([sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "-q", str(test_file), *extra], capture_output=True, text=True, env=env, timeout=900)


def test_x1_the_fixture_points_the_cache_at_the_tmp_dir_whatever_the_environment_says(tmp_path):
    """Inside a row, XDG_CACHE_HOME is under this row's tmp dir (the autouse fixture overrode the user's) and legacy.cache_path() resolves under it."""
    assert Path(os.environ["XDG_CACHE_HOME"]).is_relative_to(tmp_path), os.environ["XDG_CACHE_HOME"]
    assert Path(load_legacy().cache_path()).is_relative_to(tmp_path), load_legacy().cache_path()


def test_x2_a_whole_file_run_with_a_decoy_xdg_cache_home_leaves_the_decoy_empty(tmp_path):
    """The file run in a child process with XDG_CACHE_HOME=<decoy dir> in its environment (this row and the next excluded): every other row passes and the decoy holds NOTHING."""
    decoy = tmp_path / "decoy"
    decoy.mkdir()
    r = nested_pytest(tmp_path, HERE, decoy, "-k", "not decoy")
    assert r.returncode == 0 and " passed" in r.stdout, (r.returncode, r.stdout[-400:], r.stderr[-300:])
    assert sorted(decoy.rglob("*")) == [], f"the lane wrote into the user's cache dir: {sorted(decoy.rglob('*'))[:5]}"


def test_x3_a_mutant_without_the_fixture_line_writes_the_decoy_cache_red_control(tmp_path):
    """The control for x2: a copy of this file WITHOUT the fixture's XDG_CACHE_HOME line (one edit) run the same way on the in-process rows that fill the cache (d1b): the decoy is NOT empty."""
    src = HERE.read_text()
    assert src.count(FIXTURE_LINE) == 1, "the lane's patch point moved"
    mut = tmp_path / "mut" / "test_legacy_mut.py"
    mut.parent.mkdir()
    mut.write_text(src.replace(FIXTURE_LINE, "    pass"))
    decoy = tmp_path / "decoy"
    decoy.mkdir()
    r = nested_pytest(tmp_path, mut, decoy, "-k", "d1b and not decoy")
    assert r.returncode == 0, (r.returncode, r.stdout[-400:], r.stderr[-300:])
    assert sorted(decoy.rglob("*")) != [], "the mutant did not write the decoy cache: row x2 could not fail"
