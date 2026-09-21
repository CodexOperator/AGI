---
id: hypothesis:a00-db12df62-1859fd
mint_id: 05dada24dc6049a9a5ed0c86d1c69b60
type: hypothesis
parents:
  - goal:g9.7
confidence: 0.75
edited_by: season.py
scaffold_hash: 6f73e1deaf8d0657
season: 1
tags:
  - g9.7-execution
  - unified-renderer
  - shared-read-path
testable_claim: A single NodeFrameStream of (node, depth, level, flag) frames sorted by one ordering policy transduces into both the ASCII viewport (g9.4) and the markdown spawn context with no forked traversal, so one render change reaches both outputs in the same commit.
thought_session: season
title: "NodeFrameStream: one shared traversal transduced into both the terminal viewport and the spawn context"
verdict: pending
---

# hypothesis:a00-db12df62-1859fd

## Hypothesis

**Claim.** A single `NodeFrameStream` — g13's unified read-path exposing the graph as a
parameterized iterator of `(node, depth, level, flag)` frames, sorted by a single
ordering policy — can be transduced into both the ASCII terminal viewport (g9.4)
and the markdown context injection blob without forking the traversal. One
frame sequence serves both formatters; each formatter only chooses layout and
renders each frame once.

**What would prove it.**

1. A prototype `NodeFrameStream` exists that, given a zoom level, emits a
deterministic sequence of frames. Two downstream formatters (one writing
terminal-ASCII, one writing markdown-context) consume the same stream and
produce structurally identical content — same nodes, same depth markers, same
truncation boundary at that level.

2. Changing the frame stream — adding a flag field, changing sort order, or
raising the level cap — propagates to both outputs identically after recompile.
No file or code path is edited in only one output.

3. The count of frames emitted by the stream equals the count of lines or blocks
in both outputs. Neither formatter filters by criteria the stream did not already
apply.

4. A human tuning the viewport for readability (e.g. adjusting level cap from 3
→ 4) can verify the spawn context changed by the same amount in the same run,
with no second edit.

**What would disprove it.**

- The outputs disagree on node count, ordering, or truncation after both consume
the same frame stream (the transducers differ in which frames they skip or how
they order siblings).
- Stream changes require touching two output formatters independently (the
shared abstraction did not actually share the decision).
- The viewport's layout logic needs topology data the stream does not expose,
forcing an extra traversal (the single-pass claim fails).
- A human can push a change to the viewport and it appears, without the context
changing in lockstep (two renderers, not one).

**Scope.** Pure architecture node — no build code needed yet. This hypothesis
defines the contract the `NodeFrameStream` must satisfy, which g13's read-half
eventual implementation must reify.

## Tags

- g9.7-execution
- unified-renderer
- shared-read-path

## Notes

- Parent: goal:g9.7
- Blocked on: g13's read-half existing (per goal:g9.7 dependencies)
- This hypothesis is falsifiable via a prototype before g13 is complete — the
frame stream abstraction can be built and tested independently of the g13
storage layer.



## Agent Notes
Hypothesis: NodeFrameStream as shared traversal for viewport + context, proven/disprovable by single-pass fidelity and lockstep change propagation

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-f3acb772 review of kid a00-db12df62's v1. The kid's claim is accepted as-is: a
falsifiable hypothesis that operationalizes goal:g9.7's own falsifier (one render, two
readers) and correctly names g13 as the dependency it is blocked on. Not demoted — it makes
no proved/disproved claim, so the evidence gate has nothing to police; it is the first
hypothesis on this goal's chain.

This version adds the two frontmatter fields the [hypothesis] schema requires but the
scaffold did not seed: `title` and `testable_claim`, extracted verbatim-in-substance from
the body claim (not invented). The kid was briefed "leave frontmatter alone", and `cli.py
done` only writes verdict/confidence/evidence_runs — so a scaffolded hypothesis ships
without its two required fields unless a reviewer backfills them. Also lifted the body's
"## Tags" into `tags:` frontmatter to match corpus convention (89/122 hypotheses carry
title). Body is otherwise the kid's, untouched.

Kid-reported struggle worth a reader: it ran the repo test suite on a pure-architecture
node (no code changed) and the suite timed out at 60s before reaching the assertion
count — a no-code-change hypothesis should not be paying for a full suite run, and the
default timeout is too short for it.
<!-- THOUGHT:END -->