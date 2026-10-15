---
id: experiment:a00-e69382b6-b40d5c
mint_id: 756d7ba1d95a4a14975d825baf92b6b1
type: experiment
parents:
  - hypothesis:restart-carries-the-first-spawns-full-turn-and-identity
next_edges: []
confidence: 0.85
edited_by: a00-d4e0b947
evidence_runs:
  - experiment:a00-e69382b6-b40d5c
loop: hypothesis:restart-carries-the-first-spawns-full-turn-and-identity@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "tip bytes: dispatch._reap_one_impl(graph, iter_dir, capturing_adapter, rec, agent_id, 999, cfg) with rec={spawn_role:director, ladder_tier:2, brief_tier:parent, cli_py, skill_prompt, dispatch_py}; then rec={role:research} (old record) and rec={spawn_role:\"\", ladder_tier:0}", "expected": "adapter.restart receives role/ladder_tier/brief_tier/cli_py/skill_prompt/dispatch_py from the record; ladder_tier 0 and empty spawn_role must not be lost to truthiness; an old record falls back to role and gets None/empty identity defaults", "observed": "all six kwargs arrived (role=director ladder_tier=2 brief_tier=parent cli_py=/x/cli.py skill_prompt=/x/agent-prompt.md dispatch_py=/x/dispatch.py); ladder_tier==0 preserved; old record role==research with cli_py==\"\" and skill_prompt/ladder_tier None", "result": "HOLD - the restart seam threads the spawn identity live"}
  - {"conjunct": 2, "class": "gate", "cmd": "tip bytes: write spawn.json as null, [], \"a bare string\", 123, true, then {brief:<brief render failed>}, then {argv:[]}, then {brief:REAL-BYTES}; call dispatch._carried_restart_brief(iter_dir, a00-x)", "expected": "every non-dict payload and the failed-render sentinel returns None (no AttributeError out of the restart); a dict with real brief returns the bytes", "observed": "None for null/[]/string/123/true/sentinel/no-brief-key; REAL-BYTES returned for the real brief", "result": "HOLD - non-dict falls back to None, never raises"}
  - {"conjunct": 3, "class": "wire", "cmd": "temp engine tree with pre-fix dispatch.py (git show e64e0a3278^:extensions/agi/bin/dispatch.py) + the kid test file; pytest -k non_dict/spawn_identity/records_role/pi_restart_accepts; plus bytes check of the pre-fix restart call region", "expected": "the new dispatch-side tests are RED on the pre-fix bytes; the pre-fix restart call carries none of cli_py=/skill_prompt=/role=/ladder_tier= (it does carry rendered_brief=)", "observed": "3 failed (non_dict, spawn_identity, records_role) on pre-fix dispatch.py; pre-fix region has rendered_brief= only of the five", "result": "HOLD - the red-on-pre-fix conjunct is real, not asserted"}
  - {"conjunct": 1, "class": "auth", "cmd": "read every restart signature at tip: claude_code_adapter:826, copilot_cli_adapter:334, grok_bot_adapter:105, pi_adapter:289; check dispatch passes role/ladder_tier/brief_tier/cli_py/skill_prompt/dispatch_py to adapter.restart on EVERY harness", "expected": "every adapter restart accepts the kwargs dispatch now passes, or the restart seam TypeErrors for that harness and reads restart unavailable", "observed": "claude/copilot/grok already carried role+ladder_tier+brief_tier+paths; pi lacked role/ladder_tier and the fix adds and forwards them; no adapter refuses the seam", "result": "HOLD - no harness is regressed by the wider restart call"}
production_lines: 38
profile: balanced
role: kid
scaffold_hash: 10da6d03d6108e37
season: 2
title: Restart carries the first spawn's cli_py skill_prompt role and tiers
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e69382b6-b40d5c

**Claim** (parent `hypothesis:restart-carries-the-first-spawns-full-turn-and-identity`):
A restart must carry the FIRST spawn's full turn and identity — the brief
render (already landed) **and** `skill_prompt`, `cli_py`, `role`, the
ladder/brief tiers — and a non-dict `spawn.json` must fall back to `None`
rather than raise.

## What was built

