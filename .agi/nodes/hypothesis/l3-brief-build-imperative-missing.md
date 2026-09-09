---
id: hypothesis:l3-brief-build-imperative-missing
mint_id: fa68db7bb1934d98981f324f1271f983
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-VIII
scaffold_hash: 93fc02e5026b6eab
season: 2
testable_claim: After the change, brief.assemble renders a kid brief for a target whose body carries a BUILD marker with a literal imperative segment naming the artefact as a diff, and a red-first test asserts that segment is present for a BUILD target and absent for a probe target; measured behaviourally, the next BUILD round dispatched under the new template ends with a non-empty git diff --stat in the parent's worktree.
title: A BUILD brief reads as a question to a kid, so the kid measures instead of building
---
<!-- BODY:BEGIN -->
# hypothesis:l3-brief-build-imperative-missing

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
MEASURED SIX TIMES, DECISIVELY AT L3.34. A brief whose testable_claim is written as 'after the change, X is true' gets read by a pi/GLM-flash kid as a QUESTION about the present, not as a state to bring about. The kid checks whether X holds today, finds it does not, returns inconclusive_lean_disproved with a faithful account of the broken state, and changes no code. Its parent then accepts it, correctly, because the work IS honest. THE EVIDENCE THAT THIS IS A BRIEF-SHAPE FAILURE AND NOT A KID FAILURE: at L3.34 four parents ran concurrently on four different briefs — three of them freshly written by the prime that same hour with deliberately fix-shaped claims, per trap 0g's own remedy — and ALL FOUR returned red-first baselines with zero lines of code. Four independent kids converging on the same non-behaviour is a property of the instructions, not of the agents. Prior occurrences: L3.21 (scaffold-stamps, frontier), L3.22 (seats, probe only), L3.25 (pin-path, third probe), L3.31 (branch2 slice), L3.33 (parent-branch, fourth probe), L3.34 (all four). TRAP 0g ALREADY TRIED THE OBVIOUS FIX AND IT WAS NOT ENOUGH. 0g says write the claim as the fix's proof condition and put RE-RUN AS BUILD in the body. Both were done for all three L3.34 branch briefs. Still four probes. So the remedy is not sharper claim wording, which the prime can always be told to do better; it is a TEMPLATE change, so that no future director has to remember. THE FIX: brief.py's kid template gains an explicit imperative segment for BUILD targets — your artefact is a diff, an empty git diff --stat means you are not done, a wrong or impossible fix stated plainly is a real result while silence about the code is not. Note the shape of this defect: it is the same class as the L3.31 finding where brief.py taught every kid a broken write.py call. The kid template is a single point of failure for every kid in the graph and it has now silently degraded two rounds' worth of work in two different ways. It deserves a test of its own for content, not only for rendering.
