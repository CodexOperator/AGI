---
id: experiment:a00-1fbbdf68-efc934
mint_id: 46299ee900c54ba9a2beac181c92003f
type: experiment
parents:
  - hypothesis:l4-the-graph-as-a-golden-3d-web-in-two-layers
next_edges: []
confidence: 0.9
edited_by: a00-be97b565
evidence_runs:
  - experiment:a00-1fbbdf68-efc934
loop: hypothesis:l4-the-graph-as-a-golden-3d-web-in-two-layers@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c7e199913459474e
season: 2
title: A00 1fbbdf68 efc934
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1fbbdf68-efc934

## Experiment

KID A + KID C of the owner-priority visualization round, on top of kid B's merged
work (already in this worktree). Two parts, both in the bytes now.

**PART 1 — the LIVE OVERLAY** (the claim's original item 3, reported done by the
L4.235 harvest and NOT in the bytes):
- (1a) `graphweb.live_view` now returns `graph_version` — kid B's
  `graph_version(graph_root)` (a sha256 of the sorted ACTIVE id set) — so the
  5 s poll can decide when to re-fetch `/graph.json`.
- (1b) `app.js`: the 5 s poll that DID NOT EXIST is now real — `setInterval`
  every 5000 ms, `getJSON` with `cache: "no-store"`, replaces `state.live`;
  when `live.graph_version` differs from the last seen one (or a first frame),
  it re-fetches `/graph.json`, applies it, and `rebootRenderer()` tears down
  the stage and re-runs the active renderer (three.js or the 2D fallback) —
  no page reload.
- (1c) live seat->node work edges are now `THREE.LineSegments` (not a
  `pointsCloud` of two dots), bright gold when a seat is `active`, dim
  otherwise; AGENT edges are drawn too, from `seat:<dispatched_by>` to each
  `working_on` node, in BOTH renderers (2D `drawLive2D` now iterates
  `liveSeatPairs()` which folds in `state.live.agents`). An active seat's
  point PULSES — a sin on the seat sphere's `scale` in `frame()`.

