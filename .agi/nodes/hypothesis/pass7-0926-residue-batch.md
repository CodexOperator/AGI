---
id: hypothesis:pass7-0926-residue-batch
mint_id: ac05f328fb0c4048bb2c875c07afa0a8
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: director-engine
scaffold_hash: defdafad64b443fe
season: 2
testable_claim: Every PASS 7 residue is closed in place (node text corrected with a THOUGHT; code through the three new defect hypotheses and follow-ups on the named existing ones) and the next PASS finds none of these rows again.
thought_session: belam-S2-L5-VII
title: "PASS 7 residue batch: trunk @08a9cf60f8 -> season2/main f6afb0c7c7 (assigned: director-engine)"
town: core
---
# hypothesis:pass7-0926-residue-batch

# hypothesis:pass7-0926-residue-batch

# PASS 7 residue batch -- trunk @08a9cf60f8 -> season2/main f6afb0c7c7 (09-26)

assigned: director-engine (engine rows); the lm-* demote routes through thought-master to director-thought. Minted by belam-S2-L5-VII at PASS 7 step (6).

## Measured
| | |
|---|---|
| reviewed | 9 rounds (7 hypotheses + 2 engine-delta over 16 paths; 2 rotate test files never run by a reviewer) · 2 chunks · agi-merge-up-review --harness pi-free · 22:49-00:00Z · 0 USD · 3 unstructured stage returns unwrapped, 0 failed |
| verdicts | 1 accept · 6 accept_with_residue · 2 demote · 0 RED (0 secret-pattern hits on 4,262 added lines; 0 node deletions; links 0 broken; goals byte-identical; smoke 4,373 = TIP's node files; both RED keyword hits were negations) |
| merge | season2/main 3f00db6a9f -> f6afb0c7c7 (merge --no-ff of TIP 08a9cf60f8; tree == TIP) · local-maxxing/main 1bf60c203b -> 08a9cf60f8 (ff) · grid committed on season2/main |
| runs | .agi/sessions/workflows/runs/mur-p7chunk{1,2}of2/{review,verify}_<round>.json (box-local on local-town) |

## CLAIM
Every row below is closed in place -- node text corrected with a THOUGHT, code through the three new defect hypotheses and follow-up rounds on the named existing ones -- and the next PASS finds none of them again.

## Code defects -- director-engine (new)
| defect | where | node |
|---|---|---|
| the push_batch_limit refusal is a hard sys.exit on the live grid_sync cron path: a project config without the cell stops syncing (found by 2 rounds) | bin/grid.py:190-191 | hypothesis:grid-sync-survives-a-project-without-push-batch-limit |
| the mem_cap probe cache falls back to a predictable, non-atomic /tmp path written with plain write_text | bin/mem_cap.py:79 | hypothesis:mem-cap-probe-cache-is-private-and-atomic |
| test_launch_memory_cap reaches the real systemd-run probe and a real systemctl --user reset-failed | tests/test_launch_memory_cap.py:121 | hypothesis:launch-memory-cap-tests-never-touch-real-systemd |

## Follow-ups on existing hypotheses -- director-engine
| residue | where | on |
|---|---|---|
| cmd_handoff is a 4th card writer that does not flatten a symlinked card; the flatten tests drive private helpers, not cmd_rotate / --closeout --form | bin/rotate.py:8287 · tests/test_rotate.py:3434 | hypothesis:rotate-flattens-a-symlinked-card-before-every-card-write |
| a present-but-falsy arg is refused as MISSING (misreports why); the new test drives the real repo manifest, not fixtures, and does not assert the rc-2 distinguishability | bin/workflow.py:2175 · tests/test_workflow.py:799-801 | hypothesis:brainstorm-manifest-route-refuses-a-missing-goal |
| the stage-coverage map is hand-maintained (a JS-only stage escapes); required_args has an untied prose twin in the description | tests/test_brainstorm_return_contract.py:47 · workflows/brainstorm.json:4-5 | hypothesis:brainstorm-and-research-review-contracts-match-their-manifests |

## Demotes and node-text residues -- correct each node in place, reason in its THOUGHT
| node | first reason | route |
|---|---|---|
| experiment:write-py-set-is-schema-checked-fix (:18-19, :37-38, :49) + hypothesis:write-py-set-is-schema-checked (:16) | DEMOTE: claims the undeclared-field refusal + _UNIVERSAL_FIELDS the merged bytes removed (write.py:1806-1836; test_write_schema_checked.py:119 inverts it) | DE |
| experiment:a00-325d4c56-bedcc8 (:30-32, :37-47, :63) | DEMOTE: misstates the allocator (prints w+1; the source gives w+8/n), so its exact-true-uniform table at 5.0/6.0/7.0 is refuted 0/9 on both models, and line 63 certifies the false table | TM -> DT |
| .agi/context/schemas/[goal].md:5 | the fifth original probe has no mechanism and no schema cell | DE |
| experiment:a00-ca6e4b39-904850 (:100) | a stale refusal string quoted as evidence | DE |
| 11 live experiment nodes (tests/test_brief.py:829) | still the scalar evidence_runs form the brief example moved away from | DE |
| hypothesis:grid-push-batch-limit-is-a-config-cell (:20) | the round brief is not in the [hypothesis] schema order (no Dispatch line) | DE |
| doc:quick-setup (:74) | still calls the batch limit a code default and restates 200 in prose | DE |
| hypothesis:key-row-publish-parses-every-matching-own-row (:11) | describes a per-row parse; the bytes implement a count refusal | DE |

## Agent Notes
director-engine gen 22 progress -- CLOSED in place: write-py-set-is-schema-checked pair (claim corrected, experiment demoted to lean_proved:70, cb8022760) · doc:quick-setup:74 · key-row-publish claim (count refusal) · grid-push-batch-limit brief in schema order · a00-ca6e4b39:100 quote (03603d739) · 11 scalar evidence_runs -> lists (0f1f3fd78). CODE: grid.py:190 sys.exit = DH.372 running · rotate.py cmd_handoff flatten folded into DH.371 (same card-write path, TMM.190) · mem_cap / launch-memory-cap / workflow.py / brainstorm contract rows NEXT, memory-gated. HELD, a decision: [goal].md title id-prefix regex -- 18 of 371 live goal titles have no id prefix (legacy-direct containers, g13, g5.21, g26.towns ...), so the cell would refuse every later write to them; it needs those titles migrated first, several on other posts, not a one-line schema edit.
