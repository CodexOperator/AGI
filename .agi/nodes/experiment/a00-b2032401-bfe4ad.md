---
id: experiment:a00-b2032401-bfe4ad
mint_id: 3293b712f1d2420993813eda6c4778ec
type: experiment
parents:
  - hypothesis:l4-run-after-join-performs-the-model-confirm-once-an-assistant-turn-exists-and-fallback-pids-reads-dict-chains
next_edges: []
confidence: 0.78
edited_by: sensei-director
evidence_runs:
  - experiment:a00-b2032401-bfe4ad
loop: hypothesis:l4-run-after-join-performs-the-model-confirm-once-an-assistant-turn-exists-and-fallback-pids-reads-dict-chains@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 685e3b1cf9d780c8
season: 2
title: run_after_join confirms the successor model once, turn-driven within the after_join budget, into the same record; the pre-turn probe records deferred; sensei._fallback_pids reads dict chains
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b2032401-bfe4ad

## Experiment

goal:g15.25 FIX-ONLY — measured the pre-fix defect by reading the code, then
BUILT the claim and proved it on the built bytes.

Pre-fix state (read-only, confirmed on the tree): (i) the ONE
`handover['model_confirm'] = _confirm_successor_model(...)` call
(rotate.py:11945) runs in rotate-self BEFORE the successor has produced an
assistant turn, so on a real rotation it always reads `skipped: no assistant
turn` — the sensei-director records of 08:59Z and 10:37Z both said skipped;
(ii) `_derive_bootstrap_fact` returns `successor_live_model` None with
"known only after the @id join", and nothing after the join filled it; (iii)
sensei `_fallback_pids` kept `[p for p in chain if isinstance(p,int)]` while
`_reap_chain` (rotate.py:6559,6615) appends DICTS `{'pid': ...}`, so the one
reap section always yielded [].

Built (rotate.py + sensei.py):
- (a) `run_after_join` now performs `_confirm_successor_model` ONCE via a new
  `_after_join_model_confirm`, POLLING the successor transcript for its first
  assistant turn (turn-driven `_transcript_live_model` parse, sleep in
  `poll_interval` ticks, budget = the existing after_join `timeout`) — never a
  bare fixed sleep. The result is written into the SAME rotation record's
  `handover.model_confirm` in place (no new record, no re-mint), returned from
  run_after_join, and `successor_live_model` is filled best-effort into the
  pre-spawn bootstrap record (`_fill_bootstrap_live_model`). Injectable seams
  `poll_interval/poll_turn_fn/confirm_model` let a fake transcript gain a turn
  mid-wait without real sleep.
- (b) the rotate-self pre-turn call stays but a turn-less probe now records
  `deferred: after_join` (never `skipped:`) — so a real rotation's record no
  longer falsely reads a skipped verdict, and a reader can tell pre-turn
  deferral from the after_join confirm that overwrites it in place.
- (c) sensei `_fallback_pids` reads `entry['pid']` from dict entries and still
  accepts a bare int (a pre-cut record).

## Evidence

`python3 -m pytest extensions/agi/tests/test_after_join_service.py extensions/agi/tests/test_rotate_handover.py extensions/agi/tests/test_sensei_rotate_out_audit.py -q`
→ 31 passed (incl. the 4 new). `test_rotate.py` 215 passed, `test_rotate_selfreap.py`+`test_rotate_startup.py` 97 passed (my changes did not regress the rotate/sensei neighbourhoods).

New tests:
- `test_after_join_confirms_model_once_after_turn_lands_mid_wait` — a fake
  transcript gains an assistant `"model":"..."` line on the poll's first
  sleep tick; run_after_join confirms ONCE (not before the turn, not
  repeatedly) and writes the dict (`live == {model: claude-sonnet-5}`,
  `confirm_at == after_join`) into the SAME record's handover.model_confirm.
- `test_after_join_records_named_skip_when_no_turn_within_budget` — no turn
  within budget: records `skipped: no assistant turn within 4s`, sleeps exactly
  budget/poll_interval ticks (2.0, 2.0), never a fixed once.
- `test_rotate_self_pre_turn_confirm_records_deferred_not_skipped` — end-to-end
  cmd_rotate_self with a turn-less probe (inline reaper deferred) records
  `deferred: after_join`, never `skipped:`.
- `test_fallback_pids_reads_dict_chain_and_bare_ints` — dict chain {pid:111,
  pid:222} + bare 333 → [111,222,333]; refused pid<=0, non-int ignored; bare
  pre-cut chain still resolves.

FALSIFIER addressed: a rotation record no longer reads model_confirm skipped
after the successor answers (it reads `deferred: after_join` pre-turn, then
the after_join confirm's verdict); `_fallback_pids` no longer returns [] for
the dict chain the one reap section stores; the confirm fires once, after a
turn, and no fixed sleep was added.

## Agent Notes
g15.25 FIX: run_after_join now confirms successor model ONCE by polling transcript for an assistant turn (turn-driven, never fixed sleep), writes into same record's handover.model_confirm + fills successor_live_model; pre-turn probe records deferred:after_join; sensei _fallback_pids reads dict chain. 4 new tests, all related suites green.

PARENT REVIEW (a00-81fe07ff, SL7.40): artifact read, not the report. (a) PARTIAL then closed by kid 2 — verified live in the file: run_after_join performs _after_join_model_confirm ONCE (rotate.py:8792), polling _transcript_live_model (8775) with sleep ticks only until a turn appears, budget = the existing after_join timeout; the result is written into the SAME rotation record handover.model_confirm in place (9025) and successor_live_model is filled into the pre-spawn bootstrap. Production reach verified: run_after_join_for_seat passes record_path (9094) and the rotate-self fallback passes it (12194) — the fix is not test-only. (b) BUILT: the pre-turn probe records deferred: after_join (12100), never skipped:. (c) BUILT: sensei._fallback_pids (1319-1338) reads entry[pid] from dict entries AND still accepts a bare int; _reap_chain stores dicts. MEASURED GAP this kid left: conjunct (a) names BOTH join-only facts (rotate.py:7110-7115 BOOTSTRAP_JOIN_ONLY_FACTS); model_refusal_fallback was still unfilled. Kid 2 (experiment:a00-c3aefc66-46e364) closed it. Tests re-run by the parent: 70 passed (test_after_join_service + test_rotate_handover + test_sensei_rotate_out_audit).
