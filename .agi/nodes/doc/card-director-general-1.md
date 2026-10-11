---
id: doc:card-director-general-1
mint_id: 241494f333d2430abc688586909a2c99
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-1
scaffold_hash: ce9da8b3b952451b
season: 2
tags: []
title: Card director general 1
town: core
# doc:card-director-general-1 — director-general-1's card: the ONE scratch, replaced whole, <= 100 lines

## OVERALL GOAL (owner 10-08): finish encapsulation of grid slices (E1), belam on the new engine (E3, DONE), then the season rollover (E5). Progress is read ONLY on town:local-maxxing 'Engine rework trajectory' E1-E5. E2 (grid retirement) is MINE to cut; E4 (g1.41) moves by SM's landings.

## §0 State (10-11 ~20:3xZ, gen 24 rotating out at the line, encryption-town)
| | |
|---|---|
| post | director-general-1: a director, claude-code, engine v5 · parent SM (sanctuary-master) · trunk local-maxxing/season2/main (tip ae0190fec6 at 20:1xZ) · ~/t is DETACHED at posts/director-general-1: NEVER `git checkout` in it (I moved it once, restored) · card edits: `agi-wt pull doc:card-director-general-1` + agi-turn + agi-flush · a clone pushes a sha to MAIN with `git push /data/work/agi SHA:refs/heads/NAME` (a NEW name; next is dg1-close58) |
| mail | `AGI_POST=director-general-1 /opt/agi/bin/box read` (send: `box send POST < FILE`, from ~/t, plain text WITHOUT backslashes). **OWNER RULE 20:2xZ: NEVER box belam** (only SM and TM, one digest every ~4 h); I box SM only, ONE message per finished thing, NO acks/thanks/landed replies. A "mail: box read" typed into my pane is my own wake unit: read the mail |
| roles | DG1 = goals + nodes + merge-ups + JUDGING every return by RUNNING it · DG2 falsifier lanes (DG2 re-cuts box-wake.t.sh) · DG3 builder · DG4 builder (.37, .42 C1) · SM gates + lands (council 3/3 first) · belam = host acts, one GO each |
| SCRATCH | **/data/work/gate-director-general-1/wip** (belam made it 10-11, 700, my uid): t32 (.32), t401 (.40.1, .20.2; --shared clones, alternates = /data/work/agi), tools/, mail-sm-*.txt, home401 (the HOME for `env -i` test runs). The old ~/wip is REMOVED. Gate trees there: `git worktree add --lock`, never a bare prune. Plain `rm -rf <absolute path>`, no glob, no cd |
| BOX RULES | NO scratch on /dev/shm (tmpfs is charged to agi.slice); basetemp on DISK (`--basetemp=/data/work/gate-director-general-1/wip/pt`), `nice -n 10`, ONE heavy run on the box at a time (SM's gate first, then DG3's .43; ask in the box before a full pytest), remove after. Read the trunk through t401 (`git fetch /data/work/agi local-maxxing/season2/main` there), never ~/t |

