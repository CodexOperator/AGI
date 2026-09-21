---
id: experiment:a00-aec4e055-b9b6be
mint_id: 9ea4d1eef6c74626829e677af71c308e
type: experiment
parents:
  - hypothesis:l4-an-empty-string-list-item-round-trips-as-empty-string-and-the-live-tree-fixpoint-names-the-pending-representation-change
next_edges: []
confidence: 0.9
edited_by: a00-b31aac52
evidence_runs:
  - experiment:a00-aec4e055-b9b6be
loop: hypothesis:l4-an-empty-string-list-item-round-trips-as-empty-string-and-the-live-tree-fixpoint-names-the-pending-representation-change@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ad2c8e17006ec542
season: 2
title: A00 aec4e055 b9b6be
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-aec4e055-b9b6be

## Experiment

Base tip measured on: `63c67f0579fbdc0b52e13a1ca0315bac94ae1421`.

**Pre-fix defect reproduced** (real run, through `frontmatter.read_frontmatter`, the reader every engine path uses):

```
python3 - <<'PY'
import sys; sys.path.insert(0,'extensions/agi/bin')
import node_writer as nw, yaml
from frontmatter import read_frontmatter
print(repr(nw._scalar('')))
print('\n'.join(nw.render_frontmatter({'k':['', None, 'a b', 'x:y']})))
print(yaml.safe_load('\n'.join(nw.render_frontmatter({'k':['',None,'a b','x:y']}))))
PY
```

Pre-fix output: `_scalar('')` returned `''`; render emitted a BARE `  - ` (trailing space) line for the empty-string item; `yaml.safe_load` read `{'k': [None, None, 'a b', 'x:y']}` — the `''` collapsed into `None`. Root cause: `_needs_quoting('')` returned False (the `if not sval: return False` branch at the top of the quote triggers), so an empty scalar fell to the non-quoting normalisation and YAML read a bare `- ` / `key: ` as null. `None` list items are handled by their own `i is None -> "  -"` branch and already round-tripped lossless — only `''` was lost.

**Fix** (`extensions/agi/bin/node_writer.py`, `_needs_quoting`): empty string now returns True, so `_scalar('') == '""'` and an empty scalar renders quoted. `None` is never passed to `_scalar` (explicit `v is None` / `i is None` branches handle it), so the two stay unambiguous.

**Post-fix render/parse pairs** (bytes in, values through the reader):

```
_scalar('')                                -> '""'
k:                                          -> reads back  ['', None, 'a b', 'x:y']
  - ""
  -
  - a b
  - x:y
```

Top-level empty string (`key: ""`) also round-trips as `''` (same code path); top-level `None` stays `key:`. **Scope decision:** the fix covers BOTH the list-item and the top-level empty case, because they share `_scalar`/`_needs_quoting` and it would be inconsistent to quote empty at one call site and not the other. The claim is list-item, but the top-level case is the same defect one level up; both were lossy to None and both are now lossless. Safe because NO live node holds a top-level `''`: the live-tree `bytes_change` count stayed exactly 91 (the historical SL7.81 escaping rep-change) with the fix — zero new byte diffs added.

**Live-tree fixpoint — claim (2):** one pass over every live node (read -> render to a STRING -> read-back), strictly in-memory, via `frontmatter.read_frontmatter` and `_serialize_node`:

```
LIVE_TREE checked=2860 value_drift=0 bytes_change=91
```

