"""hypothesis:restart-admission-honours-the-per-harness-live-bound.

A restart is a NEW PROCESS and must be admitted like one — but admission
that drops the harness name skips the `harnesses.<h>.max_live` ROW check
entirely, so a `max_live: 1` row (pi-local) admitted a restarted kid beside
the one live kid it allows. The spawn path
(`hypothesis:dispatch-leases-the-resolved-harness-and-pi-local-admits-one-
live-kid`) already threads the resolved harness into `spawn_budget.acquire`;
this is the same bound on the reaper's restart path.

RED on pre-fix bytes: `_reap_one_impl` passed no `harness=` to `acquire()`,
so the restart was admitted and the adapter's `restart()` ran with the row
full. GREEN post-fix: the restart is refused BY NAME, the adapter is never
called, and the record reads a refusal rather than a running pid.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import dispatch  # noqa: E402
import spawn_budget  # noqa: E402

CONFIG = json.dumps({
    "spawn": {"harness": "pi-local", "parallel": 1, "max_live": 25},
    "harnesses": {"pi-local": {"max_live": 1, "credential": "none"}},
})


class _CountingAdapter:
    """Records whether the restart ever reached the adapter.

    Returns a pid rather than raising: dispatch's restart lane catches every
    `Exception` and rewrites the record as `failed; restart unavailable`, so
    an adapter that raised would let a pre-fix run slip past a bare
    `status == "failed"` assertion and be caught only by an accident of the
    message.
    """

    def __init__(self):
        self.calls = 0

    def restart(self, **kw):
        self.calls += 1
        return 4242


def _rig(tmp_path: Path):
    graph = tmp_path / ".agi"
    (graph / "sessions").mkdir(parents=True)
    (graph / "config.json").write_text(CONFIG, encoding="utf-8")
    iter_dir = graph / "sessions" / "iter-001"
    sess = iter_dir / "a00-kid"
    sess.mkdir(parents=True)
    (sess / "context.md").write_text("ctx", encoding="utf-8")
    return graph, iter_dir, sess


def _occupy(graph: Path) -> None:
    """One live pi-local lease: the row's single slot, held by THIS process."""
    lease = spawn_budget.acquire(graph, 25, "a00-occupant", tier="kid",
                                 iter_n=1, harness="pi-local")
    assert lease is not None, "the first pi-local lease must be admitted"
    spawn_budget.commit(lease, os.getpid())


def _record(sess: Path) -> dict:
    return {
        "tier": "kid",
        "harness": "pi-local",
        "harness_spec": {"harness": "pi-local", "credential": "none"},
        "context_file": str(sess / "context.md"),
        "target": "hypothesis:x",
    }


def _cfg() -> dict:
    """The real dispatch config: the GLOBAL cap has room, the ROW does not.

    The reaper's cap is `spawn_budget.max_live(cfg)` of the dict the CALLER
    passes, so a `cfg` that omits `spawn` falls back to
    `DEFAULT_MAX_LIVE=1` and a pre-fix run is refused by the GLOBAL bound for
    the wrong reason -- which would make the falsifier green for free.
    """
    return json.loads(CONFIG)


def test_a_restart_is_refused_while_its_harness_row_is_full(tmp_path, capsys):
    graph, iter_dir, sess = _rig(tmp_path)
    _occupy(graph)
    adapter = _CountingAdapter()
    out = dispatch._reap_one_impl(
        graph, iter_dir, adapter, _record(sess), "a00-kid", 999999,
        cfg={"reaper": {"max_restarts": 1}, **_cfg()})
    assert adapter.calls == 0, (
        "a refused restart must never reach the adapter while the row is full")
    rec = out["record"]
    assert rec["status"] == "failed", rec
    assert "not restarted" in out["message"], out["message"]
    err = capsys.readouterr().err
    assert "pi-local" in err and "(1/1)" in err, (
        f"the refusal must NAME the row it is over: stderr={err!r}")
    assert not (spawn_budget.budget_dir(graph) / "a00-kid-r1.lease").exists(), (
        "a refused restart must leave no lease behind")


def test_a_restart_is_admitted_once_its_harness_row_is_free(tmp_path):
    """The control: the bound is the ROW, not a blanket ban on restarts."""
    graph, iter_dir, sess = _rig(tmp_path)

    class _Adapter:
        def __init__(self):
            self.calls = 0

        def restart(self, **kw):
            self.calls += 1
            return 4242

    adapter = _Adapter()
    out = dispatch._reap_one_impl(
        graph, iter_dir, adapter, _record(sess), "a00-kid", 999999,
        cfg={"reaper": {"max_restarts": 1}, **_cfg()})
    assert out["record"]["status"] == "running", out["record"]
    assert adapter.calls == 1
    lease = json.loads(
        (spawn_budget.budget_dir(graph) / "a00-kid-r1.lease").read_text())
    assert lease["harness"] == "pi-local", (
        "the admitted restart's lease must carry the row it was admitted "
        f"against, so the NEXT restart counts it: {lease!r}")