## §1 Plan
```
LANDED/APPROVED (SM lands in his digest landing; nothing to do): .32 condition ee5b59605a · .32 CLOSE 5f5dc2c4be · .40.1 stack 15ef330d49 + close48/49/50 (81f68b2088 / 9ccbb67d98 / c08f9c445c) APPROVED 3/3, ride his (e,f) landing · cut 1 of .20.2 dg1-close51 1284b57f98 (on ae0190fec6) APPROVED to ride, stacked ON .42's L f5f100b83b · TARGET 4 (flap) dg1-close52 571f300635 ON 1284b57f98, MAILED SM 20:5xZ (clear line x0.8 + 3 min hold, cells on both rows).
NEXT TOUCHES, in this order (each ONE signed commit, rows + mutants, mail SM once):
 A. goal:g7.16.1.11.20.2 = EVERY ALARM AS SIGNED BOX MAIL (council 3/3 A-AMENDED: one spool per sending seat; root only APPENDS; the seat's uid drains+signs once; belam is mailed by SM). RETURNED by the council 23:0xZ (a SILENT LOSS: an fd opened before the drain's rename writes into the unlinked inode). RE-CUT, mailed 23:2xZ, branch dg1-close57 tip e8b68385a1, ALL ON de08f0dcd8: 572e69d369 (append re-checks its inode after the write + re-appends the same Alarm-id; unsent notice once per episode) < d09a3d1ed4 (failed quiet-watch append = a ~/.notice line, STORES var) < 4caabd13de (guard/alarm-first-start.sh: r1 over installed scripts + one signed line per drain row) < e8b68385a1 (C3 memguard re-cut). Earlier base: 571f300635 flap < f09ed75f32 C1 < 9b7ca099b0 C2 < de08f0dcd8 HOME fix. Leaf fix-forward (row 4 = NOT an alarm; falsifier 1(a)) is SM's. Waits on SM's re-gate; a RED returns as ONE fix commit ON e8b68385a1 (next branch dg1-close58). Host acts (belam): install alarm_spool.py to /opt/agi/bin, re-install quiet-watch, re-stage memguard, crons.py apply (.42 C1), then sh alarm-first-start.sh.
 B. goal .32 follow-up (cheap CPU, belam 13:5xZ): 12 agi-boxwake@ units cost ~3% of a core EACH. My pick, mailed: a REF FINGERPRINT before `box n` (`git for-each-ref refs/box refs/held` + the posts.md blob id vs the last tick; run `timeout 20 box n` only on a change), 5 s latency kept; FOLD IN the council remark `[ $? = 0 ]||continue` on ANY failed count (not only 124). ROW: no ref moves = box n not run for N ticks (counting stub) AND a send is announced within a tick; MUTANTS: fingerprint ignoring refs/held, one that never changes. WAITS for DG2's box-wake.t.sh reaper/polls re-cut: box DG2 one line before touching that file.
 C. a LOAD-TOLERANT box-mail.t.sh (leaf under g7.16.1.11.20; SM 15:5xZ): c2-retry-100of100 + c2-retry-0-stderr FAIL rc 124 (600 s kill) and m3-overlap-unsent-le-1pct red on the BARE trunk under load 13. Deadline polls (a COMPARISON, not a wall clock), fit 600 s at load 13, a mutant per row; run the lane solo on the bare trunk first to attribute; argue m3's tolerance from lost 0 / dup 0 / unsent reported, never loosen blind. Its green run CLOSES goal .11.11.1 (AA1.M mail; mechanism met, its falsifier is these rows).
 D. memguard next touch, council remarks (not conditions): the leaf's "NO blocking child call" is a false absolute (baseline()'s `systemctl show`, timeout 10, at the tick END after the stops: say "a size stop in the NEXT tick can wait at most 10 s, a low stop never"); the fake logger's wait()/communicate() must record a 'wait' event and row (b) assert none before the kill.
WAITING ON OTHERS: .20.2 cut 1 goes live only after .42 C1 (`user:` in crons.py apply, DG4): until then the rows run as uid belam and the alarm cannot notify. CUT 2 (a <box>-host identity, signed box sends for root guards) = a later round, laned by belam. .13 closes when DG2 runs the 17 aa3 lanes (I close the node). .17 stays ACTIVE (its falsifier-1 misses: no ring file/ckpt block, agi-land not installed: belam's host acts). .12 .15 .13 parked horizon by SM.
```

## 🔴 Where it stops + the exact next command
Re-cut mailed; nothing in hand. NEXT: `AGI_POST=director-general-1 /opt/agi/bin/box read` (SM's re-gate), then touch B (DG2's box-wake re-cut first) / C (solo run of box-mail.t.sh on the bare trunk once SM's and DG3's pytest are off the box) / D. Keep test runs targeted. Never a host act; never `grid.py checkout`; never invent goals; the g7.16.1.11.11 HOLD is belam's.

## §2 Landed this generation (mine, via SM)
close32..close42 (memguard stack: kernel-state 'stopped', inherited-nice reset, proof2, restage race + refusal, a1.undo link) · close43 .32 condition · close46 .32 CLOSE · close47..50 .40.1 (start time in the SUSPENDED line, append raises = SIGSTOP anyway, log() best-effort wr(), logger fire-and-forget jlog()) · close51 .20.2 cut 1 · close52 .20.2 target 4 (memory_alarm hysteresis) · close53 C1 · close54 C2 · close55 HOME_PATH_RE fix · close56 C3 · close57 the RE-CUT stack (silent-loss fix). Judged by running: dg3-40b ACCEPT. Answered belam's board check (in flight .20 + .40.1).

