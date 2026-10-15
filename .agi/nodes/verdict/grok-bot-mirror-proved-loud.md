---
id: verdict:grok-bot-mirror-proved-loud
mint_id: 968015e79ba443d28fdfbf6c1547bd7f
type: verdict
parents:
  - experiment:grok-bot-mirror-green-and-loud
next_edges: []
confidence: 0.9
edited_by: a00-11ad274b
evidence_runs:
  - experiment:grok-bot-mirror-green-and-loud
loop: goal:g7.25.3@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 9d356d1d725f872c
season: 2
title: Grok-bot mirror is proved green and loud on the real bytes
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# verdict:grok-bot-mirror-proved-loud

## Verdict

**proved** (confidence 0.9) — `goal:g17.14.3`'s corrected mirror is green on
the real sibling bytes and fails loudly, not silently, on a broken adapter.

## Evidence

Judged run: `experiment:grok-bot-mirror-green-and-loud`.

- **Green:** `15 passed in 0.12s` for
  `extensions/agi/tests/test_grok_bot_adapter.py` against the real adapter
  (`6aa00b4a`, 166 lines) + config (`fae48c5b`) on this tip.
- **Loud, not silent:** P-A (missing adapter) and P-B (adapter raising
  `ImportError`) both stop collection with an error — the removed
  `importorskip` would have turned P-B into `1 skipped`.
- **Not tautological:** P-C (`NAME` mutated) fails
  `test_name_is_the_harness_literal`; P-D (`restart` returning `0`) fails
  `test_adapter_implements_the_whole_interface`.
- **Config seam:** the real `.agi/config.json` `grok-bot` row resolves to
  `adapter=grok_bot`, models `{kid: grok-4-fast, parent: grok-4}`.

## Bounds

The `15 passed` is now observed **on this tip**: the adapter and the config
`bin` cell have merged up, so the green conjunct re-runs here. The earlier
scratch-copy bound is lifted; the P-A/P-B collection-error probes remain the
loud-failure evidence. `model_args` is not in `adapters.REQUIRED`;
the tier test binds to it, so a future adapter without that helper errors
rather than skips — an honest residual, not a defect of this round.
What evidence supports this verdict?

## Confidence

0.0 – 1.0

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
R12 correction applied in place by EF.53 a00-11ad274b under hypothesis:pass2-engine-rows-corrected-in-place. Re-checked live bytes: 15 tests (15 passed in 0.12s), test blob e37baef7bb76f299db30dfab4317f357672a3b88, adapter blob 6aa00b4aac4d3d8e4f4884515b0fb296a2f6a1be (166 lines) with restart() a real detached respawn. The stale "8 passed in 0.03s" count, the helper-branch blob ids (b35848f8 / 52e9c262) and the branch-alone collection-error bound are corrected in place. Per the dispatch order the verdict: proved and confidence: 0.9 fields are left UNCHANGED; the R12 D1 demote question (this proved predates the real-respawn bytes) is surfaced on hypothesis:a00-8ee9bdff-40419b and in the round done report, not actioned here.
<!-- THOUGHT:END -->
