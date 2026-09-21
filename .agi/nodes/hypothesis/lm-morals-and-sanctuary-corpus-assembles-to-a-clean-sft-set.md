---
id: hypothesis:lm-morals-and-sanctuary-corpus-assembles-to-a-clean-sft-set
mint_id: 9b7fbe36f7b74c22b1f14c2d09c89ff1
type: hypothesis
parents:
  - goal:g14.7
next_edges: []
edited_by: thought-master
scaffold_hash: c4529f2275509e4f
season: 2
testable_claim: "A corpus assembled on this box (0 USD, CPU) from (a) every moral:* node body plus the constitution head and the prayers, and (b) the public posts of the Sanctuary substack by Shaelaran (fetched once, source URLs and fetch dates recorded per document, the owner named the source), lands in datasets/sanctuary-sft/ as jsonl (one document per line: source, url, date, title, text, sha256, token count under the Qwen3.5 tokenizer) with a README, a scrub report (the kid-sft scrub: keys, IPs, emails) and a held-out 10 pct split by document, and totals >= 50 documents and >= 50k tokens; falsified if the fetch yields < 50 documents or < 50k tokens (then the corpus is too small for SFT and the next chunk is augmentation, e.g. instruction-form rewrites of the texts, measured the same way), or if the scrub finds any credential. Deliverable = the corpus + a 3-line stats table + the exact eval battery the fine-tune will be judged on (HumanEval 164 + IFEval 541 + the jev typed-acts replay), so FT.1 (the first LoRA on a Camber L4, 1 h, via the Prime) has its input and its bar before it is asked for. No training in this chunk."
title: "TRACK II chunk 1 (owner 21:4xZ: first fine-tune the bigger models on our morals and the sanctuary substack from user Shaelaran; Camber hours authorised; failing is fine): the training corpus exists, is measured and is clean BEFORE any GPU hour is spent"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-morals-and-sanctuary-corpus-assembles-to-a-clean-sft-set

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
