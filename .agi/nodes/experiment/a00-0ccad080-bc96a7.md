---
id: experiment:a00-0ccad080-bc96a7
mint_id: 81ddb3db48b44212aa0818c56e4c5f6a
type: experiment
parents:
  - hypothesis:a-declared-suite-fail-names-its-failing-tests-and-the-context-flake-is-named
next_edges: []
confidence: 0.85
edited_by: a00-9093e188
evidence_runs:
  - experiment:a00-0ccad080-bc96a7
loop: hypothesis:a-declared-suite-fail-names-its-failing-tests-and-the-context-flake-is-named@s2
model: stealth/space-bunny-alpha
probes:
  - "'wire (HELD) parent a00-9093e188 DH.393: I drove the trigger MYSELF"
  - "not the kid's driver. A thread minted throwaway nodes into the LIVE .agi/nodes/experiment every 0.4s for the whole duration of ONE run of pytest .agi/context/local-maxxing/sql -q -rsEf: suite exit 0"
  - 13 passed
  - 6 subtests
  - zero FAILED/ERROR lines
  - leftovers [] and a post-sweep glob of zz-parent-probe-*.md empty. The landed frozen-file-set bytes are reached live and hold under the exact write pressure that produced DH.387's red.'
  - "'gate (HELD"
  - "the state the gate must refuse): the naming claim is corroborated in the RESTORED test file"
  - not only in the kid's log - .agi/context/local-maxxing/sql/test_graph2sql.py:65 carries the message 'node count differs from the file set' and :71 asserts verify(...)==0
  - exactly the two AssertionError strings the kid quoted. cls.files = g.iter_files(NODES) at :50 is the frozen set
  - and every call site threads files=; the kid's temporary revert was restored.'
  - "'auth (HELD): the driver wrote only inside its own prefix (zz-parent-probe-*) and swept every file in a finally; I checked the same way and the live node tree carried no strays"
  - so no count was inflated and no foreign node was touched.'
  - "'verdict: ACCEPTED at a lean of 85. Conjunct (b) is discharged in the only honest form available: the failing tests are NAMED (test_graph2sql.py::MirrorTest::test_build_under_60s_and_covers_every_node_file and ::test_verify_roundtrip_exits_0"
  - AssertionError 4553 != 4534)
  - the cause is measured
  - and the same trigger is green on the landed bytes - which I re-measured. The 15 left is scope
  - "not doubt: the FAILED lines came from a deliberately reverted seam (the kid labels this itself)"
  - so no run of the SHIPPED bytes has ever been red
  - and DH.387's narrower single-failure window was not re-observed.'
production_lines: 0
profile: balanced
role: kid
scaffold_hash: dbb406eaa118c195
season: 2
title: "the DH.387 context flake is NAMED: test_graph2sql.py::MirrorTest::test_build_under_60s_and_covers_every_node_file (+test_verify_roundtrip_exits_0), reproduced live and green after the frozen-file-set fix"
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-0ccad080-bc96a7

## Experiment — discharge conjunct (b): NAME the flaky test, live

Conjunct (b) had never been discharged: the cause was measured and fixed
(experiment:a00-6f88eaa5), but no run had ever printed a failing `.agi/context` test id.
So I drove the KNOWN trigger — a WRITE, not luck — against the real suite and read the name off the red.

| run | bytes under test | trigger | result |
|---|---|---|---|
| `fixed` | the landed frozen-file-set seam | 104 throwaway node files minted into the LIVE `.agi/nodes/experiment` during the run | `exit=0` — 134 passed, 19 skipped, 4 xfailed, 6 subtests passed |
| `unfixed` | `test_graph2sql.py` temporarily reverted to the pre-DH.393 re-glob discipline, SAME driver | 119 node files minted mid-run | `exit=1` — **2 failed**, 132 passed, 19 skipped, 4 xfailed |
| `fixed2` | the landed bytes again (post-restore) | 107 node files minted | `exit=0` — 134 passed, 19 skipped, 4 xfailed |

## THE NAME (the conjunct's deliverable)

```
FAILED .agi/context/local-maxxing/sql/test_graph2sql.py::MirrorTest::test_build_under_60s_and_covers_every_node_file
FAILED .agi/context/local-maxxing/sql/test_graph2sql.py::MirrorTest::test_verify_roundtrip_exits_0
```

with the cause visible in the assertion, not inferred:

```
E  AssertionError: 4553 != 4534 : node count differs from the file set
E  AssertionError: 1 != 0        (verify -> DRIFT)
```

4553 = the re-glob AFTER the build, 4534 = what the db was built from: the throwaway nodes the
writer minted while the mirror was building. The first-named test is the one DH.387's single
failure was; the pair goes red together whenever the write lands between build and count, and
DH.387 saw `1 failed` because the write landed in the narrower window that only trips `verify`.
Both are the same defect (a re-glob after the build), and both are named.

**Label, as instructed.** The `unfixed` run is a deliberately reverted seam, so its FAILED lines
are evidence about the CAUSE. The `fixed`/`fixed2` runs are the real suite under the real trigger
and are the evidence about the FLAKE: the same trigger that produced 2 named failures produces a
green run on the landed bytes. The flake is fixed at its measured cause, and it is now NAMED.

## How

- `.agi/sessions/iter-DH.393/a00-0ccad080/drive_flake.py` — the driver. Confirmed first that
  `test_graph2sql.py` resolves `NODES = ROOT/".agi"/"nodes"` (the LIVE graph dir, not a fixture),
  then mints one throwaway graph node every 0.4 s for the whole duration of ONE
  `python3 -m pytest .agi/context -q -rsEf` run, and sweeps every one of them in a `finally`
  (plus a pre-run sweep, so a killed run cannot leave one).
  Ledger printed on every run: `leftovers=[]`, and a filesystem check confirms 0 strays.
- `.agi/sessions/iter-DH.393/a00-0ccad080/run_unfixed.py` — the one-shot revert: backs the file up,
  applies the re-glob discipline, runs the SAME driver, restores in a `finally` and reports
  `restored=True identical_to_backup=True`. Post-restore `.agi/context/local-maxxing/sql` is
  `13 passed, 6 subtests passed`.
- Three suite runs total, one at a time. No retry, no `--retries`, no plugin, no timeout change.
- No production bytes left changed: `git diff --numstat` shows only the four sibling experiment
  node files from earlier kids — 0 production lines from me.

## Falsifiers

1. No `FAILED <nodeid>` printed -> NOT the case; two printed, quoted above.
2. Fixed by rerun/retries/timeout -> NOT the case; the fix is the frozen file set (a00-6f88eaa5)
   and it was already landed before I ran anything. I only named the defect.
3. The named test is not the graph2sql one -> NOT the case; it is the graph2sql pair, and the
   driver did not move the suite's counts (134/19/4 on both fixed runs).
4. `>= 134 passed, 19 skipped, 4 xfailed` -> held on both fixed runs; the unfixed run is 132+2.

## Evidence

- `suite_fixed.log`, `suite_unfixed.log`, `suite_fixed2.log` (full pytest output, in my session dir)
- `drive_flake.py`, `run_unfixed.py` (the two scripts)

## Agent Notes
Flake NAMED under the live write trigger: test_graph2sql.py::MirrorTest::test_build_under_60s_and_covers_every_node_file (+test_verify_roundtrip_exits_0), AssertionError 4553 != 4534; same trigger green 134/19/4 on the landed frozen-file-set seam, twice, no retries.
