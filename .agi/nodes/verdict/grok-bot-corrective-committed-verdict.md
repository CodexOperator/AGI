---
id: verdict:grok-bot-corrective-committed-verdict
mint_id: ae9992771a1f4057bc68c8ee7fd0cc8f
type: verdict
parents:
  - experiment:grok-bot-adapter-corrective-committed
next_edges: []
confidence: 0.9
edited_by: a00-6c2bf233
evidence_runs:
  - experiment:grok-bot-adapter-corrective-committed
line_ceiling: 40
loop: goal:g17.14.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 162
profile: balanced
rebrief_request: "162/40: byte-fold re-adds committed DT.17 adapter bytes verbatim; the config row is goal:g17.14.2 and out of scope"
role: kid
scaffold_hash: bd2ccf3c15c9d760
season: 2
title: Grok-bot corrective verified except the unlanded config row
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# verdict:grok-bot-corrective-committed-verdict

## Verdict

inconclusive_lean_proved:90

## Evidence

The corrective re-lands on this tip byte-honest, and
`experiment:grok-bot-adapter-corrective-committed` records the checks: adapter
sha256 `66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c` equal
to the `a824caf71` blob; the superset test file present whole (246 lines); the
in-tree probe unmocked with `new_pid 2784092`, `is_alive True`, `group_gone
True`, `teardown_ok True`; `test_adapters.py` 35 passed;
`test_grok_bot_adapter.py` 13 passed / 2 failed; `dispatch.py` zero `grok`
hits; `links.py schema` hypothesis row 126 → 124 and `links.py links` broken 0.

### The one named residue (deliberately NOT cleared)

The `harnesses.grok-bot` row in `.agi/config.json` is `goal:g17.14.2`'s
deliverable, and `cli.py:2093` (`_round_scope_ok`) forbids this round's
round-done commit from adding `.agi/config.json`. With the row absent from a
fresh checkout, `test_live_config_grok_row_resolves` and
`test_live_bin_cell_threads_through_to_argv` fail until the row is folded from
the live-config line (`ca330ac35` / `ca3b2da28`). The superset test file means
that fold loses no peer test. This unlanded dependency is why the verdict is a
strong lean, not `proved`.

### Production lines: 162, committed only

The DT.17 tip's `production_lines: 174` counted 12 UNCOMMITTED `.agi/config.json`
lines. This tip does not touch that file (`git diff --numstat HEAD --
.agi/config.json` is empty). The committed-only production measure is 162 — the
adapter alone; the probe and test live under `extensions/agi/tests/` and are
excluded.

## Confidence

0.9 — everything except the config row is byte-verified on this tip; the row
is a real unlanded dependency, so the honest statement is a strong lean, not a
proof.

## Agent Notes
DT.20 re-land of the DT.17 grok-bot corrective: adapter folded byte-identical to a824caf71 (sha256 66b7891f…), probe teardown now killpg+waitpid with group_gone True, committed-only production_lines 162 (not 174), schema hypothesis row 126→124, links broken 0; the harnesses.grok-bot config row stays unlanded for goal:g17.14.2.
