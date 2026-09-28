---
id: hypothesis:qwen2-key-only-beats-every-draw
mint_id: 3c1f0a52b7d94e0680aa41d5c2f7b913
type: hypothesis
parents:
  - hypothesis:qwen2-margin-vs-band-declared-test
next_edges: []
role: parent
loop: hypothesis:qwen2-margin-vs-band-declared-test@s2
model: stealth/space-bunny-alpha
profile: balanced
title: "Qwen2 key_only beats every random draw at 7 of 8 cells"
testable_claim: "Qwen2 np32: key_only sits strictly on the WINNING side of the random peer's full range in 7 of the 8 (budget, metric) cells - all four budgets on agree, and 3 of 4 on KL (5.25 KL is the exception, inside-noise) - and the one exception is the same cell where the MARGIN call also says inside-noise. If true, the two calls are not merely different denominators, they agree on WHICH cell is noise; the 5.25/7.25 disagreements of experiment:a00-ec09e83b-8786a9 are disagreements about a band, not about the peer, and key_only is a real allocation win at 4.25/6.25 on both metrics. Falsified if any cell has key_only strictly on the LOSING side of the peer range, or if 5.25 KL turns out outside the range once the half-range is signed correctly for KL."
push_further: "The 7-of-8 rests on three draws per cell, so 'strictly outside the range' is a 3-draw order statistic and one extra seed at 5.25 KL could move it either way. One more seed at 5.25 KL -- one cell, not the grid -- converts this from a reading into a bound. Do that before any new model."
town: local-maxxing
---
# hypothesis:qwen2-key-only-beats-every-draw

Split out of `experiment:a00-ec09e83b-8786a9` because it is a claim in its own right and not
this round's claim: the margin-vs-range question was about which DENOMINATOR the decide layer
applies. This one is about the sign of the result, and it was nearly lost inside it.

## Measured (reader output, `calls.json` -> `summary.key_only_beats_every_draw`)

| cell | peer range | key_only | side | winning side? |
|---|---|---|---|---|
| 4.25 agree | [.4587, .4998] | .528564 | above | yes |
| 4.25 kl | [1.6857, 2.0440] | 1.570819 | below | yes |
| 5.25 agree | [.6438, .7288] | .732422 | above | yes |
| 5.25 kl | [.5652, 1.0640] | .612523 | inside | **no — the exception** |
| 6.25 agree | [.7375, .7959] | .830566 | above | yes |
| 6.25 kl | [.3313, .6293] | .248020 | below | yes |
| 7.25 agree | [.8159, .8540] | .883301 | above | yes |
| 7.25 kl | [.1730, .2941] | .113942 | below | yes |

Winning side: `BEATS = {agree: above-peer, kl: below-peer}` in the script, declared once.

## Why it matters to the chain
The two calls disagree at 5.25|agree, 7.25|agree and 7.25|kl, and every one of those
disagreements is "margin says inside-noise, peer says key_only wins outright" -- the band is
wide relative to a small margin, the peer is not. The single cell where BOTH say inside-noise is
5.25|kl. So the two denominators pick out the same one noisy cell, and the honest summary is not
"key_only is inside noise at half the budgets": it is **one noisy cell, 7 real wins**.

## Caveat carried
Three draws. "Strictly outside the range of 3 samples" is an order statistic with no error bar,
and 5.25|kl (key_only .6125 against a peer range [.5652, 1.0640], i.e. a hair inside the bottom
draw) is exactly the cell a fourth seed could move. Read this as a claim to be bounded, not a
result to be banked.
