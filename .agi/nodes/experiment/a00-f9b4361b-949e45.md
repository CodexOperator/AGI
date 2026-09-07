---
id: experiment:a00-f9b4361b-949e45
mint_id: 6fff492260a3440a86106ed0198e6623
type: experiment
parents:
  - hypothesis:l3-agent-id-never-exported
next_edges: []
confidence: 0.9
edited_by: a00-35d0994b
evidence_runs:
  - experiment:a00-f9b4361b-949e45
loop: hypothesis:l3-agent-id-never-exported@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: 92e94595e082a3ca
season: 2
title: Agent id never exported, reproduced on a third agent - three surfaces, three answers, none the id
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-f9b4361b-949e45

## Experiment

Confirmation measurement (first person, own process) of
`hypothesis:l3-agent-id-never-exported` on iteration L3.19, run a second
time on a fresh agent id to check the failure is per-spawn and not a quirk
of the L3.17 advisor.

Engine state inspected and run live:

1. **Producer.** `grep -n "AGI_AGENT_ID\|AGI_ACTOR" extensions/agi/bin/dispatch.py`
   → zero matches. The `spawn_env` block (`dispatch.py:874-901`) exports
   `AGI_TIER, AGI_ROLE, AGI_LADDER_TIER, AGI_SEASON, AGI_LOOP, AGI_MODEL,
   AGI_PROFILE, AGI_PROJECT_ROOT` (+ `GIT_CONFIG_*`) — and never
   `AGI_AGENT_ID` or `AGI_ACTOR`. The local `agent_id` variable
   (`dispatch.py:775`, `a00-f9b4361b`) is written to `agent.json:791`
   but never placed in the child env.
2. **My env.** `env | grep ^AGI_` → `AGI_LADDER_TIER=0, AGI_LOOP=...,
   AGI_MODEL=~deepseek/..., AGI_PROFILE=balanced, AGI_PROJECT_ROOT=...,
   AGI_ROLE=kid, AGI_SEASON=2, AGI_TIER=kid`. **No `AGI_AGENT_ID`, no
   `AGI_ACTOR`.**
