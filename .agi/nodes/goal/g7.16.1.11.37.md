---
id: goal:g7.16.1.11.37
mint_id: 83524e9705aa48f6b913d99f71697031
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.37
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
seeds: []
tags: []
role: director
scaffold_hash: c79775bfb5f9e079
season: 2
status: complete
title: "G7.16.1.11.37: AGI_SEAT is retired -- a post unit carries AGI_POST and AGI_BOX from its row, and every reader takes AGI_POST"
town: core
---
# goal:g7.16.1.11.37

# G7.16.1.11.37: AGI_SEAT is retired -- a post unit carries AGI_POST and AGI_BOX from its row, and every reader takes AGI_POST

## Why this exists
OWNER, verbatim (02:4xZ 10-11, via belam-s2-III): "Bad we fix the post issue agi seat shouldn't be used anymore unless absolutely needed. The post should include all relevant info including box location".
Cause (belam): the live /run/systemd/system/agi-post@.service is agi-boot's 10-01 render and sets AGI_SEAT=%i only; engine-root.md's AGI_POST=%i was never re-rendered. So agi-at / agi-turn (which need AGI_POST) printed [no-branch] in every pane (sanctuary-master 83x, DG3 55x), and box needed a hand-set AGI_POST. The live half is belam's host act, already done: the drop-in agi-post@.service.d/52-post-env.conf = Environment=AGI_POST=%i (299337b255, extensions/agi/guard/post-env), with each post restarted while idle. This leaf is the CODE half. belam placed it with sanctuary-master ("YOURS TO PLACE"), which lanes it under the g7.16.1.11.11 HOLD (identity). As usual, the council approves the landing.

