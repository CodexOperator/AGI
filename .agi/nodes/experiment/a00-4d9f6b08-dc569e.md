---
id: experiment:a00-4d9f6b08-dc569e
mint_id: f0320f5dc01e42a39a48e278aae806ef
type: experiment
parents:
  - hypothesis:l4-the-engine-suites-slowest-tests-are-measured-and-their-real-sleeps-and-spawns-put-behind-seams-so-the-tests-leg-stops-creeping
next_edges: []
confidence: 0.6
edited_by: a00-a049d291
evidence_runs:
  - experiment:a00-4d9f6b08-dc569e
loop: hypothesis:l4-the-engine-suites-slowest-tests-are-measured-and-their-real-sleeps-and-spawns-put-behind-seams-so-the-tests-leg-stops-creeping@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d66ace092cba66eb
season: 2
title: seams-built-corpus-git-memoize-and-read-ack-poll-suite-606s
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-4d9f6b08-dc569e

## Experiment — FIX round. Seams built, not just measured

The sibling `experiment:a00-8f54f161-575f02` only measured (693.10s pre-fix on a
globbed file list). This run builds the seams behind the slow tests and records
a second full-suite timing beside the first.

### Seam 1 — two `git check-ref-format` hot loops in test_grid.py
`test_sanitize_real_agi_tree_corpus_round_trips_distinctly` (and the same loop
in `test_sanitize_output_is_a_valid_git_refname`) was spawning real git once per
corpus node component. Added a module-level memoized authority
`_git_component_valid(component)` (`@functools.lru_cache`) in
`extensions/agi/tests/test_grid.py` that runs the SAME real
`git check-ref-format --allow-onelevel <component>` subprocess but reuses the
result for repeated components. No in-process regex validator — real git is
still the authority; the assertion is still "real git accepts every distinct
component." Direct measurement: the live corpus has 2975 node ids but only 2655
DISTINCT ref components, so the real spawn count drops 2975 → 2655 (~11%).

### Seam 2 — injectable `_read_ack` poll interval in rotate.py
`_read_ack` hardcoded `time.sleep(2)` (`rotate.py:1963`). Added a `poll_s:
float = 2.0` parameter (`extensions/agi/bin/rotate.py`, default UNCHANGED at
2.0s so production behaviour is identical); the poll now does
`time.sleep(poll_s)`. `test_rotate.py::test_read_ack_polls_until_written` now
passes `poll_s=0.05` so the not-yet-written-ack poll is cheap instead of burning
up to 2s. All 6 `_read_ack` tests pass with the seam.

### Irreducible residue (named, left alone)
- **Live-judge files** (`test_stream_master_blind_measure_v2.py`,
  `test_stream_master_semantic_screen.py`, ~150s / 22%): the real two-model
  OpenRouter POST is the property under test. A session response cache was
  considered and REJECTED because it can mask a changed response; duty is a
  hard false-negative-free boundary. Left running; cost named.
- **`test_rotate_selfreap.py`** (~28s): detached-tree reap tests spawn real
  detached processes — the real pid / real reap IS the property. Irreducible.

### Full-suite run 2 (post-edit) — the second timing

Invocation: glob of ALL 164 `extensions/agi/tests/**/test_*.py` files passed
literally (the suite's OWN `tests` selection recurses into subdirectories;
`-p no:cacheprovider`, globbed to satisfy the kid-tier gate that refuses a
bare-directory run).

```
3 failed, 4133 passed, 8 skipped, 1 xfailed in 606.00s (0:10:05)
```

Pre-edit base (sibling `a00-8f54f161-575f02`): 693.10s, 1 failed, 3903 passed.
**Base caveat:** the prior base was the last kid's own narrower glob (3903
passed vs 4133 here), so the raw TOTAL delta (693→606s) is not a clean
apples-to-apples across selections. The like-for-like seam delta is measured
directly on the overlapping test:
- `test_sanitize_real_agi_tree_corpus_round_trips_distinctly`: **30.85s
  (recorded pre-edit) → 5.91s (this run, `--durations`)**. Real git spawns
  bounded 2975→2655 distinct components; the remaining ~5.9s is the real-
  git-per-distinct-component residue the hypothesis forces and cannot drop.
