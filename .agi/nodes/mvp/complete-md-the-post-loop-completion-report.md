---
id: mvp:complete-md-the-post-loop-completion-report
mint_id: d999aebe622e4d4f9ecbce439460ad7a
type: mvp
parents:
  - hypothesis:a-loop-that-does-not-report-its-own-completion-repeats-its-gaps
next_edges: []
confidence: 0.8
edited_by: season.py
scaffold_hash: a544d6be1303f546
season: 1
status: open
tags:
  - mvp
thought_session: season
title: Complete md the post loop completion report
---
# mvp:complete-md-the-post-loop-completion-report

## MVP

What does this script/module do? Show the code or describe the implementation.

## Inputs

What does it take?

## Outputs

What does it produce?

## Agent Notes
**The minimum `COMPLETE.md` must satisfy.**

- **Location and shape:** repo root, `COMPLETE.md`, a `build` node with
  `payload_ref: COMPLETE.md`, versioned by the grid like `HANDOFF.md`.
- **Append-only across loops.** One section per completed loop, newest first,
  each headed with the loop id and the date range. Unlike `HANDOFF.md` it is
  never replaced — that is the entire point of having a second file.
- **Six required sections**, in `goal:g1.13`'s order: what ran; the scoreboard;
  per-active-goal progress; goals actually closed plus unsubstantiated
  completions; completion-failure categories for everything that did not close;
  what was minted in response.
- **Every per-goal claim is grounded** in a commit, a node diff or a parent
  report — never recollection. A claim that cannot be grounded is written as
  ungrounded.
- **A banked decision is a completion failure** and is categorised as one.
- **Machine-readable enough to train on:** the failure categories are a fixed
  closed set, so a classifier can later be scored against a director's labels
  (`goal:g14`).

**Falsifier:** a second loop's `COMPLETE.md` is produced with the same sections
and the carried-hazard list shrinks rather than repeats. If the second report is
a copy of the first with a new date, the format is decoration.

**Not in scope here:** generating the report mechanically. This mvp specifies the
artifact; `goal:g14` owns replacing the director with a small model that emits it.

CORRECTION 2026-09-05, owner: strike the append-only requirement above. COMPLETE.md is replaced whole by default and appended only on owner request, exactly like HANDOFF.md. Everything else in this mvp stands -- the six sections, the closed failure-category set, grounded claims, and a banked decision counting as a completion failure.

FORMAT UPDATE 2026-09-05: SEVEN required sections, not six. Section 6 is findings that are not failures, optional and omitted when empty; what was minted becomes section 7. The falsifier is unchanged.