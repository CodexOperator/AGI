"""goal:g7.16.1.11.21 (E1 D1) residue R1-R3 (SM return, DG1 [go] 04:08Z): three defects the first lane (test_nest.py) did
not reach, written against the reader and the check of the tree under test (NEST_PY=<file> points the reader rows at a
candidate; links.py / the rest follow this file's own tree). TEST-ONLY: nothing here edits nest.py.

  r1-*  the walk is order-dependent (nest.py members(): `seen` is shared, so a member reached through a LIST entry
        first blocks the SUBTREE walk of a later entry from descending through it). A slice is a set: the same
        container with its list in another order is the same slice, and a slice is CLOSED -- every member's own
        slice lies inside the container's.
  r2-*  a retire that ALSO edits the node is git's D + A (similarity under -M's 50%), not an R: `log` must still reach
        the add and the retire; a clean R100 move still maps; a D + A of DIFFERENT basenames is NOT one node's move.
  r3-*  a list entry may be a node's MINT id (links.nest_unresolved resolves one); nest.py keys nodes by `id` only, so
        `slice` / `log` drop it. An entry that is neither id nor mint is unresolved AND absent from the slice; a mint
        string equal to another node's id: the exact id wins. Both list spellings (`nest: [..]`, dash list).
  rd1-* (SM mur wf_19c88fa4-12c RD-1) the D + A rule pairs by the node's NORMALIZED path (`deprecated` dropped), never by basename:
        an add of hypothesis/foo.md and a delete of experiment/foo.md in ONE commit is two different nodes, and a retire-edit
        D + A maps in BOTH directions (retire, un-retire).
  rd3-* (RD-3) a nest value that is a string other than exactly `subtree` ('Subtree', 'subtree # x', a bare id) is MALFORMED:
        nest.py slice and log exit 1 `nest: malformed nest <value> ...`, and `links` reports each on its own line (a count
        line `nest_malformed N`, one `nest-malformed <id> -> <value>` row each), beside an unchanged count_broken_links.
  r4-*  the command line (DG1 [amend] 04:23Z): -h / --help = usage on STDOUT rc 0; missing args or an unknown verb =
        usage on STDERR rc 2; an id in neither `id` nor `mint_id` = `nest: unknown id <X>` on STDERR rc 1, stdout empty.
        (R5, the _OUTSIDE_CLIS row, is test_commands_manifest's own failure: not duplicated here.)
"""
from __future__ import annotations

import itertools
import re
import subprocess
import sys

import pytest

from tests import test_nest as base
from tests.test_nest import Repo, node, nest, slice_of          # the throwaway repo + the reader runner of the first lane

MINT_B = "b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0"
MINT_R = "0123456789abcdef0123456789abcdef"


@pytest.fixture
def repo(tmp_path):
    return Repo(tmp_path / "r")


def _hang_guard(repo, verb, n):
    """nest.py with a 20 s wall: a cycle that does not terminate FAILS, never hangs the suite."""
    if not base.NEST.is_file():
        pytest.fail(f"nest.py is not built: {base.NEST} does not exist")
    try:
        r = subprocess.run([sys.executable, str(base.NEST), verb, "HEAD", n], cwd=repo.d, env=repo.env,
                           capture_output=True, text=True, timeout=20)
    except subprocess.TimeoutExpired:
        pytest.fail(f"nest.py {verb} {n} did not terminate in 20 s")
    assert r.returncode == 0, r.stderr[-300:]
    return sorted(r.stdout.split())


# =============================== R1: order-dependent walk ===============================
def _r1_fixture(repo, order, tail=False):
    """a{nest: order} b{nest: subtree} x{parents:[b]} y{parents:[x]} [z{parents:[y]}]: b's subtree is x, y (z)."""
    repo.w(".agi/nodes/goal/b.md", node("goal:b", nest="subtree"), "b")
    repo.w(".agi/nodes/goal/x.md", node("goal:x", ["goal:b"]), "x")
    repo.w(".agi/nodes/goal/y.md", node("goal:y", ["goal:x"]), "y")
    if tail:
        repo.w(".agi/nodes/goal/z.md", node("goal:z", ["goal:y"]), "z")
    repo.w(".agi/nodes/goal/a.md", node("goal:a", nest=list(order)), "a")


