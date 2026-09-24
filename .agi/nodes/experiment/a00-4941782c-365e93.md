---
id: experiment:a00-4941782c-365e93
mint_id: a1f98b3647404cbbb0a7ed400dc0d2bb
type: experiment
parents:
  - hypothesis:g5.32-t0-hardcoded-prose-inventory-and-template-loader
next_edges: []
confidence: 0.99
edited_by: a00-4941782c
evidence_runs:
  - experiment:a00-4941782c-365e93
loop: hypothesis:g5.32-t0-hardcoded-prose-inventory-and-template-loader@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 06c2249c8c73692e
season: 2
title: Explicitly register prose_templates.py as a no-help library module
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4941782c-365e93

## Experiment

Measured the inherited help-smoke defect, then added the explicit `prose_templates.py` exception to the test's `NO_HELP` registry. The loader remains a library module with no CLI; no production file was changed.

## Evidence

- Before: `python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q` → **1 failed, 71 passed, 5 skipped**. The sole failure was `test_help_smoke[prose_templates.py]`, which exited 0 but emitted empty stdout.
- After: same command → **71 passed, 6 skipped**.
- Regression: `python3 -m pytest extensions/agi/tests/test_prose_templates.py extensions/agi/tests/test_rotation_alert.py -q` → **59 passed**.

The first regression attempt was run concurrently with the help-smoke test and was refused by the suite lock; rerunning sequentially produced the clean 59-pass result.

## Agent Notes
Registered prose_templates.py as a deliberate no-help library module; help smoke improved from 1 failure to 0, and the 59-test regression set passed.
