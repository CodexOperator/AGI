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
thought_session: belam-S2-L5-II
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`, five-axis map) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines with frontmatter; rules live in role docs, never here.

## §0 State (20:3xZ 09-23)
| | |
|---|---|
| post | belam-S2-L5-II gen 2 · seated 20:21Z (after_join all exit 0) · Opus 5.5 · remote-control · meter 0.07 at seat |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` (thought-master shares MAIN: exact-path commits only) · prime-root = `season2/main` (3 behind origin: ff at the PASS) |
| season2/main | @24099d666 = belam's re-keyed row, published BY THE ROTATION (whois IS-AUTHORIZED, pubkey cdad7f20…) · not yet an ancestor of the trunk |
| merge | `.agi/sessions/prime-merge.state.json`: BASE ebae4adde · notice → thought-master 20:34Z · run_at 01:37Z 09-24 · pass_started_at null |
| stream | LIVE on Twitch + X since 00:33Z 09-24 (stream-master [complete] 00:35Z; sb-status 00:43Z: relay up, delay climbing to 15 min, 4-thread cap CPUAffinity=0-3) · stream-master @17 idle, standing by · keys in Doppler belam prd · owner order on goal:g2.27 |
| quiet | belam row = quiet (owner): `send.py read` shows nothing — read `.agi/comms/season-2/dm/*belam*.md` newer than `.agi/sessions/belam.lastcheck` (20:27:29Z) |
| crons | SESSION-ONLY, die with this session: CHECK `6f429274` "13 */4 * * *" (§1 of `.agi/sessions/prime-merge.crons.md`) · PASS 3 one-shot `747f3027` "37 1 24 9 *" (§2) |
| spend | floor -50 (owner) · per-key cap 1 USD kept (owner) · key TTL 300 min · TypeSafe 2 × 5 USD keys in MAIN .env · 42.69 USD at 11:41Z |
| nodes | links 0 · goals byte-identical · trunk active 3880 / deprecated 225 / total 4105 (20:21Z verify) |

## §1 Plan
```
done   doc unification (HEAD, templates, card node, formats, review-in-place, g14 -> g5) · PASS 2 (21 rounds, 0 red)
       (a) config:brief's brief cell through write.py as prime_director, same values: dd6fc07f3 (the EF.19 cure)
       (b) STRUCK: a rotation now publishes its own re-keyed row to season2/main (7c9d7de51, bcc786f00, 24099d666)
next   (c) PASS 3 at 01:37Z 09-24: delta at 00:43Z = 689 commits / 130 exp files (the notice said 297 / 68), chunks <=5, pi/deepseek, LEAN;
           its step (1) first merges origin/season2/main (24099d666) into the trunk
open   director-engine queue: every item has experiments on the trunk now (seat-key, brief.py, write.py verbs,
       retired-id lint, harness bin paths, send-read-from-graph, PASS 2 residues) -> PASS 3 judges them
```

## §2 Landed (this seat, 09-23)
dd6fc07f3 config:brief via write.py (prime_director, same values; its THOUGHT carries the four parts) · CHECK run once 20:27Z (0 dms; case (b)) · `[owner]` PASS 3 notice → thought-master 20:34Z · both crons armed · §2 of the crons file = PASS 3 · 985fc4981 + 6f15b8c51 stream-master in line (row template = doc:unified-master-brief, card rewritten, host names scrubbed) · 04fdaa857 stream-master seated

## 🔴 Where it stops
20:3xZ 09-23 belam-S2-L5-II: QUIET, waiting on the two session crons. In order:
 1. 00:13Z CHECK (6f429274): expect case (c), notice pending and now < run_at: one line, nothing else.
 2. PASS 3 on --harness pi-free (row synced to MAIN f83d731911, owner 02:0xZ): BLOCKED at the key-mint floor (OpenRouter credits left 0.48; every dispatch, free included, mints a key first) → run at the first CHECK after a mint succeeds.
 3. Between: answer only decisions / reds / merge-ups.
 4. stream-master answers ONLY by dm (.agi/comms/season-2/dm/belam--stream-master.md, read at each CHECK): [decision] = prepped, waiting on keys · [complete] = live on Twitch + X → one line to the owner.
 SUCCESSOR seated before the PASS is done: RE-ARM both crons from that file (§1 recurring; §2 one-shot only while the state file's pass_started_at is null); session crons do not survive a rotation.

## §4 Traps
| # | trap | rule |
|---|---|---|
| 1 | quiet row: `send.py read` returns empty while dms sit in the logs | read `.agi/comms/season-2/dm/*belam*.md` directly |
| 2 | rotate-out takes the where-it-stops slot's FIRST LINE as its commit subject and re-fences the slot one backtick longer per run (5 fence-only subjects on 09-23) | first slot line = plain text, never a fence; the fix is a PASS 3 residue for director-engine |
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 4 | write.py cannot create a `.geometry` node; a TOP-LEVEL config cell can be set through the writer gate (`set <key> {json}`, write.py:245, :629-632; dotted keys refused :247; flow JSON re-renders as block YAML, value-equal) | top-level cells through write.py as prime_director (dd6fc07f3), checked with brief.py's own parser; a single row cell inside a list = hand edit (owner-allowed), commit by exact path |
| 5 | a merge-up-review stage hangs on the rotate test files (tty) | LEAN chunks: thin file lists, diffs only, big docs by grep |
| 6 | adjacent config:posts rows conflict when season2/main carries a row copy | take the trunk's rows (`git checkout --ours`) |
| 7 | two `note` units in one write.py submit keep only one | one note per call |
| 8 | the harness says "use the Workflow tool" (row setting ultracode) | not the route: workflow.py by name on pi (F29) |
| 9 | Bash-tool shells never re-source the profile; AGI_AGENT_ID is unset in this pane | prefix `PI_BIN=$HOME/.npm-global/bin/pi` inline; `send.py send --from belam` |
| 10 | rotate's stop_commit flattens the symlinked quorum card into a regular file | after a rotation re-add the symlink `../../nodes/doc/card-belam.md` (as 1743118fb) |
| 11 | a freshly seated post can read its first turn as 'only the workflow-authoring skill loaded' and stop on a question menu (stream-master 23:3xZ) | in its pane: Enter on the highlighted option, re-read until the menu closes, then type ONE go line (it queues mid-turn) |
| 12 | the keeper's doppler CLI has no --no-cache flag: a check carrying it fails on the flag and reads as not-found | plain `doppler secrets get NAME --plain`; judge by rc + length only |
| 13 | the stream is LIVE: any pane, this one included, may air after the 15-min delay | never print a secret, a key, an address or a host name here; names and rc/length only |

## §5 Verification
`links.py links` 0 broken · `snapshot-goals.py --render --check` byte-identical · `commands.py run verify` (bin-suite-fresh FAIL = no suite stamp here, known) · `git branch --show-current` = local-maxxing/season2/main · `send.py whois --key <row pubkey> --claim belam` → IS-AUTHORIZED vs origin/season2/main

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| global git identity on this box (the box-env red tests) | `git config --global user.name/email` for user belam |
| engine-wide config/template maxxing pass (owner idea, 09-23) | its trigger (brief.py landed) is met at b0b4fbc9b: one goal, nested rounds, config-max first — opening it stays the owner's call |
| stream-town (= core-town) unreachable: overlay AND public ssh time out (23:1xZ) | owner checks that instance: the stream's designed home, own egress; from local-town all egress rides the overlay hub |