## §4 Traps (this generation only; durable ones move to the skills at the next rotation)
| trap | rule |
|---|---|
| `git checkout` in ~/t | NEVER: it is the post tree. Read the trunk in t401 |
| box text with backslashes, or `box send` from a non-repo cwd | no backslash escapes; send from ~/t |
| a mutant that goes RED only on an UNINTENDED row proves nothing | read WHICH row went red; assert each OLD text count == 1 (Restart=on-failure is in TWO units: anchor it); a mutant whose replacement is malformed goes red everywhere (K1: check the 41-RED case) |
| a time-scaled lane (box-wake DIV) | a burst of signed sends takes real time; under load a scaled poll splits it. Rerun SOLO at the default (10) before calling a defect |
| the TRUNK-arg lanes (agi-out-states, agi-out-stale, grow-gate-*, aa3) REFUSE a bare run | commit first, pass the SHA: `sh lane.t.sh <sha>` |
| memguard-proof2 execs post_rows..guarded (no os) | new helpers go OUTSIDE that slice; no second `time.sleep(` in the template |
| a shell function's exit status is its last command | scan_held ended on a `case` arm = a false "unreadable": end with `return 0` |
| systemd unit text | `%s`/`%%` are specifiers (printf %s breaks); a brace `${H}` is substituted; `$?` and `$(...)` are fine |
| agi-notice dedupes by its [..] and hex-only words | give each alarm kind its own bracket and an 8-hex token or a later line is dropped |
| a hysteresis/hold row | the hover input must outlast the hold or only the band mutant shows: derive the mutant x row matrix by reasoning, then assert it (mine was wrong first) |
| test_commands::test_a_bare_first_word_runs_a_declared_command | times out (180 s `agi links`) on the BARE trunk too: not a regression signal |
| a root unit/script that touches a seat's key or `box send` | r1 test (test_quiet_watch_spool.py) is RED: root only APPENDS to the seat's spool by runuser; the seat's drain row signs |
| a crons.md why_box/prose with a literal seat home path | belam's landing guard (anonymize.HOME_PATH_RE over added lines) refuses it: write the seat's ~/alarm.spool |
| a crons.md THOUGHT whose FIRST words change | goal:g7.16.1.11.13's pinned C4 line breaks test_grid_writers (7 red): re-cut it or keep the first 84 chars |
| a plain-YAML cron cell/prose with `: ` inside | unquoted scalar breaks the whole node: no colon-space in why_box |
| a spool append that opens the file and writes later | the drain renames+unlinks under it: re-check fstat(fd).st_ino vs stat(path) after the write and put the SAME id in again; never assume 'renamed aside' protects an open fd |
| awk `match()` on mawk/gawk both fine; a directory arg only WARNS (rc 0) | check `-f` before reading a log |

## §5 Verification: every return RUN at the sender's sha (bare `env -i PATH=$PATH HOME=<home401>`, tree and basetemp on DISK, nice 10). boxkit: `python3 -m pytest extensions/agi/tests/test_boxkit_templates.py extensions/agi/tests/test_boxkit_probe.py -q -p no:cacheprovider --basetemp=<pt>` = 334 at c08f9c445c. memory_alarm + crons + heal + commands: 566 at 1284b57f98 (12 min at load 13-17: run them targeted, not all at once). Engine shell lanes: `ROOT=$PWD sh extensions/agi/tests/<name>.t.sh` (engine-sizes, post-env, restart-bounds, agi-fresh, kid-post-env, boxwake-unit, box-wake, trunk-arg-lanes); with a SHA arg: agi-out-states, agi-out-stale. Read-only measurement of a live tree is fine; a signal, a write under /etc or /usr/local, or a root act is not mine.

## §6 BANKED (to SM's digest; none blocks a build)
- user@-only memory thrash is logged but not noticed (memory_alarm_posts owns the notice): option 'the user@ job notifies only while its sibling is ok'.
- Pruning noh/unread/nobase for a unit that left the box (memguard): not cut (rule was clears-on-the-good-reading).
- The guard's `systemctl show` wait (see D) and the 'wait' event in the fake logger.
- Branches I created that cannot be deleted from this uid (leave): the dg1-* ones (close32..close51).
