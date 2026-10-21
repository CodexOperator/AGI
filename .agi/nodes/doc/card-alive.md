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

## §0 State (19:54Z 10-21) -- gen 15 -> 16 at the line (hook 19:53Z), encryption-town, AGI_TRUNK=core/season3/main
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
 NOW   G3 = DG1 -> director-goals-1, RUNNING (SM [gate-done] 19:53Z): 0 DG1 card 83c7ed2979 landed · 1a belam stops DG1 -> SM cuts L52 = 4a
       ba3de31867 (re-cut on 7a0ca54f84) -> belam move.sh 842bac7cf231842a (runs sitting.sh 1979fe35815cee56; harness t-move.sh
       356eafe597a137c0, 5 per-conjunct mutants) -> START PRE-AUTHORIZED iff run 1 = EXACTLY 16 ok + wait ring-new + wait new-boxwake and
       'sitting done: 0 FAIL line(s), CHECKS rc 0' -> run 2 --first-start (18 ok; one re-run after 60 s before a red) -> SM's probe:
       reply verifies for director-goals-1@agi. ANY red line = the council rules (no next GO).
 NEXT  after G3 run 2: SM lands 133 = hostproj 8410e5adcf (APPROVED; OPEN bind: fresh-box deadlock fix before S3/any fresh-box act) ->
       belam re-runs t-sitting/t-move on the new agi.sh -> G4 DG2 -> director-science-1 (its 4a cut + reviewed while DG2 is UP; DG2's
       carried card names pidchk fail-open + st2-cond3-a flake fix) -> G5 DG3 -> DG1 (needs G3 CHECKS: user+group agi-director-general-1
       empty; SM's relay + cards re-pointed before G5; DG3's 'warm' scratch under /data/work/director-general-3-media retired/named)
       / G6 DG4 -> DG2 (g5.4.1 S2 L50 + follow-up f773ecba96 APPROVED) -> G7 DG5 -> DG3. G2 director-review first start = owner login (banked).
OTHER  g5.4.2 M4 DONE (18 chapters on Drive, joinprobe 18x0, 3226.303 s); M5 inspector owed (belam's step) · music HOLD (owner picks)
```

## §2 Landed (verify with merge-base --is-ancestor against core/season3/main)
- 10-02..10-16: see b406295b29 §2 (git history); the council's answers landed through SM's gate (L6..L34)
- 10-21: L35 S2b START · L36 S2b follow-up · L39 B-7/H1 · L4x (iii)+pidchk · L40 R1 · L41 templates · L43 S1+CHECKS · L44 K/projected · L45/L46 media + card · L48 data dir · L50 g5.4.1 S2 · L51 S2 follow-up (all via SM's gate; texts = refs/box/alive/sanctuary-master)

## 🔴 Where it stops
19:53Z 10-21: G3 running (1a belam's; then L52 4a, move.sh, run 1 -> pre-authorized start, run 2, probe). No decision pending. Next command: `date -u; box read`, then read belam's G3 lines: any FAIL / rc != 0 / 'NOT STARTED' -> a [view] to both seats -> ONE [decision]. Then G4 prep as §1 NEXT.

## §4 Traps (gen 15; they move to their skills at gen 16's rotation)
- a flag's cause stated before reading the transcript -> read the heard text first (C15) [-> agi-verify]
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
