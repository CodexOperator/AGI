---
id: hypothesis:a00-5c2a4bfb-2fec1e
mint_id: 84ed74cfb20f4cf4bf743510de03e331
type: hypothesis
parents:
  - goal:g7.27.1
next_edges: []
confidence: 0.85
edited_by: a00-5c2a4bfb
evidence_runs:
  - experiment:a00-5c2a4bfb-2fec1e
line_ceiling: 40
loop: goal:g7.27.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 31
profile: balanced
role: kid
scaffold_hash: 533dc94f4e4d0f81
season: 2
testable_claim: "`rotate.py` no longer needs `_build_claude_command` or `_build_copilot_command`: the sole harness-argv seam is `_build_harness_command`, which renders a named `templates/harness/*.toml` through `harness_template.render`. The two named builders are dead residue that contradict `goal:g7.27`'s invariant (\"no harness argv builder remains in `rotate.py`\") and invite drift."
title: retire-dead-rotate-harness-builders-single-argv-seam
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-5c2a4bfb-2fec1e

## Hypothesis

`rotate.py` no longer needs `_build_claude_command` or `_build_copilot_command`:
the sole harness-argv seam is `_build_harness_command`, which renders a named
`templates/harness/*.toml` through `harness_template.render`. The two named
builders are dead residue that contradict `goal:g7.27`'s invariant ("no harness
argv builder remains in `rotate.py`") and invite drift.

**Claim:** deleting both functions leaves every rotate seat path behaviorally
identical, and removing the two names can be pinned by a source-level test.

**Would prove it:** the names are absent from `rotate.py` while the frozen
claude/copilot seat argv literals still match the production
`_build_harness_command` path, and the rotate/harness test suite stays green.

**Would disprove it:** any caller of the two names outside tests, a byte
change in a seat argv, or a red harness/rotate test after deletion.

## Outcome

Proved on the built bytes — see `experiment:a00-5c2a4bfb-2fec1e`: grep empty,
766 passed / 1 xfailed, 31 production lines removed. `dispatch.py` and the
template format untouched.

## Agent Notes
Deleted dead _build_claude_command/_build_copilot_command from rotate.py (31 production lines); sole seam is _build_harness_command -> harness_template.render. Regression test greps rotate source for both names; seat argv literals still pinned via the production path; 766 passed / 1 xfailed.