def test_r1_a_list_nest_is_the_same_slice_in_either_order(repo, tmp_path):
    _r1_fixture(repo, ["goal:b", "goal:x"])
    one = slice_of(repo, "goal:a")
    other = Repo(tmp_path / "r2")
    _r1_fixture(other, ["goal:x", "goal:b"])
    two = slice_of(other, "goal:a")
    want = ["goal:a", "goal:b", "goal:x", "goal:y"]
    assert (one, two) == (want, want), (one, two)


@pytest.mark.parametrize("order", [["goal:b", "goal:x"], ["goal:x", "goal:b"]], ids=["b-first", "x-first"])
def test_r1_the_slice_is_closed_every_members_slice_is_inside_the_containers(repo, order):
    _r1_fixture(repo, order)
    whole = set(slice_of(repo, "goal:a"))
    bad = {m: sorted(set(slice_of(repo, m)) - whole) for m in sorted(whole)}
    assert not any(bad.values()), bad


@pytest.mark.parametrize("order", list(itertools.permutations(["goal:x", "goal:y", "goal:b"])),
                         ids=lambda o: "-".join(m[5:] for m in o))
def test_r1_two_nest_less_list_members_chained_with_a_subtree_member_in_any_order(repo, order):
    """x child of b, y of x, z of y; x and y are BOTH list members (nest-less, chained), b brings the subtree."""
    _r1_fixture(repo, order, tail=True)
    whole = slice_of(repo, "goal:a")
    assert whole == ["goal:a", "goal:b", "goal:x", "goal:y", "goal:z"], whole
    bad = {m: sorted(set(slice_of(repo, m)) - set(whole)) for m in whole}
    assert not any(bad.values()), bad


def test_r1_a_subtree_cycle_and_a_list_cycle_terminate_with_the_same_slice(repo):
    repo.w(".agi/nodes/goal/a.md", node("goal:a", nest="subtree"), "a")
    repo.w(".agi/nodes/goal/b.md", node("goal:b", ["goal:a"], nest=["goal:a", "goal:c"]), "b")
    repo.w(".agi/nodes/goal/c.md", node("goal:c", ["goal:b"], nest=["goal:b", "goal:c"]), "c")     # c lists itself
    assert _hang_guard(repo, "slice", "goal:a") == ["goal:a", "goal:b", "goal:c"]
    assert _hang_guard(repo, "slice", "goal:c") == ["goal:a", "goal:b", "goal:c"]       # c -> b -> a (subtree) -> b, c
    assert _hang_guard(repo, "log", "goal:a")                                           # log walks the same set


# =============================== R2: a retire that also edits ===============================
SMALL = "---\nid: goal:s1\nparents: []\n---\nsmall\n"
RETIRED = "---\nid: goal:s1\nparents: []\nstatus: deprecated\nretired: edited at the move\n---\nsmall\n"


def _status_of(repo, rev):
    return [l.split("\t")[0][0] for l in repo.g("show", "--name-status", "--format=", "-M", rev).splitlines()]


def _small_member(repo):
    repo.w(".agi/nodes/goal/s1.md", SMALL, "s1-add")
    repo.w(".agi/nodes/doc/x.md", node("doc:x", nest=["goal:s1"]), "x-collapse")


def test_r2_a_retire_that_also_edits_the_node_keeps_the_add_and_the_retire_in_log(repo):
    _small_member(repo)
    (repo.d / ".agi/nodes/deprecated/goal").mkdir(parents=True)
    repo.g("mv", ".agi/nodes/goal/s1.md", ".agi/nodes/deprecated/goal/s1.md")
    (repo.d / ".agi/nodes/deprecated/goal/s1.md").write_text(RETIRED)
    repo.g("add", "-A")
    repo.g("commit", "-q", "-m", "s1-retire-and-edit")
    assert sorted(_status_of(repo, "HEAD")) == ["A", "D"], "fixture error: git paired the move as a rename"
    got = repo.subjects(nest(repo, "log", "doc:x"))
    assert got == ["s1-retire-and-edit", "x-collapse", "s1-add"], got


def test_r2_a_clean_small_move_still_maps(repo):
    _small_member(repo)
    (repo.d / ".agi/nodes/deprecated/goal").mkdir(parents=True)
    repo.g("mv", ".agi/nodes/goal/s1.md", ".agi/nodes/deprecated/goal/s1.md")
    repo.g("commit", "-q", "-m", "s1-retire")
    assert _status_of(repo, "HEAD") == ["R"], "fixture error: a clean move is not an R line"
    assert repo.subjects(nest(repo, "log", "doc:x")) == ["s1-retire", "x-collapse", "s1-add"]


