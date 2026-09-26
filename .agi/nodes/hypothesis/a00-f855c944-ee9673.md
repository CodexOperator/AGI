---
id: hypothesis:a00-f855c944-ee9673
mint_id: 7d2ca26ec006446d86870f4a9c959771
type: hypothesis
parents:
  - goal:g7.33.14
next_edges: []
confidence: 0.85
edited_by: director-engine
evidence_runs:
  - experiment:a00-f855c944-js-half
loop: goal:g7.33.14@s2
model: stealth/space-bunny-alpha
production_lines: 37
profile: balanced
role: kid
scaffold_hash: c6363d607a0cc982
season: 2
testable_claim: The `.js` half of each workflow pair takes the SAME `{project_root}` seam the `.json` half was migrated to last round — a zero-literal guard can then cover BOTH halves of every registered pair, and a run started in a git worktree stops pointing its readers at the main checkout.
title: The .js half of a workflow pair takes the same project_root seam as its .json half
town: core
verdict: proved
---
# hypothesis:a00-f855c944-ee9673

## Claim

The `.js` half of each workflow pair takes the SAME `{project_root}` seam the
`.json` half was migrated to last round — a zero-literal guard can then cover
BOTH halves of every registered pair, and a run started in a git worktree stops
pointing its readers at the main checkout.

| half | who renders the prompt | seam available | stale literal before this node |
|---|---|---|---|
| `<name>.json` | `workflow.py render_stage_prompt` | `args["project_root"]`, injected by `run_workflow` (workflow.py:2243) + cwd fallback (1355-1364) | 0 (last round) |
| `agi-<name>.js` | Claude Code itself, the script IS the runner | `args.project_root` only — the caller must pass it | 14 lines / 9 files |

## Why the .js half is separable, not a rewrite

The scripts are hand-maintained, not derived: `agi-l4-plan-research.js` and
`agi-trove-survey.js` had CLEAN `.json` halves BEFORE the last round and still
stale `.js` halves. Regenerating them from the manifests (`workflow.py _gen_script`)
would be the one-source fix, but it refuses anything with repeat/chains and would
cost far more than this round's ceiling. So the claim here is only the SEAM.

Precedent already on the `.js` side: `agi-research-review.js:18`
`const ROOT = (args && args.project_root) || "."`. This node spreads that one
line to the 9 remaining scripts.

## What would prove it

1. `grep -rn /home/ubuntu/work/agi extensions/agi/workflows/` = 0 (both halves).
2. Every one of the 9 declares the ROOT seam, before first use (TDZ).
3. Every one of the 9 still parses (`node --check` on the export-stripped,
   async-wrapped body) — a botched string split shows up here, not in a run.
4. `test_workflow.py` (the manifest↔script stage-label validator) stays green.

## What would disprove it

A script that still names the checkout; a ROOT used above its `const`; a parse
break; or a rendered prompt that drops the injected value (i.e. the seam exists
but nothing consumes it).

Experiment: `experiment:a00-f855c944-js-half`.

## Agent Notes
Migrated the 9 stale agi-*.js workflow scripts (14 literal lines) onto the args.project_root seam; 0 literals left in workflows/, 37 production lines, new test_workflow_template_seam_js.py (5 tests) + 136 workflow tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 8 row 50: hypothesis:a00-a5f94936-a89712 (DH.366) is the round that found this node s render wrong -- 11 occurrences of the "/" + ROOT + "" concat on 8 lines across 5 .js survived this migration; fixed by director commit 34ceccce2 with a render test. verdict proved stands for the literal migration it claimed; the concat form was outside its test.
<!-- THOUGHT:END -->
