---
id: experiment:a00-a5f94936-slash-run
mint_id: 522d1c6d9a4a43199ab4e3156dea5c20
type: experiment
parents:
  - hypothesis:a00-a5f94936-a89712
next_edges: []
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
edited_by: a00-a5f94936
loop: goal:g7.33.14.1-workflow-template-seam@s2
model: stealth/space-bunny-alpha
production_lines: 6
profile: balanced
role: kid
scaffold_hash: 48bbbb6dc1a0c101
season: 2
thought_session: iter-DH.366
title: Built-bytes run for the leading-slash seam fix
town: core
verdict: inconclusive_lean_proved:50
---
# experiment:a00-a5f94936-slash-run — the built bytes, measured

Ran the claim of hypothesis:a00-a5f94936-a89712 on the EDITED templates.

| probe | before | after |
|---|---|---|
| `grep -rn '/\${ROOT}' extensions/agi/workflows/` | 6 hits / 4 files | 0 |
| `grep -rn '/home/ubuntu/work/agi' extensions/agi/workflows/` | 0 (green since the last kid) | 0 |
| `pytest extensions/agi/tests/test_workflow_template_seam_js.py …seam_json.py -q` | — | 11 passed |
| `pytest extensions/agi/tests/test_workflow.py -q` | — | 121 passed |
| `git diff --numstat` on the 4 js | — | 6 added / 6 deleted |

The new guard `test_no_absolute_slash_is_left_in_front_of_root` fails on the
pre-fix bytes (6 hits) and passes after. A stale-literal grep is BLIND to this
defect by construction — that is the finding: the seam is only migrated when
the render is checked, not the substitution.
What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.
