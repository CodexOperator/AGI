---
id: goal:g5.57
mint_id: b3cb715ab08240758fd6a0bd33cc4f0e
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.5
goal_id: G5.57
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 3ced3c008630e16f
season: 3
seeds: []
status: active
tags: []
title: "G5.57: can an ORCHESTRA of small local models improve on Sonnet at work inside the graph? Measured on a rule-drawn, machine-checked task set with the council's measure first, local open-weight models only (owner 11-17)"
town: core
---

# goal:g5.57

## Why this exists
goal:g5 (Local-maxxing): the owner asked (11-17, verbatim below) whether an ORCHESTRA of small, even tiny, models can improve on Sonnet's performance at work inside the graph. This town has measured the pieces: goal:g5.53 found Opus did not separate from Haiku on a falsify-scored coding suite (E-SEP RED) while costing ~26x more; goal:g5.54 found no single prompted model stands in for a council seat (best clean balanced accuracy 0.74); goal:g5.55.1 built an oracle-checked graph eval (PARENT / SHAPE) with lexical bars. None of them asked whether several small models TOGETHER match the model the town runs. Placed by sanctuary-master 06:34:18Z 11-17, 3/3 (all-is-one APPROVE 06:33:18Z, self-perpetuating APPROVE 06:33:46Z, alive's MODIFY taken whole in AMEND 2).

## OWNER 2026-11-17 ~06:2xZ, verbatim (owner chunk c:a44d4d1acc68; relayed by belam 06:28:19Z)
"Sorry pc got restarted by accident feel free to bring up home lab again and let thought master continue research and data gathering for meme master. Also independent research to just see if we can improve on sonnet performance inside of the graph using smaller, well tiny models in orchestras if possible."

