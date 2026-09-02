---
id: verdict:the-write-half-has-a-floor
mint_id: 0a8c3fa7a587482a968a2a23362336cf
type: verdict
title: "An in-place edit now has one gated routine, and it cannot destroy an authored thought"
parents:
  - experiment:link-scan-and-the-thought-guarantee
next_edges: []
scaffold_hash: f54c63cf67a2cd67
verdict: proved
confidence: 0.93
evidence_runs:
  - experiment:link-scan-and-the-thought-guarantee
---

# verdict:the-write-half-has-a-floor

## Verdict

proved

## Evidence

`experiment:link-scan-and-the-thought-guarantee`:

- **905 nodes resolved, 0 broken, nothing edited.** 220 via `payload_ref`,
  685 defaulted, 0 declared.
- **Five adversarial writes could not destroy an authored `THOUGHT`.** Body
  replacement carries it; a new body's own thought wins and leaves exactly one
  block; a no-op reports `UNCHANGED` and does not touch `st_mtime_ns`; a
  missing node is refused without being created; an unparseable node is refused
  with its bytes intact.
- **No `type == goal` branch exists in the resolver** — `self` resolves like
  any other link.
- 16 new tests; suite 1279 → 1295. The type-branch claim is carried by an
  `ast` test, not a `grep` — a first attempt used `grep -c "type == goal"` and
  got 1, because the phrase is in the module docstring stating the invariant.
  A text search for a concept cannot tell prose from code.

## What is proved, at the level it holds

**`goal:g13`'s third operation — edit a node in place — now has a routine, and
that routine is safe to route edits through.** Before this, "edit the node in
place" was a convention in `CLAUDE.md` with nothing implementing it, so every
such edit bypassed the schema check and the authored-content guarantee. The
floor exists.

**The link layer's three semantics are the owner's answers, in code**: `self`
without a type branch, raise on a single read, sentinel plus `broken_links` on
a bulk scan. It generalises `payload_ref` rather than competing with it, which
the corpus scan shows by resolving 220 existing build nodes untouched.

## What is NOT proved — read this before citing it

- **The corpus is not migrated. `declared: 0`.** Nothing has opted in to
  `link_ref`, so "the graph uses the link layer" is false. 685 nodes resolve
  `self` by *default*, and the resolver reports that distinction precisely so
  this sentence stays checkable.
- **`update_node` has no production caller** beyond `write.set_link`. That it
  *can* carry every in-place edit is tested in isolation; that the four
  existing writer paths and the generators route through it is not done.
- **`broken_links` has never been nonzero in this corpus.** It is verified
  against a synthetic missing file, not a real one.
- **A node body is still a payload, not a marker.** `goal:g13`'s load-bearing
  claim — that what sits on disk is a placeholder saying where the body goes —
  is untouched. This built the mechanism a marker would need; it did not make
  any node a marker.
- The update-time schema check verifies `validation.required` only, not the
  spawn gate, so an update cannot leave a node schema-invalid but also cannot
  catch a parent-shape violation.

## Consequence

`goal:s31` — a scaffolded node ships schema-invalid — is now fixable *through*
this path rather than by hand, which is the next increment and the first real
consumer. `goal:g13.1`'s edit mode has a writer to wrap.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The limits section is longer than the evidence section, deliberately and for
the second time this session. This node will be cited as "g13's write half
landed", and the distance between "there is now a gated routine for in-place
edits" and "the graph's write path is unified" is most of the goal. Writing
`declared: 0` into the verdict itself is the cheapest available defence against
that misreading.

Confidence 0.93 rather than higher because the strongest clause — that this
routine can carry *every* in-place edit — is argued from its interface rather
than demonstrated by callers. The adversarial thought tests are solid and the
corpus scan is real; the generalisation over future callers is not yet
evidence, and s31 is the increment that will make it one.

The naming followed goal:g13's own text — `write.py`, a helper under an owner
module — rather than inventing a fourth name for the same idea. The goal says
`read.py` and `write.py` are helpers and nothing else calls them; today
`write.py` is called directly, because the owning module does not exist yet.
That is a known deviation and it is recorded here rather than quietly
resolved by renaming the file.
<!-- THOUGHT:END -->
