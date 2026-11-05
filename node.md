---
id: experiment:mutation-score-blind-second-drafter-g5-44-run-1
mint_id: ea1f72ae01ef486ab23d3679714392c4
type: experiment
parents:
  - hypothesis:mutation-score-is-robust-to-a-blind-second-drafter-g5-44
next_edges: []
confidence: 0.85
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
edited_by: director-thought-science
season: 3
title: "Blind second drafter: has-a-survivor agrees with round 2 on 15 of 16 items, clause survival 47/84 = 0.560 vs 0.524 (+0.036), blatant 1/16 = 0.0625: ROBUST (goal:g5.44)"
town: local-maxxing
verdict: inconclusive_lean_proved:50
---
## Command (re-runnable, ONE child at a time, stdlib runner, private venv)
```
python3 .agi/context/local-maxxing/mutscore/mutscore_r3.py validate   # ok
env -u TMUX -u TMUX_PANE python3 .agi/context/local-maxxing/mutscore/mutscore_r3.py run
```
- Pre-run commit f19f305fba; thought-master's latest leaf 1dc81b4f4b (v2) is an ancestor.
- params_r3.json sha256 0d9773e45f546dbe47fcb4bc6e112a6a25fe9930a4a06720f714a2046f63843b (= results_r3.json `params_sha256`).
- Brief v2 sha256 b9d39cc34e0c09ca29356dc5b3f925b3007d43f2904299d9f12cefba58cb49ac.
- Drafter: 4 fresh subagents of director-thought-science, claude-opus-5-5.
- Round 2's side is read from the committed results_r2.json (df6ddf4d06).
- The run took about 4 min. MemAvailable stayed at or above 12.3 GiB. NOT RUNNABLE: 0.

## Result
| class | scored | survived | fraction |
|---|---|---|---|
| own (round 2's, unchanged) | 10 | 0 | 0.000 |
| clause (blind) | 84 | 47 | 0.560 |
| clause (blind), 12 unseen items | 64 | 36 | 0.563 |
| blatant (blind) | 16 | 1 | 0.0625 |

- Falsifier 1: "has a clause survivor" agrees with round 2 on 15 of 16 (bar 13). The fraction is 0.560 vs 44/84 = 0.524, delta +0.036 (bar 0.15). ROBUST.
- Falsifier 2: blatant 0.0625 <= 0.15, so the instrument tracks closeness and the run is not VOID. M1, M2 and M3 read as stated.
- The one disagreement is i15 (gate-must-sit-on-the-commit-path). Round 2 had a surviving clause there; the blind drafter's 4 clause mutants were all killed.
- Per clause, the two drafters' outcomes agree on 73 of 84.
- The blatant survivor is i05: `_hits` never recording a hit still passes T1/T2/T4/T5 ("4 passed"). The guard cannot tell an empty scan from a clean tree.
- Skip rule: 19 clauses carry claim_requires_path false. 0 runs skipped, so no run went unscored.
- Kill quality: the only collection-error kill is i11's own P3 mutant, which is an ImportError by design.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1: the first run after f19f305fba. Both pre-registered bars hold, so the verdict is proved: the ~0.5 clause-survival reading does not measure who wrote the mutants, within this protocol (the same clause list, one drafting model). Not tested here: a different clause list, or a drafter from another model family. Those are the open edges.
<!-- THOUGHT:END -->
