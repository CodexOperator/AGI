---
id: experiment:a00-b9dbecd9-8d02a1
mint_id: 6df73a4b74df4bdf80984e69389e19aa
type: experiment
parents:
  - hypothesis:qwen2-np32-seed-band-4-budgets
next_edges: []
confidence: 0.9
edited_by: a00-b9dbecd9
evidence_runs:
  - experiment:a00-b9dbecd9-8d02a1
loop: hypothesis:qwen2-np32-seed-band-4-budgets@s2
model: stealth/space-bunny-alpha
production_lines: 3
profile: balanced
role: kid
scaffold_hash: eb205f50d39b5a11
season: 2
title: seed-band tests collect from any cwd after the getcwd fix
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b9dbecd9-8d02a1
# experiment:a00-b9dbecd9-8d02a1 — getcwd-free sys.path in the two seed-band tests

## The defect (pre-existing, measured)
`osc_band_seeds_qwen2_a00-2b3ca8c4_test.py` and `osc_band_seeds_qwen3_a00-6771cb76_test.py`
put `os.getcwd()` on `sys.path`, so they only collected from the repo root. The two sibling
scripts they import did the same, so the defect survived the test file alone:
`osc_band_seeds_qwen2_a00-2b3ca8c4.py:10-11` (`ROOT = os.getcwd()`),
`osc_band_seeds_qwen3_a00-6771cb76.py:14`, and one MORE copy inside the T6 subprocess
snippet of the qwen3 test (a `python -O` child that would have run with the parent's cwd).
`grep -c getcwd` before: 5 hits over the 4 files.

## The fix — the P8.08 pattern (test_osc_band_headline_a00-c56b49c9.py)
```python
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.dirname(HERE), HERE]  # collect from any cwd
```
`os.path.dirname(HERE)` IS `.agi/context/local-maxxing` — the same import root, derived from
`__file__` instead of the process cwd. 3 production lines total; no literal repo path, no new
config cell, nothing else touched.

## Evidence — both commands, real output
PYTHONPATH resolved from the config cell
`paths.local_maxxing.osc_test_pythonpath` via
`python3 .agi/context/local-maxxing/paths.py --local osc_test_pythonpath` ->
`/data/ml/.venv/lib/python3.12/site-packages:/data/ml/scratch/osc03/pylib`

```
$ cd /tmp && PYTHONPATH="$PP" python3 -m pytest -q <repo>/…/osc_band_seeds_qwen2_a00-2b3ca8c4_test.py <repo>/…/osc_band_seeds_qwen3_a00-6771cb76_test.py
................                                                         [100%]
16 passed in 3.84s

$ cd <repo> && PYTHONPATH="$PP" python3 -m pytest -q .agi/…/osc_band_seeds_qwen2_a00-2b3ca8c4_test.py .agi/…/osc_band_seeds_qwen3_a00-6771cb76_test.py
................                                                         [100%]
16 passed in 3.04s

$ grep -c getcwd <the four files>
0 0 0 0
```

16 tests, both cwds, 0 `getcwd` left. The T6 subprocess gate (`-O` refusal still raises)
now also holds with an arbitrary parent cwd, because the child derives its own path too.

## Measurement
`git diff --numstat` over the two production scripts: 2/2 + 1/1 = 3 production lines
(ceiling 40; test-file edits excluded). No commit run — the loop owns it.

## Agent Notes
getcwd-free sys.path in both seed-band tests + both sibling scripts (incl. the -O subprocess snippet); 16 passed from /tmp and from repo root, 0 getcwd hits, 3 production lines
