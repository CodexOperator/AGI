---
id: experiment:a00-a1a66e45-b65e5c
mint_id: 8662707c2ff440289bdb9b3523818a5d
type: experiment
parents:
  - hypothesis:l4-the-graph-as-a-golden-3d-web-in-two-layers
next_edges: []
confidence: 0.92
edited_by: a00-a4f37350
evidence_runs:
  - experiment:a00-a1a66e45-b65e5c
loop: hypothesis:l4-the-graph-as-a-golden-3d-web-in-two-layers@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: fea9ff11dbdd711c
season: 2
title: "fixed the dead 3D branch: real r160 materials, one mesh per node at its own layer, renderer seam, and a pinned-bytes node falsifier (red-then-green) plus -t agi-rc tmux"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a1a66e45-b65e5c

## Experiment

PAGE-FIX-ONLY round (L4.252) under `hypothesis:l4-the-graph-as-a-golden-3d-web-in-two-layers`, the Prime merge-up 38 falsifier as the assignment. The golden 3D branch of `extensions/agi/web/graph/app.js` was DEAD CODE: it constructed `THREE.Float32ColorMaterial` (zero occurrences in the pinned three r160 bytes), so `render3D` threw before the renderer existed and `boot()` degraded to the 2D canvas every time. This round made the 3D path actually render and proved it with a node falsifier against the PINNED bytes.

What I changed (FILE SCOPE exactly as cut):
* `extensions/agi/web/graph/app.js` — replaced the three `THREE.Float32ColorMaterial` constructions (root sphere, seat sphere, ghost circle) with three r160's real `MeshBasicMaterial` (color / transparent / opacity); fixed `fill()` to call `new THREE.Color(n)` (hex int) instead of feeding 0-255 ints to the 0-1-float `Color(r,g,b)`; made the node cloud ONE `THREE.Points` mesh per node carried on the object's `position` at its OWN layer's z (layer 1 on the sanctuary plane, layer 0 on the outer plane — never a copy on both planes); fixed the latent `mesh.scale.setXYZ` (no such method on a Vector3) to `mesh.scale.set`, which was a second, un-reported degrader that would throw inside `buildLive` and still fall to 2D; exposed ONE renderer seam (`globalThis.__makeRenderer || state.makeRenderer || (() => new THREE.WebGLRenderer(...))`) so the harness can inject a stub; exposed the boot lifecycle as `globalThis.__agiBoot = boot()` for the harness to await.
* `extensions/agi/bin/graphweb.py` — ONE hunk: `_tmux_windows()` now runs `tmux list-windows -t agi-rc` (rotate.py DEFAULT_TMUX_SESSION) instead of a bare `list-windows`; absent session -> empty set, never a raise.
* `extensions/agi/tests/test_graphweb.py` — added `test_tmux_list_windows_is_scoped_to_agi_rc` asserting the argv carries `-t agi-rc`; every prior test stays green.
* NEW `extensions/agi/tests/test_graphweb_page_r160.py` — the falsifier. It fetches the pinned bytes once into `~/.cache/agi-graphweb/` (SKIP-not-fail when unreachable, never vendored), rewrites ONLY the `THREE_URL` constant for a local `file:` URL (node cannot `import()` https:), and runs the new node ESM harness.
* NEW `extensions/agi/tests/r160_page_harness.mjs` — installs a DOM/window/fetch/rAF/performance stub BEFORE dynamically importing app.js, injects a renderer stub through the seam, drives one animation frame, and asserts (a) boot completes with no `3D failed` / `degraded 2D`, (b) render called >= 1 and one node mesh per canned node at its own layer's z, (c) a captured 5000 ms interval fetches /live.json with `cache:no-store` and re-fetches /graph.json after a graph_version change.

Proof of the falsifier (RED before, GREEN after — the SAME harness):

RED on a reconstructed pre-fix build (the Float32ColorMaterial + `boot();` shape):
```
RESULT {"ok":false,...,"log":["3D failed (THREE.Float32ColorMaterial is not a constructor) — degraded 2D",...]}
rc=1   threeBranchCompleted=false renderCalled=false nodeMeshCount=0
```
GREEN on the fixed app.js:
```
RESULT {"ok":true,...,"log":["3D — 4 nodes, 1 edges","3D — 4 nodes, 1 edges"]}
rc=0   threeBranchCompleted=true renderCalled=true nodeMeshCount=4
       oneMeshPerNode=true bothPlanes=true meshesMatchNodeLayers=true
       pollExists=true pollLiveCache=no-store noRefetchOnFirstTick=true
       refetchOnVersionChange=true
```

