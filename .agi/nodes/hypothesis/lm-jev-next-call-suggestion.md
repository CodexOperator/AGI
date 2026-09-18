---
id: hypothesis:lm-jev-next-call-suggestion
mint_id: 9b0245ac9def43459720ff0f9b127878
type: hypothesis
parents:
  - idea:lm-jev-mcp-sandwich
  - goal:g14
next_edges: []
ceiling: $1 OpenRouter + $0.30 TypeSafe; $0 compute; no engine file, no hook, no MCP server; file scope = .agi/context/local-maxxing/typesafe/{next_call.py, next_call.jsonl, next_call.md, json_cache/} + the kid experiment node + this node.
edited_by: thought-master
falsifier: top-1 < 0.55, or no T with precision >= 0.90 at >= 25% retention, or > $0.003 per decision -- then a suggestion layer would ADD a confirm step to most calls instead of removing calls, and the sandwich waits for a better model or a smaller roster.
scaffold_hash: bc33b7e7b936b624
season: 2
testable_claim: On 200 held-out decision points sampled from kid transcripts on this box (each = the transcript prefix up to a tool call, truncated to <= 24k tokens, plus the roster of tools available to that kid), one jev-1.13.0 request with noul is-a-tool-call-needed + choice over the roster (+ choice over the top-5 argument shapes when the roster tool has a closed set) reaches (1) top-1 agreement >= 0.70 with the call actually made, (2) precision >= 0.90 on the subset where confidence >= T for some T that retains >= 40% of decisions (the auto-dispatch band), (3) median added latency <= 300 ms (the live transcript view budget), (4) <= $0.001 per decision on billed input tokens.
tests: ONE pi parent, ONE kid, API-only, cap $1 OpenRouter + $0.30 TypeSafe ledger; decision points mined from .agi/sessions/**/output.log (1,943 files) with a logged seed, held-out by session; every jev response cached as json; rows to .agi/context/local-maxxing/typesafe/next_call.jsonl, sweep table precision/retention vs T to next_call.md; parent re-probes one row against the raw transcript bytes. Blocked on SM.103 like its sibling; no UI, no MCP wrapper, no hook until the numbers clear the bar.
title: "The jev-MCP sandwich post-layer, measured before any UI: a jev choice over the tool roster from the pre-call context reproduces the next tool call kids actually made at >= 0.70 top-1 on replayed transcripts, at < $0.001 per decision"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-next-call-suggestion

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
