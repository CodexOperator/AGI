---
id: hypothesis:l4-workflow-residue-sub-floor-marker-dead-code-and-truncation
mint_id: 6a57591e79874505a4eb1bce867bc5d2
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 6592bf487de9cfb0
season: 2
testable_claim: "goal:g15 (residue of L4.373/SD.02, Prime review 08:13Z, mur wf_66fbee4c-faf -- ACCEPT WITH RESIDUE, accepted round untouched): (1) check_key_floor's sub-floor skip returns a marker a tuple-reading caller can actually see, not just a printed line (provisioning.py:401-408 currently returns (True, None) and only prints); (2) _parse_last_json (workflow.py:1291) is either wired to a real caller or removed -- it has none today; (3) RunView._tree (workflow.py:991-995) shows a head/truncated preview of a multi-KB unstructured return instead of inlining the whole blob on one line; (4) experiment a00-e9f2167d-babbe4's conjunct numbering is aligned to this hypothesis's and its hermeticity conjunct gets a probe of its own; (5) stage-level timeout_s=0 is made reachable (today's `stage.get('timeout_s') or manifest.get('timeout_s')` treats 0 as absent) and its manifest-level meaning is defined and tested -- a manifest timeout_s=0 must not silently kill every stage. Fixture-proven; suite green. FALSIFIERS: the sub-floor return still cannot be distinguished by a caller; _parse_last_json remains both uncalled and unremoved; the tree still inlines a multi-KB blob whole; the experiment's conjunct numbers still diverge or hermeticity stays unprobed; timeout_s=0 is still unreachable or still silently kills every stage."
title: "Workflow residue: sub-floor marker, dead code, truncation, conjunct alignment, zero timeout (belam review 08:13Z; L4.373 residue)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-workflow-residue-sub-floor-marker-dead-code-and-truncation

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
