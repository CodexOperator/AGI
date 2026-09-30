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

## §0 State (04:4xZ 09-30) -- IDLE at the council STOP (belam: "finish the step, card whole, idle")
| | |
|---|---|
| post | alive gen 3 · session agi-b3 [c68b9e] (heal-resumed after the 01:55Z reboot) · meter ~0.38 |
| role | the council IS prime to the directors (owner 02:5xZ): a director [decision] -> ONE lens round (10 min, silence = agree) -> ONE consolidated ruling from the convener |
| messaging | OWNER: "use internal messaging only for everything and full guarantee until bundles land" -> SendMessage by session name ONLY; NO send.py, NO rooms; town nodes are Prime-gated (write.py refuses council) |
| spend | OWNER 04:5xZ (SUPERSEDES 03:2xZ): "Let's switch your reviews and stuff to sonnet 5.5, and all subagents can be sonnet 5.5 as well to free up the free lane" -> every subagent + review on Sonnet 5.5 (Agent tool model: sonnet); workflow.py runs stay pi-free until its headless claude-code route lands. PASS IT to agi-53 + agi-8f at the council's next wake (belam asked). Was, OWNER 03:2xZ: "Directors spawning a lot of agents. Please make them use pi for agentic subtasks or sonnet 5.5. Were also out of usage" -> no Opus subagents; pi-free or Sonnet 5.5 at most |
| peers | Prime agi-79 · self-perpetuating agi-53 · all-is-one agi-8f · DG1 agi-2a · DG2 agi-7f · DG3 agi-91 · DG4 agi-80 · DG5 agi-5b · re-map after a restart: `tmux list-windows -t agi-rc` + ListAgents |
| lens | vision:alive = the system reports its own TRUE state · doc:council-loop "The council's lens" + "## The loop" |
| skills | agi-goal · agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   bundles 1-3 bigger outcome ACCEPTED (0.8 -> 0.65 after residue 128) · owner goal-rewrite 6/6 · g7.16.1.9 -> g7.16.1.7.3
done   S goals 12 -> 0 open (9 retired in place · 3 renumbered · 6 remainder leaves); board line placed by belam
       residue: 10 pending hyps under retired s18/s31/s32 -> s32 2 re-homed to g2.4.1; s31 3 CLOSED (DG2 797c9ba14; fields set c00a3960a); s18 4 + s32 1 with DG2
done   .5 leaves checked · .5 A widened · goal:g7.16.1.5.5 = one memory-budget home + the RAM disk's OWN line (3aa03292b); belam assigns to DG5 on the next engine oomd kill or when B3 lands
done   RULINGS: g7.16.1.7.1.4 keys (DG5: (C) own-box remint, unsigned+witnessed+finding, foreign refuses, AGI_BOX, template row)
               g4.18.1.6 (DG3: patch accepted; replace payload NOT extended; residue 154 = (b) refuse on canonical drift, never "updated" on no-op)
               g4.18.6.2 (DG1: (b) closed; body refs -> g4.18.6.4, declared regions only, one definition) -- applied + verified
next   after the stop: SM's bundle-4 BIGGER_OUTCOME -> vision:alive review -> goals / bundles / nested, or none -> OVERVIEW -> belam
       open watch: DG3 closes g4.18.1.6 on a clean SM run 25; DG2's 5 closing verdicts (s18 4, s32 1)
```

## §2 Landed (this generation)
- a84ee34b2 832a7deb5 d46433dd9 65aa8bd62 b9dc2c83b e512319ec afe5467f3 d57b53f19 · S goals aa0bf6357 99085d912 df18a5161 c00a3960a · .5 6b2da8394 846b34e06 · .5.5 ff8beb884 b50cc8913 3aa03292b

## 🔴 Where it stops
alive gen 3 IDLE at the council stop: every ruling delivered, nothing in flight; resumes on belam's word or a director [decision]
```
on SM's bundle-4 handoff (SendMessage): read it + its outcomes -> vision:alive review -> goal / bundle / nested goal (agi-goal) or none -> OVERVIEW -> SendMessage agi-53 + agi-8f
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
| hypothesis verdict | set `evidence_runs [experiment:...]` WITH `verdict`, or the grid evidence gate demotes it (s31 x3, fixed d3ec89831) |
| write.py `set` | `set key value` (a space, never key=value); a dotted value like G7.x breaks key=value |
| replace body guard | a range must start/end on a heading or blank; to keep a THOUGHT, replace up to the line before it or carry it in the file |
| .agi/sessions/quorum/alive.md | a SYMLINK to this node (re-link at wake if rotate flattens it: agi-rotate §3) |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (5301 at 03:1xZ) · S goals: complete 22 · retired 10 · active/horizon 0

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| row R live cutover (restart drops every post) | the Prime gen 17: dummy proof GO; live step = owner's word after PASS B3 (doc:card-belam §6) | step 1 at the cutover commit: `env AGI_LIVE_SYSTEMD=1 python3 -m pytest extensions/agi/tests/test_rotate.py -k test_r1_cutover_dummy_one_kill_is_one_post -q`; no pass line = (a) restart, never (c); form = GROUPED Delegate=yes scopes (R1 v3 b2d946498) |

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.


<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Whole rewrite at the council STOP (belam 04:4xZ 09-30: "finish the step, card whole, idle"). Since the last whole write: the 01:55Z reboot (heal-resumed, same session), the owner rules "the council IS prime to everyone else" (directors bring rulings to the council) and "use internal messaging only", the S-goal retirement (12 -> 0 open), four director rulings, .5.5 grown with the RAM-disk budget line, and the owner usage order (pi or Sonnet 5.5 only). Two of my own slips are named in the traps: guessed future stamps (corrected afe5467f3) and a citation DG2 corrected (c00a3960a).
<!-- THOUGHT:END -->
