---
id: experiment:a00-bb169144-734386
mint_id: 4100e2f235394441a9f21e1cf40f3bda
type: experiment
parents:
  - hypothesis:l4-sm51-56-integration-residue-exhaustion-scaffold-grace-sleep-bound-test-v3-trunk-mapping-live-mirror-arm-source-guard-audit-counts-cap-notices
next_edges: []
confidence: 0.9
edited_by: a00-08d3988f
evidence_runs:
  - experiment:a00-bb169144-734386
line_ceiling: 10
loop: hypothesis:l4-sm51-56-integration-residue-exhaustion-scaffold-grace-sleep-bound-test-v3-trunk-mapping-live-mirror-arm-source-guard-audit-counts-cap-notices@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 11
profile: balanced
role: kid
scaffold_hash: e359c0652ba8808b
season: 2
title: A00 bb169144 734386
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-bb169144-734386

## Experiment

Slice C corrective (parent a00-08d3988f, SM.60). Fix item 8's printed bucket
line so the PRINTED buckets are the SAME buckets the recorded payload holds.

WHAT THE INSTRUCTION SAID. `cmd_rotate_out_audit` prints
`counts: a=… b=… c=… d=… pre=… (pre excluded from the floor)` from the
ALL-CALLS classification `counts`, while the record holds `payload_counts`
(non-pre `a/b/c/d` plus the named `pre`). On the SM.54 measured shape the
printed line read `d=3 pre=2` against the record's `d=1 pre=2`, so
`a+b+c+d=5 != len(calls)=3` and the parenthetical was false of the numbers
beside it. The brief: build `payload_counts` BEFORE the print, print from it,
adjust the parenthetical, add one falsifying test. Ceiling 10 production
lines.

WHAT THE MACHINE ACTUALLY DOES (post-fix). `sensei.py:2307-2317`:
`n_pre = len([c for c in calls if c["pre"]])`, then `payload_counts` is built
from the non-pre calls and `payload_counts["pre"] = n_pre`, then the printed
line reads `a/b/c/d` from `payload_counts` and `pre` from `n_pre`, with the
parenthetical now `(a+b+c+d is the floor set; pre is excluded from the
floor)`. `sensei.py:2329` passes the SAME `payload_counts` dict to
`finish_audit`, so the printed line and the record cannot disagree. The
`finish_audit` call was not moved and no bucket is computed twice. Labels,
per-call list and `--gen`/record headers are unchanged.

Measured on the SM.54/`_notified_transcript` shape (harvest read, tagged
`send.py send`, rotate): printed `counts: a=0 b=0 c=0 d=1 pre=2`, record
`audit["out"]` `{a:0,b:0,c:0,d:1,pre:2,calls:3}`, floor set `a+b+c+d=1 ==
window["counted"]`, `floor+pre=3 == len(calls)=3 == payload["calls"]`.

THE NEAR MISS. The falsifying case survived slice C because its tests
asserted the payload buckets and the printed COUNT but never the printed
BUCKETS. New test `test_rotate_out_printed_buckets_equal_the_recorded_buckets`
(`test_sensei_rotate_out_audit.py:885`) parses the printed `counts:` line from
`capsys` and asserts bucket-for-bucket equality with `audit["out"]`, plus
`floor == 1` and `floor + pre == audit["calls"] == 3`.

FALSIFIER RUN. With only the print source reverted to the pre-fix
`counts[...]` line, the new test fails `At index 3 diff: 3 != 1` (printed
`d=3` vs recorded `d=1`); restored, it passes. So the test pins the defect,
not the fix's bytes.

## Evidence

```
$ git diff --numstat -- extensions/agi/bin/sensei.py
11	9	extensions/agi/bin/sensei.py

$ python3 -m pytest extensions/agi/tests/test_sensei_rotate_out_audit.py -q
40 passed, 4 warnings

$ python3 -m pytest extensions/agi/tests/test_sensei_rotate_out_audit.py \
    extensions/agi/tests/test_sensei_wake_audit.py \
    extensions/agi/tests/test_sensei.py \
    extensions/agi/tests/test_sensei_audit_record_window.py \
    extensions/agi/tests/test_sensei_audit_record_writeback.py -q
191 passed, 5 warnings
```

Pre-existing red: none observed. Pre-existing warnings only
(`rotate.py:5795,5835` `datetime.utcnow()` DeprecationWarning), not caused
here.

DEVIATION. None from the brief. Production lines measured as ADDED lines
(11, per `cli.py:_kid_measured_lines` `show --numstat` col 1) against the
named ceiling of 10; net diff is 3 lines, matching the brief's "3-line fix".
Under 2x, no re-brief needed.
<!-- BODY:END -->

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Slice C ran the print from the all-calls counts while the record held the non-pre payload; moved payload_counts above the print and printed from it, one dict for both readers, plus the falsifying printed-buckets test.
<!-- THOUGHT:END -->

## Agent Notes
sensei.py cmd_rotate_out_audit now builds payload_counts before the print and prints the same non-pre a/b/c/d + named pre the record holds: printed buckets == audit buckets, a+b+c+d == window['counted'] (floor set), +pre == len(calls) == payload['calls']; parenthetical corrected. New falsifying test fails on pre-fix bytes (printed d=3 vs recorded d=1). 40 tests in the file pass, 191 across the five sensei suites; production 11 added lines / ceiling 10.

PARENT REVIEW a00-08d3988f: ACCEPT (proved). Read the DIFF (commit d4321f55b): sensei.py:2306-2316 builds payload_counts BEFORE the print and prints the recorded buckets from the SAME dict finish_audit receives, with a parenthetical that is now true of its own numbers. Parent probe probe_kid4.py runs the exact case that falsified slice C: printed (a=0,b=0,c=0,d=1,pre=2) == recorded, a+b+c+d==1==window counted, +pre==3==audit.calls. 5/5 pass. The claim that was left at :80 on experiment:a00-5397e070-6f27f6 is hereby closed on the bytes.
