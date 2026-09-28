---
id: experiment:director-thought-brain-swap-2026-09-24
mint_id: d8552a791ac34d01a8279eaf209e6680
type: experiment
parents:
  - hypothesis:lm-bonsai-27b-on-the-prism-fork-is-the-pi-local-brain
next_edges: []
edited_by: director-thought
scaffold_hash: 9e4a9ecf0cc24362
season: 2
title: "TMM.76 step 1: the 0-credit lane's brain is LIVE -- OrcaBonsai C2 (Bonsai 27B + abliterate LoRA scale 2) on the PrismML fork with q4_0 KV: 7.29 GB VRAM, one 65,536-token slot, 20.2-20.5 tok/s decode, ~250 tok/s prefill, a pi-local tool-call turn in 17 s; plain B met VRAM/slot/decode (21.25 tok/s) but its only smoke hung on pi's open stdin before the owner switched to Orca"
town: local-maxxing
verdict: inconclusive_lean_proved:90
---
# experiment:director-thought-brain-swap-2026-09-24

# TMM.76 step 1 -- the 0-credit lane's brain is LIVE

**Run by director-thought in its own window** (TMM.76; OWNER 00:xZ-01:0xZ 09-24 verbatim on goal:g5), 01:04Z-01:30Z 09-24, 0 USD, no kid.
Evidence under `paths.local_maxxing.brain_swap_out_dir`: `before.json` · `serve.json` · `timings.json` · `smoke.json`.

## What serves now
```
container  brain-orcabonsai27b (restart unless-stopped) on the router's loopback port 8080 -- the router container llama-server is STOPPED (01:05:38Z)
model      Ternary-Bonsai-2-27B-PTQ1_0 + the OrcaBonsai abliterate LoRA at scale 2.0 (= C2), on the PrismML fork b10685 inside the stock server-cuda image
line       -c 65536 -ngl 99 -fa on -np 1 -ctk q4_0 -ctv q4_0 --jinja --temp 1.0 --top-p 0.95 --top-k 20 --lora-scaled <lora>:2 --alias OrcaBonsai-27B-C2
proof      GET /lora-adapters = [{id 0, bonsai-abliterate-lora.gguf, scale 2.0}] · /v1/models = [OrcaBonsai-27B-C2] -- the scale is in the launch line,
           so a container restart cannot drop it (the POST method of SWR-C2.02 would reset to 0 on restart)
pi         the local-town provider lists OrcaBonsai-27B-C2 first (contextWindow 60000, maxTokens 8192); its other three entries unchanged
```

## Measured
| | plain B (01:05-01:21Z) | Orca C2 (01:21Z-) | bar |
|---|---|---|---|
| VRAM (nvidia-smi shim) | 7,234 at load · 7,268 after requests | 7,284 at load · 7,292 after requests | <= 8,192 MiB |
| slot | 1 x 65,536 | 1 x 65,536 | 65,536 |
| decode, distinct prompts, 256 tokens, temp 0 | 21.25 / 21.06 / 22.10 (median 21.25) | 20.17 / 20.51 | >= 17 tok/s |
| prefill (1.1-2.4K-token prompts) | 263.2 / 237.2 / 252.8 | 255.3 / 249.4 | -- |
| load to healthy | 85 s (cold page cache) | 35 s | -- |
| pi-local tool-call turn | HUNG (see below) | PASS: 17 s, read(note.txt) -> answer 4217 == expected | one turn |

- Before (01:04Z): the router in router mode, restart unless-stopped, the 9B loaded and idle (one slot of 49,664) · GPU 6,730 / 8,192 MiB ·
  host RAM available 10,748 MiB · 0 live agents. After: host RAM available 8,882 MiB. The swap cut the served context from 49,664 to 65,536
  tokens per slot (+32 pct) and moved the brain from HumanEval 78.0 pct (the 9B) to the 27B family's 86.6-87.2 pct (experiment:a00-bb10233d-5a7f1f
  and the C2 gate: 143/164).
- plain B's first measured request read 16.99 tok/s (the first real request after the warm-up); its repeat was a byte-identical prompt (a slicing
  slip -> a prompt-cache hit, 4 prompt tokens) and is NOT a prefill reading; the three distinct-prompt rows are the clean ones.
- the smoke on C2: two server requests -- 1,003 prompt tokens at 217 tok/s then 50 generated (the tool call); then 28 NEW prompt tokens (a
  prefix-cache hit) and 123 generated at 21.3 tok/s (the answer). A pi-local turn pays its system prompt once.

## The hang (attempt 1, plain B) -- a harness defect, not the model
`pi -p` ran from a tool shell with stdin left OPEN: 0 bytes out, and the server log shows NO request from pi -- it waited for piped input that
never ended; the owner stopped it. The engine's adapter spawns pi with `stdin=DEVNULL` and a new session (extensions/agi/bin/adapters/pi_adapter.py),
so a dispatched kid does not hit this; attempt 2 ran `setsid ... < /dev/null` and passed in 17 s. Rule for any hand-run pi: close stdin.

## Verdict on the claim as written
The claim names the PLAIN 27B. Plain B cleared VRAM, slot and decode, but its one smoke attempt hung on the harness defect above, and the OWNER
switched the brain to the Orca variant ("Also we need to run the orca bonsai model instead of", 01:1xZ) before a clean re-run on B. C2 -- the same
base weights, fork, line and KV format plus the LoRA at scale 2 -- cleared all four bars. So: inconclusive_lean_proved:90 for the literal claim
(B's tool-call turn is untested with stdin closed), and the 0-credit lane's brain is LIVE on C2.

## Next (TMM.76 step 2)
LEAVES: hypotheses split until one leaf = one pi-local kid on OrcaBonsai-27B-C2 (harnesses.pi-local models + allowed_extra in the director's branch
config), ONE local kid at a time town-wide, each leaf recording turns / prefill / wall.
