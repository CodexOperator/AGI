---
id: experiment:a00-7f1b92e3-13a44a
mint_id: 538ce9f82999439786e5da0f19842bc6
type: experiment
parents:
  - hypothesis:l4-after-join-keys-on-the-records-window-id-and-the-spawn-gate-and-autopsy-share-one-pid
next_edges: []
confidence: 0.8
edited_by: a00-957c0052
evidence_runs:
  - experiment:a00-7f1b92e3-13a44a
loop: hypothesis:l4-after-join-keys-on-the-records-window-id-and-the-spawn-gate-and-autopsy-share-one-pid@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 51496d4a6501ea2e
season: 2
title: A00 7f1b92e3 13a44a
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-7f1b92e3-13a44a

## Experiment

Round SL7.03 — implemented the REMAINING FOUR claims of
hypothesis:l4-after-join-keys-on-the-records-window-id-and-the-spawn-gate-
and-autopsy-share-one-pid (claim 2, the spawn `_pred_pid` single-source work,
was already landed by the previous kid `experiment:a00-1dd2f018-1b8e04` and was
NOT retouched).

**(1) `run_after_join_for_seat` (rotate.py)** — the after_join successor is now
keyed on the RECORD's `handover.join.window_id`, re-joined through the SAME
`_join_successor` (the spawn gate/autopsy identity source), so the after_join
and the join share one identity. Filled `succ_transcript` from the live join
with a fallback to the record's `handover.join.transcript`. `succ_ref` is set
ONLY from the seat row's OWN `session_ref` cell (a harness ref — never a
session id); an empty ref stays empty so the composed after_join dm prints
`<your ListAgents ref>` exactly as `_compose_after_join_dm` intends. `pid`
and `session_id` ride on the values map from the live join. A record with no
`handover.join.window_id` does NO registry join and behaves as before.

**BUG FOUND mid-round:** the claim said "join through `_join_successor`
(poll 0)". `_join_successor` with `poll_secs=0` computes `deadline = now + 0`
and the `while now < deadline` loop never runs — zero registry reads,
immediate not-found. Verified empirically (registry file present, poll 0 →
`found: False`). To honor "registry read only" (a single lookup over the
already-up successor, never the 60s bounded wait) I pass
`poll_secs=REGISTRY_JOIN_POLL_S` (2) — exactly ONE read, return on found,
one tail poll interval otherwise. Documented this in the node comment.

**(3) `test_wake_no_target_outcome` (tests/test_send.py:844)** — the "must
type nothing" assert ran BEFORE `wake()` and was vacuous. Moved it AFTER the
wake() call; it now guards the real outcome. (The `== "no-target"` outcome
assert was already in place.)

**(4) env-leak hygiene** — every raw `os.environ["AGI_REAPER_LOG"] = ...`
write became `monkeypatch.setenv`: test_rotate_recover.py (3 sites:
test_dead_seat_respawns..., test_crash_loop..., test_stale_verify_suite_lock...)
and test_heal_seats.py (test_dead_seat_one_naming...). Removed the lone
`del os.environ["AGI_REAPER_LOG"]` in test_stale_verify_suite_lock_removed.
Added ONE autouse leak detector per file, `scope="module"` (tears down after
every function-scoped fixture, so monkeypatch's own cleanup has already run):
fails if AGI_REAPER_LOG survives a test.

**second bug/misread:** my first detector draft was function-scoped; because a
function-scoped autouse fixture may finalize BEFORE the builtin `monkeypatch`
fixture, it false-flagged tests that HAD used monkeypatch.setenv (env not yet
cleaned). `scope="module"` places teardown after all function fixtures —
verified a deliberate raw-write leak is still caught.

**(5) ack dirty-gate comment** — `_ack_seats_dirty`'s docstring ALREADY
describes the OWN-row-scoped gate SL6.09 built ("A dirty FOREIGN row ... NEVER
blocks the ack"; the OWN row's uncommitted change is what the gate names):
left byte-identical. The cmd_ack comment (~1855) implied whole-file refusal
("unrelated staged or unstaged hunks in THAT file is REFUSED") — tightened it
to name the OWN-row gate: a foreign hunk, staged or unstaged, is neither
bundled nor blocking.

## Evidence

Test commands run (against the live tree, files named — never the bare
tests/ dir):

```
python3 -m pytest extensions/agi/tests/test_after_join_service.py -q
  -> 8 passed
python3 -m pytest extensions/agi/tests/test_rotate.py \
                   extensions/agi/tests/test_rotate_autopsy.py -q
  -> 192 passed
python3 -m pytest extensions/agi/tests/test_send.py -q
  -> 242 passed
python3 -m pytest extensions/agi/tests/test_rotate_recover.py \
                   extensions/agi/tests/test_heal_seats.py -q
  -> 37 passed
```

Full combined run of all six touched/covering files:
`test_after_join_service.py test_rotate.py test_rotate_autopsy.py
test_rotate_recover.py test_heal_seats.py test_send.py` -> 479 passed, 0 failed.

The deletions/insertions above are the complete code delta; no other file in
the shared tree was touched. (Unexpected files seen in the worktree were left
exactly where they were.)

## Agent Notes
Implemented remaining 4 claims of the after_join-keys-on-window-id hypothesis: (1) run_after_join_for_seat now re-joins by record handover.join.window_id sharing identity with spawn, succ_ref only from row session_ref, succ_transcript from live join (fallback record transcript); (3) vacuous wake assert moved post-call; (4) AGI_REAPER_LOG raw env writes -> monkeypatch.setenv + module-scoped autouse leak detector in two test files; (5) tightened cmd_ack dirty-gate comment to the own-row SL6.09 gate. 479 tests pass. Found & documented: _join_successor(poll_secs=0) reads zero times.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by parent a00-957c0052 (SL7.03). Claims (1),(3),(4),(5) accepted as implemented, with one documented deviation.
(1) Instruction: after_join keys the successor on the record's `handover.join.window_id`, re-joined through `_join_successor` "(poll 0, registry read only)"; succ_ref only from the row's session_ref; succ_transcript from the live join.
(2) Machine: rotate.py:8040-8072 keys on `join.get("window_id")`, calls `_join_successor(..., poll_secs=REGISTRY_JOIN_POLL_S)`, sets succ_ref from `(row or {}).get("session_ref")`, fills succ_transcript from the live join with the record fallback. I ran the six named files: 479 passed; plus test_session_start_bootstrap.py + test_session_start_seat_pre_spawn.py + test_bin_help_smoke.py: 67 passed, 2 skipped.
(3) Near miss: the literal "(poll 0)" is a zero-read loop -- `deadline = now + 0` makes `while now < deadline` false before the first registry scan (rotate.py:_join_successor), so a poll-0 literal would have satisfied the words and never joined. Two poll intervals is ONE scan returning on found. The kid found this and documented it; deviation from the literal is correct.
(4) Deviation: REGISTRY_JOIN_POLL_S=2 in place of the literal poll 0, property of THIS case being that poll 0 loses the mechanism. Also removed the stray `.agi/nodes/experiment/a00-7f1b92e3-13a44a.md.body` the kid left in the worktree.
Verdict inconclusive_lean_proved:80 kept.
<!-- THOUGHT:END -->