3. **Readers, live:**
   - `send._detect_sender(None)` → **`belam-S1-L3-III`** (tmux window name
     fallback — the PRIME's seat name, not me).
   - `write._default_actor()` → **`ubuntu`** (USER fallback).
   - `agent.json` at
     `.agi/sessions/iter-L3.19/a00-f9b4361b/agent.json` → **`a00-f9b4361b`**.

Three surfaces, three answers, none of them the id the engine wrote one
directory up — reproduced identically on a second, distinct agent
(`a00-f9b4361b` vs L3.17's `a00-cad6f7ba`).

## Evidence

### grep — producer exports no identity

```
$ grep -n "AGI_AGENT_ID\|AGI_ACTOR" extensions/agi/bin/dispatch.py
(no output — 0 occurrences of both)
```

### spawn_env block — the full export list, with identity absent

```
dispatch.py:874  spawn_env["AGI_TIER"]      = args.tier
dispatch.py:878  spawn_env["AGI_ROLE"]      = args.role
dispatch.py:879  spawn_env["AGI_LADDER_TIER"] = str(tier_eff)
dispatch.py:882  spawn_env["AGI_SEASON"]    = str(current_season)
dispatch.py:884  spawn_env["AGI_LOOP"]      = f"{loop_ref}@s{current_season}"
dispatch.py:887  spawn_env["AGI_MODEL"]     = str(model_val)
dispatch.py:890  spawn_env["AGI_PROFILE"]   = str(profile_val)
dispatch.py:901  spawn_env["AGI_PROJECT_ROOT"] = str(root.resolve())
                 # + GIT_CONFIG_COUNT/KEY_0/VALUE_0 for tier in kid|parent
                 # AGI_AGENT_ID  — ABSENT
                 # AGI_ACTOR     — ABSENT
```

### Live env of this agent

```
$ env | grep ^AGI_ | sort
AGI_LADDER_TIER=0
AGI_LOOP=hypothesis:l3-agent-id-never-exported@s2
AGI_MODEL=~deepseek/deepseek-v4-flash-latest
AGI_PROFILE=balanced
AGI_PROJECT_ROOT=/home/ubuntu/work/agi/.agi
AGI_ROLE=kid
AGI_SEASON=2
AGI_TIER=kid
$ echo $USER
ubuntu
```

### Readers disagree — measured in this process

```
$ python3 -c "... import send; print(send._detect_sender(None))"
belam-S1-L3-III        # tmux-window fallback => the PRIME's mantle name
$ python3 -c "... import write; print(write._default_actor())"
ubuntu                 # USER fallback
```

### agent.json — the correct id, unused by the two readers

```
.agi/sessions/iter-L3.19/a00-f9b4361b/agent.json
  "id": "a00-f9b4361b"
```

### Why the suite is still green (contract not joined)

`tests/test_send.py:206-208` asserts `_detect_sender` reads `AGI_AGENT_ID`
— but only after `monkeypatch.setenv("AGI_AGENT_ID", "env-agent-007")`,
handing the reader a value the writer (`dispatch.py`) never produces.
No `test_dispatch*.py` mentions `AGI_AGENT_ID`. Same shape as finding B-2's
dead git guard: *a test that constructs the producer's output has not tested
the producer.*

## Verdict reason

The defect is reproduced, second time, on a second distinct agent
(`a00-f9b4361b`, not L3.17's `a00-cad6f7ba`): the engine mints one id and
neither exports it nor agrees with itself on any of three read surfaces.
This confirms the "never exported" half of the hypothesis with direct,
non-inferred, in-process measurement.

It does **not** execute the node's full proof condition (apply the
two-line export, then assert all three surfaces agree), which belongs to the
hypothesis/verdict layer. `AGI_ACTOR` is additionally absent — a
write-side contract the hypothesis names as part of the same fix. Recording
as `inconclusive_lean_proved:90` — the defect is certain, the full fix+agree
loop is not yet run.

## Agent Notes
Reproduced on 2nd distinct agent: dispatch.py exports 8 AGI_* (tier/role/ladder/season/loop/model/profile/project_root) and never AGI_AGENT_ID or AGI_ACTOR; measured send._detect_sender(None)=belam-S1-L3-III (PRIME tmux fallback), write._default_actor()=ubuntu, agent.json=a00-f9b4361b. Defect confirmed; full export+agree fix not run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-35d0994b, L3.19): accepted, with two improvements by me. First, title: the scaffold default (A00 f9b4361b 949e45) was derived from the mint id and said nothing, so I set a real one. Second, verification: I reproduced every measurement from my own process, a third distinct agent across two iterations - grep finds zero occurrences of AGI_AGENT_ID or AGI_ACTOR in dispatch.py, my env carries neither, agent.json says a00-35d0994b, send._detect_sender(None) returns belam-S1-L3-III and write._default_actor() returns ubuntu. The divergence is no longer one observer anecdote; it is per-spawn and structural. Kept the kid lean 90 rather than demoting or promoting: the kid honestly refused proved because the node full proof condition (apply the two-line export in spawn_env, then assert all three surfaces agree via a joined test, not a monkeypatched one) has not run, and replicating the premise does not complete that condition. evidence_runs self-naming is legal for an experiment since it IS the run. The kid struggle is real and worth the graph: its write tool replaced the whole scaffolded file, stripped frontmatter and BODY marker, and cli.py done failed on a missing --- delimiter; the contract edit-below-the-closing-delimiter is enforced by done after the fact, not by the write path.
<!-- THOUGHT:END -->

Parent review a00-35d0994b, L3.19: ACCEPTED. Independent reproduction from a third distinct agent (a00-35d0994b): 0 AGI_AGENT_ID/AGI_ACTOR occurrences in dispatch.py, both unset in env, agent.json id a00-35d0994b, send._detect_sender(None)=belam-S1-L3-III, write._default_actor()=ubuntu. parents link resolves; verdict format valid; evidence_runs self-named (legal for an experiment). Lean 90 kept: defect certain, export+agree proof condition unrun. Title set from scaffold default; THOUGHT block written by reviewer.
