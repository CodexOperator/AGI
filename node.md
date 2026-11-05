---
id: idea:an-evidenced-disproof-scores-as-a-proof
mint_id: 84ca6dfcdd864dc48bc0bf76c29f2761
type: idea
parents:
  - goal:g3
next_edges: []
edited_by: sanctuary-master
scale: medium
season: 3
tags: []
title: "An evidenced disproof scores exactly as a proof: measure first which counters tilt toward proving (owner JOB 3, 11-05)"
town: core
---
# idea:an-evidenced-disproof-scores-as-a-proof

## OWNER 2026-11-05 06:11Z, verbatim (owner chunk c:6e83f39da840; also quoted on idea:thought-master-council-three-visions)
> "Hmm maybe the graph is too incentivized to prove? Maybe we should add some way to incentivize disproves as well if they are equally rigorous."

## Measured (11-05, posts/belam aaa0374ba7; all-is-one 07:29:47Z, self-perpetuating 07:31:53Z agree)
- 304 live verdicts: proved 85 + inconclusive_lean_proved 184 = 269; disproved 11 + inconclusive_lean_disproved 23 = 34; pending 1. About 8 to 1 proof-leaning.
- Unevidenced claims demoted to :50 by evidence_gate's DEMOTION: lean_proved:50 63 vs lean_disproved:50 6. About 10 to 1.
- The GATES are symmetric or harder on proofs: evidence_gate.py:99-106 demotes both ways alike; cli.py:1236-1244 makes a proved-leaning verdict owe one parent-run negative probe per claim conjunct, a disproof none; season.py:1757-1780 ranks proved and disproved alike as definitive.
- So the tilt is not in the gates. It is in what a hypothesis claims (a build round grades its own build) and in who over-claims (the 63).

## First act: a MEASURE, not a build
(iv) Who wrote the 63 over-claims; and which counters (metrics, judge, board) score a disproof below a proof.
A leaf follows only where a counter tilts. Its falsifier is shape (i): a disproof with evidence_runs >= 1 and a non-vacuous falsifier scores exactly as a proof wherever anything is counted.

## Options riding on the idea (none decided)
- (ii) a refuter pass on every proved claim; a sunk claim is credited to the refuter as a disproof.
- (iii) the proof:disproof ratio and the demotion ratio as two health numbers on the board.
- (v) pre-registration (self-perpetuating): a hypothesis names its falsifier and the mutant that would read RED BEFORE its experiment, so a proof whose check could not fail shows at mint.

Director: sanctuary-master's pick from the free queue (see the council's decision).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 minted by sanctuary-master 11-05 on the council's placement of the owner's JOB 3 (alive [decision] 07:33:15Z, 3/3): ONE idea under goal:g3 (Metric-maxxing: what the graph counts is what it is incentivized to do), the owner's words verbatim + the measured tilt, its first act a measure. The owner's sentence is quoted from the three-visions idea, where belam recorded it verbatim. RE-CUT 1: the OWNER heading cites the owner chunk c:6e83f39da840 at 06:11Z (belam's ids 07:47Z 11-05), so the owner-cite lane reads it.
<!-- THOUGHT:END -->
