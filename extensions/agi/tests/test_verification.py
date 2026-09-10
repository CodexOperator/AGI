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
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import verification  # noqa: E402

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


def test_links_pass_uses_the_count_not_the_exit_code():
    """links exits 0 even with broken links; the broken count is the fact."""
    assert verification._passed("links", 0, {"broken": 0}) is True
    assert verification._passed("links", 0, {"broken": 2}) is False
    assert verification._passed("goals-check", 0, {"byte-identical": 1}) is True


def test_count_first_run_records_and_passes(tmp_path):
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    current = {"active": 1707, "deprecated": 194, "total": 1901}
    r = verification.compare_count(groot, current)
    assert r.status == "PASS"
    assert "baseline recorded" in r.note
    state = json.loads((groot / "sessions" / "verify-count.json").read_text())
    assert state == current


def test_count_drop_is_a_failure_that_names_the_drop(tmp_path):
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    (groot / "sessions" / "verify-count.json").write_text(
        json.dumps({"active": 9999, "deprecated": 0, "total": 0}))
    r = verification.compare_count(groot, {"active": 1707,
                                           "deprecated": 194, "total": 1901})
    assert r.status == "FAIL"
    assert "active=1707 below baseline=9999" in r.note


def test_count_steady_updates_baseline_and_passes(tmp_path):
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    (groot / "sessions" / "verify-count.json").write_text(
        json.dumps({"active": 1707, "deprecated": 194, "total": 1901}))
    newer = {"active": 1707, "deprecated": 195, "total": 1902}
    r = verification.compare_count(groot, newer)
    assert r.status == "PASS"
    state = json.loads((groot / "sessions" / "verify-count.json").read_text())
    assert state == newer


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
    assert saw_names == verification.LEVELS["quick"], "no count compare without smoke"

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
