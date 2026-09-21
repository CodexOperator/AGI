---
id: hypothesis:l3-pi-edit-tool-edits-array
mint_id: b1765470975d41d596c67abc3c592484
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-IX
scaffold_hash: f3162d6e6ae50e09
season: 2
testable_claim: After the change, the edit-call shape a kid actually emits is either accepted by the tool or taught correctly by brief.py's kid template, proven by a red-first test pinning the accepted shapes and, where the template is implicated, a red-first test asserting the rendered template CONTENT carries the correct call shape rather than only that it renders.
thought_session: belam-S1-L3-IX
title: Two independent kids in one round lost a turn each to the edit tool rejecting a stringified or nested edits-array
---
<!-- BODY:BEGIN -->
# hypothesis:l3-pi-edit-tool-edits-array

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done.

MEASURED ON TWO INDEPENDENT KIDS IN ONE ROUND (L3.37, 2026-09-08), which is what makes it a tool defect rather than a kid mistake. Kid `a00-d1c9ccb3` (deepseek-v4-flash): "the edit tool rejected an edits-array as a string, costing one turn before I fell back to a scripted body replace". Kid `a00-5da2e6ad`, on a different brief, in a different worktree, against a different file: "my first two edit() calls to heal.py were malformed (accidentally nested the edits array)". Two kids, two models' worth of prompting, same seam, same round. Neither was told about the other.

THE COST IS SMALL PER OCCURRENCE AND PAID BY EVERY KID FOREVER, WHICH IS THE ARGUMENT FOR FIXING IT. One wasted turn is roughly one wasted OpenRouter dollar-fraction and, worse, one turn of a weak model's limited attention spent on tool syntax instead of on the work. This project's whole design is against exactly that: motion spent on mundane operations rather than on the task. It also degrades the evidence, because a kid that spends turns fighting its editor has fewer left for the red-first test that the brief actually gates on.

WHAT TO FIND OUT FIRST, then fix: whether the fault is (a) the pi harness's edit tool contract being genuinely strict where a stringified or singly-nested array is the obvious thing a model will emit, (b) the kid template in `brief.py` teaching or failing to teach the correct call shape, or (c) both. Note the precedent, because it is the same shape and it was expensive: at L3.31 a parent found that `brief.py`'s kid template had been teaching every kid a BROKEN `write.py` call, silently, for rounds. The kid template is a single point of failure for every kid in the graph and it has now degraded work in at least three distinct ways. Whatever you find, the fix belongs wherever it stops recurring for the NEXT kid, not wherever it is easiest to patch.

THE PROOF CONDITION: a red-first test that pins the accepted edit-call shapes — including the forgiving handling of whatever the two kids actually emitted, if forgiveness is the right answer — plus, if the template is implicated, a test asserting the template's rendered text contains the correct shape. `brief.py`'s template is currently pinned by tests for RENDERING and not for CONTENT; that gap is what let the L3.31 defect live, so close it for this too.

DO NOT: widen this into a general rewrite of the harness adapters, and do not touch `.agi/nodes/.geometry/seats.md`.
