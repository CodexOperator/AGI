---
confidence: 1.0
goal_id: G2.7
goal_kind: subgoal
heading_level: 3
id: "goal:g2.7"
mint_id: 9d60959979ff4b2397e6722488c609d7
origin: goals-doc
parents:
  - goal:g2
seeds: []
status: horizon
tags:
  - goal
  - subgoal
title: "G2.7: The finest zoom is the chat that produced the version"
type: goal
---

**Zoom does not stop at the node.** Coarse levels are organised by tags and
addresses (**G2.5**, **G2.6**); the finer levels are organised by **mint id and
the grid**. Zooming into a node reveals its version history; zooming into a
version reveals **the chat that produced it**.

That last hop is the one nothing currently supports. Each grid commit for a node
is a version, and each version was produced by some session — but the two are
not linked, so the reasoning behind a change is only recoverable by memory or by
luck. The engine must cross-link them **automatically and seamlessly**: every
node version's grid commit carries the identity of the chat that produced it,
and every chat resolves to the commits it caused.

What follows from doing it properly:
- **Grid commit messages carry the parent nodes by mint id.** A renderer can
  then draw the hypergraph across *both* substrates — disk nodes and grid
  commits — without a separate edge store, because the edges are already written
  into the history.
- **The base graph gets flatter.** Version history stops being modelled as extra
  nodes on disk and becomes depth you zoom into. That is the direct reason the
  separate-node-per-version convention is retired (**G6.3**).
- **Provenance answers the question that matters:** not "what changed in this
  file" but "which conversation produced this line, and what was true when it
  was said".

Depends on G2.5 for the mint id (an address would break the link the moment a
node is retagged) and on **G10.1**, which already argues chats are nodes.
Unbuilt; recorded so the id and grid work is designed to make it possible rather
than to need undoing.

**Where the transcripts already are, and why that is a subsidy worth naming
(added 2026-09-01).** Under the pi harness the logs are being written for us:
pi keeps a full JSONL transcript per session at
`~/.pi/agent/sessions/<cwd-slug>/<timestamp>_<uuid>.jsonl`. **That is real
infrastructure the project is getting for free and has not had to build** — no
collector, no storage, no retention policy. What is missing is only the *link*:
nothing records which transcript produced which node, so the mapping is
recoverable by mtime comparison and luck. Confirmed on 2026-09-01 —
`thought_session:` appears in **zero** code paths and **zero** nodes, and
`pi_adapter.build_command` never learns the session path because pi chooses it
after launch. Neither direction of the link exists.

**Two directions, and the choice is not obvious.** Either stamp
`thought_session:` into the node's frontmatter (queryable, versioned with the
node, but a write-path change that `goal:g13` should own), or put the session
reference in the **grid commit message** for that version (no schema change,
naturally per-version, but only reachable through `grid.py log`). The first
makes the link data; the second makes it provenance. Both are cheap; picking
one without deciding which the hypergraph wants to traverse is how the wrong
one gets built.

**Leaving pi means building this, and that cost is easy to miss** — see
`goal:g4.3` clause 4. A raw-API harness gets one thing pi does not give us:
OpenRouter accepts a caller-chosen `session_id` in the request body, so the
session id can simply **be the node's mint id** and the link exists by
construction rather than by bookkeeping. What it loses is the transcript
itself, which then has to be collected — a webhook we host, or one of the
OpenRouter-compatible observability platforms already available at no cost
(Sentry, New Relic). Until that is built, **pi keeping the logs is a reason not
to leave it casually.**
