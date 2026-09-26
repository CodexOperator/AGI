"""Acceptance tests for the band-call RUNNER (hypothesis:a00-66d002ad-8cee33).

Three claims, all zero model / zero GPU:
  1. on the tree's OWN qknorm data the runner is TOTAL (no traceback) and RED (exit 2),
     and every row it prints is `unresolved` -- the honest state of that data today;
  2. a synthetic 3-distinct-seed cell turns the same runner GREEN (exit 0) with a word;
  3. a record schema the rule cannot read is a REASON, never a crash and never a word.
  4. the ENTRY POINT is wire-live under a scrubbed interpreter: this file used to
     seed sys.path for the runner, which is why a clean `python3 <runner>` died
     with ModuleNotFoundError (exit 1) under a green suite. No global interpreter
     state is set here any more; a subprocess cannot inherit the test's sys.path.
"""
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER = os.path.join(HERE, "osc_band_call_run_a00-66d002ad.py")
_spec = importlib.util.spec_from_file_location("callrun", RUNNER)
run = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(run)


def _clean_run(cwd):
    """argv/env with no inherited path help: a shell, not this test process."""
    return subprocess.run([sys.executable, RUNNER], cwd=cwd, env={"PATH": "/usr/bin:/bin"},
                          capture_output=True, text=True)


def test_entry_point_reaches_the_rule_from_a_neutral_cwd():
    p = _clean_run("/")
    out = p.stdout + p.stderr
    assert p.returncode == 2, out                 # RED (unresolved), not DEAD (ModuleNotFound)
    assert "ModuleNotFoundError" not in out and "Traceback" not in out, out
    rows = [x for x in p.stdout.splitlines() if not x.startswith("TOTAL")]
    assert rows and all(r.startswith("unresolved") for r in rows), out
    assert "no cells.jsonl" not in out


def test_reach_is_cwd_independent():
    """A __file__-discovered import works from anywhere; a cwd literal would not."""
    assert _clean_run("/tmp").returncode == _clean_run("/").returncode == 2


def test_todays_own_data_is_total_and_calls_nothing(capsys):
    rc = run.main([])
    out = capsys.readouterr().out
    rows = [x for x in out.splitlines() if not x.startswith("TOTAL")]
    assert rows, "no cells.jsonl found under the config dir"
    assert all(r.startswith("unresolved") for r in rows), out
    assert rc == 2, out                      # unresolved cells are a RED run
    assert "no cells.jsonl" not in out


def _write(tmp_path, name, rows):
    p = tmp_path / name
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return p


def test_three_distinct_seeds_flip_the_same_runner_green(tmp_path, capsys):
    _write(tmp_path, "cells.jsonl", [
        {"model": "qwen2", "np": 32, "budget": 5.25, "arm": "random", "seed": s,
         "agree": a, "kl": k} for s, a, k in ((1, .50, .11), (2, .53, .12),
                                              (3, .56, .13))] + [
        # both metrics must VARY across the random arm or the band is degenerate (a refusal)
        {"model": "qwen2", "np": 32, "budget": 5.25, "arm": "key_only", "agree": .60,
         "kl": 0.10}])
    rc = run.main([str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "unresolved" not in out and "win" in out


def test_foreign_schema_is_a_reason_not_a_crash(tmp_path, capsys):
    _write(tmp_path, "cells.jsonl", [{"model": "qwen2", "np": 32, "cell": "c0",
                                       "agree": .5, "kl": .1}])   # no arm, no budget
    rc = run.main([str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 2 and out.count("unresolved") >= 1, out
    assert "Traceback" not in out
