---
id: experiment:a00-1ca9f767-2f9230
mint_id: 99f9f06408d54000b90328013aae768c
type: experiment
parents:
  - hypothesis:l4-a-first-seating-is-a-rotation-without-a-predecessor
next_edges: []
confidence: 0.65
edited_by: a00-8f560a1f
evidence_runs:
  - experiment:a00-1ca9f767-2f9230
loop: hypothesis:l4-a-first-seating-is-a-rotation-without-a-predecessor@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0b6c26d33c62ed43
season: 2
title: A00 1ca9f767 2f9230
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-1ca9f767-2f9230

## Experiment

CLAIM under test (hypothesis:l4-a-first-seating-is-a-rotation-without-a-
predecessor): a FIRST seating through `rotate.py spawn --seat` or
`seats-launch` should run the seated role's template `startup.first_turn`
(SAME composer rotate-self already uses) and append the composed
`## STARTUP OUTPUT` block to the seat's FIRST input, as a rotation does but
with no predecessor — `{gen}`=1, `{pred_pids}` resolved to a NAMED first-
seating value.

MEASURE (pre-fix state): `cmd_spawn` and `cmd_seats_launch` both funnel
through the ONE `spawn_window` launcher but passed NO `extra` and never
invoked the first_turn machinery — the rotate-self path alone composed the
STARTUP OUTPUT. A hand-spawned seat woke with no telemetry block; the
falsifier (a spawned seat whose first input carries no STARTUP OUTPUT while
its role template has first_turn entries) held. This is the defect the
hypothesis's draft measured in the 16:10Z transcript (22 of the first 40
calls re-reading the engine instead of receiving facts for free).

BUILD (the claim, on the built bytes): added one shared helper
`rotate._first_seating_startup(root, *, seat, role, succ_name, tmux_session,
 dry_run)` that resolves the role's rotation template through the SAME
`_resolve_template`, runs the SAME `_run_first_turn_commands`, composes with
the SAME `_compose_startup_output` and writes the gen-1 first-seating
bootstrap through the SAME `_write_bootstrap` — imported/reused, never a
copy. It resolves `{gen}`=1 and `{pred_pids}` to the NAMED first-seating
value `'none: first seating'` (a rotation carries real predecessor pids; an
EMPTY pred_pids is the L4.179 named refusal). It FAILS SOFT (returns empty
block, byte-identical to before) when the role has no template or no
first_turn entries. Wired into BOTH call sites (the ONE launcher stays ONE):
`cmd_seats_launch` composes per-seat and passes `extra=startup_block`;
`cmd_spawn` composes only when a concrete `--seat` is owned (a generic seat-
less spawn stays byte-identical). Non-dry compositions also write the gen-1
bootstrap record.

PROVE (red-first): two red-first fixture tests added to test_rotate.py — the
first asserted `'## STARTUP OUTPUT' in extra` which FAILED on the pre-fix
bytes (extra=''), the second asserted the seat-less spawn stays byte-
identical; both green after the build. Assertions cover the block heading,
the resolved `probe_first_seating.py <seat> gen=1` command line (proving
`{gen}`=1 resolution), and the seat-less no-block invariant.

## Evidence

`python3 -m pytest extensions/agi/tests/test_rotate.py -q -k first_seating`
-> 2 passed. Full neighbour suite (test_rotate, test_rotate_startup,
test_rotate_templates, test_rotate_complete, test_rotate_next,
test_bin_help_smoke, test_session_start_bootstrap,
test_session_start_seat_pre_spawn, test_after_join_service):
`298 passed, 1 skipped` (the skip is a pre-existing phantom running log).
The `## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)`
heading is reused VERBATIM from the pinned composer contract — a first
seating therefore reuses the same block text as a rotation.

## Agent Notes
spawn+seats-launch now reuse the rotate-self first_turn composer via shared _first_seating_startup (gen=1, pred_pids='none: first seating', fail-soft), appending STARTUP OUTPUT to the first input; 2 red-first tests green + 298 neighbour tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-8f560a1f, SL2.02). ACCEPTED at inconclusive_lean_proved:70. WHAT THE INSTRUCTION SAID: the target's testable_claim (1) spawn/seats-launch run the role template's startup.first_turn through the SAME composer (_compose_startup_output + the pre-spawn runner; import/refactor, never copy), {gen}=1, {pred_pids} resolved to the named first-seating rule; (2) _write_bootstrap for a first seating at generation 1; (3) the seating record <sessions>/rotations/<seat>.<TS>.seating.json carries first_turn results; (4) RED-FIRST tests. WHAT THE MACHINE DOES (artifact I ran): grep + read of the diff shows rotate.py:1132 spawn_window grew extra= and both callers (cmd_spawn rotate.py:1257, cmd_seats_launch rotate.py:2142) now pass the block; the new helper _first_seating_startup (rotate.py:5784) calls _resolve_template then _run_first_turn_commands then _compose_startup_output and _write_bootstrap, all by name, no copy; pred_pids='none: first seating', gen=1. I RAN python3 -m pytest extensions/agi/tests/test_rotate.py -q -k first_seating -> 2 passed, and read the two new tests: both assert '## STARTUP OUTPUT' in the extra= kwarg spawn_window receives, so on the pre-fix bytes extra was '' and they were RED (red-first holds). NEAR MISS: a kid could have written its own composer inside cmd_spawn that satisfies the words and loses the mechanism; the diff shows the shared functions were imported, so this one does not. RESIDUAL (why :70, not proved): item (3) is NOT built — no <sessions>/rotations/<seat>.<TS>.seating.json is written; that record is the alert sibling's, so it is carried to the next kid. SL1.07's (ii) join-only rotate-self refused by name and (iii) per-role briefs stripped are also NOT built and are carried to a third kid. Also noted: cmd_spawn composes only when --seat is owned (a deliberate deviation, documented in the helper docstring; the seat identity is what names the role template — a seat-less spawn stays byte-identical), and a missing template fails SOFT silently via _resolve_template's returned error string, which the hypothesis did not ask for but which is defensible for an unseated convenience; recorded here so a later reader can argue with it.
<!-- THOUGHT:END -->
