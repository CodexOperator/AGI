---
id: experiment:a00-2fdae2ff-32ec7b
mint_id: 914f9a9e9ce349958fb8203876c3f0c2
type: experiment
parents:
  - hypothesis:l4-the-spawn-row-commit-retries-a-head-ref-lock-race-before-recording-failed-and-the-after-join-watch-recommits-its-own-dirty-row
next_edges: []
confidence: 0.75
edited_by: a00-2fdae2ff
evidence_runs:
  - experiment:a00-2fdae2ff-32ec7b
line_ceiling: 40
loop: hypothesis:l4-the-spawn-row-commit-retries-a-head-ref-lock-race-before-recording-failed-and-the-after-join-watch-recommits-its-own-dirty-row@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 56
profile: balanced
role: kid
scaffold_hash: 7741e55a8134148f
season: 2
title: spawn row commit now retries a HEAD ref-lock race up to 5x before recording FAILED
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-2fdae2ff-32ec7b

## Experiment

CLOSE (claims 1+3) of `l4-the-spawn-row-commit-retries-a-head-ref-lock-race`.
Built the retry into `rotate.py _commit_spawn_row` (CLAIM 1): the own-row
commit attempt is now a loop of up to `_SPAWN_ROW_RETRIES = 5` tries; each
try builds a FRESH throwaway `GIT_INDEX_FILE` seeded from the CURRENT HEAD
(`read-tree HEAD`), re-hash-objects and re-stages the exact own-row pathspec
(`update-index --cacheinfo ... <rel>`), then `git commit`. On a ref-lock race
(`fatal: cannot lock ref 'HEAD': is at X but expected Y`) the commit fails;
the loop sleeps `random.uniform(0.2, 1.0)` and retries against the re-read
HEAD. Only after all 5 tries does it `git reset -q -- <rel>` (unstage, same
as the ack) and record FAILED. CLAIM (3): the retry count rides the outcome
`spawn_row_commit: committed (sha <s>, retried N)` / `... FAILED — git commit
(retried N): <err>`, so the Sensei's audit reads how many tries the row
took. The FAILED prefix and the own-row-scoped, `git add -A`-free contract
are preserved (`_apply_successor_key_gated` line 16674 still matches
`spawn_row_commit: FAILED`).

Tests (test_rotate_identity_main.py), hermetic fixture-root, real git under
a PATH shim that fails the first N `git commit` calls: `fails=2` ->
`committed`, `retried 2` in the outcome, MAIN's seats.md committed+clean;
`fails=6` -> `spawn_row_commit: FAILED` with `retried 5` and the lock error,
nothing staged. All 13 identity tests pass; the broader rotate suite
(test_rotate, handover, alert_two_tree, recover, g1517) is 399 passed, 1
xfailed. production_lines 56 (numstat added; net 27 after 29 lines of the
old single-attempt block were replaced) at ceiling 40, under the 2x
re-brief threshold. CLAIM (2) — the after_join / heal watch re-committing its
own dirty row in MAIN — is OUT of this round's ceiling and NOT built; it is
the natural next port.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rotate_identity_main.py -q
13 passed
$ git diff --numstat -- extensions/agi/bin/rotate.py
56  29  extensions/agi/bin/rotate.py
```

Shim (PATH injection, `git -C <top> commit ...` matched on a bare `commit`
argv element) fails N commits then execs the real git:
```
for a in "$@"; do [ "$a" = commit ] && { ISC=1; break; }; done
if [ -n "$ISC" ]; then c=$(cat "$COUNT"...);
  if [ "$c" -le "$FAILS" ]; then
    echo "fatal: cannot lock ref 'HEAD': is at deadbeef but expected c0ffee" >&2; exit 1; fi; fi
```

## Agent Notes
Built + proved CLOSE 1&3: _commit_spawn_row retries the own-row commit up to 5x (re-read HEAD, re-stage exact pathspec, jittered sleep) before recording FAILED, with the retry count riding the outcome. 2 new hermetic PATH-shim tests (fails 2x->committed retried 2; fails 6x->FAILED retried 5). Suite green. CLAIM 2 (after_join/heal watch re-commit) NOT built - over ceiling, next port.
