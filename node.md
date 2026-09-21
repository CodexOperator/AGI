---
id: hypothesis:l4b17-success-metrics
mint_id: 5dfea3cc340d478d93fc24d24bcc8b0d
type: hypothesis
parents:
  - idea:l4b17-success-metrics
next_edges: []
confidence: 0.6
edited_by: sanctuary-helper
scaffold_hash: e4475ef0cf701564
season: 2
tags:
  - hypothesis
testable_claim: Each of the Sanctuary Council's seven success metrics -- average tokens/turn, total hierarchy tokens/hour, conclusive verdicts, overview accuracy vs last season, subscription tokens per season, vision-adherence score, and the OpenRouter/subscription spend ratio -- is computed from one named source and written to one recorded place; provable by reading season N's and season N-1's recorded values for all seven and diffing them (owner, l4-plan A:263).
thought_session: sanctuary-helper-05
title: The seven success metrics each get one number, one source, one place recorded
---
<!-- BODY:BEGIN -->
# hypothesis:l4b17-success-metrics

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## L4.25 brief -- the seven success metrics: this is new tracking, not a gap-fix

SURVEYED ALREADY, so you do not have to re-discover it: `extensions/agi/
bin/metrics.py` (1186 lines) EXISTS and computes real metrics --
`thought_stats`, `node_lifecycle_stats`, `push_gap_stats`, `evidence_stats`,
`_broken_links`, `outcome_coverage`, `deprecation_score_delta`,
`goal_attribution` -- but these are all GRAPH-STRUCTURE quality metrics
(the loop's own `outcome_coverage` scoring target, per `.agi/config.json`
`metric_primary`). NONE of the Sanctuary Council's seven OPERATIONAL
success metrics appear anywhere in this file today: average tokens/turn,
total hierarchy system tokens/hour, conclusive verdicts, overview accuracy
vs last season, subscription tokens per season, vision-adherence score,
and the OpenRouter/subscription spend ratio (owner, l4-plan A:263, quoted
in full on this hypothesis's own `idea:l4b17-success-metrics` parent and
on `goal:g16.1`). This is genuinely NEW instrumentation, not a bug fix --
say so plainly in your node rather than searching for a hidden
implementation that is not there.

WHAT ALREADY EXISTS THAT YOU SHOULD REUSE, NOT REBUILD: `provisioning.py
status` already prints real OpenRouter key spend (`used`/`remaining` per
key) -- that is your subscription/OpenRouter spend DATA SOURCE, not
something to reimplement. `spawn_budget.py status` already tracks live
agents with `tier=` -- a starting point for tokens/turn or tokens/hour if
per-agent token counts are logged anywhere (check `.agi/sessions/write-
log.jsonl` and any session manifest under `.agi/sessions/iter-*/` for
token counts before assuming none exist). `season.py` (grep for it) is
where a season boundary is defined -- your "compared to last season"
half needs season.py's own notion of "this season" vs "last season", not
a new one you invent.

FILE: likely a NEW small module (e.g. `extensions/agi/bin/success_
metrics.py`) that reads from the sources above, OR an addition to
`metrics.py` if the seven fit naturally alongside its existing `compute`/
`emit` shape -- your call, but say which and why. Do not touch
`workflow.py`, `dispatch.py`, `send.py`, `write.py`, `rotate.py`, `zoom.py`.

CHANGE: each of the seven metrics gets ONE named source (a function or a
read from an existing data file) and ONE recorded place (a file under
`.agi/sessions/` for per-season telemetry is the existing convention --
check how `season.py` already records season-boundary data and match its
shape rather than inventing a new one).

VERIFY: run your new metric computation for the CURRENT season (season 2)
and show all seven values with their sources. If season 1's data still
exists anywhere (check `.agi/sessions/` for anything season-1-scoped),
diff season 2's partial-so-far values against season 1's to prove the
"compared to the one before it" half of the claim is mechanically
possible, even if season 2 is incomplete. Run only whatever test file you
add -- never the full suite.

BUILD NODE: this mints a build node for whatever new/changed file you
land -- `goal:s29` shape `[mvp:<id>]` for a genuinely new file (mint a
small `mvp` first stating what it must satisfy: the seven metrics, one
source and one recorded place each) or `[build:<id>, goal:<id>]` if you
extend `metrics.py` (parent it on `metrics.py`'s existing build node if
one exists, plus `goal:g16` since this is the Sanctuary Council's own
success-tracking goal). Never a bare `[goal:<id>]`.

KID CEILING: 3 -- one metric-family per kid is a reasonable split (e.g.
token/spend metrics; verdict/accuracy metrics; the season-diff mechanism),
or fewer kids doing more each if the parent judges that faster.

DO NOT: touch the DO-NOT-TOUCH files. Do not invent a season-boundary
concept that duplicates `season.py`'s. Do not `git add -A`. Do not run
`grid.py commit --all` on this seat branch -- end at `git commit` +
`git push` on your own branch/worktree.

REPORT: write one `experiment` node whose `parents` is this hypothesis,
showing all seven metrics computed with their sources, and a verdict.
`evidence_runs` must resolve to real node ids; your own experiment counts
once it exists. List every verify command and its actual output.
