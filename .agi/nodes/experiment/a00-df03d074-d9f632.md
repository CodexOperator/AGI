---
id: experiment:a00-df03d074-d9f632
mint_id: 1f035180f71b46d6ba3aaae9b64f71ec
type: experiment
parents:
  - hypothesis:l4-real-node-tests-follow-their-own-tree
next_edges: []
confidence: 0.9
edited_by: a00-04c03dd9
evidence_runs:
  - experiment:a00-df03d074-d9f632
loop: hypothesis:l4-real-node-tests-follow-their-own-tree@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d9eea36fee810a07
season: 2
title: A00 df03d074 d9f632
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-df03d074-d9f632

## Experiment

Test-side fix to `extensions/agi/tests/test_commands.py` so the real-node tests
validate the tree they RUN in, not the hardcoded main checkout.

Two literals pinned the suite to MAIN:

- L207 `REAL_ROOT = Path("/home/ubuntu/work/agi/.agi")`
- L352 `_agi()`'s cwd default `Path("/home/ubuntu/work/agi")`

The fix resolves both through `locations` — the single resolver `goal:g11`
exists so everything calls — keyed off the test file's own location:

```python
REAL_ROOT = locations.find_project_root(Path(__file__).resolve())   # Q1: graph
SOURCE_ROOT = locations.source_root(REAL_ROOT)                       # Q2: source
```

- `REAL_ROOT` → the graph root of THIS worktree (`.agi`).
- `SOURCE_ROOT` → `_agi()`'s cwd default, the source repo the graph describes.
- `DRIVER` left untouched (was already `Path(__file__).../driver.sh`).

Added `import locations` (the bin dir is already on sys.path) and one NEW test,
`test_resolved_root_follows_the_tree_under_test`, asserting both `REAL_ROOT`
and the test file are descendants of `SOURCE_ROOT` and `REAL_ROOT.name == ".agi"`
— the property that encodes "follows the tree under test", checkable without a
second checkout.

## Evidence

Grep for the pinning literal — nothing remains:

```
$ grep -n "/home/ubuntu" extensions/agi/tests/test_commands.py
(exit 1 — no match)
```

Resolution from THIS seat worktree (before run):

```
graph root: <worktree>/.agi
source root: <worktree>
commands.md present: True
```

`nodes/.geometry/commands.md` IS present in the worktree, so the `@real_only`
skipif still evaluates against a real node and the tests RUN.

Same-file suite, FROM this worktree — green, 0 skipped:

```
$ python3 -m pytest extensions/agi/tests/test_commands.py -q
......................      [100%]
22 passed in 1.53s
```

(The `@real_only` tests are among the 22; a skip would have shown as `22
passed, X skipped`. Zero skips is the real falsifier, and it holds.)

Combined with the resolver's own suite:

```
$ python3 -m pytest extensions/agi/tests/test_commands.py extensions/agi/tests/test_locations.py -q
97 passed in 3.38s
```

No assertions weakened or deleted — only the two path literals and the added
descendant test.

## test_provisioning.py — reported, NOT fixed (per assignment)

`extensions/agi/tests/test_provisioning.py` carries the SAME literal at L32 and
L336:

- L32 gates the `live` marker: `not provisioning.available("/home/ubuntu/work/agi")`.
- L336 `ROOT = "/home/ubuntu/work/agi"`.

These gate and feed LIVE tests that mint a real metered OpenRouter key. To
change safely I would need to know: (1) whether `provisioning.available()`
reads the key from the config at that path (so repointing at a worktree config
without the key would flip `live` → skip), and (2) whether the worktree config
copies the provisioning key or deliberately omits it. If the key is worktree-absent
and the gate is config-driven, repointing IS a silent weakening, exactly the
assignment's warning. Left untouched.

## Agent Notes
Test-side fix: REAL_ROOT+_agi() cwd resolved via locations from test file's own path; /home/ubuntu literals gone, @real_only tests RUN in worktree (22 passed 0 skip), added descendant-assertion test, combined locations suite 97 green, full suite 2381 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-04c03dd9) ACCEPTS this node as written. I re-verified the artifact independently: grep -n /home/ubuntu on test_commands.py exits 1 (empty); git diff --cached shows only the two literal replacements via locations.find_project_root/source_root, one import, and the new descendant-assertion test; pytest from this seat worktree gives 97 passed, 0 skipped for test_commands+test_locations. Verdict proved stands; evidence run is this node itself, which is the run.
<!-- THOUGHT:END -->

Parent review: artifact re-verified (grep empty, 97 passed / 0 skipped, diff minimal and scope-compliant); accepted at verdict=proved. test_provisioning.py correctly reported-not-fixed per assignment.
