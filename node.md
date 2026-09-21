---
id: hypothesis:lm-local-0p6b-direct-logit-decider-reproduces-jev-verdict-class-ranking
mint_id: 29bb4d6dbb0045c4aa2b58b6c79aefcd
type: hypothesis
parents:
  - hypothesis:lm-jev-corrected-partition-derives-the-review-call
next_edges: []
ceiling: 0 USD compute; 1 USD OpenRouter cap for parent+kid; the rig on spare threads (llama.cpp toolchain lives there; a 0.6B GGUF fetch there satisfies the bytes rule) or ARM4C only with the EXISTING GGUF at nice 19 and 2 threads; no new model above 0.8B in this hop; no change to triage.py in this hop (a proved verdict mints the follow-on mvp hop).
edited_by: thought-master
falsifier: "on the 370 acts: verdict-class macro AUC below 0.60 for BOTH Q8_0 and Q4_K_M, OR agreement with the jev argmax below 0.60, OR wall time above 2 s per act at 4 threads on the rig CPU (or ARM4C at nice 19), OR the shuffled-label control does not sit near 0.5 (then the prompt leaks the label). A narrow miss (0.60-0.70) buys exactly one step up (Qwen3.5-0.8B or 2B Q4), never a third."
scaffold_hash: 85fcb9168f27e289
season: 2
testable_claim: "MEASURED so far on the jev line (TM.47/50/51/55, experiment:a00-cb66700f-9a90c8 and successors): jev ranks VERDICT CLASSES well (ARM 2 macro AUC 0.855) while its review-call axis is mis-thresholded; the corrected-partition mapping gives held-out AUC 0.7244 (all acts) / 0.7576 (verdict acts) and the 5-feature LR 0.7945 / 0.8923; a TF-IDF bag of words ties jev on q1 (0.661 vs 0.588); the triage mvp calls the paid jev API (0.002 USD per 20 acts). The cua-survey judge (01:16Z 09-19, M2) ranks a LOCAL typed-act decider top-2 by knowledge per token. CLAIM: a 0.6B local model (Qwen3-0.6B Q8_0 or Q4_K_M, GGUF already at ~/.cache/lm-models on ARM4C; llama.cpp, one prompt per typed act, softmax over the declared option letters = the openjev direct-logit pattern, no sampling) reproduces the jev verdict-class ranking on the SAME 370 labelled acts: macro AUC over verdict classes at least 0.70 and argmax agreement with jev at least 0.60, at 2 s per act or less on 4 CPU threads, 0 USD per act -- which would make the triage gate fully local (goal:g14: the smallest model that can do the job)."
tests: "(1) the option-letter softmax is read from logits (llama.cpp logit bias or the completion logprobs of the single next token), never parsed from sampled text; (2) 5-fold macro AUC + ECE per verdict class, same folds as TM.51; (3) shuffled-label control; (4) wall-ms per act, 4 threads, nice 19; (5) side by side: jev ARM 2 numbers from the cached jsonl (no new jev calls). Outputs one jsonl per model, one experiment node."
title: Lm local 0p6b direct logit decider reproduces jev verdict class ranking
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-local-0p6b-direct-logit-decider-reproduces-jev-verdict-class-ranking

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
