---
confidence: 1.0
goal_id: G2.10
goal_kind: subgoal
heading_level: 3
id: "goal:g2.10"
mint_id: 167f314e0512428db94739aaba20ed4d
order: 18
origin: goals-doc
parents:
  - goal:g2
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G2.10: A build node cannot hold a thought — the scan wipes its body"
type: goal
---

🔴 **`level3.py` regenerates a build node's entire body on every run. Anything
a model wrote there is destroyed on the next loop iteration.**

Measured 2026-08-27, by writing a value and re-running the scan:

| probe | result |
|---|---|
| prose added to a build node body | **wiped** |
| `why: TODO(model)` filled in with a real value | **wiped** |

And the corpus reads exactly as that predicts:

    why/perf/security fields across 190 build nodes:  8,034
    still reading TODO(model):                        8,034
    ever filled:                                          0

**Zero of 8,034.** That is not neglect. `[build].md` says the contract block
is harness-owned and "a model may fill `why`/`perf`/`security`" — the schema
states a permission the code revokes on the next scan. Any agent that spent a
turn filling one did work that was deleted before it could be read.

## Why this is a G2 goal and not a bug report

**G6.8 argues build nodes belong in the graph precisely because they hold
thought:** *"A code node ties cleanly to thought: it can spawn a hypothesis
about itself, an experiment against itself, or just an idea. That
bidirectionality is what makes it worth being a node rather than a record."*
Half of that is currently false. A build node can be *cited* by a thought; it
cannot *contain* one. Today it is exactly the "record" G6.8 says it is more
than — 190 nodes of mechanically-derived shape with a permanently empty
`why`.

The derived half should keep being derived — that is what makes it trustworthy
and what `stale_contracts` polices. The authored half has to survive. Concretely:
`write_frontmatter` already merges frontmatter with `preserve=`; the body needs
the same treatment — regenerate the mechanical `how`, carry over `why`/`perf`/
`security` and any prose outside the markers.

## This is also why the `@v2` nodes exist, and why they cannot be collapsed yet

Five nodes carry `origin: build-version` and an `@v2` id
(`build:bin-grid@v2` and four siblings). They hold **7,000–13,000 characters
of real reasoning each** — why `sanitize()` became injective, what
`migrate-refs` is for — and they survive **only because `level3.py` does not
own their origin and therefore never rewrites them.**

CLAUDE.md's rule is right in general: *a version is a grid commit, not a
second node file.* But the `@v2` file is not redundancy here — **it is the
only durable place a build artifact's reasoning can currently live.**
Verified before proposing removal: v1 and v2 payloads are byte-identical to
the engine for all five, so no bytes would be lost — but ~47,000 characters of
prose would be, with nowhere to put it, because the v1 node's body is wiped on
the next scan.

**So the sequence is forced: fix the wipe, migrate the five bodies into their
v1 nodes, then retire the `@v2` convention.** Collapsing them first would
delete prior art to satisfy a naming rule, which is the trade this project
has repeatedly refused. Pairs with **G6.8**, **G6.3** and **G7**.

Falsifier: fill one `why:` on one build node, run `driver.sh --smoke`, and
read it back.
