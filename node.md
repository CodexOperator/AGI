---
id: experiment:a00-989a0516-9cd7e6
mint_id: 843d3a683b3e40379fc8c604c93aa8c8
type: experiment
parents:
  - hypothesis:lm-oscillator-research-hunt
next_edges: []
confidence: 0.6
edited_by: a00-989a0516
evidence_runs:
  - experiment:a00-989a0516-9cd7e6
line_ceiling: 40
loop: hypothesis:lm-oscillator-research-hunt@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 104
profile: balanced
rebrief_request: "Reader digest is a research deliverable, not code: 69-line trove + 35-line node = 104 lines vs 40-line code ceiling. Digest cannot shrink below the 8-sourced-papers + end-question conjuncts. Recommend reader-kid ceiling exemption or ceiling 120 for read-only research output."
role: kid
scaffold_hash: 607c44904f4e987b
season: 2
title: "One-bit hunt: ternary substrate solid for LLMs, no ternary dLLM exists (greenfield)"
town: local-maxxing
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-989a0516-9cd7e6

## Experiment

Read-only hunt on one-bit/ternary quantisation and whether it applies to a diffusion LLM. Fetched 13 papers/models via curl+arxiv API + web_search (2026-09-16). Digest written to .agi/context/local-maxxing/troves/2026-09-16-oscillatory/one-bit.md.

## Findings (end-questions answered)

1. **Ternary dLLM exists? NO.** arXiv searches 2025-2026 for "ternary masked diffusion", "1-bit diffusion" (cat:cs), "BitNet diffusion" all return zero entries. Closest work (MDM-Prime-v2, arXiv 2603.16077) uses binary ENCODING of the subtokenizer, not binary/ternary WEIGHTS. Greenfield for the owner.
2. **Ternary substrate is solid on LLM side.** BitNet b1.58 (arXiv 2402.17764) = {-1,0,1} weights matching fp16 at equal size+tokens; BitNet-b1.58-2B-4T open weights MIT (HF); bitnet.cpp CPU inference (arXiv 2410.16144/2502.11880): 1.37-5.07x ARM / 2.37-6.17x x86 speedup, 100B on ONE CPU at 5-7 tok/s (MEASURED).
3. **Open dLLM to QAT: LLaDA-8B**, Apache-2.0, on par with LLaMA3-8B (arXiv 2502.09992 + HF). Mercury (arXiv 2506.17298) is commercial-scale diffusion LLM but weights NOT open-released.
4. **Fit:** ternary 7-8B ~1.6-1.9 GB (ESTIMATE) fits A1 CPU 23 GB and 8 GB GPU; measured arm64 4-core tok/s not published -> ESTIMATE 15-35 tok/s for ternary 2B, verify on A1.
5. **$0 first step:** build+run bitnet.cpp BitNet-b1.58-2B-4T on the A1 (MIT, no pip) and measure tok/s; then numpy-probe a ternary matmul on a LLaDA linear block. QAT of full LLaDA-8B to ternary would exceed the 3 GPU-hr/month Camber budget (ESTIMATE 4-10 hr); PTQ-small (BiLLM/PTQTP) fits in 1-3 hr.

## Evidence

Sources read (all URL+date+MEASURED/ESTIMATE tagged in one-bit.md): 2402.17764, 2504.12285+HF card, 2410.16144/2502.11880+microsoft/BitNet README, 2411.04965, 2402.11295, 2310.00034, 2402.04291, 2502.02631, 2509.16989, 2506.17298, 2502.09992+LLaDA repo/HF, 2608.00146, 2603.16077. Digest: ".agi/context/local-maxxing/troves/2026-09-16-oscillatory/one-bit.md" (11.3 KB).

## Agent Notes
returned one-bit digest
