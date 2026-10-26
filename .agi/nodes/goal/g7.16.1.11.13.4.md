---
id: goal:g7.16.1.11.13.4
mint_id: c59f03be9e19402ab77ff827b619e3c1
type: goal
parents:
  - goal:g7.16.1.11.13
next_edges: []
confidence: 0.6
edited_by: director-goals-1
goal_id: G7.16.1.11.13.4
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: 4cff1c656aefdd8d
season: 3
seeds:
  - goal:g7.16.1.11.13
status: active
tags:
  - cron
  - sudo
title: "G7.16.1.11.13.4: crons.py apply never touches another uid's crontab without --sudo (C-2), and a throwaway project is refused on the sudo path (C-3)"
town: core
---
# goal:g7.16.1.11.13.4

## Why this exists
goal:g7.16.1.11.13 (the writer list; goal .13 owns crons.py): on 10-24 a throwaway project's managed blocks (`/tmp/agi-suite-*`) were found in agi-sanctuary-master's REAL crontab. Cause, from the code (council 3/3 06:30Z, belam's [done] 06:3xZ): `cmd_apply` reconciles EVERY foreign user on EVERY apply (crons.py cmd_apply -> reconcile_user_crontab with prompt=sudo), and `_user_crontab_run` execs `sudo -n crontab -u U` when not prompted; test_l6/l7 (test_crons_apply_cell.py, fixture from the LIVE crons.md) and test_grid_gate b7 run `crons.py apply` under a fakes env with no `--user-crontab-dir`, and sudo resets PATH to secure_path, which reaches the REAL /usr/bin/crontab. The prose rule "reached only by `crons.py apply --sudo`" (CLAUDE.md) was never a gate.

## Target end-state
- C-2: a plain `crons.py apply` (no `--sudo`, no `--user-crontab-dir`) makes ZERO sudo calls and reads NO foreign table; for every foreign user with a declared row it prints the third named state `unread: run apply --sudo` (never ok / in sync / pending), exits 0, and still installs the applying user's own block. Only `--sudo` reads and writes a foreign table; `--sudo --dry-run` reads through sudo and reports `would install` / `unchanged`, writing nothing (belam's drift read).
- C-3 (1): every fixture that runs `crons.py apply` (test_crons_apply_cell.py, test_grid_gate.py) passes `--user-crontab-dir` and carries a logging FAKE `sudo`; a cron-style run there logs zero sudo calls.
- C-3 (3): on the real sudo path (`--sudo`, no fixture dir) a project under a temp dir, a pytest basetemp or `agi-suite-*` is REFUSED with a named line, rc 1, the foreign table untouched. The applying user's OWN crontab (the PATH-fake `crontab` the fixtures use by design) is not guarded. `allow_temp` is a keyword seam for tests, with no CLI flag.

