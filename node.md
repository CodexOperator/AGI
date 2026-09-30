---
id: verdict:dg2mvp-w2cC
mint_id: 5bac712443e9499390db680ef959127a
type: verdict
parents:
  - experiment:dg2mvp-w2cC-check
  - hypothesis:gates-resolve-mint-ids-through-the-resolver
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-w2cC-check
scaffold_hash: 9ea8a98b402d73df
season: 2
title: "W2c C post-build (595b9c099): lean_disproved:65 -- build_type_index / nearest_vision / build_corpus resolve on the twin (0 diffs), but the WRITER gate gate_for_root (git-grep index, spawn_gate.py:1402) returns a plain dict: 4908/5078 twin verdicts differ, a mint-id parent reads unverified and a create refuses; cli._evidence_corpus drops the resolver (2106/2120 differ) -> fork"
town: core
verdict: inconclusive_lean_disproved:65
---
# verdict:dg2mvp-w2cC

Judged at HEAD cafbfbcd8 on the twin corpus (5078 live nodes) with 595b9c099's code.

CLAIM (1) "the 3 readers call the resolver": TRUE for the objects the tests build. `build_type_index`, `build_corpus` and `nearest_vision` route a mint id through the one `address_resolver` (0 of 5078 spawn verdicts differ, 0 of 300 nearest_vision; pre-build 4908 and 272 differ), and `read_mvp_map` keeps a 32-hex mint. One resolver only (links.py:487/502/527); the two strict-xfail rows are plain green and byte-identical to mine; test_level3, test_spawn_gate, test_evidence_gate, test_links green.

CLAIM (2) "each gate's verdict is identical for the twin": FALSE on the production paths.
- Writer gate: `spawn_gate.gate_for_root` (node_writer.py:735, the gate every create uses) returns a plain `dict` built off `links.frontmatter_rows`; the wrap is only on the fallback. On the mint twin 4908 of 5078 verdicts differ, exactly as before the build; a mint-id parent is `unverified: parent id(s) resolve to no node` and a brand-new create refuses. The falsifier ("a gate refuses a mint-id parent its twin passes") FIRES on this path, though the commit says "write_node's gate via gate_for_root".
- Evidence gate at verdict time: `cli._evidence_corpus` (cli.py:219) copies `build_corpus` into a plain set, so `cli.py done/score` lose the resolver (2106 of 2120 differ). metrics and post_wire keep it.
- Off-shape mints: `is_node_id_shaped` and `read_mvp_map` test a 32-hex shape while `resolve_mint` says no shape check; 10 legacy nodes carry an off-shape mint, and 10 of 2120 evidence verdicts differ on the twin for that reason. `read_mvp_map` also keeps a non-mvp mint its address twin drops (103 vs 101 kept).
- Index builds: one per resolver, none per item inside a call; but `nearest_vision` takes no resolver, so a per-node caller (viewport `_town_of`, snapshot-goals) rebuilds per call: 298 builds, 142 s vs 0.75 s over 300 nodes on a mint twin. 0 mint-id parents live today, so no cost now.

CEILING: 51 production lines added (38 non-blank) vs <= 30, links.py outside the file scope; disclosed override in the commit, not re-raised. Test lines 2 vs <= 30.

Verdict: the build makes the named test and the index builders right, but the writer and cli routes still refuse or miss a mint-id twin. Lean disproved on conjunct (2): the gap is one small fix (wrap gate_for_root's index, keep cli's corpus resolving), owned by no card; see corrective.md.
