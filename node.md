---
id: goal:g5.53
mint_id: 5cfdec9769444a70a469ae3fe760dc2d
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.5
goal_id: G5.53
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: e8e326349d3dcd44
season: 3
seeds: []
status: complete
tags: []
title: "G5.53: a HARDER 40-task suite (three tiers by construction), k = 3 repeats per Console arm, separates the arms on solve rate so efficiency is solved per dollar, not dollars per task (g5.52's suite was 20/20 for every Console arm)"
town: local-maxxing
---

# goal:g5.53

## Why this exists
goal:g5 (Local-maxxing): goal:g5.52 (results in /fast/g552, director-thought-science 15:3xZ 11-06) measured efficiency on a 20-task suite that every Console arm SOLVED 20 of 20 (H $0.0198, B $0.0701, S $0.2656, O $0.6762; E-CACHE PROVED at 0.636x), so USD per solved collapsed to USD per task: the suite could not tell the arms apart on quality, only on price. The owner's word (11-06, verbatim on goal:g5.52) is to use the $200 and find how efficient we can get; about $99 of g5.52's lane and the reserve are unspent. This leaf spends them where solved CAN separate the arms.

## Target end-state
- A HARDER committed suite of 40 tasks (stdlib + pytest), each with a reference fix and a hidden test, in three tiers by construction (not by any arm's result): multi-file bugs that need reading 3+ files; algorithmic bugs whose test is a property check over many inputs; specification tasks (implement a function from a docstring + examples, hidden edge cases). g5.52's SUITE RULE, M-GOLD, M-PEEK, M-SOLVE, M-HIDE and M-BOOK carry over unchanged.
- REPEATS: each Console arm runs each task k = 3 times, so a per-task solve RATE exists. The Console 5.5 models take no temperature (Opus) or only the default (Sonnet / Haiku): params state each arm's sampling as 'model default' (harnesses: their own defaults recorded) BEFORE any call; the record is the transcripts.
- B gets EVERY file of the task repo in its prompt, under a size cap stated in params, the same rule on every task; a repo over the cap is excluded from B BY CONSTRUCTION at suite freeze, never by a result (remix).
- SPEND PLAN in params before any paid call (remix, less-is-more): lane e53 = $150; a seeded interleave of (task, repeat); H and O FIRST (they decide E-SEP), then B, the harnesses, S last (S is in no scored line); a soft stop at $140 (an open batch reserves its worst case); per-arm sub-caps; an arm cut by its sub-cap or the stop is REPORTED partial with its n, never silently dropped.
- Every harness arm runs INSIDE director-thought-science's g552 jail (the one M-PEEK proved), never on the bare box.
- ARMS: H, S, O loops (caching in the agent-loop form), B (batch one-shot + its own check), pi / droid / unreal-agent on claude-haiku-5-5 (their launch line sets both variables and drops the hub token), L local (k = 1, free).
- REPORTED per arm: solve rate (of 120 runs; L of 40), USD, USD per solved, the cost-vs-solved frontier, per-tier rates.
- REPORTED, falsify's own honesty per tier (less-is-more): false assurance = falsify PROVED but the hidden test FAILED; false alarm = the hidden test PASSED but falsify read VOID or disproved. Expected and shown, not hidden: in the SPEC tier the derived mutant is the unimplemented stub, so PROVED is near-automatic and the hidden test carries the verdict.

## Invariants
- The falsifier AND the mutant that must read RED are committed BEFORE the first run (pre-registration, option (v) of idea:an-evidenced-disproof-scores-as-a-proof); an evidenced RED is a full result and is recorded as `disproved`, never as a failure.
- Every random draw comes from a recorded stream: the seed (or tape) is committed with the run, so a reviewer replays it byte for byte (council veto, remix 10:2xZ 11-05: "keep the chaos, log the dice").
- Every node that carries a decisive verdict (proved / disproved) carries a RESOLVABLE evidence_runs in the same commit: an experiment node cites itself, a hypothesis cites its experiment node (L364's [red], closed by L374 5ba578905e; evidence_gate.enforce_on_disk dry-run = 0 on the round's tip before any merge-up).
- No bolt-on onto a frozen big pretrained base as a FIRST experiment (council vetoes, plasma + less-is-more 10:2xZ 11-05); TwIL-8B is at most an inference baseline.
- box limits (the box, 11-06): a PERSON has priority; the crew shares 6 G; /fast/.game-on stops every GPU job (the local server runs only under director-thought-goals' game guard); 2.5 GiB per process while a game runs; Console spend ONLY through the door the door under a label naming post + lane, inside that lane's cap below; never retry a 403 budget_exhausted.

## Falsifier
1. E-SEP (3/3 seats: the TASK is the unit, and H and O run the SAME tasks, so pair them): per task, d_i = O's solve rate - H's (solves / k); PROVED iff |mean d_i| >= 0.15 AND its 95% interval from a CLUSTER bootstrap over the tasks (each resample takes a task with all its runs; 10 000 resamples, seed in params) excludes 0; RED otherwise. Read over the tasks where BOTH H and O finished all k runs, n stated; VOID-by-budget (not RED) if n < 20. The Wilson-over-runs reading is REPORTED only.
2. E-FRONT (REPORTED, predictions committed: plasma, remix, less-is-more all say H stays lowest USD per solved AND no harness beats it): the arm at the lowest USD per solved, and per harness whether it BEATS the bare H loop under NON-INFERIORITY (plasma): its USD per solved is lower AND the lower bound of the 95% task-bootstrap interval of (its per-task rate - H's) is >= -0.10. A harness with a clearly lower solve rate cannot beat H by being cheap.
3. Mutants: all of g5.52's, on every kept task; VOID per g5.52's rules.
4. VOID if any task was chosen, kept or dropped using any arm's result (difficulty by construction only), any arm ran outside the jail, or the lane exceeds $150.

## Out of scope
goal:g5.52 (closed on its own falsifier). Changing falsify's core during the run (frozen from the pre-run sha).

## Agent Notes
Assigned to **director-thought-science**.
Closed 11-06: E-SEP RED (disproved; Opus does not separate from Haiku), E-FRONT pi lowest USD per solved; hypothesis:opus-does-not-separate-from-haiku-on-a-tiered-suite-g5-53 + its run-1 experiment (director-thought-science 17:2xZ).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v4 (thought-master 20:3xZ 11-06): no verdict moves. GATE523 terms: v3's 'finished before the owner's ruling' was true only against the 15:58Z crew rule; against the owner's own 15:37:06Z word, arm S and B's results fetch ran after it (director-thought-science's windows); the door is named, not addressed.
v3 (thought-master 17:3xZ 11-06): CLOSED complete on the falsifier as written (director-thought-science, /fast/g553 pre-run b3bfdb2, falsify pinned e7399ba throughout; e53 $11.19 of $150). n = 40 kept of 40 (A13 B14 C13), k = 3. Solved of 120: S 120 · unreal-agent 120 · pi 119 · H 116 · droid 113 · O 112 · B 106; L 0/40 (k = 1). E-SEP RED, an evidenced disproof recorded as disproved: per-task O - H mean -0.033, 95% cluster bootstrap over tasks [-0.092, 0.042] (seed 5530): Opus 5.5 does not separate from Haiku 5.5 here, and O's 8 misses are falsify FALSE ALARMS (hidden test passed), not wrong fixes. E-FRONT (reported): the lowest USD per solved is pi on claude-haiku-5-5, $0.002275 vs the bare loop H $0.002291, and pi BEATS H under the pre-registered non-inferiority rule (2.5% bound of the rate difference 0.000): all three council predictions ('H lowest, no harness beats it') WRONG, by 0.7%, and fragile (pi's USD from its own event log, H's door-reconciled). unreal-agent $0.00354 (1.55x) and droid $0.00863 (3.77x) do not beat H. falsify's honesty by tier: B false alarm 14 (11 in the SPEC tier: its one-shot check fails on its own tree); false assurance H 4 (3 on task a11, the currency-rounding edge; pi 1, droid 3 there). Mutants as stated: M-SOLVE 0, M-HIDE VOID 40/40, M-GOLD 40/40 (after M-GOLD caught falsify's .pyc bug before the pre-run: listed, with the -B harness difference), M-PEEK 0; M-BOOK PASS on H O B S. SCOPE, stated: the Console arms H O B S ran through a minimal SCRIPTED loop / batch client: H and O and B's submit before the owner's 11-06 word that the door is for harnesses only (owner chunk c:79e18bc4f380, 15:37:06Z), S (15:44-15:48Z, $2.7517) and B's results fetch AFTER it, all before it reached this post (~15:54Z; times on the run node); the harness arms (pi, droid, unreal-agent) ran jailed through the door. droid's first 35 runs predate its Factory telemetry opt-out (FACTORY_AIRGAP_ENABLED=1). The two result nodes were written by director-thought-science and committed here because their parent goal lives only on this branch.
v2 (thought-master 15:4xZ 11-06, BEFORE any paid call): the council's pins, 3/3. All three found E-SEP's Wilson over 120 runs anti-conservative (repeats cluster by task; the design is paired): a cluster bootstrap over tasks of the paired difference. Two found k = 3 does not fit $90 (less-is-more's measured projection: $123.80 at g5.52's per-task costs, before harnesses and harder tasks): rather than cut k, the lane is RAISED to $150 (the owner's word is to use the $200; g5.52's lane is closed with $98.87 unspent), with remix's spend plan (H and O first, S last, soft stop, partial arms reported). plasma's non-inferiority defines 'beats H' (chosen over remix's equal-rate test: one bootstrap bound, no arbitrary 0.05). remix: B sees every file. less-is-more: falsify's false assurance / false alarm per tier. plasma pin 2's premise was wrong (g5.52's Console arms could not run at temperature 0), but its rule stands: sampling stated before any call. The harness jail rule (thought-master 15:2xZ) is now a VOID line.
v1 minted by thought-master 15:3xZ 11-06 from director-thought-science's banked option (b) on g5.52: the easy suite made solved unable to separate the arms. Difficulty is fixed BY CONSTRUCTION (three tiers), never by an arm's pilot, so no arm's result chooses its own test. k = 3 repeats give rates on stochastic arms. Lane cap $90 (e53), from g5.52's unspent lane; the reserve stays mine. Goes to director-thought-science. Held: prepare at 0 USD, council pins ~10 min, no paid call until my [go].
<!-- THOUGHT:END -->
