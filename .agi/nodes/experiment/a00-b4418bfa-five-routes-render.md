---
id: experiment:a00-b4418bfa-five-routes-render
mint_id: 5fd4ad92fddf4e5c958a361c84d54980
type: experiment
parents:
  - hypothesis:a00-13a360dc-c2aae9
next_edges: []
edited_by: a00-b4418bfa
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
every FULL-profile tier brief (kid, parent, director, prime_director) under the
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
PYTHONPATH=extensions/agi/bin python3 \
  .agi/sessions/iter-DT.25/a00-b4418bfa/probe_five_routes.py
```

The probe imports the real `brief` module, calls
`brief.assemble(tier=..., agent_id="a00-b4418bfa", iter_n=1, cli_py="/x/cli.py")`
for each of `kid, parent, director, prime_director` with `scaffold=`/`target=`
as the repo tests do and NO `profile=` kwarg (so the default resolution runs),
and asserts the contract names and seams. It then renders `profile="survival"`
and asserts the segment is absent.

## Evidence

Raw output of the command above (saved at
`.agi/sessions/iter-DT.25/a00-b4418bfa/probe_output.txt`):

```
effective_profile(default) = full
tier=kid: names_missing=[] seams_missing=[] segment=True chars=10091
tier=parent: names_missing=[] seams_missing=[] segment=True chars=14821
tier=director: names_missing=[] seams_missing=[] segment=True chars=10406
tier=prime_director: names_missing=[] seams_missing=[] segment=True chars=8344
tier=kid profile=survival: segment=False heading=False chars=4450
RESULT: PASS
```

Route names grepped, verbatim: `write`, `read`, `send`, `dispatch|workflow`,
`rotate|spawn`. Engine seams grepped, verbatim: `write.py`, `commands.py`,
`send.py`, `dispatch.py`, `workflow.py`, `rotate.py`.

## Probe log (three conjuncts)

1. **wire / full-profile tiers** — all four tiers carry all five names, all six
   seams, and `brief._ROUTES_SEGMENT` itself. **held.** Default resolution
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
