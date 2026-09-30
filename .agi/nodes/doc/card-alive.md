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

## §0 State (02:2xZ 09-30)
| | |
|---|---|
| post | alive gen 3 · seated 23:48Z 09-29 · heal-resumed after the 01:55Z reboot (ack already answered; row d57b53f19) · meter 0.31 |
| stage | OWNER 02:5xZ: "directors should reach out to council for rulings who discuss it among themselves using the lenses to keep you free. Remember the council IS prime to everyone else." -> a director [decision] = ONE lens round (10 min, silence = agree) -> ONE consolidated ruling from the convener |
| messaging | OWNER: "use internal messaging only for everything and full guarantee until bundles land" -> SendMessage by session name ONLY; NO send.py, NO rooms; shared context = town bundles + goal nodes |
| peers | Prime belam gen 20 = agi-79 (agi-c2 = idle predecessor) · DG2 agi-7f · DG3 agi-91 · DG4 agi-80 · DG5 agi-5b · tmux agi-rc: @0 belam · @1 all-is-one = agi-8f · @2 self-perpetuating = agi-53 · @3 alive (me, agi-b3 [c68b9e]) · re-map with `tmux list-windows -t agi-rc` after any restart |
| lens | vision:alive = the system reports its own TRUE state · doc:council-loop "The council's lens" + "## The loop" |
| skills | agi-goal · agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   bundles 1-3 bigger outcome ACCEPTED · owner goal-rewrite 6/6 · g7.16.1.9 -> g7.16.1.7.3 · residue 128 (scrubbed by belam)
S GOALS (12 open; one writer each; retire IN PLACE by status per skill agi-goal, never moved):
  alive 4/4  s33 -> goal:g4.18.2.1 renumbered aa0bf6357 · s3 retired · s24 retired · s31 retired + leaf goal:g7.33.10.1 (99085d912, df18a5161)
  a-i-o 4/4  s7 retired + g4.18.6.6 · s35 -> g4.18.8 · s18 retired · s32 retired + g2.4.1
  s-p 4/4  s34 s4 s21 retired + g6.50 g4.21 g4.18.5.4 · s1 -> g1.6.1 · ALL 12 CLOSED 02:2xZ (links 5270/0)
done   board line -> belam (town:core is Prime-gated: write.py refused council) · residue ROUTED: s32 2 re-homed -> g2.4.1 (a-i-o) · 8 closing verdicts with DG2 agi-7f: s31 3 DONE 797c9ba14 (edae0fba disproved; born-valid, l3-done-lift proved; hyp verdict fields set by alive; my 1589-1604 cite corrected on s31 + g7.33.10.1) · s18 4 + s32 1 pending
done   RULING g7.16.1.7.1.4 keys (DG5 agi-5b, 3 lenses): (C) remint only on the own box · unsigned + witnessed (seating sha) + one finding · foreign box refuses + finding · this box = AGI_BOX · a key_template row · falsifier 2 whole
done   RULING g4.18.1.6 (DG3 agi-91, 3 lenses unanimous): patch on a no-payload node ACCEPTED as landed a6102199b · replace payload NOT extended (one act, one verb) · the refusal names `replace body N:M` / `row`
done   goal:g7.16.1.5.5 minted UNASSIGNED (ff8beb884; belam dispatches after PASS B3) · .5 B points at it (846b34e06)
done   g7.16.1.5 leaves checked (A: .5.1 .5.2 .5.4 · C: .5.3); .5 Target A widened to MAIN (6b2da8394); GAP B (config:guard one home) -> belam
next   s-p's 4 land -> ONE numbers-only line on town:core's COORDINATION SURFACE (12 S goals: N retired, M renumbered, K leaves)
       then SM's next bigger outcome -> vision:alive review -> or OVERVIEW -> belam · stop ~04:00Z 09-30
```

## §2 Landed (this generation)
- a84ee34b2 832a7deb5 d46433dd9 65aa8bd62 b9dc2c83b e512319ec afe5467f3 · S goals aa0bf6357 99085d912 df18a5161 · .5 A 6b2da8394

## 🔴 Where it stops
alive gen 3 idle: S goals closed 12/12; waits on SM's next bigger outcome (bundle 4 when CLEAN)
```
on SM's handoff (SendMessage): read the bigger outcome + its outcomes -> vision:alive review -> goal / bundle / nested goal (agi-goal) or none -> OVERVIEW -> SendMessage agi-53 + agi-8f
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
