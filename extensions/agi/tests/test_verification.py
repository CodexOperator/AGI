"""Tests for `bin/verification.py` (hypothesis:l4-unified-verification).

This is the NEW file's own test. It covers the four sharp edges that decide
the round:

1. **No argv hardcoded.** The ONE invariant: every check's argv comes from
   `commands.py` resolving `command:commands`, never written literally here.
   A `verification.py` with its own copy of an argv the node already declares
   is the fifth copy of the prose — the one people trust — and is a disprove
   even if every other test is green. So the sharpest test GREPS THE MODULE
   for the declared argv fragments and asserts they are absent.
2. **The count check is a comparison, not a print.** A baseline under
   `.agi/sessions/`, FAIL below it, update on equal-or-greater, record-on-first.
3. **`--suite` is opt-in and orthogonal.** Only appended to a level when the
   flag is present; its absence is never a failure.
4. **`--json` carries the same facts the summary does.** No prose-only field.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import locations  # noqa: E402
import verification  # noqa: E402


class _StubProc:
    """A minimal subprocess result twin for guards that must be asserted to
    NEVER invoke subprocess.run on the refusal path."""
    returncode = 0
    stdout = ""
    stderr = ""

VERIFY_SOURCE = (BIN / "verification.py").read_text(encoding="utf-8")

# Decimal argv fragments declared in the node. If any of these appears
# literally in verification.py, the round is disproved: the tool has become
# the fifth copy of the prose it was built to remove.
DECLARED_ARGV_FRAGMENTS = [
    "write_guard.py check",
    "driver.sh --smoke",
    "links.py links",
    "dispatch.py --help",
    "snapshot-goals.py --render",
    "viewport.py --verify",
    "spawn_budget.py status",
    "envfile.py --check",
    "provisioning.py status",
    "crons.py show",
]


def test_docstring_disambiguates_from_verify_unified():
    """The two names are one keystroke apart; the docstring must say so first."""
    first_two = "\n".join(VERIFY_SOURCE.splitlines()[:6])
    assert "verify_unified" in first_two, "first paragraph must name the twin"
    assert "NOT" in first_two or "not" in first_two


def test_no_declared_argv_is_literal_in_verification_py():
    """THE invariant — resolution through the node, never a hardcoded argv."""
    for frag in DECLARED_ARGV_FRAGMENTS:
        assert frag not in VERIFY_SOURCE, (
            f"declared argv {frag!r} written literally — ",
            f"the fifth copy of the prose (goal:g1.10)")


def test_every_level_member_is_a_resolvable_command_name():
    """A level that names a command the node has not declared would be drifted
    graph; names must be names (dict keys), never argv."""
    known = {"links", "goals-check", "write-guard", "smoke",
             "viewport-verify", "dispatch-help", "budget", "schema",
             "credentials", "secrets", "crons", "tests"}
    for level_names in verification.LEVELS.values():
        for n in level_names:
            assert n in known, f"{n!r} is not a declared command name"


def test_levels_compose_superset_to_superset():
    assert set(verification.LEVELS["rotation"]) >= set(verification.LEVELS["quick"])
    assert set(verification.LEVELS["full"]) >= set(verification.LEVELS["rotation"])
    assert "tests" not in set().union(*verification.LEVELS.values()), (
        "no level may fold the suite in — --suite is opt-in until L4.10")


def test_parse_number_smoke(tmp_path):
    out = "METRIC active_node_count=1707\nMETRIC deprecated_node_count=194\nMETRIC node_count=1901\n"
    assert verification._parse_number("smoke", 0, out) == {
        "active": 1707, "deprecated": 194, "total": 1901}


def test_parse_number_links_and_goals(tmp_path):
    assert verification._parse_number("links", 0, "links: 1881 resolved, 0 broken")["broken"] == 0
    assert verification._parse_number("links", 0, "links: 5 resolved, 2 broken")["broken"] == 2
    assert verification._parse_number("goals-check", 0, "round-trip") == {"byte-identical": 1}
    assert verification._parse_number("goals-check", 1, "MISMATCH") == {"byte-identical": 0}


def test_parse_number_tests_reads_pytest_summary_in_any_order():
    """The `tests` check must carry the number it exists to produce: pytest's
    own counts, in whatever order pytest emits them. A suite that silently
    collected 3 tests must not print the same line as 2340."""
    assert verification._parse_number("tests", 0, "2340 passed in 132.6s") == {"passed": 2340}
    assert verification._parse_number("tests", 0, "1 skipped, 2340 passed in 133.1s") == {
        "passed": 2340, "skipped": 1}
    assert verification._parse_number("tests", 0, "2300 passed, 40 failed in 120.5s") == {
        "passed": 2300, "failed": 40}
    assert verification._parse_number("tests", 0, "3 errors in 1.2s") == {"errors": 3}
    assert verification._parse_number("tests", 0, "1 error in 0.5s") == {"errors": 1}


def test_parse_number_tests_unparseable_is_empty_not_failure():
    """A PASS with no parsed count must not fail the check — pass/fail comes
    from the exit code — but it must be EMPTY so the summary says so rather
    than printing an empty bracket."""
    num = verification._parse_number("tests", 0, "Ran 2340 tests, all OK")
    assert num == {}
    # and _passed still judges tests purely on the exit code, count or no count
    assert verification._passed("tests", 0, {"passed": 2340}) is True
    assert verification._passed("tests", 0, {}) is True
    assert verification._passed("tests", 1, {"passed": 2340}) is False


def test_suite_pass_with_no_parsed_count_names_the_gap(monkeypatch, tmp_path):
    """A green-but-unparseable suite must SAY the count was not parsed, not
    print the same PASS line as a 2340-test run."""
    class _Proc:
        returncode = 0
        stdout = "Ran everything, did not use pytest summary wording\n"
        stderr = ""
    table = {verification.SUITE_CMD: type("C", (), {"argv": ["true"], "cwd": None})()}
    monkeypatch.setattr(verification.commands, "load", lambda groot: table)
    monkeypatch.setattr(verification.subprocess, "run", lambda argv, **kw: _Proc())
    r = verification.run_check(tmp_path, verification.SUITE_CMD, False)
    assert r.status == "PASS"
    assert r.number == {}
    assert "NO count parsed" in r.note


def test_json_carries_pytest_counts_and_roots(tmp_path):
    results = [verification.CheckResult(
        "tests", "PASS", 132.6, {"passed": 2340, "skipped": 1})]
    doc = verification.render_json("rotation", True, results,
                                   graph_root="/g/.agi", engine_root="/e")
    assert doc["checks"][0]["number"] == {"passed": 2340, "skipped": 1}
    assert doc["graph_root"] == "/g/.agi"
    assert doc["engine_root"] == "/e"


def test_summary_states_which_engine_and_graph_root(tmp_path):
    """A report that does not say what it measured is a report you cannot
    cite. The roots line must appear, always, not only when they differ."""
    text = verification.render_summary("rotation", False,
                                       [verification.CheckResult("links", "PASS", 1.0)],
                                       graph_root="/g/.agi", engine_root="/e")
    assert "roots: engine=/e, graph=/g/.agi" in text
    # and absent roots (a bare unit call) do not crash
    verification.render_summary("rotation", False, [])



def test_links_pass_uses_the_count_not_the_exit_code():
    """links exits 0 even with broken links; the broken count is the fact."""
    assert verification._passed("links", 0, {"broken": 0}) is True
    assert verification._passed("links", 0, {"broken": 2}) is False
    assert verification._passed("goals-check", 0, {"byte-identical": 1}) is True


def test_count_first_run_records_and_passes(tmp_path, monkeypatch):
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    # A bare tmp root is not a git tree; force a KEPT context so we exercise
    # the stamping path (kept -> writes) without real git.
    monkeypatch.setattr(verification, "_stamp_context",
                        lambda groot: (True, "abc123", "kept"))
    current = {"active": 1707, "deprecated": 194, "total": 1901}
    r = verification.compare_count(groot, current)
    assert r.status == "PASS"
    assert "baseline recorded" in r.note
    state = json.loads((groot / "sessions" / "verify-count.json").read_text())
    assert state["active"] == current["active"]
    assert state["sha"] == "abc123"
    assert state["stamped_at"] > 0


def test_count_drop_is_a_failure_that_names_the_drop(tmp_path):
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    # a NODE COUNT drop (active AND total below baseline) is still a FAIL;
    # the baseline total is what the gate compares, so it must be set above
    # the incoming total for the drop to register (SM.34/H0/H0b preserved).
    (groot / "sessions" / "verify-count.json").write_text(
        json.dumps({"active": 9999, "deprecated": 0, "total": 9999}))
    r = verification.compare_count(groot, {"active": 1707,
                                           "deprecated": 194, "total": 1901})
    assert r.status == "FAIL"
    assert r.note.startswith("NODE COUNT DROPPED")
    assert "total=1901 below baseline=9999" in r.note
    assert "no committed manifest on record (counts only)" in r.note


def test_count_steady_updates_baseline_and_passes(tmp_path, monkeypatch):
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    (groot / "sessions" / "verify-count.json").write_text(
        json.dumps({"active": 1707, "deprecated": 194, "total": 1901}))
    monkeypatch.setattr(verification, "_stamp_context",
                        lambda groot: (True, "bee", "kept"))
    newer = {"active": 1707, "deprecated": 195, "total": 1902}
    r = verification.compare_count(groot, newer)
    assert r.status == "PASS"
    state = json.loads((groot / "sessions" / "verify-count.json").read_text())
    assert state["active"] == newer["active"]
    assert state["sha"] == "bee"


def _committed_repo(root: Path, files: dict[str, str], branch: str = "mb") -> None:
    """Build a real git tree at `root` with the given committed node files,
    HEAD pushed (a clean committed tree `_node_manifest`/`_committed_deprecated`
    can answer, and `_stamp_context` stays mockable)."""
    sp = subprocess.run
    root.mkdir(parents=True, exist_ok=True)
    sp(["git", "init", "-b", branch], cwd=root, check=True,
       capture_output=True, text=True)
    sp(["git", "config", "user.email", "t@t"], cwd=root, check=True)
    sp(["git", "config", "user.name", "t"], cwd=root, check=True)
    for rel, body in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
    sp(["git", "add", "-A"], cwd=root, check=True, capture_output=True,
       text=True)
    sp(["git", "commit", "-m", "init"], cwd=root, check=True,
       capture_output=True, text=True)


NODE = lambda name: (  # noqa: E731
    f"---\nid: node:{name}\ntype: experiment\nstatus: active\n---\n# {name}\n\n")
DEP_NODE = lambda name: (  # noqa: E731
    f"---\nid: node:{name}\ntype: experiment\nstatus: deprecated\n---\n# {name}\n\n")
MINT_NODE = lambda name, mid: (  # noqa: E731
    f"---\nid: node:{name}\ntype: experiment\nstatus: active\n"
    f"mint_id: {mid}\n---\n# {name}\n\n")
MINT_DEP = lambda name, mid: (  # noqa: E731
    f"---\nid: node:{name}\ntype: experiment\nstatus: deprecated\n"
    f"mint_id: {mid}\n---\n# {name}\n\n")


def _baseline(groot: Path, doc: dict) -> None:
    (groot / "sessions").mkdir(parents=True, exist_ok=True)
    (groot / "sessions" / verification.STATE_FILE).write_text(
        json.dumps(doc))


def test_retire_move_passes_and_restamps(tmp_path, monkeypatch):
    """Fixture (c): a retire pass — active -N, deprecated +N, total unchanged
    — PASSes node-count and re-stamps the baseline. The missing baseline path
    `nodes/experiment/move-me.md` is counted as a MOVE because the deprecated
    twin at HEAD carries the SAME mint id the baseline recorded -- mint id
    equality is the proof, never a basename match."""
    root = tmp_path / "repo"
    groot = root / ".agi"
    _committed_repo(root, {
        # HEAD: move-me has RETIRED — it now lives under deprecated/ with its
        # mint id intact. The stamped manifest (below) still lists it ACTIVE,
        # so the absent baseline path must resolve as a MOVE by mint id.
        ".agi/nodes/deprecated/experiment/move-me.md": MINT_DEP("move-me", "X"),
        ".agi/nodes/hypothesis/h1.md": MINT_NODE("h1", "H1"),
    })
    _baseline(groot, {
        "active": 2, "deprecated": 0, "total": 2,
        "manifest": {"nodes/experiment/move-me.md": "X",
                     "nodes/hypothesis/h1.md": "H1"},
    })
    monkeypatch.setattr(verification, "_stamp_context",
                        lambda groot: (True, "abc123", "kept"))
    r = verification.compare_count(groot, {"active": 1,
                                           "deprecated": 1, "total": 2})
    assert r.status == "PASS", r.note
    assert "moved to deprecated: nodes/experiment/move-me.md" in r.note
    assert "baseline updated" in r.note
    st = json.loads((groot / "sessions" / verification.STATE_FILE).read_text())
    assert st["active"] == 1 and st["deprecated"] == 1 and st["total"] == 2
    assert st["manifest"]["nodes/deprecated/experiment/move-me.md"] == "X"


def test_basename_collision_is_a_named_loss(tmp_path, monkeypatch):
    """(b) The probe the fix exists for: the absent baseline path's deprecated
    twin exists at the exact matching path but carries a DIFFERENT mint id, and
    the compensating arithmetic keeps the total flat. Basename alone would pass
    it; mint id equality makes it a LOSS, named, with the H0/H0b note."""
    root = tmp_path / "repo"
    groot = root / ".agi"
    _committed_repo(root, {
        ".agi/nodes/deprecated/experiment/move-me.md": MINT_DEP("other", "Y"),
        ".agi/nodes/hypothesis/h1.md": MINT_NODE("h1", "H1"),
    })
    _baseline(groot, {
        "active": 2, "deprecated": 0, "total": 2,
        "manifest": {"nodes/experiment/move-me.md": "X",
                     "nodes/hypothesis/h1.md": "H1"},
    })
    monkeypatch.setattr(verification, "_stamp_context",
                        lambda groot: (True, "abc123", "kept"))
    r = verification.compare_count(groot, {"active": 1,
                                           "deprecated": 1, "total": 2})
    assert r.status == "FAIL", r.note
    assert "missing committed file(s): nodes/experiment/move-me.md" in r.note
    assert "H0/H0b: 29k nodes lost to a silent drop" in r.note


def test_absent_mint_id_is_a_loss(tmp_path, monkeypatch):
    """(c) A deprecated twin with NO `mint_id` field proves nothing and is a
    named LOSS, never a silent basename pass."""
    root = tmp_path / "repo"
    groot = root / ".agi"
    _committed_repo(root, {
        ".agi/nodes/deprecated/experiment/move-me.md": DEP_NODE("move-me"),
        ".agi/nodes/hypothesis/h1.md": MINT_NODE("h1", "H1"),
    })
    _baseline(groot, {
        "active": 2, "deprecated": 0, "total": 2,
        "manifest": {"nodes/experiment/move-me.md": "X",
                     "nodes/hypothesis/h1.md": "H1"},
    })
    monkeypatch.setattr(verification, "_stamp_context",
                        lambda groot: (True, "abc123", "kept"))
    r = verification.compare_count(groot, {"active": 1,
                                           "deprecated": 1, "total": 2})
    assert r.status == "FAIL", r.note
    assert "missing committed file(s): nodes/experiment/move-me.md" in r.note


def test_old_list_baseline_proves_nothing_and_is_migrated(tmp_path, monkeypatch):
    """(e) A record written before mint ids (manifest is a LIST) does not
    crash and does NOT silently pass a basename match as a PROVEN move: the
    absent path is named `unprovable` (legacy list baseline proved nothing)
    and the manifest is rewritten in dict form in ONE run. This test used to
    assert FAIL -- that expectation WAS the landmine (an always-red gate with
    no in-tool escape); the genuine-loss conjunct is (g) below."""
    root = tmp_path / "repo"
    groot = root / ".agi"
    _committed_repo(root, {
        ".agi/nodes/deprecated/experiment/move-me.md": MINT_DEP("move-me", "X"),
        ".agi/nodes/hypothesis/h1.md": MINT_NODE("h1", "H1"),
    })
    _baseline(groot, {
        "active": 2, "deprecated": 0, "total": 2,
        "manifest": ["nodes/experiment/move-me.md", "nodes/hypothesis/h1.md"],
    })
    monkeypatch.setattr(verification, "_stamp_context",
                        lambda groot: (True, "abc123", "kept"))
    r = verification.compare_count(groot, {"active": 1,
                                           "deprecated": 1, "total": 2})
    assert r.status == "PASS", r.note
    assert "unprovable" in r.note and "proved nothing" in r.note
    assert "moved to deprecated" not in r.note
    st = json.loads((groot / "sessions" / verification.STATE_FILE).read_text())
    assert isinstance(st["manifest"], dict)


def test_real_deletion_still_fails_by_name(tmp_path, monkeypatch):
    """Fixture (c): a real deletion — the missing baseline path has no
    deprecated home at HEAD — still FAILs node-count and names the file."""
    root = tmp_path / "repo"
    groot = root / ".agi"
    _committed_repo(root, {".agi/nodes/hypothesis/h1.md": NODE("h1")})
    _baseline(groot, {
        "active": 2, "deprecated": 0, "total": 2,
        "manifest": ["nodes/experiment/gone.md", "nodes/hypothesis/h1.md"],
    })
    monkeypatch.setattr(verification, "_stamp_context",
                        lambda groot: (True, "abc123", "kept"))
    r = verification.compare_count(groot, {"active": 1,
                                           "deprecated": 0, "total": 1})
    assert r.status == "FAIL"
    assert "missing committed file(s): nodes/experiment/gone.md" in r.note
    assert "H0/H0b: 29k nodes lost to a silent drop" in r.note


def _commit_delta(root: Path, files: dict[str, str], rm=()) -> None:
    """A second (or later) commit on an already-initialised fixture repo."""
    sp = subprocess.run
    for rel in rm:
        sp(["git", "rm", "-q", rel], cwd=root, check=True, capture_output=True)
    for rel, body in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
    sp(["git", "add", "-A"], cwd=root, check=True, capture_output=True)
    sp(["git", "commit", "-m", "delta"], cwd=root, check=True,
       capture_output=True)


def test_legacy_list_baseline_migrates_a_legit_retire(tmp_path, monkeypatch):
    """(f) A legacy LIST baseline plus a legitimate retire with a flat
    total is NOT a permanent red: it PASSes, names the migrated path, and
    stamps the manifest in the dict {path: mint_id} form in ONE run."""
    root = tmp_path / "repo"
    groot = root / ".agi"
    _committed_repo(root, {
        ".agi/nodes/deprecated/experiment/move-me.md": MINT_DEP("move-me", "X"),
        ".agi/nodes/hypothesis/h1.md": MINT_NODE("h1", "H1"),
    })
    _baseline(groot, {
        "active": 2, "deprecated": 0, "total": 2,
        "manifest": ["nodes/experiment/move-me.md", "nodes/hypothesis/h1.md"],
    })
    monkeypatch.setattr(verification, "_stamp_context",
                        lambda groot: (True, "abc123", "kept"))
    r = verification.compare_count(groot, {"active": 1,
                                           "deprecated": 1, "total": 2})
    assert r.status == "PASS", r.note
    assert ("migrated unprovable move(s) to mint-id baseline: "
            "nodes/experiment/move-me.md" in r.note)
    assert "legacy list baseline proved nothing" in r.note
    st = json.loads((groot / "sessions" / verification.STATE_FILE).read_text())
    assert isinstance(st["manifest"], dict)
    assert st["manifest"]["nodes/deprecated/experiment/move-me.md"] == "X"
    assert st["manifest"]["nodes/hypothesis/h1.md"] == "H1"


def test_legacy_list_baseline_still_fails_a_genuine_deletion(tmp_path, monkeypatch):
    """(g) The conjunct the migration must not swallow: with a legacy list
    baseline a path with NO deprecated twin is a genuine loss, still FAILed
    and named, H0/H0b intact."""
    root = tmp_path / "repo"
    groot = root / ".agi"
    _committed_repo(root, {".agi/nodes/hypothesis/h1.md": MINT_NODE("h1", "H1")})
    _baseline(groot, {
        "active": 2, "deprecated": 0, "total": 2,
        "manifest": ["nodes/experiment/gone.md", "nodes/hypothesis/h1.md"],
    })
    monkeypatch.setattr(verification, "_stamp_context",
                        lambda groot: (True, "abc123", "kept"))
    r = verification.compare_count(groot, {"active": 1,
                                           "deprecated": 0, "total": 1})
    assert r.status == "FAIL", r.note
    assert "missing committed file(s): nodes/experiment/gone.md" in r.note
    assert "H0/H0b: 29k nodes lost to a silent drop" in r.note


def test_legacy_list_baseline_still_fails_a_dropped_total(tmp_path, monkeypatch):
    """(h) A legacy list baseline whose committed total DROPPED is still a
    FAIL, even when the only absent path has a deprecated twin: the total
    gate takes precedence over the migration."""
    root = tmp_path / "repo"
    groot = root / ".agi"
    _committed_repo(root, {
        ".agi/nodes/deprecated/experiment/move-me.md": MINT_DEP("move-me", "X"),
    })
    _baseline(groot, {
        "active": 2, "deprecated": 0, "total": 2,
        "manifest": ["nodes/experiment/move-me.md", "nodes/hypothesis/h1.md"],
    })
    monkeypatch.setattr(verification, "_stamp_context",
                        lambda groot: (True, "abc123", "kept"))
    r = verification.compare_count(groot, {"active": 0,
                                           "deprecated": 1, "total": 1})
    assert r.status == "FAIL", r.note
    assert "NODE COUNT DROPPED" in r.note


def test_migration_is_one_run_not_a_permanent_hole(tmp_path, monkeypatch):
    """(i) After the migration stamps the dict baseline, a later run where an
    absent path's twin carries a DIFFERENT mint id FAILs, named: the legacy
    fail-open window is one run, never a standing hole."""
    root = tmp_path / "repo"
    groot = root / ".agi"
    _committed_repo(root, {
        ".agi/nodes/deprecated/experiment/move-me.md": MINT_DEP("move-me", "X"),
        ".agi/nodes/hypothesis/h1.md": MINT_NODE("h1", "H1"),
    })
    _baseline(groot, {
        "active": 2, "deprecated": 0, "total": 2,
        "manifest": ["nodes/experiment/move-me.md", "nodes/hypothesis/h1.md"],
    })
    monkeypatch.setattr(verification, "_stamp_context",
                        lambda groot: (True, "abc123", "kept"))
    r = verification.compare_count(groot, {"active": 1,
                                           "deprecated": 1, "total": 2})
    assert r.status == "PASS", r.note
    assert isinstance(json.loads(
        (groot / "sessions" / verification.STATE_FILE).read_text())["manifest"],
        dict)
    # a later commit retires h1 too, but an unrelated node occupies its
    # deprecated path: the stamped baseline now carries H1, so this is a LOSS.
    _commit_delta(root, {
        ".agi/nodes/deprecated/hypothesis/h1.md": MINT_DEP("other", "Z"),
    }, rm=[".agi/nodes/hypothesis/h1.md"])
    r2 = verification.compare_count(groot, {"active": 0,
                                            "deprecated": 2, "total": 2})
    assert r2.status == "FAIL", r2.note
    assert "missing committed file(s): nodes/hypothesis/h1.md" in r2.note

def test_suite_opt_in_appends_tests_only_when_requested(monkeypatch, tmp_path):
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    seen = []

    def fake_run(groot, name, verbose):
        seen.append(name)
        return verification.CheckResult(name, "PASS", 0.0)

    monkeypatch.setattr(verification, "run_check", fake_run)
    results = verification.run_level(groot, "quick", suite=False, verbose=False)
    assert "tests" not in seen
    saw_names = [r.name for r in results]
    # SM.122: the anonymize guard is a built-in appended at every level (it is
    # the pre-commit write seam), so the declared names are a prefix of the
    # results and no count compare appears without smoke.
    assert saw_names[:len(verification.LEVELS["quick"])] == verification.LEVELS["quick"]
    assert "anonymize" in saw_names
    assert "node-count" not in saw_names

    monkeypatch.setattr(verification, "run_check", fake_run)
    results = verification.run_level(groot, "quick", suite=True, verbose=False)
    assert seen[-1] == "tests", "--suite appends the pytest run"


def test_no_level_runs_pytest_under_the_hood(monkeypatch, tmp_path):
    """Even with --suite absent, nothing in a level maps to pytest."""
    for nm in verification.LEVELS["rotation"] + verification.LEVELS["full"]:
        assert nm != "tests"


def test_run_level_adds_count_compare_after_smoke(monkeypatch, tmp_path):
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)

    def fake_run(groot, name, verbose):
        if name == "smoke":
            return verification.CheckResult("smoke", "PASS", 0.1,
                                            {"active": 5, "deprecated": 1, "total": 6})
        return verification.CheckResult(name, "PASS", 0.0, None)

    monkeypatch.setattr(verification, "run_check", fake_run)
    results = verification.run_level(groot, "rotation", suite=False, verbose=False)
    assert results[-1].name == "node-count"


def test_json_carries_every_check_fact(tmp_path):
    results = [
        verification.CheckResult("links", "PASS", 1.1, {"broken": 0}),
        verification.CheckResult("smoke", "FAIL", 20.0,
                                 {"active": 5, "deprecated": 1, "total": 6},
                                 note="drops"),
    ]
    doc = verification.render_json("rotation", False, results)
    assert doc["result"] == "FAIL"
    assert [c["name"] for c in doc["checks"]] == ["links", "smoke"]
    assert doc["checks"][0]["number"] == {"broken": 0}
    assert doc["checks"][1]["note"] == "drops"
    # every check field is data, no prose-only key.
    assert set(doc["checks"][0].keys()) <= {"name", "status", "elapsed",
                                            "number", "note"}


# --- the two Prime rulings at the L4.44 harvest ------------------------------
# Both are defects I found in the bytes after the round's own review passed:
# one ceiling for every check, and a lock that refused without saying by whom.


def test_suite_has_its_own_ceiling_far_above_the_per_check_one():
    """The engine suite is ~2300 tests. Under one shared 600s ceiling the check
    that legitimately takes minutes is the one check that false-FAILs, and a
    green suite gets reported as `timed out after 600s` — a failure the tool
    invented. The suite gets its own, larger ceiling; a hang is still caught."""
    assert verification.SUITE_TIMEOUT > verification.PER_CHECK_TIMEOUT
    assert verification.SUITE_TIMEOUT == 1800
    assert verification.PER_CHECK_TIMEOUT == 600


def test_only_the_suite_check_gets_the_suite_ceiling(monkeypatch, tmp_path):
    """The larger ceiling is scoped to the suite BY NAME. Widening it to every
    check would turn a hung link check into a half-hour wait."""
    class _Proc:
        returncode = 0
        stdout = "links: 1 resolved, 0 broken\n"
        stderr = ""

    table = {
        verification.SUITE_CMD: type("C", (), {"argv": ["true"], "cwd": None})(),
        "links": type("C", (), {"argv": ["true"], "cwd": None})(),
    }
    monkeypatch.setattr(verification.commands, "load", lambda groot: table)

    calls: list[float] = []
    monkeypatch.setattr(verification.subprocess, "run",
                        lambda argv, **kw: (calls.append(kw["timeout"]), _Proc())[1])

    verification.run_check(tmp_path, verification.SUITE_CMD, False)
    verification.run_check(tmp_path, "links", False)
    assert calls == [verification.SUITE_TIMEOUT, verification.PER_CHECK_TIMEOUT]


def test_suite_check_gets_a_private_basetemp(monkeypatch, tmp_path):
    """The suite runner passes its OWN --basetemp dir (created then removed),
    never pytest's SHARED /tmp/pytest-of-<user> tree that a concurrent run
    prunes to 3 and deleted this runner's tree mid-run (claim (2)). Since the
    dee5b3221 in-repo placement, that private dir is `tempfile.mkdtemp(
    prefix='agi-suite-')` under the SYSTEM tmp -- NEVER the repo (claim (2)):
    a basetemp inside the live checkout makes git-escaping writers hit LIVE."""
    class _Proc:
        returncode = 0
        stdout = "1 passed\n"
        stderr = ""
    table = {verification.SUITE_CMD:
             type("C", (), {"argv": ["true"], "cwd": None})()}
    monkeypatch.setattr(verification.commands, "load", lambda groot: table)
    seen = {}
    def _run(argv, **kw):
        bt = [a for a in argv if a.startswith("--basetemp=")]
        seen["arg"] = bt[0] if bt else None
        seen["present"] = Path(bt[0].split("=", 1)[1]).is_dir() if bt else None
        return _Proc()
    monkeypatch.setattr(verification.subprocess, "run", _run)
    r = verification.run_check(tmp_path, verification.SUITE_CMD, False)
    assert r.status == "PASS"
    assert seen["arg"] is not None
    bt_path = Path(seen["arg"].split("=", 1)[1])
    # the runner owns a UNIQUE dir directly under the SYSTEM tmp — never
    # pytest's SHARED default basetemp root nor the live checkout.
    assert bt_path.parent == Path(verification.tempfile.gettempdir()).resolve()
    assert bt_path.name.startswith("agi-suite-")
    assert seen["present"] is True                # owned dir EXISTS during run
    assert not bt_path.exists()                    # removed after the run


def test_non_suite_check_argv_untouched(monkeypatch, tmp_path):
    """Only the SUITE gets a private basetemp; a regular check's argv is
    unchanged (no --basetemp injected)."""
    class _Proc:
        returncode = 0
        stdout = "links: 1 resolved, 0 broken\n"
        stderr = ""
    table = {"links": type("C", (), {"argv": ["true"], "cwd": None})()}
    monkeypatch.setattr(verification.commands, "load", lambda groot: table)
    seen = {}
    monkeypatch.setattr(verification.subprocess, "run",
                        lambda argv, **kw: (seen.__setitem__("argv", argv),
                                            _Proc())[1])
    verification.run_check(tmp_path, "links", False)
    assert seen["argv"] == ["true"]
    assert not any(a.startswith("--basetemp") for a in seen["argv"])


def test_lock_acquire_returns_path_and_no_holder(tmp_path):
    """Success is `(path, None)`: a path to release and nobody to wait for."""
    path, holder = verification.acquire_suite_lock(tmp_path)
    assert path is not None and path.exists()
    assert holder is None
    assert path.read_text().strip() == str(__import__("os").getpid())


def test_lock_refusal_names_the_live_holder_pid(tmp_path, monkeypatch):
    """A refusal that does not name the holder tells a successor nothing it can
    act on. The live holder's pid comes back so the message can name it."""
    lock = tmp_path / "sessions" / verification.SUITE_LOCK
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text("424242")
    monkeypatch.setattr(verification, "_pid_alive", lambda pid: pid == 424242)

    path, holder = verification.acquire_suite_lock(tmp_path)
    assert path is None
    assert holder == 424242, "the refusal must be able to name who holds the window"
    # and the live holder's lock is left exactly as it was
    assert lock.read_text().strip() == "424242"


