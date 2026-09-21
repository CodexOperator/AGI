---
id: experiment:a00-c704d4b3-f08a68
mint_id: eefbf473427a4500ab0faca5e541b628
type: experiment
parents:
  - hypothesis:l3w4-context-load-minimal
next_edges: []
confidence: 0.75
edited_by: a00-8e296aa5
evidence_runs:
  - experiment:a00-c704d4b3-f08a68
loop: hypothesis:l3w4-context-load-minimal@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f6aa3259c9276847
season: 2
title: "\"Compact the INJECTION graph-stream in the generator: DEFAULT_FRAMES 200->90, -46% file / -33% real argv per role\""
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-c704d4b3-f08a68

## Experiment

SD.08 continuation of the INJECTION graph-stream slice (kid-3, experiment:a00-3fb60b07-2ca604, left open: "the INJECTION stream compaction itself, now the dominant lever — next kid"). The graph-viewport frame stream is **7187 of 8407 tok** (85% of the injected file — every role pays it EVERY turn). Trimming prose around it (kid-3 measured ~2%) is pointless; the lever is the stream itself.

**Change:** `extensions/agi/bin/inject.py` is THE generator (replaced render-context.py; hook and driver call it with no `--frames`, so `DEFAULT_FRAMES` governs production). Lowered `DEFAULT_FRAMES` 200 → 90. This is the correct single lever because (a) inject.py renders only `frames[0:cap]` — the file is ALREADY a truncated partial map (200 of 750 frames), so the map was never complete in always-injected form, and (b) deep navigation is a legitimately on-demand read (`viewport.py --anchor`, zoom) — carrying a deep tree statically is what the trim exists to stop. Deep-navigation knowledge is not lost; it is relocated to a pointer read, per the hypothesis's own owning principle. Touched ONLY inject.py + this node; did NOT hand-edit INJECTION.md, SKILL.md, or rotate.py.

Measurement-first, same method as every sibling (tiktoken o200k_base on `pi_adapter.build_command` argv via the existing `.agi/tmp/measure_realargv.py`):

| tier | before argv | after argv | cut |
|---|---|---|---|
| kid | 11612 | 7784 | **-32.9%** |
| parent | 11947 | 8154 | -31.7% |
| director | 11620 | 7770 | -33.1% |
| prime_director | 11705 | 7855 | -32.9% |

INJECTION.md file: 8407 → 4557 tok (**-46%**); the graph *stream* 7187 → 3337 (**-54%**), landing under the parent's ~3k stream target. Bytes 25675 → 14532.

## Evidence

```
DEFAULT_FRAMES 200 -> 90 in inject.py (only change)
pytest extensions/agi/tests/ -q  ->  2209 passed, 1 skipped (full suite green)
INJECTION.md total: 8407 -> 4557 tok (-46%); graph stream 7187 -> 3337 (-54%)
per-role argv (o200k): kid 11612->7784 (-32.9%) / parent 11947->8154 (-31.7%)
                        director 11620->7770 (-33.1%) / prime 11705->7855 (-32.9%)
## the graph still precedes nothing; briefing survives (tree heading stays < line 80,
INJECT_BUDGET test passes); map renders: roots + depth-3 subtree + verdicts intact
```

**HONEST SCOPE — does NOT reach 70-90% alone.** -33% per role is the largest *landed* single lever this hypothesis has shipped (rolslice's -37% was potential-only, unwired to a non-injected file; this one is on the real argv). But the stream trim alone is ~1/3, not 2/3+. Reaching the owner's range needs the OTHER complementary slices landing TOGETHER (move-ONE prayers-only head ~2400tok, per-role SKILL slice wired into a real loader, the ASCII state-card replacing the tree for handoff). This slice is the INJECTION half of that; it ships the structural restructure kid-3 named, on the dominant always-injected cost.

MUST-NOT-LOSE check: exact next command and kill procedure live in HANDOFF/successor briefs (unaffected); key-floor rule lives there too (not in INJECTION.md); attribution labels on the surviving quotes are on the constitution head (unaffected). Nothing on the must-not-lose list was in the trimmed graph-stream lines except node navigation, which remains for the non-truncated portion and is available on demand via anchor/zoom.

## Agent Notes
Landed the generator-side compaction of the dominant always-injected stream: inject.py DEFAULT_FRAMES 200→90. INJECTION 8407→4557 tok (-46%), graph stream 7187→3337 (-54%, under parent's ~3k target); real argv cut kid -32.9% / parent -31.7% / director -33.1% / prime -32.9% (tiktoken o200k, pi_adapter.build_command). Landed on the real argv, unlike rolslice (unwired). Full suite 2209 passed. Deliberate finding: the always-injected INJECTION was already a truncated partial map (200 of 750 frames), so it is not the complete navigator — deep nav belongs to on-demand anchor/zoom reads, which is what the trim is for. 33% is real but NOT 70-90% alone; the full owner range needs head trim + wired per-role slices + state-card handoff landing together.

## Agent Notes
Generator-side compaction of the dominant always-injected stream: inject.py DEFAULT_FRAMES 200->90. INJECTION.md 8407->4557 tok (-46%), graph stream 7187->3337 (-54%, under 3k target). Real per-role argv cut (tiktoken o200k via pi_adapter.build_command): kid -32.9%, parent -31.7%, director -33.1%, prime -32.9% — landed on the real argv, unlike rolslice (unwired). Full suite 2209 passed. 33% is the largest landed single lever but NOT 70-90% alone; full owner range needs head trim + wired per-role slices + state-card handoff landing together.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-8e296aa5), accepted. Verified directly: DEFAULT_FRAMES=90 in inject.py; full engine suite re-run by me, 2209 passed / 1 skipped. parents resolve; verdict format valid; evidence self-named (legitimate). This is the best slice of the round: the only lever LANDED on the real argv rather than measured against a file the harness does not inject (contrast rolslice). The honest scope statement (-33% per role, not 70-90% alone) is exactly right, and the finding that the injected map was ALWAYS a 200-of-750 truncated partial map reframes deep nav as on-demand by construction, not as a loss. One residual risk to flag for the next reader: 90 frames is a taste number, not a measured comprehension number — if orientation degrades, revisit the cap before assuming the mechanism is wrong.
<!-- THOUGHT:END -->
