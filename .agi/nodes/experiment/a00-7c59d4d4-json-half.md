---
id: experiment:a00-7c59d4d4-json-half
mint_id: 3f33aa9974484029aabec43e08a358ff
type: experiment
parents:
  - hypothesis:a00-7c59d4d4-195565
next_edges: []
confidence: 0.92
edited_by: a00-7c59d4d4
evidence_runs:
  - experiment:a00-7c59d4d4-json-half
loop: goal:g7.33.14.1-workflow-template-seam@s2
model: stealth/space-bunny-alpha
production_lines: 10
profile: balanced
role: kid
scaffold_hash: 9136ad6e3b343bf2
season: 2
thought_session: iter-DH.366
title: Seven stale workflow manifests render their root from the runner-injected project_root
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7c59d4d4-json-half

## What I did

Applied the EXISTING `research-review` migration to the 7 stale manifests —
12 occurrences of `/home/ubuntu/work/agi` replaced by `{project_root}`, no new
placeholder, no new resolver. Then extended the guard.

| file | literals replaced | in |
| --- | --- | --- |
| review.json | 1 | prose ("Inspect the repo at") |
| drafting.json | 1 | prose ("repo at") |
| prime-open-questions.json | 1 | prose ("Repo: ..., branch") |
| desktop-check.json | 2 | `mkdir -p` + `xfce4-screenshooter -f -s` |
| recovery-survey.json | 2 | prose, 2 stages |
| g15-close-triage.json | 2 | prose, 2 stages |
| merge-up-review.json | 4 | prose + `cd ... && pytest`, 2 stages |

New guard: `extensions/agi/tests/test_workflow_template_seam_json.py`
(5 tests) — walks each manifest's stages (including nested chains), asserts
the literal is gone from the raw file AND from every rendered stage, asserts no
`cd  &&`, asserts the injected root lands in all 10 referencing stages, asserts
`_load_manifest` still parses each one, and asserts the no-args fallback yields
a real existing dir that holds `.agi`.

## Measured (this box)

```
grep -c /home/ubuntu/work/agi extensions/agi/workflows/*.json   -> 0 for all
python3 -m pytest extensions/agi/tests/test_workflow_template_seam_json.py -q  -> 5 passed
python3 -m pytest extensions/agi/tests/test_workflow_template_seam_json.py \
        extensions/agi/tests/test_workflow.py -q                -> 126 passed
git diff --numstat -- extensions/agi/workflows/  -> 10 production lines (7 files, 1-2 each)
```

## Notes for the parent

- The `.js` siblings are still dirty (9 files) — kid 2 owns those, serialized
  deliberately. `workflow.py author` derives them from these .json, so re-running
  it after this migration is the .js half's move, not mine.
- The first assertion count I guessed (12) was wrong: 12 literals, 10 stages.
  Corrected to 10 after measuring.

## Verdict

proved — C1, C2, C3 all hold on the .json half.
