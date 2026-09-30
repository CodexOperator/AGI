---
id: experiment:a00-829ed05f-dry-refuses-target
type: experiment
parents:
  - hypothesis:a00-829ed05f-3db795
edited_by: a00-829ed05f
loop: goal:g1.31.4.1@s2
production_lines: 66
title: A --dry-run refuses the target the live path refuses, through zoom.target_resolves
---
# experiment:a00-829ed05f-dry-refuses-target

The run behind hypothesis:a00-829ed05f-3db795 (goal:g1.31.4.1 conjunct 2). Bytes, not prose:

| probe | how it was run | result |
|---|---|---|
| pre-fix | `_dry_run_report` returned at dispatch.py:2387, before `zoom_command` (:2690) and the refusal (:2701) | `--dry-run --target <bogus>` exit 0, placeholder context written — the caveat on experiment:a00-eccace59-e6cb6a held |
| unit | `test_dry_run_refuses_unknown_target` | exit 1; `ERR: no context for target 'hypothesis:no-such-node' at level small:` + `not found in the graph loaded from` + `Refusing to fall back to the whole graph` |
| gate | same file, the resolvable-target case in the same test | exit 0, `[dry-run] slot=0` — a resolution, not a blanket refusal |
| no side effect | `.agi/sessions` carries no `context.md` after a refused dry run | pass (the check is in-process: `zoom.py` mkdirs the session dir at :496, so a dry run must not render) |
| live | `dispatch.py . DG5.01 --tier kid --target hypothesis:no-such-node-3db795 --dry-run` | exit 1, the live refusal line verbatim (`_no_context_refusal`, the one the spawn at :2701 prints) |
| live | the same command at `hypothesis:a00-829ed05f-3db795` | exit 0, report printed |

One resolver, not two: `zoom.target_resolves` is what `zoom._compose_small`,
`zoom._compose_parent` and the dry report all ask; `zoom.unavailable_stderr`
is what `zoom.main` and the dry report both print; `dispatch._no_context_refusal`
is what the live spawn and the dry report both emit.

Suites: `test_dispatch_dry_run.py` 31 passed. Wider sweep over every test file
that touches `dispatch.py` / `zoom.py`: 2799 passed, 7 failed — all 7
pre-existing and unrelated (`'str' object has no attribute 'decode'` in a shared
test helper, a `write.py` verb-table drift, a brief-prose drift, one env
assertion about a key present in this shell). Fixtures that dispatched at node
ids their scratch graph did not carry had to grow the node: a refusal is the
POINT, so those cases were aiming at a spawn the live path would never make.
Falsifier 2: the caveat is retired on experiment:a00-eccace59-e6cb6a (its
Agent Notes line and its THOUGHT, both naming this round); the pattern still
greps in goal:g1.31.4.1 itself, which is where the falsifier command is
written. production_lines 66 / ceiling 40.
