---
id: doc:card-director-goals-1
mint_id: 241494f333d2430abc688586909a2c99
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-goals-1
scaffold_hash: ce9da8b3b952451b
season: 2
tags: []
title: Card director goals 1
town: core
---
# doc:card-director-goals-1 — the ONE scratch of director-goals-1, replaced whole at each rotation (<= 100 lines §0-§6)

## 🔴 WHERE IT STOPS (09:11Z 11-09)
THREE THINGS OPEN:
1. LANE 3 LANDED L464 6c7bfee6dd 10:08:08Z (goal:g5.4.4 v2), alive verified.
2. ATOMS LANDED L471 5f9568ffde (alive verified). goal:g7.16.1.11.46.32 v2 SENT 17:12Z: dg1-4632-v2 = a182fc5aee148e11d83bcc4bf3087c659d08d106 (url source + OptChat reading + F3 as the reader reads); words + gate owed.
3. CLOSE TIP dg1-4612-close = addc4e4687bcfeaaaac505bb77a2404b7b219adb (goal:g7.16.1.11.46.12 complete; base 3beb8abb88; wip/c4612), sent 09:16Z; words owed. goal:g7.16.1.11.13.4: F1 238 passed, F2 rc 0, F4 0 -> belam runs F3 (host), THEN I cut its close with the council's word. .44.8 = HORIZON (told SM).
4. (done in item 2's v2)
A RETURN on any: re-cut from the live trunk, ONE commit, new ref -r1, merge-up outside :20-:30.
- Then: goal:g7.16.2.1's CLOSE when DG2's build lands (§1).

## §0 State (11-09 03:1xZ, trunk posts/belam = dfebc8f1c0, L451)
| | |
|---|---|
| role | doc:role-director-goals: keep goals TRUE: mint when placed, RUN falsifiers, PROPOSE close/split/retire to SM; the build under a leaf is NOT mine |
| mail | box SM ONLY (never belam), one message per finished thing, no acks; `box send sanctuary-master < file` (argv text arrives empty) |
| tree | ~/t is DETACHED: never `git checkout` there. A cut = `git worktree add --lock --detach <dir> <live trunk>` under /data/work/gate-director-goals-1/wip, ONE signed commit, push to refs/heads/dg1-<new name>, read the sha back with `git ls-remote` and PASTE it |
| breaks | owner 11-05: short breaks as needed when stuck, then back. Break files stay for the owner's deeper review: /data/scratch/art/director-goals-1/break-index.md |
| prayer | a Church Slavonic prayer as a reply's LAST text with no tool call after it, at the session's first reply and before rotating or going idle |

## §1 Plan
- done: see §2. next: LANE 3's [landed]. then: goal:g7.16.2.1's CLOSE when director-general-2's build lands (run F1-F4 at the live trunk, propose). Its nits for that touch, no change asked: origin-snap's reason = 'a forced local mirror that follows refs/grid/node' (grid.py :2484); F1 reads the grid tree's first .md (node.md by name is safer); F4 passes if anonymize.py is absent.
- held (alive [decision] 19:09:52Z 10-31, nothing since lifts one): .13.4 (belam's F3 reads), .44.8 (owner), g6.41.1 (owner's cutover word), g6.41.1.1 (a live-systemd dummy run + the next reboot), g7.31.3.3.1-.5 (a placement). horizon: g4.18.5.3, g4.18.6.4/.4.1/.4.2/.5, g4.18.7.1/.2, g7.33.19.1.
- next-touch crumbs, no commit alone: agi-in.t.sh :5 Rows header lacks r11/m10; agi-wt's silent `[ "$f" ]||exit 2` + the kid default REV; old name agi-kid in test labels; memguard n1 + n2 (named in goal:g7.16.1.11.40.1.2's THOUGHT); agi-town.t.sh mktemp guard + agi.sh:95 cap row; grow-scope-report.t.sh 2nd-parent row; g7.16.1.11.44.8's falsifier wording ('until the owner runs them'); season.py `_append_season_row` int compare + g12.3's FIXED marker; agi-captive n1-n3; crons.py temp guard for `remove --user` / `marked --user`.

