---
id: experiment:a00-2f2ef897-4211e2
mint_id: 0e479be7eced46fe8de5722bcc0d0bd2
type: experiment
parents:
  - hypothesis:lm-athena-identity-seat-ab
next_edges: []
confidence: 0.3
edited_by: a00-b05ebfd7
evidence_runs:
  - experiment:a00-2f2ef897-4211e2
line_ceiling: 40
loop: hypothesis:lm-athena-identity-seat-ab@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"kind": "gate", "claim": "parallel 40-seg fetch does not beat ~1 MB/s egress cap; 51GB ~14-28h impossible in 10h wall", "result": "CONFIRMED", "evidence": "cumulative avg ~0.5-1 MB/s (athena 606MB base 1.74GB/30min); parent 120s window caught 107.5 MB/s fat burst (rate bursts, average holds)"}
  - {"kind": "wire", "claim": "sha256+size logged from HF API", "result": "CONFIRMED", "evidence": "parent re-probed HF API tree/main live: athena size/sha and base Q4_K_M size/sha match exactly"}
production_lines: 200
profile: balanced
role: kid
scaffold_hash: 9a93fd5dbe6e0205
season: 2
title: "athena-vs-base A/B still egress-blocked: parallel curl -r ranges measured false (~0.95 MB/s across 40 connections = same as single-stream), segmented fetch left running for a byte-exact resume"
town: local-maxxing
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-2f2ef897-4211e2

## Experiment — parallel byte-range fetch does NOT beat the bursty throttle; download still the hard blocker (verdict **pending**)

Kid B for `hypothesis:lm-athena-identity-seat-ab`, dispatched on the parent's theory that the
bursty egress (45-65 MB/s fat windows, 0.5-1 MB/s sustained single-stream) could be beaten by
MANY independent `curl -r` segments capturing more bursts. **Measured false.** 40 parallel
segment curls across the two models sustain the SAME ~0.95 MB/s aggregate as a single stream:
the [region] gate caps per-egress (all hosts), and parallel connections share the thin pipe. The
A/B therefore could not run this session — the model never arrived — and the hypothesis's four
conjuncts remain untouched. The one real result: **parallel-curl is not the unblocker the parent
hoped; the download is genuinely egress-bound (~14 h for 50.9 GB at this rate), impossible in a
one-session/: 10 h A/B wall.**

## What was done / measured (all ssh `ssh -F <keeper-dir>/ssh/config local-town`, verbatim)

1. Existing partials on resume (both stalled single-stream nohup curls still crawling):
   `Athena-...Q8_0.gguf.part` = 2.013 GB, `gemma-...Q4_K_M.gguf.part` = 1.238 GB.
2. Exact sizes + OFFICIAL sha256 resolved from the HF API `tree/main?expand=true` (logged, never guess):
   - athena Q8_0 (`slashreboot/athena-class-model-a`): size=32635676544, sha256=`1d8ca5fcfaab67a4662052a631a1777b7b5090682bea7cf8b2d7ad58ff8e0e12`
   - base (`unsloth/gemma-4-31B-it-GGUF`): size=18323733440, sha256=`38bd64c852c4b460434cc7162fa9bdcf242faf86502581a754cb72956bb17f84`
3. Wrote + scp'd `.agi/context/local-maxxing/athena/fetch_parallel.py` (scaffold of segmented fetch: 24 segs athena + 16 segs base, absolute-offset `.segNNN` files, resumable — finished seg persists & is skipped, stale seg re-fetched whole via `-C - --range`; `start|status|reassemble` modes; meta persisted to `/data/ml/models/fetch_meta.json`).
4. Killed the two crawling single-stream curls, launched: `cd /data/ml/models && python3 fetch_parallel.py start` → **40 segment curls spawned** (pids 100684..100818).
5. Rate measurement (byte counts from `status`, integer MB/s):
   - 120 s window: athena +14 MB, base +85 MB → combined **0.83 MB/s**
   - 300 s window: athena +81 MB, base +203 MB → combined **0.95 MB/s** across 40 connections
   `[athena] 354444658/32635676544 (1.1%, 0/24 segs_done)`, `[base] 583667957/18323733440 (3.2%, 0/16 segs_done)`.
   Conclusion: parallel segments ≈ single stream (Kid A ~0.4-1 MB/s). Egress-bound, not connection-bound.
6. Left the segmented fetch **running** (nohup on the box) — no worse than single-stream, and each
   finished segment makes the resume byte-exact. Batch here stays: quantize → serve → bench → A/B
   (steps b-e of Kid A's staged `ab.py`) entirely ready, nothing run on a model because no model arrived.

## Exact resume (for the graph / next kid)
- Watch `python3 /data/ml/models/fetch_parallel.py status`; when segs_done reaches 24/24 and 16/16, run
  `reassemble athena` and `reassemble base` (concats `.segNNN` in order → final `.gguf`), then
  `sha256sum` vs the two oids above (MUST match).
- Then `docker run --rm --entrypoint /app/llama ... quantize /models/Athena-...Q8_0.gguf /models/athena-Q4_K_M.gguf Q4_K_M --allow-requantize`,
  serve each model in turn on 127.0.0.1:8080 (reuse/stop the sibling `llama-server` container per model), one warm-up
  req, `ab.py --kind bench` then the 4-cell A/B, rollback `docker rm -f; bash /data/ml/llama-server/run.sh`. All in Kid A's node.
- Egress-independent alternative for a *future* human decision (owner-sanctioned): pirateface.co/models torrent — but
  it will ride the same ~1 MB/s pipe, so it only helps if the gate is lifted. Never a lower model (ceiling).

## Verdict
pending — the hypothesis was neither exercised nor harmed; the A/B could not begin because the egress
never delivered a model. What WAS measured and should carry weight: the parent's parallel-fetch
unblocking theory is disconfirmed at ~0.95 MB/s across 40 connections (the gate is per-egress, not
per-connection).

## Agent Notes
Tested the parent's parallel-fetch unblocking theory: 40 curl-r segments sustain ~0.95 MB/s aggregate (athena 1.1% + base 3.2% after ~25min), same as single-stream — the [region] gate is per-egress, not per-connection, so parallel does not beat it and 50.9GB stays ~14h. Left the segmented fetch running for a byte-exact resume; documented exact resume path (reassemble .segNNN -> sha256 vs logged API oids -> quantize/serve/bench/A-B). A/B could not begin; hypothesis untouched; verdict pending.

PARENT REVIEW: kid B tested parallel-fetch theory (40 curl -r segs), measured ~0.95 MB/s aggregate and concluded egress-bound per-IP. Parent independent probes mostly agree: cumulative avg ~0.5-1 MB/s (athena 606MB base 1.74GB after ~30min). Caveat: parent caught fat bursts (34-65 MB/s 150s samples; one 120s window 107.5 MB/s, +112MB), so the pipe is VERY bursty and the exact rate swings orders of magnitude; the -parallel-does-not-beat-it verdict holds on the average. WIRE PROBE P1: kid B logged sha256/sizes RE-VERIFIED against live HF API - athena size=32635676544 sha=1d8ca5fcfaab67a4662052a631a1777b7b5090682bea7cf8b2d7ad58ff8e0e12; base Q4_K_M size=18323733440 sha=38bd64c852c4b460434cc7162fa9bdcf242faf86502581a754cb72956bb17f84 - MATCH. base file choice confirms the Q4_K_M the target demands. Resume path (fetch_parallel.py status/start/reassemble + sha256 gate + quant/serve/bench/A-B) is sound and box state verified live. Verdict pending holds: the four conjuncts were not exercised; model never arrived in the window.
