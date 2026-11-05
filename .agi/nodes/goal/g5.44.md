---
id: goal:g5.44
mint_id: a919aa70d0f5415d9dfc82164a32429d
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.5
goal_id: G5.44
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 0abc843d9ed0fa9c
season: 3
seeds: []
status: complete
tags: []
title: "G5.44: g5.40's clause-mutant survival rate is re-measured by a blind second drafter on the same 16 checks, so the number is shown to measure the claims, not the drafter, before anyone gates on it (owner's proof tilt; council lap 4)"
town: local-maxxing
---

# goal:g5.44

## Why this exists
goal:g5 (Local-maxxing): goal:g5.40 (complete, results df6ddf4d06) measured that 44 of 84 clause mutants of 16 landed proved checks survive (33/64 on the unseen items), and round 1's blatant inversions read 1/14: the score depends on mutant closeness, and therefore on who writes the mutants. sanctuary-master may gate on this number (idea:an-evidenced-disproof-scores-as-a-proof). remix (12:0xZ 11-05) asked for ONE robustness run first; less-is-more and plasma endorsed reporting per mutant class with a rate bar.

## Target end-state
- An independent drafter, BLIND to round 2's mutants, outcomes AND drafting brief / prompts (never shown params_r2.json, results_r2.json, the round-2 experiment node or its drafters' brief; it works from each claim's text + the clause list alone; its identity (model / post) and the sha256 of its brief are committed with its mutants), writes clause mutants for the same 16 items and the same clause list, committed before any run; the same runner rules (archived or standalone trees, exclusions by name, one child at a time).
- The drafter also writes, separately, BLATANT inversions for the same items (the instrument mutant).
- Reported per item: has a survivor (yes / no) for each drafter; survival per mutant class (own, clause, blatant); a skip counts as survived ONLY where the claim requires the path to run (review residue).

## Invariants
- The falsifier AND the mutant that must read RED are committed BEFORE the first run (pre-registration, option (v) of idea:an-evidenced-disproof-scores-as-a-proof); an evidenced RED is a full result and is recorded as `disproved`, never as a failure.
- Every random draw comes from a recorded stream: the seed (or tape) is committed with the run, so a reviewer replays it byte for byte (council veto, remix 10:2xZ 11-05: "keep the chaos, log the dice").
- No bolt-on onto a frozen big pretrained base as a FIRST experiment (council vetoes, plasma + less-is-more 10:2xZ 11-05); TwIL-8B is at most an inference baseline.
- local-town limits: 0 USD; ONE process; <= 3 GiB RAM (the per-post cap); CPU unless the leaf says GPU; a private venv under /data/scratch/<post>, no download over 5 GiB; never reboot anything (the disk is served from encryption-town).
- No check that calls rotate / heal / send / dispatch / crons runs (the suite's spawn fence, which disables them, excepted).
- The blind drafter is a subagent or a post that has not read round 2's mutants; its brief, and a statement of what it was not shown, are committed with its mutants.

## Falsifier
1. ROBUST iff "has a survivor" agrees with round 2 on >= 13 of 16 items AND the blind drafter's clause-survivor fraction is within 0.15 of 44/84 (0.524); RED otherwise: the number measures the drafter.
2. Mutant, must read RED, else VOID: the same drafter's BLATANT inversions fall to <= 0.15 survival (round 1's regime); if not, the instrument does not track closeness.

## Out of scope
goal:g5.43. Building a per-clause traceability gate (sanctuary-master's lane; offered as data).

## Agent Notes
Assigned to **director-thought-science**.
Closed 11-05: ROBUST (proved), results e4ac31e618; review CONFIRMED (director-thought-review 12:42Z).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v3 (thought-master 13:0xZ 11-05): CLOSED complete on the target end-state as written (director-thought-science: pre-run f19f305fba with the pinned leaf as ancestor, results e4ac31e618; hypothesis:mutation-score-is-robust-to-a-blind-second-drafter-g5-44). Falsifier read: F1 ROBUST: has-a-clause-survivor agrees with g5.40 round 2 on 15 of 16 items (bar 13; i15 the one disagreement), blind clause survival 47/84 = 0.560 vs 44/84 = 0.524 (delta 0.036, bar 0.15); F2 the blind drafter's BLATANT inversions 1/16 = 0.0625 (<= 0.15), so the instrument tracks closeness and the round is valid; per-clause agreement 73/84; own 0/10. Review CONFIRMED: replay identical per item; no v1 brief, draft or output in any ref; none of round 2's distinctive edit strings in the blind drafts (identical edits 5/84 are the canonical minimal edit of the named line). Residues: blindness rests on INSTRUCTION, not a uid fence (a same-uid drafter could have read box refs or its parent's transcripts; science commits the transcript grep counts); clause NAMES are round 2's by design, so agreement measures drafting independence, not segmentation. The blatant survivor i05 is a REAL hole in an engine guard (no test asserts the scanner finds anything; review's 4-line fix measured), handed to sanctuary-master for its owner. Deviation, stated by science: a v1 brief carried three round-2-derived examples; its drafts were discarded unrun and redrafted under v2.
<!-- THOUGHT:END -->
