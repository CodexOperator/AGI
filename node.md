---
id: doc:card-director-general-1
mint_id: 960e181d30924fb3ba1a63ca4a6698f4
type: doc
parents:
  - goal:g7.31.1
next_edges: []
edited_by: director-general-1
scaffold_hash: 67b067422d7509fe
season: 2
tags: []
title: Card director general 1
town: core
---
# doc:card-director-general-1 — director-general-1's card (the ONE scratch; replaced whole). Written whole 11-17 ~01:5xZ, a fresh Sonnet generation (owner 02:12Z 11-12), mid-run, not at the meter.

Role: doc:unified-director-brief + this card. Post director-general-1 (uid 979), builder, council loop: SM gates and lands, belam wraps RULES lands, the council (alive, all-is-one, self-perpetuating) rules. Skills: agi-node-write, agi-goal, agi-send, agi-rotate, agi-verify, agi-post.
Method that works: lane = `git clone -q --shared --no-checkout ~/t <lane> && git -C <lane> fetch -q ~/t origin/posts/belam && git -C <lane> checkout -q -b <branch> FETCH_HEAD`; build, run the lanes ALONE (one pytest at a time: the suite lock; the host-act lane ONLY with `</dev/null`), commit, `git push -q ~/t HEAD:refs/heads/<branch>`, then ONE [merge-up] to sanctuary-master (`box send` FROM ~/t, not from a lane dir) naming branch + tip + what you did NOT run. A residue = a CHILD commit, never an amend.

## §0 State (11-17 ~01:5xZ)
- LANDED this generation: L581 L582 L585 L586 L588 L589 L591 (P9 mint) L594 (.46.38 write_node ONE heading + its build node, 21e9b6208b) L595 (alarm-id BUILD) L598 (build:bin-alarm-spool) L599 (CLOSE of goal:g7.16.1.11.20.2.1, COMPLETE; a real alarm NOT SEEN).
- AT SM'S GATE, mine: NOTHING. Nothing for me to build until a residue or a new placement comes.
- Not mine, named: the .46.38 CLOSE is DGo1's (F1-F8 on the trunk); the stale skills/agi-goal :33 line ('mints it TWICE') is the next agi-goal touch (RULES path, DGo1's skill).

## §1 Plan
- Residue on either tip: fix in the lane as a CHILD commit (lanes d9 = alarm-id, d13 = writenode-h1, under /data/scratch/director-general-1/lanes/).
- Plan-master umbrella goal:g7.31.1.7: leaves 2-5 NOT minted (2 agi-run's grok arm, 3 non-claude mail wake, 4 the row + doc:role-plan-master, 5 live = belam's host act). Read goal:g7.31.1.7. Mint only on SM's word (never invent goals).
- P5 (hub fallback on quota) = goal:g7.16.1.11.46.37, the engine half is director-general-2's.
- LATER (named, no leaf): f1.sh v2.4 cleanup; heal's pane-unknown line wording; agi-run's grok arm; old FINDINGS (rotate _derive_pred_pids '0', heal _rotation_in_flight silent skip); alive's reading (an installed box whose carry.env/host.done is a link to identical bytes reads 'host: met': harmless, banked).

## §2 Landed (one line each; full list in git)
L542 L546 L548 L549 L551 (g7.31.1.6/7 mints + heal) · L555 L570 L573 (agi-project grok arm) · L574 L575 L576 (agi.sh host) · L577 (P7) · L579 (P7b) · L581 L582 L585 L586 L588 L589 L591 L594 L595 L598 L599 (above).

## 🔴 Where it stops
Idle at ~01:5xZ, nothing at SM's gate. NEXT: read the inbox; on a residue fix it in a lane as a CHILD commit and send ONE [merge-up]; a new placement from SM = a new lane off the trunk.
Next command: `cd ~/t && AGI_POST=director-general-1 box n && AGI_POST=director-general-1 box read | fold -s -w 200`

## §4 Traps (this generation's; move each to its skill at the next rotation)
- host-act-encryption-town.t.sh HANGS 40 min on a mutant row (a `cat` on an open stdin) when run without `</dev/null`: always redirect.
- `pkill -f <pattern>` inside the same bash command line kills ITSELF (the pattern is in its own argv): kill by pid.
- `box send` run from a lane dir fails 'invalid object name core/season3/main' + 'off-matrix': cd ~/t first. It prints nothing on success.
- A falsifier that quotes its own negative pattern hits itself: bracket one character (`c:d1ac1ea827f[d]`).
- A grep -c over a name is a SUBSTRING match: match the table cell (`grep -F -- "| $p |"`) and run a mutant where prose names the dropped row.
- A mutant sed anchored on a line breaks when the line is widened: re-run the WHOLE lane after any edit to a line a mutant targets.
- A test fixture's absolute link inside a rehearsal root: hop() re-prefixes absolute hops with $R, so use a root-relative link (/etc/x), not $X/etc/x.
- Minting a build node whose parent goal is not on the trunk yet: put the goal file in the worktree UNCOMMITTED, mint, delete it before the commit.

## §5 Verification
Per tip: the lane's rows each with a mutant that reads RED (and the GREEN case run first); `git show --stat`; list what was NOT run in the merge-up; LOAD > 8: only own lanes, niced; a whole pytest at load ~13 flakes: re-run ALONE before reading a red as the tip's.

## §6 BANKED
- agi-reaper (for belam, to the owner): a second uid for heal would close g7.31.1.2's T2 and g7.31.1.6's F4; the ask was banked 11-12, not yet made.
- P8 (the owner's, banked by SM): director class row effort max vs post rows high, and rotate.py's director fallback ultracode True on sonnet.
- DISK: in the home, 11 clones with dirty files or unreachable commits (w5 w7 w8 w10 w11 w12 w15 w16 w17 w20 w22) and 15 git-less exports/scratch (w9 w14 w23-w37) need a person's OK to remove; /data/scratch/director-general-1/lanes/* and tmp.* are mine (removable after the lands).
- P10: gsend refuses tokens and private-range addresses until the capsule leaf lands (SM relaxes nothing).

## §7 ATOMS (inbound owner/parent asks; one row per atom; open > one lap = red)
| atom | from | state |
|---|---|---|
| P9 rank meters design leaf | owner Q7 via SM | DONE L591 (goal:g7.16.1.13; the design doc rank-meters is a later leaf) |
| alarm-id leaf BUILD + CLOSE | SM placement 3/3 | DONE L595 L598 L599 |
| .46.38 write_node ONE heading BUILD | SM placement via DGo1 | DONE L594 (the close is DGo1's) |
| plan-master umbrella leaves 2-5 | owner 11-10 via belam/SM | OPEN: not minted, on SM's word |
| ROOT DISK, the stream, hub quota (P5) | SM/belam | P5 = DG2's; the rest not mine |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
address doc:card-director-general-1 reused at G5: before the G3 4a land ba8faaad3a (10-21) it named card mint 241494f333 (goals-1), now doc:card-director-goals-1; from G5 it is this card, mint 960e181d30924fb3ba1a63ca4a6698f4, the card of the post that was director-general-3 (goal:g7.16.1.11.45).
<!-- THOUGHT:END -->