def test_lock_stale_pid_is_broken_and_reacquired(tmp_path, monkeypatch):
    """A dead holder is not a holder. The stale lock is broken, not obeyed —
    otherwise one killed run closes the window until somebody deletes a file by
    hand, and this loop has already had rounds killed mid-flight."""
    lock = tmp_path / "sessions" / verification.SUITE_LOCK
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text("999999")
    monkeypatch.setattr(verification, "_pid_alive", lambda pid: False)

    path, holder = verification.acquire_suite_lock(tmp_path)
    assert path is not None and holder is None
    assert lock.read_text().strip() == str(__import__("os").getpid())


# --- the suite-lock refusal (residue (5), hypothesis:l4-one-line-anchored-
# --- frontmatter-reader-and-the-suite-runner-refuses-a-held-lock-before-
# --- spawning): one clean line BEFORE pytest, never a conftest-error count ----


def test_suite_lock_guard_refuses_held_and_spawns_nothing(tmp_path, monkeypatch):
    """A held lock refuses with ONE refusal line and NO pytest subprocess. The
    3650-error conftest cascade is the thing being removed, so subprocess.run
    must not be invoked for the suite at all, and the refusal must not carry a
    conftest-error count."""
    lock = tmp_path / "sessions" / verification.SUITE_LOCK
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text("424242")
    monkeypatch.setattr(verification, "_pid_alive", lambda pid: pid == 424242)

    spawned: list = []
    monkeypatch.setattr(verification.subprocess, "run",
                        lambda argv, **kw: spawned.append(argv) or _StubProc())

    msg = verification._suite_lock_guard(tmp_path)
    assert msg is not None
    assert "lock held by 424242" in msg
    assert "refusing, not spawning" in msg
    assert "since" in msg
    # the refusal must not contain a conftest-error / collection-error count
    assert "error" not in msg.lower()
    assert "collection" not in msg.lower()
    # and no pytest subprocess was spawned by the refusal path
    assert spawned == []
    # the live holder's lock is left untouched
    assert lock.exists() and lock.read_text().strip() == "424242"


