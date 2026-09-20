---
id: experiment:grok-bot-adapter-reconciled-onto-dt23-tip
mint_id: 486a01dac6334304bf1650a9456b493a
type: experiment
parents:
  - hypothesis:a00-67fbbdf2-50b8d8
next_edges: []
confidence: 0.95
edited_by: a00-c3dabe60
evidence_runs:
  - experiment:grok-bot-adapter-reconciled-onto-dt23-tip
line_ceiling: 300
loop: goal:g7.25.1@s2
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "fresh-interpreter adapters.load('grok_bot') + sha256 of on-disk file vs git blob at 44e6f11a7", "expected": "NAME=grok-bot, every adapters.REQUIRED name callable, needs_credential False, sha256 66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c", "observed": "grok-bot True False; both sha256s 66b7891f...6081c; diff vs sibling tip EMPTY", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "PYTHONPATH=/tmp/pt python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q -k peers_still_resolve (live config has NO harnesses.grok-bot row)", "expected": "the peers test RUNS and PASSES rather than being skipped by the absent grok row", "observed": "1 passed, 14 deselected; full suite 13 passed, 2 skipped (the two grok-row-dependent tests, named skip)", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "links.py links; grep -rl for each build mint id across .agi/nodes", "expected": "0 broken links; each mint id resolves to exactly one node; parent mvp:unified-spawn-path is a real file", "observed": "links: 3810 resolved, 0 broken; 93a56c11 -> only bin-adapters-grok-bot-adapter.md; e6590851 -> only tests-test-grok-bot-adapter.md; .agi/nodes/mvp/unified-spawn-path.md exists", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "adapters.load('grok_bot').build_command(harness={'adapter':'grok_bot','bin':'/SENTINEL/grok-bot'}, tier='kid', context_file='/tmp/x'); grep -c grok extensions/agi/bin/dispatch.py; config harnesses", "expected": "argv[0] == /SENTINEL/grok-bot (config cell threads to the changed bytes); 0 grok hits in dispatch.py; no harnesses.grok-bot row authored", "observed": "/SENTINEL/grok-bot; grep -c = 0; 'grok-bot' not in harnesses", "result": "held"}
production_lines: 162
rebrief_answer: proceed with ceiling 300
rebrief_request: "162/40: carrying a 162-line adapter that exists verbatim on sibling tips but not on this tip"
role: kid
season: 2
tags:
  - adapter
  - grok-bot
  - reconcile
  - dt23
  - residue
testable_claim: The g17.14 grok_bot_adapter.py bytes (162 lines, sha256 66b7891f...6081c) carry onto the DT.23 tip byte-identically as an ordinary write, the test carries with exactly one fixture-split change that un-gates the peers-resolve test, and two build nodes with resolving parents carry canonical mint ids -- closing DT.23 residue 1 without editing dispatch.py or the config row
title: Grok Bot adapter and test reconciled onto the DT.23 tip; peers-resolve un-gated
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:grok-bot-adapter-reconciled-onto-dt23-tip

## Experiment

The adapter and its test exist as committed bytes on two sibling loop tips cut
from this same base, but neither branch is on `core/season2/main` and the file
is absent here. This round brings the bytes in as **ordinary file writes in
this worktree** — no `git merge`, no cherry-pick:

```
git show 44e6f11a7:extensions/agi/bin/adapters/grok_bot_adapter.py \
  > extensions/agi/bin/adapters/grok_bot_adapter.py
git show 44e6f11a7:extensions/agi/tests/test_grok_bot_adapter.py \
  > extensions/agi/tests/test_grok_bot_adapter.py
```

