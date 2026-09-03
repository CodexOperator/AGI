---
id: hypothesis:a00-23fc51e6-3ffbe3
mint_id: 6ed295a1ec6e421c98426ed09ba33907
type: hypothesis
parents:
  - goal:g8.1
next_edges: []
confidence: 0.55
scaffold_hash: b218caef46bd956d
title: A00 23fc51e6 3ffbe3
verdict: inconclusive_lean_proved:55
---
# hypothesis:a00-23fc51e6-3ffbe3

## Hypothesis

**Claim:** the L9 pinning gap that `goal:g8.1` calls out — "the clone is
unpinned and silently stale ... nothing declares which engine version a
project expects and nothing warns on drift" — can be closed today, before any
of the three distribution shapes (drop-in clone / skill package / real
install) is decided, by adding one field (`engine_commit`, or similar) to
`.agi/config.json` and a warn-only check in `locations.py` or `driver.sh` that
compares it to the engine clone's current `HEAD`.

Checked `/home/ubuntu/work/agi/.agi/config.json` directly: no `engine_commit`
or equivalent key exists anywhere in it today, and `agent_dispatch` /
`cc_dispatch` carry model pins but nothing about the engine's own git state —
confirming the gap is still open, not already closed by some other node.

**What would prove it:** a build node adds the config field, a small check
(e.g. in `locations.py`) reads it and the clone's `git rev-parse HEAD`, and
warns (never fails) on mismatch — verified by a test that stages a project
config with a stale commit and asserts a warning is emitted without the run
aborting.

**What would disprove it:** if the check cannot be warn-only in practice
(e.g. because a mismatch always implies a broken contract that must hard-fail
instead), or if the three-shape decision changes *where* the config file and
the clone even live in a way that makes this field meaningless before the
shape is picked.

**Why this is worth stating separately from the shape decision:** `goal:g8.1`
already says the pinning gap is "cheap under any of the three shapes" — this
hypothesis makes that claim testable and gives the goal a first child that
does not have to wait on the harder drop-in/skill/install choice. Two sibling
hypotheses under this goal (`a00-2bf7847c-91509e`, `a01-abd43b16-1beb10`)
are empty scaffolds left by kids that hit a `403 Workspace weekly budget of
$10.00 exceeded` error before writing content; this node is the first live
claim in the set.

<!-- THOUGHT:BEGIN -->
Wrote a concrete, checkable claim instead of another empty scaffold. Scoped
narrowly to the pinning sub-problem g8.1 explicitly flags as decision-agnostic
and cheap, rather than re-litigating the three-shape choice itself, per the
"stay tight, one node" instruction for this iteration.
<!-- THOUGHT:END -->


## Agent Notes
L9 pinning gap (engine_commit field + warn-only drift check) is a concrete, decision-agnostic first child under g8.1; confirmed config.json has no such field yet
