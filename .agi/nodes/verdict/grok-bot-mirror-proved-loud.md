---
id: verdict:grok-bot-mirror-proved-loud
mint_id: 968015e79ba443d28fdfbf6c1547bd7f
type: verdict
parents:
  - experiment:grok-bot-mirror-green-and-loud
next_edges: []
confidence: 0.9
edited_by: a00-8ee9bdff
evidence_runs:
  - experiment:grok-bot-mirror-green-and-loud
loop: goal:g17.14.3@s2
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

- **Green:** `8 passed in 0.03s` for
  `extensions/agi/tests/test_grok_bot_adapter.py` against the helper-branch
  adapter (`b35848f8`) + config (`52e9c262`) in a scratch tree.
- **Loud, not silent:** P-A (missing adapter) and P-B (adapter raising
  `ImportError`) both stop collection with an error — the removed
  `importorskip` would have turned P-B into `1 skipped`.
- **Not tautological:** P-C (`NAME` mutated) fails
  `test_name_is_the_harness_literal`; P-D (`restart` returning `0`) fails
  `test_adapter_implements_the_whole_interface`.
- **Config seam:** the real `.agi/config.json` `grok-bot` row resolves to
  `adapter=grok_bot`, models `{kid: grok-4-fast, parent: grok-4}`.

## Bounds

The `8 passed` was measured on **scratch copies of the sibling bytes**, not on
this branch: this branch owns only the test file, so it collection-errors at
`adapters.load("grok_bot")` until `goal:g17.14.1` / `goal:g17.14.2` merge up.
That is the intended loud behaviour, but it means the green conjunct cannot be
re-observed on this branch alone. `model_args` is not in `adapters.REQUIRED`;
the tier test binds to it, so a future adapter without that helper errors
rather than skips — an honest residual, not a defect of this round.
What evidence supports this verdict?

## Confidence

0.0 – 1.0