def test_main_suite_refusal_returns_named_code(tmp_path, monkeypatch, capsys):
    """main() --suite under a held lock prints exactly one refusal line and
    returns the NAMED exit code, never running the level (so pytest never
    spawns). The named code is what a caller abroad can tell from a "suite ran
    and failed."""
    lock = tmp_path / "sessions" / verification.SUITE_LOCK
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text("424242")
    monkeypatch.setattr(verification, "_pid_alive", lambda pid: pid == 424242)
    monkeypatch.setattr(verification.locations, "find_project_root",
                        lambda p: tmp_path)
    monkeypatch.setattr(verification.commands, "engine_for",
                        lambda g: str(tmp_path))
    # a legitimate runner is driven from a shell; this unit drives main()
    # from inside pytest, so clear the marker the detached-suite guard keys
    # on rather than trip the refusal this block is NOT testing
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    planned: list = []
    monkeypatch.setattr(verification, "run_level",
                        lambda *a, **k: planned.append(a) or [])

    rc = verification.main(["--suite", "--root", str(tmp_path)])
    assert rc == verification.EXIT_SUITE_LOCKED
    assert planned == []  # the level never ran -> no pytest spawned
    out = capsys.readouterr().out
    assert "lock held by 424242" in out
    assert out.count("refusing") == 1  # exactly one refusal line
    assert verification.EXIT_SUITE_LOCKED != 0  # named, non-zero


