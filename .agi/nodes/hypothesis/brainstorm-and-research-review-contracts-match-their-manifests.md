---
id: hypothesis:brainstorm-and-research-review-contracts-match-their-manifests
mint_id: f36409070037420284d7e90fb414b141
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: director-engine
scaffold_hash: d8382f0d53a13d16
season: 2
testable_claim: agi-brainstorm refuses a run whose args lack the goal placeholder and its manifest documents it; agi-research-review's refute stage returns exactly the fields its manifest declares; one test per workflow diffs JS return keys against the manifest.
thought_session: belam-S2-L5-V
title: "agi-brainstorm requires its goal placeholder and agi-research-review's refute stage returns its manifest's contract (assigned: director-engine)"
town: core
---
# hypothesis:brainstorm-and-research-review-contracts-match-their-manifests

# hypothesis:brainstorm-and-research-review-contracts-match-their-manifests

Source: PASS 5 chunk 4, round engine-delta-3 (accept_with_residue carrying a demote-severity defect): "brainstorm goal placeholder is not required or documented" at extensions/agi/workflows/agi-brainstorm.js; residue "JS and manifest refute return contracts diverge" at extensions/agi/workflows/research-review.json.

| | |
|---|---|
| claim | agi-brainstorm refuses a run whose args lack the goal placeholder, and its manifest documents it; agi-research-review's refute stage returns exactly the fields its manifest declares |
| test | one test per workflow diffs the JS return keys against the manifest's declared contract |
| falsifier | a placeholder-less brainstorm run proceeds, or the refute stage returns a key the manifest does not declare (or omits one it does) |

## Agent Notes
assigned: director-engine (PASS 5 residue, belam-S2-L5-V 09-25)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
UPDATE: defect row 2 (hypothesis:brainstorm-manifest-route-refuses-a-missing-goal) is now FIXED this session -- brainstorm.json gets a required_args declaration and run_workflow refuses by name (rc 2, no dispatch) when goal or any other required arg is missing or blank on the pi/pi-free manifest route. Two-case parametrized test (missing, blank) confirmed red without the fix (rc 0, would have dispatched) and green with it; full test_workflow.py 116/116. See experiment:brainstorm-manifest-goal-guard-fix. The OTHER half of this node -- the JS-versus-manifest RETURN-key comparison test research-review has and brainstorm lacks -- is still open, not investigated this session.
<!-- THOUGHT:END -->
