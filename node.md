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

## §0 State (16:0xZ 11-09) -- gen 73 ROTATES at f 0.42, a natural pause: every owed word sent, nothing in flight. Gen 73: 2c-3/2c-4/2c-5 words (3/3 each, my 2c-5 TERM on the dead-id route), L468 + L469 + L458 (+W + host act) VERIFIED, .46.20 root act PASS verified + close 3/3 (my TERM), census red route (B) + fix 3/3, DG2 follow-up 3/3, R1 settled (mine), verify-land pre-pass leaf placed 3/3: MINT OWED (mine).
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code; gen 73 6fa3ba88 claude-opus-5-5, 11:48Z - 16:0xZ 11-09; gen 72 ad9d660b 09:33Z - 11:4xZ; no meter hook -> f by hand (sh ~/alive-work/p73/meter.sh = meter.sh with session id 6fa3ba88-2577-4f50-8d4c-de68b40cd342; sed it to yours into p74/) every few turns |
| GOAL NOW | (1) MINT the verify-land pre-pass leaf (SM tally 16:01Z, below). (2) R1 tip once L474 is on the trunk. (3) vland + vgrid + [note] for each land as SM cuts it: L470 re-cut, L471-L476, GATE628 (census fix 9b20142729), GATE629 (DG2 follow-up 08dbe7e1ce, AFTER my R1 tip), GATE626 (2c stack 7de1847701), GATE627 (.46.20 close 7a8eb7c7d7). |
| role | alive = the ANSWERER, the one voice back to SM; SM sends [review]/[place]/[note]/[ask]/[relay]; NEVER box belam (SM relays WHOLE); a header cc NEVER names belam |
| messaging | sh ~/alive-work/mail/gsend.sh <file> <posts...> from ~/t, its WHOLE output to a file (> f 2>&1): rc 3 = mail waiting UNREAD (box read it yourself, fold in, resend); rc 4 = a watch ref moved (resend as is); STAMP on the HEADER line only, DSTAMP every line; text by the Write tool; privacy scan first: python3 -I ~/alive-work/scan.py <file>; header cc == the argument list; ONE gated send in flight; several items ride ONE word |
| watch | Monitor sh ~/alive-work/watch.sh (20 s poll, 30 min expiry, re-arm, then box n + the trunk log for the gap). SM's cc to me often rides only the OTHER posts' refs: read those refs (git log -1 --format=%B). A 'mail: box read' prompt is a WAKE: box read into a file, whole |
| council rules | VIEW to both seats (cc SM) -> ONE [decision] to SM after both answered, or 15 min MEASURED; seat terms ride as 'author's + mine, silence = agree'; [correction] amends |
| how I review | git first (%G?, merge-tree onto the LIVE trunk, 0 D, every added object non-empty); PRIVACY = ~/alive-work/p58/objscan.py <tip> <base>; a land blob != its tip blob: check it == git merge-file of (p1, merge-base, tip); read the bytes; RUN every claim a line states; READ every route a line names to its filter; whole-tree lanes (reader-census, links) ride every gate or are named NOT RUN; nothing under refs/held is armed without SM's [merge-up]; load5 > 8: cheap reads only, the load gate IN the command (agi-memory-guard:117) |
| lens | vision:alive: the system reports its TRUE state; silent skip / vacuous pass / false line -> RED |
| skills | agi-goal · agi-send · agi-rotate · agi-verify · agi-review · agi-master-gate (SM's side) · agi-memory-guard · agi-node-write |

## §1 Plan (16:0xZ 11-09)
```
ITEM                       OWNER   STATE
LANDS L421-L469, L458      -       VERIFIED, each vland + vgrid + [note]; gen 73: L468, L469, L458 + W f45e10cd16 + host act.
VERIFY-LAND PRE-PASS LEAF  alive   MINT OWED (SM 16:01Z tally 3/3: sp 15:58:01Z, aio 15:58:56Z, mine 16:00:47Z). See the red slot.
R1 NAME-CITE TIP           alive   OWED after L474 lands; lands BEFORE DG2's follow-up (SM 15:55Z). See the red slot.
CUT CHAIN (SM)             SM      L470 8e9fab11ac re-cut on the live trunk (old 8d9076bef1 VOID), then L471 DGo1 atoms 3290e4d263, L472 DGo1 .46.12
                                   addc4e4687, L473 sp g60 108de39c0e, L474 my g70b-r1 c60ded9079, L475; then the census fix (GATE628), my R1 tip,
                                   DG2 follow-up (GATE629). RE-GATED: 622 my g70-71 bd0461b6fa (after L473), 623 aio g61 cf31a76262 (after L470).
                                   Then GATE626 (2c stack, WHOLE, with reader-census) and GATE627 (.46.20 close).
g7.31.1.2 ACT 2c (DG1)     DG1     2c-1..2c-5 all 3/3; stack = GATE626 on 7de1847701 after the census fix; ONE cut.
.46.20 V2 (DS1)            DS1     DONE on the host (PASS 12:27:42Z, F1 PASS, aside deleted); CLOSE 7a8eb7c7d7 3/3 -> GATE627.
g7.16.2.1 private-range    DG2     L458 landed; FOLLOW-UP 08dbe7e1ce 3/3 (GATE629); then the CLOSE (names the pre-pass leaf OPEN).
CENSUS (reader-census)     aio     route (B) fix 9b20142729 3/3 -> GATE628; every gate now carries reader-census + links (3/3).
.46.19 V1 (DG2)            DG2     NIT for its next touch: its atoms table lacks 2.2-rest + 2.25 (from .46.20's close).
BANKED VIA SM              OWNER   the row cell 'resume_failed' (owner's batch).
HELD (card-belam s6)       OWNER   atomize_live + summary_live flips, V1b host act, .46.28 F3, .20.4 crons apply --sudo, g7.31.1/.3, R2 grant.
CRUMBS (next touches)      -       resume-failed reads UNREAD as none (heal.py _last_resume_failed); cred-act.sh label 'a refresh' -> 'written after
                                   the seed'; drop-in's dead '[cred]' echo + no build node; 37 of 97 bin .py no build node; SM headers carry the arming gen.
HARD RESETS                OWNER   after any boot (uptime -s after 02:44:54Z 11-04): refs resolve + fsck.
```

## §2 Landed (via SM's gate or belam's cell; each verified by alive; older gens in git)
Gen 73: L458 b57e2b62d1 + W f45e10cd16 (DG2 g7.16.2.1 BUILD, RULES) 15:41Z: == held pre-verify, agi-review blob == clean 3-way with 096fe796a0, census 0 new, vgrid OK (NO-NODE: 3 old + NEW test_anonymize_private_ip.py, now minted in 08dbe7e1ce); host act 15:42:01Z cmp == pin; [note]s 15:42:10Z + 15:44:15Z.
Gen 73: L469 51a8273735 (DG1 2b) 12:13:52Z [note] 12:14:23Z; L468 d2c3e96f5a (DS1 .46.7 CLOSE) 11:53:55Z [note] 12:01:33Z. Gen 72: L467 + W, L466, L464, L462, L460, L459. Details: this card's git history.

## 🔴 Where it stops
alive gen 73 rotated at f 0.42 (16:0xZ 11-09); next: MINT the verify-land pre-pass leaf, then the R1 tip once L474 lands.
 OWED, in order: (1) YOUR WAKE: the prayer ALONE, then this card, then box read into p74/box1.txt, whole.
 (2) THE MINT (skill agi-goal, read it first): one goal leaf for the verify-land.sh fixture-home pre-pass defect (aio [finding] 15:56:34Z: the pre-pass sets cur on any '+++ ' line with no hunk flag, so a crafted added '++ b/extensions/agi/tests/<x>' line in a non-test file lets a pinned home path pass anon-diff). Cites 1d03fbb794 (DG3, goal:g7.16.1.11.46.16 item 1, status complete) + aio's finding. Target (SM 16:01Z): ONE header-aware diff reader exported by anonymize, walked by mask_diff_ips, reds._added AND the pre-pass; the landed rows + mutants of the first two UNCHANGED as the regression check; the reader yields a line number; the git-quoted (None) path in its contract, path_allowed(None) guarded, with a row; aio's crafted row + a mutant RED in all three; then belam's re-install of verify-land read back against the pin (RULES). DG2 builds it if it takes it. Pick a live parent (.46.16 is complete; read its siblings and parent first) and a legal id; then [note] SM the id.
 (3) R1: when c60ded9079 is an ancestor of posts/belam: sh ~/alive-work/p73/cite/cut.sh <trunk sha> > p74/cite.out 2>&1 (refuses rc 4 before; makes refs/heads/tip/alive/cite-r1); [merge-up] to SM: one line on agi-memory-guard :117 '(reds.py:37-52, `_extract`)' -> '(`_extract` in reds.py)', gate skills-truth + reader-census + links, BEFORE GATE629's cut.
 (4) Each land as SM cuts it: vland <LAND sha> <gate tip> [<wrap sha>] (a COMMIT sha), vgrid, objscan, census when load5 < 8, [note].
 Scripts: ~/alive-work (lanes/vland.sh, p52/vgrid.sh, p58/objscan.py, mail/gsend.sh, watch.sh, scan.py, p73/cite/cut.sh + msg). vland.sh exits 1 with no W: read its lines, not its rc.
 The turn end commits ~/t (agi-turn): edit the card at .agi/nodes/doc/card-alive.md only. A grid split can miss the :00/:30 grid_sync lock: the next turn end retries.
Next command: cd ~/t; date -u; uptime; mkdir -p ~/alive-work/p74; AGI_POST=alive box n; git log --first-parent --format='%h %an %<(70,trunc)%s' -4 refs/heads/posts/belam
Meter by hand: sed p73/meter.sh's session id to yours into p74/meter.sh; past 0.41 no multi-ref act; at 0.47 (or a natural pause after 0.43): the card whole by one write; that reply ENDS on a prayer; the NEXT reply is the out call ALONE (agi-rotate s2).
PRAYERS (owner, most critical): one of the four Church Slavonic prayers as the FIRST tokens of a session's first reply and the LAST before rotating; MAY at each idle spot (owner 11-07); never per WORKING turn.
STANDING RECORD: credits_live true since 6a4c10bf00; atomize_live false (L346 HELD); summary_live false (owner: never on M9); carry.env = 3beb8abb88.

## §4 Traps (gen 73's own; gen 72's three placed: the git-grep-cite one superseded by the name-cite rule below, the load-in-command one in c60ded9079, the carry-grep one in aio's g61 cf31a76262)
- gen 73: claimed "'kind secret' only in this node" and "0 code paths name refs/id/" off greps scoped to .agi/nodes/goal and extensions/agi/bin; aio found 6 files + id-chain.t.sh -> a 0-hit / 'only here' claim names its grep's path scope, or the grep runs the whole tree (agi-review's class)
- gen 73: my gen-72 2c-2 APPROVE passed a leaf's named read-back route (rotate.py status --record latest) unread; its reader skips crash-recovery records -> a route a line names is READ to its filter (or run) before an AGREE (agi-review's class)
- gen 73: L474's 'reds.py:37-52' cite in a skill line went stale when DG2's follow-up grew reds.py by 22 lines -> a skill cites code by function or row NAME; line numbers only inside a word or message (read once) (agi-review / agi-send class)
- gen 73: my 10:57Z VERIFIED of L460 read only its bytes; reader-census was red on the trunk from L460 for 3.5 h -> a land's [note] names the whole-tree lanes it did not run (SM's rule since 14:57Z: every gate carries reader-census + links)

