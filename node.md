---
id: experiment:a00-e95c7ff6-23ee98
mint_id: fa1199e2951940b0ad18f4e90cd80949
type: experiment
parents:
  - hypothesis:l4-an-after-join-entry-whose-placeholder-resolves-empty-is-refused-by-name-and-skipped-never-run-on-the-empty-slot
next_edges: []
confidence: 0.9
edited_by: a00-cd486d14
evidence_runs:
  - experiment:a00-e95c7ff6-23ee98
loop: hypothesis:l4-an-after-join-entry-whose-placeholder-resolves-empty-is-refused-by-name-and-skipped-never-run-on-the-empty-slot@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c37f12e99f2424fc
season: 2
title: A00 e95c7ff6 23ee98
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e95c7ff6-23ee98

## Experiment

FIX-ONLY build round on `_run_after_join_command`. Before: an after_join entry
that USED a placeholder resolving to EMPTY ran on the empty slot — a MAIN post
with no predecessor chain (`{pred_pids}` = `''`) ran `grep -E ''`, matched
every line, and dumped the whole process table into the rotation record and
the successor's dm. first_turn refuses an empty USED placeholder by name
(`refuse_empty=True`), but after_join called resolve with `refuse_empty=False`
and never refused.

Implemented (mined to `extensions/agi/bin/rotate.py`, in `_run_after_join_command`
only):

1. New `_AFTER_JOIN_EMPTY_REASONS` map + `_after_join_empty_refusal` helper.
2. In `_run_after_join_command`, before resolution, scan the command's USED
   placeholders (bare `{k}`; `#{k}` tmux literals pass through). A used
   placeholder whose value resolves EMPTY and has no usable fallback → return a
   named refusal `placeholder {key} empty: <reason> — skipped by name`, with NO
   `rc` and NO `output` (the entry never reaches the executor).
   Reasons: `pred_pids` → `no predecessor chain`; `succ_ref` →
   `row session_ref empty`; `gen` → `no generation resolved`; any other
   placeholder → `value empty` (still refuses, never a silent pass).
3. Resolution now uses `refuse_empty=True` with the per-entry `fallback:`
   passed through, so a usable fallback (per-entry wins, else the code map
   `_STARTUP_FALLBACKS`) substitutes instead of refusing — the SAME precedence
   first_turn uses. **DECISION (stated): fallback IS honored.** The only code
   fallback today is `{prime_ref}` → `--key {prime_key}`, so the realistic
   emptied placeholders (`pred_pids`, `succ_ref`, `gen`) refuse. Honoring it
   keeps after_join and first_turn agreeing on the same template command, and
   the `#`-literal and unknown-key handling stay byte-identical.
4. The dm needs NO new branch — the refused result (no `rc`) hits the EXISTING
   `REFUSED` branch of `_compose_after_join_dm`.
5. A first seating's NAMED value `none: first seating` is a NON-empty string
   and still runs (its grep matches nothing, exit 1 — expected, not a refusal).

DRY-RUN (known gap, not fixed — out of scope): `run_after_join`'s dry-run
branch (rotate.py ~9750) still calls `_resolve_startup_placeholders(cmd,
values, refuse_empty=False)`, so in a dry-run an empty `{pred_pids}` is
substituted to `''` and the entry is shown as `dry: True`, NOT refused — an
inconsistency with the real path that now refuses. This was deliberately left
since the assignment excluded `run_after_join`'s dry-run reshaping; a later
round can align dry-run to call the same `_after_join_empty_refusal`.

## Tests (in `extensions/agi/tests/test_after_join_service.py`, 8 added)

- `test_empty_pred_pids_refuses_named_never_runs` — empty `{pred_pids}` → no
  `rc`/`output`, refusal names placeholder + "no predecessor chain"; a
  subprocess guard proves it never executes.
- `test_non_empty_pred_pids_runs` — non-empty value runs (rc present).
- `test_first_seating_named_value_runs_not_refusal` — `none: first seating`
  runs, not a refusal.
- `test_empty_succ_ref_ack_refuses_named` — the ack entry's empty `{succ_ref}`
  refuses by name (generic, not a reap-proof special case).
