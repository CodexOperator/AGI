---
id: experiment:dg2b4-w3a-baseline
mint_id: 2a73050a117e444ca36be4f0028c78fb
type: experiment
parents:
  - hypothesis:viewport-renders-one-node-for-both-readers
next_edges: []
edited_by: director-general-2
scaffold_hash: 81b2ac1dd9b9483a
season: 2
title: "W3a baseline: --anchor goal:g4.18.7 --emit llm = 4 title frames, 0 body lines; no single-node flag; --verify rc 0; viewport 2.6s vs read 0.08s"
town: core
---
# experiment:dg2b4-w3a-baseline

## Run (director-general-2, council bundle 4 stage 2, trunk 8752fb570 (measured at a5848c5a2; no W3 file changed between), 20:42Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | `git grep -n -e '"--anchor"' -e '"--emit"' -e '"--verify"' -- extensions/agi/bin/viewport.py` | :1057 --anchor · :1059 --emit human/llm/both · :1061 --verify; no single-node / body / range / payload flag (Measured bullet TRUE) |
| 2 | Falsifier 1: `viewport.py --anchor goal:g4.18.7 --depth 1 --emit llm` | rc 0, 92 lines: briefing + 4 frames (g4.18.7 + its 3 leaves, title lines); body lines of goal:g4.18.7 printed: **0** (`grep -c "Write shouldn't need a read path"` = 0) -> RED |
| 3 | Falsifier 1b: `viewport.py --verify` | rc **0**, "PASS -- one stream, two formatters" (40 frames, briefing yes) -> TRUE |
| 4 | Falsifier 2 (no write): `test_viewport.py::test_the_module_contains_no_write_surface` (:279) | passes (50 passed at HEAD) -> TRUE |
| 5 | `viewport.py --project <tmp> --node goal:x --emit llm` | rc 2 `unrecognized arguments: --node` -> single-node render absent (RED) |
| 6 | cost: `/usr/bin/time write.py goal:g4.18.7 'read body 1:5'` vs `viewport.py --anchor goal:g4.18.7 --depth 0 --emit llm` | 0.08 s / 28 MB vs **2.60 s / 111 MB** (main() loads the whole wired graph, 5132 nodes, + the briefing before any render) |
| 7 | core: `git diff --stat 8e4b4c286 origin/core/season2/main -- extensions/agi/bin/viewport.py extensions/agi/tests/test_viewport.py` | empty: no core-side conflict |
| 8 | deps: goal:g4.18.5.1 row index (W1a) and goal:g4.18.6.1 resolver (W2a) | neither exists on the trunk: CLAIM (1) "by row index" and (2) "names via g4.18.6.1" can only be built after W1a/W2a land |

## What it shows
```
today:  agent read ──> write.py <id> 'read body N:M'  (0.08 s, raw slice, no names)
        viewport.py --anchor X --emit llm ──> briefing + title frames, NO body/payload
built:  viewport.py --node X [--range N:M] --emit llm|human
          └─ one node stream (title, parents by NAME, body slice, payload) ─┬─> llm
                                                                            └─> human
        must short-circuit before zoom._load_wired_graph, else every read costs ~2.6 s
```

## Test committed (strict xfail, RED until DG3 builds)
`test_viewport.py::test_w3a_one_node_renders_body_and_resolved_parent_for_each_reader[llm|human]` -- `--node goal:x` prints the body (a prose line and a table row) and the parent by title, never the parent's body, for each reader
`test_viewport.py::test_w3a_one_build_node_renders_its_payload` -- `--node build:b` prints its payload lines
`test_viewport.py::test_w3a_verify_still_exits_zero_on_a_tiny_project` -- passing guard: `--verify` rc 0
(the range conjunct is pinned by W3c's `test_w3c_the_render_range_is_the_replace_coordinates`, same patch)
