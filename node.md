---
id: goal:g9.6
mint_id: 109544c597b047f78178c67f641721f0
type: goal
parents:
  - goal:g9
confidence: 1.0
edited_by: season.py
goal_id: G9.6
goal_kind: long-term
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
thought_session: season
title: "G9.6: A build node's description survives the scan; its body becomes the rendered payload"
---
**Under G9 — legibility: a human can see what the loop is doing — because
today the only readme a build node offers is a mechanically-derived contract,
and that is not what a human reads to learn what a file is for.**

## Two changes

- **`description:`** — a short authored field in a build node's frontmatter:
  a small, built-in readme that rides with the node. What it is for: a reader
  — human or agent — should be able to learn what a file is *for* without
  opening the file and without parsing a `BUILD-CONTRACT` block that states
  `how`, not why.
- **Body becomes a rendered view of the payload** — the actual content of the
  file the node owns, rendered rather than authored. Not a contract *about*
  the file; the file itself, as the node's body.

## Why this resolves a live contradiction

`bin/level3.py` regenerates a build node's entire body on every scan.
`goal:g2.10` measured the consequence directly: **8,034 `why`/`perf`/
`security` contract fields across 190 build nodes, all still `TODO(model)`,
0 ever filled** — because anything authored into a body is wiped by the next
scan. `goal:g2.11` responded by adding the `THOUGHT` block as the one
authored region that survives regeneration, keyed on the general rule
**`body` is state; `thought` is delta.**

That fix is now absorbing a second job it was not built for. This session
found `build:bin-grid`'s `THOUGHT` block has grown to roughly 2,000 words —
not because 2,000 words of per-version delta accumulated, but because
`goal:g6.8` records that it absorbed a migrated `@v2` node body: the five
`origin: build-version` nodes carried 7,000–13,000 characters of real
reasoning each, "with nowhere to put it," and `goal:g2.10`'s own record of
that migration shows exactly this — `build:bin-grid`'s body went from 13,113
to 26,399 characters and its `THOUGHT` region absorbed 13,284 characters in
the same move. That prose is durable reference material — what the file is
and why it exists — not a delta explaining how this version differs from the
last one. `THOUGHT`'s own convention says it is "rewritten from scratch each
time rather than appended to," and on build nodes practice has diverged from
that: the region is doing two incompatible jobs at once, permanent readme
prose and per-version delta, because it is the only authored region that
survives a scan.

**`description:` gives the durable readme its own home, so `THOUGHT` can go
back to being a delta.** That is this goal's real payoff, with the ~2,000-word
block on `build:bin-grid` and the 8,034/0 figure as the evidence that the
gap is not hypothetical — it is already being papered over by a region that
was designed for something else.

## The three regions, made explicit

| region | owner | lifetime |
|---|---|---|
| `description` | whoever authors the node | durable, short, survives every scan unless deliberately rewritten |
| body | `bin/level3.py` (harness) | derived, regenerated every scan — the payload, rendered |
| `THOUGHT` | whoever authored the version | per-version delta, rewritten from scratch each time (`goal:g2.11`) |

Same split as today's `BUILD-CONTRACT` / `THOUGHT` pair, with one region
added and one redefined: `description` takes over the durable-readme job
`THOUGHT` was never meant to hold, and body stops being a derived *contract
about* the payload and becomes the payload itself, rendered. `why`/`perf`/
`security` — the fields `goal:g2.10` fixed the carry-over for — need a new
home once `BUILD-CONTRACT` is no longer the body's organizing structure;
this goal does not resolve where they land, only that `description` is not
it, since those are per-field annotations, not a whole-node readme.

## Falsifier

A build node's `description` survives two consecutive `level3.py` runs, AND
its body matches the payload byte-for-byte after rendering. Today the first
half fails for any authored body content — `level3.py` overwrites the whole
body region unconditionally except for the marked `THOUGHT` block — and the
second half is not yet a defined operation at all: body currently holds a
derived contract, not a rendering of the payload.

## Measured facts (2026-08-29, do not re-measure without cause)

- 195 build nodes exist; 190 are written by the level-3 scan on each run.
- 799 nodes total.
- `level3.py` re-derives and rewrites build node bodies on every run; two
  consecutive runs currently leave an identical, stable diff (verified this
  session) — the regeneration is idempotent, which is what makes swapping its
  output from "contract" to "rendered payload" a change in *what* is derived,
  not a change in whether regeneration is safe to run repeatedly.

## Out of scope

**Where `why`/`perf`/`security` move once `BUILD-CONTRACT` is no longer the
body's shape** is not decided here — flagged above as an open question this
goal surfaces but does not close, so it does not get answered by default
while this goal is still at `horizon`.