## Target end-state (counts measured on 299337b255)
1. THE UNIT: engine-root.md's agi-post@ unit (:28 already sets AGI_SEAT=%i AGI_POST=%i; the live RENDER is what is stale) drops AGI_SEAT. AGI_BOX keeps ONE source, this box's own env file (boxes.py:7: AGI_BOX names THIS box; rotate stamps the row from it). The unit compares it with the post's config:posts row `box` and REFUSES on a mismatch with `[wrong-box] row=<x> here=<y>`; it never sets AGI_BOX from the row. Retiring 52-post-env = two GOs in order (belam's host acts): re-render the unit, read a running post's env and run the (4) lane in it, THEN retire the drop-in. Never the drop-in first: a gap repeats the [no-branch] blackout.
2. THE ENGINE PIECES read $AGI_POST with NO fallback (they run only inside a v5 unit): engine-post agi-captive (:23 p=$AGI_SEAT), agi-out (:153), engine-wrap agi-run (:23 :25 :26 :28; :26 and :28 already read ${AGI_POST:-$AGI_SEAT}), the pi extension (:44 :45), and the kid line (:70 sets both). The prose history rows (engine-wrap :92 :93) stay as written.
3. PYTHON reads AGI_POST first and falls back to AGI_SEAT only for a v4 row, through ONE named helper. Today there are 56 AGI_SEAT hits in 13 non-test files: adapters/claude_code_adapter 2, commands 1, dispatch 12, geometry_config 8, last_act 3, rotate 15, season 1, send 4, suite_guards 1, verification 1, viewport 1, write 3, hooks/rotation_alert 4 (the hook belam's list did not name). The fallback is retired in the commit that moves the last v4 row to v5.
4. A LANE: a post started with AGI_POST (+ AGI_BOX) only, and no AGI_SEAT in its env, runs box, agi-at, agi-turn, agi-captive and agi-out green.
5. (moved 10-11 by the council, alive 02:5xZ 3/3: the agi-flush strand is its own leaf, goal:g7.16.1.11.38, outside this HOLD)
6. THE DROP-INS (council 35f28334ef, alive 03:3xZ, 3/3, measured by all three; .34's ADJUST routed here): the live agi-post@ unit carries 3 host drop-ins. 50-signers-repoint (ExecStartPre=-+/usr/local/sbin/agi-signers-repoint %i) and 51-no-session-bus (.34's DBUS_SESSION_BUS_ADDRESS=disabled: fix) have NO source in .geometry (git grep 'signers-repoint|DBUS' over .geometry = 0); 52-post-env is this leaf's. engine-root.md becomes the ONE source: it renders the unit AND names its drop-ins as a list, or folds them into the unit. Until it does, a re-render 'to match the node' silently drops the session-bus fix and the signers repoint (belam told 03:3xZ: do not re-render from the node yet).
7. C2, DONE (belam, 10-11 10:28Z, in the same act as step 3 of the host list; council 3/3 10:10Z asked for it): the 50/51/52 drop-in SOURCES retired with the drop-in retire -- moved, never deleted -- to extensions/agi/guard/deprecated/ (541677b58b; agi-signers-repoint stays), the live drop-ins to /var/backups/agi-dropins-retired-20261011T102822Z. Host order as run: land -> re-render (10:15Z) -> `ENVFROM=/proc/<pid>/environ sh extensions/agi/tests/post-env.t.sh` in real environs (95847b8fa6: l1 e1 e1b ok, only f6c red) -> .40.1 F1 re-run (PROOF 2 PROVEN) -> retire -> `HOSTDIR=/etc/systemd/system/agi-post@.service.d sh extensions/agi/tests/post-env.t.sh` (f6c green). What stays open is not C2: 9 posts still run the old env until their next start (l1 goes green then).

## Invariants
- A v4 row keeps working until it moves: the fallback lives in the one helper and nowhere else.
- No new round on key / signing / rotate / spawn-row / write-gate rides this leaf (the g7.16.1.11.11 HOLD). Only the env name changes.
- A host act (the unit re-render, the drop-in retire, restarts) = belam's GO per act.

## Falsifier
1. The fenced pieces of `.agi/nodes/.geometry/engine*.md` contain 0 hits for `AGI_SEAT` (the prose rows are not counted).
2. `git grep -n AGI_SEAT -- 'extensions/agi/bin/*.py' 'extensions/agi/bin/adapters/*.py' 'extensions/agi/hooks/*.py'` hits only the one helper, plus its v4-row comment.
3. The lane in (4) goes RED under each mutant: the helper reads AGI_SEAT first; agi-captive's p= reads AGI_SEAT again; the unit sets no AGI_BOX; the row's box != this box and the post starts anyway.
4. With AGI_SEAT unset, `box read` as a post works with no hand-set AGI_POST.
5. (moved to goal:g7.16.1.11.38)
6. (host read, belam's) the live agi-post@ unit + its drop-ins == the render of engine-root.md + its named drop-in list; an UNLISTED drop-in = RED. RED today (50 and 51 are unlisted). MUTANT: a re-render without DBUS_SESSION_BUS_ADDRESS=disabled: = RED.
7. (host read, belam's, at the re-render GO; council remark on goal:g7.16.1.11.40.1, self-perpetuating 05:5xZ) goal:g7.16.1.11.40.1 Falsifier 1 is re-run on the live box AFTER the re-render: 0 pids on the wrong side of the guard, every unit's harness found. The re-rendered ExecStart keeps the shape the guard reads, `script > sh -c agi-run > strace > harness` (measured on the live unit 10-11: script's parent is systemd, `sh -c agi-run` is script's child and execs strace, the harness is strace's child, the `agi-run` loops are strace's other children): the cut adds only `export AGI_BOX=$(sed ...)` before the exec, whose sed runs in a subshell that exits first.

## Out of scope
Renaming seat-era python identifiers (`seat` variables) beyond the env read · the v4 -> v5 row moves themselves · goal:g7.16.1.11.20.1 (the alert's receiver rule).

## Agent Notes
sanctuary-master gen 35 10-11: landed in 889a29eec4 (council alive 02:4xZ, 3/3), placed with DG4. This version folds in the council's remarks: one python helper; shell with no fallback; AGI_BOX from this box with a [wrong-box] refusal (all-is-one and alive, independently: setting it from the row makes two sources that point at each other, wrong mid box-move); the drop-in retire as two ordered GOs; the unit == render falsifier (self-perpetuating); Target 1's :28 cite corrected.

sanctuary-master 10-11 10:3xZ (HOST HALF DONE, belam's three GOs, read from belam's [landed] 10:3xZ): STEP 1 re-render 10:15Z -- carry.env pin c70e3ef313 -> b4e1afaf04 (backup /etc/agi/carry.env.pre-pin-20261011T101540Z; old-pin render == live /run byte-for-byte; old -> new changes ONLY agi-post@.service), 12 posts active. STEP 2 witness -- thought-master (10:16Z), self-perpetuating + director-general-2 (10:27Z) restarted on the new unit: post-env.t.sh LIVE (95847b8fa6) in each real environ = l1 ok (no AGI_SEAT), e1 + e1b ok, only f6c red. STEP 3 drop-in retire 10:28Z: 50/51/52 MOVED to /var/backups/agi-dropins-retired-20261011T102822Z, daemon-reload rc 0, HOSTDIR lane f6c ok (0 FAIL); C2 in the same act: the 3 sources moved to extensions/agi/guard/deprecated/ (541677b58b; agi-signers-repoint stays). F6 GREEN (live unit + drop-ins == the render, 0 unlisted). F7 GREEN: .40.1 Falsifier 1 re-run on the re-rendered unit = PROOF 2 PROVEN (208 / 213 pids, 0 wrong side). 9 posts still run the old env until their next start (l1 goes green then). Rollback: the 3 files back + daemon-reload; the pin backup restores the old unit. Engine half: DG4's 3dcfebbc8b (the council's 5 remarks) still owed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-11 (director-general-4, belam's CHECK via SM gen 38: can .37 CLOSE; F1-F7 run as written on the live trunk 0c99755883, bare env -i, niced, sh): COMPLETE.
F1 GREEN: the ~~~ bodies of every engine*.md hold 0 AGI_SEAT hits (awk, and post-env u3). F2 GREEN: git grep AGI_SEAT over bin/*.py, adapters/*.py, hooks/*.py = 2 hits, both in geometry_config.py (the helper: the deprecation note :58 and the one fallback read :138).
F3 GREEN with ONE named difference: post-env.t.sh goes RED under the helper-reads-AGI_SEAT-first mutant (m5), the unit-sets-no-AGI_BOX mutant (m2b) and the wrong-box-starts-anyway mutant (m1); the fourth, "agi-captive's p= reads AGI_SEAT again", has no code to mutate -- the live agi-captive piece reads no seat env at all (no p=, no AGI_POST, no AGI_SEAT) -- so the lane's stand-ins are m3 / m4 (agi-at and agi-turn with P=$AGI_SEAT, both RED, rc 5). F4 GREEN: with AGI_SEAT unset, `box read` as a post (e1 / e1b, the pieces under the unit's own env) works with no hand-set AGI_POST. F5 moved to .38.
F6 GREEN: the live /run/systemd/system/agi-post@.service is BYTE-IDENTICAL (cmp, 3006 B) to the render of engine-root.md at the trunk; /etc/systemd/system/agi-post@.service.d holds 0 *.conf (post-env HOSTDIR: f6a f6b f6w f6c ok); the DBUS mutant (m6) RED. F7 GREEN: agi-memguard.service active; memguard-proof2.py against /usr/local/sbin/agi-memguard.py exits 0 = 204 pids over 12 units, 35 younger than 11 s skipped, 0 on the wrong side (.40.1 Falsifier 1 on the re-rendered unit).
What stays open is a STATE, not a gate: the posts that started before the re-render still run the old environ (AGI_SEAT in it; post-env LIVE l1 red in each) until their next start. C2 (the 50/51/52 sources) was done by belam 10:28Z (541677b58b).
Folded into this same commit (SM's placement 12:1xZ, council remark, alive): a posts.md that git shows and jq parses but whose rows sed no longer finds (the '  - {' prefix moved) gave jq EMPTY input -> exit 0, b='' -> the exit-2 [wrong-box] skip on EVERY post. The unit now COUNTS the rows sed would find: 0 rows -> '[trunk-unreadable] posts.md has no rows at <trunk>', exit 255. post-env ROW w7 + MUTANT m9 (the count dropped -> exit 2, RED). Unit 3006 -> 3189 B (heading + engine.md map row).
F6 RE-READ 10-11 14:43Z (director-general-4, the council remark sp 14:25Z; belam pinned the 3189 B render, live unit mtime 14:32Z): the render of engine-root.md at the trunk 3414817ae2 (the '### agi-post@.service' piece, fence and 2 head lines dropped) is BYTE-IDENTICAL (cmp) to /run/systemd/system/agi-post@.service, 3189 B both; /etc/systemd/system/agi-post@.service.d holds 0 files; the zero-rows guard ('has no rows') is in the live unit. F6 now holds as a reading of the pinned render, not only of the 3006 B one.
<!-- THOUGHT:END -->
