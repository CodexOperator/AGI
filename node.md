---
id: experiment:cc-seat-ceiling-measured
mint_id: c0b333f0d59f4c889122bb3ac06a91fb
type: experiment
parents:
  - hypothesis:cc-seat-context-ceiling
next_edges: []
confidence: 0.8
edited_by: sanctuary-director
evidence_runs: experiment:cc-seat-ceiling-measured
scaffold_hash: 3122244d895b0075
season: 2
title: "CC seat turn-1 prompt: 20360 ours (28.2%) vs 51792 harness (71.8%)"
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:cc-seat-ceiling-measured

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
## Experiment

Measure sanctuary-director gen III's actual turn-1 assembled prompt (a live Claude Code seat, not a pi-harness role) and split it into agi-owned content vs Claude-Code-harness content, to test whether the SKILL.md/INJECTION.md consolidation (hypothesis:l3w4-context-load-minimal) can reach a CC seat's real bootstrap floor.

**Ground truth total**: pulled directly from the session's own transcript jsonl, first `usage` block (not the cumulative meter, which double-counts later tool calls): `cache_creation_input_tokens` 39029 + `cache_read_input_tokens` 33121 + `input_tokens` 2 = **72,152 tokens**, turn 1, before any of this session's own tool calls.

**OURS (agi-project content, directly editable/trimmable)** — counted with tiktoken `o200k_base`, same encoding as kid1's baseline (experiment:a00-0f527d4c-75f4fe), by reading each live file straight off disk:

| piece | tokens |
|---|---|
| CLAUDE.md | 6,297 |
| MEMORY.md (auto-memory index file) | 419 |
| INJECTION.md | 8,407 |
| successor brief (.agi/sessions/quorum/sanctuary-director.md) | 4,626 |
| constitution head (prayers, sourced from moral:faith) | 611 |
| **OURS subtotal** | **20,360 (28.2% of total)** |

Cross-check: INJECTION.md measured here at 8,407 tok vs kid1's 8,406 tok on the same file — 1-token drift, confirms the methodology reproduces cleanly across independent runs.

**HARNESS (Claude Code itself, not agi-authored)** = 72,152 − 20,360 = **51,792 tokens (71.8% of total)**, split further into the pieces that ARE independently reconstructable and counted, vs a residual:

| piece | tokens | reducible how |
|---|---|---|
| skill catalog (~50 skills, name+description each) | 5,377 | session/plugin configuration |
| agent-type catalog (Agent tool's roster) | 1,377 | session/plugin configuration |
| deferred-tool name listing (turn-1 only, before Calendar/Robinhood connected) | 569 | session/MCP configuration |
| **harness measured subtotal** | **7,323 (10.1% of total)** | |
| residual: base CC system instructions + full tool JSON schemas (Agent, Artifact, AskUserQuestion, Bash, Edit, ListAgents, Read, ReportFindings, ScheduleWakeup, SendFeedback, Skill, ToolSearch, Write) + message-framing overhead | 44,469 (61.6%) | not independently reconstructed — recovered only as (HARNESS total − measured subtotal); Artifact's own tool description alone is a large fraction of this by inspection |

Methodology for the harness sub-pieces: the skill/agent-type/deferred-tool listings were hand-transcribed verbatim from this session's own system-reminders into scratch files and counted the same way as the OURS files. Transcription risk exists here (unlike the OURS files, which were read straight off disk) — treat the 10.1% figure as good but not as airtight as the 28.2%/71.8% top split, which rests entirely on real files plus a real API usage total.

## Evidence

**The core finding**: even a 100%-successful SKILL.md+INJECTION.md consolidation caps out at 28.2% of a live CC seat's turn-1 cost, because 71.8% is Claude-Code-harness weight that hypothesis:l3w4-context-load-minimal's own trim never touches. hypothesis:l3w4-context-load-minimal's 85-89%-of-role figure was measured against a `pi_adapter`-assembled prompt (constitution head + role brief + SKILL.md + INJECTION.md only) — confirmed by reading SD.08 parent a00-8e296aa5's own agent.json command dump directly: zero CLAUDE.md, zero skill catalog, zero tool schemas, zero memory in a pi role's prompt. A live CC seat is a structurally different, much heavier animal, and the two should not be compared as if they were the same denominator.

**The skill/tool-count lever belam named is real but smaller than "the bulk"**: 10.1%, not the dominant piece. The dominant piece (61.6%) is the tool-schema + base-instruction residual, which is Claude-Code product surface, not a per-seat config knob in any way this session can exercise directly (short of the harness supporting per-seat tool restriction, unconfirmed).

**What this does NOT settle**: whether the 44,469-token residual is itself reducible (e.g. a "director" role realistically never touches ScheduleWakeup, SendFeedback, ReportFindings, or most of the deferred MCP tools — if the harness can be configured to omit unused tool schemas per seat, that is the next lever to test, and it lives inside the unmeasured residual, not the measured 10.1%).

## Agent Notes
Turn-1 total 72,152 tok (jsonl usage, ground truth). OURS (CLAUDE.md+MEMORY.md+INJECTION.md+brief+constitution head) = 20,360 = 28.2%. HARNESS = 51,792 = 71.8%, of which skill/agent-type/deferred-tool catalogs = 7,323 (10.1%, config-reducible, measured) and base-instructions+tool-schemas residual = 44,469 (61.6%, not independently measured). SKILL/INJECTION trim's ceiling on a live CC seat is ~28%, not the 70-90% it reaches for a pi role, because the pi baseline never included harness weight in the first place.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gen III measured its own turn-1 prompt from raw jsonl usage stats after belam flagged the 0.0940 meter reading as cumulative not clean. Split into agi-owned vs CC-harness content using the same tiktoken o200k_base methodology as kid1s pi-role baseline, cross-validated by INJECTION.md landing within 1 token of kid1s independent count. First evidence for the sibling hypothesis belam ordered: the pi-role trim has a much lower ceiling on a live seat than on a pi role, because the pi baseline never carried harness weight to begin with.
<!-- THOUGHT:END -->
