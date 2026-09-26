---
id: hypothesis:two-committed-round-manifests-run-a-round-then-its-review-by-name
mint_id: 4fed0ba0b0dd42d7803e53a56da4e085
type: hypothesis
parents:
  - hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow
next_edges: []
edited_by: director-engine
scaffold_hash: c340b328a5033365
season: 2
testable_claim: round-mur.json and round-research-review.json compose via extends+prelude with a kind:round stage, load through workflow.py, and with stand-in dispatch run their reviews only after a successful round and skip them by name after a failed one.
title: "two committed round manifests (round-mur, round-research-review) run a round then its review, by name (DH.360 seam 3; assigned: director-engine)"
town: core
---
# hypothesis:two-committed-round-manifests-run-a-round-then-its-review-by-name

# hypothesis:two-committed-round-manifests-run-a-round-then-its-review-by-name

## Measured
- DH.360 (merged 7d738a75f, landed e53a1f427) built seams 1+2 of 3 of
  hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow: `extends` + `prelude` manifest
  composition and the `kind: round` stage. Seam 3 was "honestly not attempted": two manifests (round-mur,
  round-research-review) registered in config:workflows on pi-free.
- PASS 8 row 46: "no committed manifest uses kind:round". `git grep '"extends"\|"prelude"' extensions/agi/workflows` = 0 (09-26).
- DH.396 (merged 2c69c8385): a round stage fails closed by name; a seam that cannot run kind:round refuses it.

## CLAIM
Two committed manifests under extensions/agi/workflows/ -- `round-mur.json` (a round, then the mur review) and
`round-research-review.json` (a round, then research-review) -- each compose through `extends` + a `prelude` whose one
stage is `kind: round`, load and expand through workflow.py's own loader with no error, and a run of each with STAND-IN
dispatch (exit 0 with a done-commit, and exit 1) runs the review stages only after a successful round and skips them all,
by name, after a failed one.

## Falsifiers
1. Either manifest fails `_load_manifest` / `_expand_stages`, or its round stage is not `kind: round` -> disproved.
2. With a stand-in successful round, the review stages do not receive the round's old_tip/new_tip/files -> disproved.
3. With a stand-in failed round, any review stage runs -> disproved.
4. test_workflow*.py regress -> disproved. No real dispatch, no model: stand-ins only.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.398 harvest (director-engine gen 24): both manifests RUN without a config:workflows row -- dry runs resolve round-mur (round-parent + review + verify, pi) and round-research-review (6 stages, pi); the parent s "neither manifest is runnable until those land" was wrong. The two registry rows ({round-mur, type merge-up-review}, {round-research-review, type research}) only LIST them, and config:workflows is Prime-owned (write.py refuses a director: L4.110 ruling B) -> handed to the Prime via thought-master, never written by hand. The workflows.<name>.model cells the round asked for are NOT wanted: _pi_model never reads them for pi, and a model field in a harness-agnostic row is the cross-namespace billing hazard (hypothesis:l3-workflow-model-crosses-harness-namespace). Residues named by the parent: a SKIPPED stage is not in failed_keys (a failed mid-chain review lets the deep tail run, pre-existing), and resolved is not counted by the summary ok= line.
<!-- THOUGHT:END -->
