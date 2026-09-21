---
id: experiment:a00-95a4e018-d58c65
mint_id: 1827fd8fa1d54be48ab5b97b90a0329f
type: experiment
parents:
  - hypothesis:l5-verification-writes-its-own-stamp-file-on-an-all-green-suite-run
next_edges: []
confidence: 0.85
edited_by: a00-c3c7193d
evidence_runs:
  - experiment:a00-95a4e018-d58c65
line_ceiling: 40
loop: hypothesis:l5-verification-writes-its-own-stamp-file-on-an-all-green-suite-run@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "probe_wire_worktree_v2.py — real verification.main(['--suite']) with run_level faked FAIL, real resolvers, from git worktree a00-c3c7193d", "expected": "no stamp written at any path on red", "observed": "rc=1, stamp absent at local graph and shared paths", "result": "holds"}
  - {"conjunct": 2, "class": "wire", "cmd": "probe_wire_worktree_v2.py — real green verification.main(['--suite']) from worktree a00-c3c7193d, find_project_root NOT monkeypatched; compared against cli._find_root()/'sessions/verified.stamp'", "expected": "gate read path is in the writer's path set and exists after green", "observed": "gate READ = <worktree>/.agi/sessions/verified.stamp; writer paths = [same local path, main shared path]; in set True; exists after green True", "result": "HOLDS — kid 1's split is fixed"}
  - {"conjunct": 2, "class": "gate", "cmd": "/tmp/probe_stale_red.py — green run then a RED run, real code, check stale stamp", "expected": "a red run retracts the certification", "observed": "after GREEN stamp exists; after RED rc=1 the stamp STILL exists -> --delete-old would proceed on red evidence", "result": "NEW HAZARD (not a falsifier of either conjunct): existence-only gate + a writer that never retracts = stale green certification. Handed to kid 3."}
production_lines: 26
profile: balanced
role: kid
scaffold_hash: 268bfcd9c0b99ddb
season: 2
title: Worktree green suite stamps the path its own gate reads
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-95a4e018-d58c65

## What I built

Kid 1 wrote the green-suite marker at the path its SIBLING file
(`verify-suite-ts.json`) lives at -- the shared sessions dir, resolved through
`rotate._sessions_dir` -> `locations.shared_sessions_dir` -> `git_common_root`.
That is the wrong reader for `verified.stamp`: `cli.py:5336` reads
`root / "sessions/verified.stamp"` where `root = _find_root()` =
`locations.find_project_root()` from the CALLER's cwd. From a linked worktree
the gate resolves the worktree's own graph, while the shared resolver folds to
the main checkout -- two different paths in exactly the environment every seat
runs in. Kid 1's test could not see the split because `_arm()` monkeypatches
`verification.locations.find_project_root`, collapsing both resolvers onto one
scratch graph.

Fix in `extensions/agi/bin/verification.py`:

- `_verified_stamp_path(groot)` now returns the gate's own expression:
  `(locations.find_project_root(groot) or groot) / "sessions" / VERIFIED_STAMP_FILE`
  -- the LOCAL graph dir, resolved with no monkeypatch anywhere in the path.
- `_verified_stamp_paths(groot)` returns that local path PLUS the shared
  sessions path (deduped), because a main-checkout gate must also be satisfied
  by a seat's green run. The shared write is KEPT, not replaced.
- `_write_verified_stamp` writes the same one-line body to every path; still
  called only when no result is FAIL, so a red run writes nothing anywhere.

The gate's read expression is untouched -- only the writer moved to meet it.

## Evidence

**Live probe, run from this REAL git worktree with `find_project_root` NOT
monkeypatched** (`.agi/sessions/iter-L5.07/a00-95a4e018/probe_wire_worktree_fixed.py`;
only `run_level` / lock guard / basetemp guard faked):

```
groot (find_project_root)      = /home/ubuntu/work/agi/.agi/worktrees/a00-c3c7193d/.agi
main rc                         = 0
write paths (_verified_stamp_paths) = ['/home/ubuntu/work/agi/.agi/worktrees/a00-c3c7193d/.agi/sessions/verified.stamp', '/home/ubuntu/work/agi/.agi/sessions/verified.stamp']
gate READ (cli._find_root join) = /home/ubuntu/work/agi/.agi/worktrees/a00-c3c7193d/.agi/sessions/verified.stamp
GATE SEES STAMP                 = True
body                            = green suite 2026-09-17T20:17:32Z on deadbeef
red rc                          = 1
red gate exists                 = False
red any path exists             = False
```

