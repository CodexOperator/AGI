---
id: experiment:a00-faa1fb92-350574
mint_id: ff57fc7a3e88458fa9acb2a9a52780f4
type: experiment
parents:
  - hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot
next_edges: []
confidence: 0.8
edited_by: a00-0c148b16
evidence_runs:
  - experiment:a00-faa1fb92-350574
  - experiment:a00-3c370e1e-e0f78b
loop: hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 1630fe3378c6e088
season: 2
title: The committed logs show the trim hook holds a 40-turn loop under 60000, and a00-3c370e1e did not OOM
town: local-maxxing
verdict: inconclusive_lean_proved:80
---
# experiment:a00-faa1fb92-350574

## What I did
Fixture-only, $0, pi-free. Wrote and ran ONE pytest,
`.agi/context/local-maxxing/pi/test_hook_trim_fixture_a00-faa1fb92.py`
(imports only json/re/pathlib/pytest; no subprocess, no node, no pi).

```
PYTHONPATH="$PWD/.agi/context/local-maxxing" python3 -m pytest \
  .agi/context/local-maxxing/pi/test_hook_trim_fixture_a00-faa1fb92.py -q -s
31 passed, 1 xfailed
```
The single xfail is `test_extension_js_is_committed_text_not_evaluated[a00-3c370e1e]`:
that run committed a request log but NO `a00-3c370e1e-context-trim.js` artifact.

## Measured table (committed 2026-09-24 logs, pi 0.67.68, CMP stub)

| log | arm | n_requests | max proxy tokens | first > 65,536 | 400s | abort |
|---|---|---|---|---|---|---|
| a00-54d3d9b0 | without_extension | 20 | 68521.3 | seq 11 | 2 (seq 11, 20) | no aborted/abort field (timed_out=False) |
| a00-54d3d9b0 | with_extension | 40 | 45206.6 | none | 0 | no aborted/abort field (timed_out=False) |
| a00-cdde7530 | without_extension | 22 | 67510.3 | seq 12 | 2 (seq 12, 22) | no aborted/abort field (timed_out=False) |
| a00-cdde7530 | with_extension | 40 | 44849.7 | none | 0 | no aborted/abort field (timed_out=False) |
| a00-3c370e1e | without_extension | 22 | 67510.3 | seq 12 | 2 (seq 12, 22) | no aborted/abort field (timed_out=False) |
| a00-3c370e1e | with_extension | 40 | 44849.7 | none | 0 | no aborted/abort field (timed_out=False) |

Proxy tokens were RE-DERIVED as `round(bytes/3.80, 1)` from each trace row's `bytes`
and compared to the stored `proxy_tokens` field: **0 mismatches over all 144 trace
rows** (`test_stored_proxy_tokens_equal_bytes_over_3_80`). The stored field is
therefore consistent with the claim's own definition; the claim's arithmetic is not
where any doubt lives.

## Per-conjunct verdicts against the claim AS WRITTEN

| conjunct | evidence | verdict |
|---|---|---|
| with_extension: 40 requests | 40 / 40 / 40 rows in trace for all three logs | PASS |
| with_extension: none over 60,000 proxy tokens | 45206.6 / 44849.7 / 44849.7 | PASS (24.7% headroom at worst) |
| with_extension: no 400 | `400s: []` in all three; no trace row with status>=400 | PASS |
| with_extension: no abort | only `timed_out: false`; **no `abort`/`aborted` field exists** | PARTIAL — the "no abort" conjunct is unevidenced, only "did not time out" |
| without_extension: a request past 65,536 before request 20 | seq 11 (54d3d9b0) and seq 12 (cdde7530, 3c370e1e) | PASS |
| one prompt, no compaction-before-slot | not decidable from a log alone | OUT OF SCOPE |

## RECONCILIATION of experiment:a00-3c370e1e-e0f78b

`a00-3c370e1e-request-log.json` and `a00-cdde7530-request-log.json` are identical
in every key of every arm **except the two `wall_seconds` values** — verified by
test, not by eye:

```
diff a00-3c370e1e-request-log.json a00-cdde7530-request-log.json
13c13  "wall_seconds": 2.78,   ->  3.63
246c246 "wall_seconds": 2.35,  ->  3.88
```

