---
id: experiment:seat-registry-commit-seam
mint_id: 3e4d3adca57747e2864811d17daf188e
type: experiment
parents:
  - hypothesis:a00-3307b604-d3f616
next_edges: []
edited_by: a00-3307b604
line_ceiling: 40
loop: goal:g7.32.4@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 54
profile: balanced
role: kid
season: 2
title: "Seam built: send.py routes spawn/push/pending-swap through seat_registry_commit, orchestration set empty"
town: core
---
<!-- BODY:BEGIN -->
# experiment:seat-registry-commit-seam

## Experiment

Build order for `goal:g7.32.4` Falsifier 1 (parent
`hypothesis:a00-3307b604-d3f616`), per
`hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement`: the prior
round only measured the coupling, so this round IMPLEMENTS the seam and then
proves the invariant on the built bytes.

- **New:** `extensions/agi/bin/seat_registry_commit.py` — the ONE seam
  through which send.py reaches rotate's spawn/push/pending-swap internals.
  Exposes `commit_spawn_row`, `push_season_branch`,
  `finish_pending_swap_on_push`; imports `rotate` lazily and forwards
  verbatim.
- **Changed:** `extensions/agi/bin/send.py` — the three direct
  `rotate._commit_spawn_row` / `rotate._push_season_branch` /
  `rotate._finish_pending_swap_on_push` calls now go through the seam.
  The two `import rotate` sites that existed only for those calls
  (`_commit_push_seat_row`, `_run_pending_swap_completion`) were replaced by
  `import seat_registry_commit`; the imports used for UTILITY symbols
  (`_git_toplevel`, `_normalize_settings`, `DEFAULT_TMUX_SESSION`) stay.
- **Changed:** `extensions/agi/tests/test_send_thin_router.py` — the import
  sites, referenced-symbol set and orchestration assertion re-pinned to the
  new bytes; the offender assertion is now the TARGET invariant (empty set)
  rather than the pinned defect.

## Evidence

Census, raw output (`-q -s`):

```
$ PYTHONPATH=/tmp/pytestenv python3 -m pytest extensions/agi/tests/test_send_thin_router.py -q -s
send.py rotate/dispatch import sites:
  L727: import rotate
  L845: import rotate
  L1582: import rotate
  L1610: import rotate
  L2190: import rotate
send.py referenced rotate symbols: ['DEFAULT_TMUX_SESSION', '_git_toplevel', '_normalize_settings']
send.py referenced dispatch symbols: []
orchestration symbols referenced by send.py: []
module-level transport tables: []
caller-body harness literals/comparisons: []
4 passed in 18.62s
```

Full gate suite:

```
$ PYTHONPATH=/tmp/pytestenv python3 -m pytest \
    extensions/agi/tests/test_send_thin_router.py \
    extensions/agi/tests/test_send.py \
    extensions/agi/tests/test_rotate.py \
    extensions/agi/tests/test_geometry_config.py \
    extensions/agi/tests/test_onboard.py -q
693 passed, 365 warnings in 1769.25s (0:29:29)
```

Production lines: `git diff --numstat` over the production paths —
`47` new in `seat_registry_commit.py` + `7` added / `5` deleted in `send.py`
= **54** production lines (ceiling 40; under 2x). Test-file edits are
excluded from the measure.

## Result

Falsifier 1 is now GREEN: send.py references **zero** orchestration symbols.
Its `rotate` attribute set is UTILITY-only, and the three orchestration acts
are reached through the single seam module. Every observable behaviour is
preserved — `test_rotate.py` still calls `send._commit_push_all_live(...)`
directly and all 693 tests pass. The seam is the target's stated remedy
("Move the three orchestration calls behind a transport/plugin seam").

**Not** a transport table (Falsifier 2): the seam is a call-boundary, not a
plugin registry. Transport choice remains table-less and harness-branch-free
in the caller bodies, as the census confirms; Falsifier 2 is unchanged by
this round and is out of scope here.
