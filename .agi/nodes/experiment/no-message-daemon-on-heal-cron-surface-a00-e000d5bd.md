---
id: experiment:no-message-daemon-on-heal-cron-surface-a00-e000d5bd
mint_id: f21d51ba795649b9aabaa83b0b412187
type: experiment
parents:
  - hypothesis:a00-e000d5bd-bbf531
next_edges: []
edited_by: a00-e000d5bd
evidence_runs: experiment:no-message-daemon-on-heal-cron-surface-a00-e000d5bd
line_ceiling: 40
loop: goal:g7.31.4.3@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
season: 2
title: No message daemon on the heal/cron surface -- declared table, live probe, and a tripwire test
town: core
---
<!-- BODY:BEGIN -->
# experiment:no-message-daemon-on-heal-cron-surface-a00-e000d5bd

## Experiment

The claim is a NEGATIVE: no new message daemon appears in the heal/cron
surface for `goal:g7.31.4`. A negative cannot be proved by a single probe, so
this run measures three surfaces and lands one durable tripwire:

1. the DECLARED surface (`crons.md` frontmatter: `cadences:` + `services:`),
2. the LIVE surface (`crontab -l`, `systemctl --user`, `ps`),
3. the SEAM's shape (`send.py` long-running possibility + `heal.py`'s repair
   pass), and
4. a committed test that FAILS if a message daemon is added:
   `extensions/agi/tests/test_no_message_daemon.py`.

No production code was changed. All probes below are read-only.

**Command (naming the file explicitly, kid-tier gate honoured):**

```
python3 -m pytest extensions/agi/tests/test_no_message_daemon.py -q
```

Raw output:

```
....                                                                     [100%]
4 passed in 13.94s
```

Overlap sanity check (the surface this test reads): `test_crons.py` 89 passed
in 243.26s. Production lines measured: **0** (`git diff --numstat` empty;
only the new test file and this node are untracked).

## 1. Declared surface -- `crons.md` frontmatter (READ-ONLY)

`python3 extensions/agi/bin/crons.py show` / the frontmatter of
`.agi/nodes/.geometry/crons.md`. Every entry classified:

| declared | kind | rendered command | class |
|---|---|---|---|
| `grid_sync` (5m, enabled) | cadence | `grid.py commit --all` + ref push + `crons.py apply` | NOT |
| `branch_push` (:07, enabled) | cadence | `git push` the checked-out branch | NOT |
| `mail_poll` (5m, enabled) | cadence | `send.py read --box-local` ; `rotate.py migrate --receive` | MESSAGE-TRANSPORT, one-shot |
| `nudge_sweep` (2m, enabled) | cadence | `send.py wake --all-local` | MESSAGE-TRANSPORT, one-shot |
| `publish_engine` (:37, disabled) | cadence | `publish-engine.sh` | NOT |
| `engine_push` (:47, disabled) | cadence | `git push` engine | NOT |
| `prime_merge` (13 */6, enabled) | cadence | guarded `prime_merge.py tick` | NOT |
| `agi-alarms-sanctuary-master` (enabled) | service | `rotate.py alarms --holder sanctuary-master` | NOT |
| `agi-reaper` (enabled) | service | `heal.py watch --root {repo_root} --poll-s 30` | NOT |

The two MESSAGE-TRANSPORT entries are CRON cadences, not services: both invoke
`send.py` ONE-SHOT. `nudge_sweep` renders as `python3 .../send.py wake
--all-local` (`crons.py:605-613`; the renderer builds exactly that line) and
`test_crons.py::test_nudge_sweep_renders_on_every_box_and_is_not_a_generic_cmd`
already pins it. `mail_poll` renders `send.py read --box-local` plus
`rotate.py migrate --receive` (`crons.py:592-603`). Neither is a resident
process.

Neither declared service runs a message program. `agi-reaper` is a REAPER
(`heal.py watch`), and its wake repair is a bounded pass INSIDE that service,
not a message daemon -- see §3.

## 2. Live surface (READ-ONLY; pasted in full)

`crontab -l | grep -i agi`:

```
*/5 * * * * cd /data/work/agi && python3 /data/work/agi/extensions/agi/bin/grid.py commit --all --allow-branch --prefix 'cron: ' >> /home/belam/logs/grid-sync-agi.log 2>&1 && git push -q origin 'refs/grid/*:refs/grid/*' >> /home/belam/logs/grid-sync-agi.log 2>&1
7 * * * * git -C /data/work/agi push -q origin core/season2/main >> /home/belam/logs/grid-sync-agi.log 2>&1
```

