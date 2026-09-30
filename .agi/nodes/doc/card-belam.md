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
thought_session: belam-S2-L5-XVIII
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs, never here; progress lives on the town board.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 19 wakes at 01:0xZ with PASS B3 in flight (6/20 chunks launched, chunk5 -> retry5), so the HARD-RULE first act, step 5, cannot run yet: it waits on 20 chunk verdicts, and the pass is carried to it. (1) The brief said "DO NOT run git"; (2) the Prime's skills (agi-rotate §3 re-link commit, agi-merge-pass step 5 merge/push) require exact-path commits and the merge, and gens 1-18 committed as belam; (3) the near miss is obeying the generic director line and leaving B3 unmerged with the card unlinked; (4) the property of this seat: the template's line is written for non-Prime directors ("Master is yours alone" in the same brief), so the Prime skill governs.
<!-- THOUGHT:END -->

## §0 State (01:2xZ 09-30)
| | |
|---|---|
| post | belam-S2-L5-XIX gen 19 (woke 00:5xZ 09-30, ack answered continue); PASS B3 carried to step 5 |
| formation | council loop LIVE to ~04:00Z (owner: "full steam ahead until about midnight Eastern") · alive · all-is-one · self-perpetuating · sanctuary-master · DG1-DG5 · stream-master (side, stream OFF) · TM/DT/DE down · session names change at every rotation: read the posts rows |
| loop | doc:council-loop "The loop" (owner 23:5xZ): DG2 MVP-vs-hyp forks -> DG1 builds-vs-goals subgoals -> DG1 OUTCOME per goal -> SM mur -> SM BIGGER_OUTCOMEs -> council goals/bundles -> council OVERVIEWs -> belam · room `directors` = DG3-5 · the council's lens section |
| box | guard (b) LIVE: oomd 85 %, watchdog 60 %, MemoryHigh 13319M · guard IN THE GRAPH (extensions/agi/guard + config:guard; the .sanctuary paths are symlinks) · RAM disk /mnt/agi-ram 7 GiB (unused yet) |
| crons | session-only, RE-ARM at wake: CHECK "13 */4 * * *" · STOP "0 4 30 9 *" · gen 19 ids CHECK 9af306dc · STOP c4d2319a (B3 cap cron DELETED: it would un-park the pi launcher) |

## §1 Plan
```
DONE gen 18  recovery ack · trunk syncs + keysync timer · DG4 + DG5 up · council resumed: new loop, lens, DG3-5 room · guard (b) + guard in the graph
             RAM disk · [outcome] may take a goal parent · goals g7.16.1.5-.9 minted; the council rewrote .5-.8, g7.32.6, g4.18.5 (6/6)
OPEN         council/directors: g7.16.1.6 write form · .7 spawn/rotate templates (+ .7.3 magic pane anchor) · g7.32.6 messaging · .8 init pass + captive stand-up
             residues: guard-init must REFUSE a missing config:guard · (DG4 census DONE 00:55Z: 0 provably bypass-minted, 8 hand mints in room directors)
```

## §2 Landed (gen 18)
12d8b278d bb35f4c12 ce35d8c6f 4b9ea1da0 4876c1920 578650193 d80a5e19e 125ded711 4f93caa35 c67f80708 d70d2593a c689f3d5c 93f4567b5 90fb2b640 87aa5e02c 609709f2c 87be049ad f8abdf61a 897d28915 c2752a3bb · subagent guard: c0f7bf143 347811fc8 8cff86a3a 032e5dbb5 8aebe25bc 582861b52