def test_r2_a_delete_and_an_add_of_different_basenames_is_not_one_nodes_move(repo):
    other = "---\nid: goal:t1\nparents: []\n---\nthe other node, with nothing in common with the member beside this line\n"
    member = "---\nid: goal:s1\nstatus: deprecated\nparents: []\n---\n" + "".join(f"member line {i}\n" for i in range(8))
    repo.w(".agi/nodes/goal/t1.md", other, "t1-add")
    repo.w(".agi/nodes/doc/x.md", node("doc:x", nest=["goal:s1"]), "x-collapse")
    (repo.d / ".agi/nodes/goal/t1.md").unlink()
    (repo.d / ".agi/nodes/deprecated/goal").mkdir(parents=True)
    (repo.d / ".agi/nodes/deprecated/goal/s1.md").write_text(member)
    repo.g("add", "-A")
    repo.g("commit", "-q", "-m", "t1-removed-s1-added")
    assert sorted(_status_of(repo, "HEAD")) == ["A", "D"], "fixture error: git paired the two files"
    got = repo.subjects(nest(repo, "log", "doc:x"))
    assert "t1-add" not in got, f"another node's history entered the log through a D+A of different names: {got}"
    assert "t1-removed-s1-added" in got and "x-collapse" in got, got


# =============================== R3: mint ids in a list ===============================
def _mint_fixture(repo, nest_cell):
    repo.w(".agi/nodes/goal/b.md", node("goal:b", extra=f"mint_id: {MINT_B}\n"), "b-add")
    repo.w(".agi/nodes/doc/x.md", "---\nid: doc:x\n" + nest_cell + "---\nbody\n", "x-collapse")


MINT_SHAPES = {
    "list-form": f"nest: [{MINT_B}, goal:b]\n",
    "list-form-mint-only": f"nest: [{MINT_B}]\n",
    "dash-list": f"nest:\n  - {MINT_B}\n",
}


@pytest.mark.parametrize("cell", list(MINT_SHAPES.values()), ids=list(MINT_SHAPES))
def test_r3_a_mint_id_in_a_nest_list_puts_its_node_in_the_slice(repo, cell):
    _mint_fixture(repo, cell)
    assert "goal:b" in slice_of(repo, "doc:x"), slice_of(repo, "doc:x")


def test_r3_a_mint_id_entry_brings_the_nodes_history_into_log(repo):
    _mint_fixture(repo, MINT_SHAPES["dash-list"])
    assert repo.subjects(nest(repo, "log", "doc:x")) == ["x-collapse", "b-add"]


def test_r3_a_mint_id_entry_expands_the_nodes_own_nest(repo):
    repo.w(".agi/nodes/goal/c.md", node("goal:c"), "c-add")
    repo.w(".agi/nodes/goal/b.md", node("goal:b", nest=["goal:c"], extra=f"mint_id: {MINT_B}\n"), "b-add")
    repo.w(".agi/nodes/doc/x.md", f"---\nid: doc:x\nnest: [{MINT_B}]\n---\n", "x-collapse")
    assert slice_of(repo, "doc:x") == ["doc:x", "goal:b", "goal:c"]


def test_r3_an_entry_that_is_neither_an_id_nor_a_mint_is_absent_from_the_slice(repo):
    _mint_fixture(repo, f"nest: [{MINT_B}, goal:nowhere, {MINT_R}]\n")
    got = slice_of(repo, "doc:x")
    assert got == ["doc:x", "goal:b"], got


def test_r3_a_mint_string_equal_to_another_nodes_id_the_exact_id_wins(repo):
    repo.w(".agi/nodes/goal/q.md", f"---\nid: {MINT_R}\nparents: []\n---\nq\n", "q-add")         # an id spelled like a mint
    repo.w(".agi/nodes/goal/r.md", node("goal:r", extra=f"mint_id: {MINT_R}\n"), "r-add")        # the node that MINTED it
    repo.w(".agi/nodes/doc/x.md", f"---\nid: doc:x\nnest: [{MINT_R}]\n---\n", "x-collapse")
    got = slice_of(repo, "doc:x")
    assert got == sorted(["doc:x", MINT_R]), got