**PART 2 — GHOST NODES** (owner verbatim 2026-09-11 15:5xZ, parents AND kids
have no seat but float near the future node they'll build):
- (2a) SERVER (`live_view`): each live agent gains `target` (its dispatch
  manifest `agents[].target`; "" when unreadable), `parent` (the parent-tier
  lease id with the same `iter`, else None), and `new_nodes` — real
  `{id, type, title, parents}` records parsed from every NEW (`??`/`A`) node
  file's frontmatter in the relevant worktree (a kid's own file lives in its
  PARENT's worktree, filtered to ids containing the agent id). Every read
  wrapped; no manifest / corrupt manifest / dead worktree all fail open with
  no traceback. New helpers: `_worktree_for_agent`, `_agent_parent_id`,
  `_agent_target`, `_new_node_records`.
- (2b) CLIENT (`app.js`): every live agent whose node is not in the served
  graph floats as a GHOST — a blank semi-transparent circle (opacity 0.45,
  no text) with a seeded 8-15-unit offset from its `target` node's position
  and a slow bob (a sin on the z-axis, ~3 s), breathing (a sin on `scale`).
  When `new_nodes` carries the record the ghost SNAPS: solid gold, real
  id/type/title (tooltip on hover), an edge to its first parent. When
  `/graph.json` later contains that id (graph_version change -> re-fetch
  from (1b)), the ghost retires and the real node stands at its layout
  position. `ghostFor`/`liveGhosts`/`drawGhosts2D`/`buildLive` cover BOTH
  renderers. Pointer-hover shows `<tier> <agent> -> <target>` in 3D and 2D.

**TESTS ADDED** (fixture-only, never a live pane):
- `test_live_agents_carry_target_parent_and_new_nodes` — a fake parent worktree
  (absolute path) with a dispatch manifest and one untracked KID node file;
  `/live.json` agents[] carries `target`, `parent`, and the `new_nodes` record
  for the kid, and the untracked id is in `working_on`.
- `test_no_manifest_yields_empty_target_no_traceback` — absent + corrupt
  manifest both give `target ""` and no traceback.
- `test_live_view_carries_graph_version` — `/live.json` carries `graph_version`;
  changes when an id is added.

Run: `pytest extensions/agi/tests/test_graphweb.py
      extensions/agi/tests/test_bin_help_smoke.py -q` -> **76 passed, 1 skipped**
(was 73 before; the 3 new ghost/version tests added).

## Evidence

REAL-TREE PROOF (server against THIS worktree's `.agi`, `graphweb.py serve
--port 8892`):
- `/live.json` carries `graph_version: 37868854a089`.
- My own live kid lease: `{'agent': 'a00-1fbbdf68', 'tier': 'kid',
  'target': 'hypothesis:l4-the-graph-as-a-golden-3d-web-in-two-layers',
  'parent': 'a00-be97b565', 'new_nodes': [{'id':
  'experiment:a00-1fbbdf68-efc934', 'type': 'experiment', 'title': 'A00
  1fbbdf68 efc934', 'parents': ['hypothesis:...']}]}` — the ghost's lifecycle
  (float near target -> snap on new_nodes) works on real live data.
- Parent `a00-be97b565`: `target` set, `parent: None`, `new_nodes` = the three
  kid nodes unfiltered. Parent `a00-fbb3edda` (L4.251): `target` set to its
  hypothesis, `new_nodes` = its kid's node.
- `/graph.json` warm-memo: 0.12 s (persist/reuse contract holds; cold
  fresh-process parse+persisted-read 2.7 s — not re-proven, that's kid B's
  defect B). `/live.json`: 0.17 s. `/`, `/graph.json`, `/app.js` all 200 with
  correct content types.
- `node --check extensions/agi/web/graph/app.js` -> clean (JS syntax valid).

No node files were edited on the real tree; nothing to restore. No server left
running. index.html and the palette untouched; no new Python or JS deps.

## Agent Notes
Live overlay (5s poll, graph_version re-fetch, LineSegments seat+agent work edges, seat pulse) + ghost nodes (target/parent/new_nodes server-side, breathing blank->snap->retire circles both renderers). 76 passed, 1 skipped; real-tree /live.json shows graph_version + my kid lease target/parent/new_nodes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-be97b565, L4.250) — ACCEPTED as proved.
(1) INSTRUCTION: the target's item (3) — "the page polls /live.json every 5 s ... edges appear and disappear without reloading the page" — plus the owner's 15:5xZ ghost order; the helper had measured that NONE of it was in the L4.235 bytes.
(2) MACHINE: app.js:101 `setInterval(tick, 5000)`, getJSON with `cache:"no-store"` (app.js:53), graph_version diff -> re-fetch (app.js:87); live edges built by `THREE.LineSegments` (app.js:322) and the 2D `liveSeatPairs()` folds in agents (app.js:239); ghosts `ghostFor`/`liveGhosts`/`drawGhosts2D` (app.js:121-266). graphweb.py `live_view` returns `graph_version`; I called it on the real tree -> `37868854a089`, and my own parent lease carried `target` = the hypothesis, `parent` = None, `new_nodes` = 3 kid records. `pytest test_graphweb.py test_bin_help_smoke.py -q` -> 76 passed, 1 skipped, reproduced.
(3) NEAR MISS: a poll that re-fetches /graph.json on EVERY tick satisfies "polls /live.json every 5 s" and rebuilds the geometry 12x a minute; the graph_version gate is what makes the poll cheap. Likewise a ghost drawn from `working_on` alone would be a circle with no future-node identity — `new_nodes` is what lets it snap.
(4) DEVIATION: none.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-be97b565, L4.250): accepted as proved; 5s poll/graph_version/LineSegments+agent edges/pulse and ghost nodes all found in app.js and graphweb.py, real-tree /live.json carries graph_version 37868854a089 and my lease target/parent/new_nodes, 76 tests reproduced.
