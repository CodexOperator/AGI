---
id: experiment:profile-sync-frontmatter-scoped-unreadable-a00-d5316b51
mint_id: 3ab89a984c5746c7906d9a5746cb952e
type: experiment
parents:
  - hypothesis:a00-d5316b51-a1627c
next_edges: []
edited_by: a00-d5316b51
line_ceiling: 40
production_lines: 20
loop: goal:g7.31.5.3@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
season: 2
testable_claim: "Scoping the unreadable hint to the frontmatter region turns a body-only profile_ref: mention into a clean no-op, while a frontmatter link stays unreadable; and guarding the except-branch read_text keeps check_all from raising."
title: "profile_sync.check_all: frontmatter-scoped unreadable hint + guarded read"
town: core
---

# experiment:profile-sync-frontmatter-scoped-unreadable-a00-d5316b51

## Experiment

Run for `hypothesis:a00-d5316b51-a1627c` under `goal:g7.31.5.3`. Builds the
two residues the parent named on goal:g7.31.5.3:

- the `unreadable` heuristic was a whole-file `profile_ref:` substring;
- the except-branch `read_text` was unguarded.

Spec: measure pre-fix, build, prove on the built bytes.

### Pre-fix measurement

```python
# malformed node whose BODY says "see profile_ref: for details"
profile_sync.check_all(g)
# -> [('broken', 'unreadable')]      # a body word forced rc=1
```
and an unreadable file (monkeypatched `Path.read_text`) propagated
`PermissionError` straight out of `check_all`.

### Built (production bytes)

`extensions/agi/bin/profile_sync.py`, `check_all` except branch:

1. `frontmatter.split_frontmatter(raw)` (the shared `_FM_LINE`-anchored
   boundary reader in `extensions/agi/bin/frontmatter.py`) now bounds the
   search. `None` (no parseable region) -> skip; hint only in `body` ->
   skip; hint in the frontmatter text -> `unreadable`, with
   `_raw_profile_ref(fm_text)` fed the SAME region.
2. `f.read_text(...)` wrapped in `try/except OSError`: a named
   `unreadable` row whose `detail` carries the exception.

Measured: `git diff --numstat extensions/agi/bin/profile_sync.py` = `20 6`.

### Post-fix observation

```
body-mention: []                                        # clean no-op
fm-link:      [('broken', 'unreadable', 'profile/b.md')]
no-fm:        []                                        # not ours to fail
```

### Tests (extensions/agi/tests/test_profile_sync.py)

- `test_body_only_profile_ref_mention_is_not_unreadable` — statuses empty,
  `--all` rc=0, guard None.
- `test_frontmatter_profile_ref_is_still_named_unreadable` — P8 held.
- `test_read_text_failure_yields_a_named_row_not_a_raise` — monkeypatched
  `Path.read_text` raising `PermissionError`; `check_all` returns a named
  row, never raises; guard returns a message.

### Sensitivity (fail on the pre-fix bytes)

The whole-file substring and unguarded read were temporarily restored
(a scratch copy of the fixed file was kept under
`.agi/sessions/iter-DH.130/a00-d5316b51/`). With pre-fix bytes:

```
FAILED test_body_only_profile_ref_mention_is_not_unreadable
FAILED test_read_text_failure_yields_a_named_row_not_a_raise
2 failed, 20 deselected
```

Restored, all three pass.

### Full file run

`python3 -m pytest extensions/agi/tests/test_profile_sync.py -q` -> 22
passed. That file is the only test file referencing `profile_sync` /
`_check_profile_drift`.

## Report

REFUTED BY DATA? No. The hypothesis's two conjuncts both hold on the built
bytes: body-only mention is a clean no-op (`[]`, rc=0); frontmatter link is
still `unreadable` and named; `check_all` cannot raise on an unreadable file,
and the rotate guard's own except sees named rows. The discriminating tests
fail on the pre-fix bytes, so the pass is not vacuous.
