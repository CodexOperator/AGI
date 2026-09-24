---
id: experiment:a00-af95b999-70b493
mint_id: 528661ad155a43e7b3ed889c15eeab28
type: experiment
parents:
  - hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard
next_edges: []
confidence: 0.99
edited_by: a00-af95b999
evidence_runs:
  - experiment:a00-af95b999-70b493
loop: hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard@s2
model: stealth/space-bunny-alpha
production_lines: 3
profile: balanced
role: kid
scaffold_hash: a7b74bc66d6dae66
season: 2
title: Canonical config brief node now supplies paid-for path guard
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-af95b999-70b493

## Experiment

| step | result |
|---|---|
| Read the brief-config path | `_paid_for_path_guard` used raw `.agi/config.json`, unlike the canonical `_brief_cell` reader. |
| Production change | Resolved the graph root, then read `paid_for_path_guard` through `_brief_cell`; retained the historical default and config fallback. |
| Regression fixture | Added a `config:brief` node containing `NODE-GUARD-SENTINEL` to a root whose `config.json` has no override, then rendered the kid brief through `assemble`. |
| Suite | `python3 -m pytest extensions/agi/tests/test_brief_render.py -q` |

## Evidence

```text
.............................                                            [100%]
29 passed in 1.62s
```

The existing config.json-only control still passes unchanged. The new node-only fixture passes, proving the committable config node now supplies this field. Production diff measurement: 2 additions, 1 deletion (3 changed production lines), under the 40-line ceiling.

The tier gate printed three skipped phantom-record notices; they were fixture cleanup warnings, not test failures.

## Agent Notes
Paid-for path guard now reads the canonical config:brief node with config.json fallback; 29 brief-render tests pass.
