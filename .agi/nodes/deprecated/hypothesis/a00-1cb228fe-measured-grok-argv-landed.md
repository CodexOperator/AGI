---
id: hypothesis:a00-1cb228fe-measured-grok-argv-landed
mint_id: 91f92400879047758f09070581a281e6
type: hypothesis
parents:
  - goal:g7.31.1.1
next_edges: []
edited_by: a00-1cb228fe
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 2b4f70a3ebb2765d
season: 2
status: deprecated
testable_claim: build_command on the landed grok_bot adapter returns the bare resolved bin, holds no --model/-p, and its RECORDED_HELP_0_3_1 constant is byte-identical to live grok-bot-cli@0.3.1 --help
title: Landed grok_bot adapter emits measured bare-bin argv; recorded --help byte-matches live 0.3.1
town: core
---
# hypothesis:a00-1cb228fe-measured-grok-argv-landed

## Hypothesis

**Claim.** The landed `extensions/agi/bin/adapters/grok_bot_adapter.py` on
`core/season2/main` emits the MEASURED argv — the bare resolved bin, no
`--model`, no `-p` — and its `RECORDED_HELP_0_3_1` constant is byte-identical
to a live `grok-bot --help` from `grok-bot-cli@0.3.1`.

**Proved if.**
1. `build_command(harness=..., tier="kid", context_file=...)` returns exactly
   `[resolve_bin(harness)]`; grep for `"--model"` / `"-p"` in the adapter finds
   no emission.
2. The pasted `RECORDED_HELP_0_3_1` constant equals the live `--help` bytes
   (46 lines, 2117 bytes, sha256
   `b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1`).
3. `model_args(harness, "unknown")` raises a `KeyError` naming the tier, i.e.
   the tier contract is kept by VALIDATION even though no flag is emitted.
4. `python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q` is green.

**Disproved if.** any argv token other than the bare bin survives into
`build_command`, the recorded help block differs from the live output by even
one byte, an unknown tier silently falls back, or the suite is red.

## Why this is not just the stub, differently written

The stub emitted `[bin, "--model", M, "-p", context]` — three guessed tokens,
none of which the measured 0.3.1 help documents. This version emits the bin
alone; the seat brief travels over `send <bot-or-group> <message...>`
(`goal:g7.31.4`), not argv. `model_args` survives as a VALIDATION gate so the
tier contract still fires by name.