| Seam | Before | After |
|---|---|---|
| `agent_record` (dispatch.py:2833ff) | `role` (per-TARGET, may be null), no tiers/paths | + `spawn_role` (=`args.role`, the role `build_command` got), `ladder_tier`, `brief_tier`, `cli_py`, `skill_prompt`, `dispatch_py` |
| restart call (dispatch.py:3600ff) | `rendered_brief` only | + `cli_py`, `skill_prompt`, `dispatch_py`, `role` (`spawn_role` \|\| `role`), `ladder_tier`, `brief_tier` |
| `_carried_restart_brief` (:3342) | caught `OSError, ValueError` only; `null`/list/str raised `AttributeError` → `restart unavailable` | + `isinstance(rec, dict)` guard → `None` |
| `pi_adapter.restart` | no `role`/`ladder_tier` params (TypeError) | accepts and forwards them (accepted-and-unused; pi has no tool bundle) |

Why `spawn_role`: the record's `role` is the per-target role (research /
implementation, often null); the first spawn's `build_command` got `args.role`,
which selects the tool bundle. `spawn_role` is null on old records and the
restart falls back to `role`, so back-compat holds.

## Evidence

RED on the pre-fix bytes (measured before the fix, `env -u TMUX -u TMUX_PANE`):
```
4 failed, 13 passed
FAILED test_carried_restart_brief_tolerates_a_non_dict_spawn_json
FAILED test_reap_restart_threads_the_spawn_identity_to_the_adapter
FAILED test_reap_restart_falls_back_to_the_records_role
FAILED test_pi_restart_accepts_role_and_ladder_tier
E  TypeError: restart() got an unexpected keyword argument 'role'
```

GREEN on the built bytes:
```
test_dispatch_restart_render.py            17 passed
test_*adapter*.py (4 files)               123 passed
with test_real_adapter_restart.py
  + test_dispatch.py                      169 passed
```

Production lines (`git diff --numstat`, tests excluded): `30 dispatch.py +
8 pi_adapter.py = 38` — ceiling 40.

Adapter test doubles only; no real spawn, no model call.
<!-- BODY:END -->

## Agent Notes
Restart now carries the first spawn's full identity: agent_record stores spawn_role/ladder_tier/brief_tier/cli_py/skill_prompt/dispatch_py; _reap_one_impl passes them to adapter.restart; _carried_restart_brief falls back to None on a non-dict spawn.json; pi_adapter.restart accepts role/ladder_tier. 4 new tests RED pre-fix, GREEN post-fix (17/169/123 pass). 38 production lines, ceiling 40.

PARENT REVIEW EF.80 (a00-d4e0b947): ACCEPTED. Diff e64e0a3278 read byte-for-byte (dispatch.py +30, pi_adapter.py +8, tests +104). Every deliverable the kid named is in the diff: agent_record identity keys, _reap_one_impl restart kwargs, _carried_restart_brief isinstance guard, pi_adapter role/ladder_tier, 4 new tests. Parent probes HOLD (4 entries, classes wire/gate/wire/auth): the six kwargs thread live and ladder_tier 0 + old-record role fallback survive; null/[]/string/int/true/sentinel -> None; 3 dispatch-side tests RED on pre-fix dispatch.py and the pre-fix restart call carried rendered_brief only; all four restart signatures accept the widened kwargs, no harness regressed. Named tests green on tip: test_dispatch_restart_render.py + test_real_adapter_restart.py + test_dispatch.py = 169 passed. proved stands.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review version. The kid version carried verdict proved, the implementation and the tests. This version adds the parent `probes:` block (SL7.110: a tier-parent proved record without probes is refused) and appends the review note. (1) The order said: "prove the new committed test red on the pre-fix bytes (run it against the base), the named tests green on the tip" and "A kid that passes its own tests and fails your probe is lean_disproved, with the probe NAMED". (2) What I actually did: read the kid DIFF e64e0a3278, never its result file; re-checked each Measured line at the tip; ran my own probes in a temp tree (pre-fix dispatch.py via git show e64e0a3278^) rather than re-running the kid suite as evidence. (3) Near miss: accepting "4 failed pre-fix" because the kid wrote it in prose — the checkable version is running the new dispatch tests against the pre-fix bytes (3 failed: non_dict, spawn_identity, records_role) and confirming the pre-fix restart region carries rendered_brief= but none of cli_py=/skill_prompt=/role=/ladder_tier=. (4) No standing rule deviated from.
<!-- THOUGHT:END -->