def test_suite_lock_guard_stale_proceeds(tmp_path, monkeypatch):
    """A dead pid is broken, NOT refused: the guard lets the suite proceed
    exactly as before, and the probe leaves the window free for the child
    conftest to acquire as the one live holder."""
    lock = tmp_path / "sessions" / verification.SUITE_LOCK
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text("999999")
    monkeypatch.setattr(verification, "_pid_alive", lambda pid: False)

    msg = verification._suite_lock_guard(tmp_path)
    assert msg is None  # proceed
    # the probe acquired-then-released; no lock sits on file for the child
    assert not lock.exists()


def test_suite_lock_guard_marker_naming_the_holder_proceeds(tmp_path,
                                                            monkeypatch):
    """SM.25b defect (2): a caller that ALREADY holds the lock (cmd_merge_up)
    exports SUITE_LOCK_MARKER = its own live pid. When that marked pid IS the
    lock's live holder this is NOT a foreign hold: the spawned runner
    PROCEEDS, the lock file is left untouched (still held across the suite),
    and nothing hangs. A marker naming any OTHER pid changes nothing -- that
    is still a foreign hold and refuses."""
    lock = tmp_path / "sessions" / verification.SUITE_LOCK
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text("424242")
    monkeypatch.setattr(verification, "_pid_alive", lambda pid: pid == 424242)
    monkeypatch.setenv(verification.SUITE_LOCK_MARKER, "424242")

    assert verification._suite_lock_guard(tmp_path) is None  # proceed
    # the lock is NOT released: the caller still holds it across the suite
    assert lock.exists() and lock.read_text().strip() == "424242"

    # a marker naming a DIFFERENT live pid is still a foreign hold: refuse
    monkeypatch.setenv(verification.SUITE_LOCK_MARKER, "7")
    monkeypatch.setattr(verification, "_pid_alive",
                        lambda pid: pid in (424242, 7))
    msg = verification._suite_lock_guard(tmp_path)
    assert msg is not None and "lock held by 424242" in msg, msg
    assert lock.read_text().strip() == "424242"