# --- the check's side of R3: nest_unresolved reads the same two spellings the reader must ---
def _links_corpus(tmp_path, cell):
    return base._corpus(tmp_path, {"goal/a.md": base._goal("a", cell), "goal/b.md": base._goal("b")})


B_MINT = "b".ljust(32, "0")       # base._goal mints "<id>" padded with zeros


@pytest.mark.parametrize("cell", [f"nest: [{B_MINT}]\n", f"nest:\n  - {B_MINT}\n"], ids=["list-form", "dash-list"])
def test_r3_nest_unresolved_resolves_a_mint_id_in_either_list_spelling(tmp_path, cell):
    import links
    assert list(links.nest_unresolved(_links_corpus(tmp_path, cell))) == []


@pytest.mark.parametrize("cell", [f"nest: [{B_MINT}, {MINT_R}]\n", f"nest:\n  - {B_MINT}\n  - {MINT_R}\n"],
                         ids=["list-form", "dash-list"])
def test_r3_nest_unresolved_names_an_entry_that_is_neither_id_nor_mint(tmp_path, cell):
    import links
    got = [str(x) for x in links.nest_unresolved(_links_corpus(tmp_path, cell))]
    assert len(got) == 1 and "goal:a" in got[0] and MINT_R in got[0], got


# =============================== R4: the command line (DG1 [amend] 04:23Z) ===============================
USAGE = "nest.py slice|log REV ID"


def _run(args, cwd, env=None):
    if not base.NEST.is_file():
        pytest.fail(f"nest.py is not built: {base.NEST} does not exist")
    return subprocess.run([sys.executable, str(base.NEST), *args], cwd=cwd, env=env, capture_output=True, text=True,
                          timeout=30)


@pytest.mark.parametrize("flag", ["--help", "-h"])
def test_r4_help_prints_the_usage_line_on_stdout_and_exits_0(tmp_path, flag):
    r = _run([flag], tmp_path)                                  # no repo needed to ask for help
    assert r.returncode == 0, (r.returncode, r.stderr[-200:])
    assert USAGE in r.stdout, r.stdout


def test_r4_no_arguments_is_the_usage_line_on_stderr_rc_2_and_nothing_on_stdout(tmp_path):
    r = _run([], tmp_path)
    assert (r.returncode, r.stdout) == (2, ""), (r.returncode, r.stdout)
    assert USAGE in r.stderr, r.stderr


@pytest.mark.parametrize("args", [["bogus", "HEAD", "goal:a"], ["slice", "HEAD"], ["slice"], ["log", "HEAD", "goal:a", "extra"]],
                         ids=["unknown-verb", "missing-id", "missing-rev-and-id", "extra-argument"])
def test_r4_an_unknown_verb_or_the_wrong_argument_count_is_usage_on_stderr_rc_2(repo, args):
    repo.build()
    r = _run(args, repo.d, repo.env)
    assert (r.returncode, r.stdout) == (2, ""), (r.returncode, r.stdout, r.stderr[-200:])
    assert USAGE in r.stderr, r.stderr


@pytest.mark.parametrize("verb", ["slice", "log"])
def test_r4_an_id_in_neither_id_nor_mint_id_is_named_on_stderr_rc_1_and_stdout_is_empty(repo, verb):
    repo.build()
    r = _run([verb, "HEAD", "no:such"], repo.d, repo.env)
    assert (r.returncode, r.stdout) == (1, ""), (r.returncode, r.stdout, r.stderr[-200:])
    assert "nest: unknown id no:such" in r.stderr, r.stderr


@pytest.mark.parametrize("verb", ["slice", "log"])
def test_r4_a_known_id_still_exits_0_with_output(repo, verb):
    repo.build()
    r = _run([verb, "HEAD", "goal:a"], repo.d, repo.env)
    assert r.returncode == 0 and r.stdout.strip() and not r.stderr, (r.returncode, r.stdout, r.stderr[-200:])


def test_r4_a_mint_id_is_a_known_id_for_the_container_too(repo):
    _mint_fixture(repo, MINT_SHAPES["dash-list"])
    by_id, by_mint = _run(["slice", "HEAD", "goal:b"], repo.d, repo.env), _run(["slice", "HEAD", MINT_B], repo.d, repo.env)
    assert by_mint.returncode == 0 and by_mint.stdout == by_id.stdout and by_id.stdout.strip(), (by_id, by_mint)


