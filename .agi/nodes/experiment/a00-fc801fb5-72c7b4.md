---
id: experiment:a00-fc801fb5-72c7b4
mint_id: 5acd51f89bdf4025a4c745bc25272e6f
type: experiment
parents:
  - hypothesis:l4-remote-thought-town-a-box-cell-one-guard-and-a-five-minute-mail-poll-verified-on-a-stand-in-box
next_edges: []
confidence: 0.65
edited_by: director-sanctuary
evidence_runs:
  - experiment:a00-fc801fb5-72c7b4
line_ceiling: 40
loop: hypothesis:l4-remote-thought-town-a-box-cell-one-guard-and-a-five-minute-mail-poll-verified-on-a-stand-in-box@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 170
profile: balanced
rebrief_request: "OVER 2x CEILING: 170 added production lines vs 40 (crons.py +52, send.py +40, heal.py +9, rotate.py +7, boxes.py 62 new). The box guard, three call sites, the crons box filter and mail_poll are BUILT and green (6 new tests + 880 regression tests). REMAINS: STEP 6 stand-in (clone under /home/opc with AGI_BOX=local-town + placeholder key, local bare hub, crons.py apply, one mail_poll tick, envfile --check + verification quick from the stand-in side) and the one [decision] line for the thought-master/director-thought box row edit. Need either a higher ceiling to absorb the verbose blocks or a ruling that docstrings and the fail-open guard are not counted."
role: kid
scaffold_hash: 47ed83634c94755a
season: 2
title: SM.117 box guard + crons box filter + mail_poll built and tested; core render unchanged, local-town = branch_push + mail_poll; stand-in not done (over ceiling)
town: core
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-fc801fb5-72c7b4 — the box guard, the crons box filter, and `mail_poll`

## Experiment

Built the SM.117 box-membership machinery on the bytes of this round and
proved it with a new hermetic test file. Measured first, then implemented:

- `bin/boxes.py` (NEW): `default_box(root)` reads the `default_box` cell on
  `nodes/.geometry/posts.md`; `this_box(root)` reads `AGI_BOX` from the env or
  the resolved `.env`, else that cell; `row_is_local(root, row)` compares the
  row's `box` cell (else the default) to `this_box`. An undeclared graph
  (no `AGI_BOX`, no `default_box`) is fail-open `True` so no watcher crashes
  on a legacy/single-box graph. The module docstring records the deliberate
  distinction from `rotate.py`'s unrelated `_box_fact()` load-snapshot `box`.
- Schema: `box` added to the `sanctuary-master` `actor_rows` fields in
  `.agi/context/schemas/[config].md`; `AGI_BOX` added to `.geometry/secrets.md`
  `optional_keys`; `default_box: core-town` added to `.geometry/posts.md`
  (top-level cell only — NO `posts:` row touched).
- Three call sites: `send.py` whois (`_whois_answer` now names a foreign row's
  box instead of asserting its `@id` window) and nudge (`_nudge_target`
  refuses a foreign row by name); `heal.py` `_watch_seats` drops foreign rows
  and logs their names; `rotate.py` `cmd_status --seats` skips them with one
  `box=... skipped: foreign box` line instead of a false `age=?`.
- `crons.py`: `mail_poll` added to `KNOWN_JOBS`; every job takes an optional
  `box`. **Rule, stated once:** a job with NO `box` renders on EVERY box; an
  explicit string or list RESTRICTS it to exactly those boxes. Malformed
  values are refused by name. `render_managed_lines(..., box_name=None)` takes
  the box as a test seam. Live `.geometry/crons.md`: `grid_sync` gets
  `box: core-town`, `mail_poll` gets `box: local-town`, `branch_push` stays
  boxless (universal).
- `send.py read --box-local`: mail_poll's one service reader — consumes every
  LOCAL row's inbox and names each foreign row it skips.

## Evidence

Rendered crons, same node dict, two box names (in-process, this checkout):

```
core-town  : grid_sync base + 5 mirror lines + branch_push  = today's 7 lines
local-town : branch_push + `send.py read --box-local`        = exactly 2
```

