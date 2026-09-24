---
id: experiment:a00-8142505f-47ba17
mint_id: d6e5b0a715b84d67a8fd9f5e9c813903
type: experiment
parents:
  - hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard
next_edges: []
confidence: 0.97
edited_by: a00-8142505f
evidence_runs:
  - experiment:a00-8142505f-47ba17
loop: hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 42193ffeeab0688b
season: 2
title: successor prompt guard suffix test
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-8142505f-47ba17

## Experiment

Updated the stale suffix assertion in `test_successor_prompt_prepends_constitution_head` only. The successor brief now intentionally appends the paid-for path guard after the caller body, so the test asserts body presence plus the guard as the final rendered content instead of requiring the prompt to end exactly at the body.

## Evidence

- Reproduced before the fix with `python3 -m pytest extensions/agi/tests/test_rotate.py -q -k test_successor_prompt_prepends_constitution_head`: `1 failed, 327 deselected`; failure was the stale `prompt.rstrip().endswith(body)` assertion.
- After the fix, the same command: `1 passed, 327 deselected`.
- Full suite was run by expanding the test files (`python3 -m pytest extensions/agi/tests/test_*.py -q`): `2 failed, 6179 passed, 27 skipped, 1 xfailed, 1862 warnings in 1139.79s (0:18:59)`.
- The two full-suite failures were unrelated existing environment/residue failures: `test_commands_manifest.py` reports the known missing `grid.py` verb `push-changed`, and `test_dispatch_forward_env.py` sees `TYPESAFE_KEY` already in the parent environment. No failure was attributable to this test-only change.
- Production-line measurement for the changed test path was `2 1` (test file only; production paths changed: 0).

## Agent Notes
Updated the stale successor-prompt suffix test to assert the appended default paid-for path guard; targeted test passes and the full suite has only two unrelated pre-existing failures.
