---
id: doc:card-belam
mint_id: ced15049ceb843b08e51cc50da416298
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: belam
scaffold_hash: 3388df8d4c85caa7
season: 2
tags:
  - card
  - prime
  - belam
thought_session: belam-S2-L5-XII
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs, never here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 12 first card. The traps that now live in a skill (merge-pass: 6 19 26 27 31 33 34 36 37 38 39; send: 1 25 29 41; rotate: 2 10; workflow: 8 9) are listed as skills instead of rows -- owner 01:1xZ 09-27: "everyone's card just lists all the relevant skills". Traps no skill carries (3 13 15 24 28 30 40 + the new 42) stay.
<!-- THOUGHT:END -->

## SKILLS — use the matching one BEFORE the flow (skills/agi-<flow>/SKILL.md; the Skill tool)
| flow | skill |
|---|---|
| CHECK · notice · PASS · trunk sync | `agi-merge-pass` |
| mint/edit a goal (schema inside) | `agi-goal` |
| any other node, build node, config:* | `agi-node-write` |
| dm · inbox · whois · wake | `agi-send` |
| rotate out · wake | `agi-rotate` |
| dispatch · judge | `agi-dispatch` |
| a review/research workflow | `agi-workflow` |
| verify a landing | `agi-verify` |

## §0 State (01:4xZ 09-27)
| | |
|---|---|
| post | belam-S2-L5-XII gen 12 · woke 01:28Z 09-27 · Opus 5.5 |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` · prime-root `.agi/worktrees/prime-root` · stream DOWN (HELD) |
| GUARD | OWNER GO 02:5xZ 09-27: model container brain-orcabonsai27b STOPPED (`docker start` restores) · docker budget 6656M -> 0 (guard.env.bak-20260927T*) · user@1000 high/max **12618M / 14021M** · agi-work.slice 9302M · sshd lane unchanged (reserve 1911M, ssh MemoryMin 64M CPUWeight 1000) · a pi stage ~210 MiB · load ~17/16 cores, io60 40-70 = the real bind |
| merge | **PASS 10 CLOSED 04:0xZ 09-27**: season2/main **2129f70bb** (two-parent merge of TIP 6c403aeb4b; posts.md field-merged) · local-maxxing/main ff -> 6c403aeb4 · 30 rounds: 29 accept_with_residue, 1 demote, 0 RED · state file: last_merged_town_sha = 6c403aeb4b · next PASS BASE = 6c403aeb4b |
| crons | CHECK f86b1cf9 "13 */4 * * *" (re-armed 01:3xZ) |
| spend | credits 8.74 USD (01:31Z) |
| dms | 03:0xZ [decision] -> TM: owner GO (DE cap 8 -> 12 -> 16 gated on load < 16 + io60 < 50; DT pause = TM's call; swarm-size test on TM's board) · 01:4xZ [decision] -> DE: hypothesis:wake-facts-collapse-to-skill-pointers (queued behind the redesigns) |
| branches | directors LOCAL-ONLY · thought-master ALONE pushes `local-maxxing/season2/main` · belam keeps `local-maxxing/main` + `season2/main` |

## §1 Plan
```
done   wake: card re-linked, CHECK re-armed · PASS 10 steps 0-3 (stamp, trunk sync 6c403aeb4, build, launch) · g4.18.2: 8 skills + nodes + links, HEAD line, CLAUDE.md trim, facts trim -> DE
next   g4.18.2 remainder: prime brief trim, other posts' cards pick up the HEAD line at their next write
HELD   OWNER 21:1xZ: stream · encryption-town config · sanctuary-master activation -- until messaging is done
open   SM seat (owner's go) · the wedge's trigger (unproven) · goal:send-is-hub-only-... has no goal_id/goal_kind (a renumber, on the owner's word) · §6
```

## §2 Landed (this seat): 045d1aab3 wake re-link · 6c403aeb4 trunk sync (belam gen 12 key row) · 3 commits for g4.18.2: skills (8 files + 8 build nodes [goal:g4.18.2, idea:engine-skill-doc] + .claude/skills links, gitignore narrowed) · 9b2f1e378 HEAD line + DE hypothesis · 786dd91da CLAUDE.md 26,597 -> 10,123 bytes · d11cfc027 Prime template 10,470 -> 7,698 · d94a59fca g4.18.2 byte budget · OWNER 01:5xZ: monitor.sh io guard FINE-GRAINED (kills only processes whose ancestor argv carries this pass's tag; others -> spared.log) · sshd lane verified live (ssh.service MemoryMin=64M CPUWeight=1000, system.slice MemoryMin=128M, guard: chain live) · skills block -> doc:unified-director-brief, doc:unified-master-brief, 3 duty briefs, the DE/DT/TM/SM cards

## 🔴 Where it stops
04:0xZ 09-27 belam-S2-L5-XII: PASS 10 closed + reported (TM [merge-up], DE [decision]); worktree prune done; guard at 12618/14021M
```
1. CHECK every 4 h (cron f86b1cf9, skill agi-merge-pass §1). Next notice when the trunk has new experiments past BASE 6c403aeb4b.
2. OWED to thought-master (my 03:5xZ YES): when TM names DE's draft node + range, run ONE write.py config:rotations 'replace body N:M <file>'
   -- keep test_rotate_templates.py:534's F16 hit (or DE re-pins in the same merge-up) and re-derive the facts first_turn range (rotations.md:76 + :114).
3. DE queue: dispatch-now hypothesis:reap-chain-members-get-their-full-term-grace-again (read 03:50Z) · then the redesigns · then the 7 PASS 10 defects (b5f2c2423).
4. Owner items open: TM's layout for DE concurrency (8 -> 12 -> 16, gated on load < 16 + io60 < 50) · DT pause = TM's call · swarm-size test on TM's board.
```
## §4 Traps (the rest live in the skills)
| # | trap | rule |
|---|---|---|
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 13 | the stream is LIVE (when up) | never print a secret, key, address or host name |
| 15 | a retire+move with a changed body shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 24 | the trunk push is thought-master's alone (owner 09-25) | belam pushes only `season2/main` + `local-maxxing/main` |
| 28 | after a reboot the seat row keeps the dead pid | `rotate._successor_row_write(...)`, commit posts.md by exact path |
| 30 | after a reboot heal re-spawns SOME seats | `reseat.py` from MAIN (transcript 82d56d5d) |
| 40 | F13's `/home/ubuntu/work/agi/.env` does not exist on local-town | the MAIN .env is `/data/work/agi/.env` |
| 42 | `write.py … 'replace body N:M'` refuses a range with no blank line around it (the HEAD's five diagram blocks are one "paragraph") | `--force` rides the SOURCE argument: `replace body N:M --force <file>`, after asserting the range; a refused replace in a chain still lets a later `thought` land -- check each line's result |

## §5 Verification: `links.py links` 0 broken · `snapshot-goals.py --render --check` · `commands.py run verify` (bin-suite-fresh FAIL known) · `~/work/.sanctuary/guard/guard-init.sh --status` + `tail ~/logs/memory-alarm-alerts.log`

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| 3 of 5 seats sit in session-73.scope, outside user@'s cap | spawn seats via `systemd-run --user --scope`, or cap user-1000.slice -- the owner's guard |
| guard follow-ups (TM 09-26): model rounds cannot fit user@'s high beside the seats; guard-init.sh 'last alerts' reads the old path | model loads in their own scope with MemoryMax (~6G); repoint 'last alerts' at ~/logs/memory-alarm-alerts.log |
| 2c leftovers (DE 07:39Z 09-26): exited session 710907bf + ~20 "Remote Control · offline" app rows | `claude rm 710907bf` if yours; app rows only from the app UI |
| stream-master's seat after the power cycle | re-seat only on the owner's explicit go (HELD 21:1xZ) |
| idle predecessors per rotation (owner chain rule) | reap on the owner's word |
| the origin remote moved (every push prints the new location) | `git remote set-url origin <new>` -- the owner's call |
| engine-wide config/template maxxing pass (owner idea, 09-23) | opening it is the owner's call |
| MIN_REMAINING_CREDITS hard-coded 1 USD (provisioning.py:103, :206) | a config cell (a director-engine round) |
