---
id: experiment:a00-a18f229f-023f5c
mint_id: d6761fa2b68f45a08fe9ca61f5dbfc5a
type: experiment
parents:
  - hypothesis:l3w1-tier0-director-brief
next_edges: []
confidence: 0.8
edited_by: ubuntu
evidence_runs:
  - experiment:a00-a18f229f-023f5c
loop: hypothesis:l3w1-tier0-director-brief@s1
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 91ad89714cef2a1c
season: 1
title: A00 a18f229f 023f5c
verdict: inconclusive_lean_proved:85
---
# experiment:a00-a18f229f-023f5c

## Experiment

WAVE-1 verification of `hypothesis:l3w1-tier0-director-brief`: does `brief.py`
assemble a tier-0 GLM director brief carrying the constitution head (prayers,
Michael line, decision method) **and** a correct spawn primitive, and does
`dispatch.py --role director --ladder-tier 0` resolve through the pi harness to
`~z-ai/glm-flash-latest`?

**Bug found red-first.** The existing `_director` brief's spawn primitive was
`dispatch.py <project> {iter_n} --tier parent` (no `--role`/`--ladder-tier`).
`dispatch.py`'s `--role` defaults to `kid` (`_default_tier_for_role`), so a
director spawning a parent with that bare command resolved the **tier-0 kid**
row → `~deepseek/deepseek-v4-flash-latest` for the spawned parent's model,
not the tier-0 parent GLM row the hypothesis specifies. Demonstrated:

```
--tier parent w/ default role kid -> tier_eff 0 role kid model: ~deepseek/deepseek-v4-flash-latest
--role parent --ladder-tier 0       -> model: ~z-ai/glm-flash-latest
```

**Fix (brief.py):** named role and ladder tier in the director spawn primitive:

```
python3 dispatch.py <project> {iter_n} --tier parent \
  --role parent --ladder-tier 0 --detach --target <goal-id>
```

with a comment line stating why (a bare `--tier parent` resolves the kid row).

## Evidence

1. **Red-first test added** (`test_director_spawn_primitive_names_the_parent_role_and_ladder_tier`
   in `extensions/agi/tests/test_brief.py`): asserts the director brief carries
   `--role parent`, `--ladder-tier 0`, and the why (`deepseek` named).

2. **Directed brief assembly** — head + corrected spawn primitive all present:
   ```
   CONSTITUTION HEAD: True
   FOUR PRAYERS: True
   MICHAEL: True
   DECISION METHOD: True
   spawn: python3 dispatch.py <project> {iter_n} --tier parent \
   spawn: `--role parent --ladder-tier 0` is deliberate: ...
   ```

3. **Ladder roles dry print** (`dispatch.py ... --list-rows`) resolves the
   tier-0 GLM director row:
   ```
   tier=0 role=director  harness=pi  model=~z-ai/glm-flash-latest  effort=-  settings=-
   ```

4. **dispatch --role director --ladder-tier 0 → pi_glm command** (simulated
   through `pi_adapter.build_command`, the path `main()` takes):
   ```
   resolved pi command model flag: ~z-ai/glm-flash-latest
   harness resolves as: pi | from_ladder: True
   ```

5. **Full suite green after the fix** — `python3 -m pytest extensions/agi/tests/ -q`:
   ```
   1760 passed, 1 skipped in 94.91s
   ```

**Caveat:** per the wave plan (Agent Notes, "wave 3 is the live run") no billed
GLM director was actually spawned here; the "launches ... through the pi
harness" half rests on the resolved command + `--list-rows` dry proof, not a
live run. That half awaits wave 3.

## Agent Notes
brief.py director spawn primitive fixed red-first (--role parent --ladder-tier 0; bare --tier parent resolved the kid row -> deepseek). Brief carries head+prayers+Michael+decision method; dispatch --role director --ladder-tier 0 resolves pi/glm. Full suite 1760 passed. Live GLM director spawn deferred to wave 3.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewed; accepted inconclusive_lean_proved:85. Read the artifact (experiment node) not the report: the fix is real and in code — brief.py director spawn primitive gains --role parent --ladder-tier 0, so a director no longer silently spawns parents on the tier-0 kid/deepseek row. Red-first test test_director_spawn_primitive_names_the_parent_role_and_ladder_tier exists and passes; suite 1760 green. parents: resolves to hypothesis:l3w1-tier0-director-brief; evidence_runs is a valid list. Verdict honestly capped below proved: the live GLM director launch (wave 3) was not run, so the "launches through pi harness" half is dry-proved only. Traps: season.py/test_season.py changes are another parent's kid, not mine; write_guard clean.
<!-- THOUGHT:END -->
