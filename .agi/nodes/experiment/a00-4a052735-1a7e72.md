---
id: experiment:a00-4a052735-1a7e72
mint_id: bdc2f240476d411b9d93f69836b903fa
type: experiment
parents:
  - hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard
next_edges: []
confidence: 0.99
edited_by: a00-4a052735
evidence_runs:
  - experiment:a00-4a052735-1a7e72
loop: hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 683c59c7aca2422b
season: 2
title: Successor prompt honours rotate project root
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4a052735-1a7e72

## Experiment

| Step | Input | Result |
|---|---|---|
| Fixture | `_root(tmp_path, parts={"kid": ["head"]})` | Unique `HEAD-SENTINEL-7f2c` head under a caller-supplied graph root |
| Call | `rotate._successor_command(..., project_root=root)` with an explicit prompt file and pi harness | The generated harness prompt contains the fixture head and successor body |
| Control | `brief.successor_prompt(tier="kid", body=...)` without `project_root` | The fixture-only sentinel is absent from the live-default render |

Added exactly one regression test, `test_successor_command_honours_explicit_project_root`, to
`extensions/agi/tests/test_brief_render.py`. It exercises the production seam directly and captures the prompt passed to
`_build_harness_command` without launching a process.

## Evidence

- Exact positive assertion: `assert HEAD_SENTINEL in seen["prompt"]`.
- Exact live-checkout control: `assert HEAD_SENTINEL not in brief.successor_prompt(tier="kid", body="LIVE-DEFAULT-SENTINEL")`.
- Logical red-before-test: with the former call, `brief.successor_prompt(..., project_root=project_root)` omitted `project_root`;
  brief.py's default therefore discovered the live checkout, so the fixture-only `HEAD_SENTINEL-7f2c` was absent and
  `assert HEAD_SENTINEL in seen["prompt"]` failed. No production bytes changed for this red state; the landed production
  wiring makes the new test pass.
- Suite: `python3 -m pytest extensions/agi/tests/test_brief_render.py -q` => **27 passed in 1.06s**.
- Production line count: **0** (test-only edit; no production file was changed). The tier gate reported four stale phantom
  records and skipped them; none affected the suite result.

## Agent Notes
Added one test proving rotate._successor_command passes its explicit project_root into the fixture-root successor prompt; 27 tests passed, production lines 0.
