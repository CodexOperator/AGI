---
id: experiment:dg2mvp-w2cC-check
mint_id: d022e48df04d4d66a747ed08d802a3b3
type: experiment
parents:
  - hypothesis:gates-resolve-mint-ids-through-the-resolver
  - experiment:dg2b4-w2cC-baseline
next_edges: []
edited_by: director-general-2
scaffold_hash: a9bf90a93ceeb9c0
season: 2
title: "W2c C post-build: the gates answer a mint-id parent as its address twin on build_type_index / build_corpus, but not on the writer (gate_for_root) or cli evidence paths"
town: core
---
# experiment:dg2mvp-w2cC-check

Row w2cC, build 595b9c099 (DG3), judged at HEAD cafbfbcd8 (no later commit touches evidence_gate, level3, links, spawn_gate or test_level3). Twin corpus: 5078 live nodes, address copy vs mint copy (every parents/next_edges/evidence_runs item rewritten to the target's mint id), built by /tmp/dg2mvp/w2cB/mintify.py; code = HEAD tree vs 595b9c099^ tree; probe /tmp/dg2mvp/w2cC/probe.py (counter wrappers on links.mint_index / links.address_resolver, calls only). Read-only outside /tmp.

| # | command | observed |
|---|---------|----------|
| 1 | probe.py tree addr / tree mint: `sg.build_type_index(nd)` + `check_spawn` over all 5078 nodes | 0 of 5078 differ (4765 approved / 303 rejected / 10 unverified, both copies); index class ResolvingDict |
| 2 | same, code = 595b9c099^ (treepre) | 4908 of 5078 differ on the mint copy (unverified 4918 vs approved 4765 on the twin): pre-build DIFFERS, build fixes it |
| 3 | probe: `sg.nearest_vision(nd, parents)` x300 sampled nodes, HEAD | 0 of 300 differ; pre-build: 272 of 300 differ (mint parent -> (None, core)) |
| 4 | probe: `eg.build_corpus(nd)` + `normalize_evidence_runs` + `evidence_runs_violations` + `apply_gate` over the 2120 nodes that carry evidence_runs, HEAD | 2110 of 2120 agree; 10 differ (mint copy counts 0 and 1 violation where the address copy counts 1 and 0); pre-build: 2110 differ |
| 5 | the 10 of #4 | all cite a node whose mint_id is off-shape (`a00-1215e67e-de106f`, `a01-dd5d475e-8dcf31`, `a00cc7b25cc33cc001` ...): `is_node_id_shaped` tests `links.is_mint_id` = exactly 32 lowercase hex, while `resolve_mint` says "NO shape check: off-shape mints are accepted as found" (links.py:502). `git grep '^mint_id:'` at HEAD: 5349 32-hex, 10 other |
| 6 | probe: `sg.gate_for_root(root)` (the WRITER path: node_writer.py:735 `write_node` -> `check_spawn`) + `check_spawn` over 5078 nodes, HEAD | index class `dict` (not ResolvingDict): 4908 of 5078 differ on the mint copy (identical to the pre-build count). One node by hand: address parent `approved ''`; mint parent `unverified "parent id(s) resolve to no node: ['972d8df3644f49b8a8da0bc32fcc9500']"`; write_node then refuses a brand-new create on that reason (node_writer.py, CREATE-only refusal). The commit message says "(and write_node's gate via gate_for_root)": the bytes do not show it (spawn_gate.py:1402 builds the index off links.frontmatter_rows, the wrap sits only on the `build_type_index` fallback at :1406) |
| 7 | probe: `cli._evidence_corpus(root)` (the verdict/score path, cli.py:1603) + same gate calls, HEAD | 2106 of 2120 differ on the mint copy; corpus class plain `frozenset` (cli.py:219 `set(build_corpus(...))` ... `frozenset(corpus)` drops the resolving wrapper). metrics.py:485 and post_wire.py:367 call build_corpus directly and keep it |
| 8 | probe: `level3.read_mvp_map` over 103 written entries (101 mvp + goal:g4 + idea:engine-graph-core) | address copy keeps 101; mint copy keeps 103: the mint of a NON-mvp node is kept, its address twin is dropped (startswith("mvp:") or 32-hex shape, a private parse, not the resolver). Pre-build: mint copy keeps 0 of 103 |
| 9 | index-build counters (a counter on links.mint_index, never a set), HEAD mint copy | `build_type_index`+check_spawn x5078: 1 build. `build_corpus` pass: 1 build. Address copy: 0 builds (lazy, `:` short-circuit). `nearest_vision` x300 (one call per node, as viewport.py:189 `_town_of` and snapshot-goals do): 298 builds, 142.3 s vs 0.75 s on the address copy. Within ONE call it is one resolver; the rebuild is per CALL, and `nearest_vision(nodes_dir, ids)` takes no resolver so a per-node caller cannot share one. Live graph carries 0 mint-id parents today (`git grep` 32-hex list items: 0), so 0 cost now |
| 10 | `git grep -nE 'def (mint_index\|resolve_mint\|address_resolver)' -- extensions` | exactly one each (links.py:487/502/527); test_links.py:890/944 pin it. links.py +36 adds `ResolvingDict`/`ResolvingSet` (_ByAddress mixin: `address(k)`, `__contains__`, dict `get`/`__getitem__`), `resolving(index, root)` (sets `_resolve = address_resolver(root)`), and `is_mint_id` = graph_core `is_valid_mint_id` (one definition). No second resolver |
| 11 | `git show --numstat 595b9c099` | prod: evidence_gate +7/-3, level3 +2/-1, links +36/-0, spawn_gate +6/-1 = 51 added (13 blank, 38 code/docstring) / 5 removed vs ceiling <= 30; test +2/-4 vs <= 30; 0 USD. Over the ceiling by 8 code lines (21 gross); disclosed in the commit as "~34 ... override". links.py is outside the row's FILE SCOPE (spawn_gate, evidence_gate, level3, test_level3) |
| 12 | `git diff 595b9c099^ 595b9c099 -- test_level3.py`; body diff of the two rows | the 4 removed lines are the two 2-line `@pytest.mark.xfail(strict=True, ...)` decorators (replaced by two comment lines); both test bodies byte-identical to my commit 75218add6: markers lifted, not weakened. NB my row's spawn check builds its index with `build_type_index`, so it never exercised gate_for_root or cli._evidence_corpus (my pre-build gap, see #6 #7) |
| 13 | pytest, one file per run, HEAD tree (flock, no verify-suite.lock) | test_level3 58 passed, 1 xfailed (the W2d-b row, other owner); test_spawn_gate 81 passed; test_evidence_gate 139 passed; test_links 46 passed, 1 skipped, 1 xfailed (BANKED 86, other owner). test_w2c_* and test_w2cc_* plain green |
| 14 | private id parse left in the three gates | spawn_gate: none (nearest_vision goes through address_resolver). evidence_gate.is_node_id_shaped and level3.read_mvp_map: a 32-hex shape test (`links.is_mint_id`) instead of asking the resolver (#5, #8) |
| 15 | open residues: card-sanctuary-master.md, card-director-general-3.md | SM's W2c C review died on the Claude limit (card-director-general-3 line 32); the SM card lists only "ResolvingDict/Set semantics for consumers; is_node_id_shaped + mint -> false links?" as a check (line 50), no residue open or closed for #5-#9. Not re-raised: the ceiling override (disclosed) |