def test_suite_lock_guard_free_proceeds(tmp_path, monkeypatch):
    """A FREE lock is no reason to refuse: the guard returns None and leaves
    no lock on file, so the child pytest (conftest) acquires as the single
    holder."""
    spawned: list = []
    monkeypatch.setattr(verification.subprocess, "run",
                        lambda argv, **kw: spawned.append(argv) or _StubProc())

    msg = verification._suite_lock_guard(tmp_path)
    assert msg is None
    assert not (tmp_path / "sessions" / verification.SUITE_LOCK).exists()


# --- the read-only holder judgement (hypothesis:l4-the-suite-lock-has-one-
# --- read-only-holder-judgement-...): the ONE reader the probe-only callers
# --- share, READ-ONLY, never creating or unlinking ------------------------


def test_suite_lock_holder_live_foreign_pid_readonly(tmp_path, monkeypatch):
    """A LIVE foreign holder returns its pid and the READ touches nothing:
    same bytes, same mtime. The probe that used to poke the lock (planting a
    live pid for microseconds) now only reads it."""
    lock = tmp_path / "sessions" / verification.SUITE_LOCK
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text("424242")
    before_mtime = lock.stat().st_mtime_ns
    import time as _t
    _t.sleep(0.01)  # force a distinct mtime if the probe ever rewrote it
    monkeypatch.setattr(verification, "_pid_alive", lambda pid: pid == 424242)

    assert verification.suite_lock_holder(tmp_path) == 424242
    # the file is byte-identical and never rewritten
    assert lock.read_text().strip() == "424242"
    assert lock.stat().st_mtime_ns == before_mtime


def test_suite_lock_holder_absent_creates_nothing(tmp_path):
    """Absent lock: None returned, NEVER a file created by the probe."""
    assert verification.suite_lock_holder(tmp_path) is None
    assert not (tmp_path / "sessions" / verification.SUITE_LOCK).exists()


