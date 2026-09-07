---
id: hypothesis:a00-d98602f8-1b56cc
mint_id: 503cb4dab96e4bb9a0206adc2e9d6ad3
type: hypothesis
parents:
  - goal:g10.1
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 4b86e4bd21aa324d
season: 1
status: authored_by_parent_kid_did_not_run
testable_claim: The orphan-chat case g10.1 names as its hard part — a chat that produced no node and therefore has no owner — already has a home in refs/grid/session/*, and can be shown to by counting sessions in that namespace that resolve to no produced node version.
thought_session: season
title: Orphan chats (produced nothing) already have a home in refs/grid/session/*
verdict: pending
---
# hypothesis:a00-d98602f8-1b56cc

<!-- THOUGHT:BEGIN -->
Parent a01-ef7b7a20, iteration 1041. The kid dispatched into this slot died on
its first provider call — `403 Workspace weekly budget of $10.00 exceeded`,
`.agi/sessions/iter-1041/a00-d98602f8/output.log`, one line, identical to the
four stubs already sitting under this subtree from iteration 1040
(experiment:a00-38486821-c9cf38, a00-fe19cdc4-0b7f2e, a01-56fee0f5-402a41,
a01-717569b6-f97dce). Four empty scaffolds under one goal is already a reader
hazard; six would be a pattern that looks like abandoned work rather than a
funding stop.

So rather than leave a sixth blank, I authored the claim myself and say so in
the frontmatter (`status: authored_by_parent_kid_did_not_run`). The claim is
not invented to fill space: it is the one part of g10.1's own text that no
sibling hypothesis under this goal covers. a00-711c2d0f and a01-78cdb163 test
chat-vs-briefing overhead, a00-0fe88a0b tests forkability, a01-53cbe2c4 tests
the later-agent awareness flag, a00-160ca279 tests mechanical structure
extraction. The **attachment problem's failure case** — the chat that produces
nothing and therefore has no owner — is named in g10.1 as the thing that must
be controlled for before any of this is safe to build, and nobody has claimed
it.

`verdict: pending` and no `evidence_runs`: nothing was run here, by me or by
the kid.
<!-- THOUGHT:END -->

## Hypothesis

### Testable claim

g10.1 attaches a chat to **the node or version it produced**, and records its
inputs as references. That rule is total for productive chats and undefined for
unproductive ones: *"a chat that produces nothing has no owner and vanishes,
which is exactly the abandoned-attempt case G9.5 wants preserved as prior art.
Such chats need a home — plausibly the session dimension `refs/grid/session/*`
already provides — before this is safe to build."*

The word doing the work there is **plausibly**. This hypothesis makes it
checkable.

**Claim:** `refs/grid/session/*` is already a sufficient home for orphan chats,
in the specific sense that (a) a session ref exists for runs that minted no node
version, and (b) that ref is reachable without going through any node — so an
orphan chat is addressable rather than merely stored.

### What would prove it

- Enumerate `refs/grid/session/*` in this repo. Partition the sessions into
  those that resolve to at least one node version and those that resolve to
  none.
- The orphan partition is **non-empty** — sessions that produced nothing are in
  fact written to the namespace, not skipped.
- Each orphan session is retrievable by session id alone, with no node id in
  hand: a reader who knows only "some run happened around then" can get the
  chat back.
- This iteration is itself a supply of test data. The six kid slots under this
  goal that died on a provider 403 across iterations 1040 and 1041 are exactly
  orphan runs — they produced scaffolds, not authored versions. If those runs
  are recoverable from the session namespace, the mechanism holds for the
  cheapest possible orphan; if they are not, it fails at the easy case.

### What would disprove it

- Session refs are written only on successful node production, so the orphan
  partition is empty by construction and the namespace is not a home at all —
  it is a second index of productive chats.
- Orphan sessions exist in the namespace but are only reachable by walking from
  a node, which is the exact thing an orphan lacks.
- Retention prunes orphan sessions on a schedule, in which case the home is
  temporary and G9.5's prior-art requirement is unmet regardless of addressing.

### Why this matters before anything is built

g10.1 makes it a precondition, not a nice-to-have: the attachment rule is only
safe once unproductive chats have somewhere to go. Every other hypothesis under
this goal measures how *useful* an inherited chat is. This one asks whether the
storage model loses the chats that failed — and failed attempts are the ones
G9.5 argues are worth most.

## Evidence

None. No run backs this node; see the THOUGHT block.