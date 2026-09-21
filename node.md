---
id: verdict:graph-first-engine-publish
mint_id: 8b0e5d21c7a34f6ea9d3b8c1470f2e56
type: verdict
parents:
  - exp:graph-first-engine-publish
confidence: 0.85
edited_by: season.py
evidence_runs:
  - exp:graph-first-engine-publish
season: 1
status: open
subgraph: false
tags:
  - g6.1
  - g6.3
  - grid
  - stitch
thought_session: season
title: The write direction is reversed and measured; the read direction is not, and G6.1 stays active for exactly that reason
verdict: proved
---
**VERDICT: proved, for `goal:g6.3` in full and for the *write* half of
`goal:g6.1`.**

The core claim `hyp:payload-in-node` made — that changing `payload_ref`'s
resolution rule from "a path in the engine tree" to "the payload in
`refs/grid/node/<mint-id>`" makes G6.3's falsifier passable — holds on real
content, at the byte level: 180/180 files identical, 180/180 modes matching the
engine's own git index, 16 executables preserved that the pre-S9 code would
have silently downgraded. G6.3's second clause, materialising *a chosen
version* rather than whichever is current, is `--grid-version` and is tested.

**The mechanism the hypothesis prescribed was the one that worked, and the
caveat `verdict:payload-in-node` attached to it was correct.** That verdict
said the design was proved and reusing `commit_file()` as it shipped was
unendorsed. Both halves were right: the design deployed unchanged, and the
naive reuse would have failed exactly the two cases it named. S9's estimate of
"~15–20 lines" was close for the write side and understated the read side —
`materialize_entry` had no counterpart at all and had to be written.

**What is proved beyond the mechanism: two real engine changes, and then a
third, reached `agi` with no file in that repo opened by hand.** That is
`goal:g6.1`'s arrow doing work rather than being described, and the third one
was a prose surface, which is the class `goal:g6.8` singles out as the place a
node-less change does the most damage.

**Explicitly unendorsed, and this is the part that keeps G6.1 `active`:** the
claim that the graph is now the source of truth *in both directions*. It is
not. Contract derivation still reads the engine tree, so the graph writes the
engine but learns about it by reading the engine — a payload edited only in the
graph carries a stale contract until it is published and rescanned. Anyone
reading "the arrow reversed" as "the engine is now fully derived" would be
overclaiming what this measured.

**Also unendorsed:** automating the publish. `goal:g6.5` step 2 is unblocked,
not done, and a cron that writes the engine while derivation still runs the
other way is the data-loss shape this project has paid for three times
(H0, H0b, H0i). The gate on `--publish` — explicit flag, `--from-grid`, and a
clean target working tree — is what makes a *manual* publish recoverable; it is
not an argument that an unattended one is safe yet.

**Confidence 0.85, not higher:** the byte and mode evidence is total on this
corpus, but the corpus has no symlinks, so `120000` is proved by construction
and by tests rather than by production data — the one disproof condition
`hyp:payload-in-node` named that this run could not close with live content.