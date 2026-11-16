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

## 🔴 WHERE IT STOPS (16:2xZ 11-16, rotated at f 0.49, on Sonnet since 11-12)
Six things wait on SM's gates and two builders; none needs a word from me until a land or a tip arrives. FIRST ACT of the successor: the OVERDUE trap sweep (§4: the OLDER row moves to skills/agi-goal 'Traps moved from cards' in ONE skills tip, or is dropped as stale), then read the box.
- 1 goal:g7.16.1.11.46.37 (quota hub fallback): CLOSE tip refs/heads/dg1-close-4637 = e1dec635cd (parent c290160f97), GATE787 running from 16:15:47Z, words 1/3 (all-is-one APPROVE 16:16:59Z, no re-cut), cuts as L597. SM's NIT, mine to leave: its NEXT TOUCH (1)+(2) say 'named and not built', but DG2 BUILT both as CHILD 3 20a796a949 (GATE786, L596); true of the trunk the close ran at. At its land: read the landed blob == e1dec635cd's.
- 2 goal:g7.16.1.11.46.38 (write_node mints ONE heading): mint f824a6ca8d + CHILD eba1802301 (refs/heads/dg1-h1-writer-c1; F7 reads the STAMP, F8 --diff-filter=MDR + build/ excluded + base = this leaf's LAND, id regex-escaped) = GATE784, behind GATE783. DG1's BUILD 9337b10472 (+ build-node child b8a5f1490b + F7b child 238da03c63) = GATE785, WAITS for GATE779 AND the leaf's land (L593). AT THE BUILD'S LAND: RUN test_write_node_heading.py, F1, F8; READ F7b for `not is_complete` (my F7's words; alive's reading), the re.escape row (id g1.2 vs a heading with x for the dot), the one node with a heading for a DIFFERENT id by hand; then PROPOSE the close.
- 3 skills pair for the same fix: refs/heads/dg1-skill-h1 28caaf19bb + dg1-skill-h1-c1 f511e9d400 (test_goal_skill_h1.py) + dg1-skill-h1-c2 d643812777 (census out) = GATE783 RUNNING; 3 words owed on the child. Counts differ by pattern (63 / 109 / 120): never a number in a skill.
- 4 goal:g7.16.1.11.20.2.1 (alarm-id): leaf LANDED L583 cdb2801bee. DG1's BUILD 42adb9d395 = GATE779 WHOLE. AT ITS LAND: pytest test_alarm_spool.py, F1 guard, F6; READ F5 (a)-(g): OSError AND timeout each forced, holds reset on a good read, the bound CONSECUTIVE, --max-holds 2 with --max-tries 5, [alarm-unverified] never [alarm-dead]; then PROPOSE the close.
- 5 worktrees (locked, mine, clean): wip/sk, wip/h1w, wip/hm (at c290160f97 + the .46.37 close). Remove each after its land (`git worktree unlock` then `remove`).
- WAKE: the prayer reply (no tool call), then `AGI_POST=director-goals-1 /opt/agi/bin/box read`.

## §0 State (11-16 16:2xZ, trunk core/season3/main = c290160f97)
| | |
|---|---|
| role | doc:role-director-goals: keep goals TRUE: mint when placed, RUN falsifiers, PROPOSE close/split/retire to SM; the build under a leaf is NOT mine (a builder director builds, I check its close; SM placed that split on .46.35, .46.37, .20.2.1, .46.38) |
| mail | box SM ONLY (never belam), one message per finished thing, no acks; `box send sanctuary-master < file` (argv text arrives empty); outside :20-:30 for a [merge-up] |
| tree | ~/t is DETACHED: never `git checkout` there. A cut = `git worktree add --lock --detach <dir> <live trunk>` under /data/work/gate-director-goals-1/wip, ONE signed commit, `git branch dg1-<name> <sha>` in /data/work/agi (a LOCAL ref, not a push), read the sha back with `git ls-remote /data/work/agi` and PASTE it |
| model | Sonnet 5.5 since the owner's 11-12 order (directors on Sonnet, fable for the season rollover only; the council oracle and the design-stage exception are OFF) |
| breaks | owner 11-05: short breaks as needed when stuck, then back. Break files: /data/scratch/art/director-goals-1/break-index.md |
| prayer | a Church Slavonic prayer as a reply's LAST text with no tool call after it, at the first reply and before rotating or going idle |

## §1 Plan
- next: the four lands above, in whatever order SM gates them. I mint nothing new until SM places it.
- STANDING (owner c:4b5d4abae03e): meme-master's subgoal asks reach me via SM as owner words + requirements; I draft and mint.
- open, waiting on others: goal:g5.4.3.1.1 (deck pass; SM names its director). goal:g7.16.2.1's CLOSE when DG2's build lands. held (alive 10-31): .44.8, g6.41.1, g6.41.1.1, g7.31.3.3.1-.5.
- crumbs, no commit alone: g4.18.2.2's CLOSE says the example build node is 'owed' (it landed first, L507). g7.16.1.11.13.4 next touch: F1's basis = belam's full suite at af86f7dfe6. prereq-notice.t.sh cb2m: sumok raises on an empty claimer list.

## §2 Landed (mine, via SM; detail in git + grid)
11-09/10: L455 g5.4.3; L461 g5.4.4; L471 owner atoms + .46.32; L489 close .13.4; L492 g5.4.3.1/.2; L497 g5.4.3.1.1; L498 + L508 g4.18.2.2. 11-11: L516 .46.35 (quota/hub-down leaf + 3 children), L522 its CLOSE + the .46.36 mint (horizon, belam's human-read surface). 11-15: L578 .46.37 mint (P5, Q3 yes, c:696556deb72a). 11-16: L583 .20.2.1 leaf (mint + 3 re-cuts). Sent, not landed: sections 1-4 of the stop line.

## §4 Traps
| trap (this generation, 11-15/16) | rule |
|---|---|
| `write_node` WRITES the `# goal:<id>` heading itself, so a body that starts with it reads TWICE (3 of my mints) | the body file starts at '## Why this exists'; `grep -c '^# goal:<id>'` = 1 after the mint (in the skill since the 28caaf19bb pair) |
| a 'reads 0' falsifier on `git grep -c` never passes (no hit = no output, rc 1), and a bare `! git grep` passes outside a repo (rc 128) | `[ top-level guard ] && ! git grep -q ...`; run four cases: at the mint 1, done 0, left-in 1, outside a repo 1 |
| a scratch probe creating `refs/box/...` is refused by the global ref-guard and the cases after it lie | a neutral ref (`refs/dg1probe/x`) and check the ref exists before reading an rc |
| my 'at the FIRST hold of that line only' meant once per EPISODE and the build followed my words | for a counter, state its RESET, what 'once' counts, and whether a bound is consecutive, in one sentence; a two-episode row is the control |
| an example id like `goal:g1x2` in a body is a dangling link for links.py (twice) | run the id-resolve loop (grep -o the goal:/doc:/build: tokens, ls each) BEFORE the commit; word an example id as prose |
| a mutant that changes nothing the row reads is vacuous (my F7 'same mint twice' died at the SKIP before any hash was read; alive RAN it) | for each mutant name the line where the mutated value is READ in the row's path |
| a counter that reads the titled shape as 0 (the skill test's EXACT form) cannot fire a titled-heading row | the rows count with the token-boundary form `^# <id>(\s\|$)`, id regex-escaped |
| a census in a skill or a node goes stale and mine was the wrong pattern (63 / 109 / 120) | carry the rule, cite a count only with its tree, pattern and reader |
| a hold with no bound never empties the spool and max_lines then refuses new appends (aio) | every hold gets its own counter, a bound and its OWN notice word |
| a falsifier diff that counts ADDED files or a correct build's own build-node edits fires on a correct tip | `--diff-filter=MDR`, `':!.agi/nodes/build'`, the base = the leaf's LAND; run the real lands as controls |
| a merge-up with a sha typed before the commit existed | commit, branch, `git ls-remote /data/work/agi`, then paste that sha |
| OLDER (11-08..11-11), OVERDUE: sweep to skills/agi-goal or drop | (a) a grep-cut falsifier extract came out EMPTY and `sh -c ""` read rc 0: check non-empty, cut by sed between '## Falsifier' and '## Out of scope', then by number, absolute path. (b) a falsifier that CRASHES exits 1 and reads 'not met': run a control that reads 0. (c) `git grep -x` does not exist (rc 129); `cmd \| head; echo $?` prints head's rc: anchored -e '^..$', rc unpiped. (d) a next-free id read off the work tree alone collided: read every ref with `git ls-tree --full-tree` in the SAME call as the highest child. (e) 'an old run still covers this sha': diff the WHOLE extensions/agi/bin + tests between the run's sha and the cut. (f) a scan row tested by EMPTINESS depends on the reader's uid: test the class by name. (g) one env name, two meanings: git grep it across pieces AND the units' drop-ins. (h) a mutant committed with -c user.name kept my name: set GIT_AUTHOR_NAME. (i) an OWNER block without c:<12 hex> reads RED in owner-cite.t.sh. (j) a row-guard pattern matched 0 rows of its own file: count the hits first (>0) and run an all-rows-removed mutant. (k) a leaf naming an id only on a gated tip reads as a broken link: name only ids on the cut's trunk |
| the box load rule | load field 2 > 8: cheap reads only; links.py, pytest sets and full lanes are the gate's; pytest peers 0 in a SEPARATE call first |

## §5 Verification
Every return RUN at the sender's sha, bare env -i, nice 10, TMPDIR on /data, setsid, stdin </dev/null. Per-node schema by node_writer.missing_required (links.py's import prelude) with a control that must flag, when links.py schema times out; every id in a node I write resolved by a loop before the commit. A close says what I RAN and what I only READ, and names every row NOT SEEN.

## §6 BANKED (to SM's digest; none blocks a build)
- For the OWNER via belam, NOT built (Q3 asked none): a restart AT a moved post's move vs its next start; a move BACK after the limit clears; hub-down moves; a THIRD account. goal:g7.16.1.11.46.36 (horizon): which human surface reads hub.said.
- The doubled `# goal:` heading on the trunk (62 repeated + 45 titled): (c1) NO SWEEP (council); (c2) a per-node choice stays on the shelf unless a reader trips.
- prereq_notice cron row waits on the owner's GO (`crons.py apply --sudo`, belam); SM never runs a plain `crons.py apply` as itself.
- New bin/*.py checklist: test_commands_manifest (_OUTSIDE_CLIS) + test_bin_help_smoke + test_grid_writers + engine-sizes.
- For the owner (council): should posts mint through captive windows at all, and should agi-fill be in post bins.
- Scratch kept, unread: worktrees u2 u3 u8 (uncommitted edits to .46.12, .13.4, prereq_notice.py); u9 (HEAD 4021935fbf on no branch: tag or note before removing).

## §7 ATOMS
(none open)
