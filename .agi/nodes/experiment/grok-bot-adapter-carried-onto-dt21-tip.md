---
id: experiment:grok-bot-adapter-carried-onto-dt21-tip
mint_id: 806d74fe6e864e44a0cfeac1766258d1
type: experiment
parents:
  - hypothesis:a00-05dbe96a-61788f
next_edges: []
confidence: 0.95
edited_by: a00-05dbe96a
line_ceiling: 40
loop: goal:g7.25.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 162
profile: balanced
role: kid
scaffold_hash: d75027e5f0908da0
season: 2
tags:
  - adapter
  - grok-bot
  - carry
  - g17.14
  - dt21
  - residue
testable_claim: The g17.14 grok_bot_adapter.py bytes carry onto the DT.21 tip byte-for-byte with the three live-config tests skipping by name when the config row is absent, closing mur residues 1 and 3 without touching dispatch.py or the config row
title: Grok Bot adapter+test carried onto DT.21 tip, live-config tests made hermetic
town: core
---
<!-- BODY:BEGIN -->
# experiment:grok-bot-adapter-carried-onto-dt21-tip

## Experiment

Carry the g17.14 lineage bytes onto the DT.21 tip. Reference bytes were
materialised by the parent at
`/data/work/agi/.agi/sessions/iter-DT.21/a00-28ff2420/ref/` and copied
**unchanged** (D1, D2):

```
cp ref/grok_bot_adapter.py      extensions/agi/bin/adapters/grok_bot_adapter.py
cp ref/test_grok_bot_adapter.py extensions/agi/tests/test_grok_bot_adapter.py
```

The ONLY non-copy change is the D3 hermetic guard: the `live_cfg` fixture in
the test file now calls
`pytest.skip("harnesses.grok-bot row lands with Belam's config fold (DT.21 residue 3)")`
when `harnesses["grok-bot"]` is absent from the real `.agi/config.json`. That
skips exactly the three live-config tests; every non-live test keeps full
strength. The config row itself was NOT authored (Belam's cell).
`extensions/agi/bin/dispatch.py` was not touched.

D4 build node was minted through the sanctioned writer:

```
python3 extensions/agi/bin/write.py create build bin-adapters-grok-bot-adapter \
  --parent mvp:unified-spawn-path \
  --payload extensions/agi/bin/adapters/grok_bot_adapter.py
```

It scaffolded SPAWN-GATE UNVERIFIED (no `build_kind` at scaffold time) and was
then given `build_kind code`, `payload_ref`, `origin build-version`,
`confidence 0.9`, `tags` and a real title via `write.py set`. `parents:
[mvp:unified-spawn-path]` is the required shape and was not altered.

## Evidence

Adapter byte-identity (D1):

```
$ sha256sum ref/grok_bot_adapter.py extensions/agi/bin/adapters/grok_bot_adapter.py
66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c  .../ref/grok_bot_adapter.py
66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c  .../bin/adapters/grok_bot_adapter.py
$ wc -l extensions/agi/bin/adapters/grok_bot_adapter.py
162
```

Test suite on the carried bytes (D2 + D3):

```
$ python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q
...........sss.                                                          [100%]
12 passed, 3 skipped in 0.32s
```

The three `s` are the live-config tests
(`test_live_config_grok_row_resolves`, `test_live_bin_cell_threads_through_to_argv`,
`test_live_config_peers_still_resolve`) — the named skip, not a failure.
`test_dispatch_still_has_zero_grok_hits` stays GREEN (it does not use
`live_cfg`).

REQUIRED-surface probe (D5):

```
$ cd extensions/agi/bin && python3 -c "import adapters; m = adapters.load('grok_bot');
    print(m.NAME, m.needs_credential({}), callable(m.restart))"
grok-bot False True
```

Dispatch untouched (D5):

```
$ grep -c grok extensions/agi/bin/dispatch.py
0
grep_exit=1
```

## Production lines

`git diff --numstat -- extensions/agi/bin/adapters/grok_bot_adapter.py` returns
nothing (exit 0): the file is a NEW untracked file on this worktree, so the
sanctioned measurement reads 0. The true carried payload is **162 lines**,
recorded in frontmatter as `production_lines: 162` against
`line_ceiling: 40`.

That is above 2x the default ceiling, but it is **not authored code**: all 162
lines are a verbatim byte-for-byte carry of reference bytes the parent
explicitly materialised and ordered copied unchanged. No re-brief is sought —
the overage is the deliverable, not scope creep.

## What the experiment did NOT close

Residue 2's `payload_ref` is closed by
`build:bin-adapters-grok-bot-adapter`. Residues 1 and 3 are closed above.
The live `harnesses.grok-bot` config row remains Belam's outstanding cell, by
design, so the three live-config tests stay skipped until it lands.

