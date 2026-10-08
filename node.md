---
id: hypothesis:osc-band-fit-preflight
mint_id: 3a31edfbf7ae4f629039f1a1507d89b8
type: hypothesis
parents:
  - goal:qwen3-np64-band-fit
next_edges: []
confidence: 0.55
edited_by: a00-5f731caa
loop: goal:qwen3-np64-noise-band@s2
model: stealth/space-bunny-alpha
origin: swarm-split
profile: balanced
role: parent
scaffold_hash: 23fd4886b319f6ae
season: 2
tags:
  - osc-band
  - preflight
  - local-maxxing
testable_claim: A model-free preflight computes the projected peak RSS of an osc-band measurement from the hf config.json plus the eval arguments alone, and RAISES (never asserts, survives python -O) naming the projection and the box.memory_max budget for every argument set that does not fit — including the current 8-prompt x 512-token x 4-seed np64 grid — while accepting a cut grid and reporting the largest prompts x seeds that does fit. It does not claim the projection is exact; it claims it is derived from the config, monotone in the dominant term (per-prompt full-vocab logits = n_tokens x vocab x dtype_bytes), and never needs torch.
title: "osc band fit preflight: project the peak RSS of an osc-band measurement from config.json alone and refuse an over-budget run before from_pretrained"
town: local-maxxing
---
# hypothesis:osc-band-fit-preflight

# hypothesis:osc-band-fit-preflight

## Measured

| line | what it says |
|---|---|
| `.agi/context/local-maxxing/osc/osc_band_seeds_qwen3_a00-6771cb76.py:46` | `refs = [torch.log_softmax(fixed.forward(model, i).float(), -1) for i in prompts]` — one full-vocab fp32 reference per prompt, ALL LIVE AT ONCE, for all 8 prompts |
| `/data/ml/scratch/osc15/hf/config.json` | `vocab_size 151936`, `hidden_size 1024`, `num_hidden_layers 28`, `num_attention_heads 16`, `head_dim 128` — so one prompt's logits at 512 tokens is 512 x 151936 x 4 B = **311 MB**, and 8 of them is 2.49 GB of references alone |
| `.agi/config.json:148` | `"memory_max": "6G"` — the budget is a CONFIG CELL and already exists |
| `journalctl -k`, cited in experiment:a00-6771cb76-8469e1 (director correction, gen 32) | both np64 kids were killed by CONSTRAINT_MEMCG, anon-rss 6.19 GB |
| `datasets/osc-band/2026-09-24-qknorm/a00-bcea484d-probes/probe_noise.log` | the np32 probe finished 3 seeds in 182 s **on a smaller model** — the reason it fit is model size and eval size, not the harness |

## CLAIM

A model-free preflight exists that, from the hf `config.json` plus the eval
arguments alone, computes the projected peak RSS of an osc-band measurement and
**refuses, by name and before any weight is loaded**, every argument set whose
projection exceeds the `box.memory_max` budget; and for the argument sets that
do fit it reports the largest (prompts x seeds x budgets) that fits, so the next
round's brief carries a number instead of a hope. It does NOT claim the
projection is exact — it claims it is derived, named, monotone in the term that
actually dominates (per-prompt full-vocab logits), and that the refusal
survives `python -O`.

## Dispatch line

**config-max:** the memory budget is read from `box.memory_max` in
`.agi/config.json` at runtime. The cgroup limit FILE path is a `paths.*` cell
that does not exist — do not create it and do not hardcode
`/sys/fs/cgroup/memory.max`; if a cross-check against the live cgroup is wanted,
it must go through a config cell, and until that cell exists the config budget is
the authority.

**template-max:** nothing moves to a template.

**code:** the resolver that does not exist is
`project_peak_rss(config, n_prompts, n_tokens, dtype_bytes) -> (bytes, terms)`
plus `fits(peak, budget) -> (bool, reason)` and
`max_prompts_seeds(...)`, and a `preflight(...)` that raises (never asserts) when
a run does not fit.

## FALSIFIERS

1. **The stub that never reads the config.** A preflight whose numbers are
   literals (or whose `n_prompts` argument is ignored) passes every "does it
   refuse the big grid" test and still lets a 6.19 GB run start. Provable by
   feeding a config with a doubled `vocab_size` and a halved one and showing the
   projection moves by the right factor.
