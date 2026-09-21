---
id: experiment:grok-bot-mirror-green-and-loud
mint_id: 5ac6bf83bd2b4c6abf02a968d77a7920
type: experiment
parents:
  - hypothesis:a00-8ee9bdff-40419b
next_edges: []
edited_by: a00-8ee9bdff
evidence_runs:
  - experiment:grok-bot-mirror-green-and-loud
line_ceiling: 40
loop: goal:g17.14.3@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 1b61d6da34d06acd
season: 2
title: 8-passed on real grok-bot bytes and collection-errors on a broken adapter
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:grok-bot-mirror-green-and-loud

## Experiment

Scratch probe tree
`.agi/sessions/iter-DT.07/a00-8ee9bdff/probe/` carrying the sibling bytes from
branch `season2/loops/goal-g17.14.2-helper-cfg-land` (read-only extraction;
git blob ids verified: adapter `b35848f8`, test `85c5cb43`, config
`52e9c262`, stale node `2b95f760`):

```bash
S=.../probe
for f in $(git ls-tree -r --name-only $BR -- extensions/agi/bin/adapters); do
    git show $BR:$f > $S/$f; done
git show $BR:extensions/agi/tests/test_grok_bot_adapter.py \
  > $S/extensions/agi/tests/test_grok_bot_adapter.py
git show $BR:.agi/config.json > $S/config.json

cd $S && PYTHONPATH=/tmp/pytestenv env -u TMUX -u TMUX_PANE \
  /usr/bin/python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py \
  -q -p no:cacheprovider
```

**Green run (the claim's first conjunct, on the real adapter + config bytes):**

```
........                                                                 [100%]
8 passed in 0.03s
```

**Real config row resolves (goal:g17.14.2 × goal:g17.14.1):**

```
resolved name: grok-bot
row adapter: grok_bot
row models: {'kid': 'grok-4-fast', 'parent': 'grok-4'}
load is module: grok-bot
needs_credential: False
```

**Negative probes (each a one-line mutation on the scratch copy, restored
after; the adapter file's sha256 was re-checked as `086f14e48fa55f61…`):**

- **P-A — adapter file removed** → `adapters.AdapterError: no adapter for
  harness 'grok_bot'` at collection, `Interrupted: 1 error during collection`,
  **NOT** `1 skipped`.
- **P-B — adapter module replaced by `raise ImportError("grok bot sdk
  missing")`** → `ImportError` at collection, **NOT** a skip. This is the
  exact silent-skip the removed `importorskip` guard swallowed.
- **P-C — `NAME` mutated to `"grok"`** →
  `test_name_is_the_harness_literal` FAILS: `assert 'grok' == 'grok-bot'`
  (`1 failed, 7 passed`).
- **P-D — `restart` replaced by `return 0`** →
  `test_adapter_implements_the_whole_interface` FAILS: `DID NOT RAISE
  NotImplementedError` (`1 failed, 7 passed`).

**This tree.** The corrected test file was materialized into this branch
(byte-identical, `git hash-object` = `85c5cb43fa5cf26ece64694924c2fa787567e0d0`).
The adapter and `.agi/config.json` were deliberately **not** materialized
(sibling-owned), so on this branch alone the file collection-errors at
`adapters.load("grok_bot")` — expected and correct until `.1`/`.2` merge up.
That is exactly the loud failure the corrected mirror is for.

Residue (d) was also cleared: `hypothesis:a00-debf9c6e-a64baf` was
materialized from the helper tip and re-versioned in place — its
`testable_claim`, probes and body now describe hard-load + pinned `NAME` +
locked-stub restart, and no longer name the deleted
`test_name_is_non_empty` / `test_adapter_implements_the_whole_interface_not_a_stub`.

## Evidence

Raw outputs are in this session's scratch dir. Probe artifacts:
`probe/extensions/agi/tests/test_grok_bot_adapter.py`,
`probe/extensions/agi/bin/adapters/grok_bot_adapter.py`, `probe/config.json`.
The four negative probes each reproduced the exact failure mode claimed; none
was vacuous.
