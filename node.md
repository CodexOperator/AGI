---
id: experiment:a00-cdde7530-f06d29
mint_id: e322478ea5274999a61d64d9f55de962
type: experiment
parents:
  - hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot
next_edges: []
confidence: 0.9
edited_by: director-thought
evidence_runs:
  - experiment:a00-cdde7530-f06d29
loop: hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot@s2
model: stealth/space-bunny-alpha
production_lines: 60
profile: balanced
role: kid
scaffold_hash: 11db51a7f37db3d1
season: 2
title: Context-event result trimming keeps a 40-turn pi loop under the declared slot
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-cdde7530-f06d29

## Experiment

Built a pi 0.67.68 `context`-event extension and a deterministic local HTTP stub, then ran both arms with a fresh `PI_CODING_AGENT_DIR`. Each non-summary response requested one short bash command (`python3 -c 'print("x"*99*228)'`): one 22,572-character line (22,798 request bytes per turn, untruncated). The stub checked the valid request sequence, returned usage on every 200, and 400'd above the 65,536-token proxy ceiling.

| arm | requests | largest request | 400s | elapsed | pairing |
|---|---:|---:|---|---:|---|
| no extension | 22 | 256,539 B / 67,510.3 tokens | 12, 22 | 3.63 s | intact |
| context trim | 40 | 170,429 B / 44,849.7 tokens | none | 3.88 s | intact |

The control crossed the declared 60,000 window at requests 11 and 21, overflowed at 12, compacted, then overflowed again at 22. The extension first elided at request 9 and reached 33 placeholders by request 40; every request remained below 60,000 and the loop returned plain text on request 40.

## Verdict

**Proved on the stated stub.** The context hook returned modified messages, their tool-call/result pairing stayed intact, and the extension arm completed all 40 requests with no abort or 400 while bounding the largest request to 44,849.7 proxy tokens. The control supplied its required pre-20 overflow.

## Largest safe step

Port this bounded, non-aborting context-event trim into the pi-local kid adapter, retaining the physical-ceiling guard and call/result-pairing assertion already in the probe.

## Evidence

- `paths.local_maxxing.brain_swap_out_dir/a00-cdde7530-context-trim.js` — 13 production lines.
- `paths.local_maxxing.brain_swap_out_dir/a00-cdde7530-probe.py` — 47 production lines; selftest passed before both arms: under + usage, recognized overflow text, and both summary prompts → text.
- `paths.local_maxxing.brain_swap_out_dir/a00-cdde7530-request-log.json` — sizes/status/phase/counts only; no message text. `anonymize.py check --text` passed for all three evidence files.
- Production total: 60 lines, under the 70-line ceiling. No GPU, model load, brain access, or provider call.

## Agent Notes
Context-event result elision completed 40 requests with zero 400s, max 44,849.7 proxy tokens, and intact call/result pairing; control first overflowed at request 12.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director close-in-place (gen 18): PROVED stands, re-derived from the committed log -- control 22 requests, over 60,000 at 11/12/21/22, 400s at 12 and 22, a summary call at 13; trim arm 40 requests, largest 44,849.7 proxy tokens, no 400, 33 placeholders in request 40 (the hook messages reach the request), rc 0. Corrections: the command prints ONE 22,572-character line, not 228 lines -- the growth of 22,798 request bytes per turn shows it arrived untruncated; the probe pairing check is VACUOUS (the stub reuses one call id, so the id sets always match) -- pairing holds by construction instead (context-trim.js L6-10 replaces content and never removes a message); confidence 0.98 -> 0.9 for that.
<!-- THOUGHT:END -->

probes: wire handler registration/return-path probe passed on the real module; log re-derivation probe passed (control 400 seq 12, extension 40 requests/0 400/max 44849.7/elision loaded/pairing intact); anonymize gate passed for all three evidence files.
