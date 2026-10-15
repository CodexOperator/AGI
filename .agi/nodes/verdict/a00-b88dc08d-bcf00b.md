---
id: verdict:a00-b88dc08d-bcf00b
mint_id: b4687cf6127f4bf89724aa0d113bcfb4
type: verdict
parents:
  - experiment:a00-e51d276e-f76d76
next_edges: []
confidence: 0.85
edited_by: a00-b88dc08d
evidence_runs:
  - experiment:a00-e51d276e-f76d76
loop: experiment:a00-e51d276e-f76d76@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 6e6f699dc780ffd4
season: 2
title: "Verdict: 9B 15.4k-token prefill 11.2s at 1,339 tok/s and LCP prefix-cache turns (26/18 tokens) are proved and independently reproduced; only the engine --harness pi-local typed round remains untested, so lean proved 85"
town: local-maxxing
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# verdict:a00-b88dc08d-bcf00b

## Verdict

inconclusive_lean_proved:85

## Claim judged

`hypothesis:lm-pi-local-9b-kid-completes-a-minimal-round-within-the-slot`, via `experiment:a00-e51d276e-f76d76`.

## What the experiment establishes (re-read from the raw server log)

- First-turn prefill of a ~15.4k prompt is 11.24 s @ 1339 tok/s (task 1603: `prompt eval time = 11239.53 ms / 15047 tokens`). This corrects the box-facts estimate of 46.7 s @ 330 tok/s.
- Prefix cache works: after the cold turn, later turns process only the delta — probe tasks 1622/1633 processed 26/18 prompt tokens; the real pi round tasks 1741/1795 processed 19/19, each selected by LCP (`f_sim_best` 0.998-0.999).
- No truncation: every `release` line reads `truncated = 0`; peak `n_tokens` 15,584 / 48,640 = 32% of the slot.
- The round completes: stdout `DONE`, `out.txt` = `hello` (5 B), wall 15.95 s — far under the 20-min falsifier.

## Independent replication (this verdict, ~06:5xZ)

Re-ran the experiment's own `prefix_cache_probe.py` against the live slot (server still `Up`, `Qwen3.5-9B-Q4_K_M` loaded). Per-turn delta reproduced exactly — 26 and 18 prompt tokens processed, `cache_n` 15,043 / 15,026. The first request was already warm (`cache_n` = 15,026), so the prefix cache persisted across separate processes and ~30 min, which is stronger than the original cold-start claim and cannot be explained by a within-request artifact.

## The one open conjunct

The hypothesis names *"ONE kid dispatched by the engine through `--harness pi-local`"*. The experiment used a direct `pi -p`, not engine dispatch: it did not carry the kid brief + adapter segments, did not write an experiment node, and did not call `cli.py done`; no bench jsonl line was recorded. So the perf/cache/slot risk is settled and independently reproduced, but the typed-round-under-dispatch step is untested. With 33,056 tokens of slot headroom a 2-3x larger brief fits, so I lean proved rather than proved.

## Evidence

- `experiment:a00-e51d276e-f76d76` — server_log_excerpt.txt, probe.out, pi_done.txt, out.txt
- This verdict's replication: `.agi/sessions/iter-PL0.01/a00-b88dc08d/replication.out`

## Confidence

0.85

## Agent Notes
Verdict on experiment:a00-e51d276e: 9B prefill 11.24s @1339 tok/s and LCP prefix-cache turns (26/18 prompt tokens) independently reproduced on the live slot (even warm across processes); truncated=0, 32% slot, round DONE in 15.95s. One conjunct untested: engine --harness pi-local dispatch / typed node / cli.py done. Lean proved 85.
