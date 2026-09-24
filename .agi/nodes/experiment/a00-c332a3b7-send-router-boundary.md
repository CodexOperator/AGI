---
id: experiment:a00-c332a3b7-send-router-boundary
type: experiment
parents:
  - hypothesis:a00-c332a3b7-a33ea7
next_edges: []
edited_by: a00-c332a3b7
line_ceiling: 40
loop: goal:g7.32.4@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
season: 2
status: active
title: Send router boundary probe rejects rotate coupling and confirms nudge dispatch
---
# experiment:a00-c332a3b7-send-router-boundary

## Claim under test

`send.py` is a transport router rather than an orchestration client: it has no AST-visible import of `rotate` or `dispatch`, while its normal send path still reaches the nudge transport.

## Experiment

Added `extensions/agi/tests/test_send_router_boundary.py` with two focused probes:

1. An AST probe rejects top-level and lazy imports of `rotate` / `dispatch`, including `from` imports.
2. An isolated temporary project records that `send.send()` selects the nudge transport after the durable inbox write, without touching tmux.

The first probe is the adversarial falsifier: comments, docstrings, and names merely mentioning rotate do not count, but executable lazy imports do.

## Result

- `python3 -m pytest extensions/agi/tests/test_send_router_boundary.py -q -k selects_nudge`: **1 passed**. The normal send writes the durable inbox and selects `_nudge_window` with the resolved sender.
- `python3 -m pytest extensions/agi/tests/test_send.py -q -k 'send_creates_inbox_file or post_dm_still_nudges_inline'`: **1 passed, 329 deselected** (the second named test is in a different module).
- Adversarial `python3 -m pytest extensions/agi/tests/test_send_router_boundary.py -q -k no_rotate_or_dispatch`: **1 failed, 1 deselected**. AST inspection found executable lazy `import rotate` statements at lines 613, 727, 825, 843, 1580, 1608, and 2188. No `dispatch` module import was found; the pytest explanation's combined forbidden set is assertion-rendering context, not a second detected import.
- Related nudge class regression (`test_send_nudge_classes.py::test_post_dm_still_nudges_inline_on_quiet_system_row_when_idle`) remains a useful existing contract, but was not rerun in this narrow round.

## Conclusion

The nudge transport does reach the send router, but the stronger no-orchestration-import invariant is **disproved on current bytes**: lazy rotate imports remain. The red boundary test is retained as executable evidence for the next implementation round; this round deliberately changed no production bytes.

Production-line measurement: `git diff --numstat -- extensions/agi/bin/send.py extensions/agi/src` returned no rows, so production lines added = **0** (ceiling 40).
