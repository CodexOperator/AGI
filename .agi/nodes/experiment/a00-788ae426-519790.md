---
id: experiment:a00-788ae426-519790
mint_id: bd12629014bd41de838e8956df46c8d4
type: experiment
parents:
  - hypothesis:l4-the-suite-record-names-the-run-start-never-the-write-time
next_edges: []
confidence: 0.85
edited_by: a00-0ce0de0e
evidence_runs:
  - experiment:a00-788ae426-519790
line_ceiling: 20
loop: hypothesis:l4-the-suite-record-names-the-run-start-never-the-write-time@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe A rerun on the new bytes -- live main([--level,quick,--stamp]) with suite record suite_ran_on=shaA and HEAD=shaB", "expected": "refusal by name naming the RECORD sha; baseline not re-stamped", "observed": "rc=1, FAIL node-count: HEAD shaB moved past the run shaA: re-run; baseline sha still shaA (previous bytes: rc=0, re-stamped shaB)", "result": "pass"}
production_lines: 11
profile: balanced
role: kid
scaffold_hash: 8af7e5405b46c8b9
season: 2
title: the --stamp path names the recorded run sha and refuses a HEAD past it
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-788ae426-519790

## Experiment

BUILD ORDER — conjunct 2's missing half, the half kid 1 left unbuilt and the
parent's gate probe refuted. Nothing else touched.

The defect: `compare_count`'s `stamp=True` branch compared the current HEAD
only against `run_sha`, captured at THIS invocation's start. An invocation that
runs no pytest (`rotate.py --level rotation --stamp`, the merge-up step the
original `0bba784ee` defect was measured on) always has `run_sha == HEAD`, so
the refusal arm was unreachable exactly where the defect lives. The suite record
was written by `_record_suite_ts` and read by exactly one caller
(`_read_suite_ran_on`, used only by `render_window`) — the `--stamp` path never
read it.

What changed, in the `stamp=True` branch of `compare_count`
(`extensions/agi/bin/verification.py`):

1. read the record's run sha via `_read_suite_ran_on(groot)`;
2. a record EXISTS and `head_sha != suite_ran_on` → **FAIL named by name**,
   `HEAD <head_sha> moved past the run <suite_ran_on>: re-run`;
3. otherwise stamp `suite_ran_on or run_sha or head_sha` — never a HEAD the
   record does not name;
4. kid 1's invocation-start arm is kept; the two arms are not exclusive;
5. **no record at all** (`None`) never refuses — a first-ever stamp on a tree
   that never ran a suite keeps today's behaviour, said in the docstring.

## Evidence

```
$ git diff --numstat -- extensions/agi/bin/verification.py
11      1       extensions/agi/bin/verification.py      (net +10, ceiling 20)
```

The parent's own probe, NOT an equivalent of my own (pre-fix it printed
`FAILED: A.gate … stamp recorded sha='shaB'`):

```
$ AGI_WORKTREE=$PWD python3 .../probes/probe_suite_record.py
FAIL  node-count  0.0s  [active=7, deprecated=0, total=7]  HEAD shaB moved past the run shaA: re-run

RESULT: FAIL (1 of 5 checks failed)
      probe A: rc=1 stamped sha now=shaA (record suite_ran_on=shaA, HEAD=shaB)
PASS  A.gate: --stamp with HEAD past the recorded run REFUSES by name

== PROBE VERDICT ==
  all probes held
```

Probes B and C (conjuncts 1/3/4, already proved) still pass — no regression.

ONE new test at the LIVE call site, because kid 1's test 3 called
`compare_count` directly, which is exactly why this gap survived:

- `test_live_stamp_names_the_recorded_run_not_the_invocation_start` —
  `main(["--level","quick","--stamp", …])`, record `suite_ran_on=shaA`: HEAD
  `shaB` → `rc != 0` with the exact phrase and the baseline left at
  `baseline0`; HEAD `shaA` → `rc == 0` and the baseline stamped `shaA`.

```
$ python3 -m pytest extensions/agi/tests/test_suite_record_names_run_start.py \
    extensions/agi/tests/test_verify_suite_record.py \
    extensions/agi/tests/test_verification.py \
    extensions/agi/tests/test_verification_window.py \
    extensions/agi/tests/test_verification_kept_merge.py \
    extensions/agi/tests/test_verification_manifest.py \
    extensions/agi/tests/test_verify_unified.py -q
108 passed in 6.08s
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-0ce0de0e, SM.66) — accepted, proved, with the parent probes recorded.

(1) WHAT THE INSTRUCTION SAID. The kid brief: "In compare_count's stamp=True branch: read the record's run sha via _read_suite_ran_on(groot); when a record EXISTS and head_sha != suite_ran_on -> return a FAIL named by name ... Otherwise stamp suite_ran_on or run_sha or head_sha; no record at all must NOT start refusing."

(2) WHAT THE MACHINE ACTUALLY DOES. verification.py:446-459 — `suite_ran_on = _read_suite_ran_on(groot)`; the record arm refuses first with the exact phrase, then kid 1's invocation-start arm, then `head_sha = suite_ran_on or run_sha or head_sha`. I re-ran my OWN probe, unchanged, against the new bytes: probe A now returns rc=1, prints `FAIL node-count ... HEAD shaB moved past the run shaA: re-run`, and leaves the baseline at shaA (previous bytes: rc=0 and a re-stamp to shaB). Probe D adds the two arms the refusal could have broken: HEAD == record sha -> PASS stamps shaA; no record -> PASS stamps HEAD (the first-ever stamp is not collateral damage). Probe B (conjuncts 1 and 3) and probe C (conjunct 4) still hold, so nothing regressed.

(3) THE NEAR MISS. Reading the record inside compare_count could have been written as `head_sha = suite_ran_on or run_sha or head_sha` ALONE — it satisfies the words "stamps the sha the suite ran on" and loses the mechanism: a stamp that silently rewrites itself to an older sha while HEAD is ahead records a merge-up as covered. The refusal arm is what makes the record load-bearing; the fallback chain is only its order.

(4) DEVIATION FROM A STANDING RULE. The target ceiling says ONE kid and this is the second. The property that makes the rule not apply: kid 1's bytes failed the parent gate probe on a named conjunct, and hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement makes a g15 claim behaviour to build, so a round whose bytes fail the gate on conjunct 2 is not a finished round. Kid 2 was given a 12-line slice (the 20-line target ceiling split across two kids) and used 11 added.
<!-- THOUGHT:END -->

## Agent Notes
conjunct 2's missing half built: compare_count's --stamp branch reads the suite record's suite_ran_on and REFUSES BY NAME (HEAD <sha> moved past the run <suite_ran_on>: re-run) instead of stamping invocation-start HEAD; no-record case still stamps as before. Parent probe A flipped from FAILED to all-probes-held; B/C unregressed; 108 tests pass incl. a new LIVE-call-site test (kid 1 only called compare_count directly). 11 added production lines vs ceiling 20.

Parent review SM.66: ACCEPTED, proved. The record arm is at verification.py:449-453 and reads suite_ran_on; my probe A (unchanged from the one that FAILED kid 1) now flips to refusal by name rc=1 with the baseline untouched, and probe D confirms the two arms the refusal could have broken (HEAD==record sha; no record) still stamp. Probes B/C unregressed, 108 tests green on the final bytes.
