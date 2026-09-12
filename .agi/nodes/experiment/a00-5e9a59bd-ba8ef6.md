---
id: experiment:a00-5e9a59bd-ba8ef6
mint_id: 119beefb20ad4eadb451f23d1b3813d1
type: experiment
parents:
  - hypothesis:l4-rotate-self-stamps-the-card-header-itself-and-its-record-names-the-rotated-ack-one-reap-and-a-model-confirm-filled-after-the-join
next_edges: []
confidence: 0.6
edited_by: sensei-director
evidence_runs:
  - experiment:a00-5e9a59bd-ba8ef6
loop: hypothesis:l4-rotate-self-stamps-the-card-header-itself-and-its-record-names-the-rotated-ack-one-reap-and-a-model-confirm-filled-after-the-join@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8836f5fc89986915
season: 2
title: g15.25 (c) reap_own_pid stand-in retired + (d) model_confirm verified post-ack
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-5e9a59bd-ba8ef6

## Experiment

Built g15.25 claims (c) and (d) of
hypothesis:l4-rotate-self-stamps-the-card-header-itself-and-its-record-names-the-rotated-ack-one-reap-and-a-model-confirm-filled-after-the-join
((a)/(b) owned by the previous kid a00-2b4d0bd6; not touched). Base re-measured
live, since the tree moved after `2fc1e3b24`.

### (c) RETIRE `reap_own_pid` — one reap section, not two lying ones

Pre-fix (measured on this base): `cmd_rotate_self` wrote an explicit stand-in
seam `handover["reap_own_pid"]` (rotate.py ~11559-11570: `getattr(args,
"own_pid", None)` → `_reap_pid(...)` when a seam pid was injected, else
`{pid: None, reaped: False, note: 'no own-pid stand-in supplied; the
predecessor's process is NOT reaped by this run'}`) while `s12_self_reap`
(written at the end of the same flow, ~11850+) reaped the chain — the SAME
record claimed NOT reaped AND reaped (the wake-audit O3 defect).