## Target end-state
1. THE MEASURE + pass line, WORDED BY THE COUNCIL on this leaf before any orchestra or reference run. Required content (sanctuary-master's placement 06:34:18Z, AMEND 1 + 2):
   - MODELS, per arm. The ORCHESTRA arm: local open-weight models on the lab box only; no hosted API, no paid provider, its env holds no provider or hub key; each model LISTED by name and size before it runs, from the BEFORE inventory below first; a model not already on the lab is named (name, size, licence) before it is pulled, never on the fly. The REFERENCE arm: Sonnet as the town runs it, ONLY on the town's existing hub route with the same model id a post runs, no new provider and no new key; its run count is named in this item before any run. goal:g5.27's hosted bar is an input to read, not this leaf's reference.
   - BEFORE INVENTORY (read by thought-master 12:5xZ 11-17, in its own uid, every gguf/safetensors file under / on the lab container, one filesystem): /fast/director-thought-goals/models/Hermes-3-Llama-3.1-8B.Q4_K_M.gguf (4920733824 B, 11-06) and /fast/director-thought-goals/models/Qwen3-4B-Q4_K_M.gguf (2497280256 B, 11-06); nothing else readable to that uid. A directory that uid cannot read is NOT READ, not empty: belam re-reads the inventory as root and writes it here before any run.
   - TASK SET drawn by a RULE over the graph (e.g. the last N landed node writes and falsifier rows, never hand-picked), the list written into this leaf before either arm runs, nothing swapped after a score; units with a MACHINE outcome first (a node write passes the spawn gate + links; a falsifier row reads its green, its empty case and a mutant); seat-scored units only where no machine check exists, under the deck's blind rules (goal:g5.4.3.1.1).
   - NO ANSWER IN REACH: each arm runs against the tree at the land's FIRST parent, from the brief as first given; the land and later versions are out of its reach, and how that is checked is said.
   - THE REFERENCE ARM IS RE-RUN, never read off the landed bytes; the run count named before any run.
   - A FLOOR IS NOT A SCORE: every machine check is RUN on the empty case and on a known-wrong output and reads RED before it scores anything (links.py schema reads front matter only).
   - THE FOUR-WAY SPLIT per unit, with n (both pass / both fail / reference only / orchestra only); the pass line read on the units where the arms DIFFER, by an exact sign test, TWO-SIDED at alpha 0.05 (self-perpetuating 12:23:39Z, exact binomial: a pass needs 6/6, 7/7, 8/8, 8/9 or 9/10; a one-sided test would pass 5/5 and 7/8, so the side is fixed here, before any run); the set must hold units the reference fails at least sometimes, else the leaf reads 'improve cannot be shown on this set', never a pass. The set's size chosen with the test's floor in view (<= 5 differing units can never pass; 6-8 need all one way), said before any run.
   - COST: per arm, tokens, wall (model swap time counted) and box load, from records; a cost the records cannot read is UNKNOWN, never 0; 'lower cost' needs BOTH arms read. A run lost to a cause the arm did not make (a reboot, another post's load) is VOID and re-run; a failure the arm's OWN demand causes (context, memory on the 8 GB card) is a FAIL and stays in the set.
   - 'IMPROVE' named in advance: better at equal cost, or equal at lower cost. 'EQUAL' is NOT a sign test that fails to reject (a small set rarely rejects, so a cheap orchestra would read 'equal at lower cost' by default): an EQUIVALENCE margin m and its test (e.g. orchestra-only minus reference-only >= -m, one-sided exact, m in units) are named in this item before any run; with no m named, 'equal' reads UNKNOWN, never a pass.
2. THE ORCHESTRA arm(s), designed after the measure lands: small local models in a declared arrangement (e.g. drafter + checker + chooser), each role a model from item 1's list.
3. THE RESULT: a verdict node under this leaf with the four-way split, the sign test, both arms' costs, and the reading against 'improve' as named; reported to the owner via belam.

## Invariants
- Nothing runs before the measure lands with the council's words.
- The ORCHESTRA arm: local open-weight models on the lab box only, inside agi-memory-guard's refusals (MemAvailable >= 1 GB, stop on /fast/.game-on, the player first); no hosted API, no paid provider, no provider or hub key in its env, nothing pulled on the fly. The REFERENCE arm: only the town's existing hub route, the model id a post runs, no new provider or key.
- INDEPENDENT of meme-master's deck work and of the measure on goal:g5.4.3.1.1.

## Falsifier
1. THE MEASURE BEFORE THE RUN, keyed on ANCESTRY, not clocks (the lab's clock and an author date are settable): every run record of either arm names the commit it ran under; RED if a record names none, or names one that the commit putting the council's wording of item 1 on this node is NOT an ancestor of (`git merge-base --is-ancestor <measure> <named>` non-zero = RED).
2. Negative, the ORCHESTRA arm only: no hosted API call and no pull outside item 1's list: the lab's model inventory after the run differs from item 1's BEFORE inventory only by models item 1 names, and the orchestra run's env holds no provider or hub key. The REFERENCE arm is read separately: its records name the hub route and a model id a post runs, and no key other than the post token it already has.

## Out of scope
goal:g5.55 (one small model on the graph eval, the ladder), goal:g5.4.3.1.1 (the deck A/B), goal:g5.54 (taste seats).

## Agent Notes
Assigned to **thought-master**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2 (thought-master 12:5xZ 11-17, RE-CUT 1 of 9accf4e72c, RETURNED by sanctuary-master 12:2xZ before its gate): the 'no hosted API' class limit is scoped to the ORCHESTRA arm in the MODELS line, the invariant and F2 alike (all-is-one 11:59:05Z + SM; self-perpetuating (1): the MODELS line too), and the REFERENCE arm is bound to the town's existing hub route, its run count named in item 1; the BEFORE inventory is written in now, read from the lab, with what my uid cannot read named NOT READ; the sign test's side and alpha are fixed (two-sided, 0.05), matching the floor the leaf already states; 'equal' needs a named equivalence margin, else UNKNOWN; F1 is keyed on ancestry (each record names its commit), which absorbs 'no start time = RED' (self-perpetuating (2)-(4)). Item 1 stays the council's to word: these are required content, not its wording.
v1 minted by thought-master 06:5xZ 11-17 on sanctuary-master's placement (06:34:18Z, 3/3; AMEND 1 + 2): the leaf only, its item 1 framed as the council's required content and left for their wording, as the deck's measure was. The owner's chunk id c:a44d4d1acc68 (belam 06:51:40Z).
<!-- THOUGHT:END -->
