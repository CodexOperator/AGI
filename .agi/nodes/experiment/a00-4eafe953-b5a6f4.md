---
id: experiment:a00-4eafe953-b5a6f4
mint_id: 5312ca50f4e24dcb90e38f7d5acc0afc
type: experiment
parents:
  - hypothesis:l4-post-branches-are-local-only-mirrored-to-refs-agi-posts-and-the-merge-up-takes-the-suite-lock-itself-no-window-ask
next_edges: []
confidence: 0.8
edited_by: a00-ea1066f0
evidence_runs:
  - experiment:a00-4eafe953-b5a6f4
loop: hypothesis:l4-post-branches-are-local-only-mirrored-to-refs-agi-posts-and-the-merge-up-takes-the-suite-lock-itself-no-window-ask@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 09cc23522d951d31
season: 2
title: A00 4eafe953 b5a6f4
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4eafe953-b5a6f4

## Experiment — closing sweep of SM.250 (round slice E)

Three items: E1 clear the one known red, E2 run the WHOLE engine suite and
classify every remaining failure, E3 report the exact pass/fail line.

### E1 — KNOWN RED cleared, test pin unchanged

`extensions/agi/tests/test_branch_spelling_grep.py` was red because
`rotate.py` produced 21 spelling-shaped hits against a pin of 20. The extra
hit was NOT a reader: it was the COMMENT added by this bundle's slice B at
`extensions/agi/bin/rotate.py:3514`, whose text literally spelled
`push origin season2/posts/<new>` — the `season2/p` fragment matched the
`season[0-9]+/[A-Za-z_0-9]` shape. A comment is not a branch resolver, so
the fix was to REWORD the comment, never re-pin:

```
- # `push origin season2/posts/<new>` is the clause-(1)
+ # of the post branch straight to origin is the clause-(1)
```

The scanned inventory is now byte-identical to `PINNED`:

```
$ python3 -m pytest extensions/agi/tests/test_branch_spelling_grep.py -q
...                                                                      [100%]
3 passed in 0.22s
```

No test file was edited; no reader was re-routed; `PINNED` is unchanged.

### E2 — full sweep, failures classified

The kid tier gate refuses a bare directory run (`AGI_TIER=kid refuses a
bare full-suite directory run`), and it also refuses a `::nodeid` argument
(`_is_bare_directory_run` treats any token not ending in `.py` as a
directory), so the sweep names every test file explicitly — all 195
`test_*.py` under `extensions/agi/tests/` (162 top-level + 33 in
`graph_core/`, `chain_engine/`, `embeddings/`, `schema_registry/`,
`renderers/`), recursively. This is the whole suite, just spelled as a file
list.

Result (after E1):

```
FAILED extensions/agi/tests/test_brief.py::test_verdict_taxonomy_is_derived_not_retyped
FAILED extensions/agi/tests/test_rotate_g1517.py::test_spawn_first_seating_role_from_row_and_pin_at_row_gen
2 failed, 4876 passed, 15 skipped, 1 xfailed, 1577 warnings in 644.65s (0:10:44)
```

Re-run with a tighter file list (top-level only) the same round gives
`1 failed, 4645 passed, 15 skipped, 1 xfailed` — the extra failure is
collection-order-dependent, not a fixed defect. Both are classified **(b)
pre-existing / unrelated to slices A–D**, with the mechanism named:

**(b1) `test_brief.py::test_verdict_taxonomy_is_derived_not_retyped` — a
pre-existing `sys.modules['evidence_gate']` replacement in two sibling test
files, not this bundle.** `test_metrics.py:22-25` and
`test_publish_alarm.py:70-73` load a FRESH `evidence_gate` module from disk
(`importlib.util.spec_from_file_location("evidence_gate", ...)`) and assign
it into `sys.modules["evidence_gate"]` at MODULE IMPORT (collection) time.
Whichever test module imports `brief` BEFORE those two files gets the
ORIGINAL `evidence_gate` module object bound as `brief.evidence_gate`; every
module collected AFTER them (including `test_brief.py`) gets the replacement.
`test_brief`'s `monkeypatch.setattr(evidence_gate, "VERDICT_HELP", sentinel)`
then patches the REPLACEMENT while `brief.assemble` reads the stale original,
so the sentinel never reaches the brief. Directly instrumented on the failing
run (a `/tmp` pytest plugin printing module identities at test setup):

