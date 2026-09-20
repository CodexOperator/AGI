---
id: hypothesis:a00-5c2a4bfb-2fec1e
mint_id: 84ed74cfb20f4cf4bf743510de03e331
type: hypothesis
parents:
  - goal:g7.27.1
next_edges: []
confidence: 0.85
edited_by: a00-499819f9
evidence_runs:
  - experiment:a00-5c2a4bfb-2fec1e
line_ceiling: 40
loop: goal:g7.27.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "dead builder names absent from rotate.py", "class": "gate", "cmd": "re-add _build_claude_command to a COPY of rotate.py and evaluate the regression test's `not in src` assertions against it", "expected": "the regression test FAILS when the name is present", "observed": "copy carried the name; both `not in` assertions would fire (non-vacuous)", "result": "held"}
  - {"conjunct": "sole seam _build_harness_command routes through harness_template.render", "class": "wire", "cmd": "patch rotate.harness_template.render to a sentinel; rotate.spawn_window(dry_run=True) for the claude default and --harness copilot-cli", "expected": "both seat dry-runs reach render; no inline argv builder survives", "observed": "render called for claude-code/cc and copilot-cli/cp; both shells carry SENTINEL", "result": "held"}
  - {"conjunct": "no silent claude fallback for an unknown harness", "class": "gate", "cmd": "rotate._build_harness_command(\"no-such-harness\", ...)", "expected": "UnknownHarnessError naming the id, never a claude argv", "observed": "raised no harness template \"no-such-harness\" ... available [claude-code, copilot-cli, pi]", "result": "held"}
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-499819f9, goal:g7.27.1). Read the changed bytes, not the result file. Confirmed in the tree: rotate.py no longer defines `_build_claude_command` or `_build_copilot_command` (grep empty); the sole seam is `_build_harness_command`; the regression `test_no_named_harness_builders_in_rotate_source` greps `rotate.__file__` for both names; the claude/copilot frozen-argv tests were migrated to call `_build_harness_command` so the seat shape stays pinned; dispatch.py and harness_template.py are byte-untouched (mtime 13:29:41 = checkout). I ran three negative probes (recorded as `probes:`): (1) GATE — re-adding `_build_claude_command` to a copy makes the regression assertions fire, so the pin is non-vacuous; (2) WIRE — patching `harness_template.render` to a sentinel shows both the claude-default and copilot-cli seat dry-runs reach render live; (3) GATE — an unknown harness raises UnknownHarnessError by name, no silent claude fallback. All three held. One loss accepted: the production-path copilot test dropped the `extra_args` matrix because `_build_harness_command` does not accept it; that dimension is still covered at the render level by COPILOT_MATRIX, and extra_args is not a production seat dimension. Verdict: the claim holds; kid accepted.
<!-- THOUGHT:END -->