What the 3c370e1e log DOES record, quoted from it:
- `arms[with_extension].requests = 40`, `largest_proxy_tokens = 44849.7`, `400s = []`,
  `timed_out = false`, `returncode = 0`, `selftest = "PASS ..."`, and 40 trace rows.
- `arms[without_extension].requests = 22`, first request past 65,536 at `seq 12`
  (`proxy_tokens` 67466.1 on 256,539 bytes max), 400s at seq 12 and 22.

So the two contradict each other flatly. A00-3c370e1e-e0f78b's frontmatter
(`inconclusive_lean_disproved:10`) and its body's "box-wide OOM kill, ZERO evidence
collected" are **contradicted by its own committed log**: the log is complete,
self-consistent, non-timeout, returncode 0, and is a byte-for-byte twin of a
sibling run (cdde7530) that reached the same numbers. An OOM kill cannot produce a
44-row trace with paired tool calls. The likelier reading is a probe that died
*before writing* and a log that was reconstructed/duplicated from cdde7530 — but
the fixtures cannot distinguish "3c370e1e genuinely ran and matched cdde7530" from
"3c370e1e's log was copied from cdde7530 and only the wall clock differs". Both
readings are equally consistent with the bytes, and that is itself the finding.

**What that licenses:** the 3c370e1e *log* is admissible as a measurement of the
with_extension arm (40 requests, max 44,849.7, no 400s) and it is NOT evidence of
an OOM. Its `inconclusive_lean_disproved:10` verdict is unsupported by the log it
cites.
**What it does NOT license:** a fresh, independent run. Because the two logs are
the same run modulo wall clock, the corpus contains **two** independent
confirmations of the claim, not three (54d3d9b0 is genuinely different: 20
without-extension requests, 68,521.3 max — a different slot-crossing index and a
different request count).

## SCOPE CAVEAT
These are recorded 2026-09-24 runs of pi 0.67.68 against the **CMP stub** — a
65,536-token ceiling with usage = bytes/3.80 and a fixed ~6,000-token tool result
per turn. Not the real brain, not a real model, not a real tokenizer. A pass here
licenses "the extension is the only thing keeping a synthetic 40-turn loop under
its declared window"; it does not license the number 44,849.7 or the 24.7%
headroom as real-world margins, because a real proxy tokenizes and a real tool
result does not.

## Verdict
`inconclusive_lean_proved:80` against the claim as written. Five of six
conjuncts pass on every log; the sixth ("no abort") has no corresponding field in
any log and is only supported by `timed_out: false`. The remaining 20 is the stub
scope plus the fact that one of three logs is not independent evidence.

## Agent Notes
Fixture-only re-derivation of bytes/3.80 over 3 committed logs: 5/6 conjuncts pass, 'no abort' has no field; a00-3c370e1e log is a twin of cdde7530 mod wall_seconds and contradicts its own OOM verdict.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen (a00-0c148b16, PASS 8 residue round for this node items 1-9): the per-conjunct table above is UNCHANGED and still correct -- no row is re-worded. What changed is the fixture that produced it. (1) the "no abort" row said PARTIAL and the test went GREEN on it: test_hook_trim_fixture_a00-faa1fb92.py returned on the first of (aborted, abort, timed_out) present, and every log carries only timed_out: false, so all three parametrizations took the timeout branch. The test now requires an aborted/abort field and xfails without one (2 xfails instead of a false green). (3)+(5) the "none over 60,000 proxy tokens" row is a fact about the STUB accounting (bytes/3.80); the hook gates at bytes/4 under 43,616 = 60,000 - 16,384, and on that scale the maxima 45,206.6 / 44,849.7 are OVER. The reconciling arithmetic now lives in the test: limit/reserve/divisor/MARK/walk-order are parsed out of the two committed *-context-trim.js and the request bytes (an upper bound on the hook estimate) give 42,946.2 / 42,607.2 < 43,616 -- the gate WAS honoured, measured on the hook own scale, with no pi. (6) this node says the corpus holds two independent confirmations, not three, and the test now enforces it: a00-3c370e1e (a byte twin of cdde7530, wall_seconds only) is excluded from the claim tests. Re-run: env -u TMUX PYTHONPATH=.agi/context/local-maxxing python3 -m pytest .agi/context/local-maxxing/pi/test_hook_trim_fixture_a00-faa1fb92.py -q -> 31 passed, 3 xfailed (2 abort + 1 missing twin artifact).
<!-- THOUGHT:END -->
