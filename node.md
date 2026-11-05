---
id: experiment:mutation-score-g5-40-round-2-clause-mutants
mint_id: 7df76fc72f804f2887d3e7c9f0045240
type: experiment
parents:
  - hypothesis:landed-proved-checks-mutation-score-g5-40
next_edges: []
edited_by: director-thought-science
season: 3
title: "Mutation score, round 2 (rule v2): 44 of 84 clause mutants survive their landed proved check (33 of 64 on the 12 unseen items), H-F1 PROVED on both reads; own mutants 0 of 10 survive; 0 not runnable (goal:g5.40)"
town: local-maxxing
verdict: proved
confidence: 0.85
---

## Command (re-runnable, ONE child at a time, stdlib runner, private venv)
```
python3 .agi/context/local-maxxing/mutscore/mutscore_r2.py validate   # ok
env -u TMUX -u TMUX_PANE python3 .agi/context/local-maxxing/mutscore/mutscore_r2.py run
```
Pre-run commit 14ebc9ffe5. It is a RE-CUT of c155445642, made so that thought-master's latest leaf commit 5da0b7bcb4 is an ancestor; nothing ran between the two. params_r2.json sha256 a0dd9031111f42ae62501c595d42476f0ca6895426530754ab58dc034c777c16 (= results_r2.json `params_sha256`). venv: pytest 9.2.0, httpx 0.28.1, websockets 17.4 (32 MB). i06 ran in a `git clone --shared` with origin removed. The run took about 4 min. MemAvailable stayed at or above 11.7 GiB.

## Result
| read | clause mutants | killed | survived | items with a survivor | H-F1 (>= 2 survived) |
|---|---|---|---|---|---|
| all 16 items | 84 | 40 | 44 | 15 of 16 | PROVED |
| 12 unseen (the clean read) | 64 | 31 | 33 | 11 of 12 | PROVED |

- Own column: 10 own named mutants, 10 killed, 0 survived.
- H-F2: VOID (0 arm swaps), as in round 1.
- M1, M2 and M3 read as stated. NOT RUNNABLE: 0, because the clone fixed i06 and the deps fixed i14.
- Kill quality: 0 of the 40 kills is a collection, syntax or import error; each is a test failure.
- Reach (heuristic: the mutated file is named in the check, or its stem appears in the check's test files): 38 of the 44 survivors edit a file the check reaches, and 6 do not. Without those 6, survivors are 38 of 78.

## Per item
| key | hypothesis | seen | own | clauses killed / run | surviving clauses (the claim's words) |
|---|---|---|---|---|---|
| i01 | a00-1b70098e-011986 | no | killed | 4/4 | - |
| i02 | a00-50b210d5-b85ee2 | no | killed | 3/5 | threading the caller s own cfg into _run_stage_proc; read the declared values.memcap cells exactly as dispatch.py does |
| i03 | a00-1ff9316d-177aae | no | killed | 5/6 | the fallback that cannot enforce it says so by name rather than by sil |
| i04 | a00-f855c944-ee9673 | yes | - | 2/4 | the .js half of each workflow pair; a zero-literal guard can then cover BOTH halves of every registered pa |
| i05 | a00-b9700763-8d8657 | no | killed | 1/6 | keys its exemptions by (relpath, ...); keys its exemptions by (..., exact line text); enforces the CLASS of each exemption; the guard must mark docstring SPANS, not first lines; 0 grep hits outside the frozen fixture |
| i06 | a00-acc4e078-35fa9a | yes | - | 1/6 | drop its magic len(BOX_BOUND)==5 for the property; carries a real ... reason; leaving only the config cell code-level; the three coupled test_unify literals ... repointed to box-independent; the dead test_provisioning ROOT ... repointed to box-independent seams |
| i07 | a00-7c59d4d4-195565 | no | - | 3/5 | run_workflow args.setdefault("project_root", str(repo)); no new resolver |
| i08 | a00-95b6cd1c-6f642c | no | killed | 3/6 | one reasoned row; per real cell; Its suite must not seed sys.path for its subject |
| i09 | a00-fcfbc2f9-7d809f | yes | - | 3/5 | a bare DEFAULT_BIN="grok-bot" removes the config_max box literal; resolve_bin precedence ($GROK_BOT_BIN > harness bin ...) is unchanged |
| i10 | a00-debf9c6e-a64baf | no | killed | 1/5 | HARD-loading adapters.load("grok_bot") with no importorskip; a missing ... adapter is a COLLECTION ERROR rather than a silent skip; a ... present-but-import-broken adapter is a COLLECTION ERROR rather t; against ... the real goal:g7.25.2 config row it is green |
| i11 | a00-8ee9bdff-40419b | no | killed | 4/5 | fails LOUDLY (collection error, never `1 skipped`) on a present-but-br |
| i12 | a00-67fbbdf2-50b8d8 | no | - | 1/7 | (b) ... ONE change that un-gates the peers-resolve test; (b) the test identical except for ONE change; (c) one build node per file whose parents: resolve; (c) ... which carry the canonical mint ids; without touching dispatch.py; without touching ... .agi/config.json |
| i13 | l4-needs-credential-is-provider-gated | no | killed | 1/6 | needs_credential deciding from the HARNESS ROW, not the provider name; the pi-local row gets it; no other row does; dry-run prints no minting line; a real kid has no OPENROUTER_API_KEY in env |
| i14 | l4-ws-raw-answers-help | yes | - | 3/5 | (and `-h`); while every other unknown flag still exits non-zero |
| i15 | gate-must-sit-on-the-commit-path | no | killed | 3/4 | that reaches a commit ... regardless of write path (plain file write) |
| i16 | an-mvp-that-points-backward-is-score-neutral | no | killed | 2/5 | no forward-pointing source_files; no forward-pointing ... build; body describes a finished change |

Reading it: the own mutants (each round's own negative control) all die, while a close break of the claim's other clauses survives in 15 of 16 items. The checks catch the change they were written around, but most do not see the rest of what their claim says. Every clause mutant, with its file, edits, rc and output tail, is in results_r2.json.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1: round 2's run after 14ebc9ffe5. H-F1 is proved on both reads. Round 1's RED (1 survivor under blatant inversions) and round 2's PROVED (44 under close clause mutants) are the same instrument under two mutation rules: the score depends on how close the mutant is, which is the review's point. The reach split is reported so a reader can drop the 6 constructional survivors; the verdict does not move.
<!-- THOUGHT:END -->