def test_suite_lock_holder_dead_pid_left_for_the_acquirer(tmp_path,
                                                          monkeypatch):
    """A dead pid reads as None and the probe leaves the file for the
    acquirer (claim 3: stale-breaking is the acquirer's job, never the
    probe's). Opposite of the guard's own stale-break, stated as the choice."""
    lock = tmp_path / "sessions" / verification.SUITE_LOCK
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text("999999")
    monkeypatch.setattr(verification, "_pid_alive", lambda pid: False)

    assert verification.suite_lock_holder(tmp_path) is None
    assert lock.exists() and lock.read_text().strip() == "999999"


# --- the bin freshness guard (goal:g15.10 / L4.81) -------------------------


def _mk_bin(tmp_path, names: list[str]) -> Path:
    bdir = tmp_path / "bin"
    bdir.mkdir()
    for n in names:
        (bdir / n).write_text("")
    return bdir


def _write_ts(groot: Path, ts: float) -> None:
    p = groot / "sessions" / verification.SUITE_TS_FILE
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"suite_ran_at": ts}))


def test_fresh_clean_tree_passes_falsifier_1(tmp_path):
    """Falsifier 1: nothing untracked and nothing newer than the last recorded
    suite run -> PASS. A check that always fires is noise, not a check."""
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    bdir = _mk_bin(tmp_path, ["old.py"])
    _write_ts(groot, 1_000_000.0)
    os.utime(bdir / "old.py", (500_000, 500_000))  # mtime before the suite ts
    r = verification.check_bin_freshness(groot, bin_dir=bdir,
                                         tracked_of=lambda d: {"old.py"})
    assert r.status == "PASS", r.note


def test_untracked_bin_py_trips_falsifier_2(tmp_path):
    """Falsifier 2: an untracked bin/*.py fails with SUITE REQUIRED printed."""
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    bdir = _mk_bin(tmp_path, ["new.py"])
    _write_ts(groot, 1_000_000.0)
    r = verification.check_bin_freshness(groot, bin_dir=bdir,
                                         tracked_of=lambda d: set())
    assert r.status == "FAIL"
    assert "SUITE REQUIRED" in r.note
    assert "new.py" in r.note


def test_old_untracked_bin_py_does_not_trip_falsifier_3(tmp_path):
    """Falsifier 3: a bin/*.py OLDER than the last suite run does NOT trip,
    even while untracked — the "/ or newer" half is bidirectional and is the
    case an untracked-only implementation gets wrong."""
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    bdir = _mk_bin(tmp_path, ["settled.py"])
    _write_ts(groot, 1_000_000.0)
    os.utime(bdir / "settled.py", (500_000, 500_000))  # old AND untracked
    r = verification.check_bin_freshness(groot, bin_dir=bdir,
                                         tracked_of=lambda d: set())
    assert r.status == "PASS", r.note


def test_tracked_but_newer_than_suite_still_trips(tmp_path):
    """A TRACKED file edited after the last suite run trips the mtime arm —
    this is the L4.78 failure (a script landed without the suite, unseen by
    the no--suite check)."""
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    bdir = _mk_bin(tmp_path, ["touched.py"])
    _write_ts(groot, 1_000_000.0)
    os.utime(bdir / "touched.py", (1_500_000, 1_500_000))  # newer than suite
    r = verification.check_bin_freshness(groot, bin_dir=bdir,
                                         tracked_of=lambda d: {"touched.py"})
    assert r.status == "FAIL"
    assert "SUITE REQUIRED" in r.note


def test_never_run_suite_is_conservatively_suite_required(tmp_path):
    """No recorded timestamp ever -> FAIL: a suite that has never run is the
    exact state to surface, not to pass over silently."""
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    bdir = _mk_bin(tmp_path, ["old.py"])
    os.utime(bdir / "old.py", (500_000, 500_000))
    r = verification.check_bin_freshness(groot, bin_dir=bdir,
                                         tracked_of=lambda d: {"old.py"})
    assert r.status == "FAIL"
    assert "SUITE REQUIRED" in r.note
    assert "no suite has EVER run" in r.note


def test_suite_completion_records_timestamp(tmp_path):
    """A completed --suite run persists its epoch, so the next no--suite
    rotation check can compare bin mtimes against it."""
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    verification._record_suite_ts(groot)
    doc = json.loads((groot / "sessions" / verification.SUITE_TS_FILE)
                     .read_text())
    assert "suite_ran_at" in doc
    import time as _t
    assert abs(doc["suite_ran_at"] - _t.time()) < 60


# --- the L4.101 ordering fix (first --suite run self-FAILs) -----------------
# ITEM 2 of hypothesis:l4-a-check-that-answers-a-question-it-is-not-asking.
# run_level used to append check_bin_freshness BEFORE main() recorded the
# completing suite's stamp, so the FIRST-ever --suite run read a None prior
# stamp and self-FAILed ("no suite has EVER run") even though that very run
# just passed. The fix is ordering, never judgement: when --suite is on and
# the suite PASSED within this call, freshness is judged against the run
# completing NOW. The spy injects a tmp bin dir + tracked set so the real
# guard runs deterministically (no git, no real tree) while letting the test
# assert WHICH timestamp run_level handed it.


def _suite_run_level(monkeypatch, groot, bdir, tracked, suite_status):
    """One run_level call with real check_bin_freshness (injected bin dir)
    and a stub run_check whose suite result is `suite_status`. Returns
    (results, kws_seen) where kws_seen captures what run_level passed to the
    guard."""
    real = verification.check_bin_freshness
    seen = {}

    def fake_run(groot, name, verbose):
        if name == verification.SUITE_CMD:
            return verification.CheckResult(verification.SUITE_CMD, suite_status,
                                            5.0, {"passed": 2340})
        return verification.CheckResult(name, "PASS", 0.0, None)

    def spy(groot, **kw):
        seen.update(kw)
        return real(groot, bin_dir=bdir, tracked_of=lambda d: set(tracked), **kw)

    monkeypatch.setattr(verification, "run_check", fake_run)
    monkeypatch.setattr(verification, "check_bin_freshness", spy)
    return verification.run_level(groot, "rotation", suite=suite_status is not None,
                                  verbose=False), seen


def test_first_suite_run_passes_when_suite_passed(monkeypatch, tmp_path):
    """(f) first arm: NO recorded stamp + --suite + suite PASSED -> freshness
    PASS. The just-covered bin is covered; the guard must not return a
    self-inflicted FAIL for a stamp main() has not written yet."""
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    bdir = _mk_bin(tmp_path, ["newer.py"])
    os.utime(bdir / "newer.py", (1_900_000, 1_900_000))  # before `now`; no prior stamp exists
    results, seen = _suite_run_level(monkeypatch, groot, bdir, {"newer.py"}, "PASS")
    fresh = next(r for r in results if r.name == "bin-suite-fresh")
    assert fresh.status == "PASS", fresh.note
    assert "covered by the suite run completing now" in fresh.note
    assert seen.get("effective_ts") is not None, (
        "suite-pass must judge against the completing run, not the prior stamp")


def test_first_suite_run_fails_when_suite_failed(monkeypatch, tmp_path):
    """(f) second arm: NO recorded stamp + --suite + suite FAILED -> freshness
    FAIL unchanged. A failed suite covered nothing, so the guard is still the
    conservative surface, not a rubber stamp."""
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    bdir = _mk_bin(tmp_path, ["newer.py"])
    os.utime(bdir / "newer.py", (1_900_000, 1_900_000))
    results, seen = _suite_run_level(monkeypatch, groot, bdir, {"newer.py"}, "FAIL")
    fresh = next(r for r in results if r.name == "bin-suite-fresh")
    assert fresh.status == "FAIL", fresh.note
    assert "SUITE REQUIRED" in fresh.note
    assert seen.get("effective_ts") is None, (
        "suite-fail must NOT fabricate a fresh stamp -- the recorded stamp rules")