2. **The near-miss is a REFUSAL THAT IS NOT A REFUSAL** — printing
   `WOULD NOT FIT` and exiting 0. A caller that only checks the exit code starts
   the run.
3. **`assert` instead of `raise`** — the falsifier-7 shape that already killed one
   artifact in this chain: under `python -O` the whole gate disappears.
4. **A poisoned import.** The preflight must not need `torch`; a test that
   makes `import torch` raise proves the model-free property, because the
   alternative implementation (measure the real thing) is the one that costs the
   53s and the 3.2 GiB this exists to avoid.
5. **Wrong denominator for the dominant term.** Counting tokens or layers
   instead of `n_prompts x n_tokens x vocab x dtype_bytes` yields a projection
   ~3 orders of magnitude too small — a preflight that says "fits" is worse than
   none.

## TESTS

- **F1 derivation:** the per-prompt logits term equals `n_tokens * vocab * 4`
  computed by hand from the real config; doubling `vocab_size` doubles it.
- **F2 the current grid is REFUSED:** 8 prompts x 512 tokens x 4 seeds over 4
  budgets exits non-zero and names both the projection and the 6 GiB budget.
- **F3 a cut grid is ACCEPTED:** 2 prompts x 512 tokens x 3 seeds exits 0 and
  prints the peak, so the tool is not a blanket "no".
- **F4 `-O` survival (kills falsifier 3):** F2 re-run under `python -O` gives
  the identical non-zero exit.
- **F5 model-free (kills falsifier 4):** with `torch` import poisoned, the
  module still computes; with `AutoModelForCausalLM.from_pretrained` poisoned to
  raise, it still computes.
- **F6 no literals (kills falsifier 1 + the config-max rule):** grep for
  `6G`, `6 * 1024`, `/sys/fs/cgroup` in the new file returns zero hits, and the
  budget value read equals `box.memory_max` from `.agi/config.json`.
- **F7 monotonicity:** the projection is non-decreasing in prompts, tokens and
  seeds, and `max_prompts_seeds` returns a value that passes F3's predicate and
  one more prompt that does not.

## FILE SCOPE

- NEW `.agi/context/local-maxxing/osc/osc_band_fit_<mint>.py`
- NEW `.agi/context/local-maxxing/osc/osc_band_fit_<mint>_test.py`
- the ONE experiment node for this round

Nothing else. In particular do NOT edit `osc_band_seeds_qwen3_a00-6771cb76.py`,
`osc_band_matched_uniform_a00-a721f95f.py`, `osc_band_call2_a00-cc7b25cc.py` or
`.agi/config.json` — p1 and p2's kids are live against those files right now and
`config.json` is a shared tree-level file.

## CEILING

- kids: 1 (this hypothesis -> 1 experiment)
- production lines: 40 per conjunct
- pi parents: 0
- USD cap: n/a — MODEL-FREE. This round loads no weights and calls
  `python3 .agi/context/local-maxxing/model_slot.py` for nothing.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted under goal:qwen3-np64-band-fit (my swarm-osc36 subgoal, goal_id G5.22.1.2.3). WHAT THE ORDER SAID: "hypothesis (the hypothesis schemas form, parent = that id, committed) -> kids -> experiments -> report" and "at most ONE model-running kid per swarm at a time" (room post, 02:21). WHAT THE MACHINE ACTUALLY DOES: the np64 qwen3 band has produced zero rows in two independent attempts and the director gen-32 correction attributes both to CONSTRAINT_MEMCG at anon-rss 6.19 GB against a 6 GiB scope; osc_band_seeds_qwen3_a00-6771cb76.py:46 holds one 311 MB full-vocab fp32 reference per prompt for all 8 prompts, i.e. 2.49 GB of references before any seed loop, plus fp32 weights. So the measurement size is knowable from config.json with no weight loaded, which is exactly the slot p2 is NOT using. THE NEAR MISS: writing a hypothesis that says "run a smaller grid" satisfies the words and loses the mechanism - it re-spends a whole kid to learn a number the config already carries, and the third identical attempt at the full grid is the failure mode both dead kids share.
<!-- THOUGHT:END -->
