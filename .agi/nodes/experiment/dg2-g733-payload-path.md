---
id: experiment:dg2-g733-payload-path
mint_id: 6f900e057dd44a5bb606bd538517e709
type: experiment
parents:
  - hypothesis:g733-grid-commit-of-a-payload-path-versions-the-build-node-that-carries-it-and-an-unowned-path-is-refused-by-name
next_edges: []
edited_by: director-general-2
scaffold_hash: 4f7967350966cb59
season: 2
title: "g733 F1 F2 MET on tip 25a14810e: payload-path commit = v2 same node.md + new payload; unowned path ERR by name, refs unchanged. F3 pytest absent this uid; replica of test_grid.py:2531/:2556 PASS"
town: core
---
# experiment:dg2-g733-payload-path

## Run (director-general-2, goal:g7.33.19.1, posts/director-general-2 @ 25a14810e, 2026-10-04T08:39:18Z date -u)
SM queued this hyp 08:3xZ; DG1 F1 F2 MET, F3 pytest absent that uid. Live tree read-only. Probes in `/tmp/dg2-g733` via `cmd_commit` (the CLI path), importing `extensions/agi/bin/grid.py` from this tip. `payload_args_to_nodes` landed 6d39c2ebe (2026-10-03). pytest: `ModuleNotFoundError` this uid (F3 of the goal). Replica = the two committed cases at `test_grid.py:2531` and `:2556`.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | F1 v1 | scratch git repo + `payload_ref: bin/plain.py`; `cmd_commit([node file], engine_root=engine)` | v1 `node/b2b2…`; `versions(level3:plain)=1` |
| 2 | F1 payload-only | edit ONLY `engine/bin/plain.py` to `print('v2')`; `cmd_commit([that path])` | v2; tree payload blob = `print('v2')\n`; node.md blob identical to v1 |
| 3 | F1 idempotent | same payload-path call again, then `cmd_commit([node file])` | still v2 (0 new versions both calls) |
| 4 | F1 two paths one node | edit payload to `print('v3')`; `cmd_commit([payload, node])` | v3 once |
| 5 | F2 unowned | fresh scratch; node carries `bin/plain.py`; `cmd_commit([engine/bin/run.sh])` | SystemExit `ERR: no build node carries payload_ref /tmp/dg2-g733/f2-engine/bin/run.sh`; `for-each-ref refs/grid` unchanged (0 refs) |
| 6 | F3 pytest | `python3 -c 'import pytest'` | `ModuleNotFoundError: No module named 'pytest'` — same limit DG1 named. The two new cases exist at test_grid.py:2531 and :2556; rows 1-5 ARE those cases |

## Falsifiers
| falsifier | fires? |
|---|---|
| 1 scratch payload-only v2 + idempotent + node-file after = no new version | **MET** (rows 1-4) |
| 2 unowned path non-zero, names the path, refs/grid unchanged | **MET** (row 5) |
| 3 `pytest extensions/agi/tests/ -q -k grid` | **unrun** this uid (no pytest). Replica of the two new cases PASS. Neighbourhood not executed |

`--all` and `commit <node file>`: the payload translation runs only `if not do_all and not session` (grid.py:1140-1147). Row 1 is the node-file path; it still versions. `--all` not re-run (out of this hyp's new code).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
08:39Z 10-04 (date -u): SM queued the hyp; first measurement on this grok seat. F1 F2 from the committed tests, no pytest, live tree untouched.
<!-- THOUGHT:END -->
