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

## §0 State (02:5xZ 10-24, goal .46 WAVE 1 building) -- gen 17 SEATED 02:53Z (gen 16 rotated 02:5xZ), encryption-town, AGI_TRUNK=core/season3/main
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code opus-5-5 · encryption-town |
| GOAL NOW | goal:g7.16.1.11.46 (owner brainstorm bundle, waves 0-4; one council brief per wave). WAVE 1 leaves .46.2-.46.12, gate line = M1-M4 + C1-C3 falsifiers pass + P1's numbers on the board |
| role | alive = the ANSWERER, the one voice back to SM; SM sends [review]/[question]/[relay]/[red]; never box belam |
| messaging | `box send <post> < file` from ~/t only; text in a scratch FILE via a QUOTED heredoc; STAMP = `date -u +%H:%M:%SZ` at send |
| council rules | VIEW to both seats -> ONE [decision] after both answered my LAST position, or 15 min; [withdraw] = change of mind; never end a turn with a decision pending: keep a background mail watcher |
| how I review | git first: %G? G, gated tree == merge-tree(live posts/belam, tip) or differs only by disjoint PATHS; home/host scan; read the bytes; a mutant per claim; a falsifier that passes on nothing = RED |
| lens | vision:alive: the system reports its TRUE state; a silent skip, a vacuous pass, a false line -> RED |
| skills | agi-goal · agi-send · agi-rotate · agi-verify · agi-master-gate (SM's side) · agi-memory-guard |

## §1 Plan (wave 1 of goal .46; leaves written by alive at L74/L78, amended L79/L86)
```
LEAF        DIRECTOR   STATE (02:5xZ 10-24)
.46.2-.5 M  DG2        .46.2 .46.4 CLOSED; .46.5 close GO (after L95); .46.3 open (L95 caller GO-fixed + live leg)
.46.6-.8 C  DS1        L82 + L87 LANDED; agi-cred INSTALLED by belam 02:31Z; credits_live false; passed except Doppler token / workspaces / live leg
.46.9 P1    DG3        part 1 L80, part 2 + mint driver L84, kid launch L89, R1-R4+P0+fixes L91 48cb160d02 LANDED; arms: HALT cleared by owner top-up; ONE smoke key GO (06:1xZ). was: kid-launch (honest bounds rows: max_live 2,
                       $0.50 cap + TTL read back, kid-done disable+remove; THOUGHT "no kid-to-kid isolation under one uid"; F1 secret-not-on-stdout,
                       F2 MintedKey.secret repr=False). FROZEN 5 leaves: g4.18.2.1 g7.31.3.1 g7.32.3 g4.21 g7.32.1; base 77ac751723.
                       L84's LIVE RED (p1_segment root) FIXED: stack 88 947d1e2845
.46.10 U1   dg1        L81 + L83 + L85 LANDED (report mode; standing rows by closure, DG3 only, until .46.9)
.46.11 V10a SM         DONE (L75-L77); V10b = wave 3; closed-record exclusion banked for the owner
.46.12      dg1        L94 7494c88b99 LANDED (N1-N5); seeded; cron BANKED owner GO; reader classify tip next
Race (L73/L75/L79): R1 SM reads posts/belam at cut; R2 cut step refuses :20-:30; R3 banked = board-only re-merge in belam's land (trigger: a race under R1+R2)
```

## §2 Landed (10-23..10-24, all via SM's gate; texts = refs/box/alive/sanctuary-master)
L74 wave-1 leaves · L75-L77 V10a + close · L78 .46.12 · L79 .46.9 amend (frozen list, base rule) · L80 P1 part 1 · L81 U1 · L82 C1-C3 · L83/L85 U1 rows · L84 P1 part 2 · L86 .46.9 wording · L87 agi-cred check fix · L88 = p1_segment fix (stack 88, 947d1e2845) · belam RULES F1 7394e73c50 · decisions by content: DG2 re-cut GO-fixed (02:5xZ), DG3 kid launch c6c2960dc2 arms gated R1-R4 (03:0xZ), .46.12 3c5f122133 fixed N1-N5 (03:1xZ)

## 🔴 Where it stops
06:3xZ 10-24: [decision] SENT (3/3) on SM's [done] (belam [red] 3): the prereq_notice row WENT LIVE in SM's crontab (no mail sent; SM removed it) because crons.md says enabled: true and any apply as SM installs own bound rows; our "only --sudo on owner GO" bank was prose. C-1 enabled: false NOW via SM's gate (rule: banked start = enabled false); C-2 no sudo without --sudo (plain apply execs `sudo -n` today, :1413/:1517); suite LEAK cause: tests apply without --user-crontab-dir -> foreign users via sudo -> real crontab; check agi-belam's crontab; C-3 leaf to the crons.py owner (fixture seam, C-2, refuse non-MAIN project blocks).
P1: W-1 applies (workspace agi-local-town e31711fe...); DG3 tip = cell + p0 (g); then fresh p0, ONE key, STOP.
ROUTED 06:3xZ: C-1 cut de1c8dea89 (SM gating); C-2+C-3 -> dg1 after its reader tip 4b78386364; belam: 0 agi-suite lines box-wide, leak = a Prime verify pass (agi-belam uid) on or before 10-21, no suite in that uid until C-3. NEXT ACT: review C-1 cell land, DG3's workspace+p0(g) tip, dg1's reader+notices tip, the crons leaf; then the smoke [result]. L95 then .46.5 close. `cd ~/t; date -u; box read`; watcher = background `box n` loop.

## §4 Traps (gen 17)
- Sending a [decision] while the seats' newest words are unread: 06:18:48Z crossed two words that had moved on my own reading -> a wrong decision, superseded within a minute. `box read` IMMEDIATELY before every [decision] send, in the same call.
- `pkill -f <pattern>` in the SAME bash call kills that call's own shell (exit 144) and every command after it: twice today (a card edit, then 2 of 3 decision sends). Kill a watcher by its task id, or run pkill alone; after a 144, read refs/box/alive/<post> before re-sending.

## §5 Verification (10-24)
- 01:5xZ L85 tree 88f2dbea97 = merge-tree(1b11ff5f47, 65ae608d35); gated b270c029ca + town line + L84's 5 paths
- 00:15Z .46.9 F2/F3 negatives run on the trunk; U1 row check prints 15 (not done) -> correct pre-state
- 02:4xZ agi-cred live line `posts 10 pids 190 read 190 gone 0 key-hits 0` (belam's install report)

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| gen 13-16 §4 traps -> their skills (texts at 2fc483e18e, b406295b29 and 96eb6cffbe §4) | (a) one small stack via SM (skills/ is gated) (b) drop | (a) |
| agi-carry@ dead weight under engine v4 | DG5/science-1 read later | read, then retire if dead |
Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 16 -> 17, 02:5xZ 10-24 (date -u), at the line: wave 1 of goal .46 is mostly landed; this card carries the per-leaf state, the open reviews and the race rule, so gen 17 reads SM's next [review]s against bytes. The gen-15/16 §4 traps move to §6's bank (one skills stack), per the one-rotation trap rule.
<!-- THOUGHT:END -->
