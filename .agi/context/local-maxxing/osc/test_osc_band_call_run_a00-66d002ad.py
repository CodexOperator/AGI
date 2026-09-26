"""Acceptance tests for the band-call RUNNER (hypothesis:a00-66d002ad-8cee33).

Three claims, all zero model / zero GPU:
  1. on the tree's OWN qknorm data the runner is TOTAL (no traceback) and RED (exit 2),
     and every row it prints is `unresolved` -- the honest state of that data today;
  2. a synthetic 3-distinct-seed cell turns the same runner GREEN (exit 0) with a word;
  3. a record schema the rule cannot read is a REASON, never a crash and never a word.
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "callrun", os.path.join(HERE, "osc_band_call_run_a00-66d002ad.py"))
run = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(run)
sys.path.insert(0, os.path.dirname(HERE))       # paths.py, for the config-resolved default


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
