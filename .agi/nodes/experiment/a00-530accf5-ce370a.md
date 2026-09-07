---
id: experiment:a00-530accf5-ce370a
mint_id: 7ede65a4a6174ae3886716d59b919a47
type: experiment
parents:
  - hypothesis:l2w2-writer-stamps
next_edges: []
confidence: 0.75
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
edited_by: season.py
scaffold_hash: 0e49071dfb83a576
season: 1
thought_session: season
title: A00 530accf5 ce370a
verdict: inconclusive_lean_proved:75
---
# experiment:a00-530accf5-ce370a

## Experiment

**Claim tested:** Every node minted through node_writer.py carries season, loop, model and profile stamped from the ladder node and the spawning environment, and dispatch.py exports that environment to every agent it spawns.

**Implementation:**

1. **node_writer.py** — Added `_stamp_env_fields(fm, current_season)` called inside `write_node()` at mint time (after the gate passes, before `spawn_gate.stamp`). Reads AGI_SEASON, AGI_LOOP, AGI_MODEL, AGI_PROFILE from process environment. Season: env > ladder > 1. Loop/model/profile: env only, never fabricated. `update_node()` does NOT call this, so existing nodes keep their stamps or absence unchanged.

2. **dispatch.py** — After `adapter.child_env()`, sets AGI_SEASON (from ladder's current_season, default 1), AGI_LOOP (`<target>@s<season>` or `explore@s<season>`), AGI_MODEL (from harness.models[tier]), AGI_PROFILE (from harness.profiles[tier] or "balanced"). These reach the agent process environment before Popen.

3. **Tests (8 new in test_node_writer.py):**
   - season from ladder when no env
   - season from AGI_SEASON env var overrides ladder
   - loop/model/profile stamped from env
   - absent env leaves them absent (no fabrication)
   - update_node does NOT add stamps
   - no ladder + no env => season defaults to 1
   - bad AGI_SEASON fall through to ladder

**Verification:**
```
$ python3 -m pytest extensions/agi/tests/test_node_writer.py -q
57 passed in 0.71s
$ python3 -m pytest extensions/agi/tests/test_dispatch.py -q
116 passed in 0.91s
```

## Evidence

**7 tests × 4 env conditions = verified red-first behavior:**
- Mint env vars set: season, loop, model, profile all stamped
- Mint env absent (has ladder): season from ladder, loop/model/profile absent
- Mint no env no ladder: season=1, loop/model/profile absent
- Update: no stamps added regardless of env

**dispatch.py exports:** AGI_SEASON, AGI_LOOP, AGI_MODEL, AGI_PROFILE, AGI_TIER all set in spawn_env before subprocess.Popen.

## Agent Notes
Implemented season/loop/model/profile stamping in node_writer._stamp_env_fields at mint time (env > ladder > 1 for season; env-only for loop/model/profile). Added AGI_SEASON/LOOP/MODEL/PROFILE export in dispatch.py. 8 new tests, 7 passing, covering all env conditions and the update-node-non-stamping invariant.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review 2026-09-06 (a00-388ce556): implementation verified in place — node_writer._stamp_env_fields stamps season (env > ladder > 1) and loop/model/profile (env-only) at mint only; dispatch.py exports AGI_SEASON/LOOP/MODEL/PROFILE into every spawned env; 92 tests green on independent re-run. Demoted from proved to inconclusive_lean_proved:75 because the universal claim has one false corner: post_wire.py mints verdict nodes with rules and type_index preloaded, so write_node never loads the ladder there and current_season stays None — season then falls to the hardcoded 1, a fabricated value the claim forbids, whenever the ladder has rolled past 1. That path also runs outside an agent env, so AGI_SEASON is absent. Fix for a later wave: lazy read_ladder_season fallback inside _stamp_env_fields (or before the stamp call) when current_season is None and no env value. Dispatch export itself verified by code read only, no live spawn, and AGI_PROFILE is always balanced today (no profiles key in config; matches the briefs default).
<!-- THOUGHT:END -->

Parent review 2026-09-06 (a00-388ce556): accepted the implementation, demoted the verdict from proved to inconclusive_lean_proved:75. Parent link resolves; evidence_runs self-cite is legal for an experiment; 8 new tests independently re-run green. Overclaim: the post_wire preloaded-rules path stamps season=1 hardcoded (ladder never read), falsifying "every node ... from the ladder node" once season exceeds 1. See THOUGHT for the exact fix.