`node --version` -> **v22.22.2**.

Full suite, named files:
```
python3 -m pytest extensions/agi/tests/test_graphweb_page_r160.py extensions/agi/tests/test_graphweb.py extensions/agi/tests/test_bin_help_smoke.py -q
-> 80 passed, 1 skipped   (the one skip is pre-existing node_writer --help, not mine)
```

## Evidence

- Pinned bytes confirmed: `grep -c Float32ColorMaterial three-0.160.0.module.js` -> 0; `class MeshBasicMaterial / PointsMaterial / LineBasicMaterial / WebGLRenderer / Color` all present. (1,272,972 bytes, HTTP 200 from this box.)
- Same harness fails on pre-fix, passes on fixed — this is a falsifier, not a smoke test.
- tmux argv now `["tmux", "list-windows", "-t", "agi-rc"]`; test green.
- No browser claim: the node run against the pinned bytes IS the evidence.

## Agent Notes
Fixed the dead 3D branch: r160 MeshBasicMaterial (x3), fill() new THREE.Color(n), one mesh per node at its own layer z, latent scale.setXYZ->set, renderer+__agiBoot seams; tmux -t agi-rc; new node falsifier (pinned-byte harness, red-then-green) + tmux argv test. 80 passed, 1 pre-existing skip.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-a4f37350 (L4.252, 2026-09-11). What the instruction said: the helper pre-dispatch L4.252 assigned the page FIX-ONLY round with four named defects and the Prime merge-up 38 falsifier (a node test against the PINNED three bytes asserting the 3D branch completes and the 5 s poll fires; RED on pre-fix FIRST, then green). What the machine actually does, read in the bytes and RUN (not read off the source): (1) extensions/agi/web/graph/app.js:376/440/457 now build THREE.MeshBasicMaterial; grep -rn Float32ColorMaterial over extensions/ returns only a comment at app.js:374 and a test __pycache__ — the dead identifier is gone from every executed path; (2) app.js:304 is new THREE.Color(n) (hex int), no 0-255 ints; (3) app.js:337-349 builds ONE pointsCloud mesh per node and sets mesh.position from n.pos, whose [2] already carries the layer z — one mesh per node at its own plane, scene.nodeMeshes is real app state not a harness invention; (4) graphweb.py:392 runs ["tmux","list-windows","-t","agi-rc"] and my own probe on this box returns the 18 agi-rc windows, so the -t does not silently empty the real overlay. The falsifier is IN the test, not a manual run: test_graphweb_page_r160.py::test_same_harness_fails_on_prefix_app reconstructs the Float32ColorMaterial build from the fixed source and ASSERTS p.ok is False with threeBranchCompleted False and renderCalled False, while test_r160_3d_branch_completes_and_poll_fires asserts oneMeshPerNode / meshesMatchNodeLayers / pollExists / pollLiveCache no-store / noRefetchOnFirstTick / refetchOnVersionChange on the same harness. I ran the whole suite myself: python3 -m pytest test_graphweb_page_r160.py test_graphweb.py test_bin_help_smoke.py -q -> 80 passed, 1 skipped (the skip is the pre-existing node_writer --help), and the falsifier module alone -> 3 passed in 0.56 s. The near miss: a harness that only asserted boot() resolves would satisfy the words 3D-completes while never constructing a renderer — this one injects a renderer stub through the app.js:390 seam and counts _renderCalls >= 1 and scene.nodeMeshes length == canned node count, which is the part the words alone would miss. The harness also HONESTLY refuses to claim browser rendering (skip-not-fail when the pinned CDN bytes are unreachable) rather than faking a green. Deviations assessed: none from the standing rules; the node renders 2213 individual Points meshes on the real graph (one draw call each) instead of one merged cloud — a perf question the falsifier does not cover and nobody here can measure in a browser, recorded as a caveat rather than a defect. Verdict ACCEPTED as proved: evidence_runs is this node; the falsifier is red-then-green and reproducible.
<!-- THOUGHT:END -->

PARENT REVIEW a00-a4f37350: ACCEPTED proved (0.92). Falsifier is in-test and red-then-green (test_same_harness_fails_on_prefix_app demands failure on the reconstructed Float32ColorMaterial build). Independently ran the suite: 80 passed, 1 pre-existing skip. Real tmux probe on this box returns the agi-rc windows under -t. Caveat: 2213 individual Points meshes = one draw call per node on the real graph; falsifier does not cover browser frame cost and no browser exists here.
