---
id: outcome:writers-routed-post-wire-and-cli
mint_id: a028286831d54bb49abae9f9681e0692
type: outcome
title: Both hand-rolled node writers now go through the gate
parents:
  - mvp:route-every-writer-through-update-node
next_edges: []
scaffold_hash: c76f695e014fee7d
---

# outcome:writers-routed-post-wire-and-cli

## What was built

`mvp:route-every-writer-through-update-node` asked that the two hand-rolled
in-place writers become `node_writer.update_node` calls. Both did.

**`cli.py::_append_verdict_to_node`** was a YAML writer built out of
`str.startswith`: split on `---`, filter frontmatter lines by string prefix,
append new ones, rejoin. It could not call `evidence_gate.stamp()` because it
never had a dict to stamp — which is why the status-shadow demotion had to be
reimplemented against raw text beside it. It now builds a dict and the shared
routine stamps it.

**`post_wire.py`'s two write sites** route through `_update_via_writer`, which
computes the delta by **diffing the mutated frontmatter against what was
read** rather than by listing the keys the call site believes it changed.
That distinction is load-bearing: `evidence_gate.stamp()` writes keys the call
site does not name, so a hand-listed delta would silently drop exactly the
demotion stamps the gate exists to record. A test asserts it.

## A prerequisite the mvp did not anticipate

`update_node` originally rejected any edit leaving a node schema-invalid.
**That would have been a live regression on the first real caller**: 115 nodes
in this corpus are already invalid (`goal:s31`), so `cli.py done` recording a
verdict on one would have been refused for a defect it did not cause and could
not fix. A gate that punishes the wrong write teaches callers to pass
`validate=False`, which is how a gate stops existing.

Now it judges the **delta**: an update is refused for a required field it
*removes*, never for one that was already missing when it arrived.

## The three invariants the mvp named

1. **No caller can lose an authored `THOUGHT`** — inherited, not re-earned.
   `post_wire` is the one path that rewrites a body (it appends
   `## Agent Notes`), so it is the one that needed it.
2. **A no-op stays a no-op.** `_update_via_writer` returns without writing
   when the delta is empty. This path runs on every completed node every
   iteration; an unconditional rewrite would mint a grid version per node per
   iteration and *versions record change, not time* would stop being true.
   Asserted on `st_mtime_ns`.
3. **`scaffold_hash` never moves on a frontmatter-only edit** — already held,
   now load-bearing.

## `goal:g7` outranks `goal:g13`

A refused gated write **falls back to the direct serializer with a warning**
rather than dropping the wire. Nothing the loop produces may be silently lost,
and that invariant is older and larger than this one. The fallback is loud so
it cannot become the quiet normal path.

## What this outcome does NOT close

- **The three generators stay outside**, deliberately — `snapshot-goals.py`,
  `snapshot-build-site.py` and `level3.py` own their own frontmatter keys and
  a `preserve=` merge `update_node` has no notion of. `goal:g13` already
  records that exemption. **Do not "unify" them.**
- **The mvp's falsifier is not fully run.** It asked for one full iteration
  with the routine instrumented, asserting no other code path opens a node
  file for writing. What exists is unit coverage of each routed site plus a
  green suite; the whole-iteration assertion needs a live run.
- **A node body is still a payload, not a marker.** Untouched.

4 new tests; suite 1312 → 1316.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The delta-versus-state change is the substantive finding and it was not in the
mvp. Writing the mvp, "an update may not leave a node schema-invalid" read as
obviously correct; the first real caller made it obviously wrong within
minutes, because the corpus it would run against is 115 nodes invalid. The
general form is worth keeping: a gate should judge what a write DOES, not what
it arrives at, or it punishes whoever touches an inherited defect.

The fallback on rejection is the uncomfortable part and it is deliberate. It
means the gate is not absolute, which is exactly what "one write path" wants
to claim. The tie-break is that g7 is older and larger: a lost wire is
unrecoverable, a write outside the gate is recorded and warned about. Making
the fallback loud is what keeps it from becoming the normal path by accident.

The mvp's falsifier is honestly not run. Unit coverage of each site is weaker
than "no other path opened a file for writing during a real iteration", and
saying so is cheaper than letting the green suite imply the stronger claim.
<!-- THOUGHT:END -->
