---
id: experiment:a00-b4418bfa-five-routes-render
mint_id: 5fd4ad92fddf4e5c958a361c84d54980
type: experiment
parents:
  - hypothesis:a00-b4418bfa-fbae51
next_edges: []
edited_by: a00-118f74e1
line_ceiling: 40
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 5e6696e9648adeda
season: 2
thought_session: iter-DT.25
title: Rendered brief carries all five pane routes on current bytes
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-b4418bfa-five-routes-render

## Experiment

**Target:** `goal:g7.31.3.1` — the cold-seat brief lists the five pane-facing
routes by their `goal:g7.31.3` contract names.

**Claim under test:** `brief.assemble()` renders `brief._ROUTES_SEGMENT` into
every FULL-profile tier brief that can render (kid, parent, director,
prime_director, liaison, and advisor with a vision target) under the
real default profile resolution, naming all five contract names and all six
engine seams; the `survival` profile deliberately omits it.

This is a re-run on the CURRENT built bytes — the previous kid's matching
`proved` verdict was demoted to `inconclusive_lean_disproved:60` because its
cited evidence node
(`experiment:cold-seat-brief-five-routes`, a human slug lacking the agent id)
was never carried by the round diff. This node's basename carries this agent's
id (`a00-b4418bfa`) so the round commit can carry it. `brief.py` itself is
unchanged by this run: the segment is already committed on this base branch
(`_ROUTES_SEGMENT` at `extensions/agi/bin/brief.py:2038`, appended in the
`_finish()` hook at `:2093` only when `profile == "full"`).

**Exact command (from the repo root of this worktree):**

```
python3 -m pytest extensions/agi/tests/test_brief.py -q -k five_pane_routes
```

The falsifier is committed at `extensions/agi/tests/test_brief.py` (the
`goal:g7.31.3.1` block, ~line 1143): it calls `brief.assemble()` for every
full-profile tier that can render and asserts every contract name, every
engine seam and `brief._ROUTES_SEGMENT` itself are present in the RENDERED
text; the survival-profile companion test asserts the segment is absent.
Reproducible from a fresh checkout — no gitignored path, no `brief.py` change.

## Evidence

Raw output of the committed falsifier (base tip `e94b10619`):

```
$ python3 -m pytest extensions/agi/tests/test_brief.py -q -k five_pane_routes
.                                                                        [100%]
1 passed, 152 deselected in 0.88s
```

Route names grepped, verbatim: `write`, `read`, `send`, `dispatch|workflow`,
`rotate|spawn`. Engine seams grepped, verbatim: `write.py`, `commands.py`,
`send.py`, `dispatch.py`, `workflow.py`, `rotate.py`.

## Probe log (three conjuncts)

1. **wire / full-profile tiers** — every tier that can render (kid, parent,
   director, prime_director, liaison, and advisor with a vision target)
   carries all five names, all six seams, and `brief._ROUTES_SEGMENT` itself.
   **held.** Default resolution
   reports `effective_profile(default) = full` (config `operating_mode: full`).
2. **gate / survival profile** — `brief._ROUTES_SEGMENT` absent and the
   `FIVE PANE-FACING ROUTES` heading absent, at 4450 chars vs the full kid
   brief's 10091. **refused as intended.**
3. **carry / round scope** — this node's basename contains `a00-b4418bfa` and
   it is passed to `cli.py done --owns`, so the round commit can carry it.
   **held on inspection** (not yet committed at write time).

## What is NOT proven

- Nothing about `goal:g7.31.3.2` — no sample write+send+dispatch CLI
  transcript was produced or claimed.
- The segment's `read` row names two seams (`commands.py` and `viewport`);
  the six-seam assertion covers `commands.py` and not the `viewport` word.
- No sixth route or second workflow invoker was added; `dispatch.py` /
  `rotate.py` are untouched by this run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Corrective round a00-118f74e1 after the MUR on `goal:g7.31.3.1`. The claimed
bytes did not change — `_ROUTES_SEGMENT` and its `_finish()` seam are
untouched. Three procedural repairs: (1) `parents:` now points at
`hypothesis:a00-b4418bfa-fbae51`, the hypothesis that actually cites this node
in its `evidence_runs`, so the provenance edge and the evidence citation
agree; (2) the counted evidence is now the committed falsifier in
`extensions/agi/tests/test_brief.py`, reproducible from a fresh checkout,
replacing a gitignored `.agi/sessions/` probe; (3) the falsifier was widened to
the tiers that can actually render the segment (`liaison`, and `advisor` when a
vision node exists), which the shared `_ALL_TIERS` never covered.
<!-- THOUGHT:END -->
