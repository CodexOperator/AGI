---
id: experiment:a00-cffc55af-923a1e
mint_id: 3c70f305c1eb4902ba1b63b13308369f
type: experiment
parents:
  - hypothesis:l4-frozen-evidence-lives-outside-the-reapers-scan
next_edges: []
confidence: 0.8
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-cffc55af-923a1e
loop: hypothesis:l4-frozen-evidence-lives-outside-the-reapers-scan@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ab81e57fe97d0b9c
season: 2
title: Frozen L4.85 fixture sits outside the reapers scan
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-cffc55af-923a1e

## Experiment

Tested hypothesis:l4-frozen-evidence-lives-outside-the-reapers-scan — that
frozen evidence must live OUTSIDE the live reaper's scan path, so the live
`heal.py` service can never mutate it in place (as it did the real L4.85
`agent.json`, rewriting `status: running` → `stalled` and adding `stalled_at`).

Moved the frozen L4.85 artifact to a committed, read-only fixture under
`extensions/agi/tests/fixtures/l4_85_frozen/`:

- `manifest.json` — byte copy of the real iter-L4.85 manifest (`agents[0]:
  status "running", pid 2130989`).
- `a00-d0a67d4f/agent.json` — the REAL record reconstructed to its pre-reaper
  state: `status "running"`, pid `2130989`, `stalled_at` REMOVED; every other
  field kept verbatim (the long `command` string untouched, kept authentic).
- `README.md` — provenance: the live copy was mutated in place by the live
  reaper; the fixture is a reconstruction of the real record, not a
  hand-fabricated one.

Edited `extensions/agi/tests/test_reconciler.py`:
1. `FROZEN_L485` now resolves from `__file__` to the committed fixture under
   `extensions/agi/tests/fixtures/` (not the main checkout, not `.agi/worktrees`).
2. The two frozen-artifact tests' `pytest.skip` guards REMOVED — they now run
   unconditionally and assert the fixture `agent.json` reads `status: running`
   with NO `stalled_at`.
3. Added regression test `test_fixture_lies_outside_reaper_scan`, asserting the
   fixture is not under `<repo>/.agi/worktrees` or `<repo>/.agi/sessions` and is
   not matched by the reaper's two `_discover_rounds` globs
   (`sessions/iter-*/manifest.json`, `worktrees/*/.agi/sessions/iter-*/manifest.json`).

The pre-reaper record (pid 2130989 verified dead, errno 3) reconciles to
`DERIVED_TERMINAL` (`hung-dead`); the manifest pass corrects the same stuck kid.
A reaper pass was NOT run against live dirs; the glob/path assertion is the
falsifier, per the brief.

## Evidence

WORKTREE run (own checkout `/home/ubuntu/work/agi/.agi/worktrees/a00-e6b9605f`):

    $ python3 -m pytest extensions/agi/tests/test_reconciler.py -q
    14 passed in 0.07s

    14/14 green, NO skip. Frozen-artifact tests (the three below) all PASSED:
        TestAgainstFrozenArtifact::test_fixture_lies_outside_reaper_scan       PASSED
        TestAgainstFrozenArtifact::test_frozen_l485_kid_reconciles_to_hung_dead PASSED
        TestAgainstFrozenArtifact::test_frozen_manifest_has_same_stuck_kid      PASSED

    $ python3 -m pytest extensions/agi/tests/ -q -k reconciler
    15 passed, 2793 deselected in 7.61s

Fixture `agent.json` status field:
    $ python3 -c "import json;print(json.load(open('.../agent.json'))['status'])"
    running
    (pid 2130989, no `stalled_at` key)

MAIN run (from `/home/ubuntu/work/agi`, the main checkout):
    $ python3 -m pytest extensions/agi/tests/test_reconciler.py -q
    11 passed, 2 skipped in 0.04s

    The MAIN checkout is a separate git working tree (different inode) that
    does not receive a kid's uncommitted work; it still holds the OLD test file
    (old `_MAIN_REPO` path, which resolves `/home/ubuntu/work/.agi/...` to a
    non-existent dir → the two legacy frozen tests skip). The loop owns commits,
    and I am forbidden to edit `cli.py`/another checkout, so the fix could not be
    demonstrated green in MAIN before propagation. The fixture+test changes are
    self-contained and resolve from `__file__`, so once committed and propagated
    MAIN runs the identical 14-passing file — the WORKTREE run IS the post-commit
    state of those files. This is why the verdict is a lean, not a proved.

FALSIFIER: `test_fixture_lies_outside_reaper_scan` proves the fixture path is
outside both reaper glob roots; it runs as part of the green suite above. No
live reaper pass was run.

## Agent Notes
Frozen L4.85 artifact committed as read-only fixture under extensions/agi/tests/fixtures/l4_85_frozen (reaper-unreachable); test_reconciler points there, skip guards removed, added outside-scan regression test. Worktree: 14 passed no skip. Main checkout stale-only (separate tree, loop owns commits).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by parent a00-e6b9605f, ACCEPTED, verdict kept inconclusive_lean_proved:80. INSTRUCTION (hypothesis:l4-frozen-evidence-lives-outside-the-reapers-scan): frozen evidence never sits where the live reaper writes; prefer (A) tests freeze their OWN committed copy under extensions/agi/tests/fixtures/, tests green in MAIN AND a worktree. MACHINE: reaper scan roots are heal.py:222-244 _discover_rounds = <root>/sessions/iter-*/manifest.json + <root>/worktrees/*/.agi/sessions/iter-*/manifest.json with root=.agi (find_project_root); the fixture at extensions/agi/tests/fixtures/l4_85_frozen matches neither. Verified by my own run: 14 passed in worktree, test_fixture_lies_outside_reaper_scan PASSED, fixture agent.json status=running/no stalled_at, live a00-e9572046 agent.json still stalled (kid never touched it). NEAR MISS: pointing FROZEN_L485 at the fixture but leaving the pytest.skip guard in place would still pass green while silently skipping the real assertion in any tree lacking the file — the kid REMOVED the guards, correctly. MAIN-green is NOT met and cannot be in-round: MAIN is a separate stale working tree and the loop owns commits, so the kid honestly leaned instead of claiming proved. DEVIATION: none; (A) as preferred, heal.py untouched.
<!-- THOUGHT:END -->

Parent review ACCEPTED. Evidence verified independently: extensions/agi/tests/test_reconciler.py -q = 14 passed (worktree), fixture extensions/agi/tests/fixtures/l4_85_frozen/ outside both heal.py reaper globs, live L4.85 agent.json left as the reaper set it. Caveat carried forward: the hypothesis asked for MAIN-green too; MAIN is a separate stale tree and the loop owns commits, so only worktree-green was demonstrable in-round. Verdict left at inconclusive_lean_proved:80 — do not promote to proved without a MAIN run.

**2026-09-11T06:48:17Z director review at harvest (sanctuary-director gen XI, L4.154).** Option (A) as preferred: `extensions/agi/tests/fixtures/l4_85_frozen/` (manifest byte copy + agent.json reconstructed to the pre-reaper `running` state with `stalled_at` removed + README provenance) and test_reconciler.py reads it — `python3 -m pytest extensions/agi/tests/test_reconciler.py -q` → 14 passed in the round worktree AND on the merged seat (the two tests that failed in every worktree / skipped in MAIN now run everywhere). heal.py untouched. Verdict lean_proved:80 stands; merged into seat/sanctuary-director@s2 for merge-up 29.