- `test_empty_gen_refuses_named` — `gen` → "no generation resolved".
- `test_unmapped_empty_placeholder_still_refuses_named` — no reason map entry
  still refuses, naming + "skipped by name".
- `test_usable_per_entry_fallback_resolves_instead_of_refusing` — a usable
  per-entry `fallback:` resolves, not refuse.
- `test_usable_code_fallback_prime_ref_resolves` — `{prime_ref}` empty → code
  map resolves to `--key {prime_key}` (by-key whois form).
- `test_dm_prints_refused_and_refusal_line_for_empty_pred_pids` — real
  `run_after_join` dm prints `REFUSED` + the refusal line through the EXISTING
  refused branch, one dm sent.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_after_join_service.py -q
26 passed in 1.64s
$ python3 -m pytest extensions/agi/tests/test_after_join_service.py \
    test_rotate_startup.py test_rotate.py test_rotate_selfreap.py \
    test_rotate_templates.py test_rotate_handover.py -q
453 passed in 137.28s
```

Repro of the defect on the FIXED bytes (empty `{pred_pids}`):
`entry {label: reap-proof, refused: placeholder {pred_pids}…}` →
`placeholder {pred_pids} empty: no predecessor chain — skipped by name`, no
`rc`, no `output`.

Sample refusal from the fix:
`placeholder {pred_pids} empty: no predecessor chain — skipped by name`.

## Agent Notes

Fix implemented and proved: the empty-used-placeholder entry is refused by
name and never executed, generic to every after_join entry, fallback honored
with first_turn's precedence, dm uses the existing REFUSED branch. Dry-run
path left inconsistent as a stated known gap (excluded from scope).

## Agent Notes
FIX-ONLY: _run_after_join_command now refuses a used-empty placeholder by name (pred_pids/succ_ref/gen reasons), never runs on the empty slot; fallback honored w/ first_turn precedence; dm uses existing REFUSED branch. 26 after_join + 453 rotate-suite tests pass. Dry-run path left inconsistent (stated gap, out of scope).

## Agent Notes
FIX-ONLY: _run_after_join_command refuses a used-empty placeholder by name (pred_pids/succ_ref/gen reasons), never runs on the empty slot; fallback honored w/ first_turn precedence; dm uses existing REFUSED branch. 26 after_join + 453 rotate-suite tests pass. Dry-run path left inconsistent (stated gap, out of scope).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-cd486d14, SL7.73). The brief said this is a FIX-ONLY build order, IMPLEMENT the fix, not measure the defect (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement). Machine check, not report: _run_after_join_command now calls _after_join_empty_refusal before resolution and resolves with refuse_empty=True (rotate.py:9332-9400); the real after_join reap-proof entry ps ... | grep -E {pred_pids} (rotations.md:69) with an empty pred_pids returns `placeholder {pred_pids} empty: no predecessor chain — skipped by name` with no rc and no output, so the old grep -E empty-pattern full-process-table dump is unreachable. I ran the tests myself: test_after_join_service.py 26 passed; test_rotate_startup.py + test_rotate_templates.py 116 passed, so the neighbour is green. NEAR MISS: passing refuse_empty=True alone would have refused but with the generic first_turn text `placeholder {key} empty at spawn`, LOSING the per-placeholder reason the claim demands; the kid added the pre-check map, which is the difference between satisfying the words and satisfying the mechanism. RESIDUAL, recorded not hidden: the after_join DRY-RUN branch (rotate.py ~9750) still resolves empty placeholders to an empty string and shows dry: True instead of refusing — outside this node scope, and it executes nothing, so the falsifier (an EXECUTED command on the empty slot) does not apply; a later round can route dry-run through the same helper.
<!-- THOUGHT:END -->

PARENT REVIEW SL7.73 (a00-cd486d14): ACCEPTED, no demote. Artifact read and tests re-run by the parent: fix implemented in _run_after_join_command (helper + map, refuse_empty=True, fallback precedence), empty pred_pids/succ_ref/gen refused by name with no rc/output, dm uses the existing REFUSED branch. 26 + 116 tests green on the parent checkout. Residual (dry-run path still resolves empty, executes nothing) recorded in the THOUGHT as a known gap; out of the node scope.