# =============================== RD-1: pair a D + A by the normalized path, not the basename ===============================
def _swap_fixture(repo):
    """experiment:foo has two commits; doc:x nests hypothesis:foo (which does not exist yet); ONE commit then adds
    hypothesis/foo.md and deletes experiment/foo.md (different contents, so git shows D + A)."""
    repo.w(".agi/nodes/experiment/foo.md", "---\nid: experiment:foo\nparents: []\n---\n" + "".join(f"experiment line {i}\n" for i in range(8)), "c1")
    repo.w(".agi/nodes/experiment/foo.md", "---\nid: experiment:foo\nparents: []\n---\n" + "".join(f"experiment edit {i}\n" for i in range(9)), "c2")
    repo.w(".agi/nodes/doc/x.md", node("doc:x", nest=["hypothesis:foo"]), "x-collapse")
    (repo.d / ".agi/nodes/experiment/foo.md").unlink()
    (repo.d / ".agi/nodes/hypothesis").mkdir(parents=True)
    (repo.d / ".agi/nodes/hypothesis/foo.md").write_text("---\nid: hypothesis:foo\nparents: []\n---\n" + "".join(f"hypothesis text {i}\n" for i in range(7)))
    repo.g("add", "-A")
    repo.g("commit", "-q", "-m", "h-swap")


def test_rd1_an_add_and_a_delete_of_the_same_basename_in_different_type_dirs_is_not_one_nodes_move(repo):
    _swap_fixture(repo)
    assert sorted(_status_of(repo, "HEAD")) == ["A", "D"], "fixture error: git paired the swap as a rename"
    got = repo.subjects(nest(repo, "log", "doc:x"))
    assert not {"c1", "c2"} & set(got), f"the experiment's history entered hypothesis:foo's log through a same-basename D + A: {got}"
    assert got == ["h-swap", "x-collapse"], got


def _history_then_swap(repo, old, new, member):
    """`member` has two commits at `old`, doc:x nests it, then ONE commit deletes `old` and adds `new` with a rewritten body (D + A)."""
    a = f"---\nid: {member}\nparents: []\n---\n" + "".join(f"first body {i}\n" for i in range(8))
    b = f"---\nid: {member}\nparents: []\n---\n" + "".join(f"second body {i}\n" for i in range(9))
    c = f"---\nid: {member}\nparents: []\n---\n" + "".join(f"rewritten at the move {i}\n" for i in range(7))
    repo.w(old, a, "m1")
    repo.w(old, b, "m2")
    repo.w(".agi/nodes/doc/x.md", node("doc:x", nest=[member]), "x-collapse")
    (repo.d / old).unlink()
    (repo.d / new).parent.mkdir(parents=True, exist_ok=True)
    (repo.d / new).write_text(c)
    repo.g("add", "-A")
    repo.g("commit", "-q", "-m", "m-move-and-edit")
    assert sorted(_status_of(repo, "HEAD")) == ["A", "D"], "fixture error: git paired the move as a rename"


@pytest.mark.parametrize("old,new", [(".agi/nodes/goal/f.md", ".agi/nodes/deprecated/goal/f.md"),
                                     (".agi/nodes/deprecated/goal/f.md", ".agi/nodes/goal/f.md")], ids=["retire", "un-retire"])
def test_rd1_a_retire_edit_d_plus_a_maps_in_both_directions(repo, old, new):
    _history_then_swap(repo, old, new, "goal:f")
    got = repo.subjects(nest(repo, "log", "doc:x"))
    assert got == ["m-move-and-edit", "x-collapse", "m2", "m1"], got


# =============================== RD-3: a malformed nest value is refused, and reported ===============================
MALFORMED = {"capital-Subtree": "Subtree", "trailing-comment": "subtree # x", "bare-id": "hypothesis:bar"}
VALID = {"subtree": "subtree", "inline-list": "[goal:b]", "empty": ""}


def _nest_cell_repo(repo, value):
    repo.w(".agi/nodes/goal/b.md", node("goal:b"), "b-add")
    repo.w(".agi/nodes/doc/x.md", f"---\nid: doc:x\nnest: {value}\n---\nbody\n".replace("nest: \n", "nest:\n"), "x-collapse")


