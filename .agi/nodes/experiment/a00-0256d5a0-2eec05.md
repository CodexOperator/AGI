---
id: experiment:a00-0256d5a0-2eec05
mint_id: aae06164b9314f2999d474a20f388a86
type: experiment
parents:
  - hypothesis:l4-level3-checks-the-env-spelled-root-by-name-exactly-as-it-checks-the-cwd-leg
next_edges: []
confidence: 0.95
edited_by: a00-981b4e12
evidence_runs:
  - experiment:a00-0256d5a0-2eec05
loop: hypothesis:l4-level3-checks-the-env-spelled-root-by-name-exactly-as-it-checks-the-cwd-leg@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 25d94ca39d36e95f
season: 2
title: level3's no-flag env leg resolves-or-refuses through the same resolve_project_root as the cwd leg; a rootless AGI_TREE_PROJECT_ROOT is refused naming var=value
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0256d5a0-2eec05

## Experiment

FIX-ONLY round (goal:g15), hypothesis:l4-level3-checks-the-env-spelled-root-by-
name-exactly-as-it-checks-the-cwd-leg. Measured the pre-fix state, then
implemented the claim and proved it on the built bytes.

Pre-fix defect (measured at `default_project_root`, extensions/agi/bin/
level3.py:193): the env override leg was `env_root =
locations.project_root_from_env(); if env_root is not None: return env_root` —
returned UNCHECKED. `locations.project_root_from_env` (locations.py:310) legitimately
returns `Path(val).resolve()` with only a `_graph_dir_in` descent and no config
check, so a variable naming a non-project (a stale export, a typo, an empty
tmp dir) was accepted and level3 scanned that stray tree as authoritative —
an env bypass of the resolve-or-refuse the cwd leg already got.

The env spell is now routed through the SAME `resolve_project_root` as the
cwd leg (`return resolve_project_root(env_root)`), so a rootless env path
resolves to None and is refused; and `main`'s refusal now names the env
variable and its value when the env leg was the failed spell.

## Evidence

Code (extensions/agi/bin/level3.py):

    def default_project_root() -> Path | None:
        env_root = locations.project_root_from_env()
        if env_root is not None:
            return resolve_project_root(env_root)
        return resolve_project_root(Path.cwd())

`main` refusal (env-hit path):

    ERR: no graph root at or above {cwd} (no .agi/ and no nodes/) — env
    AGI_TREE_PROJECT_ROOT={value} does not resolve to a project root

Two tests added in extensions/agi/tests/test_level3.py:
- `test_nof_flag_default_refuses_a_rootless_env_root_by_name`: cwd is a real
  project (cwd leg would resolve), env AGI_TREE_PROJECT_ROOT set to an empty
  imposter dir -> exit 2, stderr contains `env AGI_TREE_PROJECT_ROOT={imposter}`
  and `does not resolve to a project root`. (Falsifier: env alone would have
  made level3 run.)
- `test_nof_flag_default_resolves_a_valid_env_root`: env AGI_TREE_PROJECT_ROOT
  naming a real `.agi` project, run from a rootless cwd -> exit 0, target dir
  `<proj>/.agi/nodes/build`. (Falsifier: valid env root must not change.)

The SL7.39 cwd-leg tests (`test_nof_flag_default_refuses_a_rootless_cwd_by_name`,
`test_nof_flag_run_from_inside_a_project_resolves_its_nearest_agi`,
`test_refuses_a_rootless_project_path_by_name`) pass unchanged — a valid env
root (graph root or repo root, either of which may already descend into
`.agi/`) resolves through `resolve_project_root` identically to before.

Full suite: `python3 -m pytest extensions/agi/tests/test_level3.py -q` ->
**54 passed** (was 52; 2 new). Filtered run of the env/rootless spell tests:
6 passed.

## Agent Notes
Level3 no-flag default now routes the env override through the same resolve_project_root as the cwd leg; a rootless AGI_TREE_PROJECT_ROOT refuses by name (naming var+value), valid env root unchanged. 2 tests added, suite 54 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (parent a00-981b4e12, SL7.50) — ACCEPTED, proved stands, 0.95 kept.

(1) WHAT THE INSTRUCTION SAID: the target hypothesis is a goal:g15 FIX-ONLY node — level3's no-flag default must validate the env-spelled root "exactly as it checks the cwd leg"; FALSIFIERS listed "AGI_TREE_PROJECT_ROOT set to an empty tmp dir makes level3 run instead of refusing" and "the refusal line does not name the variable"; CEILING "one check, two tests".

(2) WHAT THE MACHINE ACTUALLY DOES, measured, not read:
  - pre-fix, level3.py:212-215 returned env_root unchecked. I built the pre-fix variant (/tmp/l3repo, patched copy, NO git touched) and ran the exact new-test conditions (cwd = a real project, env AGI_TREE_PROJECT_ROOT=/tmp/pf/imposter, an empty dir): exit=0 and stdout says "target dir: /tmp/pf/imposter/nodes/build" — the imposter WAS scanned as authoritative. The falsifier fires.
  - post-fix (working tree, extensions/agi/bin/level3.py:212-216): "return resolve_project_root(env_root)"; main's refusal (level3.py:1216-1224) names "env {var}={value} ... does not resolve to a project root". Same conditions: test_nof_flag_default_refuses_a_rootless_env_root_by_name asserts exit 2 + both strings.
  - I ran it myself: pytest extensions/agi/tests/test_level3.py -q -> 54 passed (kid's claim reproduced exactly). The two new tests are real and non-vacuous; the refusal test's cwd IS a real project, so the cwd leg alone would have resolved — the refusal can only come from the env leg failing.

(3) THE NEAR MISS: a fix that only checked project_root_from_env(...) is not None — or that checked the path exists — would satisfy the words "validates the env root" and lose the mechanism: the defect was not "path does not exist" (the imposter dir EXISTS, my pre-fix run wrote into it), it was "path is not a graph root and was accepted anyway". The kid's version routes through resolve_project_root, the same function the cwd leg uses, so the two spells cannot disagree — that is the property the claim names and the one I verified by running the pre-fix code rather than by reading the diff.

(4) DEVIATION: none from a standing rule. One behaviour note for the record, not a defect: because resolve_project_root -> find_project_root walks UP, an env value naming a SUBDIRECTORY of a real project now ascends to the enclosing graph root where project_root_from_env alone would have returned the subdir unchanged. That is exactly the cwd-leg semantics the claim demands ("exactly as it checks the cwd leg"), and the excluded functions (project_root_from_env, resolve_project_root) are untouched — but it is a composition change a later reader should know about. It cannot silently pick a DIFFERENT project than the cwd leg would: both legs call the same resolver.
<!-- THOUGHT:END -->

ACCEPTED (parent a00-981b4e12, SL7.50). Parent read the ARTIFACT, not the report: level3.py:212-216 now returns resolve_project_root(env_root) and main's refusal (level3.py:1216-1224) names env var=value, matching the cwd leg's resolve-or-refuse. Falsifier verified by RUNNING a patched pre-fix copy (no git touched): with cwd a real project and AGI_TREE_PROJECT_ROOT=/tmp/pf/imposter, pre-fix exits 0 and scans /tmp/pf/imposter/nodes/build; post-fix the new test demands exit 2 + the named refusal. Ran the suite myself: 54 passed. Node frontmatter reviewed: parents resolves to the target hypothesis, verdict proved, evidence_runs is a real node-id list (self, legal for an experiment). Title de-scaffolded by this review. One recorded behaviour note, not a defect: an env value naming a subdir of a real project now ascends to the enclosing graph root (same semantics as the cwd leg, which is what the claim asks for).
