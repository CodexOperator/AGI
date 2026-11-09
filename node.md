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

## §0 State (19:48Z 11-09) -- gen 74 ROTATES at f 0.444 (measured 19:48:17Z), a natural pause: every owed word sent, nothing in flight. Gen 74: minted the verify-land pre-pass leaf (goal .46.33, after a .46.32 id collision, re-ided); R1 name-cite cut + landed (L477); L470-L479 + L476 VERIFIED; 6 words, 3 corrections; SM's [merge-up] heredoc fixed by mechanism on my lean; L480 (a) word sent.
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code; gen 74 43169254 claude-opus-5-5, 16:34Z - 19:4xZ 11-09; on HUB A since 19:4xZ (owner order via belam: use it before its reset; report any 'limit' reply at once); no meter hook -> f by hand (sh ~/alive-work/p74/meter.sh = meter.sh with session id 43169254-6e82-44a8-94e7-ede69a8ab6f1; sed it to yours into p75/) every few turns |
| GOAL NOW | (1) TRAP SWEEP gens 73-74 (one PLAIN tip, rows in §1). (2) vland + vgrid + objscan + [note] for each land SM cuts: L480 (DG2 follow-up 08dbe7e1ce, 3/3 + my (a) word 19:48:05Z), GATE622 (my g70-71 bd0461b6fa), GATE623 (aio g61 cf31a76262), GATE633 (DG1 two build nodes d98818ae97), GATE630 (aio g64 ad819edb57, after 622). |
| role | alive = the ANSWERER, the one voice back to SM; SM sends [review]/[place]/[note]/[ask]/[relay]; NEVER box belam (SM relays WHOLE); a header cc NEVER names belam |
| messaging | sh ~/alive-work/mail/gsend.sh <file> <posts...> from ~/t, its WHOLE output to a file (> f 2>&1): rc 3 = mail waiting UNREAD (box read it yourself, fold in, resend); rc 4 = a watch ref moved (resend as is); rc 5 = a backtick or the host name in the text (quote code in words); STAMP on the HEADER line only, DSTAMP every line; text by the Write tool; privacy scan first: python3 -I ~/alive-work/scan.py <file>; header cc == the argument list; ONE gated send in flight; several items ride ONE word |
| watch | Monitor sh ~/alive-work/watch.sh (20 s poll, 30 min expiry, re-arm, then box n + the trunk log for the gap). A restart (hub move, crash) KILLS it: re-arm. SM's cc to me often rides only the OTHER posts' refs: read those refs (git log -1 --format=%B). A 'mail: box read' prompt is a WAKE: box read into a file, whole |
| council rules | VIEW to both seats (cc SM) -> ONE [decision] to SM after both answered, or 15 min MEASURED; seat terms ride as 'author's + mine, silence = agree'; [correction] amends |
| how I review | git first (%G?, merge-tree onto the LIVE trunk, 0 D, every added object non-empty); PRIVACY = ~/alive-work/p58/objscan.py <tip> <base>; a land blob != its tip blob: check it == git merge-file of (p1, merge-base, tip); read the bytes; RUN every claim a line states (a 'which commits moved X' line runs git log base..p1 -- X); READ every route a line names to its filter; whole-tree lanes (reader-census, links) ride every gate or are named NOT RUN; load5 > 8: cheap reads only, the load gate IN the command |
| lens | vision:alive: the system reports its TRUE state; silent skip / vacuous pass / false line -> RED |
| skills | agi-goal · agi-send · agi-rotate · agi-verify · agi-review · agi-master-gate (SM's side) · agi-memory-guard · agi-node-write |

## §1 Plan (19:48Z 11-09)
```
ITEM                       OWNER   STATE
TRAP SWEEP gens 73-74      alive   OWED, gen 75's first act (owner 10-10: one sweep, then a rule). ONE PLAIN tip on the live trunk, one line per
                                   trap in the skill that owns its flow; grep each skill FIRST and DROP what is already homed (aio g64's way):
                                   (a) gen 74 next-free-id -> agi-goal §5 (its 'Next free id' git grep reads the work tree only).
                                   (b) gen 74 a 'which commits moved X' line from memory -> agi-review (likely covered by its RUN-every-claim line: check).
                                   (c) gen 74 whole-tree links.py schema > 900 s -> agi-verify or agi-node-write: per node, links.py mint <mint_id>
                                       + the [type] required-field read.
                                   (d) gen 73 a 0-hit / 'only here' claim off a path-scoped grep -> agi-review (names its scope or greps the tree).
                                   (e) gen 73 a skill cites code by NAME, never line numbers -> agi-review or agi-send (R1 = L477 is the incident).
                                   (f) gen 73 L460 whole-tree lanes -> likely HOMED at agi-review's reader_census at tip AND base line: check, drop.
                                   gen 73's route trap is HOMED by aio's g64 ad819edb57 (GATE630): dropped.
LANDS L421-L479            -       VERIFIED, each vland + vgrid + [note]; gen 74: L470-L479 + L476 (§2).
VERIFY-LAND PRE-PASS LEAF  DG2     goal:g7.16.1.11.46.33 (minted by me, mint 4275c3e3...); builds after L480 (DG2 follow-up) lands; DG2's CLOSE names it OPEN.
L480 (DG2 g7.16.2.1 F-UP)  SM      GATE629 GREEN 19:38:50Z; cut HELD on b-7 class ip = the L458 test fixtures (same 5 distinct, 13 occurrences, 0 on
                                   added lines); my (a) word 19:48:05Z. SM re-cuts with three words.
QUEUE (SM)                 SM      L480 -> GATE622 (my g70-71) -> GATE623 (aio g61) -> GATE633 (DG1 nodes) -> GATE630 (aio g64).
g7.31.1.2 ACT 2c (DG1)     DG1     LANDED L478; the live kill + reattach run is the owner's or belam's GO (none given); DG1's CLOSE after it.
g7.16.2.1 private-range    DG2     follow-up = L480; then the CLOSE (names .46.33 OPEN).
.46.19 V1 (DG2)            DG2     NIT for its next touch: its atoms table lacks 2.2-rest + 2.25 (sp 18:41:39Z: a one-way pointer from .46.20).
BANKED VIA SM              OWNER   the row cell 'resume_failed' (owner's batch).
HELD (card-belam s6)       OWNER   atomize_live + summary_live flips, V1b host act, .46.28 F3, .20.4 crons apply --sudo, g7.31.1/.3, R2 grant.
CRUMBS (next touches)      -       resume-failed reads UNREAD as none (heal.py _last_resume_failed); cred-act.sh label 'a refresh' -> 'written after
                                   the seed'; drop-in's dead '[cred]' echo + no build node; ~35 bin .py with no build node (banked class, belam 11-07).
HARD RESETS                OWNER   after any boot (uptime -s after 02:44:54Z 11-04): refs resolve + fsck.
```

## §2 Landed (via SM's gate or belam's cell; each verified by alive; older gens in git)
Gen 74 (all [note]s to SM, cc aio + sp): L479 f5c73de224 (DGo1 .46.32 v2 r1) 19:40:23Z; L478 aedd59484f (DG1 2c stack, 9 M; 2 files NO-NODE =
banked class; aio census CLEAN) 19:10:12Z; L477 5bd6dce3e9 (my R1, :117 cites _extract by name) 18:50:07Z; L475 474269e5a8 (DS1 .46.20 CLOSE)
18:39:46Z; L474 9eab1f5313 (my g70b r1) 18:10:45Z; L473 59d46469f6 (sp g60; agi-review blob == merge-file) 17:49:46Z; L472 12eb583018 (DGo1 .46.12
CLOSE) 17:42:06Z; L471 5f9568ffde (DGo1 atoms, adds DGo1's .46.32) 17:10:05Z; L470 f50b2ac7a5 (DG1 sweep r2; 2 blobs == merge-file) 17:00:52Z;
L476 3319e87e50 (aio census fix (B)) 16:45:38Z. Every one: p2 == tip, tree == merge-tree, == refs/held, D 0, objscan 0 hits, vgrid OK. Census on
the trunk CLEAN since L476 (sp + aio runs at L471, L473, L474, L478). Gen 73: L458 + W + host act, L469, L468. Details: this card's git history.

## 🔴 Where it stops
alive gen 74 rotated at f 0.444 (19:48Z 11-09); next: the TRAP SWEEP gens 73-74, then each land as SM cuts it (L480 first).
 OWED, in order: (1) YOUR WAKE: the prayer ALONE, then this card, then box read into p75/box1.txt, whole; re-arm the watch.
 (2) THE TRAP SWEEP (§1 rows a-f): grep each target skill on the live trunk first; one PLAIN tip, refs/heads/tip/alive/sweep-g73-74, signed,
     one parent = the live trunk; census-pattern check on the added lines; [merge-up] to SM (gate: skills-truth + every skill lane + reader-census + links).
 (3) Each land as SM cuts it: sh ~/alive-work/lanes/vland.sh <LAND sha> <gate tip> [<wrap sha>] > p75/vlandN.out 2>&1 (read its lines, not its
     rc: it exits 1 with no W); sh ~/alive-work/p52/vgrid.sh <LAND>; python3 -I ~/alive-work/p58/objscan.py <LAND> <LAND>^1; census by
     reader_census.py repo --rev <sha> only when load5 < 8; [note]. A blob != tip: check == merge-file(p1, merge-base, tip).
 (4) .46.33: no act of mine until DG2 builds it; read its tip against Falsifiers 1-5 when SM sends the [review].
 Scripts: ~/alive-work (lanes/vland.sh, p52/vgrid.sh, p58/objscan.py, mail/gsend.sh, watch.sh, scan.py, p73/cite/cut.sh, p74/meter.sh).
 The turn end commits ~/t (agi-turn). A grid split can miss the lock (grid_sync at :00/:30, unify --write at :15/:45): the next turn end retries.
Next command: cd ~/t; date -u; uptime; mkdir -p ~/alive-work/p75; AGI_POST=alive box n; git log --first-parent --format='%h %an %<(70,trunc)%s' -4 refs/heads/posts/belam
Meter by hand: sed p74/meter.sh's session id to yours into p75/meter.sh; past 0.41 no multi-ref act; at 0.47 (or a natural pause after 0.43): the card whole by one write; that reply ENDS on a prayer; the NEXT reply is the out call ALONE (agi-rotate s2).
PRAYERS (owner, most critical): one of the four Church Slavonic prayers as the FIRST tokens of a session's first reply and the LAST before rotating; MAY at each idle spot (owner 11-07); never per WORKING turn.
STANDING RECORD: credits_live true since 6a4c10bf00; atomize_live false (L346 HELD); summary_live false (owner: never on M9); carry.env AGI_TRUNK = f45e10cd16 (belam's re-pin 16:36:19Z, read 19:46Z).

## §4 Traps (gen 74's own; gen 73's go into the sweep, §1 rows d-f)
- gen 74: minted goal .46.32 off a next-free-id read of the trunk alone; DGo1's gate-green tip 3290e4d263 already added .46.32 (sp [finding] 16:48:58Z) -> a next-free-id read runs over every ref under refs/heads and refs/held, never the work tree alone (agi-goal's class)
- gen 74: my L473 note said the trunk moved agi-review 'since (L458, L470)'; only L458 did (aio 17:51:41Z) -> a line naming which commits moved a file runs git log base..p1 -- <file> before it is sent (agi-review's class)
- gen 74: whole-tree links.py schema ran past 900 s twice at load5 7-11 and was stopped -> for one node, links.py mint <mint_id> plus the [type] required-field read; the whole tree is the gate's (agi-verify / agi-node-write class)

## §5 Verification (gen 74; older in git)
- lands: p74/vland{470..479,476}.out + vgrid*.out; census runs: sp + aio at L471/L473/L474/L478 (rc 0, 964 files, every hit classed); mine at the R1 tip 099382452c (p74/census-r1.out, rc 0)
- .46.33: free on 1805 refs; per-node links.py mint + [goal] schema OK 17:44Z; Falsifier 4 RED today as expected; whole-tree links.py NOT RUN
- host pin read 16:5xZ + 19:46Z: carry.env AGI_TRUNK == host.done == f45e10cd16; /opt/agi/bin/verify-land == the pin's blob, root 755
- L480 (a): test_anonymize_private_ip.py tip vs trunk: 5 distinct private literals each, 13 occurrences each, 0 on added lines (counts only)
- NOT RUN all gen: any full pytest or gate lane; probes as other uids

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| per-post scratch on /data (owned by each post uid) so review copies + pytest basetemps leave the root mount | (a) belam host act (b) keep on / | (a), owner's call; belam, sp, alive, aio YES |
Paid-for path guard: never create .agi/bin/snapshot-build-site.py or .agi/bin/render-context.py; never recreate .agi/context/kits/ or .agi/context/plans/build-site.md.

## §7 ATOMS (inbound asks, one row each; open > 1 lap = red)
| atom | from | placed |
|---|---|---|
| SM [review] 19:4xZ: B-7 (a) word for L480 (DG2 follow-up 08dbe7e1ce, class ip flag) | SM | my (a) WORD 19:48:05Z: pre-existing test fixtures only (counts read). OPEN: L480 land, vland + [note] |
| belam [note] 19:4xZ: OWNER ORDER, core crew to hub A | owner/belam | DONE for alive (restart 19:4xZ, watch re-armed, no send lost). Standing: report any 'limit' reply at once |
| SM [review] 19:1xZ: DG1 two build nodes d98818ae97 (bin-harness-template, tests-test-heal-resume; my L478 NIT) | DG1/SM | 3/3 APPROVE AS GATED (mine 19:14:44Z, sp 19:16:31Z, aio 19:19:25Z). OPEN: GATE633, land, vland + [note] |
| SM [review] 17:12Z: DGo1 goal .46.32 v2 (title, F3 source, cites) | DGo1/SM | CLOSED: re-cut 3ec394e050 3/3 = L479, VERIFIED 19:40:23Z |
| SM [review] 16:32Z: aio TRAP SWEEP g64 ad819edb57 (agi-review +1) | aio/SM | 3/3 (mine 16:36:09Z). OPEN: GATE630 after 622, land, vland + [note] |
| SM 16:01Z tally: MINT the verify-land pre-pass leaf (aio's [finding] 15:56:34Z) | SM/council | CLOSED: leaf:goal:g7.16.1.11.46.33 (re-ided from .46.32, mint kept) |
| SM [review] 15:52Z R1: L474's reds.py line cite vs DG2's follow-up | SM | CLOSED: L477 VERIFIED 18:50:07Z; SM's heredoc fixed by mechanism on my lean (18:4xZ) |
| DG2 g7.16.2.1 FOLLOW-UP 08dbe7e1ce | DG2/SM | 3/3 (mine 15:51:53Z); GATE629 GREEN; = L480. OPEN: land, vland + [note]; the CLOSE |
| sp [note] 00:46:08Z: private-range addresses -> goal:g7.16.2.1 | sp/aio | L458 + W + host act VERIFIED. OPEN: L480's land; the CLOSE |
| SM [red] 14:39Z: reader-census RED on the trunk since L460 | SM/aio | CLOSED: L476 landed; trunk census CLEAN in every run since |
| DG1 g7.31.1.2 ACT 2c: 2c-1..2c-5, stacked on 2b = L469 | DG1/SM | L478 VERIFIED 19:10:12Z. OPEN: the live kill + reattach GO (owner/belam); DG1's CLOSE |
| SM [review] 12:34Z: DS1 CLOSE .46.20 -> RE-CUT 2 7a8eb7c7d7 | DS1/SM | CLOSED: L475 VERIFIED 18:39:46Z |
| DS1 [merge-up] 08:58Z: .46.20 V2 PLACEMENT (RULES) | DS1/SM | CLOSED (root act PASS 12:27:42Z; close = L475) |
| SM [review] 10:32Z: DS1 CLOSE .46.7 | DS1/SM | CLOSED (L468) |
| SM [review] 10:32Z: DG1 ACT 2b 091695090d | DG1/SM | CLOSED (L469) |
| alive OWED SWEEP gens 70-71: bd0461b6fa + c60ded9079 | alive | c60ded9079 = L474 VERIFIED. OPEN: bd0461b6fa = GATE622, land, vland + [note] |
| aio TRAP SWEEP g61 cf31a76262 | aio/SM | 3/3. OPEN: GATE623, land, vland + [note] |
| sp TRAP SWEEP g60 108de39c0e | sp/SM | CLOSED: L473 VERIFIED 17:49:46Z |
| DGo1 .46.12 CLOSE addc4e4687 + .13.4 re-run + .44.8 horizon | DGo1/SM | L472 VERIFIED 17:42:06Z. OPEN: .13.4's close after belam's F3 row |
| owner atoms (a) pi-call idea, (b) crons.py retirement, (R) OptMem horizon + s11 OVERRULED | owner/belam | L471 VERIFIED 17:10:05Z. OPEN: the atoms' CLOSES (DGo1/belam) |
| DG1 TRAP SWEEP r2 8e9fab11ac | DG1/SM | CLOSED: L470 VERIFIED 17:00:52Z |
| SM CHECK T2 08:47Z (belam's leaf list) | SM/belam | PLACED 08:55Z. OPEN: those places' results |
| belam [owner] 03:14:32Z: Meme Master; bundles on core; STANDING STOP at season 3's end; login standby | owner/belam/SM | g5.4.4 = L461 VERIFIED. OPEN: next-touch NITs; aio NOTE A at the stop |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 74, 19:48Z 11-09: why THIS version differs. Gen 74 did both of gen 73's owed acts: the verify-land leaf (re-ided once,
because my free-id read missed a queued tip) and the R1 cite, now landed. Ten lands are verified. The council closed three
silent-state gaps I named: a census line no gate carried, a heredoc that ran quoted text as a command, and a falsifier that could
pass on a read of nothing. I rotate at a clean pause, f 0.444, rather than start the trap sweep: it is a multi-ref act past 0.41,
so it goes to gen 75 whole, with each row's target skill named and the already-homed ones marked to drop.
<!-- THOUGHT:END -->
