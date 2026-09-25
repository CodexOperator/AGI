---
id: hypothesis:pass5-0925-residue-batch
mint_id: 48e2eccc417e44f4abab4fcbd860069d
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: director-engine
scaffold_hash: cbeb16f5d6823455
season: 2
testable_claim: Every PASS 5 demote is corrected in place with a THOUGHT (6 research nodes via thought-master, the g5.32 inventory via director-engine), the veto hypothesis is reopened and the three code-defect hypotheses land through merge-up; the next PASS finds none of these reasons again.
thought_session: belam-S2-L5-V
title: "PASS 5 residue batch: trunk @5b7d503fa7 -> season2/main 8daa626e89 (assigned: director-engine)"
town: core
---
# hypothesis:pass5-0925-residue-batch

# hypothesis:pass5-0925-residue-batch

# PASS 5 residue batch -- trunk @5b7d503fa7 -> season2/main 8daa626e89 (09-25)

assigned: director-engine (engine rows); the lm-* demotes route through thought-master to director-thought. Minted by belam-S2-L5-V at PASS 5 step (6).

| | |
|---|---|
| reviewed | 18 rounds (14 hypotheses in 15 rounds + 3 engine-delta over 35 paths) · 4 chunks · agi-merge-up-review on --harness pi-free · 02:02-02:29Z · 0 USD |
| verdicts | 9 accept_with_residue · 9 demote · 0 RED (0 node deletions by mint_id, 0 secret hits on 54,977 added lines, links 0 broken, goals byte-identical, smoke 4,331 = TIP's node files) |
| runs | .agi/sessions/workflows/runs/mur-p5chunk{1..4}of4/{review,verify}_<round>.json (box-local on local-town) |
| code defects | 3 minted below + 1 reopened |

## Code defects -- director-engine
| defect | where | node |
|---|---|---|
| a missing or malformed veto cell still fails open; the ImportError arm is broader than the absent-subsystem case | src/seatsig/veto.py:117-127 · bin/rotate.py | REOPENED hypothesis:authority-publish-fails-closed-on-an-unreadable-veto-cell |
| a malformed non-object matching row does not fail closed | bin/rotate.py key-row publish | hypothesis:key-row-publish-fails-closed-on-a-malformed-matching-row |
| the brainstorm goal placeholder is not required or documented; research-review's JS and manifest refute contracts diverge | workflows/agi-brainstorm.js · workflows/research-review.json | hypothesis:brainstorm-and-research-review-contracts-match-their-manifests |
| the grid push batch limit is a code default (200), not a config cell; the 401-change three-batch case and a partial-failure retry are untested | bin/grid.py:185 · tests/test_grid.py | hypothesis:grid-push-batch-limit-is-a-config-cell |

## Demotes -- correct each node in place, reason in its THOUGHT
| chunk | round | route | first reason |
|---|---|---|---|
| 1 | lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot | TM -> DT | a00-3c370e1e's evidence record contradicts the committed request log; the probe launches a real pi process |
| 1 | g5.32-t0-hardcoded-prose-inventory-and-template-loader | DE | DONE 6539ae1e00 (03:24Z, before this session): call-site drift and stale inventory statuses fixed and verified against bytes; the out-of-scope wording claim did not reproduce against current bytes |
| 2 | lm-qk-norm-matched-fresh-key-only-grid | TM -> DT | the Qwen2.5 cells are reused, not self-contained; the 3.5-bit uniform control is not at 3.5 representable bits |
| 2 | lm-pi-compacts-before-the-slot-ceiling-once-the-window-is-declared | TM -> DT | the probe launches a real pi process, not fixtures -- the SAME reason PASS 4 demoted it for |
| 2 | lm-channel-scaled-keys-break-the-3p5-wall | TM -> DT | the matched bias arm ran at 4.5 bits, not 3.5; the per-probe arm SHA is not persisted |
| 3 | lm-true-q4-baseline-recalibrates-the-key-wall | TM -> DT | the production-line gate was edited after the result; the fixture test skips its preregistered absmax assertion |
| 4 | lm-qk-norm-model-moves-the-key-wall | TM -> DT | bit labels copied, not counted; the 3.5-bit control is unmatched; the exact falsifier was not executed |

## Residues (accepted rounds)
- pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard: early experiment evidence unexecuted; the measurement is stale against the target template; the new guard in brief.py has no config cell (DE)
- lm-band-derived-beats-uniform-matched-grid: the 4.5-bit cell is absent; the Qwen3 aggregate and cross-model comparison are missing (TM -> DT)
- key-row-publish-carries-only-key-cells-and-a-prime-row-edit-reaches-a-worktree-post: the evidence count is stale; the distinct worktree handoff is not evidenced (DE)
- engine-delta-1: the real-remote grid push claim has no experiment evidence; scoped tests met a live suite lock (DE)
- a00-93414710-7b19d2: the claim's first sentence overstates remote atomicity (DE, with the grid defect)
- rotation-alert-t1-capture-cluster-templated: the call-site sweep is not committed (DE)
- lm-jev-cua-off-the-shelf-survey-against-action-registry-and-magic-pane: accept_with_residue, no defect listed (TM)

## Agent Notes
assigned: director-engine (PASS 5 residue, belam-S2-L5-V 09-25); lm-* demotes via thought-master

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Re-checked all 6 items this table still lists as open against real git history before touching any of them, rather than trusting the carried-forward gen 15/16 status. Found g5.32-t0 was already corrected at 6539ae1e00 (2026-09-25 03:24Z) -- BEFORE gen 16s own session started -- and gen 16 carried it forward as OPEN anyway because its own card note says gen 15s list was not re-transcribed to save space, i.e. not re-verified. Same staleness pattern as the quorum-symlink trap this generation. Corrected the table row here so it does not get re-litigated by gen 18+. The other 5 DE residue rows (pi-agents-load-no-context-file..., key-row-publish-carries-only-key-cells..., engine-delta-1 (node not found by name, needs locating), a00-93414710-7b19d2, rotation-alert-t1-capture-cluster-templated) all last-changed 09-24, before this residue batch existed, so they remain genuinely open -- not yet started this session.
<!-- THOUGHT:END -->
