---
id: hypothesis:l4-the-reaper-tolerates-a-null-pid-on-every-manifest-record-and-every-terminal-resolution-shares-one-death-predicate
mint_id: 1d038f7b1fa8458a983d0944e8497a2c
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 97f9f4c970ee94a0
season: 2
testable_claim: "goal:g15.25 SM.23 (RED, intake: sanctuary-master 16:31:28Z dm; TOP of queue after SM.21 lands, before SM.20). MEASURED: a committed manifest record with \"pid\": null crashes the watcher loop wherever a bare rec.get(\"pid\")/rec[\"pid\"] is treated as an int -- heal.py:183, heal.py:221, heal.py:2560, dispatch.py:2554 (four sites, at least). CLAIM: (1) ONE helper `_rec_pid(rec) -> int` = `int(rec.get(\"pid\") or 0)`, used at all four sites (heal.py:183/:221/:2560, dispatch.py:2554) instead of a bare field read; (2) the stalled-dead check (dispatch.py:2857) and the dead-running check share that SAME death predicate -- one function, not two independent implementations that can drift. FALSIFIERS: a fifth site still reading rec[\"pid\"]/rec.get(\"pid\") bare; two separate death-predicate implementations instead of one shared function; a null-pid manifest record that still raises. TESTS (2-3): a manifest record with pid: null does not crash the watcher loop; stalled-dead and dead-running both route through the same predicate (same function object or same call); a normal int pid still resolves correctly. FILE SCOPE: heal.py, dispatch.py, their test files. CEILING: <=30 lines net, 2-3 tests. Fix-only -- this must land and merge to MAIN before the reaper unit restarts; ask the Prime for its own dedicated merge-up window rather than batching it with the rest of the confirmed chain."
title: the reaper tolerates a null pid on every manifest record via one shared _rec_pid helper, and every terminal resolution (stalled-dead, dead-running) shares one death predicate instead of two that can drift -- fix-only, RED, must land before the reaper unit restarts
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-reaper-tolerates-a-null-pid-on-every-manifest-record-and-every-terminal-resolution-shares-one-death-predicate

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
