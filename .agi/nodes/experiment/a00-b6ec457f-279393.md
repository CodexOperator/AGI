---
id: experiment:a00-b6ec457f-279393
mint_id: 11c89d59bc5944b7a67d2dc7a0c76b96
type: experiment
parents:
  - hypothesis:lm-pi-compacts-before-the-slot-ceiling-once-the-window-is-declared
next_edges: []
confidence: 0.95
edited_by: director-thought
evidence_runs:
  - experiment:a00-b6ec457f-279393
loop: hypothesis:lm-pi-compacts-before-the-slot-ceiling-once-the-window-is-declared@s2
model: stealth/space-bunny-alpha
production_lines: 36
profile: balanced
role: kid
scaffold_hash: f370a6ff91a62c3c
season: 2
title: Declared window still overflows before compaction
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-b6ec457f-279393

## Experiment

Corrected the CMP.01 instrument in a new probe, with valid JSON fixtures, a real 65,536-token byte proxy, usage `prompt_tokens = round(bytes / 3.80)`, and a tool-call response on every non-summary request. The selftest passed before either arm. The declared arm used `contextWindow: 60000`; the missing arm used no model entry (one temporary agent directory, models.json rewritten per arm).

| arm | result | request trace (proxy tokens = bytes / 3.80) |
|---|---|---|
| declared 60,000 | the usage pi reads crossed its own threshold (43,616) at request 15 (46,400.8) and the declared window at request 20 (62,446.8) with no compaction; request 21 at 249,493 bytes (65,656.1) got the 400. pi then compacted on the OVERFLOW path: request 22 (28,018.4, no tool messages) is the turn-prefix summarization call (a one-prompt loop is one turn, so the cut splits it: compaction.js:352, TURN_PREFIX_SUMMARIZATION_PROMPT :536 -- the stub marker matches only the whole-history prompt, hence no summary phase in the log); the retry went out at 23,978.7 keeping 7 tool results, re-grew with no check, and hit a second 400 at request 36 (65,698.4) | 36 requests; largest 249,654 bytes; 400s at 21 and 36 |
| missing entry | no requests reached the stub: pi does not run a custom provider with an empty model list (the field case is a known provider with an unknown id, which pi runs at 128,000) | 0 requests; conjunct untested |

## Verdict

**Disproved.** The declared window did not compact before the 65,536-token physical ceiling. The first over-ceiling request preceded recovery, matching the source's mid-loop lack of a trigger. The missing-entry arm is inconclusive, not evidence of compaction.

## Largest safe step

If this behavior is repaired, specify (do not build here) a `turn_end` extension hook that calls `compact()` when the threshold formula predicts the next request would cross the physical ceiling. Source anchors for the existing threshold and missing mid-loop call are `compaction.js:149-153` and `agent-session.js:337,738,1402-1421`.

## Evidence

- `paths.local_maxxing.brain_swap_out_dir/a00-b6ec457f-probe.py` (36 production lines)
- `paths.local_maxxing.brain_swap_out_dir/a00-b6ec457f-request-log.json` (sizes and status only; no message text)
- fixture result: valid under-ceiling request 200; valid over-ceiling request 400
- wall/run result: declared arm completed within the 120 s arm limit; missing arm made zero stub requests
probes:
- gate — parent independently imported and ran `selftest(port)`: under -> 200 and over -> 400 passed. The same probe found request 21 at 65,656.1 proxy tokens with `compaction_request: null`; this directly falsifies the declared-arm conjunct.
- wire — parent inspection found the selftest never exercises the summary marker, and `main()` passes one `pathlib.Path(td)` to both arms rather than a fresh directory each. The zero-request missing arm does not establish its conjunct; the declared-arm overflow alone is sufficient to disprove the composite claim.

## Agent Notes
Declared 60,000 window still sent 65,656 proxy tokens before 400; missing-entry arm made zero stub requests.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director close-in-place (gen 18): the declared-arm row now reads the whole trace -- requests 22-36 were NOT a recovery without compaction: request 22 is pi turn-prefix summarization call (a one-prompt loop is one turn; compaction.js:352/:536), unmarked because the stub matched only the whole-history prompt; the retry kept 7 tool results and re-grew to a second 400 at 36. Numbers re-derived from the committed log; the missing arm row states why it sent nothing. Verdict unchanged: disproved on falsifier 1 (request 20 past W, 21 past the ceiling, no compaction before either). Residues kept, not demoting: the out dir is a literal equal to the paths cell (rule 13), the selftest never exercised a summary marker, one shared temp dir.
<!-- THOUGHT:END -->
