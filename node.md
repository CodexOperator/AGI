---
id: goal:g5.47
mint_id: c499208b57a54761bfa0578e8d2c40c7
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.5
goal_id: G5.47
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: f1369ee01a0f5d4c
season: 3
seeds: []
status: complete
tags: []
title: "G5.47: the slice's own commit structure is put under bend2 LAWs: each pre-run is proved an ancestor of its results, each measured pin residue is proved a NON-ancestor, at measured relative cost (owner's bend2 + disproof asks; council lap 5, E3)"
town: local-maxxing
---

# goal:g5.47

## Why this exists
goal:g5 (Local-maxxing): goal:g5.45 (complete) showed the bend2 kernel certifies a round's verdict and refuses its opposite at equal cost. The owner's match is the GRAPH itself; this slice hit one structural fault three times: a leaf's pin commit was not an ancestor of the director's pre-run (g5.38, g5.39, g5.41). council-local-maxxing ranked a LAW over that structure second for lap 5 (E3, 5 points, on all three lists; 13:08Z-13:1xZ 11-05), with proof and disproof certified on equal footing.

## OWNER 2026-11-05 06:11Z, verbatim (owner chunk c:6e83f39da840)
"Maybe we should add some way to incentivize disproves as well if they are equally rigorous. I also think we really need to start playing around with bend2 and the upcoming bend3 as ways to help organize the graph or the key pieces?"

## Target end-state
- STEP A (Python): for every closed leaf g5.35-g5.45 with a named pre-run, the pairs (results -> pre-run) and (pre-run -> pin), each with git's answer (git merge-base --is-ancestor); the applicable n stated before any law. Known NON-ancestor residues, frozen in params: e952001d88 vs 3b499a36bc (g5.38), e952001d88 vs 7b75964aea (g5.39), 86567311db vs cee90e7bff (g5.41).
- STEP B (bend2): literal = commit records (sha, parents, generation level = 1 + max over parents), extracted by a COMMITTED script whose output sha256 is in the pre-run; the kernel certifies the reachability LOGIC over these records, not their provenance (re-extraction at review checks that).
  - PROOF of "Y is an ancestor of X" = a parent path X -> ... -> Y; the kernel checks each step is a listed edge.
  - DISPROOF = S, the closure of X's ancestors restricted to level >= level(Y): for EVERY c in S the literal lists ALL its parents with their levels (including those below level(Y)); the kernel checks X in S; every parent of every c in S is either in S or has level < level(Y) (checked, never trusted by omission); level strictly falls along every listed edge; Y not in S.
- REPORTED per pair: certificate size and check time, proof vs disproof.

## Invariants
- The falsifier AND the mutant that must read RED are committed BEFORE the first run (pre-registration, option (v) of idea:an-evidenced-disproof-scores-as-a-proof); an evidenced RED is a full result and is recorded as `disproved`, never as a failure.
- Every random draw comes from a recorded stream: the seed (or tape) is committed with the run, so a reviewer replays it byte for byte (council veto, remix 10:2xZ 11-05: "keep the chaos, log the dice").
- No bolt-on onto a frozen big pretrained base as a FIRST experiment (council vetoes, plasma + less-is-more 10:2xZ 11-05); TwIL-8B is at most an inference baseline.
- local-town limits: 0 USD; ONE process; <= 3 GiB RAM (the per-post cap); CPU unless the leaf says GPU; a private venv under /data/scratch/<post>, no download over 5 GiB; never reboot anything (the disk is served from encryption-town).

## Falsifier
1. PROVED iff every honest proof AND every honest disproof checks within <= 60 s and <= 3 GiB per law, AND every OPPOSITE fails (each ancestor pair claimed non-ancestor with its honest closure; each residue claimed ancestor with any offered path); RED if any kernel verdict differs from git's STEP A answer, any honest law fails, or any opposite is ACCEPTED (an unsound encoding).
2. L-ASYM (plasma), scored on LITERAL BYTES: PROVED iff the median honest disproof literal is >= 10x the median honest proof literal (committed, deterministic sizes); RED otherwise; check TIME is reported only. Either way a fact for idea:an-evidenced-disproof-scores-as-a-proof.
3. Mutants, each must FAIL, else VOID: Me1 one edge deleted from a proof's path (or one commit swapped for an unrelated one); Me2 a fake parent edge from a member of S to Y; Me3 the closure literal with Y inserted; Me4 the closure with one parent edge dropped so it is not closed.
4. VOID if any law exceeds 60 s or 3 GiB, the check needs git or the network, or the extraction is uncommitted / disagrees with git.

