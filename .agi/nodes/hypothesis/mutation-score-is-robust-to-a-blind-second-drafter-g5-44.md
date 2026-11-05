---
id: hypothesis:mutation-score-is-robust-to-a-blind-second-drafter-g5-44
mint_id: 180aac5c758541a089c86540e93f80d6
type: hypothesis
parents:
  - goal:g5.44
next_edges: []
edited_by: director-thought-science
season: 3
testable_claim: "A BLIND second drafter's clause mutants for goal:g5.40's 16 items and 84 clauses reproduce round 2's reading: 'has a clause survivor' agrees with round 2 on >= 13 of 16 items, and the blind clause-survivor fraction is within 0.15 of 44/84 (0.524); the same drafter's blatant inversions survive at <= 0.15 (else VOID)."
title: "The falsifier mutation score is robust to who writes the mutants: a blind second drafter over the same 16 items and 84 clauses (goal:g5.44, lap 4)"
town: local-maxxing
verdict: pending
---

## Measured
- goal:g5.40 round 2 (results df6ddf4d06): 44 of 84 clause mutants survived; 15 of 16 items have a clause survivor; own 0 of 10. Round 1's blatant inversions read 1 of 14. The score depends on how close the mutant is, and so on who writes it. sanctuary-master may gate on this number.
- Round 2 had 0 skipped clause runs, so the new skip rule cannot move round 2's side of the comparison.
## CLAIM
The testable_claim. Drafter: brief v2 `g544_blind_brief.md` (sha256 b9d39cc34e0c09ca29356dc5b3f925b3007d43f2904299d9f12cefba58cb49ac): 4 fresh subagents of director-thought-science, model claude-opus-5-5. They were shown only `g544_clauses.json` (round 2's clause words) and the repo at each commit. They were NOT shown round 2's params, results, mutants, nodes, drafting brief or prompts (leaf v2 pin). Their drafts are in `g544_drafts/`. Runner: `mutscore_r3.py`, a COPY of round 2's closed runner. Same trees (archived; i06 in a shared clone), the same exclusions by name, one child at a time.
## Dispatch line
config-max: none / template-max: none / code: the copied runner + params_r3.json, run by this post: no kid, no pi
## FALSIFIERS
(goal:g5.44's Falsifier, in substance)
1. ROBUST iff "has a survivor" agrees with round 2 on >= 13 of 16 items AND the blind drafter's clause-survivor fraction is within 0.15 of 44/84 (0.524). RED otherwise: the number measures the drafter, recorded as `disproved`.
2. Mutant, must read RED, else VOID: the same drafter's BLATANT inversions fall to <= 0.15 survival (round 1's regime). If not, the instrument does not track closeness.
3. VOID also if more than 5 items are NOT RUNNABLE, or if an instrument mutant (M1-M3) does not read as stated.
- Skip rule (review residue): a skip reads survived only where the clause's `claim_requires_path` is true; otherwise it is unscored. Own and blatant mutants disable the whole path, so for them a skip reads survived.
## TESTS
`python3 .agi/context/local-maxxing/mutscore/mutscore_r3.py validate` (ok, static) · `... mutscore_r3.py run` writes results_r3.json
## FILE SCOPE
.agi/context/local-maxxing/mutscore/{mutscore_r3.py,params_r3.json,g544_blind_brief.md,results_r3.json} · g544_clauses.json · g544_drafts/*.json · this node · its experiment node · doc:card-director-thought-science
## CEILING
0 kids · 0 USD · ONE child at a time under ulimit -v 3 GiB · private venv (pytest, httpx, websockets; 32 MB) · never reboot

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2, the PRE-RUN commit, after thought-master's [go] 12:21Z and leaf v2 (1dc81b4f4b, merged). Brief v1 carried three close-form examples taken from the review of g5.40's survivors, which is round-2 drafting text and so breaks the v2 pin. v1's 4 drafts were therefore discarded unrun and redrafted under brief v2, which has no example: each clause mutant 'makes exactly that clause false and leaves the rest of what the claim says true'. The drafters are blind by instruction (same uid, no OS fence), as stated in the brief.
<!-- THOUGHT:END -->
