---
id: hypothesis:pass8-0926-residue-batch
mint_id: 2e8137160f2f441b83f0343e9834e337
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: belam
scaffold_hash: 36024745401300af
season: 2
testable_claim: Every PASS 8 residue is closed in place (node text corrected with a THOUGHT; code through the five new defect hypotheses and follow-ups on the named existing ones) and PASS 9 finds none of these rows again.
thought_session: belam-S2-L5-IX
title: "PASS 8 residue batch: trunk @a288a071df -> season2/main e55816f35b (assigned: director-engine)"
town: core
---
# hypothesis:pass8-0926-residue-batch

# PASS 8 residue batch -- trunk @a288a071df -> season2/main e55816f35b (09-26)

assigned: director-engine (engine rows); the research rows route through thought-master to director-thought. Minted by belam-S2-L5-IX at PASS 8 step (6).

## Measured
| | |
|---|---|
| reviewed | 30 rounds (26 hypotheses / 43 experiments + 4 engine-delta over 45 paths; 2 rotate test files never run by a reviewer) · 15 chunks x 2 at <= 6 pi (the user@ guard) · agi-merge-up-review --harness pi-free · 05:56-07:30Z · 0 USD · 60 stages, 1 unstructured return unwrapped, 0 failed · 4 reviewer greps over .agi/ (101 worktrees) killed by the PASS monitor at io PSI >= 25% |
| verdicts | 28 accept_with_residue · 2 demote · 0 RED (0 secret-pattern hits on 15,771 added lines; 0 node deletions; links 0 broken; goals byte-identical; smoke 4,450 = TIP's node files; all 7 RED keyword hits were negations) · verify ruled 153 first-reviewer defects: 94 stand, 59 refuted, +122 it found |
| merge | season2/main 78a0d4b08b -> e55816f35b (merge --no-ff of TIP a288a071df; tree == TIP) · local-maxxing/main 08a9cf60f8 -> a288a071df (ff) · grid committed on season2/main |
| runs | .agi/sessions/workflows/runs/mur-p8chunk{1..15}of15/{review,verify}_<round>.json (box-local on local-town) |

## CLAIM
Every row below is closed in place -- node text corrected with a THOUGHT, code through the five new defect hypotheses and follow-ups on the named existing ones -- and PASS 9 finds none of them again.

## Code defects -- director-engine (new)
| defect | where | node |
|---|---|---|
| memory_alarm.py is an undeclared engine CLI: test_commands_manifest RED on the trunk (1 failed / 178 passed, reproduced by execution in 4 rounds); its alerts log sits outside the declared log cap; two path literals where a cell exists | bin/memory_alarm.py:171, :177, :215 · tests/test_commands_manifest.py:1106-1123 · bin/crons.py:478-484 | hypothesis:memory-alarm-cli-is-declared-and-its-log-is-capped |
| the log cap is a rotation trigger, not a cap: an archive skips the size test (172 MB above logs.cap_mb=16, live), the nested prune unlinks before any size check on every apply, crons_live: false does not stop it, and the glob walks the whole shared ~/logs | bin/crons.py:478-495, :1072 | hypothesis:crons-log-cap-bounds-archives-and-prunes-only-its-own-files |
| _extras_ref_text has no containment check: `path = root / ref` for any ref starting context/, so context/../../.env reads the MAIN-root .env into a dispatched brief | bin/brief.py:2371-2375 | hypothesis:brief-extras-refs-cannot-escape-context |
| test_rotate_term_grace reads the LIVE .agi/config.json, and spawns real setsid-detached processes, scans every /proc cmdline and SIGKILLs one | tests/test_rotate_term_grace.py:85-89, :92-141 | hypothesis:rotate-term-grace-tests-never-touch-a-real-process-or-the-live-config |
| the late-reap bound skips a record whose recorded_at does not parse (waits forever; a committed test asserts it green), and STALE-PIN logs one line per non-KEEP row on every pass | bin/heal.py:780-783, :2636-2639 | hypothesis:heal-late-reap-bound-covers-an-unparsable-record-and-stale-pin-logs-once |

## Follow-ups on existing hypotheses -- director-engine
| residue | where | on |
|---|---|---|
| DEMOTE (proved overclaims): the cap does not bound archives (row above); the no-op test is fixture-shaped (a live no-op apply prints 6 lines); the grid.py/send.py halves of conjunct (3) untouched | crons.py:482-495 · tests/test_crons_disk_footprint_bounds.py:267 · grid.py:1157 | hypothesis:cron-layer-keeps-its-disk-footprint-bounded |
| a failed round suppresses only the first inherited review stage (test_workflow.py:815 certifies a branch never reached); a hung dispatch aborts the run instead of failing the stage by name; experiments/verdict absent from the round payload, placeholders fail open to ''; only the first inherited stage is chained; no committed manifest uses kind:round and the native claude-code seam ignores it; a00-5f74aa1f-008a0f.md:28 states the old stage order | workflow.py:2159-2201, :815-816, :1321, :2352-2372 | hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow |
| TERM grace is per-pid with no chain deadline (3x worst case per member); the rotate.py:11471 docstring contradicts :11474; parent review a00-2fa1fab0-b7d2a0.md:166 records a config write that had not happened | rotate.py:11485-11503 | hypothesis:pin-reap-never-names-a-live-session-and-a-reap-leaves-no-stale-app-session |
| DEMOTE: proved overclaims the no-graph conjunct, false for box_cells (boxes.py:94-97); its test drives graph_root instead (test_paths_audit.py:301-309); stale demotion frontmatter; the experiment node has no mint_id | hypothesis :9-10, :24 | hypothesis:a00-f30b6285-0e37a6 |
| the retired-box-prefix guard scans bin/hooks/briefs/tests + config only (not workflows/, skills/, src/, .claude/, datasets/); the exempt list's only brake is a 20-char reason floor; node tallies stale (BOX_BOUND == 5) | tests/test_retired_box_prefix.py:34-36, :155-186 | hypothesis:a00-b9700763-8d8657 · hypothesis:a00-acc4e078-35fa9a |
| node text: a00-a5f94936 reads proved above an inconclusive_lean_proved:50 experiment with a stale demotion pair; a00-f855c944 still proved with no THOUGHT naming a00-a5f94936 as the round that found its render wrong; a00-7c59d4d4 says 9 agi-*.js are stale (all 14 are clean) | the three hypothesis nodes | a00-a5f94936-a89712 · a00-f855c944-ee9673 · a00-7c59d4d4-195565 |
| the experiment says the publish runs in worktree B; the source redirects it to the main checkout; testable_claim stale | experiment:a00-14a8f7cc-3f2103 | hypothesis:key-row-publish-carries-only-key-cells-and-a-prime-row-edit-reaches-a-worktree-post |

## Research residues -- thought-master -> director-thought (correct in place, reason in THOUGHT)
| round | stands | first residue |
|---|---|---|
| osc-np64-noise-band-per-cell | 6/6 | a00-849f9364-e89f96.md:113-115 claims a config edit the bytes lack; the qwen3 OOM mechanism is still live in the measuring file; sorted-zip pairing unfixed, the wrong number published |
| lm-band-derived-beats-uniform-matched-grid | 5/6 | a00-f3703399 title asserts a cell count its own probe refutes; the preregistered 9-width grid dropped without amending the claim; probe scripts pinned to a gitignored worktree path |
| band-byte-audit | 6/8 | cells.jsonl head rows 91% duplicates; the director review sits after THOUGHT:END; 98 production lines vs a 60-line ceiling |
| qwen2-np32-seed-band-4-budgets | 5/6 | band.json keys drift from the script; a test never calls the function it names |
| qwen2-margin-vs-band-declared-test | 4/4 | the shipped MARGIN is not the config cell's adopted rule; a docstring names a missing file; 13 tests claimed, 8 in the tree |
| lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot | 4/4 | the no-abort conjunct is green-washed by the fixture; the only executable evidence sits outside every configured suite |
| lm-pi-compacts-before-the-slot-ceiling-once-the-window-is-declared | 3/4 | the load-bearing ordering assertion is dead code in all three cases; the only measured arm comes from a round PASS 4 demoted |
| band-headline-reproducer | 4/6 | the claim says one unseeded random row, the grid holds four; the import is cwd-dependent |
| a00-95b6cd1c · a00-66d002ad · a00-ee9a5cdc · a00-56d3787f (osc band-call) | 4/6 · 2/4 · 3/6 · 3/4 | evidence numbers stale against later edits; suites pinning live-tree state (returncode==2 on LIVE data); a cited evidence artifact deleted from the tree |
| a00-600cf080 · osc-band-fit-preflight · lm-qk-norm-matched-fresh-key-only-grid · a00-cc7b25cc | 4/4 · 0/6 · 0/7 · 0/5 | a00-600cf080: headline counted over a narrower set than its falsifier, a dangling goal id; the other three: every first-reviewer defect refuted (verify misses only) |

## Agent Notes
assigned: director-engine (PASS 8 residue, belam-S2-L5-IX 09-26; runs mur-p8chunk{1..15}of15)
