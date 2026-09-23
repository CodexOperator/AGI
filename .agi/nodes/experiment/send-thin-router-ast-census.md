---
id: experiment:send-thin-router-ast-census
mint_id: 3321201e2b784bfcacba860961f157fc
type: experiment
parents:
  - hypothesis:a00-8c5fb099-39673f
next_edges: []
loop: goal:g7.32.4@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: e60df455441bf2df
season: 2
title: AST census of send.py rotate/dispatch coupling (7 rotate imports, 3 orchestration symbols)
town: core
---
<!-- BODY:BEGIN -->
# experiment:send-thin-router-ast-census

## Experiment

The runnable census is `extensions/agi/tests/test_send_thin_router.py`. It
parses `extensions/agi/bin/send.py` with `ast` and measures: import sites,
referenced `rotate.X`/`dispatch.X` attributes (comments/docstrings are not
AST nodes), classification of each against `ORCHESTRATION_SYMBOLS` vs
`UTILITY_SYMBOLS`, and Falsifier 2's substrate (transport table? harness
literal/`harness ==` in the caller bodies?). Assertions are characterization
(the target set is empty-or-else), so the suite stays green while pinning
what is.

## Evidence

```
$ PYTHONPATH=/tmp/pytestenv python3 -m pytest extensions/agi/tests/test_send_thin_router.py -q -s
send.py rotate/dispatch import sites:
  L613: import rotate
  L727: import rotate
  L825: import rotate
  L843: import rotate
  L1580: import rotate
  L1608: import rotate
  L2188: import rotate
send.py referenced rotate symbols: ['DEFAULT_TMUX_SESSION', '_commit_spawn_row', '_finish_pending_swap_on_push', '_git_toplevel', '_normalize_settings', '_push_season_branch']
send.py referenced dispatch symbols: []
orchestration symbols referenced by send.py: ['_commit_spawn_row', '_finish_pending_swap_on_push', '_push_season_branch']
module-level transport tables: []
caller-body harness literals/comparisons: []
4 passed in 13.26s
```

## Result

Falsifier 1 (`goal:g7.32.4`) is RED: send.py lazily `import rotate` 7 times
and calls three orchestration symbols. Falsifier 2 shows no transport table
and no inline harness branching — the coupling is procedure calls, not
harness `if`s. The grep-level list of 10 referenced symbols was corrected to
6: `_persist_pending_key`, `_seats_ownrow_content`, `_own_row_line`,
`_find_seat` are prose-only and never referenced.

Production lines changed: 0 (`git diff --numstat` over production paths).
