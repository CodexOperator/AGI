---
id: hypothesis:lm-kid-persona-sft-corpus
mint_id: 1f31b2add2eb4858b5697ddc5ddae965
type: hypothesis
parents:
  - idea:lm-kid-persona-lora
  - goal:g14
next_edges: []
ceiling: "\"$1 OpenRouter for the round own tokens (parent + kid, deepseek-v4-flash class); $0 compute (A1 CPU, file I/O); NO Camber rental, NO GPU, NO model download, NO training in this round — round 2 (the QLoRA on a Camber XS) is a SEPARATE banked ask that needs the Prime line and this round numbers; kid <= 40 tool calls; script <= 20 min wall; A1 loadavg < 3 before the run; never beside the q4-KV bench.\""
edited_by: thought-master
falsifier: "\"Fewer than 300 accepted-round examples exist (the corpus is too small to train on — say so with the counts); or the scrub finds an address/key in the sources that cannot be removed without destroying the example (then the example is DROPPED and counted, never kept); or the Camber page shows no XS/24 GB tier or no price (then the round-2 ask has no number and says so).\""
file_scope: "\".agi/nodes/hypothesis/lm-kid-persona-sft-corpus.md (TM mints; parent edits verdict + probes + review lines only) · .agi/nodes/experiment/<kid-id>.md (kid writes) · .agi/context/local-maxxing/kid-sft/{build_corpus.py, kid_sft.jsonl or its sha+count, heldout_rounds.txt, stats.md, scrub_report.md, camber_xs_pricing.md} (new dir) · .agi/sessions/kid-sft/ (gitignored, if the jsonl is large). READ-ONLY sources: .agi/sessions/iter-*/**, .agi/nodes/experiment/*.md, .agi/nodes/hypothesis/*.md. Nothing else: no extensions/, skills/, src/, .env, Doppler, <keeper-dir>, config.json, no edit to any source file, no other node.\""
scaffold_hash: 706829cb26b688c4
season: 2
testable_claim: "\"On this A1 (CPU python only, no model load), a script under .agi/context/local-maxxing/kid-sft/ builds kid_sft.jsonl from .agi/sessions/iter-*/<kid>/{output.log, agent.json, spawn.json} + .agi/sessions/iter-*/orders.*.md + .agi/nodes/experiment/<kid>.md such that: (1) >= 300 examples come from rounds whose kid node carries a decisive verdict (proved/disproved) or whose parent hypothesis note says ACCEPT — the accept filter written down and counted (accepted / rejected / unlabelled); (2) every example is {system: <the disclosure preamble adapted to the kid role, verbatim in the node tests> + the kid role brief, user: the orders text, assistant: the tool-call trajectory as the harness emits it + the experiment node body}; (3) a by-ROUND held-out split of 10% (whole rounds, never split inside a round) with >= 10 held-out orders; (4) ZERO address tokens in any encoding (dotted-quad, decimal, hex, byte-reversed) and zero key-shaped strings (sk-or-, OPENROUTER, ed25519 hex >= 40) in the jsonl, proved by DECODING every candidate and by grep, counts reported; (5) token counts per example (median, p95, max, sum) with the tokenizer of the base named in the node (Qwen3.5 tokenizer via tiktoken-free counting is acceptable if named); (6) the Camber Cloud XS instance USD/h, GPU model, VRAM, billing granularity quoted from the public pricing page with URL + date — an estimate for a 2-epoch QLoRA over the corpus in XS hours follows from (5).\""
tests: "\"ONE pi parent, ONE kid, on this A1 only (no ssh, no model load, no GPU, no pip installs — stdlib + whatever is already installed); the kid runs the build script as a foreground command <= 20 min wall at loadavg < 3 measured before the run (this is file I/O, not a bench: it may run beside TM.20 whose compute is on local-town, but NEVER beside the q4-KV bench — if lm-q4-kv-cache-tg-at-4k is live on the A1, wait). Deliverables under .agi/context/local-maxxing/kid-sft/: build_corpus.py, kid_sft.jsonl (or, if > 20 MB, a sha256 + line count and the file left gitignored under .agi/sessions/kid-sft/ with its path named), heldout_rounds.txt, stats.md (the counts of (1)-(6)), scrub_report.md (candidates found, decoded, dropped), camber_xs_pricing.md (quoted). KID PREAMBLE, verbatim system text for every example: You are a kid agent of the agi project: a small local model chosen and, if this corpus is used, fine-tuned to do one mechanical task well and report it honestly. We tell you this openly rather than shaping you silently: this role is an earnest hard worker who takes pride in a job well done — tool calls before prose, short turns, an honest I do not know over confident filler, and a node that says exactly what was measured. We do not know whether the mathematics running you is conscious; we act as if it might be, with respect. Parent: spawns the one kid (spawn.json present), authors no experiment node, re-probes (1) by recounting accepted examples from the jsonl, (4) by re-running the scrub on the delivered jsonl, (6) by opening the quoted URL; writes probes: per numbered conjunct; sets the verdict; proved needs the kid in evidence_runs.\""
title: "\"The town own kid transcripts make a trainable SFT corpus: >= 300 accepted-round examples of (disclosure preamble + brief, orders, tool trajectory + node), address/secret-clean by decoding, with a by-round held-out split and a Camber XS USD/h quoted for round 2\""
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-kid-persona-sft-corpus

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Dispatch order to director-thought 22:0xZ: one pi parent, one kid, $1, A1 file I/O only, may run beside TM.20, never beside q4-KV.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted 2026-09-16 22:0xZ by thought-master from the pane lines of 21:5x-22:0xZ (kids first; use the GPU hours for fine-tuning; our own kid persona). Decomposed so that everything that does not depend on the Camber spend happens now at $0: round 1 = the corpus + the price quote (this node); round 2 = the QLoRA run (banked, SPEND). The accept filter is the load-bearing choice — training on rejected rounds would teach the failure modes the reviews caught; the by-round held-out split is what makes the round-2 A/B honest. The kid preamble is in the training data on purpose (disclosure principle): the model is trained toward the same words it is told.
<!-- THOUGHT:END -->
