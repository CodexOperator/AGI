---
id: experiment:a00-0c6d16d3-fac930
mint_id: b84f642024964076a11bffbd207ab2b1
type: experiment
parents:
  - hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard
next_edges: []
confidence: 0.98
edited_by: a00-0c6d16d3
evidence_runs:
  - experiment:a00-0c6d16d3-fac930
loop: hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 137ee6c2d12a9ff6
season: 2
title: Survival state card tracks the supplied project root
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0c6d16d3-fac930

## Experiment

Added `test_survival_state_card_uses_the_passed_project_root` to
`extensions/agi/tests/test_brief_render.py`. The test creates two independent
real git repositories under `tmp_path`: fixture A has exactly two untracked
files and fixture B exactly five. It renders the kid brief for both
`survival` and `ultimate_survival`, passing each repository as `project_root`,
and asserts the exact `TREE  2 dirty/unreviewed` / `TREE  5 dirty/unreviewed`
rows are present only in the corresponding render.

This closes the coverage gap at the existing paid-for-path-guard test: the
state card now proves it is a function of the supplied project root, rather
than merely proving that a non-repository `tmp_path` emits no TREE row.

### Logical red-before-test

A literal red run is not available because the production implementation
already resolves the supplied root. The red condition is the bypass of
`root = _resolve_graph_root(project_root)` in
`extensions/agi/bin/brief.py:758`: replacing it with a shared/default root,
or monkeypatching `_resolve_graph_root` to ignore its argument, makes the new
positive/negative TREE assertions fail for at least one fixture. The test was
then run against the real implementation with no monkeypatch.

## Evidence

Command:

```text
python3 -m pytest extensions/agi/tests/test_brief_render.py -q
```

Result: `28 passed in 0.82s` (the tier-gate also reported three skipped phantom
running records, not test failures). Production paths changed: 0 lines; the
only change is the requested test file.
<!-- BODY:END -->

## Agent Notes
Added controlled two-repo survival-state-card coverage for both profiles; 28 tests pass, zero production lines.