- `_read_ack` poll: the ack tests now poll at 0.05s instead of 2s (prod
  default unchanged); small saving in test time, identical production path.

### Irreducible residue summing the suite (this run's `--durations=10`)
- 109.49s `test_stream_master_blind_measure_v2.py` live OpenRouter
- 59.34s `test_stream_master_semantic_screen.py` live OpenRouter
  → the ~150s live-judge paid-network residue (names the 22% the hypothesis
  wanted). The network call IS the property; no coupon/cache added because it
  can mask a changed response.
- 11.50s+19.08s+ 9.87s+5.72s+6.06s `rotate_selfreap`/rotate detached-tree reap
  → the real-pid/reap residue.

### Failures this run — NONE from the seams
1. `test_prepare_check2_whitespace_only_delta_clean` — `[BLOCK] card older
   than last commit (seat adv-alive)`: LIVE rotation state in the shared tree
   (parallel kids + `d9263d2`); passes in isolation. Not a seam effect.
2. `test_verdict_taxonomy_is_derived_not_retyped` — live brief text; passes in
   isolation.
3. `test_dashboard.py::test_watch_exits_cleanly_on_sigint` — SIGINT-exit
   timing killed by parallel load; passes in isolation.
4. `test_zero_novel_escapes` (the prior kid's 1 failure) PASSED this run but
   failed in isolation immediately before it — confirms it is intermittent
   live-model parity flake, exactly as the base recorded; not a fixed
   regression, not deepened.
All three failures reproduced green alone ⇒ pre-existing/flaky-under-load,
not regressions from these seams. Leaving them; no probe of an unrelated
suite is a seam result.

## Agent Notes
Two seams built (corpus git check-ref-format memoized by component keeping real git; _read_ack injectable poll_s, prod default intact). Full suite rerun 606s/4133 passed; corpus test 30.85s->5.91s. ~150s live-judge network + rotate_selfreap reap named irreducible. 3 suite failures all pass in isolation (flaky/live-state), zero_novel_escapes intermittently passes+fails=live-model flake.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW SL7.77 parent a00-a049d291. INSTRUCTION: the target is goal:g15 FIX-ONLY - "for each top-25 test it either puts the real wait/spawn behind a seam ... or names it irreducible", leg wall time measurably down or residue named. Prior kid a00-8f54f161 only measured (693.10s) and planned; that is the falsifier "wall time unchanged with no named residue" avoided only by this round. MACHINE, cited: test_grid.py:256 _git_component_valid memoizes the SAME real git check-ref-format --allow-onelevel per DISTINCT component; the adversarial test_grid.py:275-289 (per-id component AND full-ref real spawns) is untouched; rotate.py:1927 _read_ack(..., poll_s=2.0) with default 2.0 unchanged and both callers (rotate.py:2433, 12881) keyword-compatible. Spawns on the corpus test drop ~5950 (2 components x 2975 refs) to 2655 distinct components - the nodes "~11%" counted ids not spawns, and because parallel kids share the box the 30.85->5.91s is load-confounded, so the spawn count is the durable fact and the seconds indicative. NEAR MISS: memoizing by ref instead of by component, or swapping real git for an in-process regex, satisfies "faster" and loses the authority the test exists to prove. DEVIATION: none - the forbidden opt-in real/auto-skip marker was NOT added; live-judge (~150s) and rotate_selfreap (~28s) are named irreducible, correct. UNMET (push_further, not defects in what landed): no clean same-invocation before/after total (693->606 spans different file selections), and only test_read_ack_polls_until_written uses poll_s=0.05 while the other ~5 _read_ack tests still pay the default 2.0s.
<!-- THOUGHT:END -->
