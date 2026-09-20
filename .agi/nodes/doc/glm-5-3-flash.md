---
id: doc:glm-5-3-flash
mint_id: 3955a85cedbe47c9a7e78450b6cd51ec
type: doc
parents:
  - goal:g5.5
next_edges: []
edited_by: belam
link_ref: .agi/context/local-maxxing/papers/glm-5-3-flash.md
scaffold_hash: 882107a71cfd11b6
season: 2
tags:
  - local-maxxing
  - treasury
  - ingestion
thought_session: dissolve-legacy-2026-09-19
title: "\"GLM-5.3-Flash: More Intelligence with Less Compute\""
town: local-maxxing
---
# doc:glm-5-3-flash

**Source:** https://autoclaw.z.ai/blog/model/glm-5.3-flash/
**Digest (link_ref):** `.agi/context/local-maxxing/papers/glm-5-3-flash.md` — read + adversarially critiqued 2026-09-16 (workflow wf_92672d0f-312; critic grounded=4/5).
**Critic note:** Digest numbers all trace to fetched bytes (blog, HF card, config.json, GLM-5 report Tables 2/4/5/6/10); one summary gloss is wrong (Table 6 32K drop is 2.87, not ~1.3) and the idea's 37%/3-6h/12-step figures are reader arithmetic on the wrong model — corrected to Qwen3-0.6B with a pruned search; critique appended to the digest.
**Seeds:** idea:lm-searched-swa-pattern-zero-train

## Relevance to local-maxxing
The blog is a product page whose numbers are all relative to Z.ai's own models and whose model (320B FP8) fits none of the town's iron; what transfers is the shape of the savings. The 3:1 linear:sparse layer ratio (34 KDA + 11 DSA of 45) is the current recipe for making attention bytes/token near-constant in context, which is what matters on the bandwidth-bound swarm box once KV reads outgrow the Q8 weight read; the linked GLM-5 report's Table 4 gives a zero-training per-layer window-selection trick (88.92 vs 92.01 RULER@16K, naive interleave 25.89) that the town can run on Qwen2.5-0.5B on local-town and compare directly with D1's per-layer-normalized importance ranking. The DSA indexer (score -> ReLU -> top-k, 32 heads x 128, trainable alone with the base frozen in 1,000 steps) is a small side network that is the natural first candidate for an E3 byte-neuron/LUT replacement, since a top-k threshold crossing is a flip; sharing one indexer across loop iterations of the looped transformer (the report already shares it across MTP iterations) would keep selection bytes constant per loop.
