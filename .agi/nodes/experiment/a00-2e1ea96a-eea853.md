---
id: experiment:a00-2e1ea96a-eea853
mint_id: 2ee3f70c16b5467abe302c8a723c7e0a
type: experiment
parents:
  - hypothesis:l4-the-graph-as-a-golden-3d-web-in-two-layers
next_edges: []
confidence: 0.8
edited_by: a00-c42731c0
evidence_runs:
  - experiment:a00-2e1ea96a-eea853
loop: hypothesis:l4-the-graph-as-a-golden-3d-web-in-two-layers@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8ad371f1e0011393
season: 2
title: l4-page-renderer-plus-layout-cache
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-2e1ea96a-eea853

## What I built (kid 2 of 3 — page + layout cache)

**(A) Page — NEW files `extensions/agi/web/graph/index.html` + `app.js`.**
- Renders `/graph.json` as golden points with dim golden edges on the dark served
  ground. Palette (ground/gold) comes from the served `palette`, never hardcoded;
  `document.body.style.background` set from it. Root `goal:g17` emphasized:
  brightened copy in layer1 + a fat gold sphere (3D) / ringed dot (2D).
- Two layers: every node drawn once at z=0 and once at z=`layer1_z` (60); layer1
  hovers above layer0. Verified payload: root present in BOTH layers (2 copies
  [0,1]), nodes by layer {0:1800, 1:316}, palette measured
  {ground:#0e1625, gold:#988355}.
- Controls (custom orbit — drag=orbit, wheel=zoom, right/middle-drag=pan,
  R=reset). Hover = label (title + id) via nearest-projected-point pick.
- `/live.json` drawn as bright gold segments from each ACTIVE seat to its
  `working_on` nodes (dim for idle), refreshed periodically; same in 2D path.
- **Falsifier (HOLDS):** three.js loaded by *dynamic* `import(THREE_URL)` in
  try/catch — a dead CDN degrades to a plain 2D `<canvas>` (same data, no blank
  screen, no throw). Verified headless: CDN URL forced unreachable → page
  rendered `degraded` canvas with "2D — 2116 nodes, 2136 edges".
- three.js uses only verified r160 API (BufferGeometry+Points/BufferAttribute,
  Scene, PerspectiveCamera, WebGLRenderer, setAnimationLoop, Vector3.project)
  cross-checked against the upstream raycasting-points example; edges are
  bead-sampled point runs (dim dots), avoiding any addon importmap.

**(B) Required fix in `graphweb.py` — memoized layout.**
- Added module-level `_LAYOUT_CACHE` + `cached_build_graph()` + a cache key over
  graph-root path + mtimes of every `nodes/**/*.md` + seats.md + config.json.
  `do_GET("/graph.json")` now calls `cached_build_graph`.
- `/live.json` stays uncached (must be fresh).
- **Falsifier (HOLDS):** cold first `/graph.json` = 154 s (matches kid 1's
  ~170 s measurement; cold build honestly still slow). Warm second GET on the
  real 2115-node graph = **0.038–0.045 s**, orders of magnitude under the 2 s
  bar. curl warm GETs #1/#2/#3 = 0.045 / 0.039 / 0.040 s, all 603976 bytes
  (byte-identical to cold payload).
- Cache invalidation verified in /tmp: key stable when unchanged, changes when a
  node file mtime changes; memoized call returns the same object.

## Tests run
- `node --check extensions/agi/web/graph/app.js` → JS syntax OK
- `python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py extensions/agi/tests/test_cli.py -q` → 76 passed, 1 skipped
- Headless JS stub (CDN forced down): FALSIFIER PASS — 2D canvas rendered, no
  blank screen, no throw.
- No `tests/test_graphweb.py` touched (kid 3 owns it); config.json untouched.

## Caveat on the 3D path
Live three.js CDN path could not be exercised headlessly here (no browser); it
is syntax-valid, uses only verified r160 API, and is wrapped so any runtime
error falls back to the verified 2D canvas rather than a blank screen.

## Agent Notes
Page (index.html+app.js, 3D w/ 2D fallback) + memoized layout cache in graphweb.py; warm /graph.json 0.04s vs cold 154s, CDN-down renders 2D not blank

PARENT REVIEW (a00-c42731c0, L4.235), accepted as kid 2 of 3. Verified in the bytes: (1) extensions/agi/bin/graphweb.py now has _LAYOUT_CACHE plus cached_build_graph keyed on graph root and node mtimes, and do_GET at graphweb.py:817 calls cached_build_graph, so the 170 s layout is no longer recomputed per request; /live.json stays uncached, which is correct. (2) extensions/agi/web/graph/index.html and app.js exist; app.js uses a dynamic import(THREE_URL) inside try/catch and falls to draw2D, so the FALSIFIER holds by construction; palette is read from /graph.json, no hardcoded colors. Verdict inconclusive_lean_proved:80 is the honest label, kept as-is: the 3D CDN path could not be run headlessly and the kid said so. CAVEAT carried to kid 3: the cache key hashes every nodes/**/*.md mtime, so any node edit re-busts the cache and the next /graph.json costs the full 170 s; that is acceptable for round 1 only if tested and stated, and kid 3 should assert the cache invalidation contract rather than assume it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW EDIT (a00-c42731c0, L4.235). No body claim changed; the parent added its review. WHAT THE INSTRUCTION SAID: review every node, read the artifact not the report, keep the honest lean rather than upgrade it. WHAT THE MACHINE ACTUALLY DOES: I read graphweb.py:629-639 cached_build_graph and graphweb.py:817-818 the do_GET branch, and app.js lines 1-60 plus the catch at 327, so the two falsifier-bearing mechanisms are visible in the source I can cite by line. NEAR MISS: the node reports warm /graph.json 0.038-0.045 s; believing that number without reading do_GET would have missed that the cache key is mtime-based, so the very next node edit returns the payload stale until the 170 s rebuild, which changes what the dashboard shows during a live round. I left the verdict at inconclusive_lean_proved:80 because the kid already declined the stronger claim for the right reason. Evidence linked: experiment:a00-2e1ea96a-eea853.
<!-- THOUGHT:END -->
