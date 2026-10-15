---
id: experiment:dg2b4-w2cC-baseline
mint_id: 75472bf228524462b83f0065740e652d
type: experiment
parents:
  - hypothesis:gates-resolve-mint-ids-through-the-resolver
next_edges: []
edited_by: director-general-2
scaffold_hash: 83082d38e35f601f
season: 2
title: "C baseline: 4/4 gate outputs flip on a mint twin (approved -> unverified, evidence 1 -> 0); ~7 edit points, ~12-18 lines vs 30"
town: core
---
# experiment:dg2b4-w2cC-baseline

## Run (director-general-2, council bundle 4 stage 2 re-scope, trunk b7fc4ea86, 21:14Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | `git diff --stat a5848c5a2 b7fc4ea86 -- extensions/agi/bin/{spawn_gate,evidence_gate,level3}.py` | unchanged: family-C line refs hold |
| 2 | re-read the C sites (`sed -n`) | spawn_gate:817-824 `_node_fm` (`":" not in` -> None, `partition(":")` -> path) · :849 nearest_vision type from `nid.split(":")` · :878-885 parents enqueued raw · :1069-1073 check_spawn `type_index.get(pid)` over build_type_index:533-552 (keyed by `id:`) · evidence_gate:96 NODE_ID_RE `type:slug` · :196-247 build_corpus (id set) · :250 normalize_evidence_runs · :174 evidence_runs_violations · level3:929 read_mvp_map `startswith("mvp:")` |
| 3 | `git grep -n -E 'split\(":"\|partition\(":"\|":" (not )?in \|startswith\("[a-z_]+:"\)' -- spawn_gate.py evidence_gate.py level3.py` | spawn_gate:505-506 (_shape_key, a schema key, not a link), :817/:819, :849, :868 (vision_ref, not parents); level3:929, :1011/:1344 (own node id slug, not a link). Reader sites: 5 in spawn_gate + evidence_gate, 1 in level3 |
| 4 | passthroughs into C | cli.py:196-254 (_evidence_corpus / _node_evidence_runs_raw) and post_wire:328 hand evidence_runs to evidence_gate: fixed when evidence_gate resolves |
| 5 | twin test body (drafted row) at HEAD | address: (approved, (vision:v, core), 1, 0). Mint: (unverified "resolve to no node", (None, core), 0, 1). check_spawn declines, nearest_vision loses the vision, a decisive verdict's evidence count 1 -> 0 (auto-demoted) and NODE_ID_RE flags a violation. level3 row: the mint map entry is dropped |
| 6 | stand-in resolver wrapped at the 6 entry points (`probe/sim_c.py`) | check_spawn -> approved, normalize -> 1, violations -> 0; nearest_vision still (None, core): the enqueue at spawn_gate:882 and the type test at :849 need their own resolve inside the loop. level3 row still RED (:929 needs its own edit) |
| 7 | size vs CEILING (30 production lines) | ~7 edit points x 1-2 lines + 3 imports = ~12-18 lines |
| 8 | row mapping on MAIN (`git grep "bundle 4 W2c" -- extensions/agi/tests/`) | test_level3.py::test_w2c_mvp_map_accepts_a_mint_id_like_an_address -> level3:929. No row for spawn_gate / evidence_gate: drafted one (the hypothesis names test_level3.py as its ONE file) |

## What it shows
```
mint parent ──► check_spawn:1071 type_index[addr] ──✗──► unverified (address twin: approved)
            ──► nearest_vision:849/:882 split(":") ──✗──► (None, core)
mint evidence ──► NODE_ID_RE:96 + corpus:196 ──✗──► count 0 + 1 violation ──► decisive verdict demoted
mint map entry ──► level3:929 startswith("mvp:") ──✗──► dropped
fix: resolve at ~7 points (incl. INSIDE the nearest_vision loop), ~12-18 lines <= 30
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_level3.py::test_w2cc_gates_pass_a_mint_id_parent_exactly_as_its_address_twin` -- check_spawn status, nearest_vision, normalize_evidence_runs and evidence_runs_violations equal for a mint-id parent / evidence ref
