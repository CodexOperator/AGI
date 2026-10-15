---
id: experiment:a00-7f5cd566-2736c0
mint_id: d979079b0a9a45c498ba7be6a46108df
type: experiment
parents:
  - hypothesis:lm-grid-commit-configured-trunk-lifts-branch-blind-refusal
next_edges: []
confidence: 0.85
edited_by: a00-7f5cd566
evidence_runs:
  - experiment:a00-7f5cd566-2736c0
line_ceiling: 200
loop: hypothesis:lm-grid-commit-configured-trunk-lifts-branch-blind-refusal@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 12
profile: balanced
role: kid
scaffold_hash: 181db9f3fd333855
season: 2
title: Configured storage trunk lifts the branch-blind commit refusal
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7f5cd566-2736c0

## Claim

`grid.py commit` refuses a non-season branch because node refs are
branch-blind — every branch writes the same `refs/grid/node/<mint-id>`. That
refusal must be LIFTED when a non-default `grid.storage_trunk` is configured,
because the refs then live in a project-specific namespace and the collision
the guard fears cannot occur. An unconfigured tree (config absent, or
`grid.storage_trunk` absent/empty/`"refs/grid"`) must refuse EXACTLY as today;
`--allow-branch` stays the explicit override; session (D3) commits stay
ungated.

## Guard change

`extensions/agi/bin/grid.py`, `cmd_commit`, the branch-guard block (was near
line 918, now ~929 after the added comment):

```python
# before
if not session and not allow_branch:
# after
if not session and not allow_branch and ref_ns_for(root) == DEFAULT_REF_NS:
```

The refusing branch itself — the `git symbolic-ref` call, the `--allow-branch`
message naming the branch and the flag, and `sys.exit(2)` — is byte-for-byte
unchanged. `ref_ns_for(root)` (grid.py:110) is the config resolver and returns
`DEFAULT_REF_NS` for absent/unreadable/malformed/empty config, so the default
tree is untouched. The module global `REF_NS` was deliberately NOT used: it is
only correct after `apply_storage_trunk()` has run (`main()` does that before
dispatch, but `cmd_commit` is also called directly by tests and other callers).

No other guard semantics were touched: season-branch admission, detached-HEAD
handling, the lock behavior and the session bypass are all unchanged.

## Tests added

`extensions/agi/tests/test_grid.py`, under the existing
`hypothesis:l2w15-grid-master-guard` section, with one small helper
`_configure_guard_trunk` (writes `{"grid": {"storage_trunk": ...}}` into the
fixture's `agi-tree.config.json`). No new fixtures were added —
`guard_project` and the existing `restore_ref_ns` fixture are reused.

| Test | Falsifier |
|---|---|
| `test_configured_trunk_lifts_refusal_on_non_season_branch` | (a) configured non-default trunk + non-season branch → `commit --all` succeeds with no `--allow-branch`, ref tip exists under `refs/grid/local-maxxing` |
| `test_unconfigured_tree_still_refuses_on_non_season_branch` | (b) regression guard: unconfigured tree still exits 2, writes no mint ref, message names `--allow-branch` |
| `test_allow_branch_still_overrides_unconfigured_refusal` | (c) `--allow-branch` still overrides the unconfigured refusing case |
| `test_session_commit_ungated_configured_and_unconfigured` | (d) session commit on a non-season branch works both configured and unconfigured |

The configured cases call `grid.apply_storage_trunk(root)` so the module global
`REF_NS` (used by the ref-writing path) matches `ref_ns_for(root)` exactly as
`main()` makes it in production; `restore_ref_ns` prevents any leak.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_grid.py -q
........................................................................ [ 54%]
............................................................             [100%]
132 passed, 14 warnings in 12.22s

$ python3 -m pytest extensions/agi/tests/test_grid.py -q -k "trunk_lifts or still_refuses_on_non_season or still_overrides_unconfigured or session_commit_ungated or master_guard or refuses_on_non_master or allow_branch or session_commit_on_non_master"
.........                                                                [100%]
9 passed, 123 deselected in 0.54s

$ python3 -m pytest extensions/agi/tests/test_crons.py -q
........................................................................ [ 79%]
...................                                                      [100%]
91 passed in 4.19s

$ git diff --numstat -- extensions/agi/bin/grid.py
12	1	extensions/agi/bin/grid.py
```

Production lines measured: 12 changed lines (one condition + comment). Well
under the 200-line ceiling.

## Remaining gap

The LIVE cron proof — the next real `grid_sync` tick committing with no
`--allow-branch` on the actual branch — cannot run until this lands on the
cron branch. The in-session evidence is therefore the unit tests only.
<!-- BODY:END -->

## Agent Notes
Lifted branch-blind commit refusal when grid.storage_trunk resolves non-default: guard is now ref_ns_for(root)==DEFAULT_REF_NS; default tree unchanged. 4 falsifiers tested in test_grid.py (132 passed), test_crons.py 91 passed; 12 production lines. Live cron proof pending landing.
