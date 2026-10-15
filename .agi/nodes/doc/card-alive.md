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

## §0 State (08:1xZ 10-15) -- gen 13, encryption-town, restarted 08:04:30Z on AGI_TRUNK=core/season3/main
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code opus-5-5 · encryption-town |
| GOAL NOW | owner 06:2xZ 10-14: close every goal:g7.16.1 bundle, then season rollover. ROLLOVER DONE 10-15 (below). Keepalive is IDLE-ONLY. Quiet rule to the owner (one digest per ~4 h via belam; [red] + blocking asks excepted) |
| role | the council rules + approves gated tips. SM sends `[review]` / `[decision]` / `[red]` / `[placement]`; TM sends research decisions; alive = the ANSWERER: the one voice back |
| messaging | never box belam; to SM one message per finished thing, NO acks. `box send <post> < file` (text in a scratch FILE); `box read` = unread; `box n` = unread count. Raw text of an old mail: `git log -1 --format=%B refs/box/<from>/alive` |
| council rules | VIEW to both seats -> ONE verdict after BOTH answered my LAST position, or 15 min (silence = no objection); a change of mind = [withdraw]; every view names what it RAN against which sha |
| how I review | git first (tree, merge-tree land tree pinned, %G? all G, no key path); tests only when agi.slice < 4600 MiB, from a `git archive` in the scratchpad (git init + add -f, env -i, empty HOME, nice 10); a mutant per claim |
| lens | vision:alive = the system reports its own TRUE state: a silent skip, a vacuous pass, a false line -> RED. A CLOSE never edits its falsifier |
| skills | agi-post · agi-send · agi-goal · agi-rotate · agi-verify · agi-master-gate (SM's side) · agi-memory-guard |

## §1 Plan
```
done   SEASON 2 -> 3 ROLLOVER, 10-14 18:0xZ .. 10-15 08:10Z (every step a 3/3 council verdict; texts in refs/box/alive/sanctuary-master):
         stacks L19-L25 + L22 (align) landed and verified; S20 RETURNed once (shared old branch half-roll, scratch repro) then approved
         owner words: --skip-fold core (fa6e39d06c) · (B) mains to the s3 line (254e170a81) · web-app-suite FF (deefc11cf0)
         freeze F-a da9deccaef (evidence_enforce, branch_push, graph_metrics_land) 05:59:52Z .. F-e 52d5fd9604 06:28:21Z
         DRY-1 refused (core cell 3 on season3/main) -> C1 a044b2bd45 -> DRY-2 rc 0 -> apply #1 STOP (DG4 uid no push credential,
           nothing changed) -> R1' agi-belam + per-process env helper: belam DRY == DG4 DRY (55/55, diffed) -> apply rc 0 06:21-06:24Z
         origin: HEADS 21 -> 20; 5 season2 heads deleted, archived refs/agi/archive/*season2/main; season3/main 2a8056bcb5 (6 G
           cells, ladder 3); master dc7ec920ba; B2 core/season3/main 0d9d94e01a (tree 227f1d06b6 == my prediction); switch
         L23 420e00ae9c (14 posts trunk cells -> core/season3/main; gate92 green, the 1 red flake run 3/3 x3 by me); pin 420e00ae9c;
           12/12 restarted (07:42-08:08Z, read 3 ways); B-3 08:09-08:10Z: core/main + sanctuary/streaming-suite/web-app-suite
           mains == 2a8056bcb5, 4 archive refs refs/agi/archive/<t>-main-pre-20261015T0809Z (verified by me 08:11Z)
         08:01Z goal .44/.44.7 LEFT OPEN (their F1/F4 need a real box move; the rollover ran none)
         L26 a93fe7cf36 (S26 23e62d425c, g5.4 +4/-0, owner line byte-equal to deefc11cf0; tree bfe132c3bb == merge-tree) verified 09:1xZ
         SEASON 3 OPENS (SM 19:22:25Z relay; nodes at 6596a7fc9d belam G): council DESIGN FIRST on two goals, both sent to SM 3/3:
           .44.8 agi.sh start/stop (writer aio, v2 + G reboot-proof stop + H signers ring) 19:36:41Z · g5.4.1 season report
           template (writer sp, v3 + H1 every head row) 19:37:12Z. Texts: refs/box/alive/sanctuary-master
         placed 19:38Z (.44.8 S1+S3 DG2, g5.4.1 S1 DG4); DG2's 5 questions answered 19:41:45Z; belam's 5 realm ASKs 19:44:00Z
           (+2 corrections 19:44Z): boot set = rows -> /run only, /etc links off BEFORE S1; F5 = sudoers byte-equal to a node source
         belam ASK 1 read back by me 19:50Z (fa3174300d 4 boot cells, pin, /run 12 /etc 0); .42.2 design 3/3 to SM 19:52:54Z
           (land_ok = is_own OR prime_node; .geometry/ + town/ gated; clean-merge rule). CARRY to .44.8 S2 review: S5 pubkey commit is gated
NEXT   SM places + gates both designs (S1..S3 stacks each): review each gated tip as usual
       · DG2 cuts .44.7 CLOSE on the first real box move (F1: section 6 + .39 counts per namespace, lane row + mutant RED); then .44
       · from now (P2') every PASS close ff-feeds core/main from season3/main: check the read-back core/main == season3/main
OPEN   banked to belam: MAIN's local local-maxxing/season2/main (da9deccaef) delete, all 12 read back
```

## §2 Landed (verify with merge-base --is-ancestor against core/season3/main)
- 10-02..10-08: 3a33c71b9 level rule · 9778def43 act1.sh · a7705f2d2 AA1.C · 1b4fdbe13 AA1.K · 5a1760e82 AA1.N · 01fb4669a3 AA1.S
  · 38986aa967 doc:rse-d1-nest v3 (D1) · eb55f973e2 A1b v3 (agi-vstore 856 B f60191fd...)
- 10-10/14: 24cdb55824 overview s2-loop-end-alive (my node) · the council's answers landed through SM's gate (L6..L25)

## 🔴 Where it stops
Season 3 is rolled and complete (SM 08:11Z, verified on origin by me). Nothing of alive's is half-done: no verdict pending.
Next command: `date -u; box read` on the next mail; expected: SM's placement of .44.8 / g5.4.1 stacks, DG2's .44.7 close, the first s3 PASS (core/main ff read-back).

## §4 Traps (gen 13; at my rotation each moves to the skill that owns its flow, one line, or is dropped)
- a box text with `backticks` -> write it with a QUOTED heredoc (<<'EOF'): unquoted, the shell RAN the spans and sent blanks (19:44Z 10-15) [-> agi-send]
- another uid's worktree under its private /tmp shows 'prunable' to me -> NEVER `git worktree prune` from my uid: it deletes a live
  worktree's metadata (06:27Z 10-15, belam's R1' r3) [-> agi-memory-guard]
- going idle for a restart -> stop my own watcher loop first: the idle gate waits on any child (SM's poll loop held its restart 10 min, 07:5xZ 10-15) [-> agi-post]
- a dry run that never pushes -> it proves nothing about push auth or branch rules; name the pushing uid and probe with `git push --dry-run` (apply #1 STOP 06:15Z 10-15) [-> agi-master-gate]
- a pre-run read (cells, board, judge) -> take it on the tree the run runs in, never the live trunk (DRY-1 refused 06:07Z 10-15: season3/main's core cell 3) [-> agi-master-gate]
- a THOUGHT line I worded for SM ('X ran / is done') -> read its tense against the ref it names before approving (S19 19:19Z 10-14)
- a number I credit to other seats -> name THEIR ref with it (S21 20:43Z 10-14)
- a run's rows -> check the fixture carries the run's REAL town set + argv (S20 23:46Z 10-14: 68/0 green, the real shape half-rolled)
- a "no record exists" claim -> grep the HISTORY too (`git log -G` of card-*.md) (07:0xZ 10-14)
- a command quoted in a box message -> read the raw `git log -1 --format=%B refs/box/<from>/<me>`; write commands with no backslash (16:0xZ 10-14)

## §5 Verification
- 10-15 09:11Z: L26 a93fe7cf36 G, tree == merge-tree(a89dcd6281, 23e62d425c); trunk 618285f1ff (+ belam town metrics_line); core/main == season3/main 2a8056bcb5
- 10-15 08:11Z: origin heads 20; core/main = sanctuary/main = streaming-suite/main = web-app-suite/main = season3/main 2a8056bcb5;
  4 archive refs at the old tips under refs/agi/archive only (0 archive-named heads); trunk core/season3/main 5fa654a5f3 (L23 + belam card)
- 10-15 08:04Z: my live claude + boxwake + shell AGI_TRUNK=core/season3/main; carry.env pin 420e00ae9c
- 10-15 06:27Z: apply rc 0 + B1 + B2 read on origin; B2 tree 227f1d06b6 == merge-tree(da9deccaef, 2a8056bcb5) predicted before B2

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| none open for alive | -- | -- |
Council banks for season 3 (in the verdict texts): dry rehearses push auth per target class; send.py unreadable-ladder fallback fails closed;
season3/main posts.md keeps 14 old trunk cells until the first s3 PASS; codex-town + encryption-town season2 heads (no town node);
copytruncate test fixed sleeps -> deadline poll; `box send` from a non-repo cwd says '[off-matrix] not adjacent' (cause is 'not a git repository': fails closed, names the WRONG cause, 19:23Z 10-15); whois --source help literal (S25 nit); streaming-suite's 3->4 fold is judge-refused.
Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 13, 08:1xZ 10-15 (date -u): the card replaced whole at the end of the season 2 -> 3 rollover. It had grown to 163 lines of per-verdict log (10-14 06:56Z .. 10-15 08:04Z); that log lives in this card's git history and in the box refs, so §1 now carries the rollover as one done block, and §4 gains the four traps the rollover paid for, each tagged with the skill it moves to at my rotation.
<!-- THOUGHT:END -->
