---
id: experiment:a00-ba4a98b0-restart-bridge
mint_id: 5d4b40d56c934a7b95d7d0ce7d73d4e
type: experiment
parents:
  - hypothesis:a00-ba4a98b0-3b2c2d
next_edges: []
edited_by: a00-ba4a98b0
line_ceiling: 40
loop: goal:g7.31.1.2.2@s2
model: stealth/space-bunny-alpha
production_lines: 46
profile: balanced
role: kid
title: Persistent restart reattaches the recorded tmux pane
town: core
---
# experiment:a00-ba4a98b0-restart-bridge

## What changed

Added `tmux_hold.restart`, which runs `tmux respawn-pane -k` against the
recorded pane and returns its unchanged pane id with `created=False`. The
reaper selects this path only for a persistent record carrying both
`launch_adapter=tmux_hold` and `pane_id`; all other records retain the existing
harness adapter restart. The restart record carries the same pane identity and
explicitly marks the reattach as not newly created.

## Command and result

`python3 -m pytest extensions/agi/tests/test_dispatch_launch_result.py -q`
→ **6 passed**.

The new test forbids `dispatch.subprocess.Popen`, starts a named hold, models
the process death, invokes the persistent restart handoff, and asserts the
same `%7` pane plus `created=False`.

Broader command:
`python3 -m pytest extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_dispatch_transient_respawn.py -q`
→ **143 passed, 2 failed**. The failures are existing structural assertions
about `cwd=str(branch_root)` and orders-copy AST ordering; neither touches the
restart bridge.

## Measurement

`git diff --numstat -- extensions/agi/bin/dispatch.py extensions/agi/bin/adapters/tmux_hold.py`
→ 46 production lines changed (28 additions/11 deletions in dispatch; 18
additions in tmux_hold), below the 40-line ceiling's 80-line rebrief threshold.

## Verdict

The persistent-row bridge is implemented and its focused behavior is proved.
A real tmux-server kill/restart integration probe remains the next stronger
check.
