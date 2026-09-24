---
id: experiment:a00-0b1ff16a-tmux-env
mint_id: 0b1ff16a97787401
type: experiment
parents:
  - hypothesis:a00-0b1ff16a-977874
next_edges: []
loop: goal:g7.31.1.2.1@s2
role: kid
model: stealth/space-bunny-alpha
profile: balanced
title: "tmux hold carries alternating -e environment entries; grok child env is sanitized"
town: core
---
# experiment:a00-0b1ff16a-tmux-env

## Claim under test

The held-pane seam must not silently lose its environment: `tmux_hold._cmd`
must emit one `-e` flag per entry, while `grok_bot_adapter.child_env` must
remove the runtime credential for `needs_credential=False` and preserve a
harness sentinel.

## What changed

`extensions/agi/bin/adapters/tmux_hold.py` was corrected from an invalid list
comprehension (module could not import) and now builds alternating
`["-e", "KEY=VALUE", ...]` arguments. Focused tests were added to
`extensions/agi/tests/test_grok_bot_adapter.py`; they spy on `subprocess.run`
through `tmux_hold.start` and assert both the exact argv and the Grok env policy.

## Measurements

- Initial focused run failed at collection: the pre-existing `_cmd` comprehension
  was a SyntaxError, so the held seam was unusable.
- The first corrected shape exposed a second real defect: it emitted
  `["-e", "A=1", "B=2"]` rather than `["-e", "A=1", "-e", "B=2"]`; the new
  test caught this.
- Final focused run: `17 passed` for
  `python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q`.
- Test proves `OPENROUTER_API_KEY` is absent from `grok.child_env` and
  `GROK_SENTINEL=kept` survives; test proves the exact alternating `-e` argv
  reaches `new-session` for the named pane.

## Scope limit

This checkout contains the `tmux_hold` seam but no `HOLD_PANE` held-restart
caller in `dispatch.py`; therefore this experiment certifies the seam and the
adapter env contract, not an end-to-end held restart integration. The missing
caller is the next ancestor seam, not a reason to invent a new API here.
