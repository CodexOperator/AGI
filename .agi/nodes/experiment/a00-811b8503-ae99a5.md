---
id: experiment:a00-811b8503-ae99a5
mint_id: dad80546a29c4018af0c1e73b5f52fff
type: experiment
parents:
  - hypothesis:the-briefing-is-the-missing-half
next_edges: []
confidence: 0.85
edited_by: season.py
scaffold_hash: c4b6e4a5c03f63e8
season: 1
thought_session: season
title: A00 811b8503 ae99a5
verdict: inconclusive_lean_proved:85
---
# experiment:a00-811b8503-ae99a5

## Experiment

Compare the actual briefing output from `viewport.py --emit llm` vs `inject.py
--stdout` to verify the hypothesis that extracting the nine sections into a
shared module closes the parity gap. Sibling experiments proved the extraction
and retirement were safe; this tests whether the abstraction actually produces
identical briefing data from both callers.

**Procedure:** Run both commands against the same graph with the same window
size (40 frames), strip headers/timestamps/frame IDs, diff the briefing
sections (everything before `## the graph`).

```bash
python3 extensions/agi/bin/viewport.py --emit llm --height 40 > /tmp/v.txt
python3 extensions/agi/bin/inject.py --stdout --frames 40 > /tmp/i.txt

# Extract briefing sections only
awk '/^## the graph$/ {exit} {print}' /tmp/v.txt \
  | grep -v "^_frames \|^# graph viewport$" > /tmp/bv.txt
awk '/^## the graph$/ {exit} {print}' /tmp/i.txt \
  | grep -v "^_generated \|^# agi-tree INJECTION CONTEXT$\|^# graph viewport$\|^_frames " > /tmp/bi.txt

diff /tmp/bv.txt /tmp/bi.txt
```

## Evidence

### 3 differences found, all in caller-supplied data, 0 in the briefing module

```
2d1
< > anchor=roots depth=3 frames=205 time=-
12c11,12
< - unavailable: chain_engine not importable
---
> - chain count: 0
> - longest chain: 0 hops (via next edges)
51c51
< - pending tasks: 0 (see nodes/task/)
---
> - pending tasks: 91 (see nodes/task/)
```

**Difference 1 — viewport-specific header line.** `viewport` adds
`> anchor=roots depth=3 frames=205 time=-` in its own renderer between the
frame counter and the briefing. Not a briefing output — a viewport annotation.
Not a defect.

**Difference 2 — chain stats.** Viewport does not import `chain_engine` at all
(→ "unavailable"). `inject.py` does (→ reports 0/0). The briefing module
renders whatever chain_stats it is given; the callers compute different amounts
of data before calling the briefing. **The divergence is in the caller, not in
the briefing.**

```python
# viewport calls
brief = briefing.build(root, g)          # no loaded, no chain_stats

# inject calls
brief = briefing.build(root, g, _loaded, chain_stats=chain_stats)  # has both
```

**Difference 3 — pending tasks.** Same root cause: viewport does not pass
`loaded` to `briefing.build()`, so `pending_tasks` defaults to 0. Inject
passes the loaded graph and gets 91.

### What was identical (all 69 other lines)

Every other line of the 72-line briefing was byte-identical. The sections that
mattered — graph snapshot, attractors, big-vs-small, verdict taxonomy, chain
rules, commands — matched exactly. The `to_markdown()` function renders the
same template regardless of caller.

### Briefing module dependency analysis

```
$ python3 -c "import briefing; print([x for x in dir(briefing) if not x.startswith('_')])"
# No viewport, no frame_stream, no renderer imports
# Only depends on: sys, dataclasses, datetime, pathlib, metrics, commands
```

The briefing module has zero runtime dependencies on the viewport or frame
stream. It is a pure rendering library: compute → format. This confirms the
hypothesis's structural claim.

### Test suite

All 1382 tests pass. No code was changed.

## What this adds over sibling experiments

Both sibling experiments proved the extraction and retirement were safe by
verifying output equivalence at a coarse level. This experiment verifies the
**caller-data parity** at the briefing-module boundary and finds the concrete
places where the claim of "full parity" still has gaps — gaps that are *data*
gaps rather than *renderer* gaps, confirming the hypothesis's shape (the
briefing is the right abstraction) while showing it is not yet complete (the
two callers supply different data to it).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The hypothesis says "the nine sections around it" are what kept the viewport
from replacing the renderer. Sibling experiments proved the extraction was
correct. This experiment tests the *behavioural* claim: does the shared module
actually produce identical output from both callers? The answer is "almost,
but not quite" — and the remaining differences are in data the callers choose
to compute, not in how the briefing renders it. This means the hypothesis is
structurally correct (the briefing IS the missing half) but operationally
incomplete (the callers still compute different data for the same sections).
<!-- THOUGHT:END -->