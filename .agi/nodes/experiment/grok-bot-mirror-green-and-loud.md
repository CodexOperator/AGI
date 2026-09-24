---
id: experiment:grok-bot-mirror-green-and-loud
mint_id: 5ac6bf83bd2b4c6abf02a968d77a7920
type: experiment
parents:
  - hypothesis:a00-8ee9bdff-40419b
next_edges: []
edited_by: a00-11ad274b
evidence_runs:
  - experiment:grok-bot-mirror-green-and-loud
line_ceiling: 40
loop: goal:g7.25.3@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 1b61d6da34d06acd
season: 2
title: 15-passed on the real grok-bot bytes and collection-errors on a broken adapter
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:grok-bot-mirror-green-and-loud

## Experiment

Scratch probe tree
`.agi/sessions/iter-DT.07/a00-8ee9bdff/probe/` carrying the sibling bytes from
branch `season2/loops/goal-g17.14.2-helper-cfg-land` (read-only extraction;
git blob ids verified at extraction time: adapter `b35848f8`, test `85c5cb43`, config
`52e9c262`, stale node `2b95f760` -- the CURRENT committed bytes are adapter
`6aa00b4a`, test `e37baef7`, config `fae48c5b`:

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
...............                                                          [100%]
15 passed in 0.12s
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
  (`1 failed, 14 passed`).
- **P-D — `restart` replaced by `return 0`** →
  `test_adapter_implements_the_whole_interface` FAILS: `DID NOT RAISE
  TypeError` (`1 failed, 14 passed`).

**This tree.** The adapter and the `.agi/config.json` `bin` cell have since
landed on this tip, so the file no longer collection-errors: it runs green
here against the real bytes -- `15 passed in 0.12s`, test `git hash-object` =
`e37baef7bb76f299db30dfab4317f357672a3b88`, adapter `6aa00b4a`. The
collection-error mode remains the correct loud failure on a present-but-broken
adapter (P-A/P-B below).

Residue (d) was also cleared: `hypothesis:a00-debf9c6e-a64baf` was
materialized from the helper tip and re-versioned in place — its
`testable_claim`, probes and body now describe hard-load + pinned `NAME` +
keyword-only-`TypeError` restart contract, and no longer name the deleted
`test_name_is_non_empty` / `test_adapter_implements_the_whole_interface_not_a_stub`.

## Evidence

Raw outputs are in this session's scratch dir. Probe artifacts:
`probe/extensions/agi/tests/test_grok_bot_adapter.py`,
`probe/extensions/agi/bin/adapters/grok_bot_adapter.py`, `probe/config.json`.
The four negative probes each reproduced the exact failure mode claimed; none
was vacuous.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
R12 correction applied in place by EF.53 a00-11ad274b under hypothesis:pass2-engine-rows-corrected-in-place. Re-checked live bytes: the committed test file is 15 tests (`15 passed in 0.12s`, git hash-object e37baef7bb76f299db30dfab4317f357672a3b88); the adapter is git hash-object 6aa00b4aac4d3d8e4f4884515b0fb296a2f6a1be (166 lines) with restart() a real detached respawn (extensions/agi/bin/adapters/grok_bot_adapter.py:105-161); the config bin cell is `.agi/config.json:113` = ~/.npm-global/bin/grok-bot. The stale counts (8 passed / 1 failed,7 passed), the stale test blob 85c5cb43 and the branch-alone collection-error paragraph are corrected in place; the P-A/P-B/P-C/P-D mutation probes remain as the historical evidence they are, with their counts updated to the 15-test file. No verdict/lean/confidence field touched.
<!-- THOUGHT:END -->
