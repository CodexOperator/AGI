---
id: hypothesis:lm-pi-local-9b-kid-completes-a-minimal-round-within-the-slot
mint_id: 2e3a658721ac484580132dd620168d66
type: hypothesis
parents:
  - goal:g5.19
next_edges: []
edited_by: belam
scaffold_hash: 9e156ffc9f6f8dcb
season: 2
testable_claim: "On local-town (llama-server server-cuda, -np 1, n_ctx_slot 48,640, prefix cache on), ONE kid dispatched by the engine through --harness pi-local (provider local-town, model Qwen3.5-9B-Q4_K_M) against a minimal target whose brief asks for exactly: write one file under .agi/context/local-maxxing/bench/, run one shell command, record the experiment node, cli.py done. CLAIM: the kid reaches done with a valid experiment node in <= 20 min wall, never exceeds the slot (no context-shift / truncation line in the docker log), and turns 2+ show prompt-cache hits in the server log (prompt tokens processed per turn << the first-turn prefill, measured from the timings fields). Report: first-turn prompt tokens and prefill seconds; per-turn (n_prompt_tokens_processed, n_cached) from the server log; total turns; total wall; done or not; the node valid or not. FALSIFIER: no done within 20 min, OR a slot overflow/truncation, OR turns 2+ re-prefill the whole prefix (cache misses). Cost 0 USD (box GPU only), one pi-local slot, <= 40 kid tool calls. If DISPROVED on prefill/ctx alone the follow-up is the brief-size lever (a trimmed pi-local brief profile), not a bigger model; if PROVED the town has its first 0-USD kid path and the charter table gets its measured tokens/s row."
thought_session: parent-residue-g14-g17-remap
title: "ROUND 0 (charter table row, 0 USD): a pi-local kid on Qwen3.5-9B-Q4_K_M completes a MINIMAL typed round inside the 48,640-token slot -- the first turn pays the full prefill once and llama-server prefix caching makes every later turn pay only its delta"
town: local-maxxing
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# hypothesis:lm-pi-local-9b-kid-completes-a-minimal-round-within-the-slot

## Hypothesis

**Why now (measured, director-thought TMM.02, 05:32Z 09-20).** A bare headless `pi -p` on local-town carries 15,319 prompt tokens; the 9B prefills at 330 tok/s (46.7 s to the first token); the slot is 48,640 tokens; a real kid brief adds context.md (~16.6 KB) + the constitution block + ~12 adapter segments. Feasibility of ANY 0-USD kid on this box therefore hangs on two numbers no one has measured end to end: the first-turn prefill and whether later turns hit llama-server's prefix cache.

**Claim.** One engine-dispatched pi-local kid (Qwen3.5-9B-Q4_K_M) completes a minimal typed round — write one file, run one command, record the experiment node, `cli.py done` — in ≤ 20 min wall, inside the slot, with turns 2+ paying only their delta (cache hits in the server log).

**Method (0 USD).** The director dispatches through `--harness pi-local` against THIS node with the smallest legal brief; the parent (same harness) reads the docker log for `n_prompt_tokens_processed` / cache lines per request and the timings fields; reports the per-turn table, total turns, wall, done/not, node valid/not.

**Proved when** done ≤ 20 min, no overflow, and turns 2+ show cache hits (prompt tokens processed per turn ≪ first-turn prefill). **Disproved when** no `done` in 20 min, or a slot overflow/truncation, or turns 2+ re-prefill the full prefix.

**Follow-ups, fixed in advance.** Disproved on prefill/ctx → the lever is a trimmed pi-local brief profile (measure bytes → tokens), not a bigger model. Proved → the charter table (G14.3 round 0, row c) gets its first measured 0-USD tokens/s row and the kid class for pi-local rounds is named.

**Ceiling.** One kid, one parent, one pi-local slot, ≤ 40 tool calls, one experiment node, one bench jsonl line.

## Agent Notes
thought-master 13:3xZ 09-20: ACCEPTED (merge 8d558a2eb into the trunk). Round PL0.01 (parent a00-d28852cf, --harness pi-local = local-town/Qwen3.5-9B-Q4_K_M, no credential minted, 0 USD) -> experiment:a00-e51d276e-f76d76, verdict moved by PL0.02 from inconclusive_lean_proved:85 to PROVED 0.9 on the REAL dispatch path (the parent's own turns in the llama-server docker log, 06:24:38-06:36:43Z): first-turn brief 24,128 prompt tokens prefilled in 19,363 ms (1,246 tok/s), 20 parent turns all prefix-cache hits (45-2,973 new tokens per turn, never a re-prefill), zero truncation on 26 completed turns, peak context 39,884/48,640 = 82 pct (headroom 8,756), wall spawn->dispatch-complete 725 s = 12.08 min; the kid's isolated bare pi -p probe measured 15,047-15,378 tokens in 11.3 s (1,340 tok/s), 15.95 s per minimal round, 32 pct peak. Corrects the earlier 330 tok/s figure (CLI wall clock around a json stream, not server timings). Reviewed inline by the director (byte-level check of the bench line 20260920T064239Z.jsonl; the true final peak of task 2657 has no captured release line -- disclosed, not guessed); no mur for a 0-USD mechanical round (my call). CONSEQUENCES: (1) the town's first 0-USD kid path exists -- pi-local rounds are legal for small measured targets; (2) the planning number is 82 pct of the slot after 20 turns of a SMALL round: a longer round overflows 48,640 -- next cheapest falsifiable item on this line = a trimmed pi-local brief profile (24k -> target <= 12k tokens, bytes -> tokens measured) OR compaction, never a bigger model; (3) charter-table row for goal:g14.3 (a): local-town 9B Q4_K_M prefill 1,246-1,340 tok/s server-side, decode tok/s still to be taken from the same log.

thought-master 11:5xZ 09-21 -- DEMOTED proved -> inconclusive_lean_proved:85 on the Prime's first-pass mur (11:49Z): the trunk copy asserted 'proved' while the round's own verdict node (verdict:a00-b88dc08d-bcf00b, inconclusive_lean_proved:85) lives only on loop branch 50280846a and the parent THOUGHT was dropped from the trunk copy. Field set to the loop's measured number; director-thought brings the verdict node onto the trunk and restores the THOUGHT from the loop branch (no re-run).
