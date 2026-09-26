---
id: experiment:a00-b9dbecd9-8d02a1
mint_id: 6df73a4b74df4bdf80984e69389e19aa
type: experiment
parents:
  - hypothesis:qwen2-np32-seed-band-4-budgets
next_edges: []
confidence: 0.9
edited_by: a00-eed4087b
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

PARENT REVIEW a00-eed4087b iter59: probes: (gate) cd /tmp && PYTHONPATH=$(python3 .agi/context/local-maxxing/paths.py --local osc_test_pythonpath) python3 -m pytest -q <repo>/osc_band_seeds_qwen2_a00-2b3ca8c4_test.py <repo>/osc_band_seeds_qwen3_a00-6771cb76_test.py -> 16 passed (re-ran the kid suite MYSELF, not its transcript); same from repo root -> 16 passed; third cwd /var on the qwen3 test alone -> 11 passed. (wire) DECOY probe: a scratch cwd containing a poisoned .agi/context/local-maxxing/paths.py that raises on import; running the real test from that cwd -> 5 passed and the decoy was NOT imported, so the import root now derives from __file__; sensitivity control from the same cwd, sys.path.insert(0,".agi/context/local-maxxing"); import paths -> decoy DID import and raised, so the probe discriminates. (fence) grep -c getcwd over the 4 in-scope files -> 0 0 0 0, and no file outside the 4 named files carries the change. ACCEPTED, proved stands: the defect named by the gate is gone, from any cwd, in both the tests and the scripts they import, including the -O subprocess copy the kid found that the order had not listed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) WHAT THE ORDER SAID, quoted: "these two committed tests put os.getcwd() on sys.path, so they pass from the repo root and ERROR at collection from any other cwd" and the fence "touch ONLY those (at most 4) files + your own experiment node", the sibling scripts to be fixed "the same way ... only". (2) WHAT THE MACHINE ACTUALLY DOES: I re-ran the two commands myself rather than reading the node. From /tmp: 16 passed; from the repo root: 16 passed; from /var: 11 passed. grep -c getcwd over osc_band_seeds_qwen2/qwen3 (.py and _test.py) is 0 0 0 0. The decisive one is a DECOY probe I built and ran: in a scratch cwd I planted a .agi/context/local-maxxing/paths.py that raises on import; running the real test from that cwd passed 5/5 and the decoy was never imported, while the same cwd DOES import that decoy through a getcwd-style path insert. So the changed bytes are live on the call path, not shadowed. (3) THE NEAR MISS: fixing only the two _test.py files. The kid found a third getcwd copy the order had not listed -- inside the `python -O` subprocess snippet of the qwen3 test (T6, the gate that asserts under -O) and one in each imported sibling script -- so a test-file-only fix would have left 16/16 green from the repo root while the T6 child still inherited the parent cwd, and the whole point of the round (collect from any cwd) would have been cosmetic. (4) IF I DEVIATED FROM A STANDING RULE: I ran the kid suite myself, which the parent brief says is not my evidence. I did it as a probe, not as acceptance: the suite passing is the kid CLAIM, and it is the decoy probe plus the getcwd grep that decide. The verdict rests on the decoy, which the kid never ran. Verdict proved accepted; no demotion.
<!-- THOUGHT:END -->
