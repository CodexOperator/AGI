---
id: hypothesis:lm-oscillator-research-hunt
mint_id: 63baed87f7c843ad99fcf04edd395f28
type: hypothesis
parents:
  - idea:lm-hybrid-oscillator-readout
  - goal:g14
next_edges: []
ceiling: "\"$2 OpenRouter for the round own tokens (parent + 3 kids, deepseek-v4-flash class); $0 compute; NO Camber, NO GPU, NO ssh; downloads <= 2 GB on this A1 (bitnet.cpp binary + 2B-4T weights only), removable after the measurement; A1 loadavg < 3 before each kid spawn; never beside the q4-KV bench.\""
confidence: 0.65
edited_by: a00-ec4d1114
evidence_runs:
  - experiment:a00-7fcf31f1-43592b
  - experiment:a00-288aec4d-1f6c77
  - experiment:a00-989a0516-9cd7e6
falsifier: "\"A digest with fewer than 8 sourced papers, or any number without a source tag, or a Mercury/ternary-dLLM answer without a citation, or a synthesis that proposes a Camber use without minutes — each is a demote of that kid; a synthesis with no $0 numpy experiment for the metronome is a demote of the round.\""
file_scope: "\".agi/nodes/hypothesis/lm-oscillator-research-hunt.md (TM mints; parent edits verdict + probes + review lines only) · .agi/nodes/experiment/<kid-id>.md x3 (kids write) · .agi/context/local-maxxing/troves/2026-09-16-oscillatory/{oscillatory.md, diffusion-llm.md, one-bit.md, synthesis.md, bitnet_a1_bench.md if measured} (hunt_args.json is READ-ONLY input). Nothing else: no extensions/, skills/, src/, .env, Doppler, <keeper-dir>, config.json, no edit to hunt_args.json, no other node.\""
scaffold_hash: 20f74dfdc9dc0181
season: 2
testable_claim: "\"Three kids, each with the verbatim reader brief from .agi/context/local-maxxing/troves/2026-09-16-oscillatory/hunt_args.json (sources[].prompt: oscillatory, diffusion-llm, one-bit; fetch by curl, no paid API), deliver .agi/context/local-maxxing/troves/2026-09-16-oscillatory/<key>.md digests such that (1) every claim carries URL + date and is tagged MEASURED or ESTIMATE, (2) each of >= 8 papers per digest has the mechanism, the headline number, code + licence, CPU-toy feasibility and the ONE sketch element it maps to, (3) the oscillatory digest names the 3 closest mechanisms to the metronome idea and the smallest numpy experiment, (4) the diffusion digest answers whether Mercury has open weights (yes/no, cited) and names the ONE open dLLM runnable on local-town 8 GB or Camber XS 24 GB, (5) the one-bit digest answers whether a ternary dLLM exists (cited) and gives a CPU tok/s figure for BitNet-b1.58-2B-4T on an ARM CPU (MEASURED from a source, or run bitnet.cpp on this A1 if it installs from a release binary in <= 20 min — else ESTIMATE, flagged); and the parent synthesises the three angles from hunt_args.json (angles[]: metronome-toy, hybrid-readout, iron-fit) into synthesis.md: a ranked top 8-12 by knowledge-per-token with a falsifier each, the round-0 $0 measurements, and the only planned Camber minutes against the 3 GPU-hours/MONTH budget.\""
tests: "\"ONE pi parent, THREE kids (oscillatory, diffusion-llm, one-bit), READ-ONLY web + this box: fetch with curl -sL + python3 tag-stripping, no pip installs, no model downloads except the bitnet.cpp release binary + the 2B-4T weights (~1.2 GB) for conjunct (5) IF it installs without pip in <= 20 min, no ssh, no GPU, no paid API; each kid <= 40 tool calls, <= 45 min wall; kids write their digest + an experiment node each; the parent spawns all three (spawn.json x3), authors no experiment node, writes synthesis.md from the angles, re-probes one citation per digest by opening it, writes probes: per numbered conjunct, sets verdicts; proved needs the kids in evidence_runs. This round is file I/O + curl on the A1: it MAY run beside TM.21; it must NOT run beside the q4-KV bench (if q4-KV is live, wait).\""
title: "\"Research hunt for the metronome: three kid readers (oscillatory/energy/prediction models; diffusion LLMs incl. Mercury open-weights status; 1-bit/ternary quantisation incl. any ternary dLLM) each mapped line-by-line onto the owner sketch, synthesised by the parent into a ranked list with the smallest $0 numpy metronome experiment\""
town: local-maxxing
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# hypothesis:lm-oscillator-research-hunt

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Dispatch order to director-thought = TM.22: one pi parent, three kids, $2, beside TM.21 ok, never beside q4-KV. g15 side-finding for the Prime/SM lane (not mine to build): trove-survey stages need a per-stage timeout_s in the manifest (web hunts exceed 600 s).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted 2026-09-16 22:5xZ by thought-master. The owner (pane line 22:3xZ) asked for agents to hunt research on prediction-, energy- and frequency-based oscillatory models, a hybrid with a heavily quantised diffusion LLM (Mercury), and single-bit quantisation applied to a dLLM — priority: make the internal metronome oscillation system WORK. First attempt: trove-survey on pi (run key ts-metronome-toy-…) — the first reader stage timed out at the manifest 600 s wall (a web hunt with many fetches does not fit one pi stage; the timeout is manifest-only, not an --args knob, and editing the manifest is an engine change = a g15 item, not mine to hand-edit). Second attempt = this node: the same three briefs as kid rounds under the loop, where a kid has 40 tool calls and its own wall budget. The briefs and angles live in hunt_args.json so the orders quote them verbatim.
<!-- THOUGHT:END -->

PARENT REVIEW TM.22 a00-ec4d1114: three reader kids all digested, nodes set, titles set in own words. Verdict inconclusive_lean_proved:65, evidence_runs = the 3 kid experiment nodes. Conjunct probes: (1) every claim URL+date tagged MEASURED|ESTIMATE — scanned all 3 digests, none untagged; (2) >=8 papers per digest — counted oscillatory 11, diffusion 11, one-bit 13, all with mechanism/headline-number/code+licence/CPU-toy/sketch-element; (3) oscillatory 3-closest + smallest numpy — probe opened AKOrN arxiv 2410.13821 title+abstract match, phase-codes 2310.07908 title match, numpy spec present; (4) Mercury open-weights NO cited + ONE open dLLM — probe opened arxiv 2506.17298 Mercury Transformer-diffusion API-mentioned, Fast_dLLM_v2_1.5B named; (5) ternary dLLM NO cited + CPU tok/s — probe opened microsoft/BitNet README, MEASURED figures match byte-for-byte (ARM 1.37x-5.07x, 100B at 5-7 tok/s), A1 tok/s is a flagged ESTIMATE under the conjunct fallback, bitnet not run so no download and no cleanup needed. No falsifier triggered on any kid. synthesis.md written: ranked 8 by knowledge-per-token with a falsifier each, round-0 $0 measurements, only Camber minutes budgeted (30-60 min LLaDA cost probe and 1-3 hr sub-1B ternary QAT) against the 3 GPU-hr/month.
