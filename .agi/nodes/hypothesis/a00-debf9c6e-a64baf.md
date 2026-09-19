---
id: hypothesis:a00-debf9c6e-a64baf
mint_id: b69527b743a74b99a88424c50c377228
type: hypothesis
parents:
  - goal:g17.14.3
next_edges: []
confidence: 0.75
edited_by: a00-debf9c6e
evidence_runs:
  - hypothesis:a00-debf9c6e-a64baf
line_ceiling: 40
loop: goal:g17.14.3@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 6c703b2fe83de13c
season: 2
testable_claim: "A test-only mirror of the adapter interface suite for the `grok-bot` harness can guard the `goal:g4.6` seam *before* the adapter exists, by making the guard an `importorskip` rather than a hard import: the file collects and skips on a tree without `bin/adapters/grok_bot_adapter.py`, and passes unchanged once `goal:g17.14.1` lands a conforming module."
title: Mirror adapter interface tests for grok-bot
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# hypothesis:a00-debf9c6e-a64baf

## Hypothesis

A test-only mirror of the adapter interface suite for the `grok-bot` harness
can guard the `goal:g4.6` seam *before* the adapter exists, by making the
guard an `importorskip` rather than a hard import: the file collects and
skips on a tree without `bin/adapters/grok_bot_adapter.py`, and passes
unchanged once `goal:g17.14.1` lands a conforming module.

**Deliverable:** `extensions/agi/tests/test_grok_bot_adapter.py` (test-only;
the adapter and the `.agi/config.json` row are owned by siblings `goal:g17.14.1`
and `goal:g17.14.2` and were NOT touched).

## What proves it

The file asserts the seven required surfaces, mirroring
`test_claude_code_adapter.py` / `test_copilot_cli_adapter.py`:

1. non-empty `NAME`;
2. every name in `adapters.REQUIRED` is callable (`build_command`,
   `child_env`, `is_alive`, `restart`, `needs_credential`) and `restart` is
   real, not a stub;
3. `is_alive(os.getpid())` is `True` and a reaped pid is `False`;
4. `needs_credential(grok-bot row)` is the EXPLICIT bool `False`;
5. `restart` callable (`goal:g4.7`);
6. a tier missing from a declared `models` block raises a `KeyError` naming
   the tier (`model_args`), never a fallback;
7. `adapters.resolve(cfg, "grok-bot")` defaults `adapter` to `grok_bot` and
   `adapters.load(harness["adapter"])` is the module.

## Evidence

- Against THIS tree (adapter absent): `1 skipped in 0.12s` — collection does
  not fail, the guard does its job.
- Against a scratch-only conforming stub adapter under the session dir
  (`probe/bin/adapters/grok_bot_adapter.py`, never in production):
  `8 passed in 0.03s` — every assertion is satisfiable by a conforming module
  and none is tautological. See `probe/` in this session dir.

## Disproof

A collection error on the real tree before `.1` lands, or any test that fails
against a module satisfying the `goal:g4.6` interface, would disprove it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Practice-run scope. Chose `pytest.importorskip` over a try/except at module
level so a missing adapter yields one honest skip, not a hard error, and the
file needs no edit on the day `.1` lands. Deliberately did NOT exercise
`build_command`: its argv shape is the adapter author's contract and not yet
written, so pinning a fixture session here would freeze a guess. `model_args`
carries the same no-fallback claim and is the shared spelling across all three
shipped adapters, so the tier test binds to that instead. Test-only, so
production_lines is 0.
<!-- THOUGHT:END -->

## Agent Notes
test_grok_bot_adapter.py written test-only; importorskip guard skips (1 skipped) on the real tree and 8 tests pass against a scratch conforming stub; adapter/config untouched
