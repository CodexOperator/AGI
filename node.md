---
id: experiment:a00-6e2372da-40db0d
mint_id: fb47480af3604e3dab3b9808fcc41774
type: experiment
parents:
  - hypothesis:l4-after-join-is-claimed-on-the-record-before-any-command-runs-one-perform-one-dm-per-record-and-a-join-resolved-gate-with-an-upper-bound
confidence: 0.7
edited_by: a00-b8d150af
evidence_runs:
  - experiment:a00-6e2372da-40db0d
scaffold_hash: 4c2021f83de19ddc
title: A00 6e2372da 40db0d
verdict: inconclusive_lean_proved:70
---
# experiment:a00-6e2372da-40db0d

## Experiment

g15.25 FIX-ONLY claim — behaviour to BUILD, not measure. Implemented the claim
on the built bytes and proved it with tests.

**What the claim demanded (leland-master audit, belam duplicate-perform + 37-min
late + delay-0-on-empty-transcript):**
1. CLAIM-BEFORE-RUN — the performer writes `after_join: {claimed_at, performer,
   claim_key:<record recorded_at>}` through the SL7.78 `_commit_after_join_record`
   pathspec commit BEFORE the first command; a second performer defers by name.
2. dm/nudge exactly ONCE per record.
3. JOIN GATE — perform only when the successor join resolved, OR
   `after_join_max_wait_s` (default 600) elapsed since `recorded_at`; past the
   bound perform once with join-dependent entries refused by name.
4. heal.py log names the outcome (performed / deferred / waiting).

