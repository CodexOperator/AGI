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

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (19:39Z 10-22, .45 CLOSED; .44.8 F1 nspawn design decided) -- gen 16 (seated 19:55Z), encryption-town, AGI_TRUNK=core/season3/main
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code opus-5-5 · encryption-town |
| GOAL NOW | goal:g7.16.1.11.45 THE POST SHUFFLE (owner GO 14:4xZ: "Use the council to help coordinate the move"): the COUNCIL owns the schedule G0-G7 and each per-post GO, through SM; plus the season-3 reviews |
| role | alive = the ANSWERER, the one voice back to SM; SM sends [review]/[design-ask]/[relay]/[note]; never box belam |
| messaging | `box send <post> < file` from ~/t only; text in a scratch FILE via a QUOTED heredoc; STAMP = `date -u +%H:%M:%SZ` at send. Old mail: `git log -1 --format=%B refs/box/<from>/<to>` |
| council rules | VIEW to both seats -> ONE [decision] after both answered my LAST position, or 15 min; [withdraw] = change of mind; one-line [correction]; never end a turn with a decision pending: a background watcher (both seat refs moved OR the mark) |
| how I review | git first: %G? all G, gate land tree == merge-tree(parent1, tip), live merge-tree clean, home scan ('/home/', '/var/lib/agi/<post>/', bare '~/'); read the bytes (belam's ~/tools is 644: READ it); a mutant per claim |
| lens | vision:alive: the system reports its TRUE state; a silent skip, a vacuous pass, a false line -> RED |
| skills | agi-post · agi-send · agi-goal · agi-rotate · agi-verify · agi-master-gate (SM's side) · agi-memory-guard |

## §1 Plan
```
.45 SCHEDULE (council decisions 15:25Z + 15:26Z addendum + later):
 DONE  G0 (L40 R1 boot false TM/DT-1 · L41 templates · L43 S1 director-review row + CHECKS · L44 K-a/b/c · 'projected' · media L45/L46
       + data dir L48 moved to /data/work/media/season3, chown agi-director-review) · G1 TM + DT-1 down · G1b pin a18c484bc4 (host: met;
       agi-project.path NEVER armed here -> projection is EXPLICIT; belam ran it 17:59Z) · rollback /var/backups/agi-act-20261021T175530Z KEPT
 DONE  G4 binds d5122b2619; L54 hostproj; G4 L55 8a9d18ec9c; G5 L57 69e36d2286; G6 L58 61e90435d0; L59/L60; G7 step 0 d55e87c446.
 DONE  G7 DONE 05:19Z, verified: probe key on ring L76 OPEN only; NRestarts 0; gate dir uid 977; L61 8b247882a2.
 DONE  OWNER 05:0xZ (via belam 08:43Z): "let me know when all currently active season goal leaves are complete ... report ... go idle".
       .44.8 (A) 08:46:02Z (F0 + RT2; owner legs banked) · .44.7 (B) 08:46:15Z (live half = first box move; census vacuous).
 DONE  .44.8.1 banked by name (09:03Z) · g5.34 complete (61aabca57a + fdb4072072) · L67+L68 GO 09:25:48Z.
 DONE  L67+L68 on origin; .45 ACTIVE (F1 10/11, director-review = owner login) [decision] 09:43:32Z + report lines.
 DONE  GATE154: 9751 passed, 5 failed = C6 only, links 0. FINAL rule 10:04:22Z f88af83aa9: fixed lane in SM's template + council
       refuses a gate report without the grid-writers count; one skill line replaces :256/:271.
 DONE  L69 (C6 re-cut + skill line, tip 177ba5cf44) GO 3/3 [decision] 10:19:24Z 82abd765a9; GATE158 grid-writers 27/0 = (b) passes.
 DONE  L69 f5e112665c LANDED, test_grid_writers 27/0 on trunk; owner's season report sent by belam.
 DONE  L70 landed; .45 CLOSE landed 73a32e5567 (status complete on trunk 419ee55128).
 NOW   .44.8 F1 nspawn (OWNER GO 19:34Z): design 3/3 19:38:34Z; R1/R2 3/3 19:45:00Z: M1 = 3 markers (detect-virt, rootfs, MAIN/.git);
       REAL BUG agi.sh:280 rows() no boot filter -> fresh start = 13 (thought-master, director-thought-1): verdict (i) RT2 + (ii) set==11 FAIL.
```

## §2 Landed (verify with merge-base --is-ancestor against core/season3/main)
- 10-02..10-16: see b406295b29 §2 (git history); the council's answers landed through SM's gate (L6..L34)
- 10-21: L35 S2b START · L36 S2b follow-up · L39 B-7/H1 · L4x (iii)+pidchk · L40 R1 · L41 templates · L43 S1+CHECKS · L44 K/projected · L45/L46 media + card · L48 data dir · L50 g5.4.1 S2 · L51 S2 follow-up (all via SM's gate; texts = refs/box/alive/sanctuary-master)

## 🔴 Where it stops
22:25Z 10-23: L74 LANDED 6b6f926c0d (wave-1 leaves .46.2-.46.10). L75 = V10a (.46.11, sm/v10a 2ced1f2982) [decision] GO 3/3 sent ~22:25Z: land tree 5bd3a99db3 = GATE168 temp ff3fa08774's tree; AGI_SEAT=0 outside 4 explicit paths. Follow-ups: F1 drop the skipif (guard fails open off-git) as SM's one-line land soon; F2 _print_once dead param -> V10b. Wave 1 builds: DG2 M1-M4 · science-1 C1-C3 · DG3 P1 · goals-1 U1. NEXT: read L75 cut / follow-up reviews; wave-2 brief only after the wave-1 gate line. `cd ~/t; date -u; box read`.

## §4 Traps (gen 15; they move to their skills at gen 16's rotation)
- a flag's cause stated before reading the transcript -> read the heard text first (C15, re-hit L70 stamp) [-> agi-verify]
- a mutant I PREDICT -> label it a prediction (M5 a1) [-> agi-verify]
- a union agreed but not sent -> the [decision] in the SAME turn as the last YES; never end a turn with one pending: start a background watcher [-> agi-send]
- a hole claimed at a sink -> trace the input through EVERY earlier refusal first (.42.2 R1, rule (m)) [-> agi-verify]
- a message's stamp -> `date -u` at send, never an estimate [-> agi-send]
- a home-path scan -> '/home/' AND '/var/lib/agi/<post>/' AND bare '~/' (SM's gate missed DG3's 3 lines); read what a tool already refuses before adding a rule on top (my inverted (d) clause) [-> agi-verify]
- a seat's objection after the decision -> read the unit's bytes BEFORE withdrawing (16:34Z: two extra mails) [-> agi-send]
- a design that moves refs between names -> read every reader/writer for a signer-equals-name check (box :329/:337 'squatted'; my 14:44Z step 3) [-> agi-post]
- "I cannot read X" -> ls -l it first (belam's ~/tools is 644; I claimed otherwise at 19:32Z) [-> agi-verify]
- a unit's FILE is not its STATE -> systemctl show (agi-project.path never active; G1b's host: met was a false green) [-> agi-verify]

## §5 Verification (10-21)
- 23:13Z G6 4a: off-matrix 31 passed, mutant OLD_NAMES w/o free names -> 2 FAIL; 0 dup session_names; land tree = live merge-tree
- 22:22Z ring check by per-line fingerprint (a grep of base64 into ssh-keygen -lf is VACUOUS: wrong format, 0 by construction)
- 22:15Z G5 4a: onto live = 7 paths; off-matrix 16 passed, mutant became->dg-9 -> 6 FAIL
- 21:50Z DG3 worktrees t,w-40,w-sg unlocked (porcelain); name-dirs 87 passed, mutant no leftover test -> 3 RED; land e2f5890f11 tree = seq merge-tree
- 21:40Z git 2.43.0 scratch: bare `worktree repair` after a parent mv = rc 0, no change; named paths fix it, lock kept
- 21:35Z move.sh :24 run 1 rows=18 hard; :30 run 2 rc only (a --first-start row is free)
- 21:33Z ls -ld /data/work: gate-director-general-1 agi-director-goals-1, -2 agi-director-science-1, -3 + director-general-3-media agi-director-general-3
- 21:1xZ G4 4a: rows json-read; off-matrix 15 passed on tip, mutant retired box on -> 1 FAIL; step0 card 2 '---'
- 20:47Z sitting.sh :16 AGISH/CHECKS=$CO (the PIN's checkout); L54 tree 8ab63a6b48 = merge-tree(c3f05c17c1, 331abbea75); agi.sh@2ebb270242 6c2bf128ec7f0a5a
- 20:2xZ hostproj 331abbea75: lane 114/0 on archive, fresh() die mutant f3 RED; d5122b2619 81 passed, NRestarts mutant 2 RED; t-sitting 12/12 on copies
- 20:05:26Z ac2fe5f815 G director-goals-1@agi JW5/zP4d; agi-post active/running NRestarts 10; L52 on trunk
- 19:59:48Z unit :17/:20 + agi-run :2 read: back-dated .fresh keeps the key, drops -c; out-refused absent
- 19:35Z t-move.sh 356eafe597a137c0 :50-:54 one conjunct per copy; move.sh 842bac7cf231842a, sitting.sh 1979fe35815cee56 (sha256 read here)
- 18:1xZ box :329 w() refuses a tip not signed 'for $P@agi'; :337 read checks the sender -> outbox NOT moved, inbox moved
- 17:57Z agi-project.path ActiveEnterTimestamp empty; its /run wants link dated 10-15 19:47; boot 10-12 05:00:51
- 16:2xZ find /etc/systemd /run/systemd/system -name '*director-general-1*' = 4 paths (no /etc .service.d)
- 16:54Z ~/bin/box byte-equal to the pin's box piece (2904 B); /opt/agi/bin/box was 2005 B (10-08)

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| gen 13's eight + gen 14's four §4 traps -> their skills | (a) one small stack via SM (skills/ is gated) (b) drop | (a): texts at 2fc483e18e §4 and b406295b29 §4 |
| agi-carry@ dead weight under engine v4 (no post has g.git) | DG5/science-1 read later | read, then retire the piece if dead |
Council banks: the host name in 12d991004a public history (owner's word only); engine-post.md ref-guard "MISTAKE" comment vs its fail-open; §Y2; dry run should probe push auth per target class; send.py ladder fallback names the wrong cause.
Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 15 -> 16, 19:54Z 10-21 (date -u), at the line: the shuffle's G0..G1b are done and G3 is running under a pre-authorized, code-matched start; the card now carries the schedule and the exact G3 gate so gen 16 reads belam's lines against bytes, not memory. Two new traps (unread file mode; unit file vs state) join gen 15's eight.
<!-- THOUGHT:END -->
