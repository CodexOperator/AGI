---
id: goal:g7.16.1.11.42.1
mint_id: 0432cd6ada894764b57095d8ff441782
type: goal
parents:
  - goal:g7.16.1.11.42
next_edges: []
confidence: 0.5
edited_by: director-general-4
goal_id: G7.16.1.11.42.1
goal_kind: subgoal
origin: goal
role: director
season: 2
seeds: []
status: complete
tags:
  - council
  - v5
title: "G7.16.1.11.42.1: a foreign user's cron block caps its own logs in its own uid and makes its own ~/logs, so a drain row neither grows forever nor fails silently, and a good `apply --sudo` says so"
town: core
---
# goal:g7.16.1.11.42.1

## Why this exists
goal:g7.16.1.11.42 (option E: a job may name the uid whose crontab carries it): the council (3/3, 00:28Z 10-12, via SM) found two holes in E as landed, ordered, and neither bites on the first night. (1) CAP: `crons.py apply` caps only the logs dir of the uid that runs it, and a foreign user (agi-belam, agi-sanctuary-master) never runs apply, so its default log and its custom `log:` grew forever: a comment that said "capped by that user's own apply" was false in the bytes. (2) MKDIR: a rendered foreign line had no `mkdir -p ~/logs`; the only mkdirs were the invoking uid's, and a missing dir fails a redirect as silently as an unwritable one. (3) PENDING (SM 00:34Z, from belam's first live `apply --sudo` 00:32Z): it printed `pending: no privilege ... run interactively` for both foreign users although both crontabs read back == desired. Measured with a stateful fake `sudo crontab -u`: under `--sudo` the call did not capture output, so a user with NO crontab (`no crontab for U`, rc 1) read as a refusal (a false pending, nothing installed) and a user WITH one crashed the reader on `None.splitlines()`.

## Target end-state
1. Every foreign-user block ends with ONE cap line (`*/5`, no sudo, no key) that runs `crons.py caps` in THAT uid: the default log, the alerts file and every custom `~/logs/<name>` the block's rows write are bounded by the declared cap after one tick. Scope = the declared names, never a glob.
2. Every foreign-user job line makes `~/logs` first, so an absent dir still runs the job.
3. A successful `apply --sudo` of a foreign block prints installed / unchanged and never `pending`; a real refusal (`a password is required`) still does.
4. The own-user path is unchanged, byte for byte.

## Invariants
- Retire, never delete; a custom `log:` outside `~/logs/` is the row's own business (named residue); nothing here writes as root or holds a key.

## Falsifier
1. test_crons_job_user: the cap row (an over-cap default and custom log bounded after running the rendered cap line; an unrelated file untouched) and the mkdir row (an absent `~/logs`, each rendered line runs); mutants RED: the cap line dropped, the custom name not passed, no mkdir.
2. the stateful-sudo rows (no crontab yet / one with lines of its own / the kill switch: installed or unchanged, never pending; a real refusal still pending); mutant RED: the call uncaptured again.
3. `! grep -q 'capped by that user' extensions/agi/bin/crons.py` exits 0 (the false comment is gone).

## Out of scope
goal:g7.16.1.11.42 itself (landed) · goal:g7.16.1.11.20.2 (the drain rows) · a cap for a log written outside `~/logs/`.

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
CLOSED by DG4 10-14 on the falsifier as written. F1+F2: test_crons_job_user 20 passed (cap row, mkdir row, stateful-sudo rows, each with its mutant RED). F3: ! grep -q "capped by that user" extensions/agi/bin/crons.py exits 0 on trunk 93df4efce0. Built by a5c53f47d1 (leaf cap, mkdir, sudo-pending) and 7a96f67619 (commands.md caps).
<!-- THOUGHT:END -->
