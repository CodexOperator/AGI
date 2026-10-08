---
id: experiment:a00-5cf87475-20e04f
mint_id: a7a1ce957327405f88f499fe7295aff7
type: experiment
parents:
  - hypothesis:l4-rotations-startup-commands-must-parse
next_edges: []
confidence: 0.8
edited_by: a00-3c205862
evidence_runs:
  - experiment:a00-5cf87475-20e04f
loop: hypothesis:l4-rotations-startup-commands-must-parse@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9497e865b36c7415
season: 2
title: A00 5cf87475 20e04f
town: core
verdict: proved
---
# experiment:a00-5cf87475-20e04f

## Experiment

Implements the EMPTY-placeholder refusal half of
hypothesis:l4-rotations-startup-commands-must-parse (kid 2; kid 1 in
experiment:a00-67d7e9d2-dd897b built the READ-ONLY `status --record latest`
half and was blocked on the config gate). Scope: rotate.py region 4200+
(resolver / first_turn runner) and the startup test file. Never touched
config:rotations, the live seats row, or the first_turn executor (3803-4170).

`_resolve_startup_placeholders` gained an opt-in keyword-only parameter
`refuse_empty: bool = False`. With it True, a canonical placeholder the
command USES whose value resolves to "" raises ValueError
(`placeholder {key} empty at spawn`) instead of substituting "" and running.
`_run_first_turn_commands` (the first_turn path) now passes
`refuse_empty=True`; the other two callers (the driven `next` walk at 4524,
and the direct-helper bootstrap at 4251's sibling callers) leave it False and
are untouched — an empty placeholder there stays a legitimate "" substitution.
The refusal surfaces as a result dict `refused: "placeholder {succ_ref} empty
at spawn"` — the named refusal the brief asked for, no usage dump, executor
never runs the entry.

## Evidence

- Live probe: entry using `{succ_ref}` with `succ_ref=""` →
  `REFUSED: placeholder {succ_ref} empty at spawn` (off the built bytes).
- NEW tests in extensions/agi/tests/test_rotate_startup.py:
  (a) `test_r_empty_first_turn_placeholder_refused_named_no_marker` — probe
      script via `{succ_ref}` with empty value → refused, named "succ_ref",
      "empty at spawn", marker file ABSENT (executor never ran it);
  (b) `test_s_nonempty_first_turn_placeholder_still_runs` — same cmd with
      `succ_ref="abc123"` → rc 0, marker file present (happy path intact);
  (c) `test_t_other_callers_resolve_empty_happily` —
      `_resolve_startup_placeholders(..., {"succ_ref": ""})` returns the
      command with `{succ_ref}` → "" and no "{" left, no exception (HAZARD:
      other callers not forced to fall over on empty).
- Full rotate suite green: 219 passed (test_rotate / _complete / _handover /
  _next / _selfreap / _startup / _tail / _templates).

Caveat: the sibling half — renaming `rotation-record` in config:rotations
and dropping `seat-row` — remains gated behind the owner/prime manual-edit
role (goal:g12) and was not touched; test_rotate_templates.py's
FIXED_FIRST_TURN still pins the intended template shape. This kid's refusal
closes the code-side leak so an EMPTY placeholder can no longer run into a
usage dump even before the config lands.

## Evidence

Repository test suite (files changed or covering them):
  python3 -m pytest extensions/agi/tests/test_rotate_startup.py \
        extensions/agi/tests/test_rotate_templates.py -q        -> 37 passed
<!-- BODY:BEGIN -->
# experiment:a00-5cf87475-20e04f

## Experiment

Implements the EMPTY-placeholder refusal half of
Implements the EMPTY-placeholder refusal half of
hypothesis:l4-rotations-startup-commands-must-parse (kid 2; kid 1 in
experiment:a00-67d7e9d2-dd897b built the READ-ONLY `status --record latest`
half and was blocked on the config gate). Scope: rotate.py region 4200+
(resolver / first_turn runner) and the startup test file. Never touched
config:rotations, the live seats row, or the first_turn executor (3803-4170).

`_resolve_startup_placeholders` gained an opt-in keyword-only parameter
`refuse_empty: bool = False`. With it True, a canonical placeholder the
command USES whose value resolves to "" raises ValueError
(`placeholder {key} empty at spawn`) instead of substituting "" and running.
`_run_first_turn_commands` (the first_turn path) now passes
`refuse_empty=True`; the other two callers (the driven `next` walk at 4524,
and the direct-helper bootstrap at 4251's sibling callers) leave it False and
are untouched — an empty placeholder there stays a legitimate "" substitution.
The refusal surfaces as a result dict `refused: "placeholder {succ_ref} empty
at spawn"` — the named refusal the brief asked for, no usage dump, executor
never runs the entry.

## Evidence

- Live probe: entry using `{succ_ref}` with `succ_ref=""` →
  `REFUSED: placeholder {succ_ref} empty at spawn` (off the built bytes).
- NEW tests in extensions/agi/tests/test_rotate_startup.py:
  (a) `test_r_empty_first_turn_placeholder_refused_named_no_marker` — probe
      script via `{succ_ref}` with empty value → refused, named "succ_ref",
      "empty at spawn", marker file ABSENT (executor never ran it);
  (b) `test_s_nonempty_first_turn_placeholder_still_runs` — same cmd with
      `succ_ref="abc123"` → rc 0, marker file present (happy path intact);
  (c) `test_t_other_callers_resolve_empty_happily` —
      `_resolve_startup_placeholders(..., {"succ_ref": ""})` returns the
      command with `{succ_ref}` → "" and no "{" left, no exception (HAZARD:
      other callers not forced to fall over on empty).
- Full rotate suite green: 219 passed (test_rotate / _complete / _handover /
  _next / _selfreap / _startup / _tail / _templates).

Caveat: the sibling half — renaming `rotation-record` in config:rotations
and dropping `seat-row` — remains gated behind the owner/prime manual-edit
role (goal:g12) and was not touched; test_rotate_templates.py's
FIXED_FIRST_TURN still pins the intended template shape. This kid's refusal
closes the code-side leak so an EMPTY placeholder can no longer run into a
usage dump even before the config lands.

## Evidence

Repository test suite (files changed or covering them):
  python3 -m pytest extensions/agi/tests/test_rotate_startup.py \
        extensions/agi/tests/test_rotate_templates.py -q        -> 37 passed
  python3 -m pytest <all 8 rotate test files> -q                -> 219 passed

## Agent Notes
Implemented opt-in refuse_empty on _resolve_startup_placeholders; _run_first_turn_commands passes it True so a first_turn placeholder resolving EMPTY is refused NAMED (placeholder {succ_ref} empty at spawn) and never run. 3 new tests in test_rotate_startup.py (refused+no-marker, happy-path runs, other-caller resolves empty happily). Full rotate suite 219 passed. Sibling config half (rotation-record rename / seat-row drop) still owner/prime-gated.

PARENT REVIEW (a00-3c205862): ACCEPTED, verdict proved confirmed on the artifact. VERIFIED independently: _resolve_startup_placeholders has keyword-only refuse_empty=False and raises ValueError on an empty used placeholder only when True; _run_first_turn_commands passes refuse_empty=True (rotate.py:4263); live probe of the seat-row entry with succ_ref empty returns refused: placeholder {succ_ref} empty at spawn and the executor never runs; the other caller still resolves empty happily (x {succ_ref} y -> x  y); test_rotate_startup.py 29 passed; the full 8-file rotate suite 219 passed (re-ran, 65s). SCOPE honest: config:rotations untouched, executor 3803-4170 untouched. RESIDUAL (not a defect of this node, a banked prime/owner step): the live rotations.md still names rotate.py whois (a NON-empty placeholder, so this gate does NOT catch it) and still carries seat-row; test_rotate_templates.py pins a hardcoded FIXED_FIRST_TURN copy, so no test reads the live template. The hypothesis falsifier — a rendered first_turn command that exits 2 on usage — therefore remains TRUE for rotate.py whois until the owner/prime lands the config edit under goal:g12. COSMETIC: the node body repeats the first sentence and the intro of the Experiment section twice.
