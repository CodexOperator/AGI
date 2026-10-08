---
id: experiment:a00-3feeca19-a022df
mint_id: 249bb21c6a264462b35ac4a1c73dfada
type: experiment
parents:
  - hypothesis:l3w0-ladder-roles-table
next_edges: []
confidence: 0.9
edited_by: ubuntu
evidence_runs:
  - experiment:a00-3feeca19-a022df
scaffold_hash: b742fc650369d3db
season: 1
title: A00 3feeca19 a022df
verdict: proved
---
# experiment:a00-3feeca19-a022df

## Experiment

Implemented the L3 command-ladder roles table end to end on
`hypothesis:l3w0-ladder-roles-table`.

**What changed (all red-first; new tests failed before the code landed):**

1. **Ladder node declares the roles table.** `.agi/nodes/.geometry/ladder.md`
   now carries `roles:` (7 rows), `season_names: {1: genesis}`, `mantles:
   {prime_director: Belam}` (the legacy `mantles_prime_director` kept as an
   alias). Rows match the owner's L3 focus: the top three levels fixed
   (prime/advisors fable+opus ultracode, director-kids fable max), the lower
   ladder GLM/DeepSeek under them; tier-2 rows dropped; tier-1 director at
   effort max, not xhigh. Schema `[ladder].md` extended with `roles` (now
   required), `season_names`, `mantles` + types.

2. **dispatch.py resolves (tier, role) -> harness/model/effort/settings.**
   New `resolve_role_spec(cfg, roles, tier, role)` — a declared row wins,
   config `harnesses.*.models[role]` is the fallback (pre-existing behaviour
   for missing rows). New `--role` (default kid), `--ladder-tier`, and
   `--list-rows` (dry print, nothing spawned). Launched harness may switch
   to the row's harness; model injected under `models[args.tier]`; effort and
   settings merged in.

3. **claude_code_adapter passes effort (as today) and settings.** New
   `settings` handling: `"ultracode"` -> `--settings '{"ultracode": true}'`;
   per-tier map or direct JSON supported; absent -> no flag.

4. **Env stamps.** dispatch exports `AGI_LOOP` (already present) and now
   `AGI_ROLE` (+ `AGI_LADDER_TIER`) for every spawn. node_writer stamps
   `role:` at mint from `AGI_ROLE`.

5. **Fixed a pre-existing bug** in `node_writer._stamp_env_fields`: it
   early-`return`ed after a successful `AGI_SEASON` parse, so in the real
   dispatch environment — where dispatch sets `AGI_SEASON` and `AGI_LOOP`
   together — the loop/model/profile (and now role) stamps never landed.
   Removed the early return; the `test_minted_node_stamps_loop_model_
   profile_from_env` test was failing under an AGI_SEASON=1 shell and now
   passes.

**Dry proof (VERIFY):** `python3 extensions/agi/bin/dispatch.py . L3.01
--list-rows` prints every declared row resolved — exact output below.

**Test run:** `python3 extensions/agi/bin/commands.py run tests` equivalent
— `python3 -m pytest extensions/agi/tests/ -q` → **1684 passed, 9 skipped**
(baseline 1661 passed / 9 skipped; +16 new assertions-bearing tests).

## Evidence

`--list-rows` (verbatim):

```
ladder roles table: 7 rows
tier=3 role=prime_director  harness=claude-code model=claude-fable-5-1             effort=max   settings=ultracode
tier=3 role=parent          harness=claude-code model=claude-opus-5                effort=max   settings=ultracode
tier=1 role=director        harness=claude-code model=claude-fable-5-1             effort=max   settings=-
tier=1 role=parent          harness=pi          model=~z-ai/glm-flash-latest       effort=-     settings=-
tier=0 role=director        harness=pi          model=~z-ai/glm-flash-latest       effort=-     settings=-
tier=0 role=parent          harness=pi          model=~z-ai/glm-flash-latest       effort=-     settings=-
tier=0 role=kid             harness=pi          model=~deepseek/deepseek-v4-flash-latest effort=-     settings=-
```

New tests (all green):
- `test_dispatch.py`: `test_ladder_row_wins_over_config`,
  `test_config_fallback_when_no_ladder_row`, `test_empty_cell_values_resolve_
  to_none`, `test_missing_roles_table_falls_back_to_config`,
  `test_compile_role_rows_covers_every_declared_row`,
  `test_default_tier_for_role`, `test_dispatch_exports_agi_role_env` (AST).
- `test_claude_code_adapter.py`: `test_no_settings_flag_when_absent`,
  `test_settings_ultracode_appends_settings_flag`,
  `test_settings_per_tier_map`, `test_effort_and_settings_combine`.
- `test_node_writer.py`: `test_minted_node_stamps_role_from_env`,
  `test_minted_node_omits_role_when_env_absent`; hardened
  `test_minted_node_omits_loop_when_env_absent` to control all AGI_* vars.
- `test_ladder_node.py`: `test_ladder_node_declares_roles_table`,
  `test_ladder_node_declares_season_names`, `test_ladder_node_declares_mantles`.

`links.py schema` shows no ladder-type violations after adding `roles` etc.

**Files touched:** `.agi/nodes/.geometry/ladder.md` (roles/season_names/
mantles + Roles table section), `.agi/context/schemas/[ladder].md`,
`extensions/agi/bin/dispatch.py`, `extensions/agi/bin/adapters/
claude_code_adapter.py`, `extensions/agi/bin/node_writer.py`,
`extensions/agi/bin/spawn_gate.py` (`read_ladder_roles`), and the four test
files.

## Agent Notes

Kid note (not a git instruction): engine files and the ladder node are all
edited in place; the loop owns commits. No `git` was run. The ladder node's
`roles` was written by direct file edit because `write.py set` cannot express
a list-of-dicts (`_coerce` split a `[...]` on commas before attempting JSON),
a tooling gap worth fixing another day.

## Agent Notes
L3 roles table: ladder declares roles(+season_names+mantles), dispatch resolves (tier,role)->harness/model/effort/settings with config fallback, --list-rows dry proof, adapter emits --settings ultracode + --effort, AGI_ROLE exported & node_writer stamps role; fixed AGI_SEASON early-return bug that skipped loop/model/profile stamps. Suite 1684 passed / 9 skipped.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-bb739a25, L3.01): artifact verified against the tree, not just the report — reran dispatch.py --list-rows and got the same 7 rows verbatim; AGI_ROLE export at dispatch.py:651 and role stamping in node_writer confirmed. Verdict proved is legitimate: claim (roles table + season_names + mantles declared, dispatch resolves with config fallback, --settings/--effort reach the adapter, AGI_LOOP/AGI_ROLE exported and stamped at mint) is all demonstrated with red-first tests and a green full suite (1684 passed). One deviation noted, not demoting: the hypothesis addendum said tier-2 rows would be declared but unused; the kid dropped them entirely, which satisfies the owner-fixed L3 shape and the claim as written, so it stands. Two caveats accepted as recorded: write.py cannot set a list-of-dicts (tooling gap, deferred), and the AGI_SEASON early-return bug fix in node_writer is a genuine pre-existing defect this experiment surfaced and closed.
<!-- THOUGHT:END -->

Review ACCEPTED by parent a00-bb739a25: parents resolve, verdict proved valid, evidence_runs is a real node id (self), --list-rows output reproduced by parent, suite green. No demotions.