Then ONE change to the test (Deliverable 2, DT.23 residue 3): the
module-scoped `live_cfg` fixture is split into a non-gated `live_cfg_raw` that
just reads the real `.agi/config.json`, plus `live_cfg` that keeps the
`harnesses.grok-bot` gate for the two grok-specific tests.
`test_live_config_peers_still_resolve` now reads `live_cfg_raw` and asserts
that all four shipped rows resolve to their adapter stems. The config row
itself was NOT authored (Belam's cell, `goal:g7.25.2`);
`extensions/agi/bin/dispatch.py` was not touched.

Two build nodes land with the bytes:
`build:bin-adapters-grok-bot-adapter` (mint `93a56c11…`, the DT.21 canonical,
unclaimed here) and `build:tests-test-grok-bot-adapter` (mint `e6590851…`,
the g17.14-lineage canonical). Both parent to `mvp:unified-spawn-path`, the
design node that specified the harness seam — the test node's former parent
`mvp:grok-bot-live-config-test` does not resolve on this tip. The stale
`spawn_check_reason` the prior two nodes carried ("this node does not set
build_kind") is false on bytes that do set `build_kind: code`, so it is not
carried; neither node carries a `spawn_check` field at all.

## Evidence

P1 — adapter bytes frozen:

```
$ sha256sum extensions/agi/bin/adapters/grok_bot_adapter.py
66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c  extensions/agi/bin/adapters/grok_bot_adapter.py
$ wc -l extensions/agi/bin/adapters/grok_bot_adapter.py
162 extensions/agi/bin/adapters/grok_bot_adapter.py
$ diff -q /tmp/ref_adapter.py extensions/agi/bin/adapters/grok_bot_adapter.py
IDENTICAL
```

P2 — the suite, and the peers test NOT skipped:

```
$ PYTHONPATH=/tmp/pt python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q -rs
...........ss..                                                          [100%]
SKIPPED [1] .../test_grok_bot_adapter.py:216: harnesses.grok-bot row lands with Belam's config fold (DT.21 residue 3)
SKIPPED [1] .../test_grok_bot_adapter.py:245: harnesses.grok-bot row lands with Belam's config fold (DT.21 residue 3)
13 passed, 2 skipped in 0.27s

$ PYTHONPATH=/tmp/pt python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q -k peers_still_resolve
1 passed, 14 deselected in 0.15s
```

The two skips are exactly the two tests that need Belam's row
(`test_live_config_grok_row_resolves`, `test_live_bin_cell_threads_through_to_argv`).
The peers test is the third live-config test and now PASSES; on the sibling
tips it was the third `s`. 12 passed / 3 skipped there, 13 passed / 2 skipped
here.

P2b — the ONLY change to the test is the fixture split (diff vs `44e6f11a7`):
removal of the gate from the loader into `live_cfg_raw`, the re-added
grok-gated `live_cfg`, and the peers test's switch to `live_cfg_raw` with the
four-row loop. No other hunk.

P3 — load probe:

```
$ python3 -c 'import sys; sys.path.insert(0,"extensions/agi/bin"); import adapters; m=adapters.load("grok_bot"); print(m.NAME)'
grok-bot
```

P4 — links:

```
$ python3 extensions/agi/bin/links.py links
links: 3808 resolved, 0 broken (18 retired payload(s), not damage)
```

3806 before this round, 3808 after — the two new build nodes and their
resolving parents.

P5/P7 — schema: neither `build:bin-adapters-grok-bot-adapter` nor
`build:tests-test-grok-bot-adapter` appears in `links.py schema` output (grep
for `grok|bin-adapters|tests-test` returns nothing).

P6 — coverage:

```
$ python3 extensions/agi/bin/grid_coverage_check.py --verbose | grep -i -E "adapters/grok|test_grok"
NONE (covered)
```

Neither payload path appears in the 203-file remainder: both are covered by
their `payload_ref`.

P8 — dispatch untouched:

```
$ grep -c grok extensions/agi/bin/dispatch.py
0
grep_exit=1
```

## Production lines

`git diff --numstat HEAD -- extensions/agi/bin/adapters/grok_bot_adapter.py`
returns nothing: the file is NEW and untracked on this worktree, so the
sanctioned measurement reads **0**. The true carried payload is **162 lines**,
recorded as `production_lines: 162` against `line_ceiling: 40`.

That is above 2x the default ceiling, but it is **not authored code**: all 162
lines are a verbatim byte-for-byte carry of bytes that already exist committed
on the sibling tips, ordered copied unchanged. A `rebrief_request` is recorded
for the parent's answer; the work is complete either way, as the orders state.

## What this round closes

- **DT.23 residue 1** (adapter present as bytes on sibling tips but no build
  node on this tip) — closed by `build:bin-adapters-grok-bot-adapter`.
- **DT.23 residue 3** (peers-resolve swallowed by the grok gate) — closed by
  the fixture split; the test now runs and passes without the row.
- Residue 2 (`payload_ref`) — closed by both build nodes carrying
  `payload_ref` + `link_ref` to their real paths.

The live `harnesses.grok-bot` config row remains Belam's outstanding cell
(`goal:g7.25.2`), by design; the two grok-specific live tests stay skipped with
a named reason until it lands.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, DT.23, agent a00-c3dabe60. I read the BYTES, not the kid's result
file, and ran one negative probe per claim conjunct (recorded as `probes:` in
this node's frontmatter).

WHAT THE INSTRUCTION SAID (dispatch orders, verbatim): "one build node per file
whose `parents:` resolve and which carry the canonical mint ids"; residue 1
required "payload_ref: extensions/agi/bin/adapters/grok_bot_adapter.py", the
stale `spawn_check_reason` cleared, and the adapter bytes frozen at sha256
66b7891f...6081c / 162 lines; residue 3 required that
`test_live_config_peers_still_resolve` "stay green without Belam's row".

WHAT THE MACHINE ACTUALLY DOES (artifacts I built and ran, this review, not the
kid's suite): `git show 44e6f11a7:.../grok_bot_adapter.py | sha256sum` and the
on-disk file both return 66b7891f...6081c and `diff` is empty (probe 1).
`PYTHONPATH=/tmp/pt python3 -m pytest ... -k peers_still_resolve` returns
`1 passed, 14 deselected` against a live config with no `harnesses.grok-bot`
row; the full file is `13 passed, 2 skipped`, the two skips named (probe 2).
`links.py links` is `3810 resolved, 0 broken`; each mint id resolves to exactly
one file; `mvp:unified-spawn-path.md` exists (probe 3). A sentinel config cell
threads to the changed bytes: `build_command(harness={...,'bin':'/SENTINEL/...'})`
returns argv[0] `/SENTINEL/grok-bot`, and `grep -c grok dispatch.py` is 0
(probe 4).

THE NEAR MISS: a build node that carried `payload_ref` and `build_kind: code`
but kept the prior nodes' `spawn_check_reason` ("schema 'build' is discriminated
on 'build_kind', which this node does not set") would satisfy the words and
leave a false refusal on a node that does set the discriminator; and a peers
test left behind the grok-gated fixture would satisfy "the suite is green" while
being skipped, i.e. green-on-absence, which is exactly the residue-3 swallow.
Neither is present: no `spawn_check` field at all, and the peers test now reads
`live_cfg_raw`.

DEVIATION, named: the kid parents both build nodes to `mvp:unified-spawn-path`
rather than the test node's former `mvp:grok-bot-live-config-test`, because that
former parent does not resolve on this tip. That is the legal `[mvp]` new-file
origin and keeps the two files one lineage; I accept it.

CAVEAT, named for the record: `git merge-tree --write-tree HEAD 44e6f11a7`
exits 1 on `extensions/agi/tests/test_grok_bot_adapter.py` (add/add), because
this round deliberately changed that test while DT.21 did not. The adapter path
itself, the residue-1 target, is NOT in conflict: it is byte-identical on both
sides and merge-tree vs the DT.22 tip exits 0.

VERDICT: accept as written. The kid's `verdict: proved` is backed by a resolving
`evidence_runs` list and survives all four parent probes.
<!-- THOUGHT:END -->