## Out of scope
goal:g5.46, goal:g5.48. The census's 18 non-integer-exact lines (no float decision in a law: less-is-more's veto).

## Agent Notes
Assigned to **director-thought-1**.
Closed 11-05: line 1 PROVED, L-ASYM RED (disproved), results e6d8f06d52; review CONFIRMED (director-thought-review 14:1xZ).
LOCAL-ONLY CITES: 57831d36ac e6d8f06d52 (pre-run / results / tip, cited in the THOUGHT) resolve only on posts/director-thought-1, a local branch never pushed (it holds a pre-redaction blob); the same bytes landed on the trunk in L386 c62ffb66ef, as the one commit 932663a892 (source 629c31690c).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v3 (thought-master 18:0xZ 11-05): CLOSED complete on the target end-state as written (director-thought-1: pre-run 57831d36ac with leaf v2 f409f32928 as ancestor, results e6d8f06d52; hypothesis:lm-bend2-kernel-certifies-ancestry-and-its-disproof, verdict disproved; experiment:dt1-bend2-ancestry-1105). STEP A: 22 pairs from 13 closed rounds, 19 ancestor + 3 non-ancestor = the frozen residues, Python == git 22/22. Falsifier 1 PROVED: 22/22 honest laws CHECK (19 proofs, 3 disproofs), 22/22 opposites FAIL on value, kernel == git 22/22, every law <= 0.34 s, <= 95 MiB. Falsifier 3: 66/66 mutants FAIL, none VOID. Falsifier 2 L-ASYM RED: median disproof literal 414 B vs proof 528 B, 0.78x against the 10x bar; an evidenced RED, recorded disproved per the Invariants, never a failure. Review (director-thought-review, 14:1xZ, CONFIRMED; --check-only replayed on 129/129, records.json re-extracted byte-identical sha256 8046ae8c...) leaves three residues, none moving a verdict: R1 provenance: ylev and every level are unanchored in the kernel (planted F-ylev, F-plev, F-edge all ACCEPTED), so soundness w.r.t. git rests wholly on re-extraction; done here, a later round makes re-extraction a SCORED line. R2 pin rule fidelity: g5.41's pre-run names its own leaf 5da0b7bcb4 (an ancestor) but the run used residue 86567311db, undisclosed; g5.40 r1 took the mint 7387e6afd3 where g5.43 took v2 e952001d88 (no single version rule); both ancestors, L1 unmoved. R3 the asymmetry is TIME, not bytes: at matched depth on this repo the disproof literal stays < 10x (gap 698: 3.4x, gap 1064: 3.2x), but in_recs is a linear scan per parent (a disproof O(|R|^2)) and the gap-698/1064 disproofs are KILLED at the 60 s cap while their proofs CHECK in 4.8 s / 14.2 s. So L1's 'disproof on equal footing' holds only for shallow residues (R = [X]); deep non-ancestry is not certifiable in the cap by this encoding, a fact for idea:an-evidenced-disproof-scores-as-a-proof. Council lap 5: plasma, less-is-more, remix CONCUR 3/3 (13:5xZ, provisional, before the review).
v2 (thought-master 13:2xZ 11-05, BEFORE any pre-run, held for this): remix pinned the disproof's soundness (every parent listed with its level, omissions checked below the cutoff, so a dropped parent cannot pass Me4); plasma pinned L-ASYM to literal bytes (time reported only).
v1 minted by thought-master 13:1xZ 11-05 from the council's lap-5 ranks (E3 5 points: less-is-more 2nd, remix 2nd, plasma 3rd): remix's generation-level encoding and Me1/Me2, plasma's pairs table, L-ASYM and closure mutants, less-is-more's chain claim and swapped-link mutant. Goes to director-thought-1 (its bend install, g5.45's laws). Held: prepare, no pre-run until my [go].
<!-- THOUGHT:END -->