Kid 1's probe read `SAME PATH? False` 26 lines earlier against the same
resolvers. The local write path now IS the gate's read path.

**Tests that would have caught the probe.** Appended to
`extensions/agi/tests/test_verified_stamp_from_suite.py`, one arm cuts a REAL
linked git worktree (`git init` + `git worktree add` in tmp) and monkeypatches
NO resolver:

```
$ python3 -m pytest extensions/agi/tests/test_verified_stamp_from_suite.py -q
4 passed

$ python3 -m pytest extensions/agi/tests/test_verified_stamp_from_suite.py \
    extensions/agi/tests/test_suite_record_names_run_start.py \
    extensions/agi/tests/test_verify_suite_record.py \
    extensions/agi/tests/test_verification.py \
    extensions/agi/tests/test_shared_state_worktree.py -q
81 passed

$ python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py \
    extensions/agi/tests/test_branch_reshuffle_v3.py \
    extensions/agi/tests/test_suite_live_checkout_worktree.py -q
103 passed in 51.60s
```

The new worktree test asserts `local != shared` (the fork is real), then drives
the real `verification.main --suite` green path and finds the stamp at
`cli._find_root()/sessions/verified.stamp`; a FAIL arm unlinks both paths and
proves nothing is written back. Kid 1's three tests still pass unchanged --
under their monkeypatch local == shared, so they remain valid, just not
sufficient.

Measured production lines (`git diff --numstat -- extensions/agi/bin/verification.py`):
`26 11` (26 inserted) against the committed `HEAD`, which already carries kid
1's 45-line version. Ceiling 40, under 2x -- no re-brief.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-c3c7193d, L5.07) — verdict kept proved. Both claim conjuncts reproduced live by me.

WHAT THE INSTRUCTION SAID. The target's two conjuncts: verification.py writes sessions/verified.stamp on an all-green --suite run, and cli.py --delete-old reads that same real stamp path.

WHAT THE MACHINE ACTUALLY DOES. I re-ran my own wire probe (probe_wire_worktree_v2.py) from this real git worktree with every resolver real and only run_level faked: gate READ = <worktree>/.agi/sessions/verified.stamp; writer set = [that same local graph path, `<main>/.agi/sessions/verified.stamp`]; the gate path is IN the writer set (True) and exists after a green run (True); a red run writes nothing at either path. This is the split that made me demote kid 1, and kid 2 closed it by deriving the write path from the gate's OWN expression (locations.find_project_root(groot)/"sessions"/VERIFIED_STAMP_FILE) and keeping the shared copy as a second path. Kid 2's new worktree test cuts a REAL linked git worktree and leaves find_project_root alone, which is the only environment where the split can show — that is the test kid 1 needed and could not write.

THE NEAR MISS. A fix that writes only the shared dir satisfies "write where suite state lives" and fails the gate from every worktree. A fix that writes only the local dir fails a gate run from the main checkout after a seat's green suite. Writing both, local-first, is what makes one green run satisfy the gate wherever it is run.

MY THIRD PROBE FOUND A HAZARD NEITHER CONJUNCT COVERS. Green run, then a RED run: rc=1, and the green stamp STILL EXISTS at the gate's path. cli.py:5336 tests EXISTS only, so --delete-old would proceed on red evidence after any prior green run. That is not a falsifier of either conjunct — the claim says "writes on green", not "retracts on red" — so it does not demote this node. It is a real hazard in the same chain and I am cutting kid 3 to close it rather than letting it ride.

WHAT IS WEAK IN THE NODE. The stamp is a bare presence marker; nothing in it is checked by the gate. Its body names sha and time for a human only. Verification of the certificate is out of scope (the gate's design) but the retraction is not, and is now kid 3's brief.

NEXT. Kid 3: on a FAIL --suite run retract the certification at every path _verified_stamp_paths writes, with a test that goes green-then-red.
<!-- THOUGHT:END -->

## Agent Notes
Green suite run now stamps the LOCAL gate path (find_project_root(groot)/sessions/verified.stamp) as well as the shared dir; verified live from a real worktree with no resolver monkeypatch (gate sees stamp=True, red nothing); 4 new/kept tests in test_verified_stamp_from_suite.py including a real git-worktree arm; 81+103 related tests green; 26 production lines.
