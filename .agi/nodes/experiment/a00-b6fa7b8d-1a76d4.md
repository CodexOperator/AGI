---
id: experiment:a00-b6fa7b8d-1a76d4
mint_id: 8759ab9aea73419c891329cc22a4665d
type: experiment
parents:
  - hypothesis:l5-drift-refusal-prints-its-message-once-not-twice
next_edges: []
confidence: 0.95
edited_by: a00-bada6e8e
evidence_runs:
  - experiment:a00-b6fa7b8d-1a76d4
line_ceiling: 40
loop: hypothesis:l5-drift-refusal-prints-its-message-once-not-twice@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python3 .agi/sessions/iter-L5.10/a00-bada6e8e/probe_l5_drift_once.py (gate section)", "expected": "rc==2 and exactly ONE stderr line 'rename-post REFUSED: staged plan drifted', drifted surface named, stage intact, nothing applied", "observed": "rc=2; count=1; 'old.extra' named; stage exists; no new.key. PASS", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "python3 .agi/sessions/iter-L5.10/a00-bada6e8e/probe_accept_and_loadbearing.py (accept section)", "expected": "a NON-drifted stage is NOT refused: rc==0, zero drift lines, stage consumed -- the single line must be the drift refusal's, not a blanket print", "observed": "rc=0; count=0; stage consumed. PASS", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "probe_l5_drift_once.py (wire section): duplicate re-injected into a scratch COPY of extensions/agi/bin/rotate.py, helper called on a real drift stage", "expected": "the injected duplicate appears in stderr -> the drift call path reaches the changed bytes live, not a stub", "observed": "count of the refusal line == 2 with the duplicate injected, rc==2. PASS", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "probe_accept_and_loadbearing.py (load section): duplicate re-injected into the REAL rotate.py, then pytest extensions/agi/tests/test_rotate_boundary_rename.py::test_boundary_drift_refuses_and_leaves_stage", "expected": "the kid's own new assertion FAILS with the duplicate restored -> the assertion is load-bearing and the deletion is what makes it pass", "observed": "1 failed: assert 2 == 1 at test_rotate_boundary_rename.py:119; rotate.py restored byte-identical; suite then 7 passed. PASS", "result": "pass"}
production_lines: 1
profile: balanced
role: kid
scaffold_hash: f25174042ca6c1c6
season: 2
title: Drift refusal prints its named line exactly once
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b6fa7b8d-1a76d4

## Experiment

BUILD ORDER (g15), not a measurement. The pre-fix state was measured, the
claim was built, then proved on the built bytes.

**Pre-fix (measured, HEAD 20aa9dd07 at cut):** `_apply_staged`'s drift branch in
`extensions/agi/bin/rotate.py` printed TWO stderr lines -- L3967 the named line
(`rename-post REFUSED: staged plan drifted -- <names>`) and L3970 the bare
duplicate (`rename-post REFUSED: staged plan drifted`). A scratch probe that
restores the deleted line into a copy of the file counts the string
`rename-post REFUSED: staged plan drifted` **2** times pre-fix and **1** time
post-fix (`.agi/sessions/iter-L5.10/a00-b6fa7b8d/rotate_prefix_probe.py`).

**Fix:** deleted the L3970 bare duplicate. Only the named line survives, so the
drift refusal still names the drifted surfaces. Return code (2) and refusal
semantics unchanged; the stage is still left intact.

Diff (`git diff --numstat -- extensions/agi/bin/rotate.py`): `0	1` -- one
deleted production line, zero added. Production lines touched: 1 (well under
the 40-line ceiling).

```
@@ -3967,7 +3967,6 @@
         print("rename-post REFUSED: staged plan drifted -- "
               + _refusal_names([...]),
               file=sys.stderr)
-        print("rename-post REFUSED: staged plan drifted", file=sys.stderr)
         return 2
```

**Regression assertion:**
`test_rotate_boundary_rename.py::test_boundary_drift_refuses_and_leaves_stage`
now asserts, next to the existing `rc == 2` / `"old.extra" in err` / stage-intact
checks:

```python
assert err.count("rename-post REFUSED: staged plan drifted") == 1, err
```

`str.count` is the assertion, per the order. The count is over the full-prefix
string so it matches both the pre-fix bare line and the named line -- pre-fix it
returns 2 and the assertion fails; post-fix it returns 1.

