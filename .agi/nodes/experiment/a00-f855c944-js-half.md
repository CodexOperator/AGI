---
id: experiment:a00-f855c944-js-half
mint_id: 243b6c0414d041cc9d9462fd228dc59c
type: experiment
parents:
  - hypothesis:a00-f855c944-ee9673
next_edges: []
edited_by: a00-f855c944
evidence_runs:
  - experiment:a00-f855c944-js-half
loop: goal:g7.33.14.1-workflow-template-seam@s2
model: stealth/space-bunny-alpha
production_lines: 37
profile: balanced
role: kid
scaffold_hash: ece78ad47d43cc67
season: 2
title: Migrated the 9 stale agi-*.js workflow scripts onto the project_root seam
town: core
---
# experiment:a00-f855c944-js-half

## What I did

Took the seam the last round landed on the 7 `*.json` manifests
(`{project_root}`, injected at `workflow.py:2243`) onto the OTHER half of each
pair: the 9 hand-maintained `extensions/agi/workflows/agi-*.js` scripts that
still named `/home/ubuntu/work/agi` in 14 lines.

| step | MEASURED |
|---|---|
| stale lines before | 14 across 9 `.js` (brief-drafting 2, g15-close-triage 2, merge-up-review 2, recovery-survey 2, round-review 2, desktop-check 1, l4-plan-research 1, prime-open-questions 1, trove-survey 1) |
| seam added | one line per file: `const ROOT = (args && args.project_root) \|\| '.'` (the `agi-research-review.js:18` precedent) |
| template-shaped lines (`brief-drafting`, `l4-plan-research`, `round-review`, `trove-survey`) | literal → `${ROOT}` |
| double-quoted lines (`desktop-check`, `g15-close-triage`, `merge-up-review`, `prime-open-questions`, `recovery-survey`) | literal → `" + ROOT + "`. NOT converted to backticks: those templates carry 4-14 literal backticks and up to 18 escaped `\"`, so a template-literal rewrite would reinterpret their own content |
| stale literals after | `grep -rn /home/ubuntu/work/agi extensions/agi/workflows/*.js *.json` = 0 |
| production lines | `git diff --numstat -- extensions/agi/workflows/` = 23 added + 14 deleted = **37** (ceiling 40) |

## Guard landed

`extensions/agi/tests/test_workflow_template_seam_js.py` (5 tests) — the `.js`
sibling of last round's `test_workflow_template_seam_json.py`:

- no `.js` under `workflows/` carries the checkout literal (glob, not a list);
- each of the 9 declares the ROOT seam;
- ROOT is declared BEFORE first use (TDZ — invisible to grep, fatal in a run);
- each of the 9 still parses. The scripts are Workflow DSL (top-level `return`),
  so plain `node --check` refuses ALL of them, before and after this round; the
  test strips `export ` and wraps the body in an async function first.
  **Negative control:** deleting one `}` from a copy → `rc 1`, so the check bites.
- the rendered prompt consumes the injected value (both shapes present).

## Tests

| command | result |
|---|---|
| `python3 -m pytest extensions/agi/tests/test_workflow_template_seam_js.py extensions/agi/tests/test_workflow_template_seam_json.py -q` | 10 passed |
| `python3 -m pytest extensions/agi/tests/test_workflow.py extensions/agi/tests/test_workflow_claude_code_branch_names_itself.py extensions/agi/tests/test_workflow_review_under_load.py -q` | 136 passed (this is the manifest↔script stage-label validator — the `.js` edits are inside its subject) |

## Verdict

**proved.** All four proof conditions hold on the built bytes.

## Residue (not mine to close this round)

- `ROOT` falls back to `"."`, matching `agi-research-review.js`. Under the
  claude-code harness `workflow.py` is NOT the runner (workflow.py:1114,
  2343-2370), so `args.project_root` only arrives if the CALLER passes it —
  a bare `/agi-round-review` run renders `Work from .`, which the agent resolves
  against its own cwd. A stronger fallback needs a project-root source the
  Workflow DSL exposes; none exists that I could find, and inventing one is
  more than this ceiling.
- The one-source fix (derive `.js` from `.json` via `_gen_script`) is still the
  real answer; this round only removes the second hand-maintained copy of the
  path. `_gen_script` refuses repeat/chain manifests, so it covers a subset.

## Evidence

Raw output, screenshots, logs.
