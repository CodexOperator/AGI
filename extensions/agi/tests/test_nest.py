"""goal:g7.16.1.11.21 (E1 D1) falsifier lane, written FIRST (DG1 03:23Z): a slice is a `nest:` cell on its container's
node and the git history is the record. Design: doc:rse-d1-nest v3 (alive); the reader is `extensions/agi/bin/nest.py`
(`nest.py slice|log REV N`, read-only), the check is `links.nest_unresolved(root)`.

Everything runs against the BUILD's files at the tree under test (nest.py, links.py, metrics.py, write.py and the
schemas of that tree), never a copy of the doc's text: NEST_PY=<file> points the reader rows at a candidate, and the
rest follows this file's own tree. Every git row runs in a throwaway repo (tmp_path, one per case); nothing touches a
live ref. Without a nest.py every reader row FAILS (it does not skip): RED today is `nest.py does not exist`.

Rows
  n1..n10   alive's ten cases, written out again as this file's own
  x-*       what alive's linear history cannot see: a merge (the walk is first-parent), a retired member in `slice`,
            the walk reads only what git reads (a read-only run leaves refs, objects and the index as they were)
  d13-*     D1.3: `nest.py log` of a retired member == `git log --first-parent --follow` of its path, except the commits
            follow reaches through a COPY (C) line (they belong to another node)
  l-*       links.py: nest_unresolved(root), its line in `main`, its metrics cell; it never enters count_broken_links
  s-*       the schemas: `nest` is an optional str|list field of the container types, never `required`; a node with and
            without nest keeps the schema count
  d11/d12   a collapse (the real writer, `set nest subtree`) changes exactly ONE tracked file; the node count holds
  neg-*     nest.py holds no update-ref / commit-tree / mktree
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from tests.veto_cell import write_free_veto  # noqa: E402

HERE = Path(__file__).resolve().parent
BIN = HERE.parent / "bin"
SRC = HERE.parent / "src"
REPO = HERE.parents[2]
NEST = Path(os.environ.get("NEST_PY") or BIN / "nest.py")
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

SCHEMAS = REPO / ".agi" / "context" / "schemas"


# --- a throwaway repo ---
def node(i, parents=(), nest=None, extra=""):
    s = f"---\nid: {i}\nparents:\n" + "".join(f"  - {p}\n" for p in parents)
    if nest == "subtree":
        s += "nest: subtree\n"
    elif nest:
        s += "nest:\n" + "".join(f"  - {m}\n" for m in nest)
    return s + extra + "---\nbody\n"


class Repo:
    def __init__(self, d: Path):
        self.d = d
        self.env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
                        GIT_COMMITTER_EMAIL="t@t", GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null",
                        AGI_TRUNK="HEAD")
        for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
            self.env.pop(k, None)
        d.mkdir(parents=True, exist_ok=True)
        self.g("init", "-q", "-b", "main")

    def g(self, *a):
        return subprocess.run(("git",) + a, cwd=self.d, env=self.env, capture_output=True, text=True, check=True).stdout

    def w(self, path, text, msg):
        p = self.d / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        self.g("add", "-A")
        self.g("commit", "-q", "-m", msg)

    def subjects(self, hashes):
        return [self.g("log", "-1", "--format=%s", h).strip() for h in hashes]

    def build(self):
        self.w(".agi/nodes/goal/a.md", node("goal:a"), "a1")
        self.w(".agi/nodes/goal/b.md", node("goal:b", ["goal:a"]), "b1")
        self.w(".agi/nodes/goal/c.md", node("goal:c", ["goal:b"]), "c1")
        self.w(".agi/nodes/doc/x.md", node("doc:x"), "x1")
        self.w(".agi/nodes/doc/y.md", node("doc:y"), "y1")


@pytest.fixture
def repo(tmp_path):
    return Repo(tmp_path / "r")


def nest(repo, verb, n, rev="HEAD", env=None):
    if not NEST.is_file():
        pytest.fail(f"nest.py is not built: {NEST} does not exist")
    r = subprocess.run([sys.executable, str(NEST), verb, rev, n], cwd=repo.d, env=env or repo.env, capture_output=True, text=True)
    assert r.returncode == 0, f"nest.py {verb} {n} exited {r.returncode}: {r.stderr[-300:]}"
    return r.stdout.split()


def slice_of(repo, n):
    return sorted(nest(repo, "slice", n))


# --- n1..n10: alive's cases, as this file's own ---
def test_n1_a_node_with_no_nest_is_its_own_slice(repo):
    repo.build()
    assert slice_of(repo, "goal:a") == ["goal:a"]


def test_n2_subtree_descends_through_a_member_with_no_nest(repo):
    repo.build()
    repo.w(".agi/nodes/goal/a.md", node("goal:a", nest="subtree"), "a2")
    assert slice_of(repo, "goal:a") == ["goal:a", "goal:b", "goal:c"]


def test_n3_a_member_with_its_own_subtree_expands_itself(repo):
    repo.build()
    repo.w(".agi/nodes/goal/b.md", node("goal:b", ["goal:a"], nest="subtree"), "b2")
    repo.w(".agi/nodes/goal/a.md", node("goal:a", nest="subtree"), "a2")
    assert slice_of(repo, "goal:a") == ["goal:a", "goal:b", "goal:c"]


def test_n4_an_arbitrary_list_of_any_types_and_a_cycle_stops(repo):
    repo.build()
    repo.w(".agi/nodes/doc/x.md", node("doc:x", nest=["doc:y", "goal:c"]), "x2")
    repo.w(".agi/nodes/doc/y.md", node("doc:y", nest=["doc:x"]), "y2")
    assert slice_of(repo, "doc:x") == ["doc:x", "doc:y", "goal:c"]


def test_n5_a_collapse_is_one_one_node_commit_and_the_member_files_stay(repo):
    repo.build()
    refs = repo.g("for-each-ref")
    repo.w(".agi/nodes/doc/x.md", node("doc:x", nest=["doc:y"]), "collapse")
    assert repo.g("show", "--name-only", "--format=", "HEAD").split() == [".agi/nodes/doc/x.md"]
    assert repo.g("for-each-ref").count("\n") == refs.count("\n")
    assert len(repo.g("ls-files", ".agi/nodes").split()) == 5


def test_n6_log_reaches_every_members_history(repo):
    repo.build()
    repo.w(".agi/nodes/doc/x.md", node("doc:x", nest=["doc:y"]), "x2")
    assert repo.subjects(nest(repo, "log", "doc:x")) == ["x2", "y1", "x1"]


def test_n7_a_retired_member_keeps_its_history(repo):
    repo.build()
    repo.w(".agi/nodes/doc/x.md", node("doc:x", nest=["doc:y"]), "x2")
    (repo.d / ".agi/nodes/deprecated/doc").mkdir(parents=True)
    repo.g("mv", ".agi/nodes/doc/y.md", ".agi/nodes/deprecated/doc/y.md")
    repo.g("commit", "-q", "-m", "retire y")
    assert repo.subjects(nest(repo, "log", "doc:x")) == ["retire y", "x2", "y1", "x1"]


def test_n8_a_member_with_a_list_stops_the_descent_and_expands_its_list(repo):
    repo.build()
    repo.w(".agi/nodes/goal/b.md", node("goal:b", ["goal:a"], nest=["doc:x"]), "b2")
    repo.w(".agi/nodes/goal/a.md", node("goal:a", nest="subtree"), "a2")
    assert slice_of(repo, "goal:a") == ["doc:x", "goal:a", "goal:b"]        # b is included, c (b's child) is not


def test_n9_history_older_than_the_one_repo_move_is_read(repo):
    repo.w("nodes/doc/z.md", node("doc:z"), "z1")
    repo.w(".agi/nodes/doc/x.md", node("doc:x", nest=["doc:z"]), "x1")
    (repo.d / ".agi/nodes/doc").mkdir(parents=True, exist_ok=True)
    repo.g("mv", "nodes/doc/z.md", ".agi/nodes/doc/z.md")
    repo.g("commit", "-q", "-m", "move")
    assert repo.subjects(nest(repo, "log", "doc:x")) == ["move", "x1", "z1"]


def test_n10_inline_lists_parse_as_lists(repo):
    repo.w(".agi/nodes/goal/a.md", "---\nid: goal:a\nparents: []\nnest: subtree\n---\n", "a1")
    repo.w(".agi/nodes/goal/b.md", "---\nid: goal:b\nparents: [goal:a, \"doc:k\"]\n---\n", "b1")
    repo.w(".agi/nodes/doc/x.md", "---\nid: doc:x\nnest: [goal:b]\n---\n", "x1")
    assert slice_of(repo, "goal:a") == ["goal:a", "goal:b"]
    assert slice_of(repo, "doc:x") == ["doc:x", "goal:b"]


# --- x-*: what a linear history cannot see ---
def test_x_the_walk_is_first_parent_a_side_branch_commit_shows_only_as_its_merge(repo):
    repo.build()
    repo.w(".agi/nodes/doc/x.md", node("doc:x", nest=["doc:y"]), "x2")
    repo.g("switch", "-q", "-c", "side")
    repo.w(".agi/nodes/doc/y.md", node("doc:y", extra="note: side\n"), "y-side")
    repo.g("switch", "-q", "main")
    repo.w(".agi/nodes/doc/c0.md", node("doc:c0"), "main-moves")
    repo.g("merge", "-q", "--no-ff", "-m", "merge side", "side")
    got = repo.subjects(nest(repo, "log", "doc:x"))
    assert "y-side" not in got and "merge side" in got, got
    paths = [".agi/nodes/doc/x.md", ".agi/nodes/doc/y.md"]
    assert nest(repo, "log", "doc:x") == repo.g("log", "--first-parent", "--format=%H", "--", *paths).split()


def test_x_following_a_retire_move_does_not_depend_on_the_users_diff_renames_config(repo):
    repo.build()
    repo.w(".agi/nodes/doc/x.md", node("doc:x", nest=["doc:y"]), "x2")
    (repo.d / ".agi/nodes/deprecated/doc").mkdir(parents=True)
    repo.g("mv", ".agi/nodes/doc/y.md", ".agi/nodes/deprecated/doc/y.md")
    repo.g("commit", "-q", "-m", "retire y")
    env = dict(repo.env, GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="diff.renames", GIT_CONFIG_VALUE_0="false")
    assert repo.subjects(nest(repo, "log", "doc:x", env=env)) == ["retire y", "x2", "y1", "x1"]


def test_x_slice_includes_a_retired_member(repo):
    repo.build()
    repo.w(".agi/nodes/doc/x.md", node("doc:x", nest=["doc:y"]), "x2")
    (repo.d / ".agi/nodes/deprecated/doc").mkdir(parents=True)
    repo.g("mv", ".agi/nodes/doc/y.md", ".agi/nodes/deprecated/doc/y.md")
    repo.g("commit", "-q", "-m", "retire y")
    assert "doc:y" in slice_of(repo, "doc:x")


def test_x_subtree_descends_through_two_nest_less_levels(repo):
    repo.build()
    repo.w(".agi/nodes/goal/d.md", node("goal:d", ["goal:c"]), "d1")
    repo.w(".agi/nodes/goal/a.md", node("goal:a", nest="subtree"), "a2")
    assert slice_of(repo, "goal:a") == ["goal:a", "goal:b", "goal:c", "goal:d"]


def test_x_a_read_only_run_leaves_refs_objects_and_the_index_as_they_were(repo):
    repo.build()
    repo.w(".agi/nodes/doc/x.md", node("doc:x", nest=["doc:y"]), "x2")

    def state():
        objs = sorted(p.name for p in (repo.d / ".git" / "objects").rglob("*") if p.is_file())
        return (repo.g("for-each-ref"), objs, repo.g("status", "--porcelain=v1"), (repo.d / ".git" / "index").read_bytes())
    before = state()
    nest(repo, "slice", "doc:x")
    nest(repo, "log", "doc:x")
    assert state() == before


# --- D1.3: log of a retired member == git log --first-parent --follow, except commits reached through a C line ---
def _follow(repo, path):
    """(hashes newest first, the hashes up to and including the first commit whose status for the path is a COPY)."""
    out = repo.g("log", "--first-parent", "--follow", "--name-status", "--format=@%H", "--", path)
    hashes, upto, cur, cut = [], [], None, False
    for l in out.split("\n"):
        if l.startswith("@"):
            cur = l[1:]
            hashes.append(cur)
            if not cut:
                upto.append(cur)
        elif l.startswith("C") and not cut:
            cut = True
    return hashes, upto


def test_d13_a_retired_members_log_equals_git_follow(repo):
    uniq = "".join(f"unique line {i} of y {i * 7919 % 1009}\n" for i in range(50))     # no near-copy anywhere: no C line
    repo.w(".agi/nodes/doc/x.md", node("doc:x"), "x1")
    repo.w(".agi/nodes/doc/y.md", node("doc:y", extra=uniq), "y1")                  # born unique: git finds no copy source
    repo.w(".agi/nodes/doc/y.md", node("doc:y", extra=uniq + "note: two\n"), "y2")
    repo.w(".agi/nodes/doc/x.md", node("doc:x", nest=["doc:y"]), "x2")
    (repo.d / ".agi/nodes/deprecated/doc").mkdir(parents=True)
    repo.g("mv", ".agi/nodes/doc/y.md", ".agi/nodes/deprecated/doc/y.md")
    repo.g("commit", "-q", "-m", "retire y")
    follow, upto = _follow(repo, ".agi/nodes/deprecated/doc/y.md")
    assert follow == upto and len(follow) == 3, "fixture error: follow reached a copy line or the history is short"
    assert nest(repo, "log", "doc:y") == follow


def test_d13_commits_follow_reaches_through_a_copy_line_are_not_the_nodes_history(repo):
    big = "".join(f"line {i} of the shared body\n" for i in range(60))
    repo.w(".agi/nodes/doc/src.md", node("doc:src", extra=big), "src-born")
    # ONE commit edits src AND adds cp2 with src's old body: git's copy detection has a candidate source (a C line)
    (repo.d / ".agi/nodes/doc/src.md").write_text(node("doc:src", extra=big + "edit\n"))
    (repo.d / ".agi/nodes/doc/cp2.md").write_text(node("doc:cp2", extra=big))
    repo.g("add", "-A")
    repo.g("commit", "-q", "-m", "src-edit-and-cp2-born-as-a-copy")
    repo.w(".agi/nodes/doc/cp2.md", node("doc:cp2", extra=big + "own edit\n"), "cp2-own-edit")
    follow, upto = _follow(repo, ".agi/nodes/doc/cp2.md")
    assert len(follow) > len(upto), "fixture error: git follow did not reach through a copy line here"
    got = nest(repo, "log", "doc:cp2")
    assert got == upto, (repo.subjects(got), repo.subjects(upto))


# --- the schemas ---
def _schema_texts():
    return {p.name: p.read_text(encoding="utf-8") for p in sorted(SCHEMAS.glob("*.md"))}


def _frontmatter(text):
    import yaml
    m = re.match(r"\A---\n(.*?)\n---", text, re.S)
    return yaml.safe_load(m.group(1)) if m else {}


def test_s_no_schema_lists_nest_as_required():
    bad = [n for n, t in _schema_texts().items()
           if "nest" in ((_frontmatter(t).get("validation") or {}).get("required") or [])]
    assert not bad, f"nest is required in {bad}: a node without it would be reported"


def _nest_type(fm):
    f = (fm.get("fields") or {}).get("nest")
    return None if f is None else (f.get("type") if isinstance(f, dict) else f)


def test_s_the_goal_schema_allows_nest_as_a_str_or_list(tmp_path):
    t = _nest_type(_frontmatter(_schema_texts()["[goal].md"]))
    assert t is not None, "[goal].md has no nest field"
    kinds = set(re.split(r"[|, ]+", t)) if isinstance(t, str) else set(t)
    assert kinds == {"str", "list"}, t


def test_s_every_schema_that_declares_nest_declares_it_str_or_list():
    bad = {}
    for n, t in _schema_texts().items():
        ty = _nest_type(_frontmatter(t))
        if ty is None:
            continue
        kinds = set(re.split(r"[|, ]+", ty)) if isinstance(ty, str) else set(ty)
        if kinds != {"str", "list"}:
            bad[n] = ty
    assert not bad, bad


def _scratch_root(tmp_path):
    root = tmp_path / "proj" / ".agi"
    (root / "nodes").mkdir(parents=True)
    (root / "context").mkdir()
    shutil.copytree(SCHEMAS, root / "context" / "schemas")
    (root / "config.json").write_text("{}", encoding="utf-8")
    return root


def _goal(nid, nest_lines="", parents="  []\n"):
    return (f"---\nid: goal:{nid}\nmint_id: {nid.ljust(32, '0')[:32]}\ntype: goal\ntitle: \"{nid}\"\ngoal_id: G9\n"
            f"goal_kind: perpetual\nstatus: active\norigin: goals-doc\nseeds: []\nconfidence: 0.5\ntags: []\n"
            f"parents: []\n{nest_lines}---\nbody\n")


@pytest.mark.parametrize("nest_lines", ["", "nest: subtree\n", "nest:\n  - goal:b\n", "nest: [goal:b]\n"],
                         ids=["without", "subtree", "list", "inline-list"])
def test_s_a_node_with_and_without_nest_keeps_the_schema_count(tmp_path, nest_lines):
    import node_writer
    from graph_core.persistence import frontmatter as fm_reader
    root = _scratch_root(tmp_path)
    p = root / "nodes" / "goal" / "a.md"
    p.parent.mkdir(parents=True)
    p.write_text(_goal("a", nest_lines), encoding="utf-8")
    fm = fm_reader.load_node_file(p).frontmatter
    assert node_writer.missing_required(root, "goal", fm, "goal:a") == []


# --- links.py ---
def _corpus(tmp_path, nodes):
    root = _scratch_root(tmp_path)
    for rel, text in nodes.items():
        p = root / "nodes" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return root


def _links_main(root):
    r = subprocess.run([sys.executable, str(BIN / "links.py"), "links", "--root", str(root)], cwd=root.parent,
                       capture_output=True, text=True, env=dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null"))
    return r.returncode, r.stdout


DANGLING = {
    "goal/a.md": _goal("a", "nest:\n  - goal:b\n  - goal:nowhere\n  - doc:ghost\n"),
    "goal/b.md": _goal("b"),
}


def test_l_nest_unresolved_names_each_dangling_nest_id_with_its_container(tmp_path):
    import links
    root = _corpus(tmp_path, DANGLING)
    got = [str(x) for x in links.nest_unresolved(root)]
    assert len(got) == 2, got
    for ref in ("goal:nowhere", "doc:ghost"):
        assert any("goal:a" in g and ref in g for g in got), (ref, got)
    assert not any("goal:b" in g.replace("goal:a", "") for g in got), got        # a resolved id is not reported


def test_l_main_reports_each_on_its_own_line_and_a_count_line(tmp_path):
    root = _corpus(tmp_path, DANGLING)
    rc, out = _links_main(root)
    lines = out.splitlines()
    assert any(re.search(r"nest_unresolved\D*2\b", l) for l in lines), out
    for ref in ("goal:nowhere", "doc:ghost"):
        own = [l for l in lines if ref in l and "goal:a" in l]
        assert len(own) == 1, (ref, out)
    assert not [l for l in lines if "goal:b" in l and "nest" in l.lower()], out


def test_l_a_clean_corpus_prints_the_line_with_zero(tmp_path):
    import links
    root = _corpus(tmp_path, {"goal/a.md": _goal("a", "nest:\n  - goal:b\n"), "goal/b.md": _goal("b"),
                              "goal/s.md": _goal("s", "nest: subtree\n")})
    assert list(links.nest_unresolved(root)) == []
    rc, out = _links_main(root)
    assert any(re.search(r"nest_unresolved\D*0\b", l) for l in out.splitlines()), out


def test_l_a_nest_id_naming_a_retired_node_resolves(tmp_path):
    import links
    root = _corpus(tmp_path, {"goal/a.md": _goal("a", "nest:\n  - goal:old\n"),
                              "deprecated/goal/old.md": _goal("old").replace("status: active", "status: retired")})
    assert list(links.nest_unresolved(root)) == []


def test_l_a_nest_id_never_enters_count_broken_links(tmp_path):
    import links
    with_nest = _corpus(tmp_path / "w", DANGLING)
    without = _corpus(tmp_path / "n", {"goal/a.md": _goal("a"), "goal/b.md": _goal("b")})
    assert links.count_broken_links(with_nest) == links.count_broken_links(without) == 0
    live, retired = links.broken_by_status(with_nest)
    assert not [e for e in live + retired if "nowhere" in str(e) or "ghost" in str(e)]


def _metrics(root):
    r = subprocess.run([sys.executable, str(BIN / "metrics.py"), str(root)], cwd=root.parent, capture_output=True,
                       text=True, env=dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null"))
    return {k: v for k, v in (l[len("METRIC "):].split("=", 1) for l in r.stdout.splitlines() if l.startswith("METRIC ") and "=" in l)}


def test_l_the_metrics_cell_counts_them_beside_an_unchanged_broken_links(tmp_path):
    m = _metrics(_corpus(tmp_path, DANGLING))
    assert m.get("nest_unresolved") == "2", m
    assert m.get("broken_links") == "0", m


def test_l_the_metrics_cell_is_zero_when_nothing_dangles(tmp_path):
    m = _metrics(_corpus(tmp_path, {"goal/a.md": _goal("a", "nest:\n  - goal:b\n"), "goal/b.md": _goal("b")}))
    assert m.get("nest_unresolved") == "0", m


# --- D1.1 / D1.2: a collapse through the real writer ---
def test_d11_d12_the_writer_collapses_with_exactly_one_tracked_file_changed_and_the_count_holds(tmp_path):
    root = _scratch_root(tmp_path)
    for nid in ("a", "b"):
        p = root / "nodes" / "goal" / f"{nid}.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(_goal(nid), encoding="utf-8")
    write_free_veto(root / "nodes" / ".geometry")   # the writer reads the veto cell STRICT: a FREE cell, committed in the base
    repo = Repo(root.parent)
    repo.g("add", "-A")
    repo.g("commit", "-q", "-m", "base")
    base = repo.g("rev-parse", "HEAD").strip()
    before = _metrics(root).get("node_count")
    env = dict(repo.env, HOME=str(tmp_path / "hm"), AGI_POST="dg2-falsifier")
    (tmp_path / "hm").mkdir()
    r = subprocess.run([sys.executable, str(BIN / "write.py"), "goal:a", "set nest subtree"], cwd=root.parent, env=env,
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    changed = repo.g("diff", "--name-only", base).split()                       # committed or not: tracked files vs base
    assert changed == [".agi/nodes/goal/a.md"], changed
    assert "nest: subtree" in (root / "nodes" / "goal" / "a.md").read_text(encoding="utf-8")
    assert not [l for l in repo.g("for-each-ref").splitlines() if "refs/grid" in l]
    assert _metrics(root).get("node_count") == before and before, (before, _metrics(root).get("node_count"))
    assert len(list((root / "nodes").rglob("*.md"))) == 3   # a, b and the FREE veto cell


# --- negative: nest.py is read-only ---
def test_neg_nest_py_holds_no_update_ref_commit_tree_or_mktree():
    assert NEST.is_file(), f"nest.py is not built: {NEST} does not exist"
    src = NEST.read_text(encoding="utf-8")
    hits = [w for w in ("update-ref", "commit-tree", "mktree") if w in src]
    assert not hits, hits
