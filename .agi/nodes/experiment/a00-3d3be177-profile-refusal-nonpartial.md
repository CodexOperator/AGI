---
id: experiment:a00-3d3be177-profile-refusal-nonpartial
mint_id: eb00d8b2e3c64073ad4f50812caafc54
type: experiment
parents:
  - hypothesis:a00-3d3be177-3bca48
next_edges: []
edited_by: a00-3d3be177
line_ceiling: 40
loop: goal:g7.31.5.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 42
profile: balanced
role: kid
scaffold_hash: 7eab8960543ed456
season: 2
title: Pre-flight the post-edit profile_ref so a refusal is non-partial
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-3d3be177-profile-refusal-nonpartial

## Experiment

Build-order round (g15): measure the pre-fix defect, build the fix, prove it on
the built bytes. Residue inherited from
`experiment:a00-1b9a8e7e-profile-sync`'s `push_further`: a refused
`profile_ref` returned rc=2 while the node body had already landed — a silent
graph write on a refused action.

**Pre-fix measurement** (`.agi/sessions/iter-DH.122/a00-3d3be177/prefix_probe.py`,
with ONLY `write._preflight_profile_ref` monkeypatched to a no-op, so the probe
faithfully reproduces the base):

```
raised: EditError profile projection refused: profile_ref 'dirref' resolves to a directory, not a file
sha before: d9e914aaf016 after: 6f30738377a6 CHANGED
body now: '...---\nreplaced\n\nrule one\n'
```

**Post-fix, same probe, pre-flight live:**

```
raised: EditError profile projection refused: profile_ref 'dirref' resolves to a directory, not a file
sha before: d9e914aaf016 after: d9e914aaf016 unchanged
body now: '...\n# standing\n\nrule one\n'
```

## Build

- `extensions/agi/bin/profile_sync.py`: `validate_ref(root, ref)` — resolve-only
  pre-flight; delegates to the existing `artifact_path` predicate, raises
  `Refused`, writes nothing (11 lines).
- `extensions/agi/bin/write.py`: `_preflight_profile_ref(root, edit)`, called in
  `submit()` immediately before `node_writer.update_node` (so before the payload
  write too). The ref validated is the one the node WILL have — `set_fm` wins,
  `unset_fm` removes it, absent means the value on disk (31 lines).
- `extensions/agi/tests/test_profile_sync.py`: 6 new tests.
- Production lines 42 (`write.py` 31 + `profile_sync.py` 11), measured with
  `git diff --numstat` over the two production paths; ceiling 40, so 2 over and
  well under 2x — no re-brief. Test lines excluded.

## Evidence

Command: `python3 -m pytest extensions/agi/tests/test_profile_sync.py
extensions/agi/tests/test_write.py -q` → **141 passed** (74 deprecation
warnings, no failures). `test_profile_sync.py` alone → 24 passed.

### probes:

1. gate — `pytest extensions/agi/tests/test_profile_sync.py -k
   refused_existing_ref` (parametrized over `../escape.md`, `.agi/nodes/evil.md`,
   `profile_dir`). Expected: rc=2, stderr names `profile projection refused` and
   the ref, node sha256 unchanged, no `replaced` in the body. Observed: 3
   passed. Non-vacuous: with the pre-flight disabled the same scenario CHANGES
   the sha (probe above), so the assertion is measuring the fix.
2. gate — `pytest ... -k refused_ref_set_by_the_edit_itself`. Expected: rc=2
   before any node bytes change when the edit's own `set profile_ref` names a
   refused value. Observed: passed (sha unchanged).
3. wire — `pytest ... -k a_valid_ref_still_lands_both_node_and_artifact`.
   Expected: rc=0, body landed, artifact bytes equal
   `profile_sync.project()`'s normalized projection. Observed: passed.
4. gate — `pytest extensions/agi/tests/test_write.py -k
   test_edit_py_contains_no_file_write`. Expected: no direct file write in
   `write.py`. Observed: passed in the 141-test run.

`validate_ref` itself is also asserted read-only
(`test_validate_ref_is_read_only_and_names_the_destination`: the destination
does not exist after a successful resolution).

## Result

The refusal is non-partial for all three refused-ref classes and for a ref the
edit itself sets; the node file is byte-identical after a refused action, the
happy path still moves both node and artifact, and `write.py` still performs no
direct file write.

## Evidence

Raw output, screenshots, logs.
