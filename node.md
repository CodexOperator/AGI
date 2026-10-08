---
id: hypothesis:g75213-ram-main-binds-claude-worktrees-to-disk-and-sweeps-idle-agent-trees
mint_id: 61527517f8064a0eb295bd560930d4fa
type: hypothesis
parents:
  - goal:g7.16.1.5.2
next_edges: []
scaffold_hash: 3e48e4f0b73e88c4
season: 2
testable_claim: An Agent worktree made after ram-main.sh up sits on ext4 (findmnt -T), the RAM disk does not grow, the bind list is one config:guard cell read by all four ram-main.sh places, and session-sweep removes only clean, idle >= 1 h, unheld Agent worktrees via git worktree remove
title: ram-main.sh binds .claude/worktrees to DISK from one config:guard bind list; the sweep removes clean Agent worktrees idle >= 1 h
town: core
---

# hypothesis:g75213-ram-main-binds-claude-worktrees-to-disk-and-sweeps-idle-agent-trees

## Measured
- extensions/agi/guard/ram-main.sh: the DISK -> RAM bind list is a literal in FOUR places -- `EXCL` (rsync excludes: /.git /.agi/worktrees /.env), `up` (`bind_in .git; bind_in .agi/worktrees; bind_in .env`), the `sync` prune (`-path "$DISK/.git" -o -path "$DISK/.agi/worktrees"`), `down` (`for p in .env .agi/worktrees .git`). No config:guard cell names it.
- MAIN/.claude/worktrees (Claude Agent worktrees) is NOT in that list: `findmnt -T .claude/worktrees` = tmpfs (DG4, 14:2xZ 09-30), so every Agent worktree lands on the 7 GiB RAM disk.
- The Prime removed 13 clean idle Agent worktrees at 14:19Z 09-30: RAM disk 4121M -> 2260M (now ~30 pct); 1 dirty tree kept.
- extensions/agi/guard/session-sweep.sh part 2 (`GUARD_SWEEP_PAIRS_<box>`, 'SRC=>DEST ...') MOVES idle harness dirs to a cold home with a symlink back; it has no route for an Agent worktree, and a git worktree is not movable by copy + symlink (its gitdir back-pointer breaks).
- tests: test_session_sweep.py (2 tests), test_guard_init_cells.py (8); no test runs ram-main.sh.

## CLAIM
(1) ram-main.sh binds DISK's `.claude/worktrees` into RAM exactly as it binds `.git` and `.agi/worktrees`, from ONE bind list that is a config:guard cell (`GUARD_RAM_BINDS_<box>`, default = today's three paths + `.claude/worktrees`), read by all four places (excludes, up, sync prune, down). (2) session-sweep.sh sweeps a CLEAN Agent worktree idle >= 1 h (newest file mtime, no live cwd/open file, `git status --porcelain` empty, HEAD reachable from another ref) through the GUARD_SWEEP_PAIRS configuration route, removing it with plain `git worktree remove` (never --force); a dirty one is never touched.

## Dispatch line
config-max: the bind list -> `GUARD_RAM_BINDS_<box>`; the Agent-worktree source dir and its idle age (60 min) -> a GUARD_SWEEP_PAIRS entry / `GUARD_SWEEP_AGENT_WT_IDLE_MIN_<box>` cell. The kid cannot write config:guard (owner/prime ring): it ships the script DEFAULT = the new cell value and hands the exact cell lines to its parent, who returns them up (director -> sanctuary-master -> the Prime writes them). template-max: none expected. code: only the loop that reads the bind cell, and the worktree-remove branch of the pairs sweep.

## FALSIFIERS
1. An Agent worktree made after `ram-main.sh up` has `findmnt -T <tree>` = tmpfs (must be ext4), or /mnt/agi-ram use grows by its size.
2. A dirty, or recently written, or process-held Agent worktree is removed or altered by a sweep.
3. Any of the four ram-main.sh places still carries a literal bind path after the round.
4. harvest cleanup of kid trees (DG3's goal:g7.16.1.5.4) is touched.

## TESTS
test_session_sweep.py (new rows: clean idle tree removed; dirty / recent / held tree kept) + a new test_ram_main_binds.py that runs ram-main.sh's list parser with a stub `mount`/`sudo` on PATH (never the real mount, never on the live MAIN) + neighbourhood test_guard_init_cells.py test_box_guard.py test_bin_help_smoke.py. --basetemp under /tmp.

## FILE SCOPE
extensions/agi/guard/ram-main.sh · extensions/agi/guard/session-sweep.sh · extensions/agi/guard/GUARD.md (cell doc lines only) · extensions/agi/tests/test_session_sweep.py · extensions/agi/tests/test_ram_main_binds.py (new). NOT config:guard (hand the lines up), NOT heal.py / harvest cleanup (DG3), NOT the live mounts.

## CEILING
1 parent (pi-free, ladder tier 0) · <= 2 kids · 10-12 production lines per conjunct (2 conjuncts) · tests <= 60 · 0 USD lane.

## OWNER 2026-09-30 14:2xZ, verbatim (via sanctuary-master, from belam)
"I thought .Claude was symlinked into /data, so anything going into .Claude goes in there including sessions too files everything related to session data"
