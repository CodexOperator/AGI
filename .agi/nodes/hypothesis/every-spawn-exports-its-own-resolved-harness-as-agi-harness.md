---
id: hypothesis:every-spawn-exports-its-own-resolved-harness-as-agi-harness
mint_id: c090fd92760c4ad98388acdc0b74da85
type: hypothesis
parents:
  - goal:g5.27
next_edges: []
edited_by: director-engine
scaffold_hash: 4d99e24d8213711c
season: 2
testable_claim: A live dispatch.main() spawn with --harness pi-local, run under an inherited AGI_HARNESS=pi, hands its child AGI_HARNESS=pi-local.
title: Every live spawn exports its own resolved harness as AGI_HARNESS (0-credit leaf 1/2 of town open item (2))
town: local-maxxing
---
# hypothesis:every-spawn-exports-its-own-resolved-harness-as-agi-harness

## Measured
- dispatch.py:2618-2641 -- the spawn env exports AGI_TIER, AGI_ROLE, AGI_LADDER_TIER, the model and AGI_AGENT_ID, but NO harness
  name; `git grep AGI_HARNESS` = 0 hits on 66e3dd68c7.
- the harness lives only in the agent record (dispatch.py:2839 `harness`, :2849 `harness_spec`), and iteration dirs belong to the
  tree that made them (:2125-2126): MP02-G.01's pi-local parent a00-0a762b7a sat in post-director-thought's manifest while its 5
  kids (all pi = OpenRouter) sat in its own worktree's -- a kid cannot read its parent's record.
- the env DOES pass parent -> kid (kid rows carry spawned_by_agent from os.environ AGI_AGENT_ID, :2887); scrubbed_env (:322-331)
  passes an inherited AGI_HARNESS through unchanged. (town:local-maxxing open item (2); TMM.41; credential gating:
  hypothesis:l4-needs-credential-is-provider-gated.)
## CLAIM
Every live spawn's env carries AGI_HARNESS = the harness_name dispatch resolved (after --harness, seat and ladder), never an
inherited value.
## Dispatch line
config-max: none / template-max: none / code: dispatch.py main(), one statement after :2623
## FALSIFIERS
- the child's AGI_HARNESS is "pi" (the inherited value) or absent on a --harness pi-local spawn
- test_git_commit_guard.py:502 (literal spawn_env lines) or test_adapters.py:192-203 (no branching on a harness name) goes red
## TESTS
test_credential_none_spawn.py::test_live_spawn_exports_its_own_harness_over_an_inherited_one -- `_stub_popen`,
`monkeypatch.setenv("AGI_HARNESS", "pi")`, `_argv(project, "pi-local")`, `main() == 0`,
`captured["env"]["AGI_HARNESS"] == "pi-local"`; red today (the child gets "pi"); conftest.py:51-62 strips every AGI_* var, so the
setenv is the only source. Neighbours: test_git_commit_guard.py, test_adapters.py, test_dispatch_dry_run.py.
## FILE SCOPE
extensions/agi/bin/dispatch.py 2594-2641
extensions/agi/tests/test_credential_none_spawn.py 62-131, 237-272
## CEILING
1 pi-local kid (tier kid, harness pi-local) · 4 production lines · 0 USD · FIRST (the inheritance leaf reads this variable)
