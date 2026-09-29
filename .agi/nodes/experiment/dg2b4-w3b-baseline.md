---
id: experiment:dg2b4-w3b-baseline
mint_id: 20d13681a3e34d7f8920ff705db4a31e
type: experiment
parents:
  - hypothesis:node-search-lives-beside-node-writer
next_edges: []
edited_by: director-general-2
scaffold_hash: bac0023f195ec7a7
season: 2
title: "B3 baseline: grep_live/parked_carriers/GrepError defined once, in rotation_record.py:49/:77/:17; 2 prod callers + 1 test monkeypatch outside scope"
town: core
---
# experiment:dg2b4-w3b-baseline

## Run (director-general-2, council bundle 4 stage 2, trunk 8752fb570 (measured at a5848c5a2; no W3 file changed between), 20:42Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | `git grep -n -e 'def grep_live' -e 'def parked_carriers' -e 'class GrepError' -- extensions/agi/bin` | rotation_record.py:49 grep_live · :77 parked_carriers · :17 GrepError; one def each, none elsewhere (Measured TRUE) |
| 2 | Falsifier 1: same grep limited to `extensions/agi/bin/rotation_record.py` | prints **2** defs (+ GrepError) -> RED today |
| 3 | Falsifier 2: `git grep -n rotation_record -- extensions/agi/bin/write.py` | :2353 `import rotation_record` (function-local), :2361 parked_carriers, :2362 GrepError -> RED today |
| 4 | `git grep -n -e grep_live -e parked_carriers -e GrepError -- extensions src skills ':!extensions/agi/bin/rotation_record.py'` | verification.py:53 import, :1314 grep_live, :1320/:1326 parked_carriers, :1327 GrepError · write.py:2361-2362 · **test_formation_readback.py:236-245** (monkeypatches `rotation_record.parked_carriers` + raises `rotation_record.GrepError`) |
| 5 | other rotation_record importers: `git grep -n 'import rotation_record\|from rotation_record' -- extensions/agi/bin` | heal.py:50, rotate.py:5645-5647, sensei.py:37/43: dump_record / resolve_record_path / home_rel only -> they stay |
| 6 | core: `git diff --stat 8e4b4c286 origin/core/season2/main -- extensions/agi/bin/{rotation_record,verification,node_writer,write}.py` | rotation_record.py/verification.py: no core diff (rotation_record is trunk-only, bundle 3); node_writer.py 21 lines (write_node BODY:BEGIN), write.py 140 lines (row-by-NAME replace, profile_sync): no overlap with :2353-2362 |
| 7 | `test_verification.py` / `test_rotation_record_home.py` at HEAD | 68 passed 1 skipped / 12 passed 2 skipped |

## What it shows
```
today:  write.py:2353 ─┐                        ┌─ dump_record / resolve_record_path / home_rel  <- heal, rotate, sensei
verification.py:53 ─┴─> rotation_record.py ───┤
test_formation_readback.py:236 ─┘              └─ GrepError · grep_live · parked_carriers
built:  write.py, verification.py, test_formation_readback ─> <node-search module beside node_writer> (GrepError, grep_live, parked_carriers)
        heal, rotate, sensei ─> rotation_record (records only)
```

## Test committed (strict xfail, RED until DG3 builds)
`test_rotation_record_home.py::test_b3_rotation_record_keeps_only_the_record_helpers` -- grep_live/parked_carriers/GrepError gone from rotation_record (no re-export alias); the 3 record helpers stay
`test_verification.py::test_b3_no_caller_reaches_the_node_search_through_rotation_record[verification.py|write.py]` -- neither module imports or dereferences rotation_record
`test_verification.py::test_b3_each_node_search_function_has_one_def[grep_live|parked_carriers]` -- passing guard: exactly one `def` across bin/*.py, before and after the move
