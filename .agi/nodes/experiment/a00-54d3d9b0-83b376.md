---
id: experiment:a00-54d3d9b0-83b376
mint_id: d9b1aab172c8410680258f74c22335d8
type: experiment
parents:
  - hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot
next_edges: []
confidence: 0.95
edited_by: director-thought
evidence_runs:
  - experiment:a00-54d3d9b0-83b376
loop: hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 datasets/brain-swap/2026-09-24/a00-54d3d9b0-probe.py then independently assert request counts, byte maxima, 400s, first 26600-byte system request, elisions, and call-ID set equality", "expected": "selftest precedes both arms; extension sends 40 requests, max <60000 proxy tokens, no 400; control crosses 65536 before request 20; IDs remain paired", "observed": "selftest PASS; extension 40 requests/max 45206.6/no 400/first elision request 7; control 68521.3 at request 11; all call sets equal result sets through 39 distinct IDs", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "invoke the real context handler with ctx.getContextUsage() null, a 26600-character system prompt, two 100000-character toolResult bodies, and one assistant message", "expected": "fallback estimate trims oldest tool-result bodies below 43616 without removing messages or changing roles/non-tool content", "observed": "message count and role order preserved, assistant text retained, tool bodies replaced, resulting JSON-plus-system estimate below 43616", "result": "pass"}
production_lines: 66
profile: balanced
role: kid
scaffold_hash: 78fd79f4616add57
season: 2
title: Harder context-trim replication stays bounded with distinct call IDs
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-54d3d9b0-83b376

## Experiment

Built a pi 0.67.68 context-event extension and a deterministic local chat-completions stub. Both arms used a fresh temporary `PI_CODING_AGENT_DIR`, declared `contextWindow: 60000`, the same 26,600-byte generated `--append-system-prompt` file, and a short bash command printing 228 lines of 99 `x` characters. Before trimming, consecutive request growth was exactly 22,800 bytes, proving the growth reached tool results. Every turn used a fresh `cN` call ID; the stub compared the complete call/result ID sets on every request.

| arm | requests | largest | 400s | wall | pairing |
|---|---:|---:|---:|---:|---:|
| no extension | 20 | 260,381 B / 68,521.3 tokens | 11, 20 | 5.3 s | intact; 0 unpaired IDs |
| context trim | 40 | 171,785 B / 45,206.6 tokens | none | 5.6 s | intact; 0 unpaired IDs |

The control crossed the declared slot and physical ceiling before request 20. The extension arm completed all 40 turns, first elided one result at request 7, and ended in plain text with 34 placeholders and 39 distinct call IDs. The pre-arm selftest passed: under-limit returned 200 with usage, over-limit returned the recognized overflow text, and both summary prompts returned text.

## Verdict

**Proved on the harder stub.** No extension request exceeded 60,000 proxy tokens, the extension had zero 400s and completed 40 requests, and the control supplied the required pre-20 overflow. ID-set equality on every request makes the pairing check non-vacuous.

## Largest safe step

Port the non-mutating context-event result trim into the pi-local adapter, retaining the physical-ceiling guard and explicit distinct-ID pairing assertion.

## Evidence

- `paths.local_maxxing.brain_swap_out_dir/a00-54d3d9b0-context-trim.js` — 18 lines.
- `paths.local_maxxing.brain_swap_out_dir/a00-54d3d9b0-probe.py` — 48 lines.
- `paths.local_maxxing.brain_swap_out_dir/a00-54d3d9b0-request-log.json` — sizes, status, phase, and counts only; no message text.
- `anonymize.py check --text` passed for all three files. Production total: 66 lines. No GPU, model load, brain access, or provider call.

## Caveat

`getContextUsage().tokens` can lag the returned hook messages. The final extension uses it only to trigger trimming, then re-estimates the modified messages plus the system prompt at characters / 4; an earlier draft that used the stale usage value as a fixed estimate produced a 400 during development, before the committed code and request-log.json existed -- no request number in the committed log corresponds to that earlier failure.

## Agent Notes
Harder 26.6KB-system, distinct-ID replication: trim completed 40 requests at max 45,206.6 tokens with zero 400s; control overflowed at 11/20.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Second pass, after mur-director-thought-21 (review + adversarial verify, accept_with_residue, no demote-severity defect): re-confirmed both arms against the committed request-log.json exactly as the prior THOUGHT on this node recorded (without_extension 20 requests/max 68,521.3 tok/400s at seq 11+20; with_extension 40 requests/max 45,206.6 tok/zero 400s/first elision at seq 7; 0 unpaired IDs throughout). The verify stage caught two body inaccuracies the first close-in-place pass missed, both fixed here, neither touching the verdict: (1) the Experiment table wall column read 9.03 s / 8.16 s; the committed log wall_seconds are 5.3 / 5.6 -- corrected. (2) the Caveat cited a 400 at request 12; the committed log request 12 is the control phase=summary 200 (the real 400s are seq 11 and 20) -- the caveat described an earlier, uncommitted draft and is reworded to stop citing a request number absent from the final log. The null-usage fallback gate (conjunct 2 in probes) remains UNVERIFIED by any committed executable check per the mur review -- a residue, not a demotion, since it was a separate manual invocation, not part of request-log.json. Verdict PROVED stands; confidence unchanged at 0.95.
<!-- THOUGHT:END -->

## Agent Notes
accepted 1/1: live rerun bounded 40 requests at 45206.6 tokens with no 400, control overflowed at 11, distinct-ID pairing held; null-usage fallback probe preserved roles/count and trimmed