```
$ python3 -m pytest extensions/agi/tests/test_rotate_boundary_rename.py -q
7 passed, 22 warnings in 1.58s
```

## Evidence

- `git diff --numstat -- extensions/agi/bin/rotate.py` -> `0	1`
- scratch probe `rotate_prefix_probe.py`: `pre-fix count: 2` / `post-fix count: 1`
- `grep -n "staged plan drifted" extensions/agi/bin/rotate.py` -> exactly one
  hit (L3967, the named line)
- suite pass line: `7 passed, 22 warnings in 1.58s`

## Agent Notes
Deleted the bare duplicate drift-refusal print in rotate.py; test now asserts err.count(named line)==1; suite 7 passed

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (L5.10, a00-bada6e8e). Reviewed the DIFF, not the result file:
`git diff 20aa9dd07..361e00884` carries exactly three hunks -- rotate.py `0 1`
(one deleted production line), test_rotate_boundary_rename.py `1 0` (one added
assertion), and the kid's own node. All three deliverables named in my orders
are present in the bytes. Kid set its own title. Verdict `proved` stands.

(1) WHAT THE INSTRUCTION SAID. The parent brief: "A kid's tests are its CLAIM,
not your evidence... read each kid's DIFF... Run one negative probe per claim
conjunct yourself and record them as `probes:`; a kid that passes its own suite
but fails your probe is `lean_disproved` with the probe named."

(2) WHAT THE MACHINE ACTUALLY DOES. Two probe scripts I BUILT AND RAN
(`.agi/sessions/iter-L5.10/a00-bada6e8e/probe_l5_drift_once.py` and
`probe_accept_and_loadbearing.py`, both ALL PASS):
  - gate: real drift stage -> rc==2, `err.count("rename-post REFUSED: staged
    plan drifted")==1`, drifted surface named (`old.extra`), stage left intact,
    no `new.key` written.
  - gate-accept: a NON-drifted stage -> rc==0 and ZERO refusal lines, stage
    consumed. So the single line is the drift refusal's, not a blanket print.
  - wire: re-injected the deleted duplicate into a scratch COPY of
    extensions/agi/bin/rotate.py -> the helper printed it, count 2. The call
    path reaches those bytes live; a stub would never see it.
  - load-bearing: re-injected the duplicate into the REAL rotate.py and ran the
    kid's own new test -> `assert 2 == 1` FAILED at
    test_rotate_boundary_rename.py:119. File restored byte-identical (probe
    asserts this), suite then `7 passed, 22 warnings in 1.49s`. The assertion
    is what makes the fix stick.

(3) THE NEAR MISS. A kid that deleted the line WITHOUT the count assertion
would pass its own suite and satisfy the words of my orders, while leaving the
defect free to return: the existing assertion `"staged plan drifted" in err` is
a substring test that is true for one line and for two. That is exactly the
plausible implementation my load-bearing probe kills -- and it is why I ran the
test rather than reading it.

(4) DEVIATION, WITH THE PROPERTY THAT JUSTIFIES IT. My first `auth`-class probe
assumed the drift gate was boundary-only and FAILED: the branch at
rotate.py:3966 sits OUTSIDE the `if boundary:` guard, so a non-boundary caller
is refused too (measured: rc==2 with `boundary=False`). I did not count a failed
probe as coverage and did not re-cut the kid over it -- the claim never says the
gate is boundary-gated, so the premise was mine, not the kid's defect. Recorded
as a caveat instead. No numbered `(1) (2)` conjuncts exist in this hypothesis,
so cli.py's `_parent_probe_gate` (cli.py:1190-1234) resolves an empty conjunct
set and is inert here; I recorded the probes anyway because an unevidenced
proved is worth less than an evidenced one.

caveats: the drift refusal is not boundary-gated (rotate.py:3966) -- a
non-boundary `_apply_staged` caller is refused too; out of scope for this node,
worth its own.
<!-- THOUGHT:END -->

Parent review L5.10: diff carries all three deliverables (rotate.py -1 line, test +1 assertion, kid node). Ran 4 parent probes (gate, gate-accept, wire, load-bearing) -- ALL PASS. Load-bearing probe re-injected the duplicate into the real rotate.py and the kid's assertion failed 2==1; file restored byte-identical, suite 7 passed. Verdict proved accepted. Caveat recorded: drift gate is not boundary-gated.
