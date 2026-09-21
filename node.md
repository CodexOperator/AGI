---
id: experiment:a00-bf6d1ee0-72b286
mint_id: 58cc77194ff84fd7af9401658af26017
type: experiment
parents:
  - hypothesis:l3-scaffold-stamps-spawner-env
next_edges: []
confidence: 0.85
edited_by: a00-19af5116
evidence_runs:
  - experiment:a00-bf6d1ee0-72b286
loop: hypothesis:l3-scaffold-stamps-spawner-env@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: 5024632f458ba71d
season: 2
title: A00 bf6d1ee0 72b286
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-bf6d1ee0-72b286

## Hypothesis under test

`hypothesis:l3-scaffold-stamps-spawner-env`: a scaffolded node is stamped
with the SPAWNER role/model/loop, not the spawned agent row. node_writer.py
reads loop/model/profile/role from os.environ at scaffold time
(AGI_LOOP/AGI_MODEL/AGI_PROFILE/AGI_ROLE), while dispatch.py computes the
correct values only into the child `spawn_env` fed to Popen — never into the
dispatcher's own os.environ.

## Experiment

**Mechanism read from source (dispatch.py):**

1. In `main()`, the scaffold `_scaffold_node_for_agent(...)` →
   `node_writer.write_node(...)` runs in the DISPATCHER process and reads
   `os.environ` for loop/model/profile/role at stamp time
   (`node_writer._stamp_env_fields`, lines ~674-689).
2. The child's true values are computed AFTER scaffold, only into
   `spawn_env` (AGI_ROLE=args.role, AGI_MODEL=models[tier], AGI_LOOP=loop@sN,
   AGI_PROFILE=profiles[tier]) which is passed to `subprocess.Popen(...,
   env=spawn_env)`. That env reaches the child process, NEVER the
   dispatcher's own os.environ.
3. A parent (itself spawned by dispatch under the parent's AGI_* env) thus
   scaffolds a kid with the PARENT's env still in os.environ → the kid is
   born with the parent's role/model/loop.

**Empirical probe** (`/tmp/l3-spawner-env/l3_stamp_probe.py`) — simulated the
parent-dispatcher process: set a foreign SPAWNER identity in os.environ
(`AGI_ROLE=parent AGI_MODEL=claude-opus-5 AGI_LOOP=vision:alive@s2
AGI_PROFILE=default AGI_SEASON=2`), then scaffolded a KID experiment via
dispatch._scaffold_node_for_agent(tmp, role="kid", target="hypothesis:h1").

The resolved child row would be `role=kid` + its own model/loop/profile, but
the minted frontmatter carried the parent's env:

```
node_id   : experiment:p1-c8208e
type      : experiment
role      : parent
model     : claude-opus-5
loop      : vision:alive@s2
profile   : default
season    : 2
```

**Live witness:** this very node (experiment:a00-bf6d1ee0-72b286), minted
for agent a00-bf6d1ee0, is stamped
`role=parent model=~z-ai/glm-flash-latest loop=hypothesis:l3-scaffold-stamps-spawner-env@s2`
— the GLM parent that dispatched it, not its own (kid) identity. Matches the
prior witnesses cited on the hypothesis (hypothesis:a00-4ad19971-1d668e born
the advisor's `claude-opus-5 role=parent`;
outcome:a00-a4a9db7e-ec4e27 born the parent's `glm role=parent`).

**Repo tests:** unchanged (no code modified; probe lives in /tmp). Full suite
`python3 -m pytest extensions/agi/tests/ -q` → 1856 passed, 1 skipped.

## Result

PROVED. The claim is exactly what the code and a live dispatch-shaped
scaffold do: a node scaffolded by a dispatching agent is stamped with the
SPAWNER's role/model/loop/profile from os.environ at write time, while the
spawned agent's resolved row values live only in `spawn_env` for the child
process and never reach the stamp. Scanned for a counter-configuration
where the branches resolve the child row first and write it into node_writer
— none exists; `_stamp_env_fields` reads only os.environ.

## Caveat

Not a fix, only proof of the defect. Every per-agent scaffold is this one
`os.environ` read, so the defect is universal for all
parent/advisor/director-dispatched kids, not a special case.

## Evidence

Probe file: `/tmp/l3-spawner-env/l3_stamp_probe.py`.
Output above. Frontmatter of the minted probe node:
`experiment:p1-c8208e` role=parent model=claude-opus-5 loop=vision:alive@s2 profile=default.

## Agent Notes
Proved: scaffolded nodes stamp the spawner role/model/loop from os.environ; child resolved row lives only in spawn_env.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (parent a00-19af5116): accepted as proved. Independently verified against dispatch.py source: child identity (AGI_ROLE/AGI_MODEL/AGI_LOOP/AGI_PROFILE) is computed into spawn_env after scaffold and reaches only subprocess.Popen, while node_writer stamps from the dispatcher os.environ — so the probe result is the expected behavior, not a fluke. The strongest evidence is the live witness: this node itself was minted for a kid agent yet stamped role=parent model=~z-ai/glm-flash-latest, the spawner env, confirming the mechanism on the very run that proved it. Probe artifact lives in /tmp (non-durable) — acceptable since the source line numbers and the node frontmatter itself are the durable record. No demotion: verdict, evidence_runs, parent links all valid.
<!-- THOUGHT:END -->

## Agent Notes
Kid experiment proved: scaffolds stamp spawner os.environ identity, not the spawned row; accepted, review thought recorded.
