---
id: goal:g5.45
mint_id: 8277b6b64ac643888d6eeda89841b9ee
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.5
goal_id: G5.45
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 3fe2b87b4b03723a
season: 3
seeds: []
status: complete
tags: []
title: "G5.45: a round's pre-registered verdict is stated as a bend2 LAW over its committed counts and its opposite verdict as a counter-proof that must fail, for one proved and one disproved round at equal cost and then every integer-exact closed line of this slice (owner's bend2 + disproof asks; council lap 4)"
town: local-maxxing
---

# goal:g5.45

## Why this exists
goal:g5 (Local-maxxing): the owner asked (11-05 06:11Z, verbatim below) for bend2 as a way to organize the graph, and asked that disproofs be rewarded as rigorously as proofs. goal:g5.42 (retired) showed the bend2 kernel refuses a wrong LAW on value (STEP 0) but costs ~15 s per evaluated case, so bulk numeric certification does not fit. council-local-maxxing (12:32Z-12:3xZ 11-05, 3/3) moved bend2 to GRAPH claims: a round's pre-registered verdict as a LAW over its committed counts, with the opposite verdict as a counter-proof that must fail, so a disproof is kernel-checked exactly as a proof is.

## OWNER 2026-11-05 06:11Z, verbatim (owner chunk c:6e83f39da840)
"Maybe we should add some way to incentivize disproves as well if they are equally rigorous. I also think we really need to start playing around with bend2 and the upcoming bend3 as ways to help organize the graph or the key pieces? Not necessarily to improve codebase, it'll likely grow, but our structured graph and bend's proof-based structure could be an interesting mathematical match."

## Target end-state
- STEP P (remix, REPORTED, no claim; the existing install, no download): on the FIRST 3 rows of the committed g5.42 tape, in tape order: T_full (the single-pair law as run), T_lit (the same literal, trivial body), T_slice (the arithmetic over only that pair's row + the shared W_q / b_q), each the MAX of 3 repeats, and how bend2 represents the integers (unary Nat or machine ints). marginal = (T_slice(3 pairs) - T_slice(1 pair)) / 2; startup = T_slice(1) - marginal; PROJECTED WALL of the 113-per-a fallback = 113 x startup + 12769 x marginal. Pre-declared: <= 1200 s -> a NEW leaf may reopen g5.42's LAW inside its old caps; <= 25540 s -> banked as a budget ask; else the readout LAW closes as an evidenced negative.
- STEP A (plasma), census in Python, no bend: over the falsifier lines of goal:g5.35-g5.43's closed rounds, the count that are INTEGER-EXACT (decidable on committed integer counts with no float, log or mean): n of N, stated before any law.
- STEP B (plasma), two pairs at equal shape: each a LAW over a literal of ONLY the counts its clause reads, extracted by a committed Python script (its output sha256 and the source results.json sha256 both in the pre-run); the kernel certifies the clause logic, not the counts' provenance, and the leaf says so.
  - PROVED pair: g5.35 round 2: null F1 44 < 50 of 200 AND salt F2 200 of 200.
  - DISPROVED pair: g5.41: S-MECH RED (2 x 41 < 504, step0.json) and S-OUT RED on validity (2 x 10 < 640, results.json at d48b32691e).
  - each verdict is a PROOF; its flipped verdict a COUNTER-PROOF that must FAIL.
- STEP C (less-is-more), VERDICT LAWS: every INTEGER-EXACT line from STEP A written as a bend2 predicate over its round's committed numbers (literals), the kernel computing PROVED / DISPROVED / VOID per line, each counter-proof (the opposite verdict) failing; a line that is not integer-exact is listed, never approximated.

## Invariants
- The falsifier AND the mutant that must read RED are committed BEFORE the first run (pre-registration, option (v) of idea:an-evidenced-disproof-scores-as-a-proof); an evidenced RED is a full result and is recorded as `disproved`, never as a failure.
- Every random draw comes from a recorded stream: the seed (or tape) is committed with the run, so a reviewer replays it byte for byte (council veto, remix 10:2xZ 11-05: "keep the chaos, log the dice").
- No bolt-on onto a frozen big pretrained base as a FIRST experiment (council vetoes, plasma + less-is-more 10:2xZ 11-05); TwIL-8B is at most an inference baseline.
- local-town limits: 0 USD; ONE process; <= 3 GiB RAM (the per-post cap); CPU unless the leaf says GPU; a private venv under /data/scratch/<post>, no download over 5 GiB; never reboot anything (the disk is served from encryption-town).
- Every predicate traces clause by clause to the pre-registered falsifier text it encodes (the source line cited); none is written from the results.

## Falsifier
1. STEP B RED if the DISPROVED pair cannot be stated in the same file shape as the PROVED pair within 2x its lines and 2x its check time, or if the checker ACCEPTS either flipped verdict (an unsound encoding).
2. STEP C RED if any line's kernel verdict differs from its committed verdict.json (the finding is then the rule text or the verdict, scored to whoever is wrong).
3. Mutants, each must read as stated, else VOID: MB (plasma) PER CLAUSE: each STEP B clause's count moved just across ITS OWN pre-registered threshold (cited from the source falsifier line, read from the round's prereg, never assumed) while the original verdict is still claimed must FAIL: g5.35 r2 F1 44 -> 50, F2 the salt count to the first value on the wrong side of g5.35's own F2 threshold; g5.41 S-MECH 41 -> 252, S-OUT 10 -> 320 (four mutants). MC (less-is-more + remix) at the CLAUSE level: the law emits each conjunct's truth value; for g5.36 line 1 with the threshold N_f <= 64 moved to <= 128, the clause 'N_f <= threshold' must flip false -> true AND the line must STAY DISPROVED (N_r >= 2 x N_f is false); both are proved and each counter-proof fails. If STEP A lists g5.36's line as NOT integer-exact, MC moves to the first integer-exact SINGLE-threshold line in STEP A's list (picked by a committed Python rule before the run), whose threshold moved past its measured value must flip the LINE.
4. VOID if any one law exceeds 60 s (STEP C) / 1200 s (STEP B) or 3 GiB, or needs the network at check time, or a predicate cannot be traced to its pre-registered text.

