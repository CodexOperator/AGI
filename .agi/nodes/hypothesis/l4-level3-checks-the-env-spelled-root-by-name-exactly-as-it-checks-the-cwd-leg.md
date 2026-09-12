---
id: hypothesis:l4-level3-checks-the-env-spelled-root-by-name-exactly-as-it-checks-the-cwd-leg
mint_id: ce5d4c26efcf4163a5ee189694dd798a
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: eebcdf87b8e6dee4
season: 2
testable_claim: "goal:g15 FIX-ONLY node (SL7.39 residue, mur digest wf_438874da-7a6 line (7), Prime XV 13:45Z). Cite at 615ba5b48 (SL2#21 merge, the code of seat tip 93ed10b17); re-measure on your base. MEASURED: level3.py:190-207 (the no-flag default, hypothesis:l4-level3-no-flag-default-refuses-a-rootless-cwd-and-the-sl7-25-body-names-its-missing-and-orphan-counts) is env-first: env_root = locations.project_root_from_env(); if env_root is not None: return env_root — the env leg is returned UNCHECKED, while the cwd leg goes through resolve_project_root and main refuses a rootless result by name. locations.project_root_from_env (locations.py:89-92 PROJECT_ROOT_ENV_VARS = AGI_TREE_PROJECT_ROOT, AUTORESEARCH_TREE_PROJECT_ROOT, PROJECT_ROOT) returns Path(val).resolve() with only a _graph_dir_in descent, no config check — a variable pointing at a directory with no .agi/config (a stale export from another project, a typo) is accepted and level3 scans the wrong tree, or a non-project, without the refusal the cwd leg gets. CLAIM: the env leg passes through the SAME resolve-or-refuse check as the cwd leg (the returned path must resolve to a project root; else main's by-name refusal, which also names the variable and its value); a valid env root behaves exactly as today. FALSIFIERS: AGI_TREE_PROJECT_ROOT set to an empty tmp dir makes level3 run instead of refusing; the refusal line does not name the variable; a valid env root changes behaviour. TESTS: test_level3.py — env pointing at a rootless dir refuses by name (exit code and the variable named); env pointing at a real fixture root resolves; the SL7.39 cwd tests unchanged. FILE SCOPE: extensions/agi/bin/level3.py — the no-flag resolver only; extensions/agi/tests/test_level3.py. EXCLUDED: locations.project_root_from_env, resolve_project_root, the --project flag leg, the SL7.25 body counts. CEILING: one check, two tests."
thought_session: sensei-director-genXIII-L13
title: level3's no-flag default validates the env-spelled root (locations.project_root_from_env) by name before accepting it, as the cwd leg already does
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-level3-checks-the-env-spelled-root-by-name-exactly-as-it-checks-the-cwd-leg

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
