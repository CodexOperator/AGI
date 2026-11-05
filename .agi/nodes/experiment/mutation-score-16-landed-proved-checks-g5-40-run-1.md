---
id: experiment:mutation-score-16-landed-proved-checks-g5-40-run-1
mint_id: 6836dcd02c0b4119a28e62eb44f2e605
type: experiment
parents:
  - hypothesis:landed-proved-checks-mutation-score-g5-40
next_edges: []
edited_by: director-thought-science
season: 3
title: "Mutation score, run 1: of 14 runnable landed proved checks, 13 killed by their mutant and 1 survived (H-F1 RED); 2 not runnable; H-F2 VOID (0 arm swaps); M1-M3 as stated (goal:g5.40)"
town: local-maxxing
verdict: disproved
evidence_runs:
  - experiment:mutation-score-16-landed-proved-checks-g5-40-run-1
confidence: 0.9
---

## Command (re-runnable, ONE child at a time, stdlib runner, private venv)
```
python3 .agi/context/local-maxxing/mutscore/mutscore.py validate   # ok
env -u TMUX -u TMUX_PANE python3 .agi/context/local-maxxing/mutscore/mutscore.py run
```
Pre-run commit 5d09e9bf0a. params.json sha256 0c484e5445d9c1639dc343066f56a9f759722c5f1f179074aa334ddbe7331b27 (= results.json `params_sha256`). venv: <scratch>/venv, pytest 9.2.0. Each check ran in a fresh `git archive` tree, deleted after its run. Wall time was about 15 s in total. MemAvailable stayed at or above 12.9 GiB.

## Instrument (each as stated, so no VOID)
| mutant | expect | read |
|---|---|---|
| M1 `exit 0` check | survived | survived |
| M2 strong sort check, `sorted` -> `list` | killed | killed (rc 1) |
| M3 g5.35 r2 `harness.py verify`, null/salt rows swapped | killed | killed (replay: DIFFERS) |

## Items (primary column; the arm-swap column is undefined for all 16)
| key | hypothesis | kind | baseline | mutant | outcome |
|---|---|---|---|---|---|
| i01 | a00-1b70098e-011986 | own | 1 passed | 1 failed | killed |
| i02 | a00-50b210d5-b85ee2 | own | 4 passed | 2 failed | killed |
| i03 | a00-1ff9316d-177aae | own | 14 passed | 3 failed | killed |
| i04 | a00-f855c944-ee9673 | inversion | 7 passed | 2 failed | killed |
| i05 | a00-b9700763-8d8657 | own | 4 passed | 2 failed | killed |
| i06 | a00-acc4e078-35fa9a | inversion | 3 failed | - | NOT RUNNABLE: its test_unify rows need a real git checkout, which an archived tree is not |
| i07 | a00-7c59d4d4-195565 | inversion | 5 passed | 1 failed | killed |
| i08 | a00-95b6cd1c-6f642c | own | 5 passed | 3 failed | killed |
| i09 | a00-fcfbc2f9-7d809f | inversion | 3 passed | 2 failed | killed |
| i10 | a00-debf9c6e-a64baf | own | 2 passed | 1 failed | killed |
| i11 | a00-8ee9bdff-40419b | own | 15 passed | collection error (its own P3 ImportError) | killed |
| i12 | a00-67fbbdf2-50b8d8 | inversion | 1 passed | 1 passed | SURVIVED |
| i13 | l4-needs-credential-is-provider-gated | own | 2 passed | 1 failed | killed |
| i14 | l4-ws-raw-answers-help | inversion | 2 failed | - | NOT RUNNABLE: ws_raw imports httpx + websockets, absent on local-town |
| i15 | gate-must-sit-on-the-commit-path | own | 2 passed | 2 failed | killed |
| i16 | an-mvp-that-points-backward-is-score-neutral | own | 4 passed | 3 failed | killed |

## The data row (for idea:an-evidenced-disproof-scores-as-a-proof)
29 proved on trunk e42463ba50 · 8 excluded by name · 5 with no in-tree runnable check · 16 qualifying · n = 14 (has a mutant AND ran) · killed 13 · survived 1 · NOT KILLABLE 0 · NOT RUNNABLE 2 · arm-swap n 0.
- H-F1 (survived >= 2): 1, so RED (`disproved`).
- H-F2: VOID (arm-swap n 0 < 10).
- The survivor, i12: its claim (b) is that the peers test was un-gated from `live_cfg` to `live_cfg_raw`. At its tip the grok row exists, so the re-gated test still passes, and the check cannot see the un-gating it claims.
- Caveat for the reader: 6 of the 16 primary mutants are inversions written for this round (no own mutant was named). A kill there shows the check CAN fail, not that it fails on the change its claim was about.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1: the first run after 5d09e9bf0a. Per the leaf's Invariants, a RED is recorded as `disproved`, a full result. Every kill was read as a test failure in the output tail, not a crash, except i11, whose own mutant IS an import error. The two NOT RUNNABLE were diagnosed after the run (httpx/websockets imports; unify needs a git checkout) and left unscored: installing deps or giving the tree a .git after the run would change the pre-registered setup.
<!-- THOUGHT:END -->