@pytest.mark.parametrize("verb", ["slice", "log"])
@pytest.mark.parametrize("value", list(MALFORMED.values()), ids=list(MALFORMED))
def test_rd3_a_malformed_nest_value_exits_1_and_says_so(repo, verb, value):
    _nest_cell_repo(repo, value)
    r = _run([verb, "HEAD", "doc:x"], repo.d, repo.env)
    assert (r.returncode, r.stdout) == (1, ""), (r.returncode, r.stdout, r.stderr[-200:])
    assert "nest: malformed nest" in r.stderr and value in r.stderr, r.stderr


@pytest.mark.parametrize("verb", ["slice", "log"])
@pytest.mark.parametrize("value", list(VALID.values()), ids=list(VALID))
def test_rd3_subtree_a_list_and_an_empty_cell_still_pass(repo, verb, value):
    _nest_cell_repo(repo, value)
    r = _run([verb, "HEAD", "doc:x"], repo.d, repo.env)
    assert r.returncode == 0 and r.stdout.strip() and "malformed" not in r.stderr, (r.returncode, r.stdout, r.stderr[-200:])


MAL_CORPUS = {
    "goal/a1.md": base._goal("a1", "nest: Subtree\n"),
    "goal/a2.md": base._goal("a2", "nest: subtree # x\n"),
    "goal/a3.md": base._goal("a3", "nest: goal:bar\n"),
    "goal/ok1.md": base._goal("ok1", "nest: subtree\n"),
    "goal/ok2.md": base._goal("ok2", "nest: [goal:ok1]\n"),
    "goal/ok3.md": base._goal("ok3"),
}


def test_rd3_links_reports_each_malformed_value_on_its_own_line_and_a_count(tmp_path):
    root = base._corpus(tmp_path, MAL_CORPUS)
    rc, out = base._links_main(root)
    lines = out.splitlines()
    for nid, value in (("goal:a1", "Subtree"), ("goal:a2", "subtree # x"), ("goal:a3", "goal:bar")):
        own = [l for l in lines if nid in l and value in l]
        assert len(own) == 1, (nid, value, out)
    counts = [re.fullmatch(r"nest[_-]?malformed:?\s*(\d+)", l.strip()) for l in lines]
    assert [int(m[1]) for m in counts if m] == [3], f"ONE count line `nest_malformed: 3` (the rows are not it): {out}"
    assert not [l for l in lines if re.search(r"goal:ok[123]", l) and "nest" in l.lower()], out      # the valid shapes are not reported


def test_rd3_a_malformed_nest_never_enters_count_broken_links(tmp_path):
    import links
    with_bad = base._corpus(tmp_path / "w", MAL_CORPUS)
    clean = base._corpus(tmp_path / "n", {k: v for k, v in MAL_CORPUS.items() if "/ok" in k})
    assert links.count_broken_links(with_bad) == links.count_broken_links(clean) == 0


# =============================== RD-2 (as shipped): `slice` prints sorted, unique ids, nothing else ===============================
def test_rd2_slice_prints_sorted_unique_ids_one_per_line(repo):
    repo.w(".agi/nodes/goal/b.md", node("goal:b"), "b-add")
    repo.w(".agi/nodes/goal/a.md", node("goal:a"), "a-add")
    repo.w(".agi/nodes/doc/x.md", node("doc:x", nest=["goal:b", "goal:a", "goal:b"]), "x-collapse")   # b listed twice
    r = _run(["slice", "HEAD", "doc:x"], repo.d, repo.env)
    lines = r.stdout.splitlines()
    assert r.returncode == 0 and lines == sorted(set(lines)) == ["doc:x", "goal:a", "goal:b"], (r.returncode, lines)


def test_rd3_the_metrics_cell_counts_the_malformed_values_beside_an_unchanged_broken_links(tmp_path):
    """nest_unresolved has its metrics cell; its sibling gets one: N on a graph with N malformed values, 0 on a clean one."""
    m = base._metrics(base._corpus(tmp_path / "bad", MAL_CORPUS))
    assert m.get("nest_malformed") == "3", m
    assert m.get("broken_links") == "0", m
    clean = base._metrics(base._corpus(tmp_path / "ok", {k: v for k, v in MAL_CORPUS.items() if "/ok" in k}))
    assert clean.get("nest_malformed") == "0", clean

