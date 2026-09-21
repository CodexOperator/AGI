---
id: experiment:a00-4756043d-f8729f
mint_id: 1d0f698626344325b7ce14f913fd6b23
type: experiment
parents:
  - hypothesis:l4-prepare-measures-and-merges-the-same-ref-guard-first-and-check-5-prefers-the-rows-transcript
next_edges: []
confidence: 0.9
edited_by: a00-4f25c9b5
evidence_runs:
  - experiment:a00-4756043d-f8729f
loop: hypothesis:l4-prepare-measures-and-merges-the-same-ref-guard-first-and-check-5-prefers-the-rows-transcript@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: aa0cf521fcb21001
season: 2
title: A00 4756043d f8729f
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4756043d-f8729f

## Experiment

P1-d + P2-b + R1 (goal:g15.14) on `rotate.py`. Built on the P1-a/P1-b/P1-c
inherited from the two prior kids; none of their code changed.

**P1-d — check 5's clear line prefers the ROW's transcript.** In
`_prepare_checks` check 5 the `known_transcript` was filled from the pin's
record FIRST (`_parse_pin_record` → `written_path`), falling back to the
config:seats row. When check 5 BLOCKS (stale_pin) the pin is another
generation's by definition, so preferring it named the WRONG transcript for
the re-point. Swapped the order: prefer the row's transcript
(`transcript_path` or `transcript_from_registry_dict(seat_row)`, the same
derivation the meter uses), and fall back to the pin's `written_path` only
when the row has none.
FALSIFIER (checked): row carries a `session_id`+`cwd`, pin is stale → the
clear line names the row-derived transcript, not the pin's written_path.

**P2-b — `.claude/tasks` reader deleted.** `_background_tasks` counted
`Path(root)/.claude/tasks/` — a path that NEVER exists under a worktree
(measured: the worktree has `.claude/` with only `settings.json` +
`workflows/`, no `tasks/`). The harness writes per-session task state to the
GLOBAL `~/.claude/tasks/<uuid>/` (3-4 uuid dirs present), keyed by uuid, with
no per-seat stable meaning. Per the round brief: a reader that never reads is
a lie — deleted rather than re-pointed, because no per-seat stable path
exists to point it at. Falsifier safe: no `tasks-dir` naming can be produced
now; the `_proc_children` pid path survives as the only source.

**R1 — registry gate in the rotate-self `--prepare` path.** `cmd_rotate_self`
delegated `--prepare` straight to `cmd_prepare`, which has NO registry
check, and `--prepare` sets `perform = not dry_run`. So
`rotate-self --prepare --name <unregistered>` on a behind clean worktree
would MERGE before refusing `no seat` — P1-c's hazard one spelling over.
Added the same gate (seat exists in `config:seats` unless `--throwaway`) in
the `--prepare` path, before any merge.
FALSIFIER (checked): `_real_repo` fixture (behind, clean merge), `ghost`
unregistered → refuses `no seat`, HEAD unmoved, `season.txt` absent.

## Evidence

Commands:
```
python3 -m pytest extensions/agi/tests/test_rotate_prepare.py -q
# 28 passed (was 26; +test_prepare_check5_clear_line_prefers_row_transcript_over_stale_pin,
#            +test_rotate_self_prepare_unregistered_name_refuses_without_merge)

python3 -m pytest extensions/agi/tests/test_rotate.py \
                  extensions/agi/tests/test_rotate_g1517.py \
                  extensions/agi/tests/test_rotate_handoff_driven.py \
                  extensions/agi/tests/test_rotate_startup.py -q
# 233 passed

python3 -m pytest extensions/agi/tests/test_after_join_service.py \
                  extensions/agi/tests/test_session_start_seat_pre_spawn.py -q
# 10 passed
```
All green. One existing test (`test_rotate_self_perform_merge_during_prepare_gate`)
previously passed via the missing registry check; it now registers the seat
(`_seat_row(prep_root, 3)`) so it exercises the R1 gate with a *registered*
name — the correct behaviour guard.

## Agent Notes
P1-d+P2-b+R1 in rotate.py: check5 clear line prefers ROW transcript over stale-pin written_path; .claude/tasks never-reading reader deleted (harness writes global ~/.claude/tasks/<uuid>, no per-seat path); registry gate added to rotate-self --prepare path before any merge. 28 prepare + 233 rotate/neighbour + 10 after_join/seat_pre_spawn tests green. Two new falsifier tests.

PARENT REVIEW a00-4f25c9b5 (SL5.06, kid 3/3), accepted. Evidence re-run by the parent: pytest test_rotate_prepare.py 28 passed; the wider rotate/after_join/seat_pre_spawn/g1517/handoff_driven neighbours 303 passed. P1-d verified: _prepare_checks check 5 now resolves known_transcript from the config:seats ROW first (transcript_path or transcript_from_registry_dict) and falls back to the stale pin written_path only when the row has none (rotate.py:8127-8146); the test builds a stale pin + a row with session_id/cwd and asserts the row-derived path is printed and the pin predecessor path is not. P2-b verified: the .claude/tasks reader is DELETED, not re-pointed (rotate.py _background_tasks) — the parent independently measured that ~/.claude/tasks/<uuid>/ is global and uuid-keyed with no per-seat meaning, so the deletion is right and the docstring says why; the _proc_children pid source survives. R1 verified: cmd_rotate_self prepares path now runs the registry gate before delegating to cmd_prepare (rotate.py:8682), falsified by a real-git behind fixture with --prepare --name ghost refusing with no merge. No residue found in this kid; the round is complete for the target testable_claim P1-a..d + P2-a/b.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review version (a00-4f25c9b5, SL5.06, kid 3): accepted for P1-d + P2-b + R1; this version adds the parent review note. Mechanism check against the instruction: the claim says "prefer the row session_id transcript, fall back to the pin only when the row has none" and "fix the path ... if none is stable, DELETE the reader". What the machine does (rotate.py:8127): the row lookup moved above the pin assignment and the pin written_path is consulted only when known_transcript is still None; the .claude/tasks block is gone from _background_tasks with the reason in its docstring. Near miss that satisfies the words and loses the mechanism: re-pointing the tasks reader at the global ~/.claude/tasks/<uuid>/ would keep a "counting" line that describes no seat — the kid deleted it instead, which is what the brief authorised. Deviation: none; the parent used write.py and re-ran the suite.
<!-- THOUGHT:END -->