A node dict declaring NO `box` fields renders byte-identically for
`core-town` and `local-town` (the no-regression half). With the live
box fields, `core-town` renders byte-identically to the no-box render.

```
python3 -m pytest extensions/agi/tests/test_box_guard.py -q
-> 6 passed

python3 -m pytest extensions/agi/tests/test_crons.py \
  extensions/agi/tests/test_crons_mirror.py extensions/agi/tests/test_no_literal_town.py \
  extensions/agi/tests/test_heal_watch.py extensions/agi/tests/test_heal_seats.py \
  extensions/agi/tests/test_box_guard.py -q
-> 171 passed

python3 -m pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_rotate.py \
  extensions/agi/tests/test_rotate_handover.py extensions/agi/tests/test_send_nudge_classes.py \
  extensions/agi/tests/test_send_quiet.py -q
-> 709 passed
```

The six required cases: (1) a foreign row is skipped by name at whois/nudge,
heal watch and rotate status; (2) no cell = default box = local; (3) `this_box`
from `AGI_BOX`, unset = default; (4) core byte-identical / local = branch_push
+ mail_poll, same node dict, two box names; (5) a dm committed on the core
side is read on the stand-in after ONE `git fetch` through a bare hub, and the
foreign row is named as skipped; (6) no runnable `core-town`/`local-town`
literal in `bin/*.py` (AST scan).

`sudo -n -u opc bash -c 'whoami; echo HOME=$HOME'` -> `opc` / `/home/opc`
(the stand-in user exists and is reachable without a password).

## What remains (the over-ceiling stop)

`git diff --numstat` over the production paths:
`crons.py +52`, `send.py +40`, `heal.py +9`, `rotate.py +7`, plus
`boxes.py` 62 new = **170 added production lines** against the 40-line
ceiling (> 2x). Per the round's rule I STOP here and file a rebrief request
rather than continuing.

NOT yet done, and the reason this node is not `proved`: the STEP 6 stand-in —
a clone under `/home/opc` with its own `.env` (`AGI_BOX=local-town`, a
placeholder provisioning key), a local bare hub, `crons.py apply` on the
stand-in, one `mail_poll` tick, and `envfile.py --check` /
`verification.py --level quick` output from the stand-in side. Also not
delivered: the one `[decision]` line carrying the exact `box` row edit for
`thought-master` / `director-thought` (a text deliverable, no row touched).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Independently reviewed: reran every cited test file in the kid own worktree (test_box_guard.py plus the 10 other files cited across both groups, deduped into one run) -- 880 passed, exactly matching 171+709 from the node, zero failures. Read boxes.py directly: the fail-open in row_is_local catches only the this_box() undeclared-graph case (no AGI_BOX, no default_box cell) and is narrowly scoped to a liveness/display guard, not an access boundary -- reasonable and documented in the THOUGHT block, not a concern. Merged the branch clean (no conflicts, 9 files, matches the cited diff exactly).

Evaluated against the Prime re-scope that landed mid-round (core trunk 36c1bed0d, not visible to this kid): the re-scope explicitly leaves steps 1-5 (the guard, the three call sites, the crons box filter, mail_poll) UNCHANGED and only redirects step 6 (the stand-in) to real-box work over ssh, skipped-unless-it-drops. So the one gap this node flags as remaining -- the stand-in -- is not actually a gap anymore, it is superseded scope; what is actually still open is the real-box slice, which is new work for a follow-up round (SM.117b), not something this kid left unfinished. The rebrief_request and the stop-at-2x-ceiling were the right call independent of the re-scope, and doubly right in hindsight since continuing toward the stand-in would have built something the re-scope now skips.

Accepting the verdict as delivered (inconclusive_lean_proved:65) -- the evidence supports it, and the open item is honestly scoped as open rather than papered over.
<!-- THOUGHT:END -->

## Agent Notes
SM.117 box guard built on the bytes: boxes.py + schema/geometry cells + whois/nudge/heal/status call sites + crons box filter + mail_poll/read --box-local; 6 new tests + 880 regression tests green; core render byte-identical, local-town renders exactly branch_push+mail_poll; over 2x ceiling -> rebrief_request filed; STEP 6 stand-in remains.