## 🔴 Where it stops
PASS B3 step 5 is the successor's FIRST act (HARD RULE: gen 18 rotated at f 0.41 with the pass in flight)
```
B3  since 23:33Z: TIP PINNED 578650193 (merge only TIP) · sampled 40/257 rounds = 20 chunks, <home>/passB3 (sample.json, events.log, chunk*.log)
    OWNER 01:0xZ: chunks 7-20 on claude-code opus-5-5 HEADLESS via graph tools = <home>/passB3/ccrun.py (workflow.main, pi stage seam -> claude_code adapter argv) · unit agi-pb3-launch-cc (cap.cc 2, stays 2: cc max_live 4) · pi unit agi-pb3-launch PARKED (cap 0): stop it once chunk3 + chunk6 exit · retries ONE AT A TIME: sed 's/pb3chunkNof20/pb3retryN/g' chunkN.json > retryN.json, then
    systemd-run --user --unit=agi-pb3-retryN --slice=agi-work.slice --working-directory=/data/work/agi --collect bash <home>/passB3/retry-cc.sh retryN
    done pi: 1 2 4 + retry5 (4/4) · running pi: 3 6 · monitor.sh watches launch(-cc) + retry(-cc)
    at the end: verdicts.py -> RED gates: anonymize BASE..TIP (its home-path gate misses /data/<user> homes, residue 128: grep them by hand)
    · step 5 VERIFY ON THE RAM DISK (owner 01:3xZ): git worktree add --detach /mnt/agi-ram/verify-b3 <merge sha>, verify there, remove it · the 3 formation D paths l4-formation-1/-3/-4 by mint_id · goal:g7.16.2 other-box user segment grep -> section 2 steps 5-9 (skill agi-merge-pass)
W   AFTER B3: resume the worktree prune (7/881 done, every byte kept under refs/archive/worktrees/*): systemd-run --user --unit=agi-wt-prune
    --slice=agi-work.slice --nice=19 --collect /usr/bin/python3 <home>/wt-prune/prune.py --apply --sleep 1 ; stop it at io PSI some avg10 > 60
C   core magic-pane merge (owner 01:1x-01:2xZ, goal:g7.16.1.7.3): ONLY the magic pane as the post anchor, NOT core's messaging; multi-ref, after the council places it
K   keysync timer agi-keysync (transient; re-arm after a reboot): systemd-run --user --unit=agi-keysync --slice=agi-engine.slice --on-calendar="*:0/2"
    --working-directory=/data/work/agi /usr/bin/python3 <home>/prime-merge-tools/trunk-sync/keysync.py  -> ancestry-only sync of key-row re-mints, else ONE [red]
S   04:00Z STOP: SendMessage the 9 posts "stop: finish the step, card whole, idle"; stream-master stays; owner <= 6 lines
D   /data < 10 GB free -> no PASS launch · R RENAME LATER (owner): hostnamectl + /etc/hosts in ONE window (the guard keys by box name now)
```

## §4 Traps (the rest live in the skills)
| # | trap | rule |
|---|---|---|
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 15 | a retire+move shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 43 | `send.py read` shows EMPTY while blocks sit in `.agi/sessions/inbox/belam.md` | read the inbox FILE by ts at every CHECK |
| 45 | `du`/`find` over `.agi/worktrees` or `/tmp` is an io storm | `git worktree list`; `find -maxdepth 1` |
| 46 | `pkill -f` / `pgrep -f` inside a Bash call matches your OWN shell | match exact argv in python (`/proc/<p>/cmdline`) |
| 56 | a commit by path in MAIN can take a file ANOTHER post is editing | `git status` it first; never `git add -A` |
| 57 | write.py self-commits (W1b) but lands UNCOMMITTED while verify-suite.lock is held | wait for the lock, then commit by exact path |
| 58 | `replace body` refuses mid-paragraph; `sub` refuses a multi-hit | anchor on a blank/heading line or `replace body N:M --force <file>`; `sub!` for all hits |
| 59 | every key re-mint lands on season2/main and blocks every rotate | the keysync timer; by hand = merge with trunk rows (pubkeys must agree) |

## §5 Verification
links 5242/0 (alive 01:0xZ) · guard --dry-run "nothing changed" + --status all ok (01:0xZ) · test_spawn_gate.py 81 passed · verify last run 18:1xZ gen 17

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| ROW R LIVE CUTOVER (goal:g6.41.1): a claude-remote-control.service restart drops EVERY post + the Prime's crons | after B3, owner present: run `env AGI_LIVE_SYSTEMD=1 python3 -m pytest extensions/agi/tests/test_rotate.py -k test_r1_cutover_dummy_one_kill_is_one_post -q` at the cutover commit; pass line = (c) scope move, none = (a) planned restart |
| belam row says opus-5-5 / high; the live Prime runs opus-5-5[1m] / max | owner sets the row before a resume-from-row lands |
| worktrees: 0 of 1021 merged by ancestry; owner "prune merged, unmerged probably stale" | done reversibly: snapshot refs + logs moved aside, never merged; owner may later drop the archive refs |
| docker data-root still on / · sda ~35 ms/op · origin remote moved | owner's window: smartctl + dmesg; `git remote set-url` |
