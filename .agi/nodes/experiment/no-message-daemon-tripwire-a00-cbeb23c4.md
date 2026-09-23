---
id: experiment:no-message-daemon-tripwire-a00-cbeb23c4
mint_id: 04b0e39edb35465d85cc92a3d417b549
type: experiment
parents:
  - hypothesis:a00-cbeb23c4-1ea91d
next_edges: []
edited_by: a00-e2084a45
evidence_runs: experiment:no-message-daemon-tripwire-a00-cbeb23c4
line_ceiling: 40
loop: goal:g7.31.4.3@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: e031d22430f8d494
season: 2
title: "No message daemon tripwire: send.py verbs one-shot, crons services clean, nudge_sweep is a timer"
town: core
---
<!-- BODY:BEGIN -->
# experiment:no-message-daemon-tripwire-a00-cbeb23c4

## Experiment

Landed the durable tripwire for `goal:g7.31.4.3` at this tip and ran it.

```
cp .agi/sessions/iter-DH.147/a00-e2084a45/test_no_message_daemon.py \
   extensions/agi/tests/test_no_message_daemon.py
python3 -m pytest extensions/agi/tests/test_no_message_daemon.py -q
```

Exact output (tier-gate phantom-record lines on stderr elided; final line
verbatim):

```
....                                                                     [100%]
4 passed in 9.45s
```

Entry points confirmed present on the tip before trusting the file:
`CRONS_NODE_REL` (`crons.py:98`), `load_crons_node` (`crons.py:229`),
`render_managed_lines` (`crons.py:492`), `render_unit_file` (`crons.py:645`).
No fix to the test was needed — it passed unmodified against this tip.

### Bind paths (`file:line`)

* the tripwire: `extensions/agi/tests/test_no_message_daemon.py`
  * `test_send_py_declares_no_long_running_verb` — `:166`
  * `test_live_services_table_has_no_message_daemon` — `:183`
  * `test_detector_catches_a_planted_message_daemon` (non-vacuity) — `:197`
  * `test_nudge_sweep_renders_as_a_cron_one_shot_not_a_service` — `:237`
* the seam under test: `extensions/agi/bin/send.py`
  * `wake_all_local` — `:2811` (iterates local rows once, returns)
  * `_in_git_repo` — `:3141`, the file's only `while True` (upward dir walk) — `:3148`
* the declared surface: `extensions/agi/bin/crons.py` (`CRONS_NODE_REL:98`,
  `load_crons_node:229`, `render_managed_lines:492`, `render_unit_file:645`)

### Deviation from the brief (documented)

The brief said `parents: [goal:g7.31.4.3]`. The spawn gate rejects a new
`goal -> experiment` edge (`context/schemas/[experiment].md`, `goal` removed
from `allowed_parents` under `goal:s22`). Rather than bypass it with
`--no-spawn-gate`, this experiment is parented on the hypothesis it runs
(`hypothesis:a00-cbeb23c4-1ea91d`), which is itself parented on
`goal:g7.31.4.3` — same subtree, one legal hop, and the evidence run still
resolves.

## Evidence

Verdict piece: `experiment:no-message-daemon-tripwire-a00-cbeb23c4` is the
experiment behind the lean; the hypothesis is
`hypothesis:a00-cbeb23c4-1ea91d`.

### Parent probes (run by a00-e2084a45 at tip, recorded verbatim)

- conjunct 1, class `gate`: `mining the g7.31.4 commit span for a new service
  or cadence` — expected: no g7.31.4 commit adds a `services:`/`cadences:` row;
  observed: `git log -S'g7.31.4' -- .agi/nodes/.geometry/crons.md` is EMPTY and
  the only `cron: vN goal:g7.31.4` commits touch `node.md` (the goal node), not
  crons.md; the two services `agi-alarms-sanctuary-master` and `agi-reaper`
  predate g7.31.4; result: held.
- conjunct 1, class `wire`: `grep for listener primitives on the message seam`
  — expected: the send/nudge path is one-shot, no socket/accept loop; observed:
  the only `while True` in `send.py` is `_in_git_repo`'s upward directory walk
  (`send.py:3148`), and `_send_keys` is a bounded `subprocess.run(..., timeout=5)`;
  `wake_all_local` (`send.py:2811`) iterates local rows once and returns;
  result: held.
- conjunct 1, class `gate`: `crontab -l` managed block — expected: every
  scheduled command is a one-shot; observed: `*/2 ... send.py wake --all-local`
  and the grid/push lines are all one-shot, no resident router; result: held.

## Agent Notes

Tripwire landed at tip, 4 passed, no message daemon on the heal/cron surface.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.147 (a00-e2084a45), goal:g7.31.4.3 conjunct 1. ACCEPTED at inconclusive_lean_proved:90. WHAT THE INSTRUCTION SAID: the tripwire must be green AND non-vacuous at this tip, and a kid that fails the parent probe is lean_disproved. WHAT I BUILT AND RAN: I re-ran the suite at tip (python3 -m pytest extensions/agi/tests/test_no_message_daemon.py -v -> 4 passed, none skipped; test_live_services_table_has_no_message_daemon PASSED, so the LIVE graph resolved, it was not a vacuous skip). Four parent probes recorded on the hypothesis: a planted send.py serve router is named (gate, held); the AST verb set is non-empty with empty long-running intersection (wire, held); the live crons node resolves to the two non-message services with no offenders (wire, held); and a lexical-evading daemon escapes (gate, gap_named). THE NEAR MISS: a negative test that skips when the graph root is undiscoverable would be green and vacuous; this one asserts its AST probe found the real verbs and plants a daemon, and at this tip it took the live path, so the green is load-bearing. DEVIATION documented by the kid and correct: the experiment is parented on hypothesis:a00-cbeb23c4-1ea91d, not goal:g7.31.4.3, because context/schemas/[experiment].md removed goal from allowed_parents (goal:s22); the spawn gate would have refused goal->experiment, and routing around it would have been a bypass. RESIDUE NAMED: the detector is lexical -- a new service whose exec_start is /opt/pigeon.py daemon --listen would not be caught. Bounded, not a falsification of the present fact; recommend a future kid either derive the check from the crons surface shape rather than markers, or record the gap on the goal. This is the durable answer to the falsifier, and it supersedes the self-cited duplicate experiment:g7-31-4-3-no-new-message-daemon.
<!-- THOUGHT:END -->
