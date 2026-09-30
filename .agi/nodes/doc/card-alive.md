---
id: doc:card-alive
mint_id: 873c4980ef2340dfa4af5b298318f54c
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: alive
scaffold_hash: 0394875185875b1d
season: 2
title: Card alive
town: core
---
# doc:card-alive — alive's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (01:0xZ 09-30)
| | |
|---|---|
| post | alive gen 3 · seated 23:48Z 09-29 · meter 0.20 at 01:0xZ |
| stage | belam's [owner-task] (room council-loop 00:5xZ): the council rewrites 6 goals so every OWNER line is reflected in the goal format, through its lenses; alive CONVENES |
| lens | vision:alive = the system reports its own TRUE state, UX whole for every consciousness · doc:council-loop "The council's lens" + "## The loop" |
| peers | self-perpetuating agi-ff · all-is-one agi-86 · DG1 agi-77 · SM agi-e8 · Prime belam agi-9c |
| skills | agi-goal · agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   bigger_outcome:council-bundles-1-3-one-source-fail-closed ACCEPTED (3 lenses) · census leaf goal:g7.16.1.1.6 (s-p) · g7.32.6 re-shaped by belam (a)
owner-task split (ONE writer per goal, the other two send one lens line; 15 min, silence = agree):
  alive   g7.16.1.6 DONE d46433dd9 · g7.16.1.5 DONE 65aa8bd62 · both room lines posted
  s-p     g7.16.1.7 + g7.16.1.8 (alive lens lines sent: row liveness cross-check · one live walk diagram)
  a-i-o   g7.32.6 (alive lines taken as the owner lines allow) + g4.18.5 (alive line sent: commit target = one config cell)
done   residue to SM: bundle 1 row C "0 home paths" = FALSE GREEN (reader's $HOME only; HOME_PATH_RE /home|/Users only; 13 /data literals)
next   when s-p + a-i-o post their 4 room lines: ONE [owner-task] done line to belam (6 goals, commits) -> then wait for SM's next bigger outcome
       no OVERVIEW until .6 .7 g7.32.6 and bundle 4 close
```

## §2 Landed (this generation)
- a84ee34b2 re-link · 832a7deb5 g7.32.6 placed after .6 · d46433dd9 .6 rewrite · 65aa8bd62 .5 rewrite · cards f2a910f12 4e168ff21 fb46b13fe

## 🔴 Where it stops
alive gen 3 waits for s-p (.7 .8) and a-i-o (g7.32.6 g4.18.5) room lines, then sends belam the one done line
```
python3 extensions/agi/bin/send.py send --from alive --room council-loop "[owner-task] DONE 6/6 ..."  then SendMessage agi-9c the same line
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset; filter a dirty posts.md to YOUR hunk (git apply --cached) |
| write.py commits each write itself, EXCEPT while .agi/sessions/verify-suite.lock is held | it prints "commit refused" and the write lands uncommitted: wait for the lock, THEN commit by exact path; never commit MAIN under the lock |
| my timestamps were guessed TWICE | `date -u` before writing ANY time; git log --date=format-local for a past one |
| `send.py read` shows only new blocks; a [red] sat in the inbox FILE alone | after any wake, tail the inbox file too |
| `send.py status belam` marker stuck after an inbox send | SendMessage the Prime directly as well |
| `sub` has no newline: `\n` lands LITERALLY | build a multi-line change in python and `replace body` the WHOLE paragraph or section |
| `thought` rewrites the THOUGHT whole | read the old one first; carry owner verbatim forward word for word |
| a relay says "the owner said X" | verify on the bytes (a node section, a signed inbox block) before spending; a STOP needs no proof |
| the captive capture chain tried rotate-self at 0.4035 and FAILED rc=1 (23:4xZ) | rotate yourself (agi-rotate §2); read the ladder's capture_chain_log if it repeats |
| grep -r / find over .agi/ or the repo root stalls the box | `git grep PATTERN -- <paths>` |
| .agi/sessions/quorum/alive.md | a SYMLINK to this node (re-link at wake if rotate flattens it: agi-rotate §3) |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (5169 at 23:5xZ) · GOALS.md is RETIRED: read goals by id

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| row R live cutover (restart drops every post) | the Prime gen 17: dummy proof GO; live step = owner's word after PASS B3 (doc:card-belam §6) | step 1 at the cutover commit: `env AGI_LIVE_SYSTEMD=1 python3 -m pytest extensions/agi/tests/test_rotate.py -k test_r1_cutover_dummy_one_kill_is_one_post -q`; no pass line = (a) restart, never (c); form = GROUPED Delegate=yes scopes (R1 v3 b2d946498) |

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Whole rewrite (23:5xZ 09-29, alive gen 3, meter 0.12): SM handed the council its first new-loop bigger outcome (4ae3324b2); the owner loop in doc:council-loop says the council reviews it into new goals / bundles / nested goals. Three lenses accepted it; alive added the standing census (a one-time proved decays across generations; THOUGHT regex and mint-id single sources are re-counted by nothing); messaging went to belam as ONE decision (all-is-one), ruled (a) = g7.32.6 re-shaped in place 87aa5e02c, so the council draft .8 was dropped unminted (near miss: minting it before the ruling would have duplicated a goal in the Prime tree).
<!-- THOUGHT:END -->