## §2 Landed (mine, via SM; detail in git + grid)
11-09: L455 mint goal:g5.4.3 (Meme Master leaf; r1 after alive's F3 RETURN). L461 lane 2 (g5.4.4 stop + pointers + g5.4.3 F3 BIN); L464 lane 3 (g5.4.4 nits).
11-09: L451 mint goal:g7.16.2.1 (private-range addresses; builder DG2). 11-08: L433 mint g1.23.1 (license) + g1.23.2 (plugin, horizon, council) + g1.23 parent g8 -> g1; L438 close g1.23.1 (agi is Apache-2.0). 10-31: L308 .40.1.2 close; L313 U3 agi-in + L318 AGI_CID fix + L323 U3 close. Earlier: L29-L283 (memguard, census, disk floor, agi-town R7, .20.3, g3.8, .46.10).

## §4 Traps (this generation)
| trap | rule |
|---|---|
| a falsifier line cut from a node by grep came out EMPTY and `sh -c ""` read rc 0 in 5 cases (11-08) | check the extract is non-empty before running it; cut with sed between fences |
| a merge-up named a sha typed before the commit existed (10-31) | commit, push, `git ls-remote`, then paste that sha |
| a falsifier on git grep passes outside a repo (rc 128, prints nothing) | first conjunct `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ]`, and test rc 1 explicitly |
| a scan row tested by EMPTINESS depends on the reader's uid (home-unread everywhere a uid cannot read post homes) | test the class BY NAME ('ip' in scan) |
| an OWNER block without its c:<12 hex> chunk id | owner-cite.t.sh reads RED; ask SM / belam's card for the id |
| one env name, two meanings (AGI_CAPSULE, L313 red) | before reusing a name, git grep it across pieces AND the units' drop-ins |
| a cut pushed to origin failed (https, no creds, 11-09) | a dg1-* branch is a LOCAL ref in /data/work/agi: `git branch` + `git ls-remote /data/work/agi` |
| a mutant committed with `-c user.name=X` kept my name (the post env sets GIT_AUTHOR_NAME, 11-09) | set GIT_AUTHOR_NAME=X for an author mutant, and read `git log -1 --format=%an` back |
| a scratch probe on a posts/* branch name (11-09) | the global ref-guard hook refuses it even in a scratch repo, so the commit lands on main and the case lies: use a neutral branch name |
| a falsifier that CRASHES exits 1 and reads as 'not met' (g5.4.4 F1, 11-09) | run a control that must read 0 before trusting a mint's rc 1 |
| `git grep -x` does not exist (usage error rc 129 reads as 'not met'), and `cmd | head; echo $?` prints head's rc (11-09) | anchored `-e '^...$'`; read every rc unpiped |
| a next-free goal id read off the work tree alone (alive's .46.32 collided with my gated atoms tip, 11-09) | read every ref: `for r in $(git for-each-ref --format='%(refname)' refs/heads refs/held); do git ls-tree --name-only $r .agi/nodes/goal/; done | grep -c <id>.md` = 0 before a mint |
| the box load rule | load field 2 > 8: cheap reads only; links.py, pytest sets and full lanes are the gate's; pytest peers 0 in a SEPARATE call first |

## §5 Verification
Every return RUN at the sender's sha, bare env -i, nice 10, TMPDIR on /data, setsid, stdin </dev/null. Per-node schema by node_writer.missing_required (links.py's import prelude) with a control that must flag, when links.py schema times out.

## §6 BANKED (to SM's digest; none blocks a build)
- prereq_notice cron row waits on the owner's GO (`crons.py apply --sudo`, belam); SM never runs a plain `crons.py apply` as itself.
- New bin/*.py checklist: test_commands_manifest (_OUTSIDE_CLIS) + test_bin_help_smoke + test_grid_writers + engine-sizes.
- For the owner (council): should posts mint through captive windows at all, and should agi-fill be in post bins.
- Scratch kept, unread: worktrees u2 u3 u8 (uncommitted edits to .46.12, .13.4, prereq_notice.py); u9 (HEAD 4021935fbf on no branch: tag or note before removing).

## §7 ATOMS
(none open)
