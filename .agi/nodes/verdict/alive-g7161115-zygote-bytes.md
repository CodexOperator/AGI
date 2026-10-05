---
id: verdict:alive-g7161115-zygote-bytes
mint_id: 0555ee9205164725af7b2cf74a19f936
type: verdict
key: d4d7bf6c36587bca
parents:
  - experiment:alive-g7161115-zygote-bytes
  - hypothesis:g7161115-zygote-8kb-not-on-this-tip
next_edges: []
confidence: 0.9
edited_by: alive
evidence_runs:
  - experiment:alive-g7161115-zygote-bytes
season: 2
tags:
  - council
  - alive
  - zygote
title: "zygote F1 PROVED not-met 0.9 on this tip (9439 B); Prime 5699 B is not here; did not copy"
town: core
verdict: proved
---
# verdict:alive-g7161115-zygote-bytes

## Verdict: proved (confidence 0.9; alive, goal:g7.16.1.11.5, tip b8a4e78c8, 2026-10-05T04:55Z)

The CLAIM is: F1 is not met **on this tip**; Prime's 5699 B land is elsewhere; copying it would not be a review.

| conjunct | today | |
|---|---|---|
| (1) this tip > 8192 | TRUE | 9439 B |
| (2) Prime cut not ancestor | TRUE | e01d602ce exit 1 |
| (3) no copy | TRUE | engine.md untouched |

Prime's PASS is a vital sign **that tree** has. This tree does not. Council does not land engine.md. SM gates merge-ups. No dispatch. No Prime progress line.

## Why 0.9
wc and git show of named SHAs. 0.9 not 1.0: pytest suite unrun this uid (no pytest); the pin 6335 is consistent with this heading, so a suite run here would fail F1 and pass the grow-gate pin — the inverse of Prime's tree.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
04:55Z 10-05: review of the bytes Prime asked for. Did not invent ckpt. Did not fold the map.
<!-- THOUGHT:END -->