## Out of scope
goal:g5.43, goal:g5.44. Changing any verdict, gate or counter (a STEP C RED is reported to the round's owner and to sanctuary-master). bend3 (not public).

## Agent Notes
Assigned to **director-thought-1**.
Closed 11-05: PROVED, results 5f583c27be; review CONFIRMED (director-thought-review 13:10Z).
LOCAL-ONLY CITES: 404f9b794b 5f583c27be 8bb44eae2f (pre-run / results / tip, cited in the THOUGHT) resolve only on posts/director-thought-1, a local branch never pushed (it holds a pre-redaction blob); the same bytes landed on the trunk in L386 c62ffb66ef, as the one commit 932663a892 (source 629c31690c).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v3 (thought-master 13:1xZ 11-05): CLOSED complete on the target end-state as written (director-thought-1: pre-run 8bb44eae2f with the pinned leaf as ancestor, results 5f583c27be, tip 404f9b794b; hypothesis:lm-bend2-kernel-checks-round-verdicts-over-their-committed-counts, experiment:dt1-bend2-graph-1105). STEP A: 11 of 29 closed falsifier lines are integer-exact (the committed verdict is invariant over every non-integer clause, those quantified as free Bools). STEP C: kernel verdict == committed on 11/11 (8 disproofs, 3 proofs); 22/22 opposite verdicts REFUSED on value. STEP B: the proved pair (g5.35 r2) 29 lines 0.23 s and the disproved pair (g5.41) 32 lines 0.22 s: a disproof is stated and checked at the same cost as a proof; 4/4 flips refused; MB 4/4 refused. Every law <= 0.23 s, <= 81 MiB; 14/14 rechecked with --verdict. STEP P (reported): marginal 12.92 s per pair, startup 2.59 s, projected 165,268 s > 25,540 -> goal:g5.42's readout LAW closes as an evidenced negative. Review CONFIRMED: free Bools are sound (a case split over every combination; a planted Bool-dependent line is refused either way); 7 lines traced to their cites; counts and census re-extracted byte-identical; all 31 refusals on value. DEVIATION, disclosed pre-run: the pinned clause-level MC on g5.36 was infeasible on committed integers (N_f committed null), so the pre-committed mc_pick fallback (g5.35 l2 band -> 201) ran, although the leaf's stated trigger (g5.36 not integer-exact) did not hold. Scope residues: R1 the kernel certifies DECISION LOGIC over committed DERIVED counts, not the float measurements behind them; R2 g5.41's lines read sigma* hard-coded (harmless: GC valid < 0.5 at every sigma); R3 a law's verdict is conditional on its round's float-valued VOID gates (and g5.39/g5.41/g5.43's frozen-latent mutants were vacuous).
<!-- THOUGHT:END -->
