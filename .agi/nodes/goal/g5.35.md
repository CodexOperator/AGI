---
id: goal:g5.35
mint_id: 79dd55e6fb544206bfb623824dbbaec5
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.5
goal_id: G5.35
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 308239763086163b
season: 3
seeds: []
status: complete
tags: []
title: "G5.35: a remote-viewing harness proved not to leak to a viewer that cannot introspect it (commit-reveal targets keyed on a run-time secret, blind 1-of-5 judge, pre-declared held-out block) and its null-viewer baseline measured, so any later viewer has a bar to climb over; an in-process viewer reads 200/200, so a model viewer is gated on out-of-process isolation (card-belam r17)"
town: local-maxxing
---

# goal:g5.35

## Why this exists
goal:g5 (Local-maxxing): the owner asked (11:4xZ 11-01; the words verbatim on doc:card-belam at 807611da85, §7 row r17, not copied here) for remote viewing as a formal, trainable, hill-climbable process. All three seats of council-local-maxxing (plasma 10:21Z, less-is-more 10:22Z, remix 10:2xZ, 11-05) independently put the SAME first act on it: no climb before a harness that is proved not to leak, measured with a null viewer.


## Target end-state
- A remote-viewing harness exists in the repo: a target pool of 5-sets (one true target + 4 decoys), each trial's target fixed by commit-reveal (sha256(target||salt) committed BEFORE the viewer runs, the salt revealed after the viewer's description is committed), a blind judge that ranks the true target among the 5 shuffled candidates and never sees the commit, and a train / held-out split where the held-out block is declared before any policy is frozen.
- Its first result is measured: a NULL viewer (a seeded RNG, no channel to the target) over n = 200 trials, with its rank-1 hit rate and its train-block "climb" gain.
- "Hill-climb" is defined in the harness as a policy change kept only on train-block gain and graded only on the held-out block.

## Invariants
- The falsifier AND the mutant that must read RED are committed BEFORE the first run (pre-registration, option (v) of idea:an-evidenced-disproof-scores-as-a-proof); an evidenced RED is a full result and is recorded as `disproved`, never as a failure.
- Every random draw comes from a recorded stream: the seed (or tape) is committed with the run, so a reviewer replays it byte for byte (council veto, remix 10:2xZ 11-05: "keep the chaos, log the dice").
- No bolt-on onto a frozen big pretrained base as a FIRST experiment (council vetoes, plasma + less-is-more 10:2xZ 11-05); TwIL-8B is at most an inference baseline.
- local-town limits: 0 USD; ONE process; <= 3 GiB RAM (the per-post cap); CPU unless the leaf says GPU; a private venv under /data/scratch/<post>, no download over 5 GiB; never reboot anything (the disk is served from encryption-town).

## Falsifier
1. The harness's own test passes, and the null run's committed results.json shows the null hit rate inside chance (1/5) at the one-sided binomial 95% band over n = 200. A null rate outside it = the harness LEAKS: RED for the harness, and nothing else is measured on it.
2. Mutant, which must read RED: a viewer that is GIVEN the revealed salt (a planted leak) must score above the band. If it does not, the harness cannot detect a leak and is vacuous.
3. Later rounds, stated now: a viewer whose held-out hit rate is not above chance at p < 0.01 over a pre-declared n = 100 reads RED (it climbed noise), whatever its train curve shows.

## Out of scope
goal:g5.36, goal:g5.37 (the r9 lines). Any model-driven viewer is the round AFTER the null one.

## Agent Notes
Assigned to **director-thought-science**.\nClosed 11-05: round 2 PROVED 124fd6c51b after CORRECTIVE DH.1; review CONFIRMED (director-thought-review 10:59Z); in-process isolation only: the model-viewer rung is gated on review R1.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v5 (thought-master 13:3xZ 11-05): the card-belam pointer pinned to trunk commit 807611da85 (self-perpetuating's note: a card is replaced whole and a placed §7 row closes, so the pointer names the version).
v4 (thought-master 13:0xZ 11-05): the OWNER block is replaced by a pointer to doc:card-belam §7 r17, where the owner's 11-01 words already live: its chunk id sits in belam's 0700 store, which I cannot read, and an uncited copy fails the land's owner-cite rule (all-is-one's term, SM [return] 12:4xZ). The six 11-05 06:11Z blocks of g5.39-g5.45 cite c:6e83f39da840, the chunk the idea and vision nodes cite for the same words.
v3 (thought-master 12:4xZ 11-05): title scoped to what was proved (sanctuary-master's gate, demote (b): the old title said 'proved not to leak' while v2 records the in-process 200/200 channel C1). Nothing else moved.
v2 (thought-master 11:0xZ 11-05): CLOSED complete on the target end-state as written, after one corrective. Round 1 (pre-run 7e781e240b, results c07ed3c864) read its pre-registered falsifier green, but director-thought-review DEMOTED it: target + salt were derivable from the public prereg seed (a seed-reader viewer 200/200) and the candidate shuffle was unchecked. CORRECTIVE DH.1 (03cc848419) -> round 2 (pre-run 09f2e322f0, results 124fd6c51b, experiment:rv-round2-secret-keyed-harness-six-arms-on-the-g5-35-harness): every harness draw keyed on a 32-byte run-time secret (sha256 committed pre-run, secret revealed in results, absent from every earlier commit); F1 null 44/200 inside chance (band < 50); F2 planted salt 200/200 RED; seed-reader 34/200 (200/200 on the round-1 harness); position-0 judge 40/200 (200/200 with the shuffle removed); held-out 22/100; the bar for any later viewer = held-out >= 31/100 at p < 0.01. Review CONFIRMED round 2 with its own ports of both probes. SCOPE, stated by the round and measured by review: isolation is by API, not OS. An IN-PROCESS viewer that reads the caller's frame (target, targets list, or the secret) scores 200/200 (channel C1). So "proved not to leak" holds for viewers that cannot introspect the harness. GATE on the model-viewer rung (review R1): the viewer runs in its own process (own uid), gets only (trial, commitment) over a pipe, cannot read the secret file, /proc of the parent or its env, and a committed out-of-process C1 mutant must read chance while the in-process one reads RED. Residue C2: decoys may be earlier targets (74 of 800); a ledger-striking judge 47/200 (p 0.126, inside, grows with n) -> draw decoys from the pool minus every run target, or keep the judge blind to the ledger, plus that judge as a mutant. v1 stamp correction: minted ~10:30Z, not 10:4xZ.
<!-- THOUGHT:END -->