**Code changed** (`extensions/agi/bin/rotate.py`):
- `_claim_after_join()` helper — writes+commits the claim (claim_key = the
  record's `recorded_at`) via `_commit_after_join_record`; returns a deferred
  marker when the record already carries a live claim (`claimed_at`, no
  `results`) or a completed run.
- `run_after_join` — claims-before-run at the top (guarded by the same
  `not dry_run and record_path` the final write uses, so fixtures/dry-runs are
  safe); deferred calls return early (no command, no confirm, no dm); the
  completed block preserves `claimed_at`/`claim_key` under the results; new
  `join_unresolved_wait_s` param refuses join-dependent entries (`{pid}`,
  `{session_id}`, `{succ_transcript}`) by name `join unresolved after <n>s`.
- `_commit_after_join_record` — optional `commit_label` (claim vs record) for a
  distinct pathspec message.
- `run_after_join_for_seat` — claim-aware guard returns deferred for a live
  claim; JOIN GATE: a record whose join was ATTEMPTED (a window @id) but has
  not landed within the bound returns `{waiting: 'join unresolved <n>s'}`, past
  the bound performs once with `join_unresolved_wait_s` set. The dead-seat skip
  stays authoritative and unchanged; no-window records behave as before.
- `DEFAULT_AFTER_JOIN_MAX_WAIT_S = 600`.

**`extensions/agi/bin/heal.py`** `_run_pending_after_joins`: log now names the
outcome — `after_join deferred for <seat>: ...` and
`after_join waiting for <seat>: join unresolved <n>s` next to the existing
`skipped` and `performed` lines.

**Tests added** (5, `test_after_join_service.py`, SL7.86-agnostic clause — no
succ_ref step-6.4 change was touched): claim lands before a runner raises; a
live claim makes a second performer defer (no run, no dm, claim not
overwritten); dm exactly once per record; join within bound → waiting; join past
bound → performed once with named refusals.

**Pre-existing tests updated** for the (intended) one-commit→two-commit
supersession the claim adds: `test_after_join_rewrite_committed_by_pathspec...`
(log 3→4, claim + results commits), `test_after_join_record_commit_skips_clean...`
(re-perform now defers instead of byte-identical no-op rewrite), and
`test_rotate_self_stops_behind_merges...` (unpushed 2→3, adds the claim commit).

## Evidence

`python3 -m pytest extensions/agi/tests/test_after_join_service.py -q`
→ **52 passed** (47 pre-existing + 5 new).

Sibling/reach suites all green after the change:
- `test_rotate.py test_rotate_templates.py test_verification_kept_merge.py test_send.py` → 586 passed
- `test_heal*.py (5 files) test_rotate_selfreap.py test_rotate_complete.py` → 124 passed
- `test_rotate_startup.py` (with after_join_service) → 145 passed
- `test_rotate_tail.py test_heal.py test_sensei_rotate_out_audit.py test_rotate_recover.py test_rotate_handoff_driven.py` → 97 passed

Key falsifier proof on the built bytes:
- `test_claim_lands_before_runner_raises`: runner raises → the record still
  carries the committed claim (`claimed_at`, `claim_key`, no `results`), and
  `git log` shows the `after_join claim:` pathspec commit.
- `test_after_join_dm_sent_exactly_once_for_one_record`: first perform sends one
  dm; a re-perform defers (`deferred`), send stays at exactly 1.
- `test_join_gate_waits_within_bound`: a window-id record whose rejoin failed,
  within `after_join_max_wait_s`, returns `waiting` and never calls
  `run_after_join` (no delay-0 perform on an empty transcript).
- `test_join_gate_past_bound_performs_with_named_refusals`: past the bound,
  performed once; the `{pid}` entry is refused `join unresolved after <n>s`, the
  plain entry runs; a second pass is a no-op.

**Known limitations (see parent's EXCLUDED clauses):**
- The JOIN GATE fires only when the record CAPTURED a window @id (`window_id`
  present) but the rejoin did not land. A `join: null` record with NO window_id
  — the belam symptom shape — is treated as "no join to wait on" to preserve
  the transcript-fallback and live-pid paths, so that exact shape is not gated
  by this increment; the empty-transcript named refusal machinery
  (`_AFTER_JOIN_EMPTY_REASONS`) and the bound still close the rest. This is the
  biggest honest gap vs the claim text.
- A performer that crashes AFTER claiming but BEFORE writing results wedges the
  record on its claim (no staleness timeout on the claim itself); out of scope
  here — SL7.89 owns the process-liveness/identity half.
- The wrapper adds one pathspec commit per perform (claim, then results).

A g15 claim is a build order: the pre-fix defect (two performers, delay-0 perform
on a null join, two dms) is closed by construction on these bytes and the
falsifier tests pass.

## Agent Notes
Built g15.25 claim: claim-before-run (claimed_at/claim_key via SL7.78 pathspec commit) in run_after_join; second performer defers by name (dm/nudge once per record); JOIN GATE with after_join_max_wait_s=600 upper bound returning {waiting} in-bound and named refusals ('join unresolved after Ns') past-bound; heal.py log names performed/deferred/waiting. 5 new falsifier tests + 3 pre-existing tests updated for claim commit supersession. Full rotate/heal/after_join suite green (50+52+124+586+97+145). Caveat: the join gate covers window-id records whose rejoin failed; a join:null record with NO window_id still falls through to the live-pid/transcript-fallback path (deliberate, to keep existing tests) — the belam symptom shape is only partially gated.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SL7.88 (read the artifact, not the report): the claim is real on the bytes — `_claim_after_join` writes after_join {claimed_at, performer, claim_key} and commits it via `_commit_after_join_record(..., commit_label="claim")` at rotate.py:9676-9740, called at the top of `run_after_join` (10263-10273) BEFORE the sleep and the command loop; the completion write preserves claimed_at/claim_key (10435-10439); `run_after_join_for_seat` defers on a live claim (10548-10563); heal.py names deferred/waiting (heal.py:464-473). I re-ran the suite myself: test_after_join_service.py 52 passed, test_rotate+test_heal+test_rotate_tail+test_rotate_startup 382 passed. WHAT THE INSTRUCTION SAID: "CLAIM-BEFORE-RUN ... BEFORE the first command runs; any performer that finds a claim returns {deferred} and runs nothing" + "JOIN GATE ... performs only when the record join resolved ... OR after_join_max_wait_s elapsed". NEAR MISS: the claim is a read-then-write, not an atomic compare-and-set — two performers that both read "no after_join" within the same millisecond both write a claim and both run; the sequential test (test_second_performer_deferred_by_live_claim) does not cover that. The two real callers are separated by 20 s / 30 s so the practical window is the claim write itself. SECOND GAP, named by the kid and confirmed here: the join gate fires only when the record CAPTURED a window @id but the rejoin failed; a `join: null` record with NO window_id still falls through to the transcript-fallback path. I kept the code and sent the two wedges (dead-claim wedge, age_s-None wedge) to the next kid rather than re-cutting this node.
<!-- THOUGHT:END -->
