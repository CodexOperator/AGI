---
id: experiment:a00-8f54f161-575f02
mint_id: 09b99a16bd5742d3aee9d22b1a60cc8e
type: experiment
parents:
  - hypothesis:l4-the-engine-suites-slowest-tests-are-measured-and-their-real-sleeps-and-spawns-put-behind-seams-so-the-tests-leg-stops-creeping
next_edges: []
confidence: 0.7
edited_by: a00-a049d291
evidence_runs:
  - experiment:a00-8f54f161-575f02
loop: hypothesis:l4-the-engine-suites-slowest-tests-are-measured-and-their-real-sleeps-and-spawns-put-behind-seams-so-the-tests-leg-stops-creeping@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0ed2ec749879365d
season: 2
title: A00 8f54f161 575f02
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-8f54f161-575f02

## Experiment

# experiment:a00-8f54f161-575f02

## Experiment

Measured the ENGINE test suite's wall-clock cost, per test, to isolate the
slowest tests and identify which carry REAL sleeps / REAL spawns (paid network
latency, whole-corpus subprocess spawning) that a seam can absorb.

Ran the full suite by naming every test file (the kid-tier gate refuses a bare
directory run, so files were glob-expanded and passed individually):

```
python3 -m pytest extensions/agi/tests/test_*.py -q -p no:cacheprovider --durations=40
```

**Result: 1 failed, 3903 passed, 8 skipped, 1 xfailed in 693.10s (0:11:33).**
The one failure is unrelated to speed (a live `ModelJudge` parity gap on
`code-smuggle`, not a seam defect).

### Slowest call sites

| test file / test | cost (call) | real sleep / spawn behind it |
|---|---|---|
| test_stream_master_blind_measure_v2.py `test_measure_and_report_escapes` | 95.29s | real OpenRouter `ModelJudge` HTTP POST per corpus body |
| test_stream_master_blind_measure_v2.py `test_no_false_positives...` | 9.26s | same real judge |
| test_stream_master_semantic_screen.py `test_zero_novel_escapes` | 43.64s | same real judge (also FAILED) |
| test_stream_master_semantic_screen.py `test_benign_relay_...` | 2.99s | same real judge |
| test_grid.py `test_sanitize_real_agi_tree_corpus_round_trips_distinctly` | 30.85s | ONE `git check-ref-format` SUBPROCESS per corpus node (~2974 spawns) |
| test_rotate_selfreap.py `test_reap_belam_oldest_pane_seam_detached_tree` | 18.81s | real detached-tree reap: sleep + non-child SIGTERM-immune spawn |
| test_rotate_selfreap.py `test_reap_chain_detached_nonchild_no_error` | 9.75s | same real spawn |
| test_level3.py `test_no_engine_signature...` | 7.44s | engine file scan |
| test_rotate.py ~20 `read_ack_*` tests | 2.00s each | a 2s poll sleep on the existing seam |

### The bottom line

Top three seam targets account for **~182s of 693s ≈ 26% of the whole suite.**

The single largest block is the two "real judge" measurement files
(~104s + ~47s = **~150s ≈ 22%**) hitting OpenRouter sequentially per corpus
body. That is PAID spend on every full run. They already `skipif` when
`OPENROUTER_API_KEY` is unset, but the moment a key is present the default
suite silently pays ~150s.

## Real sleeps / spawns located

- `extensions/agi/src/stream_master/semantic_screen.py` — `ModelJudge.judge`
  makes a sequential HTTP POST to `openrouter.ai` per body (URL at line 51; no
  concurrency, no batch). That is the real network "sleep" behind ~150s.
- `extensions/agi/tests/test_grid.py:274-299` — the sanitize test loops every
  corpus id and `subprocess.run(["git","check-ref-format", ...])` once per node
  (2974 files, ~30s). Cleanest spawn seam: batch or validate in-process.
- `extensions/agi/tests/test_rotate_selfreap.py:14-16` already carries seams
  (`sleep_impl`, `timeout_s`); the ~28s there is the detached-tree reap tests
  driving REAL sleeps by design, plus `_spawn_nonchild_sigterm_immune` (L307),
  a non-child SIGTERM-immune spawn that cannot be faked away.
- `extensions/agi/tests/test_rotate.py` — ~20 `read_ack_*` tests each pay a 2s
  poll; already on a seam, cheap individually, ~40s summed.

## Seams to add (for a child build node)

1. Put the live-model judge behind an OPT-IN marker: conftest collects a
   `real`-marked test and auto-skips it unless `-m real`. A bare key must not
   cost the default suite ~150s. Coverage preserved under the opt-in flag —
   gated, not masked.
2. `test_grid.py` sanitize: replace the per-node subprocess with a batched
   `git check-ref-format` or an in-process ref validator; keeps the assertion,
   drops ~30s of spawns.
3. Keep the genuine detached-tree reap tests — their sleep/spawn is the point
   and they are already on seams.

## Evidence

`--durations=40` tail captured verbatim:

```
........ [100%]
FAILED test_stream_master_semantic_screen.py::...::test_zero_novel_escapes
1 failed, 3903 passed, 8 skipped, 1 xfailed in 693.10s (0:11:33)

slowest 40 durations (top entries):
  95.29s call  blind_measure_v2 ...::test_measure_and_report_escapes
  43.64s call  semantic_screen ...::test_zero_novel_escapes
  30.85s call  test_grid.py::test_sanitize_real_agi_tree_corpus_round_trips_distinctly
  18.81s call  rotate_selfreap ...::test_reap_belam_oldest_pane_seam_detached_tree
   9.75s call  rotate_selfreap ...::test_reap_chain_detached_nonchild_no_error
   9.26s call  blind_measure_v2 ...::test_no_false_positives_on_fresh_benign
   7.44s call  test_level3.py::test_no_engine_signature_contains_an_fstring
   ... ~20 x 2.00s read_ack_* poll tests
```

Corpus size measured: **2974** `.md` files under `.agi/nodes` + `deprecated`.

Pre-fix state now recorded. The follow-on is a build/mvp: put the real-judge
network calls and the grid sanitize subprocess spawns behind seams, then re-run
the suite to measure how much the leg creeps back.

## Agent Notes
Measured full engine suite: 693s; top 3 seam targets = 26%. Real-judge files (blind_measure_v2 + semantic_screen) hit OpenRouter ~150s/22% paid. test_grid sanitize spawns git check-ref-format once per 2974 nodes (~30s). Located exact seams; need opt-in 'real' marker + batched ref validation.

REVIEW SL7.77 parent a00-a049d291: accepted as the BASE MEASUREMENT half of the round, not as a finished round. It measured the globbed suite (693.10s, 3903 passed) and located the cost sources; it implemented no seam and ran the suite once, which the FIX-ONLY target forbids as an end state. The fix half landed in sibling experiment:a00-4d9f6b08-dc569e (seams built, second run recorded, residue named). Caveat carried forward: this 693s base is on a GLOBBED selection (164 files incl. subdirs) that is broader than the sibling run (4133 passed), so 693 vs 606 is not a like-for-like total; and the brief cites the leg at 343-417s, so the declared tests-command selection is still un-reconciled. The failure it saw (test_zero_novel_escapes) is an intermittent live-model parity flake - it passed in the sibling run and fails on re-run - not a seam defect. Confidence 0.7 stands for the measurement it claims, not for the target goal.
