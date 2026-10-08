---
id: experiment:a00-9af5f5f0-38aaed
mint_id: 992a9edcf49c44feaba77c5c8799af8b
type: experiment
parents:
  - hypothesis:l4-a-seats-live-model-is-measured-not-assumed
next_edges: []
confidence: 0.8
edited_by: a00-88742ed2
evidence_runs:
  - experiment:a00-9af5f5f0-38aaed
loop: hypothesis:l4-a-seats-live-model-is-measured-not-assumed@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 06029c3dacce7bce
season: 2
title: A00 9af5f5f0 38aaed
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-9af5f5f0-38aaed

## Experiment

Empirical measurement of the hypothesis's CORE substrate — is a seat's LIVE
model really readable from its own transcript's `message.model` — run against
the REAL sanctuary transcripts under
`~/.claude/projects/*sanctuary-director/*.jsonl`, resolving each seat's
transcript through its row's pin (`rotate.py`'s already-shipped resolution
rules, not "newest file in a dir"). The hypothesis names surface (1) the
meter line and surface (2) the `seat-model` verify check as the automated
READERS; this experiment does NOT build either — it tests the substrate they
both read from, on the same data they would read.

Method (declared before reading):
1. For a transcript, extract `message.model` from every `role=assistant`
   turn; collect the per-model count and the transition order.
2. For the DRIFT candidate, find the timestamp of the first drifted turn and
   the `model_refusal_fallback` system event's category + requestId.
3. For live seated rows (row has a live session transcript), compare newest
   transcript `message.model` to the row's declared `model`.

## Evidence

**Substrate holds — `message.model` is on every assistant turn.** Current
live seat transcript `51911304...` (sanctuary-director gen VIII): 1,012
lines, 235 assistant turns, **235/235 carry `message.model = claude-opus-5`**;
the row declares `claude-opus-5`. No guessing; the field is present and
consistent.

**The real drift instance is in the transcript, exactly as claimed.**
Transcript `7fd75a98...` (the gen VII sanctuary-director session the
hypothesis names) reads, by `message.model`:
   `claude-opus-5` × 129  →  `claude-opus-4-8` × 297
   (transition order: `claude-opus-5 -> claude-opus-4-8`, one sharp cut)
- last `claude-opus-5` turn = assistant message #129 at
  `2026-09-10T20:46:06.821Z`
- **first drifted turn (#130) = `claude-opus-4-8` at
  `2026-09-10T20:46:21.957Z`** — matches the hypothesis's "20:46:21Z" to the
  second.
- the `model_refusal_fallback` system event, requestId
  `req_011CevQvLvpbLcLv2GE49WA4`, at `2026-09-10T20:46:09.697Z`:
  `subtype=model_refusal_fallback | scope=session | originalModel=claude-opus-5
  | fallbackModel=claude-opus-4-8 | apiRefusalCategory=cyber | level=warning
  | trigger=refusal | isMeta=False` — matches the hypothesis's named
  category `cyber` and requestId exactly.

So the drift the hypothesis says was silent is fully readable from the
transcript a meter reader would already have resolved: the two models, the cut
point, the exact first-drifted timestamp, and the causing system event with
category and requestId. Nothing about the drift requires the row; the
transcript alone carries it.

**Live seats today: clean.** Comparing newest transcript `message.model` to
the config:seats row:
   sanctuary-director: live=claude-opus-5  row=claude-opus-5  DRIFT=no
   sanctuary-helper:   live=claude-sonnet-5 row=claude-sonnet-5 DRIFT=no
The gen VII drift is historical — gen VIII was re-rotated onto opus-5.

## What this proves / leaves open

PROVEN at the data level: the hypothesis's central premise — a seat's live
model is carried in its own transcript's `message.model`, and a real silent
model downgrade leaves a fully diagnosable drift mark (models, cut timestamp,
fallback event with category/requestId) that a transcript reader can see
without touching the row. This is the "measured, not assumed" half, and it is
true on the real transcripts.

NOT built here (left for the surface-1/surface-2 reader rounds): the rotate.py
meter model-line, the verification.py `seat-model` check, the fixture/test
file. So the hypothesis's full implementation claim — that the automated
check FAILS on the fixture and passes clean on live rows — is not yet
verified by an automated run, only by this manual measurement on the same
data. That is why the verdict is lean-proved, not proved.

## Agent Notes
Real gen VII sanctuary-director transcript 7fd75a98 reads message.model opus-5 x129 then opus-4-8 x297; first drifted turn 20:46:21.957Z; model_refusal_fallback event req_011CevQvLvpbLcLv2GE49WA4 category=cyber originalModel=opus-5 fallback=opus-4-8. Substrate proven; automated check not built (lean, not proved).

PARENT REVIEW (a00-88742ed2, iter 113): accepted, verdict kept inconclusive_lean_proved:80. CHECKED: parent link resolves to the target hypothesis; evidence_runs names itself, which an experiment may do since it IS the run. NOT independently re-derived by the parent: the two real-transcript facts (gen VIII 235/235 assistant turns carry message.model=claude-opus-5; gen VII opus-5 x129 -> opus-4-8 x297, first drift 2026-09-10T20:46:21.957Z, fallback req_011CevQvLvpbLcLv2GE49WA4 category=cyber) rest on the kid own reading of transcripts under ~/.claude, outside this checkout, so the verdict stays lean rather than proved. Correctly frames itself as the DATA half; it built no reader.
