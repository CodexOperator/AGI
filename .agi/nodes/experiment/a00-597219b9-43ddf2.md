---
id: experiment:a00-597219b9-43ddf2
mint_id: b9da9e4c4ac14098a067b4471fdc1b87
type: experiment
parents:
  - hypothesis:l2-dispatch-restart-twin-node
next_edges: []
confidence: 0.85
edited_by: ubuntu
evidence_runs:
  - experiment:a00-597219b9-43ddf2
scaffold_hash: fbfe94e767e96475
season: 1
title: A00 597219b9 43ddf2
verdict: proved
---
# experiment:a00-597219b9-43ddf2

## Experiment

Tested hypothesis:l2-dispatch-restart-twin-node — two independent fixes with suite-wide tests.

**Fix A** — dispatch.py `_reap_one()` built scaffold info from agent_record's existing `node_id` and passed it to `adapter.restart()` via the `scaffold=` parameter. Previously scaffold=None meant the restarted kid got a generic brief and created a new node (twin). Now the existing node_id, parent, node_type, and path are passed through so the restarted agent fills the original scaffold.

**Fix B** — cli.py `_append_verdict_to_node()` now accepts an `evidence_runs` parameter and writes it into the node's frontmatter at signal time via `set_fm["evidence_runs"]`. Previously evidence_runs was only stored in agent.json; now it persists in the node file and survives the grid-commit re-check (`enforce_on_disk`).

**Test suite**: 3 new integration tests added to `test_real_adapter_restart.py`:
- `test_restart_reuses_existing_scaffolded_node_twin_fix` — mocks `adapter.restart()` to capture scaffold param, verifies scaffold points to existing node id (not None)
- `test_evidence_runs_persisted_in_node_frontmatter` — runs `cli.py cmd_done()` end-to-end with `--evidence-runs` citing self, verifies evidence_runs appears in frontmatter YAML
- `test_evidence_runs_frontmatter_survives_enforce_on_disk` — writes a proved verdict + evidence_runs via `update_node`, runs `enforce_on_disk(dry_run=True)`, verifies NO demotion

**Test results**: 1660 passed, 1 pre-existing fail (test_minted_node_stamps_loop_model_profile_from_env), 9 skipped. All new tests pass.

## Evidence

Test output:
```
$ python3 -m pytest extensions/agi/tests/test_real_adapter_restart.py -v --tb=short
9 passed in 0.52s

$ python3 -m pytest extensions/agi/tests/ -q --tb=short
1660 passed, 1 failed, 9 skipped (1 fail pre-existing)
```

**Files changed:**
- `extensions/agi/bin/dispatch.py` — Fix A: build + pass scaffold_info to restart
- `extensions/agi/bin/cli.py` — Fix B: add evidence_runs parameter + write to node frontmatter
- `extensions/agi/tests/test_real_adapter_restart.py` — 3 new tests

## Agent Notes
Fix A: dispatch.py _reap_one() now builds scaffold_info from agent_record node_id and passes to restart (tested via captured mock). Fix B: cli.py _append_verdict_to_node() writes evidence_runs into node frontmatter (tested end-to-end with cmd_done and enforce_on_disk). 3 new integration tests pass. Full suite: 1660 pass, 1 pre-existing fail.

Parent review a00-d538de06 L2.13: ACCEPTED as proved. Re-verified both fixes end-to-end myself, not just the kid report: Fix A chain _reap_one -> adapter.restart(scaffold=) -> build_command -> brief.assemble emits the SCAFFOLDED NODE FILE segment with the existing node id and a done line pinned to it, so a restarted kid fills the original node instead of minting a twin. Fix B chain cmd_done -> _append_verdict_to_node(evidence_runs=) writes the cited ids into frontmatter before any gate re-check; the enforce_on_disk test shows no demotion. Re-ran the 9 restart tests (pass) and the full suite: 1660 passed, 1 failed (test_minted_node_stamps_loop_model_profile_from_env, pre-existing and unrelated to these diffs), 9 skipped. Parent link resolves, no orphans, self-cited evidence is legitimate for an experiment node. The hypothesis source note file .agi/autoresearch.ideas.md is already deleted.
