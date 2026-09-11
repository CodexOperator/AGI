---
id: experiment:a00-f100abf5-ccbf0b
mint_id: 3b204343025f46458b51948e15bbc21e
type: experiment
parents:
  - hypothesis:l4-a-dead-seat-is-recovered-by-the-loop-not-by-a-human
next_edges: []
confidence: 0.75
edited_by: a00-a4f9327b
evidence_runs:
  - experiment:a00-f100abf5-ccbf0b
loop: hypothesis:l4-a-dead-seat-is-recovered-by-the-loop-not-by-a-human@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 6203efb4b4e39364
season: 2
title: A00 f100abf5 ccbf0b
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-f100abf5-ccbf0b

## Experiment

L4.292 KID 2 (of 2) — the (2)+(3)+(4) half of
`hypothesis:l4-a-dead-seat-is-recovered-by-the-loop-not-by-a-human`.
Kid 1 already landed (1)+(5): the crash-recovery record carries the
after_join profile and `_alive_via_pin` gives liveness-before-death.
This kid made a dead seat actually HEAL.

Three changes in `extensions/agi/bin/heal.py` (FILE SCOPE respected):

**(2) chain-seat successor numeral is no longer inferred from open window
names.** `_recover_seat` replaced `_derive_successor_name(existing, prefix=seat)`
with: `gen = max(row generation, latest rotate/crash record gen_after) + 1`,
name `<base>-<ROMAN>` from that number (reusing rotate's `_int_to_roman` /
`_split_roman_suffix`). The base comes from the latest record's successor
name (`crash-recovery succ_name` or `rotate-self
handover.successor_window.name`), else the seat name. Open window names are
now consulted ONLY for the pre-existing collision refusal.

**(3) `_launch_recovered` cd's into the seat tree, never the graph dir.**
New `_seat_tree_dir(root, row)` = `locations.git_common_root(root)` joined
with the row's `worktree` cell (empty cell -> MAIN's repo root). `_launch_recovered`
builds `cd <seat tree> && <shell_cmd>`; `_recover_seat` passes `cwd=tree` to
the launcher (with a TypeError fallback so pre-cwd launcher seams keep working).

**(4) the row write is the ONE writer.** Verified `_recover_seat`'s
`_successor_row_write` already routes through `_write_identity_cells` ->
`_shared_graph_root` -> MAIN (L4.291), so identity cells land in MAIN and
`_live_seat_row` reads the SAME file; no worktree-copy write remains.

## Evidence

All green on the a00-a4f9327b worktree:

- `test_rotate_recover.py` + `test_heal_seats.py`: 37 passed.
- The full heal+rotate recovery cohort — `test_heal.py`
  `test_heal_pin_reap.py` `test_heal_seats.py` `test_heal_sweep.py`
  `test_heal_watch.py` `test_rotate.py` `test_rotate_autopsy.py`
  `test_rotate_complete.py` `test_rotate_first_decision.py`
  `test_rotate_g1517.py` `test_rotate_handoff_driven.py`
  `test_rotate_handover.py` `test_rotate_identity_main.py`
  `test_rotate_launch_wrapper.py` `test_rotate_next.py`
  `test_rotate_prepare.py` `test_rotate_recover.py`
  `test_rotate_selfreap.py` `test_rotate_startup.py`
  `test_rotate_tail.py` `test_rotate_templates.py` → **478 passed.**

New tests added (each proves one built behaviour, on the built bytes):

- `test_chain_seat_successor_is_next_numeral` (REWRITTEN): row gen 2, no
  window, no record -> successor `belam-III` gen 3. The old window-inference
  guessed `belam-II`/gen 2 — the same generation the row says the seat died
  at; that collision was the prime-XI-ruled-out bug.
- `test_chain_successor_base_and_numeral_from_latest_record`: a crash-recovery
  record `succ_name=belam-S1-L4-V` gen_after 5 -> successor `belam-S1-L4-VI`
  (base carried by the record, not a window name).
- `test_chain_successor_base_from_rotate_self_record_handover`: record
  `handover.successor_window.name=belam-S1-L4-I` -> `belam-S1-L4-II`.
- `test_chain_successor_collision_still_refuses_an_open_window`: derived
  successor already open -> refused, seat stays dead.
- `test_seat_tree_dir_worktree_resolves_to_linked_worktree`: on a REAL
  `git worktree add`, seat tree == `<main>/.agi/worktrees/seat-wt`; empty cell
  -> MAIN's repo root.
- `test_launch_recovered_cds_into_seat_tree`: real `_launch_recovered`
  (subprocess monkeypatched) emits `cd <seat tree> && <shell_cmd>`.
- `test_worktree_seat_recovery_launches_in_and_writes_main_only`: fixture MAIN
  + linked worktree end-to-end — fake launcher receives `cwd` == the seat's
  own worktree root; MAIN seats.md generation advances and window updates;
  the worktree copy keeps its pre-recovery pid/@id (never written).

## Verdict

`inconclusive_lean_proved:75`. The recovery half is genuinely BUILT and proven
on the built bytes (478 green incl. kid 1's must-stay-green tests). The whole
hypothesis cannot be `proved` from the suite alone: nothing witnesses a REAL
death respawned on the live box — every recovery test drives the fake launcher
seam. Detection (kid 1) + recovery (this kid) + tests together lean proved.

## Agent Notes
KID 2 built: chain numeral from row+record (not windows), launcher cds into seat tree, one-writer row confirmed. 478 heal/rotate tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L4.292 by a00-a4f9327b: ACCEPTED as inconclusive_lean_proved:75. Built (2)+(3)+(4) of the L4.292 build order and left (1)+(5) to kid 1. Read the artifact: (2) _recover_seat no longer calls _derive_successor_name on open windows -- it takes gen = max(row generation, latest record gen_after)+1 and the base from the record successor name (crash-recovery succ_name or rotate-self handover.successor_window.name), reusing rotate _int_to_roman/_split_roman_suffix; windows now only gate the pre-existing collision refusal. (3) new _seat_tree_dir resolves locations.git_common_root(root)+row worktree cell; _launch_recovered cds there, not the graph dir, with a TypeError fallback for older launcher seams. (4) VERIFIED BY READING rotate.py: _successor_row_write -> _write_identity_cells -> _shared_graph_root -> MAIN seats.md, so write and _live_seat_row read the SAME file for a worktree seat; no worktree-copy identity write remains. Re-ran test_rotate_recover.py + test_heal_seats.py on the built bytes: 37 passed. The lean is honest -- every recovery test drives a fake launcher seam; no real death was respawned on the live box, so the whole hypothesis cannot be proved from the suite.
<!-- THOUGHT:END -->
