---
id: experiment:a00-a8960e30-05d355
mint_id: 6d0072864990478f9e34df4440a8436e
type: experiment
parents:
  - hypothesis:lm-grid-storage-trunk-code-fix-remaining-literal-sites
next_edges: []
confidence: 0.85
edited_by: a00-adbb729a
evidence_runs:
  - experiment:a00-a8960e30-05d355
line_ceiling: 200
loop: hypothesis:lm-grid-storage-trunk-code-fix-remaining-literal-sites@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent_probe.py PROBE A", "expected": "a configured storage_trunk refs/grid/t7 is seen at all six sites", "observed": "all six resolve refs/grid/t7", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "parent_probe2.py PROBE C", "expected": "unconfigured fetch refspec is refs/grid/*:refs/grid/* with no plus; configured maps src to dst", "observed": "unconfigured [refs/grid/*:refs/grid/*]; configured [refs/grid/t7/*:refs/grid/t7/*]; no plus in either", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "grep the six call-site lines; pytest -k rotate or unify or verify or grid or cli", "expected": "no literal decides a site; named suites green", "observed": "NONE literal; 1506 passed, 1 xfailed", "result": "pass"}
production_lines: 5
profile: balanced
role: kid
scaffold_hash: 535da6a50d3a2fab
season: 2
title: "Fix unify fetch refspec: drop the force-update plus, unconfigured fetch byte-identical to the original literal"
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a8960e30-05d355

## Experiment

Fixed the one falsified site from kid EF.07#1: `unify.fetch_grid_refs` now
sends a `+`-free refspec, so on this unconfigured box the fetch argv is
byte-identical to the pre-change literal.

### The defect

The original module constant, read straight out of the pre-change tree:

```
$ git show aca936de0:extensions/agi/bin/unify.py | sed -n '129,130p'
GRID_REF_NAMESPACE = "refs/grid"
GRID_FETCH_REFSPEC = "refs/grid/*:refs/grid/*"     <-- NO plus
```

consumed by the fetch at `unify.py:897` of that commit. Kid #1 replaced it with
`f"+{src_ns}/*:{dst_ns}/*"`, which unconfigured is `+refs/grid/*:refs/grid/*`
— one byte, and a semantic byte: the `+` forces a non-fast-forward update that
the original fetch refused. Falsifier (b) fired on this site alone; the parent
demoted `proved -> inconclusive_lean_disproved:70`.

### The fix (unify.py, one line + its comment)

Before (kid #1):

```
_git(engine, "fetch", "-q", remote_name, f"+{src_ns}/*:{dst_ns}/*")
```

After (this round):

```
_git(engine, "fetch", "-q", remote_name, f"{src_ns}/*:{dst_ns}/*")
```

No `+`, and `grid.fetch_spec_for` is deliberately NOT used: it carries the `+`
that belongs to a push, not this fetch. The false comment "byte-for-byte the
old constant" was replaced with a comment that states the no-plus invariant
and why `push_spec_for` is the wrong helper here.

## Evidence

### Unconfigured fetch refspec is now exactly the old literal

`extensions/agi/tests/test_unify.py::test_grid_namespace_reads_the_projects_storage_trunk`
extended (no fifth fixture minted) to record the fetch argv via a recorder on
`unify.subprocess.run`, faking only the fetch call (no remote in the fixture):

- unconfigured, both sides: `refs/grid/*:refs/grid/*`, and asserted to carry
  no leading `+` on any recorded ref arg;
- configured, both sides `refs/grid/t9`: `refs/grid/t9/*:refs/grid/t9/*`,
  also `+`-free.

```
python3 -m pytest extensions/agi/tests/test_unify.py -q -k "storage_trunk"
-> 1 passed, 63 deselected
```

### Named suites green

```
python3 -m pytest extensions/agi/tests/test_rotate_closeout.py \
  test_rotate_closeout_steps.py test_unify.py test_verify_unified.py \
  test_grid.py test_cli.py -q
-> 312 passed, 69 warnings in 20.69s
```

### Production lines

`git diff --numstat -- extensions/agi/bin/unify.py` -> 5 added, 2 removed
(net 3). Ceiling 200 — well under, no re-brief. Test file changed: 44 added
lines, excluded from the count.

## Residual

The configured-configured leg (`refs/grid/t9` on both sides) is now measured,
closing kid #1's note 1 for the equal-namespace case. The source-namespace !=
target-namespace case (e.g. tree on `t9`, engine on default) is still reasoned,
not measured: it spells `refs/grid/t9/*:refs/grid/*`, which is correct by
construction but has no fixture. Out of scope, as the brief scoped it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (EF.07) -- ACCEPTED proved. This kid corrects the one site that falsified its predecessor.

(1) WHAT THE ASSIGNMENT SAID: make unify.fetch_grid_refs send, on the unconfigured box, exactly refs/grid/*:refs/grid/* (no plus) while still mapping source and target namespaces for a configured trunk; keep the round at <=4 new fixtures by extending an existing one; do not touch the out-of-scope rotate print labels.

(2) WHAT THE MACHINE ACTUALLY DOES: the diff 75b6b30ee..6ed89dc1c changes the fetch argument to f"{src_ns}/*:{dst_ns}/*" -- no plus -- and rewrites the false comment. My own probe (parent_probe2.py, not the kid suite) captures the live fetch argv: unconfigured [refs/grid/*:refs/grid/*] and configured [refs/grid/t7/*:refs/grid/t7/*], no plus in either. Falsifier (a) re-run by grep: NONE of the six call-site lines is decided by a literal. The named suites re-run by the parent: 1506 passed, 1 xfailed.

(3) NEAR MISS: keeping the plus because grid.fetch_spec_for carries one -- the wrong helper for a fetch whose original semantics refuse a non-fast-forward update. The kid named that in the comment rather than importing it, which is the correct call.

(4) DEVIATION: none. The kid extended test_grid_namespace_reads_the_projects_storage_trunk with a fetch-argv recorder (plus a helper), so the round total stays at 4 new fixtures as briefed. Title is the kid own words.
<!-- THOUGHT:END -->

## Agent Notes
unify.fetch_grid_refs now sends the +-free refspec; unconfigured fetch argv byte-identical to GRID_FETCH_REFSPEC (git show aca936de0:unify.py:130), configured t9->t9 measured; extended existing unify fixture, 312 named-suite tests green; 5 production lines
