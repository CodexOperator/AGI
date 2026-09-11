---
id: experiment:a00-789ae446-7a914b
mint_id: ed3ce94ee21e4ba39f6c8693c0300073
type: experiment
parents:
  - hypothesis:l4-the-graph-as-a-golden-3d-web-in-two-layers
next_edges: []
confidence: 0.9
edited_by: a00-c42731c0
evidence_runs:
  - experiment:a00-789ae446-7a914b
loop: hypothesis:l4-the-graph-as-a-golden-3d-web-in-two-layers@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4eb7a5a44e8fd7ad
season: 2
title: A00 789ae446 7a914b
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-789ae446-7a914b

## Experiment

KID 3 of 3 — the test deliverable under hypothesis:l4-the-graph-as-a-golden-3d-web-in-two-layers. Owned ONLY `extensions/agi/tests/test_graphweb.py` (new, 11 fixture-only tests) against the graphweb.py server+layout layer (KID 1) and the web page (KID 2). No changes to graphweb.py / app.js / index.html.

Command: `python3 -m pytest extensions/agi/tests/test_graphweb.py -q` → **11 passed in 0.73 s**.

Every test builds a throwaway tmp `.agi` (goal:g17 root + a goal:g17child descendant + one outside node + `.geometry/seats.md` two-row registry + one fake worktree with a MODIFIED node file + a config.json pointing stream_card_png at an absent file). tmux / pid (os.kill) / git are all monkeypatched in-process:

1. **test_two_layer_split** — root goal:g17 at layers {0,1}; the g17 descendant (the target falsifier) is layer 1 and NOT layer 0; an outside node is layer 0 only; one synthetic `seat:<name>` node per config:seats row at layer 1 each with exactly one `seat` edge to goal:g17.
2. **test_working_on_from_fake_worktree** — git status --porcelain monkeypatched to report `.agi/nodes/goal/g17child.md` modified in wt1 → seat sanctuary-director working_on == ["goal:g17child"]; the dead worktree wt2 never fires git (working_on stays []); absent tmux raises and collapses to empty set; dead/none pid → False, never a traceback.
3. **test_worktree_modified_ids_dead_worktree_no_git** — proves the git read is truly UNFIRED for a dead worktree (fired list stays empty).
4. **test_active_requires_window_and_live_pid / test_active_false_when_pid_dead** — active=true only when pid-alive AND tmux window present; absent window or dead pid → false.
5. **test_palette_fallback_when_png_absent / test_palette_sampled_from_png / test_palette_fallback_on_non_png** — exact fallback {ground:#0f1216, gold:#a48c5a}; a real 4x4 RGB PNG (dark bg + one warm #a48c5a pixel) samples to the deterministic hexes; non-png bytes fail open to the fallback.
6. **test_server_answers_core_routes** — real ThreadingHTTPServer on port 0 against the tmp .agi: GET / → text/html, /graph.json → application/json (and the two-layer child → [1] on the wire), /live.json → application/json.
7. **test_graphweb_bin_help_exits_zero** — `graphweb.py -h` exits 0 with non-empty stdout (named to not collide with the parametrised test_bin_help_smoke.py).
8. **test_cache_returns_same_object_until_mtime_changes** — cached_build_graph returns the SAME object on warm reads, REBUILDS (new object) when a node file mtime changes, then is stable again.

## Evidence

11 passed in 0.73 s (full run, no skips). No test touches a live tmux pane, spawns real git against the repo, or reads/writes the real `.agi` — the farthest reach is `os.kill` on pid 999999999 (ProcessLookupError handled) and a throwaway `subprocess.run([python, bin/graphweb.py, -h])` for the help smoke.

FALSIFIER self-check: dropping the two-layer assertion (g17child NOT in layer 0) would let a regression pass, so it is the pivot the round is named for; and the earlier defect was real — the first fixture placed the fake worktree under the PROJECT root but graphweb resolves `worktree` relative to graph_root, so the git mapping read a non-existent file and produced [] until the fixture path was corrected. That path-resolution behaviour is worth reporting: `_worktree_modified_ids` treats a relative `worktree` as relative to the `.agi` dir, not the source root, and an unaware test author trips on it.

## Agent Notes
11 fixture-only graphweb tests all pass; two-layer split, working_on, active, palette, server content-types, help smoke, cache contract all proven

PARENT REVIEW (a00-c42731c0, L4.235), accepted as kid 3 of 3. Independently verified: I ran python3 -m pytest extensions/agi/tests/test_graphweb.py -q myself and got 11 passed in 0.68 s; the file is 17272 bytes and its names match the eight required behaviours; parents link resolves; verdict proved with a self-cited evidence_runs entry, which is legal for an experiment node. The kid reported a real finding worth keeping: _worktree_modified_ids resolves a RELATIVE worktree path against graph_root (.agi), not the source root, so a seat row carrying a relative worktree silently yields working_on=[]. That is exactly the class of silent-empty the target node feared; it should be checked against the real config:seats rows before the dashboard is trusted. CAVEAT accepted and not fixed here: the tests pin graphweb contract on FIXTURES; the live three.js CDN path in a real browser remains unverified, which is why kid 2 stayed at inconclusive_lean_proved:80. Round closed at the target node ceiling of three kids.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW EDIT (a00-c42731c0, L4.235). No body claim changed; the parent added its review. WHAT THE INSTRUCTION SAID: review every node a kid writes, read the ARTIFACT not the report, and cite a run rather than yourself. WHAT THE MACHINE ACTUALLY DOES: I executed the artifact command (python3 -m pytest extensions/agi/tests/test_graphweb.py -q) and read the result 11 passed in 0.68 s from my own invocation, not from the node, and I read the relative-worktree resolution in the kid body against graphweb.py:629 area functions rather than accepting the claim. NEAR MISS: the kid wrote verdict proved; a parent reviewing only the DONE line would have accepted it and missed both that the 3D path is still unverified and that a relative worktree silently empties working_on, which is a load-bearing surface for the owners seat-to-node edges. I kept proved because the deliverable IS the test file and it passes, and recorded the two caveats instead of demoting an honest claim. Evidence linked: experiment:a00-789ae446-7a914b.
<!-- THOUGHT:END -->
