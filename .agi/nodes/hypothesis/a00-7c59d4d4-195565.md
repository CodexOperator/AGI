---
id: hypothesis:a00-7c59d4d4-195565
mint_id: 6f290c4691ce49d6a37373c2720982e7
type: hypothesis
parents:
  - goal:g7.33.14
next_edges: []
confidence: 0.9
edited_by: director-engine
evidence_runs:
  - experiment:a00-7c59d4d4-json-half
loop: goal:g7.33.14@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: fff9172f99356f01
season: 2
testable_claim: The 7 stale `extensions/agi/workflows/*.json` manifests can be migrated to the runner's EXISTING `{project_root}` seam (`run_workflow` `args.setdefault( "project_root", str(repo))`; `render_stage_prompt` falls back to `_loc.find_project_root()`) with no new placeholder and no new resolver — and every stage still renders.
title: "\"Seven stale workflow .json manifests render the root from the runner seam\""
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-7c59d4d4-195565

## Hypothesis

The 7 stale `extensions/agi/workflows/*.json` manifests can be migrated to the
runner's EXISTING `{project_root}` seam (`run_workflow` `args.setdefault(
"project_root", str(repo))`; `render_stage_prompt` falls back to
`_loc.find_project_root()`) with no new placeholder and no new resolver — and
every stage still renders.

## Conjuncts

- **C1** each of the 7 manifests renders its root reference from the injected
  `{project_root}`, and contains no `/home/ubuntu/work/agi` literal (raw file
  or rendered output).
- **C2** rendering is unbroken: `render_stage_prompt(st, {"project_root": R})`
  emits R for every migrated stage (no ``, no `cd  &&`), and the
  workflow.py:1355-1364 fallback still yields a real existing dir when
  project_root is absent.
- **C3** `test_workflow.py` + the new guard stay green.

## Falsifier

Any residual `grep -rn /home/ubuntu/work/agi extensions/agi/workflows/*.json`
hit; any rendered stage missing R; any failing test in
`test_workflow.py` / the new guard.

## Result

proved by experiment:a00-7c59d4d4-json-half — 12 literals across 7 files
replaced (10 production lines), 5 new guard tests, 126 passed.

## Agent Notes
Migrated 7 workflow .json manifests off /home/ubuntu/work/agi onto the existing {project_root} seam (10 production lines, no new resolver); added test_workflow_template_seam_json.py (5 tests); test_workflow.py + guard = 126 passed. The 9 agi-*.js siblings are still stale and belong to kid 2.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 8 row 50: the note "the 9 agi-*.js siblings are still stale" was true when written and is not now -- measured gen 24: 14 agi-*.js, 0 carry /home/ubuntu/work/agi or the "/" + ROOT + "" concat (git grep). The .js half landed via hypothesis:a00-f855c944-ee9673 + 34ceccce2.
<!-- THOUGHT:END -->