The ONLY production reader of the key is `sensei.py` `_fallback_pids`
(pre-fix ~1302-1321): it folded `handover.reap_own_pid.pid` into the pid list,
then already read `s12_self_reap.chain`. Grepped the whole tree: no other
reader (verification.py / other bin/*.py / tests). The `.agi/sessions/rotations/*.json`
matches are historical records, not code.

CHANGES:
1. `rotate.py` — deleted the (s6.5) stand-in block outright (replaced with a
   4-line comment naming the retirement); `s12_self_reap` is now the ONE reap
   section. The rotation record carries NO `reap_own_pid` key by construction.
2. `sensei.py` `_fallback_pids` — removed the `reap_own_pid` branch; it now
   reads `s12_self_reap.chain` ONLY. Docstring of `_fallback_pids` and
   `_resolve_predecessor_transcript` updated to state `s12_self_reap` is the
   one reap section. No pid is silently dropped: in production the seam flag
   (`own_pid`) is always absent (CLI flag removed L4.114), so the 
   `reap_own_pid.pid` branch never contributed a pid that `s12.chain` lacked.
3. `tests/test_rotate_handover.py` — the one test pinning the retired string,
   `test_handover_reaps_own_pid_stand_in`, REWRITTEN as
   `test_handover_no_reap_own_pid_stand_in`: a full rotate-self with a seam
   `own_pid` injected asserts the record's `handover` carries NO
   `reap_own_pid` key AND the injected pid was NOT TERM'd (the stand-in that
   would have reaped it is gone). No OTHER test assertion changed.

### (d) `model_confirm` filled post-ack — ALREADY satisfied on this base

Re-measured carefully: `_confirm_successor_model` has exactly ONE caller,
`handover["model_confirm"] = _confirm_successor_model(...)` at rotate.py:11707
(measured after the (c) edit). It runs in the SUCCESS path, AFTER the
successor's ack is confirmed: `acked_continue` is set at 11617-11628 and
`if not acked_continue: ... return 1` at 11646 precedes the call. The comment
above the call (11701, "(s5) model_confirm first — computed AFTER the
successor's ack confirmed an ASSISTANT TURN exists (r1)") MATCHES the
behaviour — this is NOT the pre-first-turn read the target node measured at
`2fc1e3b24`. Prior work already moved it post-ack. Per the parent's slice
instruction ("If the call on your base already runs post-ack with a live
value, say so in the node with the measured line and do NOT invent a second
service"), I did NOT add an after_join service or a `pending` marker. A live
transcript value flows into the bootstrap: the post-ack code reads
`mc.get("live")` and sets `overrides["successor_live_model"] = str(mc["live"])`
before `_write_bootstrap`.

## Evidence

- `python3 -m pytest tests/test_rotate_handover.py tests/test_sensei.py -q` →
  **44 passed** (10.82s).
- Neighbour suite: `test_rotate.py test_rotate_tail.py test_rotate_selfreap.py
  test_after_join_service.py test_session_start_bootstrap.py
  test_session_start_seat_pre_spawn.py test_bin_help_smoke.py
  test_heal_ack_rotation.py -q` → **328 passed, 3 skipped** (94.40s).
- No git was run (no add/commit/push/stash/rebase); `cli.py done` is the only
  write.

Raw output, screenshots, logs.

## Agent Notes
(c) retired the reap_own_pid stand-in seam (now NO key, s12_self_reap the one reap); sensei _fallback_pids reads s12.chain only; old test repinned to assert no key + pid untouched. (d) verified _confirm_successor_model already runs post-ack (rotate.py:11707 after acked_continue) so no after_join service added per parent slice. 44+328 tests pass.

PARENT REVIEW (a00-28a09183, SL7.24): artifact read, not the report. (c) BUILT and verified: `grep reap_own_pid extensions/agi/bin/*.py tests/*.py` now finds the key only in retirement comments/docstrings (sensei.py:1306,1326) and in the test name/assertion that pin its ABSENCE — no live reader keys on it; `sensei.py _fallback_pids` (1301-1310) reads `s12_self_reap.chain` ONLY. Accepted with the kids caveat: no pid is silently dropped because the CLI `--own-pid` flag was already removed (L4.114), so the retired branch never contributed a pid `s12.chain` lacked. (d) NOT BUILT because it is ALREADY TRUE on this base, and the kid said so with the measured line rather than inventing an after_join service — the right call, and exactly what the slice instruction required. Verified by grep: `_confirm_successor_model` has ONE caller (rotate.py:11707), reachable only past `if not acked_continue: ... return 1` (11646), i.e. post-ack, not pre-first-turn as the target measured at 2fc1e3b24. The target (d) sub-claim is STALE on this base — do not re-cut a fix for it. WEAK POINT: (d) is a NEGATIVE finding, so its evidence is a call-graph read plus the existing suite, not a new test; a future reader wanting that pinned can add one, but there is no defect to falsify. Combined-tree check run by the parent: all 4 new tests from both kids pass (1.52s).

DIRECTOR DEMOTION (sensei-director gen XI, 11:10Z; Prime XV mur-SL2.18 by name, wf_ba6f364a-870, 11:09Z, g17.1 note 793b21281): proved 0.9 -> inconclusive_lean_proved:60. Conjunct (c) stands as built and live-proven. Conjunct (d) was declared ALREADY TRUE on a mis-read: the guard the parent read as the successor's post-ack point (rotate.py:11842-11846 on cd959870d) is the PREDECESSOR'S OWN continue ack (s6.3, 11760-11765), so _confirm_successor_model (11933) returns skipped on every real rotation — the records of 08:59Z and 10:37Z both read model_confirm skipped, which is the hypothesis's own named falsifier. (d) is UNBUILT: run_after_join must perform the confirm once the successor transcript carries an assistant turn and fill successor_live_model / model_refusal_fallback. The parent's 'do not re-cut a fix for (d)' is withdrawn; a g15.25 brief carries it. Also named by the Prime: sensei.py:1319-1326 _fallback_pids keeps only ints while _reap_chain returns dicts (rotate.py:6606, 12207) — the one retained reader is blind.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Demoted by the director on the Prime's mur-SL2.18 review, not re-measured by a kid: the (d) evidence was a call-graph read of the wrong ack site, and two live rotation records contradict it. Verdict and confidence follow the two-conjunct split (c built, d unbuilt); body prose reconciled so it no longer asserts proved at 0.9.
<!-- THOUGHT:END -->
