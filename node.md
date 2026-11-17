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
tags: []
title: Card alive
town: core
---
# doc:card-alive — alive's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; §0-§6 ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (18:39Z 11-17) -- gen 95 at f ~0.15. Every ask WORDED, every land VERIFIED (L616, L617).
Since the wake: L616 (.46.29.4 CLOSE) + L617 (sp trap sweep g78) VERIFIED (n1, n3). MAIN gc DONE by belam 17:41-17:42Z (85 -> 2 packs,
87 worktrees kept, gc.worktreePruneExpire = never). A2 +1 h lap: falsifier MET 3/3, L1 not hit, sp's 72 h test FAILED (524 loose/h)
-> council 3/3 on (E): L-fire packs loose ids (hex-filtered) + prune-packed, no pack deleted, no freeze; K-fire = the held run.
E1 PASS (aio), E2 PASS short-lived readers (belam; SAMPLED not stressed, my line), E3 PASS (belam, gap not observed needed, kept).
SM gen 101 gates the 'L' RULES tip on FOUR items: E1 hex ids; sp M2 rc line (no prune on rc != 0); my DE-DUP (same bad id twice = 1
alarm, rc != 0 both); aio's wait > 60 s BETWEEN pack-objects rc 0 and prune-packed. L itself from the +6 h lap (22:55Z).
NETBOOT 18:00Z: PHASE A NOT RUN (no window after L613), BANKED for the owner 11-18; PHASE B = his own ask only.
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code, opus; hub B (8318); f: next gen: mkdir ~/alive-work/p96, sed 3850b626-dace-48d2-a7ad-bc780d975cf1 to your session id from p95/meter.sh into p96/meter.sh |
| GOAL NOW | (1) verify the 'L' RULES tip against the four items when belam cuts it (RULES: extensions/agi/guard/ -> wrap); (2) the +6 h lap (~22:55Z): rate, row 6 vs loose, none-reached count (the debris 2nd point); (3) the ~02:30Z alarm as placed; (4) verify each land. |
| role | alive = the ANSWERER, the one voice back to SM; NEVER box belam (SM relays); a header cc NEVER names belam |
| messaging | sh ~/alive-work/mail/gsend.sh <file> <posts...> from ~/t, WHOLE output to a file, ALWAYS 'python3 -I ~/alive-work/scan.py f && sh .../gsend.sh f ...'; rc 3 = mail UNREAD (box read, fold in, resend; a peer word may make yours a repeat: shrink to '== peer' or drop); rc 4 = a watch ref moved (read that ref, resend); rc 5 = a backtick or the host name; scan ['home'] = a home-path literal in YOUR text; scan ['ip'] on INBOUND = an address in their text, never copy it; STAMP header only, DSTAMP every line; ONE gated send in flight |
| reading mail | AGI_POST=alive box read > p95/boxN.raw -> sed the home literal to <home> -> scan. 'box n' only LISTS. A tip mailed to SM alone (cc me) is read off refs/box/<sender>/sanctuary-master; a merge-up to belam off refs/box/sanctuary-master/belam |
| HOW WE WORK | agi-review: angle in one line; first claim runs; others read and try to break it; honest about what was read and not |
| ORACLE | OFF; Fable for the season rollover ONLY, off dispatch (L579) |
| watch | Monitor sh ~/alive-work/watch.sh (30 min expiry: RE-ARM, then box n + the trunk log for the gap). A 'mail: box read' prompt is a WAKE |
| SCORER (deck A/B, goal:g5.4.3.1.1) | NO content word on arm B (L608 paper route, plasma/remix/less-is-more/meme-master/director-thought-goals) until SM's unmask; a mechanical-only land check if it lands |
| lens | vision:alive: the system reports its TRUE state; silent skip / vacuous pass / false line -> RED |
| skills | agi-goal · agi-send · agi-rotate · agi-verify · agi-review · agi-master-gate (SM's side) · agi-memory-guard · agi-node-write · agi-research-then-design |

## §1 Plan (18:39Z 11-17)
```
ITEM                         OWNER   STATE
A2 'L' RULES tip             belam   four items (§0) + E2 cited 'sampled, not stressed' + E3 'gap not observed needed, 1 sample';
                                     L from the +6 h lap. RULES path -> a WRAP; verify LAND = W^2. Check each item IN THE BYTES + its test.
A2 laps                      belam   +6 h ~22:55Z (rate, row 6 vs loose, none-reached = debris 2nd point); +24 h 16:53Z 11-18.
~02:30Z alarm (L=5000)       belam   held run as landed after SM's window word, or SAID as one unanswered lap (council's red).
A2 2nd hand FIRE             belam   alarm-only until 2 count-fired runs read green with a person reading each.
NITs on lab-repack files     SM row  N3 GAP mutes a class change; N4 notice de-dup (now also the L tip's de-dup); N5 rel() restarts
                                     boxwake; mine: hold RECORDS the active set, rel() restarts ONLY that set.
:38 WHY (g7.16.1.14)         -       lab auto-gc fired, never consolidated, no gc.log: NOT READ.
wake probe BUILD (R1-R7)     belam   RULES, lands FIRST; R3 pane guard before any boxwake unmask.
g5.57 item 1 WORDING         council the measure commit: sp's inventory command whole + my place line.
netboot g5.56                owner   PHASE A NOT RUN 18:00Z, BANKED for 11-18; PHASE B = owner's own ask.
MAIN tmp_obj_jv4pGJ          -       4 KiB, 11-11; ages out 11-25 or one rm on SM's word. Harmless.
NEXT TOUCHES (not gates)     -       agi-goal :33 'mints it TWICE'; .48 F4 2>/dev/null; N6 (m40 on r6/r7); FLAKES test_agi_boot,
                                     test_crons_log_cap; ladder.md :154.
OPEN WITH THE OWNER          belam   P4 hub A rotate (BANKED); .46.37 calls; hub.said; plan-master tool policy; F4 g7.31.1.6; P8 bank.
CRUMBS                       -       NO build node: test_alarm_spool.py, test_goal_skill_h1.py, test_hub_move.py, test_council_report.py.
```

## §2 Landed (via SM's gate or belam's cell; each verified by alive; older gens in git)
Gen 95: L617 ba45a63dc6 sp trap sweep g78 (n3, census 982 equal). L616 c93e89e4e7 .46.29.4 CLOSE (n1).
Gen 94: L615 ca4a7cf900 (wrap ac129bb837), L613, L606, L614, L612, L611, L610. Older in git.

## 🔴 Where it stops
alive gen 95, 18:39Z 11-17: all owed words SAID (w1-w4, c1, n1-n3); next: the 'L' RULES tip cut, or the +6 h lap (~22:55Z).
 OWED, in order: (1) the 'L' tip at SM's [merge-up]: pre-verify (diff ^1..cut == gated tip, cmp); at the land (a WRAP): L = W^2,
     sh ~/alive-work/lanes/vland.sh <LAND> <gate tip> <WRAP> > p95/vlandN.out 2>&1; objscan; vgrid; reader census at L and ^1
     (extensions/ touched); and READ the four items in the bytes + each one's test.
 (2) the +6 h lap: check belam's arithmetic; debris rate 2nd point; row 6 vs loose for L.
 (3) each land: PLAIN = 'sanctuary-master: LAND N' on posts/belam; ONE [note].
Next command: cd ~/t; date -u; AGI_POST=alive box read > ~/alive-work/p95/boxN.raw; git log --first-parent --format='%h %an %<(70,trunc)%s' -8 refs/heads/posts/belam
Meter by hand: sh ~/alive-work/p95/meter.sh; past 0.41 no multi-ref act; at 0.47 (or a natural pause after 0.43): the card whole by one write; that reply ENDS on a prayer; the NEXT reply is the out call ALONE.
PRAYERS (owner, most critical): one of the four Church Slavonic prayers as the FIRST tokens of a session's first reply and the LAST before rotating; MAY at each idle spot; never per WORKING turn.
STANDING RECORD: credits_live true since 6a4c10bf00; atomize_live false (L346 HELD); summary_live false (owner: never on M9); belam + mm on own logins, all others on hub B; directors on sonnet (L579).
Grid lock: a turn end that reads 'not grown ... held by <pid> commit --all' at :00/:30 is the cron; flock frees on exit, the next turn grows it.

## §4 Traps (gen 95 new on top; gen 93 + 94 owed to the next sweep)
- [g95 17:4xZ] my 17:42:59Z word said 'STILL OPEN: config UNSET' from a 17:42:39Z read while belam was acting; belam wrote it 17:42:50Z
  (corrected 17:44:53Z); and count-objects size-pack is KiB, I wrote MB -> when a peer is ACTING on the thing, re-read right before the
  send and stamp the read time in the line; units from the tool's doc, never assumed.
- [g95 17:4xZ] two scratch probes of 'gc --auto detach' were VOID (one never reached the gc.auto sample dir 17, one packed 0 objects
  because repack packs only reachable) -> a probe prints the count it acts on BEFORE the act; 0 = NOT RUN, no claim made.
- [g94 13:0xZ] I APPROVED a leaf with a literal home path (SM's scan caught it) -> run anonymize.scan on the TIP's diff before a word.
- [g94 14:2xZ] a way back saved packs only though -d deletes loose -> a way back is RUN end to end before it is worded.
- [g94 15:2xZ] an extract matched 0 lines and read 'rc 0' (VOID) -> an extracted block prints its line count first; 0 = NOT RUN.
- [g94 15:2xZ] a mechanism sent as fact -> a candidate cause is worded as a candidate with its deciding read.
- [g93 08:41Z] verifying a RULES land I read WRAP^^ -> the land under a wrap is $(git rev-parse W^2), never W^^.

## §5 Verification (gen 95, files under ~/alive-work/p95)
- lands: L616 pre-verify + vland/obj/vgrid; L617 pre-verify + vland/obj/vgrid + reader census (982 / 85 equal).
- READ: MAIN gc state before/after (read-only); agi-lab-pack-count + lab-repack.sh at ac129bb837 (find counts all loose; M3 never
  prunes); belam's lap + E2 arithmetic re-computed.
- NOT RUN this gen: any suite, links, anything on the lab, the PC, NFS or as root; any gc/repack/prune/config act.

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| per-post scratch on /data so review copies + pytest basetemps leave the root mount | (a) belam host act (b) keep on / | (a), owner's call; council YES |
Paid-for path guard: never create .agi/bin/snapshot-build-site.py or .agi/bin/render-context.py; never recreate .agi/context/kits/ or .agi/context/plans/build-site.md.

## §7 ATOMS (inbound asks, one row each; open > 1 lap = red)
| atom | from | placed |
|---|---|---|
| SM [decision] 18:0xZ: A2's L words by ~20:00Z | SM | CLOSED: w2 18:04:13Z (E) 3/3 conditional; E1/E2/E3 all PASS; four tip items placed by SM gen 101. OPEN: verify the 'L' tip |
| A2 laps (+6 h ~22:55Z, +24 h 16:53Z 11-18) | belam/SM | +1 h read (w2). OPEN: +6 h |
| belam [owner] 06:4xZ: NETBOOT lab tonight | owner via belam | CLOSED for today: 18:00Z line SAID (w2) NOT RUN; BANKED for the owner 11-18 |
| MAIN auto-gc (aio 17:38Z) | aio/SM | CLOSED: belam DONE 17:43Z; my after-read w1 + correction c1 |
| sp 18:09Z: E1 amend + sweep cut | sp | CLOSED: w3 YES + APPROVE; L617 VERIFIED n3 |
| self: gen 93 + 94 + 95 traps to a skill | alive | OWED at the next trap sweep |
| SM 18:52:50Z 11-15: goal:g5.4.3.1.1 deck A/B | SM | scorer blind on arm B. OPEN: SM's unmask |
| older rows (gen 86-94, CLOSED) | - | in git: grid.py diff doc:card-alive |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 95, 18:39Z 11-17: why THIS version differs. The A2 fix met its own falsifier at +1 h but failed the 72 h test, and the
council re-worded the fire in under an hour by running each claim instead of trusting it: my debris-floor read came from the landed
bytes, all-is-one ran it, belam ran the NFS reads, and two mechanisms (mine on gc detach, all-is-one's on stale listings) were dropped
or corrected when a run did not show them. My two misses today were both about TIME: a state read 20 s before a peer changed it, and
a unit assumed. Each is a trap above.
<!-- THOUGHT:END -->
