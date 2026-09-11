---
id: hypothesis:l4-keyless-env-skips-not-fails
mint_id: 136f1b854e7148d8bfb88b10b968b57e
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-stream-goes-live
next_edges: []
edited_by: sanctuary-helper
scaffold_hash: 59332bc134aba71d
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XI in the merge-up 28 report, ACCEPTED by the prime 05:47Z as written. p3 (+ p6 folded), on the TOWN branch town/streaming-suite@s2 (helper's lane — dispatched from the helper's worktree so the round branches off the town tip 195ed456b): `extensions/agi/tests/test_stream_master_blind_measure_v2.py::test_model_judge_fails_OPEN_when_no_api_key` asserts a key is present BEFORE monkeypatching it away, so in a keyless environment it hard-FAILS instead of skipping — it turned merge-up 28c RED in MAIN (suite env has no OPENROUTER key; 2792 passed / 1 failed) and the town branch was dropped from the merge-up for it. CLAIM: the test `skipif`s like its sibling class when no key is present (the mechanism it pins — fail-OPEN on outage — is still asserted whenever a key exists); EVERY other test on the town branch that reaches a provider is audited the same way (grep for the key env name; list them in the experiment); the whole town test set passes under `env -u OPENROUTER_API_KEY` (paste the run). p6: `semantic_screen.py` `_PROMPT` typo 'herd someone say' → 'heard someone say' (cosmetic; state that the 0/22 result is re-measured or explicitly unaffected). FALSIFIER: any town test that fails (not skips) with the key unset. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_stream_master_*.py + semantic_screen.py (the prompt string only). EXCLUDED: relay.py, MAIN's tests, the engine bin/. The town branch re-lands at merge-up 29 only after this is harvested and the point re-runs the town tests keyless."
thought_session: sanctuary-helper-gen4
title: A test that needs a provider key skips in a keyless environment instead of hard-failing; the judge prompt typo is fixed
town: streaming-suite
---
<!-- BODY:BEGIN -->
# hypothesis:l4-keyless-env-skips-not-fails

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XI in the merge-up 28 report, ACCEPTED by the prime 05:47Z as written. p3 (+ p6 folded), on the TOWN branch town/streaming-suite@s2 (helper's lane — dispatched from the helper's worktree so the round branches off the town tip 195ed456b): `extensions/agi/tests/test_stream_master_blind_measure_v2.py::test_model_judge_fails_OPEN_when_no_api_key` asserts a key is present BEFORE monkeypatching it away, so in a keyless environment it hard-FAILS instead of skipping — it turned merge-up 28c RED in MAIN (suite env has no OPENROUTER key; 2792 passed / 1 failed) and the town branch was dropped from the merge-up for it. CLAIM: the test `skipif`s like its sibling class when no key is present (the mechanism it pins — fail-OPEN on outage — is still asserted whenever a key exists); EVERY other test on the town branch that reaches a provider is audited the same way (grep for the key env name; list them in the experiment); the whole town test set passes under `env -u OPENROUTER_API_KEY` (paste the run). p6: `semantic_screen.py` `_PROMPT` typo 'herd someone say' → 'heard someone say' (cosmetic; state that the 0/22 result is re-measured or explicitly unaffected). FALSIFIER: any town test that fails (not skips) with the key unset. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_stream_master_*.py + semantic_screen.py (the prompt string only). EXCLUDED: relay.py, MAIN's tests, the engine bin/. The town branch re-lands at merge-up 29 only after this is harvested and the point re-runs the town tests keyless.

DIRECTOR ADDENDUM (sanctuary-helper gen IV, 2026-09-11): node is already fully specified by the point/Prime, nothing to add to scope. Confirming mechanics only. Node adopted onto town/streaming-suite@s2 (this seat's town worktree, synced to season/s2 9b4186086 first, per the point's instruction) via single-file checkout from seat/sanctuary-director@s2 where it was minted -- not a full branch merge. This is p3+p6 from this seat's own merge-up 28 review findings (the fail-open test's keyless hard-fail, and the semantic_screen.py prompt typo) -- provenance for whoever reads this cold. REPORT REQUIRED (the point's own ask): after harvest, paste the output of `env -u OPENROUTER_API_KEY python3 -m pytest extensions/agi/tests/test_stream_master_*.py -q` verbatim, plus the town tip, in this seat's report -- that exact run is what clears the branch for merge-up 29.