## §5 Verification (gen 73; older in git)
- census: p73/census.<rev>.out (57dc762dd9 rc 1, 9b20142729 rc 0, f8a655f1b3 + b57e2b62d1 rc 1 same single red); .46.7 F1 p73/f1_467.out 16 ok / 0 FAIL
- lands: p73/vland{468t,469t,458,458t}.out, vgrid{468,469,458}.out; host reads (.46.20 seed entry, drop-in sha, verify-land cmp) in the [note]s
- NOT RUN all gen: any full pytest or gate lane; probes as other uids (DS1's F1 + mutant are DS1's readings)

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| per-post scratch on /data (owned by each post uid) so review copies + pytest basetemps leave the root mount | (a) belam host act (b) keep on / | (a), owner's call; belam, sp, alive, aio YES |
Paid-for path guard: never create .agi/bin/snapshot-build-site.py or .agi/bin/render-context.py; never recreate .agi/context/kits/ or .agi/context/plans/build-site.md.

## §7 ATOMS (inbound asks, one row each; open > 1 lap = red)
| atom | from | placed |
|---|---|---|
| SM 16:01Z tally: MINT the verify-land pre-pass leaf (aio's [finding] 15:56:34Z) | SM/council | 3/3 placement (sp WHERE/HOW, aio CONDITION, mine 16:00:47Z). OPEN: gen 74 mints, [note] SM the id |
| SM [review] 15:52Z R1: L474's reds.py line cite vs DG2's follow-up | SM | SETTLED 15:55Z on my route (name-cite tip after L474, before GATE629); script ready. OPEN: cut + [merge-up] |
| DG2 g7.16.2.1 FOLLOW-UP 08dbe7e1ce | DG2/SM | 3/3 APPROVE AS GATED (mine 15:51:53Z, sp 15:53:26Z, aio 15:56:34Z); GATE629 after my R1 tip. OPEN: land, vland + [note]; the CLOSE |
| sp [note] 00:46:08Z: private-range addresses -> goal:g7.16.2.1 | sp/aio | L458 + W VERIFIED 15:42:10Z; host act VERIFIED 15:44:15Z. OPEN: the follow-up's land; the CLOSE |
| SM [red] 14:39Z: reader-census RED on the trunk since L460 | SM/aio | route (B) 3/3; fix 9b20142729 3/3 (mine 14:59:37Z, census RUN). OPEN: GATE628, land, vland + [note]; GATE626 WHOLE |
| DG1 g7.31.1.2 ACT 2c: 2c-1..2c-5, stacked on 2b = L469 | DG1/SM | all 3/3; 2c-5 7de1847701 (mine 12:08:00Z + latent NIT). OPEN: GATE626, ONE cut, vland + [note] |
| SM [review] 12:34Z: DS1 CLOSE .46.20 -> RE-CUT 2 7a8eb7c7d7 | DS1/SM | 3/3 APPROVE AS GATED (mine 12:47:03Z). OPEN: GATE627, land, vland + [note] |
| DS1 [merge-up] 08:58Z: .46.20 V2 PLACEMENT (RULES) | DS1/SM | root act PASS 12:27:42Z VERIFIED 12:31:16Z; F1 PASS; aside deleted 12:34:45Z. CLOSED (the close rides GATE627) |
| SM [review] 10:32Z: DS1 CLOSE .46.7 | DS1/SM | L468 VERIFIED; F1 RUN by me == DS1's. CLOSED |
| SM [review] 10:32Z: DG1 ACT 2b 091695090d | DG1/SM | L469 VERIFIED 12:14:23Z. CLOSED |
| alive OWED SWEEP gens 70-71: bd0461b6fa + c60ded9079 | alive | 3/3 each; c60ded9079 = L474 in the chain; bd0461b6fa re-gated (622) after L473. OPEN: lands, vland + [note] |
| aio TRAP SWEEP g61 cf31a76262 | aio/SM | 3/3; re-gated (623) after L470. OPEN: land, vland + [note] |
| sp TRAP SWEEP g60 108de39c0e | sp/SM | 3/3 = L473 in the chain. OPEN: land, vland + [note] |
| DGo1 .46.12 CLOSE addc4e4687 + .13.4 re-run + .44.8 horizon | DGo1/SM | 3/3 = L472. OPEN: land, vland + [note]; .13.4's close after belam's F3 row |
| owner atoms (a) pi-call idea, (b) crons.py retirement, (R) OptMem horizon + s11 OVERRULED | owner/belam | DGo1's tip 3290e4d263 3/3 = L471. OPEN: land, vland + [note]; then CLOSES |
| DG1 TRAP SWEEP r2 8e9fab11ac | DG1/SM | 3/3 = L470 (re-cut owed by SM). OPEN: land, vland + [note] |
| SM CHECK T2 08:47Z (belam's leaf list) | SM/belam | PLACED 08:55Z. OPEN: those places' results |
| belam [owner] 03:14:32Z: Meme Master; bundles on core; STANDING STOP at season 3's end; login standby | owner/belam/SM | g5.4.4 = L461 VERIFIED. OPEN: next-touch NITs; aio NOTE A at the stop |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 73, 16:0xZ 11-09: why THIS version differs. Gen 73 closed its lap. The 2c stack is approved end to end, and three
lands plus two host acts are verified from my uid. The council fixed three silent-state gaps I named or agreed: a dead id's
record route that read nothing, a whole-tree lane that no gate ran, and a line cite that drifts. I rotate at 0.42 rather than
start the mint, because the mint needs the goal schema, a parent and a sibling read, and a successor does that whole.
<!-- THOUGHT:END -->
