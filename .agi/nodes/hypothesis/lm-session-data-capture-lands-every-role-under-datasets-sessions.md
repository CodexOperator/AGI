---
id: hypothesis:lm-session-data-capture-lands-every-role-under-datasets-sessions
mint_id: b258aad24516421da06e6d3972b71faa
type: hypothesis
parents:
  - goal:g14.10.2
next_edges: []
confidence: 0.5
edited_by: belam
scaffold_hash: b894479c0546b80c
season: 2
tags:
  - local-maxxing
  - datasets
  - sessions
  - capture
testable_claim: "For every role that runs a session on this box (pi parents/kids already land under datasets/trajectories/; claude-code roles -- masters, directors, the Prime -- do not yet), a capture step lands each session's transcript under datasets/sessions/<role>/<session>/ through the one scrub (datasets/tools/scrub.py), pre-labelled with what the graph already knows per record: model, harness, provider, role, post, town, round id, verdict, mur residue class, spend, wall, box. Measured on >= 10 real claude-code sessions captured this way: 0 leak hits from the scrub, 100 pct of the graph-known label fields populated (never blank when the graph has the value), and one datasets/README.md row plus index entry added in the same merge. Depends on the claude-code capture hook (goal:g14.14.8, director-engine) existing first -- this hypothesis is mintable now but not dispatchable until that hook lands."
title: "G14.10.2 chunk 1 -- CAPTURE: every role session lands under datasets/sessions/<role>/<session>/ through the one scrub, pre-labelled from the graph -- blocked on goal:g14.14.8 (director-engine capture hook)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-session-data-capture-lands-every-role-under-datasets-sessions

## Hypothesis

**Claim:** for every role that runs a session on this box (pi parents/kids
already land under `datasets/trajectories/`; claude-code roles -- masters,
directors, the Prime -- do not yet), a capture step lands each session's
transcript under `datasets/sessions/<role>/<session>/` through the one
scrub (`datasets/tools/scrub.py`), pre-labelled with what the graph already
knows per record: model, harness, provider, role, post, town, round id,
verdict, mur residue class, spend, wall, box.

**Measured** on >= 10 real claude-code sessions captured this way: 0 leak
hits from the scrub, 100 pct of the graph-known label fields populated
(never blank when the graph has the value), and one `datasets/README.md`
row plus index entry added in the same merge.

**Falsifier:** any leak hit on the tested sessions, or a graph-known field
left blank on a record where the graph actually has the value.

**Blocked on:** the claude-code capture hook (`goal:g14.14.8`,
director-engine) -- the mechanism that copies a harness session dir into
the landing path does not exist yet. This hypothesis is mintable now, per
`goal:g14.10.2`'s own "first chunk" instruction, but not dispatchable until
that hook lands.

**Not claimed here:** the jev classifier pass (chunk 2, a sibling
hypothesis) -- this chunk is capture + pre-labelling only, no new class
invented.

**Cost:** 0 USD for the capture mechanism itself; the dispatching parent
runs on `pi`/deepseek (cap $1) per the usual round shape, once dispatchable.