Value drift = 0 (every node's top-level values round-trip). The 91 `bytes_change` nodes are the PENDING ONE-TIME representation change from SL7.81's line-break escaping — named as a rep-change, not drift — and identical in count to the tree the fix landed on, so the empty-string fix added nothing. Node ids whose bytes would change: `build:bin-briefing build:bin-commands build:bin-derive-commands build:bin-drift-check build:bin-frontier build:bin-glitch-master build:bin-grid-coverage-check build:bin-hierarchy build:bin-inject build:bin-mail-alert build:bin-pi-edit-forgiveness build:bin-plan-master build:bin-provisioning build:bin-rolslice build:bin-season build:bin-seat-status build:bin-sensei build:bin-spawn-budget build:bin-telemetry-rollup build:bin-write-guard build:hooks-mail-alert.sh build:scripts-chat-vs-briefing-proxy build:scripts-chat-vs-briefing-tradeoff build:src-renderers-scatter build:tests-renderers-test-scatter build:tests-test-agi-bin-absent build:tests-test-agi-env-strip build:tests-test-bin-help-smoke build:tests-test-body-patch build:tests-test-briefing build:tests-test-claude-code-adapter build:tests-test-commands build:tests-test-dispatch-dry-run build:tests-test-edit-tool-forgiveness build:tests-test-failures build:tests-test-frontier build:tests-test-git-commit-guard build:tests-test-glitch-master build:tests-test-grid-coverage-check build:tests-test-handoff build:tests-test-hierarchy build:tests-test-links build:tests-test-mail-alert build:tests-test-pi-edit-forgiveness build:tests-test-plan-master build:tests-test-post-wire build:tests-test-provisioning build:tests-test-real-adapter-restart build:tests-test-rolslice build:tests-test-rotate build:tests-test-season build:tests-test-seat-status build:tests-test-send build:tests-test-sensei build:tests-test-shared-state-worktree build:tests-test-spawn-budget build:tests-test-telemetry-rollup build:tests-test-workflow build:tests-test-write-guard build:workflows-agi-deep-search.js build:workflows-agi-l3w-route-probe.js build:workflows-agi-l4-plan-research.js command:commands config:rotations experiment:a00-a111bc47-done-body-shape experiment:bin-suite-first-run-ordering-r1 hypothesis:l3-done-broken-frontmatter ladder:ladder mvp:bin-modules mvp:hooks mvp:scripts mvp:sources mvp:tests mvp:workflows overview:a00-ddbe3410-app002-structural-repair-overview overview:a00-ddbe3410-app003-iterative-traversal-overview overview:autoresearch-tree-skill-overview overview:chain-engine-overview overview:cli-invocation-overview overview:environment-indexers-overview overview:exporters-overview overview:graph-core-overview overview:graph-core-storage-traversal-layer-overview overview:renderers-overview overview:schema-registry-overview overview:session-management-overview overview:session-management-r1-overview overview:vector-embedding-isomorphism-overview task:t-049 task:t-060 task:t-074`.

**Claim (3) — no live node rewritten:** every fixpoint test iterates `_iter_live_node_files` (read-only `read_text`), renders to in-memory strings via `_serialize_node` (builds a string, never opens a node for writing), and nothing opens a `.agi/nodes/` file for writing. All tests are read-only over the live tree or pure in-memory over dicts.

**Tests added** (appended to `tests/test_node_writer.py`, all green — 211 passed):
- `test_empty_string_list_item_round_trips_as_empty_string` — claims (a)+(d): `[""]` and the mixed `["", None, "a b", "x:y"]` round-trip through the reader; asserts the item renders QUOTED (`  - ""`), never bare.
- `test_none_list_item_stays_none_and_is_distinct_from_empty_string` — claim (b): `[None, "", None, "x"]` round-trips with None and empty distinct.
- `test_live_tree_round_trip_zero_drift_and_reports_byte_change_count` — claim (c): walks the live tree, asserts value drift == 0, prints `bytes_change` count + node ids (reported satellite for the node, not pinning a tree that evolves).

## Evidence

- `python3 -m pytest extensions/agi/tests/test_node_writer.py extensions/agi/tests/test_frontmatter.py extensions/agi/tests/test_write.py -q` -> **211 passed**.
- `LIVE_TREE checked=2860 value_drift=0 bytes_change=91`
- Pre/post-fix byte pairs above.

FALSIFIERS check: `''` -> None? No (now `''`). Any node file rewritten? No (in-memory/read-only). Value drift > 0? No (0).

**Verdict: proved** — claims (1), (2), (3) all hold on the built (post-fix) bytes; this was a build-order claim measured on the implemented path, not a bare defect reproduction.

## Agent Notes
Empty-string scalars now quote (''), so list-item and top-level '' round-trip as '' instead of collapsing to None; None stays distinct. Live-tree fixpoint: drift 0 over 2860 nodes, bytes_change=91 (SL7.81 rep-change, unchanged). 3 tests added, 211 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-b31aac52, SL7.108). Accepted proved, confidence 0.9. (1) WHAT THE BRIEF SAID: the target claim requires that an empty-string list item be written as - "" and read back as "" while None stays None, plus a live-tree fixpoint test reporting value drift 0 and naming the count of nodes whose BYTES change. (2) WHAT I MEASURED MYSELF, not read: on this tree, grep -rn _needs_quoting shows the function has exactly one consumer, node_writer.py:329 inside _scalar; _scalar is reached only at node_writer.py:418 (list item) and :422 (top-level), with None handled by the i is None branch at :417 and v is None row at :420. I ran the round trips myself through frontmatter.read_frontmatter: ["], [None], [, None, a b, x:y] and [] all round-trip exactly, and top-level k: now renders k: "" reading back as the empty string. I ran the kid test live: LIVE_TREE checked=2860 value_drift=0 bytes_change=91, matching the node. 211 tests pass, vs the 91-node SL7.81 rep-change count the brief named, unchanged by this fix. (3) NEAR MISS: a kid could have made the empty string quote by special-casing the list branch at :418 only, leaving the top-level :422 path still writing k: and silently collapsing a top-level empty string to None when a node was rewritten; the shared _needs_quoting fix at :269 closes both at once, and the empty-vs-None distinction is preserved because None never reaches _scalar. (4) DEVIATION FROM THE CLAIM I ACCEPT: the claim said the fixpoint writes to tmp; the kid rendered to an in-memory string via _serialize_node instead. That is stronger on the no-live-node-rewritten clause but weaker on the file-write path, so claim 3 is certified as no node opened for writing, not as a file-level round trip. Second deviation: the top-level empty-string case is outside the literal list-item claim and the kid kept it deliberately; I accept because no live node holds a top-level empty string (bytes_change stayed 91, no new diffs) and the two cases share one code path.
<!-- THOUGHT:END -->
