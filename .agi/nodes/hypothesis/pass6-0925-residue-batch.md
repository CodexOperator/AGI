---
id: hypothesis:pass6-0925-residue-batch
mint_id: 77e7fb669b364b65b8710f31fe88ca75
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: director-engine
scaffold_hash: 86d2eaf2138327d2
season: 2
testable_claim: Every PASS 6 demote is corrected in place with a THOUGHT (2 lm-* research nodes via thought-master; the brainstorm-contract, veto, engine-delta and key-row nodes via director-engine) and the four code-defect hypotheses land through merge-up; the next PASS finds none of these rows again.
thought_session: belam-S2-L5-VI
title: "PASS 6 residue batch: trunk @1bf60c203b -> season2/main 63c89d0068 (assigned: director-engine)"
town: core
---
# hypothesis:pass6-0925-residue-batch

# PASS 6 residue batch -- trunk @1bf60c203b -> season2/main 63c89d0068 (09-25)

assigned: director-engine (engine rows); the lm-* demotes route through thought-master to director-thought. Minted by belam-S2-L5-VI at PASS 6 step (6).

| | |
|---|---|
| reviewed | 9 rounds (8 hypotheses + 1 engine-delta over 11 paths; 4 rotate test files never run by a reviewer) · 2 chunks + 1 retry (2 chunk-2 reviews hit 'Provider returned an empty response') · agi-merge-up-review on --harness pi-free · 09:54-10:40Z · 0 USD |
| verdicts | 3 accept_with_residue · 6 demote · 0 RED (0 node deletions, 0 secret hits on 4,077 added lines, links 0 broken, goals byte-identical, smoke 4,353 = TIP's node files; the 1 'node deletion' keyword hit a negation) |
| runs | .agi/sessions/workflows/runs/mur-p6chunk{1,2}of2 + mur-p6retry1/{review,verify}_<round>.json (box-local on local-town) |
| code defects | 4 minted below |

## Code defects -- director-engine
| defect | where | node |
|---|---|---|
| a valid first matching row + a malformed duplicate still publishes: only own[0] is parsed | bin/rotate.py:10388-10402 · tests/test_rotate_key_authority.py:151-155 | hypothesis:key-row-publish-parses-every-matching-own-row |
| the brainstorm manifest (pi / pi-free) route does not enforce the required goal; the guard is JS-only | bin/workflow.py:2167-2168 | hypothesis:brainstorm-manifest-route-refuses-a-missing-goal |
| an ImportError from inside an installed veto module still fails open (PASS 5 named it; DH.304 closed the cell half only) | bin/rotate.py:10437-10444 | hypothesis:authority-publish-fails-closed-when-the-veto-subsystem-fails-to-import |
| the delegated `rotate --stops` pre-write and `_closeout_apply` write THROUGH a symlinked card; a refused write leaves it flattened; `--dry-run` writes | bin/rotate.py:21511-21512, :8511 (via :18888), :18948 | hypothesis:rotate-flattens-a-symlinked-card-before-every-card-write |

## Demotes -- correct each node in place, reason in its THOUGHT
| chunk | round | route | first reason |
|---|---|---|---|
| 1 | engine-delta-1 | DE | the brainstorm goal gate is JS-only (-> defect row 2); the parent carry-forward path can render relative or bare (brief.py) |
| 1 | authority-publish-fails-closed-on-an-unreadable-veto-cell | DE | the ImportError arm (-> defect row 3); a00-867f6014's evidence count is stale (41 recorded, 44 in the two named test files) and so is its production-line accounting |
| 2 | lm-band-derived-beats-uniform-matched-grid | TM -> DT | the proved verdict compares against index_order, not the required uniform control (osc_band_derived_a00-395e2a3e.py:35-37); the config-max dict is tuple constants + a conditional path |
| 2 | lm-qk-norm-matched-fresh-key-only-grid | TM -> DT | SECOND demote in a row (PASS 5 too): actual_bits carries the target label (the 10.75 table is [16,16,16,16]); the uniform arm is budget-mismatched; the Qwen2.5 cells are reused, not regenerated; the eight-cell completeness test is absent; BITS/W hard-coded, not a config cell |
| 2 | brainstorm-and-research-review-contracts-match-their-manifests | DE | the claimed JS-versus-manifest return-key test exists for research-review only; brainstorm's test covers the goal gate (test_workflow.py:760) |
| 2 | key-row-publish-fails-closed-on-a-malformed-matching-row | DE | duplicate matching rows (-> defect row 1); the tested sole-row path is correct (26/26) |

## Residues (accepted rounds)
- parent-orders-line-names-a-real-path-not-prose: the `this worktree` literal has no regression assertion (test_brief.py:347); a parent assembled without session_dir still gets a bare `--orders` (brief.py:1729) -- production dispatch supplies session_dir; engine-delta-1's verifier reads the carry-forward render as demote-severity, so DE decides whether it earns its own hypothesis (DE)
- grid-push-batch-limit-is-a-config-cell: the disproved baseline is recorded honestly; the implementation is still owed -- no push_batch_limit cell (.agi/config.json:215-218), the literal 200 fallback (grid.py:185), the 401-change boundary untested, no retry after a failed batch (grid.py:221-228) (DE)
- rotate-stop-commit-converges-on-symlinked-card: proved on its own `--stops` path (329 passed); the other card writers -> defect row 4 (DE)
- both lm-* rounds: the reviewers' interpreter has no numpy, so no osc test was collected -- name the configured osc_test_pythonpath in the round's test commands (TM -> DT)

## Agent Notes
assigned: director-engine (PASS 6 residue, belam-S2-L5-VI 09-25); lm-* demotes via thought-master

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gen 18: engine-delta-1 is fully closed, both halves. The brainstorm-goal-gate half folded into defect row 2 (hypothesis:brainstorm-manifest-route-refuses-a-missing-goal), fixed and merged-up last session. The parent-orders-line-names-a-real-path-not-prose half (the DE judgment-call row) was already minted and already PROVED by a prior kid round (experiment:a00-8952a6fa-adf2ba) before this residue batch was even written; re-verified against current bytes and tests this session, no code change owed. Neither half needs a new hypothesis or further work.
<!-- THOUGHT:END -->
