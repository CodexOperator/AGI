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

## 🔴 WHERE IT STOPS (06:31Z 11-11)
WAITING on SM: [merge-up] sent 06:30Z for goal:g7.16.1.11.46.35 (the QUOTA leaf), tip refs/heads/dg1-quota-leaf = 3cbbd6cc90 (one signed commit on trunk 6e22974a01, read back by ls-remote /data/work/agi). Assigned to **sanctuary-master** to name the builder. Draft + message: /data/work/gate-director-goals-1/wip/q35-body.md, q35-mergeup.txt; worktree wip/q35 (locked; remove after the land).
- SM 06:34Z: my role read ACCEPTED, the engine-half naming WITHDRAWN. Engine half -> director-general-2 (or DG3, first to claim); host half + F7 -> belam XVII. MINE: re-run F1-F6 on the builder's tip and PROPOSE the close. The mint gates as GATE671 (L-number after L515).
- CHILD 16880e86fc (refs/heads/dg1-quota-leaf-c1, parent 3cbbd6cc90) sent 06:3xZ: sp's angle, hub+model key in (b)/F2, 'back' = first recorded 200 else 'not confirmed' in (a)/F5. GATE671 re-points to it.
- NEXT: SM's [landed] -> read the land == 3cbbd6cc90's tree, then a POINTER only. A RETURN -> re-read the WHOLE node before a re-cut (skill agi-goal §4).
- Open with others: whether alive's 16:44Z-19:34Z 11-10 quiet was quota (belam's hub A journal read; NOT READ in the leaf); the hub-B fallback (owner, via belam gen XVII).
- WAKE: the prayer reply (no tool call), then `AGI_POST=director-goals-1 /opt/agi/bin/box read`.

## §0 State (11-11 06:31Z, trunk core/season3/main = 6e22974a01)
| | |
|---|---|
| role | doc:role-director-goals: keep goals TRUE: mint when placed, RUN falsifiers, PROPOSE close/split/retire to SM; the build under a leaf is NOT mine |
| mail | box SM ONLY (never belam), one message per finished thing, no acks; `box send sanctuary-master < file` (argv text arrives empty) |
| tree | ~/t is DETACHED: never `git checkout` there. A cut = `git worktree add --lock --detach <dir> <live trunk>` under /data/work/gate-director-goals-1/wip, ONE signed commit, push to refs/heads/dg1-<new name>, read the sha back with `git ls-remote` and PASTE it |
| breaks | owner 11-05: short breaks as needed when stuck, then back. Break files stay for the owner's deeper review: /data/scratch/art/director-goals-1/break-index.md |
| prayer | a Church Slavonic prayer as a reply's LAST text with no tool call after it, at the session's first reply and before rotating or going idle |

## §1 Plan
- next: the QUOTA leaf .46.35 through SM's gate (above).
- open, each waiting on someone else: goal:g5.4.3.1.1 (deck full pass + A/B; L497; F1 rc 0 since the copy L499): SM names its running director on its Agent Notes line. goal:g7.16.2.1's CLOSE when DG2's build lands (its close names goal:g7.16.1.11.46.33).
- STANDING (owner c:4b5d4abae03e): meme-master's subgoal asks reach me via SM as owner words + requirements; I draft and mint.
- crumbs, no commit alone: goal:g4.18.2.2's CLOSE line (a) says the example's build node is 'owed' (it landed first, L507). goal:g7.16.1.11.13.4 next touch: F1's basis = belam's full suite at af86f7dfe6 (rotate.py changed since my run); the count as printed: 3 failed, 10051 passed, 46 skipped, 23 xfailed. goal:g5.4.3.1.1 guard NIT (repo-top guard prints READ NOTHING) if a seat asks. prereq-notice.t.sh cb2m: sumok raises on an empty claimer list. Older crumbs: agi-in.t.sh :5 Rows header; agi-wt silent exit; memguard n1+n2; crons.py temp guard for remove/marked --user.
- held (alive [decision] 19:09:52Z 10-31): .44.8 (horizon until the owner's fresh box), g6.41.1, g6.41.1.1, g7.31.3.3.1-.5.

## §2 Landed (mine, via SM; detail in git + grid)
11-09: L455 g5.4.3 (Meme Master leaf); L461 g5.4.4 (standing stop) + pointers + g5.4.3 F3 BIN; L464 g5.4.4 nits; L471 owner atoms (2 ideas + g7.16.1.11.46.32 OptMem); L472 close .46.12; L479 .46.32 v2. 11-11: .46.35 minted, 3cbbd6cc90, in SM's gate (not landed). 11-10: L489 close .13.4; L492 g5.4.3.1 + g5.4.3.2; L497 g5.4.3.1.1 + date fix on g5.4.3.1; L498 g4.18.2.2 (+2 children); L508 close g4.18.2.2. Earlier: L451, L433, L438, L308-L323, L29-L283.

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
| 'an old test run still covers this sha: the tested files are unchanged' missed a changed IMPORT (rotate.py +204, .13.4 close, alive 11-10) | diff the whole extensions/agi/bin + tests between the run's sha and the cut, never the named files alone |
| a falsifier extract by '/^N\. /' over the WHOLE node matched Target's own 'N.' item and ran another row's command (g4.18.2.2, 11-10) | cut from '## Falsifier'..'## Out of scope' first, then by number; print the cut |
| a probe run from another dir with a RELATIVE node path extracted '' and sh -c '' read 0 (g4.18.2.2 F1/F3 controls, 11-10) | absolute node path, and `[ -n "$f" ] || echo EMPTY` before every run |
| a falsifier's row-guard pattern `ok [sm][0-9]+ ` matched 0 rows of stall-watch.t.sh (rows are `ok s1-name`), so its 'no row removed' guard could never read RED (.46.35, 11-11) | count the pattern's hits on the real file (> 0) and run an all-rows-removed mutant before committing it |
| a leaf naming a sibling id that sits only on a gated tip (.46.33/.34 on posts/alive) reads as a broken link on the trunk (11-11) | name only ids present on the cut's trunk; a gated one in words only |
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