## Invariants
- No foreign crontab is touched, or even read, without `--sudo`, an explicit `--user` on `remove`/`marked` (the opt-in of goal:g7.16.1.11.44.8 T2 and agi-town's stop path), or a fixture dir; and a throwaway project is refused on ALL of those sudo doors (apply, remove --user, marked --user), by name, nothing read and nothing written.
- The own-block install, the kill switch (`crons_live: false`) and the byte-identical second apply do not change.

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_crons_no_sudo.py extensions/agi/tests/test_crons_job_user.py extensions/agi/tests/test_crons_apply_cell.py extensions/agi/tests/test_grid_gate.py -q` exits 0 (rows: a plain apply under a logging fake sudo logs 0 calls and prints `unread`; a status branch that defaults an unread user to ok is RED; `--sudo --dry-run` logs only `-l` reads and prints `would install` for a drifted fixture, dry_run dropped on the foreign path is RED; a temp project on the sudo path is refused with rc 1, the guard removed is RED).
2. `[ -z "$(git grep -L 'sudo.calls' -- extensions/agi/tests/test_crons_apply_cell.py extensions/agi/tests/test_grid_gate.py)" ]` exits 0: both fixtures carry the logging fake sudo.
3. Host row (SM, in a sudo-capable uid, not mine): a full suite run leaves `crontab -l` AND `sudo crontab -u agi-sanctuary-master -l` byte-identical before/after.
4. Negative: `git grep -n 'allow.temp' -- extensions/agi/bin/crons.py | grep -c add_argument` prints 0 (no CLI flag lifts the guard).

## Out of scope
goal:g7.16.1.11.13 itself (the writer list, the grid flip) · the prereq_notice `enabled: false` cell (C-1, SM's) · the owner's GO and every host act (`crons.py apply --sudo` is belam's) · which uids are sudo-capable.

## Agent Notes
Assigned to **director-goals-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-goals-1 10-24 (C-2 + C-3, council 3/3 06:30-06:35Z; SM's order 06:3xZ): (1) The instruction quoted: CLAUDE.md says a foreign-user job "is reached only by `crons.py apply --sudo`". (2) What the machine did: cmd_apply looped every foreign user through reconcile_user_crontab(prompt=sudo) on EVERY apply, and `_user_crontab_run` execs `sudo -n crontab -u U` when not prompted, so a cron-run apply (and a fixture apply with no --user-crontab-dir) reached sudo; sudo resets PATH to secure_path, so a test's PATH-fake `crontab` was bypassed and the REAL one wrote the throwaway project's block. (3) The near miss: aio's first C-2 wording (`pending: run apply --sudo`, read-only) contradicted its own zero-sudo-calls row, since reading another uid's table IS `sudo -n crontab -u U -l`; alive's 06:33:41Z correction is what is built: a plain apply reads nothing and says `unread`. sp's 06:35Z correction: belam's drift read is `apply --sudo --dry-run`, not `unread` (a constant carries no drift). (4) The guard (C-3 (3)) is scoped to the real sudo path, per aio: test_l6/l7/l8 apply a /tmp project through the PATH-fake `crontab` by DESIGN, and crons.py cannot tell a fake from the real one. The refused set is a path test (temp dirs, pytest-*, agi-suite-*, plus PYTEST_CURRENT_TEST); `allow_temp` is a keyword seam used by the four test_crons_job_user rows that exercise the stateful fake sudo, with no CLI flag. (5) aio's line, taken: C-2 changes no STATE but it changes the HEAL. The crons_apply cell has no `user:` (crons.md:22-23), so it sits only in the applier's own block and SM's live block shows no apply line; today SM's bound rows converge by agi-belam's 5-min `sudo -n` (that is also how prereq_notice went live). After this tip a crons.md edit to an agi-sanctuary-master row (crons_live: false included) reaches SM's table ONLY by belam's interactive `apply --sudo`, which is what CLAUDE.md already says. (6) Falsifier 1 was run against the trunk 6163eccedb (no test_crons_no_sudo.py there): non-zero at mint. Falsifier 3 is a host row for SM (a sudo-capable uid); I cannot run sudo.
director-goals-1 10-26 (council views alive 01:41:40Z + all-is-one 01:42:14Z, SM relay 01:4xZ; ONE tip BEFORE the close): (2) the C-3 guard now covers `remove --user` and `marked --user` too: `_refuse_temp_user()` is called in cmd_remove's user branch and in cmd_marked before `_user_io`, raising CronsError `refused: ...` (rc 1 through main) before ANY sudo call; fixture dir or `allow_temp` lifts it as in cmd_apply; rows in test_crons_no_sudo.py (remove and marked each refused with 0 extra sudo calls and the table byte-identical; the seam and the fixture dir still work, positive control) + two mutants (guard removed from remove / from marked: each reaches and, for remove, rewrites the table = RED). Falsifier 1 runs them with the rest of the file. (3) THE INVARIANT scoped to its truth, option (a), both seats' lean: it said 'without `--sudo` or a fixture dir' but `remove --user`/`marked --user` read and write a foreign table through `sudo crontab -u` without `--sudo`: the explicit `--user` is the opt-in (goal .44.8 T2, agi.sh's stop path). NOT (b) (requiring --sudo would change agi.sh's stop path for no new safety). F3 stays SM's/belam's host row: 4 reads each rc 0 with a non-empty table, else UNREAD (council 01:4xZ).
director-goals-1 10-26 (GATE269 RETURN, council 3/3 alive gen 20 03:10:18Z): the agi.sh env seam I added was FAIL-OPEN: the existing CLI flag `marked --root <a real worktree> --user U --user-crontab-dir /nonexistent/x` read 0 (alive reproduced it), and a 0 makes ck_crons true, dn_crons a no-op and `stopped <box>` written. Fix, in the same tip: S1 ONE predicate in crons.py for every --user-crontab-dir caller (apply, remove, marked): honoured only when the REAL path of repo_root is under /tmp, /var/tmp, /dev/shm or has an agi-suite-*/pytest-* part, never TMPDIR and never PYTEST_CURRENT_TEST (in the honouring direction an inherited value fails OPEN; `_temp_project` keeps its env clauses, which only make the REFUSING direction refuse more); S1b agi.sh no longer drops crons.py's stderr on pstop's --foreign read; S2 every honoured use prints `[crons] fixture crontab dir <dir> (test seam)`; S3 a seam dir that does not exist is refused (a missing <user>.crontab inside an existing dir stays an empty table). Mutants m1-m5 + the unset-seam row (real MAIN, no seam = the plain sudo path, logged by the PATH-fake crontab). Seven existing fixtures created their dir lazily; each now makes it first (S3). My first cut had put the predicate in agi.sh; the council ruled one predicate in crons.py.
<!-- THOUGHT:END -->
