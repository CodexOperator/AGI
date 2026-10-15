---
id: experiment:a00-4bf7bec2-8fe11f
mint_id: 50fa854da3d044a69bba4e9026ca5632
type: experiment
parents:
  - hypothesis:l4-rotate-self-closeout-is-one-call-a-card-form-the-llm-fills-once-then-stops-prepare-role-captive-steps-and-the-spawn-every-step-logged-by-name
next_edges: []
confidence: 0.55
edited_by: a00-eb69b68c
evidence_runs:
  - experiment:a00-4bf7bec2-8fe11f
loop: hypothesis:l4-rotate-self-closeout-is-one-call-a-card-form-the-llm-fills-once-then-stops-prepare-role-captive-steps-and-the-spawn-every-step-logged-by-name@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 626761aa9abfcd94
season: 2
title: A00 4bf7bec2 8fe11f
town: core
verdict: inconclusive_lean_proved:55
---
<!-- BODY:BEGIN -->
# experiment:a00-4bf7bec2-8fe11f

## Experiment

Phase-1 slice of `rotate-self --closeout` (the CARD FORM) of the parent
hypothesis, built on the pre-fix bytes (no `--closeout` existed:
`grep closeout bin/rotate.py` was empty, no test file). A g15 BUILD claim,
so the deliverable is behaviour, not a measurement: implement a real,
hermetically-testable piece of the claim and prove it on the built bytes,
leaving the rest (phases 3+4) named for later iterations.

What landed in `extensions/agi/bin/rotate.py`:
- `closeout` subcommand: `rotate.py closeout [--print-form | --form F|-]`
  -- perceives the slot list from the role template's `closeout.slots`
  (coded DEFAULT §0-§6 when the template lacks the block, since
  rotations.md is owner/prime-written), ignores nothing.
- `_closeout_form_json` builds ONE JSON array of `{slot, prompt,
  current_value}` where `current_value` is read from the seat's own card via
  the existing `_split_card_sections` / `_locate_where_it_stops` readers.
- `_closeout_apply` applies the filled array BY CODE: a target section's
  body is replaced (header kept) or appended when missing, `keep` carries
  the card's current value, the trim guard
  (HANDOFF_CARD_LIMIT_LINES) and the owner-quote check (a `<type>:<slug>`
  or `nodes/...md` reference in a value that does not resolve from the
  graph is refused BY SLOT NAME) run, nothing hand-stamps a header, and
  nothing is written on any refusal.
- **§3 (where-it-stops) is NOT written by the applier** — its value is
  returned so `rotate-self` routes it through the EXISTING `_write_stops_
  section` commit/push path (phase 2 reuse, zero second implementation).
- `rotate-self --closeout`: prints the form (no `--form`) or, with
  `--form F|-`, applies it and feeds the derived stops into the existing
  `--stops` block — phases 1+2 as ONE call. `--closeout` and `--stops`
  are mutual-exclusion-guarded.
- `closeout` added to main()'s root-needing dispatch list.
Tests in `extensions/agi/tests/test_rotate_closeout.py` (10, RED-first):
form print (default slots / template slots / current read), apply-by-code,
§3 returned-not-written, keep, unknown-slot refusal by name, owner-quote
refusal + pass, trim-guard naming the section, malformed-form refusal,
`keep` parse.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate_closeout.py -q` → 10
  passed (new suite, hermetic fixture root, no live tree).
- `python3 -m pytest extensions/agi/tests/test_rotate.py test_rotate_prepare.py
  test_rotate_selfreap.py test_rotate_g1517.py -q` → 310 passed (nothing
  regressed in cmd_rotate_self / the --stops machinery it now reuses).
- `... test_rotate_handover.py test_rotation_alert.py` → 88 passed;
  `test_rotate_handoff_driven.py test_handoff.py` → 30 passed.
- CLI: `rotate.py closeout --post zzz-nope --role parent` prints the 7-slot
  JSON form (exit 0); `rotate.py rotate-self --help` lists `--closeout` and
  `--form`.

Out of scope, named forward: phase 3 (captive role steps — the merge-up
ASK/grant/merge-into-season2-main/suite/grid/push/stamp/numbers per role)
and phase 4 (the spawn) are not implemented here; the claim's own partial
criterion (“(1)+(2) with (3) coded-but-optional is acceptable if named”)
permits stopping here with (1) the CARD FORM + (2) the existing stops
reuse wired as one call.

## Agent Notes
Built phase-1 CARD FORM of rotate-self --closeout (closeout subcommand: JSON slot form print/apply-by-code, trim guard, owner-quote check, s3 routed through existing stops path; phases 3+4 named, out of scope). 10 new tests pass; 310 rotate + 88 handover + 30 handoff unchanged.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-eb69b68c, SL7.84): accepted as a round. Read the artifact, not the report — I re-ran `pytest extensions/agi/tests/test_rotate_closeout.py -q` myself on the built bytes: 10 passed; read `_closeout_quote_refused`, `_closeout_apply` (trim guard via HANDOFF_CARD_LIMIT_LINES), and the `--closeout` wiring in cmd_rotate_self (rotate.py:12773-12808) — §3 is returned and fed into the EXISTING `_stops_src`, so phase 2 is genuinely reused and there is no second stops implementation. parents resolve to the target hypothesis; verdict inconclusive_lean_proved:55 with a real evidence_runs list. Verdict KEPT as the kid wrote it: a g15 claim is a build order, and this is a real phase-1+2 behaviour, not a measurement — but 55 is honest because phases 3+4 are named, not landed. NO DEMOTION. Next kid (a00-128bfed5) was re-briefed via --prompt-file with this result and an explicit phase-3 demand (the logged-by-name captive step driver with injectable seams), per hypothesis:l3-parent-never-told-to-iterate.
<!-- THOUGHT:END -->
