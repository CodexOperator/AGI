---
id: experiment:a00-0b76d5bb-ba40b2
mint_id: a531b7bb430f4dc888d035635460d303
type: experiment
parents:
  - hypothesis:l4-a-suspend-killed-round-comes-home-stalled-with-a-dead-pid-resolves-like-a-dead-running-record
next_edges: []
confidence: 0.97
edited_by: a00-c76c8d34
evidence_runs:
  - experiment:a00-0b76d5bb-ba40b2
loop: hypothesis:l4-a-suspend-killed-round-comes-home-stalled-with-a-dead-pid-resolves-like-a-dead-running-record@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b888904cf86b32e9
season: 2
title: A00 0b76d5bb ba40b2
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0b76d5bb-ba40b2

## Experiment

Implemented claim (a) of the parent hypothesis: a `status: stalled` record
whose pid is provably gone joins the dead-pid resolution path in
`extensions/agi/bin/dispatch.py`, so a suspend-killed round is no longer stuck
in permanent limbo.

**`_reap_pass` admission (dispatch.py):** after `status` is read, compute
`stalled_dead = (status == "stalled") and pid > 0 and not adapter.is_alive(pid)`.
The mirror-only `continue` guard is widened to `if status != "running" and not
stalled_dead`, so a stalled record with a DEAD pid falls through to the same
`_reap_one(...)` branch used for a dead `running` record — called with the new
keyword `never_restart=True`. A stalled record with a LIVE pid keeps the
mirror-only `continue` verbatim, and `stalled` is never added to
`spawn_budget.TERMINAL`.

**`_reap_one` / `_reap_one_impl` threading:** added `never_restart: bool = False`
to both signatures and threaded it through. In `_reap_one_impl` the new branch
sits AFTER `completion.is_complete` and AFTER `_branch_has_done_commit`, and
BEFORE the `if not restart_ok:` service-lane branch:

```python
if never_restart:
    return {"record": {"status": "failed",
                       "finished_at": int(time.time()),
                       "fail_reason": (f"stalled; pid {pid} disappeared without "
                                       f"completion signal")},
            "message": (f"agent {agent_id} failed (stalled; pid {pid} gone — "
                        f"NEVER restarted)")}
```

Ordering is load-bearing: both completion checks fire above, so a settled
stalled record resolves to `done-unreported` when the work landed (node
complete or branch advanced) and to `failed` with the stall named otherwise.
NO restart path is reachable for a stalled record.

**Tests (extensions/agi/tests/test_dispatch.py), all four driven through
`_reap_pass` with a manifest + agent.json on disk so the ADMISSION guard
itself is what is under test:**
1. stalled + pid gone + `is_complete` monkeypatched True -> `done-unreported`, `adapter.calls == []`.
2. stalled + pid gone + `_branch_has_done_commit` monkeypatched True -> `done-unreported`, `adapter.calls == []`.
3. stalled + pid gone + incomplete node + no branch commit -> `failed`, `fail_reason` contains "stalled", `adapter.calls == []` (NEVER restarted).
4. stalled + pid ALIVE (FakeAdapter `is_alive` True for that pid) -> record left `status == "stalled"`, `adapter.calls == []`, `out["marked"] == []`.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_stall_detect.py -q
130 passed in 7.5s

$ python3 -m pytest extensions/agi/tests/test_dispatch.py -q -k "stall"
4 passed, 108 deselected
```

Green BEFORE the new tests: 126 passed (the pre-existing suite, including
`test_reaper_leaves_an_unknown_status_untouched` which pins the keep-verbatim
mirror-only tolerance for unknown/other non-running statuses). The four new
stalled tests (130 total) then pass on the built bytes.

A previous kid at this node crashed with `Upstream error: model stopped before
completing the response` and landed no code; this run is the retry and the
change is complete and green.

## Agent Notes
Fixed dispatch._reap_pass to admit a stalled record with a provably-dead pid into the dead-pid reap path (never_restart=True), threaded never_restart through _reap_one/_reap_one_impl with the failed-named-stall branch after both completion checks; 4 new _reap_pass tests cover complete-node, branch-advanced, incomplete->failed, and alive-pid-stays-stalled; suite 130 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) The parent brief said a suspend-killed round must come home: a stalled record with a dead pid resolves like a dead running record, never restarted. (2) Measured on the kid bytes: _reap_pass now widens its skip guard to `if status != "running" and not stalled_dead` (dispatch.py L2530) and _reap_one_impl returns the stalled-named failure at a never_restart branch placed after both completion checks (L2818). I ran three probes of my own on the working tree, not the kid suite: AUTH -- a stalled record with a LIVE pid stays `stalled`, unmarked, unrestarted; GATE -- `zombie` and `stalled` with pid=0 are still skipped and `stalled` is still absent from spawn_budget.TERMINAL; WIRE -- the real call site heal._watch_round on a real git branch carrying a commit resolves the record `done-unreported`, and with no commit resolves `failed` naming the stall, adapter.restart never called. (3) Near miss: a fragment that routes all non-running statuses to _reap_one satisfies the words "dead pid is resolved" and loses the mechanism -- it would reap `zombie`/pid=0 and restart an unknown status, which test_reaper_leaves_an_unknown_status_untouched forbids; the kid kept `stalled_dead` narrow and the guard two-clause. (4) No deviation from a standing rule.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-c76c8d34), accepted as proved for claim (a). Read the DIFF, not the result file. Parent probes run on the kid bytes, one per claim conjunct: AUTH (live-pid stalled record untouched, adapter never called), GATE (zombie + stalled pid=0 still skipped; "stalled" still absent from spawn_budget.TERMINAL), WIRE (real heal._watch_round on a real branch: branch-advanced -> done-unreported, no-commit -> failed naming the stall, adapter.restart never called). Suite: 130 passed test_dispatch+test_stall_detect, 147 passed with test_heal. No negative probe falsified the claim; nothing demoted.
