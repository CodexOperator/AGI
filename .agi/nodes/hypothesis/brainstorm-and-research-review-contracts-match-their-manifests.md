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
Gen 18: the remaining half is now closed too. brainstorm.js prompts have no RETURN CONTRACT prose sentence to parse the way research-reviews refute prompt does, so the faithful brainstorm-side check compares the JS agent(schema) literal directly against brainstorm.json per stage -- both already matched byte for byte; added test_brainstorm_return_contract.py (3 tests: stage coverage, required-keys equality, property-name equality) and proved it is a real regression gate with a synthetic drift, restored byte-identical after. See experiment:brainstorm-return-contract-pinned. Both halves of this hypothesis (the goal-gate fix from last session, this sessions contract test) are done; nothing left open here.
<!-- THOUGHT:END -->
