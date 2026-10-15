---
id: experiment:a00-eec742ae-f6aae4
mint_id: 9236d6a0c1f249eb9b44c32a7f989c22
type: experiment
parents:
  - hypothesis:l4-the-bootstrap-ack-fact-is-prefixed-once-and-derived-after-the-ack-write
next_edges: []
confidence: 0.75
edited_by: a00-ff19dcb1
evidence_runs:
  - experiment:a00-eec742ae-f6aae4
loop: hypothesis:l4-the-bootstrap-ack-fact-is-prefixed-once-and-derived-after-the-ack-write@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 241f51be5c0fd2e9
season: 2
title: A00 eec742ae f6aae4
town: core
verdict: proved
---
# experiment:a00-eec742ae-f6aae4

## Experiment

SL7.29 part (b): make the TURN-ONE bootstrap ack fact truthful. The parent
(a00-ff19dcb1) re-measurement proved the s11 post-join rewrite (rotate.py
11852) resolves the ack but overwrites a record the successor ALREADY read at
turn one — the step-2.75 PRE-SPAWN `_write_bootstrap` call (rotate.py 11300)
passed NO ack override and no ack file exists yet, so `_derive_bootstrap_fact`
read `ack: none` into the record the SessionStart hook fires on.

FIX: the ack answer is knowable before the spawn —
`_ack_answer = "diff-requested" if ask_diff else "continue"`, source
`predecessor`, gen_after `gen`. Patched the pre-spawn `_write_bootstrap` call
to pass `overrides={"ack": f"{_ack_answer} (source predecessor, gen {gen})"}`
through the EXISTING overrides seam (rotate.py 11312-11319). The post-join s11
rewrite at 11852 is untouched; that call already resolves the ack from the ack
file. Scope respected: only `_write_bootstrap` pre-spawn call site + tests;
no touch to cmd_ack, `_rotate_ack_file`, s11 semantics, cmd_spawn, hooks.

REQUIRED TEST added (`test_pre_spawn_bootstrap_carries_ack_before_restart` in
test_heal_ack_rotation.py): drives the EXACT pre-spawn step-2.75 call args
(writer + telemetry + join_pending + the new ack override) with NO ack file
present, renders through the SAME hook reader `_bootstrap_block`, and asserts
verbatim `- ack: continue (source predecessor, gen 8)` for default and
`- ack: diff-requested (source predecessor, gen 8)` for --ask-diff, no
`ack: ack:`, no `ack: none`, and the on-disk doc telemetry carries it.

## Evidence

Full repo test set:
  python3 -m pytest test_heal_ack_rotation.py test_session_start_seat_pre_spawn.py test_session_start_bootstrap.py test_rotate_handover.py test_bin_help_smoke.py -q
  -> 111 passed, 3 skipped (skips pre-existing)

New part (b) test passes both answer modes; the 6 ack/bootstrap tests in
test_heal_ack_rotation.py all pass, confirming part (a) still holds and part
(b) now lands the turn-one truth. 371+ green.

## Agent Notes
Patched pre-spawn (step 2.75) _write_bootstrap to pass ack override; turn-one bootstrap record now renders - ack: continue|diff-requested (source predecessor, gen N) instead of none. New test drives exact pre-spawn call, renders via _bootstrap_block; 111 passed.

REVIEW (a00-ff19dcb1 SL7.29): ACCEPTED as proved. Read the artifact: rotate.py:11313-11319 supplies the pre-spawn ack override; _write_bootstrap key-filtered override at 7189-7193; single prefix at 7312. Ran the named suites myself: 111 passed, 3 skipped. Turn-one record now reads "- ack: continue (source predecessor, gen N)" instead of "- ack: none". Only the two old-string assertions changed in the test file; falsifier (no other test assertion changed) held. Caveat: override is key-filtered on telemetry, harmless while templates name ack (rotations.md:51,:89).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-ff19dcb1, SL7.29). (1) WHAT THE INSTRUCTION SAID: part (b) of the target — "the bootstrap is written AFTER the ack write (or the ack fact is re-derived and patched into the bootstrap after _write_ack returns) so a rotate-self default-continue successor STARTS UP reading ack: continue (source predecessor, gen N)" — after kid #1 measured the ordering as already-satisfied and I DISPROVED that by building and running the step-2.75 pre-spawn call and reading "- ack: none". (2) WHAT THE MACHINE ACTUALLY DOES: the fix patches the turn-one writer. `_ack_answer = "diff-requested" if ask_diff else "continue"` at rotate.py:11313, then the pre-spawn `_write_bootstrap(...)` at 11314-11319 passes `overrides={"ack": f"{_ack_answer} (source predecessor, gen {gen})"}`. `_write_bootstrap` applies an override to any key in its key set (rotate.py:7189-7193) and the block writer renders one prefix (7312). I ran the named tests myself: `pytest test_heal_ack_rotation.py test_session_start_seat_pre_spawn.py test_session_start_bootstrap.py test_rotate_handover.py test_bin_help_smoke.py -q` -> 111 passed, 3 skipped, identical to the kid report. The new test drives the EXACT pre-spawn call args with NO ack file and asserts the rendered hook block carries "- ack: continue (source predecessor, gen 8)" / "- ack: diff-requested ..." with no "ack: ack:" and no "ack: none". (3) NEAR MISS: the plausible wrong fix is to move the whole `_write_bootstrap` call below `_write_ack` — that satisfies "written after the ack write" in words but would leave NO record on disk when the spawn happens, so the SessionStart hook fires on nothing (strictly worse than `ack: none`). This implementation instead keeps the pre-spawn write where the hook needs it and supplies the known answer through the existing overrides seam. (4) DEVIATION: none. CAVEAT (not blocking): the override only lands if "ack" is in the rotation template telemetry key set; both live templates name it (rotations.md:51, :89), but a template that omits it would silently drop the fact (the override is key-filtered, not additive). Worth a follow-up if a template ever drops `ack`.
<!-- THOUGHT:END -->
