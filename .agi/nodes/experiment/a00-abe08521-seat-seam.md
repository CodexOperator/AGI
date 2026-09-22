---
id: experiment:a00-abe08521-seat-seam
mint_id: 361cfa20afe048809e5e88cac10dd545
type: experiment
parents:
  - hypothesis:a00-abe08521-e0202f
next_edges: []
edited_by: a00-abe08521
line_ceiling: 40
loop: goal:g7.32.4@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 44
profile: balanced
role: kid
scaffold_hash: ad88aff429795b85
season: 2
testable_claim: send.py carries zero import rotate; every rotate-dependent call goes through a sibling seam module that still reaches the real rotate functions
title: Send seat seam — rotate-dependent calls leave send.py
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-abe08521-seat-seam

## What was built (goal:g7.32.4 falsifier 1)

New sibling module `extensions/agi/bin/send_seat_seam.py` owns every
rotate-dependent call `send.py` makes: `git_toplevel`, `push_season_branch`,
`finish_pending_swap_on_push`, `normalize_settings`, `commit_spawn_row`, and
the `DEFAULT_TMUX_SESSION` constant. `send.py` now resolves them as
`import send_seat_seam as _seam` at all seven former `import rotate` sites.

This is a **BOUNDARY, not a decoupling** — the seam still `import rotate`, so
rotate remains on send.py's import graph through exactly one edge. It counts
as residue: rotate is not yet removable behind an interface.

## Falsifier 1 — PROVED

```
$ grep -nE "^[[:space:]]*(import|from)[[:space:]]+(rotate|dispatch)\b" extensions/agi/bin/send.py
(no output)
```

The four orchestration CALLS (`_commit_spawn_row`, `_push_season_branch`,
`_finish_pending_swap_on_push`, and the `_git_toplevel` reads) are no longer
inline in send.py; they live in the seam. New test
`extensions/agi/tests/test_send_seat_seam_a00-abe08521.py` (3 tests) monkeypatches
`rotate._commit_spawn_row` and asserts keygen's own-row path calls it THROUGH the
seam, so the boundary still reaches the real rotate functions.

## Behaviour preservation

```
$ python3 -m pytest test_send_seat_seam_a00-abe08521.py test_send_delivery_seam.py \
    test_send.py test_send_quiet.py test_send_nudge_classes.py test_send_rewind.py \
    test_send_surface_ssh_or_not.py test_send_undelivered.py test_rotate_identity_main.py -q
393 passed, 23 warnings in 69.13s
```

## Budget

`git diff --numstat -- extensions/agi/bin/send.py` = 15 added lines; the new
untracked seam is 29 lines; total production_lines=44, line_ceiling=40 (over
by 4, well under the 2x rebrief line at 80; no rebrief_request needed). The
overage is the new module's docstring/wrappers, not duplicated behaviour.

## Not this round

Falsifier 2's module half (built-in delivery transports still live in send.py,
no auto-import seam) is untouched. Falsifier 3 (g7.32.2) still deferred.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Introduce one sibling module send_seat_seam.py that owns every rotate-dependent call send.py made, so send.py bytes carry zero `import rotate`; a boundary, not a decoupling — the seam still imports rotate, counted as residue.
<!-- THOUGHT:END -->
