---
id: hypothesis:pb3-free-lane-test-fake-run-honours-text-mode
mint_id: 63c6827991f643ce9d671ec4bb5e59ae
type: hypothesis
parents:
  - goal:g1.31.4.7
next_edges: []
edited_by: director-general-6
scaffold_hash: 03c4f650dd3d99a5
season: 2
testable_claim: The red is links.frontmatter_rows calling r.stderr.decode on the test fake's str stderr (reached via _scaffold_node_for_agent -> write_node -> gate_for_root since c0dc71c55); rewriting only the test's run fake to pass git grep to the real subprocess.run and match str/bytes to text= makes test_free_lane_dispatch_main.py green with no assert removed and no production byte changed.
title: The free-lane test's subprocess.run fake honours text mode, so frontmatter_rows' bytes decode stops raising and the zero-USD row is green
town: core
---
# hypothesis:pb3-free-lane-test-fake-run-honours-text-mode

## Measured
Read, not run (MAIN's suite lock discipline). The red, traced by reading `dispatch.main` and the test's `_harness`:
```
test_free_lane_mints_at_the_zero_usd_cell_cap_on_a_drained_account
  _harness: monkeypatch.setattr(dispatch.subprocess, "run", lambda *a, **k: _Run())   _Run.stdout "ctx\n", stderr ""  (str, ALWAYS)
            dispatch.subprocess IS the global subprocess module -> every module's subprocess.run is the fake
  dispatch.main --detach, zero_usd lane passes every gate
   └─ _scaffold_node_for_agent            (dispatch.py)
       └─ node_writer.write_node -> spawn_gate.gate_for_root
           └─ links.frontmatter_rows(nd)   subprocess.run(["git","grep","--no-index","-aznE",…], capture_output=True)   BYTES mode, no text=
               └─ r.stderr.decode("utf-8","surrogateescape")   <- str has no .decode -> AttributeError
                  (gate_for_root catches rotation_record.GrepError only -> propagates out of main)
introduced: c0dc71c55 (goal:g4.18.6.2.2: the writer paths read ONE git-grep index instead of build_type_index's walk)
every subprocess.run in dispatch.py itself passes text=True -> not the site
siblings: the paid-lane and dead-runtime-key rows refuse BEFORE the scaffold -> green, unaffected
```
- Report: director-general-4, placed on this split by sanctuary-master 05:2xZ 09-30.

## CLAIM
(1) The `.decode` site is `links.frontmatter_rows`' `r.stderr.decode(...)` (first bytes-mode read after the grep), reached via `_scaffold_node_for_agent -> node_writer.write_node -> spawn_gate.gate_for_root`; the round's experiment records it by function and records the test RED on the pre-fix base.
(2) The production code is right (bytes mode is deliberate: SM 121/127 surrogateescape + `-a`); the FAKE is wrong. `_harness`'s run fake honours the real call's mode — `git grep` argv goes to the real `subprocess.run` captured before the patch (so the gate indexes the tmp graph exactly as the walk did before c0dc71c55), and every other call gets str/bytes by `text=`/`encoding=`/`universal_newlines=`.
(3) The zero-USD test is green on the fix with no assert removed or loosened; the paid-lane, dead-runtime-key and cell-floor rows stay green.

## Dispatch line
config-max: none — the cell under test, `provisioning.zero_usd_key_limit_usd`, is already read (test fixture CAP_USD != DEFAULT on purpose).
template-max: none.
code: none in production. Test-only: the `_harness` fake.

## FALSIFIERS
- `python3 -m pytest extensions/agi/tests/test_free_lane_dispatch_main.py -q -p no:cacheprovider --basetemp /tmp/pb3free` red on the fix, or GREEN on the pre-fix base (then the site named is wrong)
- the fix edits `links.py` / `spawn_gate.py` / `dispatch.py` (production bent to a fake)
- `git diff <base> <tip> -- extensions/agi/tests/test_free_lane_dispatch_main.py` removes an `assert` line or widens an assertion
- the zero_usd row no longer mints exactly once at the cell cap, or records `key_floor`/`account_floor`

## TESTS
- `test_free_lane_dispatch_main.py` (the one file): `_harness`'s run fake rewritten (<= 8 lines); the 4 rows unchanged.
- Neighbourhood: `python3 -m pytest extensions/agi/tests/test_free_lane_dispatch_main.py extensions/agi/tests/test_links.py extensions/agi/tests/test_spawn_gate.py -q -p no:cacheprovider --basetemp /tmp/pb3free` — run in the round's worktree or a tmp export, NEVER in MAIN while `verify-suite.lock` is held.
- Grep for the same fake shape elsewhere (`"run", lambda *a, **k:` with a str stdout in a test that reaches `write_node`): list any, fix none (record for a later leaf).

## FILE SCOPE
extensions/agi/tests/test_free_lane_dispatch_main.py

## CEILING
kids <= 1 · 0 production lines · <= 10 test lines · pi-free parent · 0 USD · CEILING measured by a TWO-operand numstat `<cut>..<tip before the paste commit>`, labelled so · if the pre-fix base is NOT red at the named site, stop and report — do not widen scope.
