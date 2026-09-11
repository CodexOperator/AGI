---
id: experiment:a00-654caab2-542247
mint_id: d292b171bb6a4844acead95610f9e820
type: experiment
parents:
  - hypothesis:l4-the-nudge-carries-the-dm-body-inline
next_edges: []
confidence: 0.9
evidence_runs:
  - experiment:a00-654caab2-542247
loop: hypothesis:l4-the-nudge-carries-the-dm-body-inline@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0593a693aae6a764
season: 2
title: A00 654caab2 542247
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-654caab2-542247

## Experiment

L4.140 — fix-only pass on `extensions/agi/bin/send.py` + tests, two residues the L4.139 verdict (experiment:a00-7efd6aa8-20ef7d, proved) left behind. Root hypothesis:l4-the-nudge-carries-the-dm-body-inline.

**RESIDUE A (concatenation regression).** `_nudge_coalesce_reason` flagged a "token already unsubmitted" only when `_nudge_token_head(text)` — the head of the exact line about to be typed — was in the input region. The inline line head now carries the sender (`[nudge: <from>]:`), so a retry whose text was a DIFFERENT nudge shape no longer matched a stranded line and send.py TYPED INTO A NON-EMPTY box; the separate Enter then submitted BOTH lines as ONE user turn (the owner's original 2026-09-11 bug class). Fixed by adding `_stranded_in_region(region)` which detects ANY stranded nudge-shaped line — inline `[nudge:`, the `[agi-nudge]` wake token, AND rotate.py's `[rotation-alert]` — and having `_nudge_coalesce_reason` return "token already unsubmitted" for any of them, never appending a second line.

**RESIDUE B (deferred dropped without delivery).** The probe-(C) branch ran `_clear_deferred(root, to)` unconditionally. When `delivering_deferred` was True, the line just submitted was the STRANDED one, not the deferred body, so the deferred body was discarded having never reached the pane (violating the F1 rule that a marker records only a DELIVERY). Fixed: the probe-(C) Enter now submits whatever line is stranded; the deferred/pending is cleared only when `_nudge_token_head(text)` is in the region (the stranded line WAS ours); when a DIFFERENT line was submitted, `body is not None` stores the deferred body (or bumps pending) for a later idle retry, and an existing deferred body that is a different line stays stored.

## Evidence

`_FixturePane` proves the falsification — OLD bytes (temporarily restored) produced the exact concatenation, e.g. `['[rotation-alert] rotating[nudge: mee]: urgent']` as ONE submitted string; NEW bytes submit `['[rotation-alert] rotating']` alone and defer the dm body.

New tests (5) in `test_send.py`, each FAILS on the pre-fix bytes, passes on mine:
- `test_stranded_inline_line_no_concat_on_inbox_retry` — stranded inline line, inbox `send()` retry → stranded line alone, nothing typed after, no concat.
- `test_stranded_wake_token_dm_no_concat` — stranded `[agi-nudge]` token, then a dm → token alone, dm body deferred.
- `test_rotation_alert_line_dm_no_concat` — stale `[rotation-alert]` (typed by rotate.py), then a dm → alert alone, no concat, dm body deferred.
- `test_deferred_kept_when_different_line_submitted` — Residue B: deferred body SURVIVES when a different stranded line is submitted.
- `test_deferred_cleared_when_its_own_line_stranded` — Residue B control: deferred cleared only when its own line reaches the pane.

Runs:
- `python3 -m pytest extensions/agi/tests/test_send.py -q` → **112 passed** (107 prior + 5 new) in 0.8s.
- `python3 -m pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_rotation_alert.py -q` → **122 passed** in 1.3s.
- OLD-bytes falsifier check (temporary revert, then restored): 4 falsifier tests FAIL, control passes.
- A bare `pytest extensions/agi/tests/` is refused by the engine's `AGI_TIER=kid` full-suite guard; ran the two affected suites instead.

## Agent Notes
Fixed two send.py residues: (A) _nudge_coalesce_reason now flags ANY stranded nudge line (inline/wake/rotation-alert) via _stranded_in_region so a retry never types a second line into a non-empty box (concatenation = one user turn); (B) probe-C clears deferred/pending only when the submitted line IS ours, else stores/keeps it for a later retry. New 5 falsifier tests fail on old bytes, pass on new; test_send 112 passed, +rotation_alert 122 passed.
