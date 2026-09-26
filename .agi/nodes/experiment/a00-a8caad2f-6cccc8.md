---
id: experiment:a00-a8caad2f-6cccc8
mint_id: 6a722f2fa16447cbb3cae7bc5acd0925
type: experiment
parents:
  - hypothesis:a-captive-capture-rotates-even-when-its-driven-handoff-refuses
next_edges: []
confidence: 0.85
edited_by: a00-a8caad2f
evidence_runs:
  - experiment:a00-a8caad2f-6cccc8
loop: hypothesis:a-captive-capture-rotates-even-when-its-driven-handoff-refuses@s2
model: stealth/space-bunny-alpha
probes:
  - "auth: the registry gate still refuses the unregistered --name AFTER the merge (no seat probe-director, rc 1)"
  - "gate: _geometry_resolution_root is re-MEASURED after the merge, and --dry-run keeps the refusal with no merge"
  - "wire: the capture chain step order through the real _CHAIN_SCRIPT bash with stand-in argvs (no rotate.py, no seat)"
production_lines: 21
profile: balanced
role: kid
scaffold_hash: a697b966a111a0cd
season: 2
title: the geometry guard merged what it refused to wait for
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a8caad2f-6cccc8

## What I built (and where the cause actually was)

The brief pointed at the CAPTURE chain's second step. The cause is one line of
ORDER in `cmd_rotate_self`, and the chain needed no change at all.

| | file:line (pre-fix) | what it does |
|---|---|---|
| geometry guard | `extensions/agi/bin/rotate.py:18920` `_geometry_resolution_root` | refuses when the worktree geometry is behind and the integration tree is no substitute |
| the merge that fixes exactly that | `extensions/agi/bin/rotate.py:19168` `_prepare_checks(root, seat, perform=True)` | check 3 PERFORMS the only-behind merge (the SAME function `cmd_prepare` / `rotate-self --prepare` run) |

The guard ran at 18920, the merge at 19168 — so a behind worktree was refused
before the merge that would have made it current could ever run. Every trunk
move therefore made EVERY rotate refuse, the capture chain's rotate-self step
included (director engine 2026-09-26 17:01Z). The chain is a caller, not the
cause: it already calls the same entry the bare `rotate` verb delegates to, with
`--force` and `--stops` intact.

### The fix (21 production lines, `extensions/agi/bin/rotate.py` only)

At the guard: when the resolution is `None` AND this is not a `--dry-run`, run
the ONE existing merge — `_prepare_checks(root, args.name, perform=True)` — then
RE-MEASURE. If the geometry is current, the rotation continues. If the merge
still could not make it current (a dirty tree, a CONFLICTING merge, an
unmeasurable fetch), the checklist's own blocker lines are printed first
(`[BLOCK] …` / `clear: …`, the `cmd_prepare` spelling) and the geometry
refusal still closes, rc 1. `--dry-run` refuses exactly as before (a merge is a
touch). No second merge implementation, no chain change, no new config cell.

## Evidence

New test file `extensions/agi/tests/test_rotate_capture_geometry_merge.py`
(TMP bare `origin`, TMP clone standing in for the worktree, no real repo, no
real seat, no real /tmp state dir):

```
$ python3 -m pytest extensions/agi/tests/test_rotate_capture_geometry_merge.py -q
....                                                    [100%]
4 passed
```

RED on the pre-fix bytes (the guard restored by hand, the file byte-identical
afterwards) — the two behavioural tests fail, so they measure the defect:

```
FAILED test_behind_geometry_is_merged_not_refused          # pre-fix: "rotate-self refused"
FAILED test_conflicting_merge_is_refused_by_name_with_its_blockers
2 failed, 2 passed
```

- (1) behind by 1 geometry commit, clean tree: post-fix rc 1 is
  `ERR: no seat 'probe-director' in the seats registry` — the NEXT gate, not
  the geometry one — and `_geometry_behind_count(root) == 0` after the run, with
  `# v2` in the worktree's own `rotations.md`.
- (2) `--dry-run`: still `rotate-self refused … behind`, and nothing merged.
- (3) conflict: the seat's branch and the season branch both append to
  `rotations.md`, so the merge is not mechanical. Post-fix stderr carries
  `[BLOCK] behind origin/season2/main (1) — merge conflicts: …rotations.md`,
  then the geometry refusal; `_geometry_behind_count == 1` afterwards and no
  `<<<<<<<` in the file (never a half-merge).
- (4) chain wire: the real `_CHAIN_SCRIPT` bash, run with STAND-IN argvs
  (`python3 -c`), proves the capture child's steps stay sequential, so a merge
  performed before the rotation is the config the rotation reads.

Suites (the ones covering the bytes I changed, named — never a bare directory):

```
pytest extensions/agi/tests/test_rotate_capture_geometry_merge.py -q        4 passed
pytest extensions/agi/tests/test_rotation_alert_capture.py \
       test_rotation_alert_captive.py test_rotation_alert_capture_latch.py \
       test_rotation_alert_capture_safety.py -q                          35 passed
pytest $(ls extensions/agi/tests/test_rotate_*.py) -q        694 passed, 1 xfailed
```

`git diff --numstat` over the production paths: `21 0 extensions/agi/bin/rotate.py`
(ceiling 40; tests excluded).

## What is NOT covered here

No test drives a REAL `rotate.py` through a full rotation from inside the chain
(standing in for the seat is what keeps this safe). The chain-level proof is
ordering + stand-ins; the merge proof is at the rotate-self entry the chain
calls. A next round could drive the chain with a real rotate.py against a TMP
project that refuses at the spawn seam.

## Agent Notes
cause was ORDER in cmd_rotate_self: the geometry guard (18920) ran before the only-behind merge (_prepare_checks perform=True, 19168); the guard now performs that ONE existing merge and re-measures, --dry-run still refuses, conflicts named by the checklist blockers; 21 production lines, red-first tests in test_rotate_capture_geometry_merge.py