Two lines, both `grid_sync`/`branch_push`. NO `send.py` line and NO message
process. (Residue, named: the live crontab does not currently carry
`mail_poll`/`nudge_sweep`; the declared node does. That is a sync residue on
the MESSAGE seam, not a daemon -- a missing one-shot is not a resident one.)

`systemctl --user list-units --type=service --all | grep -i agi`: 45 units,
every one an `agi-belam-*` / `helper-dispatch-*` dispatch or workflow runner
(`bash -c /tmp/*-run.sh`). NO `agi-alarms-*`, NO `agi-reaper`, and NO unit
whose command line invokes `send.py`, a message router, or a daemon. The two
declared services are not installed on this box -- irrelevant to the negative
(fewer processes, not more).

`ps -eo pid,args | grep -E 'send\.py|_daemon' | grep -v grep`: no `send.py`
daemon. The only `send.py`-adjacent processes are a parent's `cli.py done`
argv and a `pytest ... test_send.py` run. No message process is resident.

## 3. The seam's shape

- `send.py` defines `wake` (`send.py:2657`) and `wake_all_local`
  (`send.py:2811`): both are one-shot functions that RETURN a bool. The nudge
  is retried by the 2-minute `nudge_sweep` timer, never by a resident loop.
- `heal.py:1636 _repair_stranded_wakes` is a bounded repair pass called from
  the `_watch` loop (`heal.py:1514`, `while True` at `:1525`). The only
  `while True` in `heal.py` IS the reaper service that is already declared
  (`agi-reaper`) -- a REAPER, not a message daemon, and it does not exist to
  carry messages.
- The only `while True` in `send.py` is `_in_git_repo` (`send.py:3141`, the
  filesystem walk at `:3148`) -- a path probe, not a loop. `send.py` has no
  `threading`, no `Thread(`, no `Popen`, no `serve_forever`. `crons.py` has
  none either.

## 4. What `.1`/`.2` landed

`.1`/`.2` produced surfaces, not processes. `test_send_surface_ssh_or_not.py`
(269 lines, committed under `goal:g7.31.4.2`) contains no service, no thread,
no `Popen`, no daemon -- it is a test module. `send.py` remains one-shot: its
AST argparse verb set (parsed, never imported) is

```
ask audience escalate keygen peek prime-excluded read report rooms send
status veto vote wake whois
```

None of `{serve, daemon, watch, listen, loop, run, start, start-server}`.

## 5. The tripwire

`extensions/agi/tests/test_no_message_daemon.py` (new, test file -- excluded
from the production-line ceiling). It:
- parses `send.py` with `ast` and asserts the verb set contains NO
  long-running verb (and that the probe found the real verbs -- non-vacuous);
- reads the LIVE `.agi/nodes/.geometry/crons.md` (skips cleanly when the
  graph root is not discoverable) and asserts no enabled service runs a
  message router -- `send.py` only with a one-shot verb, and no message
  program behind `while True` / `serve` / `daemon` / `listen` / `loop`,
  naming the offending service and its `exec_start`;
- plants a message daemon and asserts the detector NAMES it (non-vacuity);
- renders `nudge_sweep` from a fixture crons node and asserts it is a cron
  one-shot `wake --all-local`, never a service.

## Result

PASS. Declared surface clean, live surface clean, seam one-shot, tripwire
green and non-vacuous. The negative is strong but not absolute -- the live
`systemctl`/`crontab` output is a point-in-time probe, so the honest verdict
is `inconclusive_lean_proved`, with the tripwire as the durable half.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This run answers a negative by measurement plus a tripwire, not by assertion.
The instruction was `prove the negative by measured inventory plus one durable
tripwire`; the machine that satisfies that is three separate checks, because
each alone is defeasible: the declared table can be clean while the machine
runs something undeclared, and the live machine can be clean while a future
edit adds a daemon. So the measured inventory covers both, and the committed
test is the half that survives this session. The near miss: reading only the
declared `services:` table would have passed trivially (it declares two
non-message services) and said nothing about the crontab, the live units, or
the future. I also refused to treat `heal.py watch` as an offender just
because it is literally a `while True`: the falsifier is a MESSAGE daemon, and
the reaper is neither new nor a message carrier -- flagging it would have been
a false positive that makes the tripwire unusable. No production byte moved
(0 lines); the only writes are the test file and the two nodes.
<!-- THOUGHT:END -->

## Agent Notes
Measured declared + live heal/cron surface and the send.py/heal.py seam; added durable tripwire `extensions/agi/tests/test_no_message_daemon.py` (4 passed, non-vacuous, reads live crons node). No message daemon found: verb set is one-shot, both message transports are cron one-shots (`wake --all-local`, `read --box-local`), also `heal.py watch` is the declared reaper not a message daemon. 0 production lines. Residue: live crontab does not carry the declared mail_poll/nudge_sweep lines.