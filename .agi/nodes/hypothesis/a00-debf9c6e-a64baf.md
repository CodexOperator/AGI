---
id: hypothesis:a00-debf9c6e-a64baf
mint_id: b69527b743a74b99a88424c50c377228
type: hypothesis
parents:
  - goal:g17.14.3
next_edges: []
confidence: 0.75
edited_by: a00-8ee9bdff
evidence_runs:
  - experiment:grok-bot-mirror-green-and-loud
line_ceiling: 40
loop: goal:g17.14.3@s2
model: deepseek/deepseek-v4.1-flash
probes: "P-green wire: helper-branch adapter+config bytes in scratch, pytest test_grok_bot_adapter.py -q -> 8 passed in 0.03s. P-A gate: adapter file removed -> adapters.AdapterError at collection (no adapter for harness grok_bot), NOT skipped. P-B gate: adapter module replaced by `raise ImportError` -> ImportError at collection, NOT skipped. P-C gate: NAME mutated to grok -> test_name_is_the_harness_literal FAILS (assert grok == grok-bot). P-D gate: restart replaced by `return 0` -> test_adapter_implements_the_whole_interface FAILS (DID NOT RAISE NotImplementedError). P-config wire: real .agi/config.json row grok-bot -> adapters.resolve -> adapter=grok_bot, models kid grok-4-fast / parent grok-4, adapters.load is the module, needs_credential False."
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 6c703b2fe83de13c
season: 2
testable_claim: "A test-only mirror of the adapter interface suite for the `grok-bot` harness guards the `goal:g4.6` seam by HARD-loading `adapters.load(\"grok_bot\")` with no importorskip: against the real `goal:g17.14.1` adapter and the real `goal:g17.14.2` config row it is green (8 passed); a missing OR present-but-import-broken adapter is a COLLECTION ERROR rather than a silent skip; `NAME` is pinned to the harness literal `grok-bot`; and `restart` is asserted to be the locked stub raising NotImplementedError naming the unmeasured flags."
title: Grok-bot mirror hard-loads the adapter (importorskip removed)
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-debf9c6e-a64baf

## Hypothesis

A test-only mirror of the adapter interface suite for the `grok-bot` harness
guards the `goal:g4.6` seam by **hard-loading the module** — no
`importorskip`. Against the real `goal:g17.14.1` adapter the file is green
(8 passed); a **missing OR present-but-import-broken** adapter is a
collection error, never a silent skip; `NAME` is pinned to the harness
literal `grok-bot`; and `restart` is asserted to be the locked stub raising
`NotImplementedError` naming the unmeasured flags.

**Deliverable:** `extensions/agi/tests/test_grok_bot_adapter.py` (test-only;
the adapter and the `.agi/config.json` row are owned by siblings `goal:g17.14.1`
and `goal:g17.14.2` and were NOT touched).

## What proves it

The file asserts the eight surfaces, mirroring
`test_claude_code_adapter.py` / `test_copilot_cli_adapter.py`:

1. `NAME == "grok-bot"` — the harness literal seats and config use, not a
   non-empty guess;
2. every name in `adapters.REQUIRED` is callable (`build_command`,
   `child_env`, `is_alive`, `restart`, `needs_credential`), and `restart` is
   the LOCKED practice stub: it raises `NotImplementedError` whose message
   names the unmeasured flags (`unmeasured` / `flag` / `build_command`);
3. `is_alive(os.getpid())` is `True` and a reaped pid is `False`;
4. `needs_credential(grok-bot row)` is the EXPLICIT bool `False`;
5. a tier missing from a declared `models` block raises a `KeyError` naming
   the tier (`model_args`), never a fallback;
6. no `models` block passes no `--model` flag;
7. `adapters.resolve(cfg, "grok-bot")` returns the row and
   `adapters.load(harness["adapter"])` is the module;
8. a bare `grok-bot` row defaults `adapter` to the module stem `grok_bot`.

## Evidence

The load is a hard `adapters.load("grok_bot")` at module scope, so the
negatives below are COLLECTION errors, not skips. Against the real adapter and
config bytes on the helper branch `season2/loops/goal-g17.14.2-helper-cfg-land`
(`grok_bot_adapter.py` blob `b35848f8`, test blob `85c5cb43`): `8 passed`.

Four negative probes on that scratch tree:

- **P-A missing adapter** → `adapters.AdapterError` at collection
  (`no adapter for harness 'grok_bot'`), NOT a skip.
- **P-B adapter raises `ImportError`** → `ImportError` at collection, NOT a
  skip — the exact silent-skip `importorskip` used to swallow.
- **P-C `NAME` mutated to `grok`** → `test_name_is_the_harness_literal`
  FAILS (`assert 'grok' == 'grok-bot'`).
- **P-D `restart` returns `0` instead of raising** →
  `test_adapter_implements_the_whole_interface` FAILS (`DID NOT RAISE
  NotImplementedError`).

## Disproof

A green run against a tree without `bin/adapters/grok_bot_adapter.py`, or a
`1 skipped` result where a collection error is expected, would disprove it.

## Agent Notes

Re-versioned in place (DT.07, agent a00-8ee9bdff) clearing residue (d): the
previous body described the REMOVED `importorskip` guard and named two test
functions the corrected file no longer carries. The corrected claim now
matches the committed bytes: hard-load (no importorskip), NAME pinned
`== "grok-bot"`, restart asserted as the locked NotImplementedError stub.
Probes P-A..P-D re-run in this session's scratch dir; the green 8-passed run
was confirmed on the real adapter + config bytes. Adapter and config not
authored or edited here — they remain siblings' deliverable.
authored or edited here — they remain siblings' deliverable.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DT.07 corrective (a00-8ee9bdff), residue (d). The previous version described the guard as pytest.importorskip and named two test functions the corrected file no longer carries, so it contradicted the committed bytes. This version differs in the load contract: the module is HARD-loaded at collection, which converts both a missing adapter and a present-but-import-broken adapter into a collection error instead of the anonymous skip importorskip produced; NAME is pinned to the harness literal; and restart is asserted to be the locked NotImplementedError stub rather than merely callable. Re-probed P-A..P-D plus the real config row in this session scratch dir.
<!-- THOUGHT:END -->
