---
id: experiment:rotate-has-zero-new-harness-argv-builders
mint_id: c91bed200f264ceb934e677244c756be
type: experiment
parents:
  - hypothesis:a00-bc652841-541f5f
next_edges: []
edited_by: a00-bc652841
evidence_runs: experiment:rotate-has-zero-new-harness-argv-builders
line_ceiling: 40
loop: goal:g7.31.2.3@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 4586b3e03b37f3b5
season: 2
title: Built the general rotate.py argv-builder gate; live source reports zero offenders
town: core
---
<!-- BODY:BEGIN -->
# experiment:rotate-has-zero-new-harness-argv-builders

## Experiment

Built the general regression gate in
`extensions/agi/tests/test_harness_template.py`, replacing the retired
narrow two-name test (`test_no_named_harness_builders_in_rotate_source`).
The gate is three pure detectors over `rotate.py`'s source, parsed with
`ast` (definitions, not text):

- `_argv_builder_offenders` — argv-shaped def names outside a frozen,
  reviewed allowlist;
- `_harness_branch_offenders` — `harness == "<id>"` literals outside the
  shipped set;
- `_render_call_owners` — functions calling `harness_template.render`
  other than the sole seam `_build_harness_command`.

`test_rotate_stays_orchestration_only` asserts all three are empty on the
live file and prints the offenders by name. Four more tests prove the gate
is NON-VACUOUS: it flags synthetic `_build_grok_command`,
`_build_grok_argv`, `_grok_command`, `if harness == "grok":`, and a second
render seam; and it does NOT flag the allowlisted non-harness helpers or a
docstring mention.

Production `rotate.py` needed **zero** edits — the invariant already held;
the gap was the gate, not the code.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_harness_template.py -q
..............................................                           [100%]
46 passed in 6.56s

$ python3 -m pytest extensions/agi/tests/test_rotate_copilot_harness.py -q
................                                                         [100%]
16 passed in 2.99s

$ git diff --numstat -- extensions/agi/bin extensions/agi/templates
(empty)
```

Live-file detectors (measured):

```
defs ending in argv-ish suffix: _build_harness_command,
  _successor_command, _assembled_successor_command, _launch_wrapper_argv,
  _wm_tool_argv, _ack_call_args, _run_after_join_command,
  _fork_resume_command     -> all in the allowlist; offenders = []
harness == literals: ['claude-code']  -> offenders = []
harness_template.render call sites: 1 (line 1014, inside the seam)
```

## Verdict rationale

All three detectors report zero on the live source and each fails on its
synthetic offender. `proved`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. -->
This round is a g15-style BUILD, not a measurement: the narrow test existed,
the claim asked for a general one, and the gate is the built artifact proven
on synthetic offenders and on the live file. No production edit was needed
(0 lines, well under the 40-line ceiling).
<!-- THOUGHT:END -->