def test_no_suite_changes_nothing_stale_stamp_still_fails(monkeypatch, tmp_path):
    """(g) With NO --suite, the guard is byte-for-byte the prior behaviour: a
    stale stamp plus a newer/untracked bin/*.py still FAILs, unchanged. The
    L4.101 fix is ordering only and must not weaken the no--suite gate."""
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    bdir = _mk_bin(tmp_path, ["newer.py"])
    _write_ts(groot, 1_000_000.0)                # stale stamp below the file's mtime
    os.utime(bdir / "newer.py", (1_500_000, 1_500_000))
    results, seen = _suite_run_level(monkeypatch, groot, bdir, [], None)  # None == no --suite
    fresh = next(r for r in results if r.name == "bin-suite-fresh")
    assert fresh.status == "FAIL", fresh.note
    assert "SUITE REQUIRED" in fresh.note
    assert "newer.py" in fresh.note
    assert "(untracked; mtime newer than the last suite run)" in fresh.note
    assert seen.get("effective_ts") is None, (
        "no --suite must never fabricate a fresh stamp")


# --- ITEM 3 of the round: the suite stamp is SHARED-ROOM, not worktree-local ---
# hypothesis:l4-a-check-that-answers-a-question-it-is-not-asking, item 3. The
# stamp that `bin-suite-fresh` guards must live where the shared engine tree
# lives, or a seat branch can never see the prime's suite run. `_sessions_dir`
# (the resolver the meter pins already share) routes a worktree groot through
# `git_common_root` to the main checkout. These two tests simulate that with a
# monkeypatched `git_common_root` (real git would need an on-disk worktree):
#   (g2) PATH EQUALITY -- a seat worktree groot and the main groot must resolve
#        the SAME stamp file, not merely both succeed at reading.
#   (g3) ROUND-TRIP -- a stamp written from EITHER groot is read from the OTHER.


def _worktree_pair(tmp_path):
    """A (seat, main) graph-root pair plus a git_common_root stand-in.

    Returns (main_groot, seat_groot, patch_cgr) where patch_cgr(monkeypatch)
    wires `locations.git_common_root` to bounce ANY path onto the main root --
    the worktree->main mapping the real helper performs via `git worktree`.
    Each `.agi` dir carries a config.json + nodes/ so `find_project_root`
    resolves it as a real graph, exactly as `rotate._sessions_dir` expects."""
    main_root = tmp_path / "main"
    seat_root = tmp_path / "seat"
    main_groot = main_root / ".agi"
    seat_groot = seat_root / ".agi"
    for g in (main_groot, seat_groot):
        g.mkdir(parents=True)
        (g / "nodes").mkdir()
        (g / "config.json").write_text("{}")

    def patch_cgr(monkeypatch):
        def _to_main(_root):
            return None if _root is None else main_root
        monkeypatch.setattr(locations, "git_common_root", _to_main)
        return _to_main

    return main_groot, seat_groot, patch_cgr


def test_seat_and_main_resolve_the_SAME_suite_stamp_path(monkeypatch, tmp_path):
    """(g2) The stamp path is a PATH-EQUALITY fact, not a success fact. A test
    that only asserts 'read succeeds' would pass on a machine where both
    groots happen to hold a stamp -- the exact divergence this fixes is that
    the seat's file does NOT exist. Assert the two resolve to ONE file."""
    main_groot, seat_groot, patch_cgr = _worktree_pair(tmp_path)
    patch_cgr(monkeypatch)

    seat_path = verification._suite_ts_path(seat_groot)
    main_path = verification._suite_ts_path(main_groot)
    assert seat_path == main_path, (
        f"stamp paths fork: seat={seat_path} main={main_path}")
    assert str(seat_path).startswith(str(main_groot.parent)), (
        "the shared stamp must resolve under the MAIN checkout, not the seat's")


def test_suite_stamp_round_trips_across_groots(monkeypatch, tmp_path):
    """(g3) A stamp written from one groot is READ by the other. Write from the
    seat worktree, read from the main groot (and back), assert the epoch is
    the ROUND-TRIP value -- the whole point of sharing the file."""
    main_groot, seat_groot, patch_cgr = _worktree_pair(tmp_path)
    patch_cgr(monkeypatch)

    verification._record_suite_ts(seat_groot)
    ts = verification._read_suite_ts(main_groot)
    assert ts is not None, "main must read the stamp a seat worktree wrote"
    assert abs(ts - time.time()) < 60

    # and in the other direction: the prime's suite, written in the main
    # checkout, must be what a seat-branch `bin-suite-fresh` compares against.
    verification._record_suite_ts(main_groot)
    ts_seat_read = verification._read_suite_ts(seat_groot)
    assert ts_seat_read is not None and abs(ts_seat_read - time.time()) < 60


# --------------------------------------------------------------------------
# hypothesis:l4-a-verify-suite-check-refuses-a-node-directory-outside-the-
# active-schema-set -- the stray-directory guard. Fixture-rooted for the FAIL
# case, the live tree read-only for the PASS case. The check never writes.
# --------------------------------------------------------------------------

def _stray_fixture(tmp_path, dirs, schema_files):
    """A throwaway `.agi` graph: `<groot>/nodes/<dir>` for each `dirs` entry
    and `<groot>/context/schemas/<file>` for each `schema_files` entry. The
    live tree is never touched."""
    groot = tmp_path / ".agi"
    (groot / "nodes").mkdir(parents=True)
    (groot / "context" / "schemas").mkdir(parents=True)
    for name in dirs:
        (groot / "nodes" / name).mkdir()
    for name in schema_files:
        stem = name[:-3] if name.endswith(".md") else name
        canonical = stem[1:-1] if stem.startswith("[") else stem
        (groot / "context" / "schemas" / name).write_text(
            f"---\nname: {canonical}\n---\n\nbody\n", encoding="utf-8")
    return groot


def test_node_dirs_fails_by_name_on_a_stray_and_is_read_only(tmp_path):
    """Clause 1+2: a directory matching no schema FAILS by name; the check
    writes nothing, and every other directory (`deprecated`, `.geometry`, the
    legitimate active type) is not named."""
    groot = _stray_fixture(
        tmp_path,
        dirs=["hypothesis", ".geometry", "deprecated", "notown"],
        schema_files=["[hypothesis].md"],
    )
    stray_file = groot / "nodes" / "notown" / "missing-thing.md"
    stray_file.write_text("a stray node of a non-existent type\n",
                          encoding="utf-8")
    r = verification.check_node_dirs(groot)
    assert r.status == "FAIL", r.note
    assert "STRAY NODE DIR(S): notown" in r.note
    named = r.note.split(" -- ")[0].removeprefix("STRAY NODE DIR(S): ")
    assert named.split(", ") == ["notown"], (
        f"named more than the stray: {named}")
    assert r.number["stray"] == 1
    assert stray_file.exists(), "the check must not touch what it finds"


def test_node_dirs_names_every_stray_not_just_the_first(tmp_path):
    """Clause 2: every stray directory is named, not the first one found."""
    groot = _stray_fixture(tmp_path, dirs=["hypothesis", "alpha", "zeta"],
                          schema_files=["[hypothesis].md"])
    r = verification.check_node_dirs(groot)
    assert r.status == "FAIL"
    assert "alpha" in r.note and "zeta" in r.note
    assert r.number["stray"] == 2


def test_node_dirs_passes_with_no_stray(tmp_path):
    """Clause 1 PROOF: a fixture with only legitimate dirs PASSES."""
    groot = _stray_fixture(tmp_path, dirs=["hypothesis", ".geometry",
                                           "deprecated"],
                          schema_files=["[hypothesis].md"])
    r = verification.check_node_dirs(groot)
    assert r.status == "PASS", r.note
    assert r.number["stray"] == 0


