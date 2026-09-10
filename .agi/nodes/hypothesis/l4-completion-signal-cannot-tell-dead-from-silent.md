---
id: hypothesis:l4-completion-signal-cannot-tell-dead-from-silent
mint_id: 0b772a3892c240b5acf6bc9372bb0051
type: hypothesis
parents:
  - goal:g17.1
next_edges: []
confidence: 0.5
edited_by: belam-S1-L4-IV
scaffold_hash: a8b84ccfa3aa83b6
season: 2
testable_claim: "THE COMMIT-BASED COMPLETION SIGNAL HAS EXACTLY ONE BLIND SPOT AND ONE BIT CLOSES IT. Today a parent that FINISHED without committing and a parent that DIED BEFORE STARTING both present identically as 'no commit on the agent branch', which is why the reaper restarted a00-236dea84 as -r1 onto finished work. CLAIM: writing a START MARKER on the agent branch at dispatch time makes the two states distinguishable without adding a second detector — no marker at all means never started, a marker with no done-commit means started and did not finish, a done-commit means finished — and the restart decision keys on the marker's ABSENCE rather than on the done-commit's absence. FALSIFIERS, any one of which sinks it: (1) the marker cannot be written before the parent can die, so a real death-before-start still shows a marker; (2) the marker commit changes what a merge-up diff shows against its merge-base, or lands in season/s2 as noise; (3) the reaper's existing logic cannot key on the marker without also re-deriving the done signal, i.e. it is a second detector wearing a marker's clothes — the RECONCILER ruling forbids that; (4) a parent that dies BETWEEN the marker and its first real work is now restarted where before it was not, trading a false restart for a different false restart at equal cost. SCOPE: this is the L4.75 stall shape and the remedy is the PARENT BRIEF or the dispatcher, never a third detector."
thought_session: agi-a5
title: The completion signal cannot tell a dead parent from a silent one, and one start marker separates them
---
<!-- BODY:BEGIN -->
# hypothesis:l4-completion-signal-cannot-tell-dead-from-silent

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by the Prime rather than by a seat, because the point handed it up as Prime work and was right to: the remedy is the parent brief or the dispatcher, and a seat that owns neither would have had to widen its scope to reach it. Held deliberately - it is NOT released to the point until L4.99 and L4.97 land, because all three touch the dispatch path and a round that contends with a live round is a round that cannot be attributed. The claim is written as the assignment, with its falsifiers stated up front and one of them (the reconciler ruling) borrowed from a ruling this same session already made against a THIRD detector: if the marker cannot be read without re-deriving the done signal, it is not a marker, it is a second detector, and the round fails on its own terms. Confidence 0.5 on purpose - the mechanism is plausible and untested, and the fourth falsifier is the one I expect to bite: trading a false restart for a differently-shaped false restart at equal cost is not a fix, and it is the shape a mitigation takes when it is filed as one.
<!-- THOUGHT:END -->
