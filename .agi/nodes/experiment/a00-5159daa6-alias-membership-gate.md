---
id: experiment:a00-5159daa6-alias-membership-gate
mint_id: 2d7c6a1e9f4b48d0b3e2a1c6f8d9e0b
type: experiment
parents:
  - hypothesis:a00-5159daa6-d01afb
line_ceiling: 40
production_lines: 0
season: 2
title: Alias tracking closes the rotate.py membership-gate blind spot
role: kid
---
# experiment:a00-5159daa6-alias-membership-gate

## Experiment

Inspected the existing general AST gate in `extensions/agi/tests/test_harness_template.py` and found one remaining source-shape blind spot: a harness read copied to a local name before a membership test was not recognized. Added conservative alias tracking for assignments whose right-hand side visibly reads `harness`, plus a synthetic non-vacuity regression test for `h = getattr(args, "harness", None); h in ("grok", "x")`.

No `rotate.py` production edit was needed; the live source remains orchestration-only.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_harness_template.py -q`
- Result: **53 passed**.
- The new synthetic case reports `["grok"]`; the live-source assertion remains green.
- Production diff: 0 lines; test-only change.

## Result

The alias-shaped branch is now caught by name while the existing allowlist and shipped-harness false-positive protections remain intact. The detector is still intentionally conservative for novel harness ids hidden in membership containers; this experiment does not claim full dataflow inference.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. -->
The prior gate covered direct harness reads but not a simple local alias. Tracking only visibly harness-derived assignments closes that narrow bypass without broad string heuristics that would turn every alias or container into a false positive.
<!-- THOUGHT:END -->