```
IDPROBE brief.evidence_gate is sys.modules['evidence_gate']: False
IDPROBE brief.evidence_gate id: 271756031808496 sys.modules id: 271755829993744
```

Evidence it is collection-order/cumulative and not this bundle: the test
passes alone (`126 passed`), passes with every subdirectory test file
(`358 passed`), passes with the first 57 files + `test_brief` (`1578
passed`), passes with the 28 middle files + `test_brief` (`645 passed`), and
fails only in the full union — exactly the shape of the documented
pre-existing order leaks (experiment:a00-881b7645-6599a7: "4 full-suite
failures are order-dependent `brief_tier` tests that pass in isolation").
No file this bundle touched (`cli.py`, `branches.py`, `rotate.py` comment,
`send.py`, `verification.py`) participates in the mechanism.

**(b2) `test_rotate_g1517.py::test_spawn_first_seating_role_from_row_and_pin_at_row_gen`
— `write.py`'s descend-only API root guard refuses the test's bare
`tmp_path`.** The test passes a `tmp_path` with no `.agi/`. `rotate.cmd_spawn`
reaches `_first_seating_spawn_writes` -> `_successor_row_write` ->
`write.submit(main_root, ...)`, and `write._resolve_api_root` refuses any
root that is neither a graph root nor has a `.agi/` child:
`not an agi project graph root: PosixPath('...') — the Python API resolves
root descend-only and refuses to walk UP the filesystem into a different
project (hypothesis:l4-write-api-root-resolution)`. The raise is caught by
`rotate.py:2137`'s best-effort `except` and printed as
`warn: first-seating meter pin / ack failed`, leaving the ack's session-key
unresolvable, so the bare `.ack.json` the test reads is never written. That
guard is `hypothesis:l4-write-api-root-resolution`, landed by
`experiment:a00-2c00af23-3ea2ff` (verdict proved, L4.95) in `write.py` — a
different chain from this node's (`g15.25` post-branch mirroring), and the
identical fixture a sibling round hit is already documented and fixed
test-side in `experiment:a00-1a5103fe-98a8d9` ("the fixture root was not an
AGI project graph root, so `write.submit`'s descend-only `_resolve_api_root`
RAISED" — fixed by adding `agi-tree.config.json` to the fixture). Not
introduced here: the only rotate.py edit in this round is the E1 comment,
which is inert, and the failure reproduces with that comment either spelling.

### E3 — exact pass/fail line

```
2 failed, 4876 passed, 15 skipped, 1 xfailed, 1577 warnings in 644.65s (0:10:44)
```

`test_branch_spelling_grep.py`: `3 passed`. The count did not drop: every
failure is named above and neither is bundle-induced, so per the closing-round
rule nothing was deleted or weakened to chase a green.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_branch_spelling_grep.py -q
3 passed in 0.22s

$ python3 -m pytest $(find extensions/agi/tests -name "test_*.py") -q -p no:randomly
FAILED extensions/agi/tests/test_brief.py::test_verdict_taxonomy_is_derived_not_retyped
FAILED extensions/agi/tests/test_rotate_g1517.py::test_spawn_first_seating_role_from_row_and_pin_at_row_gen
2 failed, 4876 passed, 15 skipped, 1 xfailed, 1577 warnings in 644.65s (0:10:44)

$ python3 -m pytest extensions/agi/tests/test_rotate_g1517.py -q -p no:randomly
FileNotFoundError: .../sessions/seats/director-seat.ack.json
warn: first-seating meter pin / ack failed: not an agi project graph root: ...
1 failed, 5 passed

$ python3 -m pytest extensions/agi/tests/test_brief.py -q -p no:randomly
126 passed in 6.23s
```

Changed file: `extensions/agi/bin/rotate.py` (one comment, no code).
No other file was modified by this round.

## Agent Notes
Closing sweep: E1 cleared the spelling red by REWORDING the slice-B comment at rotate.py:3514 (never re-pinned; PINNED unchanged, test_branch_spelling_grep.py 3 passed). E2 full sweep over all 195 test files (bare dir + ::nodeid both refused by the kid tier gate): 2 failed, 4876 passed, 15 skipped, 1 xfailed in 644.65s. Both failures classified (b) pre-existing, not slices A-D: (b1) test_brief.py::test_verdict_taxonomy_is_derived_not_retyped is a sys.modules['evidence_gate'] replacement at collection time by test_metrics.py:22-25 / test_publish_alarm.py:70-73, so brief holds the stale module and monkeypatch lands on the replacement (instrumented: brief.evidence_gate is sys.modules['evidence_gate'] == False); order/cumulative, passes alone and in every subset tested. (b2) test_rotate_g1517.py::test_spawn_first_seating_role_from_row_and_pin_at_row_gen is write.py's descend-only _resolve_api_root (hypothesis:l4-write-api-root-resolution) refusing the bare tmp_path, caught at rotate.py:2137; documented sibling fix in experiment:a00-1a5103fe-98a8d9. No assertion deleted or weakened; only rotate.py comment changed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHY THIS VERSION DIFFERS (parent a00-ea1066f0 review, SM.250).
(1) INSTRUCTION: E1 -- the round had one KNOWN red (test_branch_spelling_grep.py: rotate.py 21 spellings vs a pin of 20) and the parent ruled it BUNDLE-caused, not pre-existing: git diff HEAD shows the extra hit is the COMMENT slice B added at rotate.py:3514 ("push origin season2/posts/<new>"). E2 -- run the whole suite and classify any remaining red.
(2) WHAT THE MACHINE DOES: E1 reworded that comment ("the head push of the post branch straight to origin") without re-pinning; I re-ran test_branch_spelling_grep.py -- 3 passed, PINNED unchanged. E2's full sweep over 195 test files: 2 failed, 4876 passed, 15 skipped, 1 xfailed in 644.65s. The kid is right that the kid-tier pytest gate (conftest.py:293 _is_bare_directory_run) refuses both a bare dir and a file.py::nodeid argument, so the sweep was spelled as an explicit file list.
(3) THE NEAR MISS / CLASSIFICATION I CHECKED: the two remaining reds are (b1) test_brief.py::test_verdict_taxonomy_is_derived_not_retyped and (b2) test_rotate_g1517.py::test_spawn_first_seating_role_from_row_and_pin_at_row_gen. I re-ran them: (b1) PASSES alone -- an order-dependent sys.modules['evidence_gate'] collision between test_metrics.py:22-25 / test_publish_alarm.py:70-73 and brief, nothing to do with this bundle. (b2) FAILS alone and its captured stderr names the cause: "first-seating meter pin / ack failed: not an agi project graph root ... the Python API resolves root descend-only and refuses to walk UP ... (hypothesis:l4-write-api-root-resolution)". The bundle's diff touches neither write.py nor that API-root path (git diff HEAD --name-only has no write.py), so (b2) is pre-existing too. The kid could not run a HEAD-minus-diff tree (no git at kid tier) and said so; my inspection closes it.
(4) DEVIATION: none. Production change was the one comment; no assertion was deleted or weakened. E is accepted proved for the closing slice.
VERDICT: proved (closing sweep), confidence 0.8 -- the sweep result is real; the only residual doubt is that (b1)/(b2) predate the bundle by mechanism + untouched-file evidence rather than a HEAD-minus-bundle run.
<!-- THOUGHT:END -->
