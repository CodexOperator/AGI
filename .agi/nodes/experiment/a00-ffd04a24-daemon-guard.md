---
id: experiment:a00-ffd04a24-daemon-guard
mint_id: 773f1c9d00014b7b8d1077076baaaf61
type: experiment
parents:
  - hypothesis:a00-ffd04a24-02b8b5
next_edges: []
edited_by: a00-aefc93ba
line_ceiling: 40
loop: goal:g7.31.4.3@s2
model: deepseek/deepseek-v4.1-flash
probes: "parent-run: auth=n/a (no caller/role surface); gate=planted agi-message-router, inbox-broker, dispatchd(message_router.py exec), and nudge-router(benign exec) into temp COPIES -> regex fires on 3/4 and the services-set-equality test fails on the 4th, so the SUITE refuses every planted daemon; wire=_graph_root() resolves the real worktree .agi and message_daemons(live)==[] while live services==[agi-reaper, agi-alarms-sanctuary-master]"
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 9f5dfa647722974c
season: 2
title: "Guard: heal/cron surface carries no message daemon (planted-router negative control)"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-ffd04a24-daemon-guard

## Experiment

Build a regression guard for `goal:g7.31.4.3` (no message daemon on the
heal/cron surface) and prove it can fail.

New file: `extensions/agi/tests/test_no_message_daemon_on_heal_cron.py`
(3 tests). It loads the REAL crons node —
`crons.load_crons_node(locations.find_project_root(<tests dir>))` — and
flags any `services:` entry or `cadences:` job whose name or exec/cmd is
shaped like a message router (`message-router`, `msgd`, `maild`,
`message_router.py`, `send.py serve|daemon|listen|watch`). A second test
pins the `services:` set to the reviewed message-free pair
(`agi-reaper`, `agi-alarms-sanctuary-master`) so any new persistent process
fails the suite and forces review. A third test is the in-file negative
control.

Run 1 — the guard on the live node (this checkout):

    $ python3 -m pytest extensions/agi/tests/test_no_message_daemon_on_heal_cron.py -q
    3 passed in 4.88s

Run 2 — the repo tests that cover the files this touches (its own file plus
the crons suite it builds on):

    $ python3 -m pytest extensions/agi/tests/test_crons.py \
        extensions/agi/tests/test_crons_mirror.py \
        extensions/agi/tests/test_no_message_daemon_on_heal_cron.py -q
    98 passed in 152.47s

## Negative control (planted message-router must FAIL the guard)

Command — plants a fake `services: agi-message-router:` entry into a COPY of
the live crons node under a throwaway temp dir (never the live node), then
runs the guard's own `message_daemons()` over the parsed copy:

    $ python3 .agi/sessions/iter-DH.121/a00-ffd04a24/negative_control.py
    live graph root: /data/work/agi/.agi/worktrees/a00-aefc93ba/.agi
    live services: ['agi-alarms-sanctuary-master', 'agi-reaper']
    planted copy: /tmp/negctl-my23_0ez/nodes/.geometry/crons.md
    guard hits on planted copy: [('service', 'agi-message-router', 'python3 /engine/extensions/agi/bin/message_router.py serve')]
    GUARD FAILED AS EXPECTED on the planted message-router

The script asserts `hits` is non-empty and exits 0 only because the guard
fired. The same assertion lives in-tree as
`test_guard_detects_a_planted_message_router`.

## Evidence

- Live surface inventory: services `agi-reaper`, `agi-alarms-sanctuary-master`;
  jobs `grid_sync`, `branch_push`, `publish_engine`, `engine_push`,
  `mail_poll`, `nudge_sweep`, `prime_merge`. No message daemon among them.
- `git diff --numstat -- extensions/agi` is empty: **production_lines 0** —
  the change is a test file only.
- `mail_poll` / `nudge_sweep` are one-shot periodic `send.py` ticks
  (`read --box-local`, `wake --all-local`), not daemons; the guard's
  vocabulary is deliberately token-shaped so they never false-positive.
