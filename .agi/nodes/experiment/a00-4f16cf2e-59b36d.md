---
id: experiment:a00-4f16cf2e-59b36d
mint_id: 2c4481b074974320afccd608f3f37fb5
type: experiment
parents:
  - hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard
next_edges: []
confidence: 0.99
edited_by: a00-4f16cf2e
evidence_runs:
  - experiment:a00-4f16cf2e-59b36d
loop: hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard@s2
model: stealth/space-bunny-alpha
production_lines: 5
profile: balanced
role: kid
scaffold_hash: 675c941705ebe0d8
season: 2
title: Thread project root through default profile and rotation fallback
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4f16cf2e-59b36d

## Experiment

Implemented EF.110's two caller-root leaks while leaving EF.111/config precedence untouched:

| Seam | Before | After | Probe |
|---|---|---|---|
| `brief.assemble` default-profile resolution | `_effective_profile(profile=None)` read the live graph | passes `project_root=project_root` | two roots select `survival` vs `full` with the sentinel profile kwarg omitted |
| `rotate._assembled_successor_command` legacy fallback | `brief.assemble(...)` omitted the root | passes `project_root=project_root` | forced `brief.RenderError`; captured fallback kwargs equal the supplied root |

Production diff: two call-site edits only. `git diff --numstat` reported `1 1` for `brief.py` and `2 1` for `rotate.py` (5 changed production lines total, under the 40-line ceiling).

## Evidence

```text
$ python3 -m pytest extensions/agi/tests/test_brief_render.py -q
..............................                                           [100%]
30 passed in 0.81s
```

The two added falsifiers are `test_default_profile_resolution_follows_project_root` and `test_rotate_assemble_fallback_forwards_project_root`. The existing 28 tests remained green.

## Agent Notes
Threaded project_root through brief default-profile resolution and rotate's assemble fallback; two new falsifiers pass with 30/30 test_brief_render tests.
