---
id: hypothesis:l4b13-workflow-router
mint_id: 9c6cf3ef5c1e4ea7abb88327ae5b8076
type: hypothesis
parents:
  - idea:l4b13-workflow-router
next_edges: []
confidence: 0.6
edited_by: sanctuary-helper
scaffold_hash: 9bef96f39da1250a
season: 2
tags:
  - hypothesis
testable_claim: workflow.py exposes ONE router that every workflow dispatches through -- the parent/kid loop, brief drafting, round review, and any future Master workflow -- and a workflow started the Claude Code way still lands a row in graph workflow-tracking; provable by one workflow of each kind showing up in the same tracked-workflow log (owner, l4-plan A:320).
thought_session: sanctuary-helper-05
title: A single workflow router dispatches every workflow
---
<!-- BODY:BEGIN -->
# hypothesis:l4b13-workflow-router

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## L4.22 brief -- ONE workflow router: survey first, then close the real gap

DO NOT BUILD A NEW ROUTER BLIND. `extensions/agi/bin/workflow.py` (801
lines) ALREADY EXISTS and already IS a harness-agnostic workflow runner:
`workflow.py run <name> --harness pi|claude-code --args JSON`, a registry
read from `.agi/config.json` `workflows.<name>` (today: `review`,
`drafting`, `deep-search`), `register`/`list`/`validate` subcommands, and
its own docstring states "A workflow lives in the graph as a build node
under extensions/agi/workflows/". So the CLAIM this round must prove or
fix is narrower than "build a router" -- it is: does EVERY workflow this
plan's owner text names -- the parent/kid loop itself, brief drafting,
round review, and "any future Master workflow" -- actually dispatch
THROUGH this one router, and does a workflow started the Claude Code way
still land a row in graph tracking? The owner's own words (l4-plan A:320):
"I just put that there to illustrate that our current parent-kid loop
unit is also a workflow that should belong in the workflow layer it's
just the parent is kinda the built-in driver for the workflow" -- read
that as a strong hint that the parent/kid loop (`dispatch.py` with
`--tier parent`/`--tier kid`) is NOT YET registered as a `workflow.py`
entry the way `review`/`drafting`/`deep-search` are, which would be
exactly the gap.

FIRST, SURVEY (do this before writing any code): read `workflow.py` in
full (`run`, `register`, `list`, `validate`, and whatever tracks a
workflow's EXECUTION, not just its definition -- grep for how/whether a
`run` invocation writes anything to the graph, since only the workflow's
own script+manifest pair being a build node is confirmed, not each RUN of
it). Read `.agi/config.json`'s `workflows` key (its three current rows).
Determine precisely: (a) is the parent/kid loop unit reachable via
`workflow.py run <name>` today, or does `dispatch.py` bypass the router
entirely? (b) does a `claude-code`-harness workflow run leave any trace in
the graph beyond its static build node, or does "lands in graph tracking"
not exist yet for RUNS at all?

FILE: extensions/agi/bin/workflow.py (the router itself) and
`.agi/config.json`'s `workflows` key; do not touch `dispatch.py`,
`send.py`, `write.py`, `rotate.py`, or `zoom.py` (existing DO-NOT-TOUCH
list from prior rounds still applies unless your survey proves one of
them is the actual gap -- say so explicitly if it is, do not silently
edit it).

CHANGE: close ONLY the gap your survey actually finds. If the parent/kid
loop is not a registered workflow, register it (or explain in your node
why it structurally cannot be, e.g. because it is the fallback driver
every OTHER workflow is built on top of, which the owner's own words
above suggest may be the intended shape rather than a bug). If CC-started
runs are not tracked, add the minimal tracking (a build-node-adjacent
record, or extending the existing build-node-per-workflow-definition
pattern to also record a run) -- do not invent a whole new tracking
subsystem if a small addition to the existing pattern covers it.

VERIFY: `python3 extensions/agi/bin/workflow.py list` and `validate`
still pass after your change. Show one pi-harness workflow run and one
claude-code-harness workflow "showing the usual way" (per the owner's
words) AND landing a row in graph tracking, side by side, in your
experiment node. Run only whatever test file already covers
`workflow.py` (`grep -l workflow extensions/agi/tests/*.py`) plus any new
test you add -- never the full suite.

BUILD NODE: unlike the B23 rounds, this one DOES mint a build node if you
change `workflow.py` or `.agi/config.json` -- use `goal:s29`'s shape
`[build:<id>, goal:<id>]` for a new VERSION of either existing file
(parents: the existing build node for that file if one exists -- check
first with `links.py` or a grep of `payload_ref:` across `.agi/nodes/build/`
-- plus `goal:g15`, since most code lands there per A:162). Never
`[goal:<id>]` alone.

KID CEILING: 3 -- survey, implement, verify is a legitimate 3-step split
across kids if the parent chooses to run it that way; one kid could also
do all three if the gap turns out small.

DO NOT: rebuild `review`/`drafting`/`deep-search`'s existing behaviour.
Do not touch the DO-NOT-TOUCH files unless your survey proves otherwise
(and if so, say exactly why in your node). Do not `git add -A`. Do not run
`grid.py commit --all` on this seat branch -- end at `git commit` +
`git push` on your own branch/worktree.

REPORT: write one `experiment` node whose `parents` is this hypothesis,
with your survey findings FIRST (what already worked, what the actual gap
was) and then your verdict. `evidence_runs` must resolve to real node ids;
your own experiment counts once it exists. List every verify command and
its actual output.
