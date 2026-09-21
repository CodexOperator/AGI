---
id: experiment:a00-c938b2d2-36eae7
mint_id: 980d5d0700c74a0aa02fd5e146755a11
type: experiment
parents:
  - hypothesis:l4-level3s-env-refusal-and-env-root-ascent-agree-with-the-docstring
next_edges: []
confidence: 0.9
edited_by: a00-30e43aee
evidence_runs:
  - experiment:a00-c938b2d2-36eae7
loop: hypothesis:l4-level3s-env-refusal-and-env-root-ascent-agree-with-the-docstring@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ab8c9f4b68ea08c0
season: 2
title: "level3 no-ascent env refusal: env-only text when the env spell fails, subdir env value refused by name"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c938b2d2-36eae7

## Experiment

BUILD-ORDER round for the parent hypothesis (goal:g15). PROVED on the built bytes.

**1 Quoted instruction (the claim we built):**
> CLAIM: the refusal names only what failed (env VAR=value does not resolve to a project root; the cwd clause appears only when cwd also failed), and the subdir case is settled one way and stated in both places — either level3 refuses an env value that is not itself a project root (no ascent; matches the docstring) or the docstring is amended to name level3's deliberate ascent — the kid picks the docstring-preserving refusal unless a test depends on the ascent, and says which.

**Pick: docstring-preserving refusal (no ascent).** No test depends on level3 ascending an env value (grep of test_level3.py / test_grid.py / test_dispatch.py). locations.py:322-327 docstring forbids ascent.

**2 What the code did at this base (by function name):**
- Defect A (refusal text): main's no-`--project` else-branch composed the cwd clause `no graph root at or above <cwd> (no .agi/ and no nodes/)` unconditionally, then appended the env clause. With a real project cwd and a garbage env value, the cwd clause printed false.
- Defect B (ascent): default_project_root (level3.py:193-216) passed env_root into resolve_project_root, whose 2nd branch is locations.find_project_root(p) — walks UP (locations.py:186-194). An env value naming a subdir (<root>/extensions) resolved to the enclosing root, against the docstring.

**3 Near miss:** resolve_project_root already knows "path is its own root" (`(p / "nodes").is_dir()` -> p) vs "must walk up". But project_root_from_env performs its OWN descent first (`_graph_dir_in`), so default_project_root sees env_root already resolved-or-unresolved. The clean cut is equality against the shared resolver: accept env_root only when resolve_project_root(env_root) == env_root. A subdir ascends to a different path and is refused; garbage resolves to None and is refused. No duplicated nodes/ check.

**4 The fix (files changed: extensions/agi/bin/level3.py, extensions/agi/tests/test_level3.py):**
- main else-branch: when env_hit, print ONLY `ERR: env VAR=val does not resolve to a project root`; no cwd clause. Cwd clause appears only when the cwd leg is the failing spell (no env).
- default_project_root: `resolved = resolve_project_root(env_root); return resolved if resolved == env_root else None`. None reaches main and is refused by name.
- Docstring of default_project_root rewritten to state the no-ascent rule.
- test_level3.py: test_nof_flag_default_refuses_a_rootless_env_root_by_name now asserts the env clause AND that `no .agi/ and no nodes/` is ABSENT (cwd is a real project). Added test_nof_flag_env_subdir_of_project_refuses_by_name (exit 2, names env) and test_nof_flag_env_naming_graph_root_itself_resolves (descent preserved, writes to graph root). Rootless-cwd-without-env test unchanged.

**Deviation:** none from the brief's suggested mechanism. Optional cwd-rootless-AND-env-garbage test not added: on an env hit the impl prints only the env message, so the env var is always named; the cwd-clause decision is orthogonal, covered by the rootless-cwd test.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_level3.py -q` -> **56 passed**
- `python3 -m pytest extensions/agi/tests/test_locations.py extensions/agi/tests/test_grid.py extensions/agi/tests/test_dispatch.py -q` -> **307 passed**

Live repro of the built bytes (all four cases):
```
$ cd /tmp/envtest/proj && AGI_TREE_PROJECT_ROOT=/tmp/envtest/nonexistent level3.py --dry-run ...
ERR: env AGI_TREE_PROJECT_ROOT=/tmp/envtest/nonexistent does not resolve to a project root   # A: env-only, no cwd clause; exit=2

$ AGI_TREE_PROJECT_ROOT=/tmp/envtest/proj/extensions level3.py --dry-run ...
ERR: env AGI_TREE_PROJECT_ROOT=/tmp/envtest/proj/extensions does not resolve to a project root  # B: subdir refused; exit=2

$ AGI_TREE_PROJECT_ROOT=/tmp/envtest/proj/.agi level3.py --dry-run ...
DRY-RUN: would create /tmp/envtest/proj/.agi/nodes/build/bin-a.md ... target dir: .../nodes/build  # descent preserved; exit=0

$ cd /tmp/envtest/rootless && env -u ...AGI_TREE_PROJECT_ROOT level3.py --dry-run ...
ERR: no graph root at or above /tmp/envtest/rootless (no .agi/ and no nodes/)  # cwd clause kept; exit=2
```

Verdict: proved — the refusal names only what failed, the subdir env case refuses (docstring preserved), and the descent case is not regressed.

## Agent Notes
level3 no-ascent env fix + env-only refusal text; docstring preserved; 56+307 tests green

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, SL7.64. (1) INSTRUCTION: the target claim requires the refusal to name only what failed, and the subdir env case settled against locations.project_root_from_env docstring (locations.py:322-327, no ascent). (2) MACHINE, re-measured by the parent on the built bytes at /tmp/envtest: cwd a real project + AGI_TREE_PROJECT_ROOT=/tmp/envtest/nonexistent now prints exactly "ERR: env AGI_TREE_PROJECT_ROOT=... does not resolve to a project root" with no cwd clause, exit 2; env naming <root>/extensions refuses by name; env naming <root>/.agi still resolves and writes to <root>/.agi/nodes/build. Reviewed the staged diff, not the report: level3.py default_project_root now accepts env_root only when resolve_project_root(env_root) == env_root (no ascent, one shared resolver, no duplicated nodes/ check); the else-branch env-hit message dropped the cwd clause; the docstring states the no-ascent rule. test_level3.py flips the false assertion at :1146 to not-in and adds the subdir-refusal and graph-root-descent tests. (3) NEAR MISS: a fix that only rewrote the message would satisfy clause (a) and leave the ascent shipping; a fix that refused every env value that is not a repo root with .agi would satisfy clause (b) and break the graph-root env spelling -- the equality cut keeps both. (4) DEVIATION: none. Parent ran pytest independently: test_level3.py 56 passed; test_stitch+test_locations+test_grid+test_dispatch 368 passed. Accepted as proved.
<!-- THOUGHT:END -->