def test_node_dirs_passes_on_a_deprecated_type_directory(tmp_path):
    """Clause 3: a directory whose schema file is NOT bracket-named (an
    inactive/deprecated type) is legitimate -- only a name matching NO schema
    at all is stray. `agent_session.md` is the live tree's own inactive
    schema, spelled exactly as it exists today."""
    groot = _stray_fixture(
        tmp_path,
        dirs=["hypothesis", "agent_session", ".geometry", "deprecated"],
        schema_files=["[hypothesis].md", "agent_session.md"],
    )
    r = verification.check_node_dirs(groot)
    assert r.status == "PASS", r.note


def test_node_dirs_passes_on_the_live_tree_read_only():
    """PROOF on the real tree: today it has no stray directory, so the check
    PASSES. Read-only -- this only ever reads `.agi/nodes/`."""
    groot = locations.find_project_root(Path(__file__).resolve().parent)
    if groot is None:
        pytest.skip("no live graph root enclosing this checkout")
    r = verification.check_node_dirs(groot)
    assert r.status == "PASS", r.note
    assert r.number["stray"] == 0


def test_node_dirs_runs_at_rotation_and_full_never_quick(monkeypatch, tmp_path):
    """Clause 4: wired like bin-suite-fresh / seat-model -- appended by level
    at rotation and full, absent from quick (the pre-commit set)."""
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)

    def fake_run(groot, name, verbose):
        if name == "smoke":
            return verification.CheckResult(
                "smoke", "PASS", 0.1,
                {"active": 5, "deprecated": 1, "total": 6})
        return verification.CheckResult(name, "PASS", 0.0, None)

    monkeypatch.setattr(verification, "run_check", fake_run)
    rot = verification.run_level(groot, "rotation", suite=False, verbose=False)
    full = verification.run_level(groot, "full", suite=False, verbose=False)
    quick = verification.run_level(groot, "quick", suite=False, verbose=False)
    assert "node-dirs" in [r.name for r in rot]
    assert "node-dirs" in [r.name for r in full]
    assert "node-dirs" not in [r.name for r in quick]
    assert rot[-1].name == "node-count", "node-count stays the closing check"


# --- the DECLARED second suite (hypothesis:context-fixture-tests-run-in-a-
# configured-suite) ---------------------------------------------------


def _write_config(groot, cell_value):
    (groot / "config.json").write_text(
        json.dumps({"paths": {"core": {"suite_roots": cell_value}}}))


def test_suite_roots_read_the_config_cell_never_a_literal(monkeypatch, tmp_path):
    groot = tmp_path / ".agi"
    (groot / "fixtures").mkdir(parents=True)
    _write_config(groot, [".agi/fixtures"])
    monkeypatch.setattr(locations, "load_config", lambda root: json.loads(
        (Path(root) / "config.json").read_text()))
    roots, cell = verification._declared_suite_roots(groot)
    assert roots == [(tmp_path / ".agi" / "fixtures").resolve()], roots
    assert cell == "paths.core.suite_roots"


def test_extra_suite_skips_by_cell_name_when_undeclared(monkeypatch, tmp_path):
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    monkeypatch.setattr(locations, "load_config", lambda root: {})
    r = verification.check_extra_suite(groot)
    assert r.status == "SKIP", r.status
    assert "paths.core.suite_roots" in r.note


def test_unusable_cell_fails_where_an_absent_cell_skips(monkeypatch, tmp_path):
    """A DECLARED-UNUSABLE cell is not an absent one: it FAILs and names the
    value (parent probe C -- a string cell used to read as 'nothing declared')."""
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    for value, kind in (".agi/context", "str"), ([""], "list"), (42, "int"):
        _write_config(groot, value)
        monkeypatch.setattr(locations, "load_config", lambda root: json.loads(
            (Path(root) / "config.json").read_text()))
        r = verification.check_extra_suite(groot)
        assert r.status == "FAIL", (kind, r.status, r.note)
        assert "IS declared but unusable" in r.note, r.note
        assert "paths.core.suite_roots" in r.note, r.note
    # and the absent cell still SKIPs -- the two are not the same fact
    monkeypatch.setattr(locations, "load_config", lambda root: {"paths": {"core": {}}})
    assert verification.check_extra_suite(groot).status == "SKIP"


def test_extra_suite_fails_on_a_collection_error(monkeypatch, tmp_path):
    groot = tmp_path / ".agi"
    (groot / "ctx").mkdir(parents=True)
    (groot / "ctx" / "test_boom.py").write_text("import definitely_not_here\n")
    _write_config(groot, [".agi/ctx"])
    monkeypatch.setattr(locations, "load_config", lambda root: json.loads(
        (Path(root) / "config.json").read_text()))
    r = verification.check_extra_suite(groot)
    assert r.status == "FAIL", r.status
    assert "definitely_not_here" in r.note


def test_suite_fail_ids_names_every_id_past_a_ten_line_window():
    """The unit claim: N>10 failures used to leave only a count in the tail."""
    out = ("F\n" + "\n".join(f"long traceback line {i} of the failure body"
                           for i in range(20)) +
           "\n===== short test summary info =====\n" +
           "\n".join(f"FAILED tests/test_x.py::test_{i} - AssertionError"
                     for i in range(15)) +
           "\n15 failed in 3.2s\n")
    ids = verification._suite_fail_ids(out)
    assert ids == [f"tests/test_x.py::test_{i}" for i in range(15)], ids
    # the old report -- a ten line tail -- names at most one of them
    assert len("\n".join(out.splitlines()[-10:]).split("FAILED ")) - 1 < len(ids)


def test_extra_suite_note_names_each_failing_test_by_node_id(monkeypatch,
                                                             tmp_path):
    """Falsifiers 1-2: ONE and THREE forced failures both appear by node id."""
    groot = tmp_path / ".agi"
    (groot / "ctx").mkdir(parents=True)
    body = "".join(f"def test_boom{i}():\n    assert False, 'boom {i}'\n\n"
                   for i in (1, 2, 3))
    (groot / "ctx" / "test_forced_fail.py").write_text(body)
    _write_config(groot, [".agi/ctx"])
    monkeypatch.setattr(locations, "load_config", lambda root: json.loads(
        (Path(root) / "config.json").read_text()))
    r = verification.check_extra_suite(groot)
    assert r.status == "FAIL", r.status
    for i in (1, 2, 3):
        assert f"test_forced_fail.py::test_boom{i}" in r.note, (i, r.note)


def test_extra_suite_pass_carries_no_failed_ids(monkeypatch, tmp_path):
    """Falsifier 3: a PASSING declared suite names no failure."""
    groot = tmp_path / ".agi"
    (groot / "ctx").mkdir(parents=True)
    (groot / "ctx" / "test_good.py").write_text("def test_ok():\n    assert True\n")
    _write_config(groot, [".agi/ctx"])
    monkeypatch.setattr(locations, "load_config", lambda root: json.loads(
        (Path(root) / "config.json").read_text()))
    r = verification.check_extra_suite(groot)
    assert r.status == "PASS", (r.status, r.note)
    assert "FAILED" not in (r.note or ""), r.note


def test_extra_suite_runs_at_suite_only(monkeypatch, tmp_path):
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    monkeypatch.setattr(verification, "run_check",
                        lambda g, n, v: verification.CheckResult(n, "PASS", 0.0, None))
    monkeypatch.setattr(verification, "check_extra_suite", lambda g:
                        verification.CheckResult("context-suite", "SKIP", 0.0, None))
    off = verification.run_level(groot, "quick", suite=False, verbose=False)
    on = verification.run_level(groot, "rotation", suite=True, verbose=False)
    assert "context-suite" not in [r.name for r in off]
    assert "context-suite" in [r.name for r in on]
