"""Tests for bin/verify_unified.py — the independent goal:g11 checker.

Every fixture below is a REAL git repo built in `tmp_path`, never a mock of
git: `verify_unified.py`'s entire value is trustworthiness against a repo
something else may have just mutated, and a mocked `subprocess.run` proves
nothing about that. The "good pair" fixture is built once by
`make_unified_pair` and every negative test starts from a fresh copy of it,
then breaks exactly one invariant — so a failure in one test can never be
explained by a fixture bug shared with another.

This file must not import anything from `unify.py` or `test_unify.py` — that
is kid-g's migrator, and the whole point of writing this checker separately
is that it does not share a bug with the thing it checks.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

_spec = importlib.util.spec_from_file_location("verify_unified", BIN / "verify_unified.py")
verify_unified = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(verify_unified)


# --- git helpers -----------------------------------------------------------


def _git(repo: Path, *args: str) -> str:
    res = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"git -C {repo} {' '.join(args)} failed: {res.stderr}")
    return res.stdout


def _init_repo(repo: Path) -> None:
    repo.mkdir(parents=True, exist_ok=True)
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")


def _commit_all(repo: Path, message: str) -> str:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", message)
    return _git(repo, "rev-parse", "HEAD").strip()


NODE_A = '---\nid: "idea:a"\ntype: idea\n---\n\nfirst thought\n'
NODE_GEOM = '---\nid: "geometry:g"\ntype: geometry\n---\n\ngeometry node\n'
NODE_BUILD = (
    '---\nid: "build:thing"\ntype: build\n'
    'payload_ref: extensions/agi/bin/thing.py\n---\n\nbuild node\n'
)
PAYLOAD_BYTES = b"# thing.py\nprint('hi')\n"


# --- the "before" graph repo -------------------------------------------------


def make_before(tmp_path: Path, name: str = "graph") -> Path:
    """A small pre-migration graph repo: `nodes/`, a dot-directory node
    (`nodes/.geometry/`, the exact shape a two-level glob would miss), one
    build node with a `payload_ref`, and one grid ref."""
    repo = tmp_path / name
    _init_repo(repo)
    (repo / "agi-tree.config.json").write_text("{}")
    (repo / "nodes" / "idea").mkdir(parents=True)
    (repo / "nodes" / "build").mkdir(parents=True)
    (repo / "nodes" / ".geometry").mkdir(parents=True)
    (repo / "nodes" / "idea" / "a.md").write_text(NODE_A)
    (repo / "nodes" / "build" / "thing.md").write_text(NODE_BUILD)
    (repo / "nodes" / ".geometry" / "g.md").write_text(NODE_GEOM)
    tip = _commit_all(repo, "seed graph")
    _git(repo, "update-ref", "refs/grid/node/idea-a", tip)
    _git(repo, "update-ref", "refs/grid/node/build-thing", tip)
    return repo


# --- the "after" unified repo, correctly built from a "before" -------------


def make_after(tmp_path: Path, before: Path, name: str = "unified") -> Path:
    """A correctly migrated unified repo: `before`'s tip is grafted in as an
    ancestor via `commit-tree` (real ancestry, not a lookalike commit), grid
    refs are carried over via a plain ref-namespace fetch, node bytes are
    copied unchanged, and the build node's payload is placed where its
    (unchanged) `payload_ref` says it should resolve under the new
    `source_root` — the repo root itself, per `locations.py`."""
    repo = tmp_path / name
    _init_repo(repo)
    _git(repo, "remote", "add", "before", str(before))
    _git(repo, "fetch", "-q", "before", "HEAD")
    before_tip = _git(repo, "rev-parse", "FETCH_HEAD").strip()
    _git(repo, "fetch", "-q", "before", "+refs/grid/*:refs/grid/*")

    agi = repo / ".agi"
    (agi / "nodes").mkdir(parents=True)
    for rel in ("idea/a.md", "build/thing.md", ".geometry/g.md"):
        src = before / "nodes" / rel
        dst = agi / "nodes" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())
    (agi / "config.json").write_text("{}")
    (repo / "GOALS.md").write_text("# Goals\n")

    payload_dir = repo / "extensions" / "agi" / "bin"
    payload_dir.mkdir(parents=True)
    (payload_dir / "thing.py").write_bytes(PAYLOAD_BYTES)

    _git(repo, "add", "-A")
    tree = _git(repo, "write-tree").strip()
    commit = _git(repo, "commit-tree", tree, "-p", before_tip, "-m", "unify").strip()
    _git(repo, "update-ref", "HEAD", commit)
    return repo


@pytest.fixture()
def good_pair(tmp_path):
    before = make_before(tmp_path, "graph")
    after = make_after(tmp_path, before, "unified")
    return before, after


# --- the good pair passes every check ---------------------------------------


def test_good_pair_passes_every_check(good_pair):
    before, after = good_pair
    results = verify_unified.run_all(before, after)
    failed = [r.name for r in results if not r.passed]
    assert failed == [], f"unexpected failures: {[(r.name, r.message) for r in results if not r.passed]}"
    assert len(results) == 8


def test_good_pair_cli_exits_zero(good_pair, capsys):
    before, after = good_pair
    rc = verify_unified.main(["--before", str(before), "--after", str(after)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "OK" in out
    assert "FAIL" not in out


def test_good_pair_json_reports_ok_true(good_pair, capsys):
    before, after = good_pair
    rc = verify_unified.main(["--before", str(before), "--after", str(after), "--json"])
    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    assert data["ok"] is True
    assert len(data["checks"]) == 8
    assert all(c["passed"] for c in data["checks"])


# --- each invariant fails when it should ------------------------------------


def _result(results, name):
    for r in results:
        if r.name == name:
            return r
    raise AssertionError(f"no check named {name!r} among {[r.name for r in results]}")


def test_deleted_node_fails_count_check(tmp_path):
    before = make_before(tmp_path, "graph")
    after = make_after(tmp_path, before, "unified")
    (after / ".agi" / "nodes" / ".geometry" / "g.md").unlink()

    results = verify_unified.run_all(before, after)
    assert _result(results, "no_node_lost").passed is False
    # deleting a file also changes the hash-map diff, but the count check is
    # the one this test names and must fail on its own.
    detail = _result(results, "no_node_lost").detail
    assert detail["before_count"] == 3 and detail["after_count"] == 2


def test_flipped_byte_fails_bytes_check_without_changing_count(tmp_path):
    before = make_before(tmp_path, "graph")
    after = make_after(tmp_path, before, "unified")
    target = after / ".agi" / "nodes" / "idea" / "a.md"
    target.write_text(target.read_text().replace("first thought", "FIRST THOUGHT"))

    results = verify_unified.run_all(before, after)
    assert _result(results, "no_node_lost").passed is True
    bytes_check = _result(results, "no_node_bytes_changed")
    assert bytes_check.passed is False
    assert bytes_check.detail["diverged_count"] == 1
    assert "idea/a.md" in bytes_check.detail["offending_paths"][0]


def test_dropped_grid_ref_fails_as_missing(tmp_path):
    before = make_before(tmp_path, "graph")
    after = make_after(tmp_path, before, "unified")
    _git(after, "update-ref", "-d", "refs/grid/node/idea-a")

    results = verify_unified.run_all(before, after)
    ref_check = _result(results, "no_grid_ref_lost")
    assert ref_check.passed is False
    assert ref_check.detail["missing"] == ["refs/grid/node/idea-a"]
    assert ref_check.detail["diverged"] == []


def test_diverged_grid_ref_fails_differently_than_missing(tmp_path):
    before = make_before(tmp_path, "graph")
    after = make_after(tmp_path, before, "unified")
    # Point the ref at a different, real object in the same repo (the root
    # commit's tree) rather than deleting it — this must show up as DIVERGED,
    # not MISSING, because the name is still there.
    after_head = _git(after, "rev-parse", "HEAD").strip()
    _git(after, "update-ref", "refs/grid/node/idea-a", after_head)

    results = verify_unified.run_all(before, after)
    ref_check = _result(results, "no_grid_ref_lost")
    assert ref_check.passed is False
    assert ref_check.detail["missing"] == []
    assert ref_check.detail["diverged"] == ["refs/grid/node/idea-a"]


def test_unrelated_histories_fails_ancestry_check(tmp_path):
    before = make_before(tmp_path, "graph")
    # An "after" repo built completely fresh, with no relationship at all to
    # `before`'s history — the migration is supposed to graft `before`'s tip
    # in as an ancestor, and this fixture deliberately does not.
    after = tmp_path / "unrelated"
    _init_repo(after)
    (after / ".agi" / "nodes").mkdir(parents=True)
    (after / ".agi" / "config.json").write_text("{}")
    (after / "GOALS.md").write_text("# Goals\n")
    _commit_all(after, "independent history")

    results = verify_unified.run_all(before, after)
    hist_check = _result(results, "both_histories_present")
    assert hist_check.passed is False
    assert hist_check.detail["graph_tip_is_ancestor_of_after_head"] is False


def test_goals_left_inside_dot_agi_fails(tmp_path):
    before = make_before(tmp_path, "graph")
    after = make_after(tmp_path, before, "unified")
    (after / "GOALS.md").unlink()
    (after / ".agi" / "GOALS.md").write_text("# Goals\n")

    results = verify_unified.run_all(before, after)
    goals_check = _result(results, "goals_at_repo_root")
    assert goals_check.passed is False
    assert goals_check.detail["at_root"] is False
    assert goals_check.detail["inside_graph_dir"] is True


def test_unresolvable_payload_ref_fails(tmp_path):
    before = make_before(tmp_path, "graph")
    after = make_after(tmp_path, before, "unified")
    (after / "extensions" / "agi" / "bin" / "thing.py").unlink()

    results = verify_unified.run_all(before, after)
    payload_check = _result(results, "payload_refs_resolve")
    assert payload_check.passed is False
    assert payload_check.detail["checked"] == 1
    assert payload_check.detail["unresolved"][0]["payload_ref"] == "extensions/agi/bin/thing.py"


def test_missing_config_json_fails(tmp_path):
    before = make_before(tmp_path, "graph")
    after = make_after(tmp_path, before, "unified")
    (after / ".agi" / "config.json").unlink()

    results = verify_unified.run_all(before, after)
    assert _result(results, "config_at_expected_path").passed is False


def test_malformed_config_json_fails(tmp_path):
    before = make_before(tmp_path, "graph")
    after = make_after(tmp_path, before, "unified")
    (after / ".agi" / "config.json").write_text("{ this is not json")

    results = verify_unified.run_all(before, after)
    cfg_check = _result(results, "config_at_expected_path")
    assert cfg_check.passed is False
    assert cfg_check.detail["exists"] is True
    assert cfg_check.detail["parses"] is False


def test_resolver_disagrees_when_dot_agi_has_no_config(tmp_path):
    before = make_before(tmp_path, "graph")
    after = make_after(tmp_path, before, "unified")
    (after / ".agi" / "config.json").unlink()

    results = verify_unified.run_all(before, after)
    resolver_check = _result(results, "resolver_agrees")
    assert resolver_check.passed is False


def test_cli_exits_nonzero_and_names_failing_checks(tmp_path, capsys):
    before = make_before(tmp_path, "graph")
    after = make_after(tmp_path, before, "unified")
    (after / ".agi" / "nodes" / ".geometry" / "g.md").unlink()

    rc = verify_unified.main(["--before", str(before), "--after", str(after)])
    assert rc == 1
    out = capsys.readouterr().out
    assert "[FAIL] no_node_lost" in out
    assert "FAILED" in out


# --- the checker never writes ------------------------------------------------


def _snapshot(repo: Path) -> tuple[str | None, list[str]]:
    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                           capture_output=True, text=True)
    head_sha = head.stdout.strip() if head.returncode == 0 else None
    refs = _git(repo, "for-each-ref", "--format=%(refname) %(objectname)").splitlines()
    return head_sha, sorted(refs)


def test_checker_never_writes_to_either_repo(good_pair):
    before, after = good_pair
    before_snapshot = _snapshot(before)
    after_snapshot = _snapshot(after)

    rc = verify_unified.main(["--before", str(before), "--after", str(after), "--json"])
    assert rc == 0

    assert _snapshot(before) == before_snapshot
    assert _snapshot(after) == after_snapshot


def test_checker_never_writes_even_on_a_failing_run(tmp_path):
    before = make_before(tmp_path, "graph")
    after = make_after(tmp_path, before, "unified")
    (after / ".agi" / "nodes" / "idea" / "a.md").unlink()

    before_snapshot = _snapshot(before)
    after_snapshot = _snapshot(after)

    rc = verify_unified.main(["--before", str(before), "--after", str(after)])
    assert rc == 1

    assert _snapshot(before) == before_snapshot
    assert _snapshot(after) == after_snapshot


# --- robustness: a broken "after" reports failures, never a traceback ------


def test_after_with_no_dot_agi_reports_named_failures_not_a_crash(tmp_path):
    before = make_before(tmp_path, "graph")
    after = tmp_path / "plain-clone"
    _init_repo(after)
    (after / "README.md").write_text("just a plain repo\n")
    _commit_all(after, "plain")

    results = verify_unified.run_all(before, after)
    assert len(results) == 8
    names = {r.name for r in results}
    assert names == {
        "no_node_lost", "no_node_bytes_changed", "no_grid_ref_lost",
        "both_histories_present", "resolver_agrees", "goals_at_repo_root",
        "payload_refs_resolve", "config_at_expected_path",
    }
    assert _result(results, "no_node_lost").passed is False
    assert _result(results, "resolver_agrees").passed is False
    assert _result(results, "goals_at_repo_root").passed is False
    assert _result(results, "config_at_expected_path").passed is False


def test_payload_ref_count_loss_is_not_a_vacuous_pass(good_pair):
    """Parent review, iteration 3 — the vacuous-pass hole.

    `check_payload_refs` originally passed whenever nothing was left to
    resolve, so a migration that dropped every build node reported
    "0 checked, 0 unresolved" in exactly the same green as a correct run.
    That was observed live: in the sanity run against a never-migrated clone,
    where seven checks failed, this was the one that passed. A verifier whose
    checks get *easier* as more is lost is worse than no verifier, because it
    is trusted.
    """
    before, after = good_pair
    (after / ".agi" / "nodes" / "build" / "thing.md").unlink()

    res = verify_unified.check_payload_refs(before, after)
    assert res.passed is False
    assert res.detail["checked"] == 0
    assert res.detail["before_count"] == 1
    assert "COUNT MISMATCH" in res.message


def test_payload_ref_count_match_still_passes(good_pair):
    """The counterpart: an untouched correct pair still passes, so the new
    count invariant did not simply make the check impossible to satisfy."""
    before, after = good_pair
    res = verify_unified.check_payload_refs(before, after)
    assert res.passed is True
    assert res.detail["checked"] == res.detail["before_count"] == 1
