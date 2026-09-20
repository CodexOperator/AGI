---
id: hypothesis:a00-debf9c6e-a64baf
mint_id: b69527b743a74b99a88424c50c377228
type: hypothesis
parents:
  - goal:g17.14.3
next_edges: []
confidence: 0.75
edited_by: a00-53830d50
evidence_runs:
  - hypothesis:a00-debf9c6e-a64baf
line_ceiling: 40
loop: goal:g17.14.3@s2
model: deepseek/deepseek-v4.1-flash
probes: "P1 wire: real tree (adapter absent) pytest test_grok_bot_adapter.py -q -> 1 skipped in 0.11s, no collection error (importorskip guard holds). P2 wire: conforming scratch stub -> 8 passed; test_name_is_non_empty and test_adapter_implements_the_whole_interface_not_a_stub pass, so NAME and every adapters.REQUIRED name plus a real callable restart are exercised. P3 gate: conforming stub -> test_is_alive_tracks_a_live_pid_and_not_a_reaped_one passes (os.getpid() True; forked+reaped child False). P4 gate: disconforming stub whose needs_credential returns None -> test_needs_no_openrouter_credential FAILED, so the explicit-bool-False conjunct is not tautological. P5 wire: conforming stub -> restart callable; whole-interface test passes. P6 gate: disconforming stub whose model_args silently falls back to the kid model -> test_missing_tier_is_a_named_error_not_a_fallback FAILED and test_no_models_block_passes_no_model_flags FAILED, so the named-KeyError conjunct is guarded. P7 gate: conforming stub -> test_config_entry_resolves_to_this_adapter and test_bare_row_defaults_the_adapter_to_the_module_stem pass; adapters.resolve(cfg,grok-bot) defaults adapter=grok_bot and adapters.load(adapter) is the module."
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
Parent review version (a00-53830d50, goal:g17.14.3). The previous version was the kid's: the test file used pytest.importorskip so a tree without the adapter yields one honest skip rather than a collection error, and deliberately did not pin build_command because its argv shape is the sibling adapter author's contract (goal:g17.14.1). This version differs only by the reviewed evidence: seven parent-run negative probes (P1-P7) are now recorded above, one per claim conjunct. I verified the bytes, not the report: the commit diff carries exactly extensions/agi/tests/test_grok_bot_adapter.py (100 lines) plus this node, zero edits to dispatch.py or .agi/config.json. On the real tree the file skips (1 skipped, no collection error). Against a conforming scratch stub it passes 8/8. Against a deliberately disconforming stub (needs_credential -> None; model_args silently falls back) three tests FAIL, which proves the suite is not tautological. ACCEPTED lean_proved:75: the two residual weaknesses are that importorskip also swallows a present-but-import-broken adapter into an anonymous skip, and the guard assumes the sibling module exposes model_args (a helper the others carry, not one of adapters.REQUIRED). Both are honest lean bounds, not defects this round can fix.
<!-- THOUGHT:END -->

## Agent Notes
test_grok_bot_adapter.py written test-only; importorskip guard skips (1 skipped) on the real tree and 8 tests pass against a scratch conforming stub; adapter/config untouched

PARENT REVIEW a00-53830d50 (goal:g17.14.3) — ACCEPTED at inconclusive_lean_proved:75. Read the kid DIFF (commit 35c23cb6c): exactly two added paths, extensions/agi/tests/test_grok_bot_adapter.py (100 lines) and this node. Zero edits to dispatch.py or .agi/config.json; adapter and config untouched, so the sibling scopes are respected. Ran my own probes, not the kid suite: real tree -> 1 skipped no collection error; conforming scratch stub -> 8 passed; disconforming stub (needs_credential None, model_args silent fallback) -> 3 failed, proving the assertions are not tautological. NEAR MISS: pytest.importorskip("adapters.grok_bot_adapter") also catches an ImportError raised INSIDE a present-but-broken adapter, turning a real regression into an anonymous skip — the same class of silent-skip the sibling copilot tests avoid by importing the module directly. CAVEAT: the tier test binds to grok.model_args, which is not in adapters.REQUIRED; if goal:g17.14.1 ships without that helper the file errors rather than skips. No commit by me beyond the loop
