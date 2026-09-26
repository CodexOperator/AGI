---
id: hypothesis:brainstorm-manifest-route-refuses-a-missing-goal
mint_id: 085bf7225935470a8cad250f6ceeed8b
type: hypothesis
parents:
  - goal:g1
next_edges:
  - experiment:brainstorm-manifest-goal-guard-fix
edited_by: a00-9619f32e
scaffold_hash: dd80da4b7d8d8ef6
season: 2
testable_claim: workflow.py run_workflow refuses a brainstorm run whose required goal arg is missing or blank on the manifest (pi / pi-free) route, by name, before any stage dispatches -- the same refusal the JS route gives; a committed test drives the manifest runner with a missing and a blank goal and asserts a non-zero exit and zero [dispatch] lines.
thought_session: belam-S2-L5-VI
title: "the brainstorm manifest route refuses a missing or blank goal before any dispatch (assigned: director-engine)"
town: core
---
# hypothesis:brainstorm-manifest-route-refuses-a-missing-goal

Source: PASS 6 chunk 1, round engine-delta-1 -- DEMOTE, both reviewer and verifier: "the required brainstorm goal is guarded only on the native JavaScript route". Runs: .agi/sessions/workflows/runs/mur-p6chunk1of2/{review,verify}_engine-delta-1.json (box-local, local-town).

## Measured
- extensions/agi/bin/workflow.py:2167-2168: `run_workflow` loads the manifest and expands its stages (`_load_manifest` -> `_expand_stages`) with no required-input check, so a pi / pi-free brainstorm run with a missing or blank `goal` proceeds.
- The JS route refuses the same run (agi-brainstorm.js); test_workflow.py:760 `test_brainstorm_manifest_and_js_require_nonempty_goal` checks the manifest description and the JS gate, never the manifest runner.

## CLAIM
workflow.py `run_workflow` refuses a brainstorm run whose required `goal` arg is missing or blank on the manifest (pi / pi-free) route, by name, before any stage dispatches -- the same refusal the JS route gives; a committed test drives the manifest runner with a missing and a blank goal and asserts a non-zero exit and zero [dispatch] lines.

## Dispatch line
config-max: the required args are declared in the workflow's manifest (brainstorm.json), never a literal in workflow.py / template-max: none / code: one required-input check in `run_workflow` ahead of `_expand_stages`, reading the manifest's declaration.

## FALSIFIERS
A manifest-route brainstorm with no goal or goal='' dispatches any stage, or exits 0.

## TESTS
extensions/agi/tests/test_workflow.py (fixture manifests only; no pi process). Residue riding here (DH.307's own claim): the brainstorm JS-versus-manifest RETURN-key comparison test is absent (research-review has one).

## FILE SCOPE
extensions/agi/bin/workflow.py (`run_workflow`) · extensions/agi/workflows/brainstorm.json · extensions/agi/tests/test_workflow.py · this node + its experiment.

## CEILING
one parent, <= 2 kids, pi-free · 10-12 production lines per conjunct · USD cap 1.

## Agent Notes
assigned: director-engine (PASS 6 residue, belam-S2-L5-VI 09-25)
