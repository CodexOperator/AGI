"""plan_master.py — record-run then trend classifies falling fixes_per_draft.

(hypothesis:l3w4-plan-master, TESTS) The Plan Master seat's push-further loop:
`record-run` appends one {ts,iter,n_drafts,n_fixed,fixes_per_draft} line per
summon; `trend --last N` reads the tail back and reports the one-word
direction. Three fixture runs writing fixes_per_draft 2.0 → 1.5 → 0.5 must
classify as falling.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

BIN_DIR = Path(__file__).resolve().parents[1] / "bin"
if str(BIN_DIR) not in sys.path:
    sys.path.insert(0, str(BIN_DIR))

import plan_master  # noqa: E402


def _record_run(tmp_path, drafts, fixed, ts):
    log = str(tmp_path / "pushfurther.jsonl")
    code = plan_master.record_run(
        _ns(drafts=drafts, fixed=fixed, ts=ts, iter="L3.33", log=log)
    )
    assert code == 0, f"record-run exited {code}"
    return log


def _ns(**kw):
    import argparse

    ns = argparse.Namespace()
    for k, v in kw.items():
        setattr(ns, k, v)
    return ns


def test_record_run_then_trend_classifies_falling_fixes_per_draft(tmp_path):
    log = _record_run(tmp_path, drafts=2, fixed=4, ts="t0")
    log = _record_run(tmp_path, drafts=2, fixed=3, ts="t1")
    log = _record_run(tmp_path, drafts=2, fixed=1, ts="t2")

    records = plan_master._load_records(log)
    assert [r["fixes_per_draft"] for r in records] == [2.0, 1.5, 0.5]
    assert [r["n_drafts"] for r in records] == [2, 2, 2]

    out = plan_master.trend(_ns(last=3, tol=1e-6, log=log))
    assert out == 0
    # (classification printed to stdout; also asserted via _classify below)
    assert plan_master._classify([2.0, 1.5, 0.5], 1e-6) == "falling"


def test_trend_rising_and_flat(tmp_path):
    log = _record_run(tmp_path, drafts=2, fixed=1, ts="t0")
    log = _record_run(tmp_path, drafts=2, fixed=3, ts="t1")
    log = _record_run(tmp_path, drafts=2, fixed=4, ts="t2")
    assert plan_master._classify([0.5, 1.5, 2.0], 1e-6) == "rising"

    flat_log = str(tmp_path / "flat.jsonl")
    for i, f in enumerate([2, 2, 2]):
        plan_master.record_run(
            _ns(drafts=2, fixed=f, ts=f"t{i}", iter="L3.33", log=flat_log)
        )
    assert plan_master._classify([1.0, 1.0, 1.0], 1e-6) == "flat"


def test_record_run_rejects_bad_fixed(tmp_path):
    log = str(tmp_path / "bad.jsonl")
    code = plan_master.record_run(
        _ns(drafts=2, fixed=-1, ts="t0", iter="L3.33", log=log)
    )
    assert code == 2


def test_trend_empty_log(tmp_path):
    code = plan_master.trend(_ns(last=3, tol=1e-6, log=str(tmp_path / "nope.jsonl")))
    assert code == 1