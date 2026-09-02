---
id: hypothesis:one-gated-edit-in-place
mint_id: 2bddd3c84b42476bb70c71a9b46ca5ee
type: hypothesis
title: "The write half's floor is one gated in-place edit, and the link layer sits on it"
testable_claim: "A single gated `update_node` routine can carry every in-place node edit without destroying the authored THOUGHT region, and `link_ref` generalises `payload_ref` to every node type with zero broken links across the existing corpus."
confidence: 0.85
parents:
  - goal:g13
next_edges:
  - experiment:link-scan-and-the-thought-guarantee
scaffold_hash: d905b9eb69426ca2
verdict: pending
---

# hypothesis:one-gated-edit-in-place

## Hypothesis

`goal:g13` names five operations one interface should own — create a node,
create the file behind it, **edit it in place**, read it, read its history.
Four had a routine. **Editing in place had none**, so every fix, retag and
field addition in this project's history was a hand edit: no schema check, no
guarantee about authored content, no record that a write happened.
`goal:g13.1` names the consequence exactly — a hand edit is *"a completely
stray and untraceable commit"*.

### Testable claim, in two halves

**The floor.** One routine, `node_writer.update_node`, can carry every
in-place edit — merge frontmatter, drop keys, replace a body — and it is safe
to route edits through because it **cannot destroy the authored `THOUGHT`
region**, which is `goal:g2.10`'s defect made impossible rather than
discouraged.

**The layer.** `link_ref` generalises `payload_ref` from one node type to
every node type, with the owner's three settled semantics — `self` for a body
that is its own data, raise on a single read of a missing link, sentinel plus
a counted metric on a bulk scan — and resolves the **existing** corpus with
zero broken links and without rewriting a single build node.

### What would prove it

- An update that replaces a body preserves an authored `THOUGHT` block.
- An update that changes nothing writes nothing, so `grid.py commit --all`
  does not mint a version recording no change.
- An unparseable node is refused rather than rewritten from a partial read.
- Every node in the corpus resolves a link, `broken_links == 0`, and the 220
  nodes already carrying `payload_ref` are linked **without being edited**.
- The metric degrades loudly, never to a healthy-looking `0` it did not
  compute.

### What would disprove it

- Any path where a body rewrite loses the authored region — the whole floor is
  unsafe if this fails, because routing edits through it would then be worse
  than hand-editing.
- A resolver that has to branch on `type == goal` to make `self` work. That
  would mean the exception is a hole with a name painted on it.
- Broken links in the existing corpus, which would mean `link_ref` is not a
  generalisation of `payload_ref` but a different field wearing its clothes.

### Scope this deliberately does not claim

**It does not migrate the corpus.** 685 nodes resolve `self` by *default*
rather than by declaration, and the resolver reports which of the two it got —
so a later migration can tell what is done from what was never started. Making
the corpus declare its links is the next increment, and betting 900 nodes on
an unproven layer is how this project has previously lost work.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Two halves in one hypothesis because they are not separable in practice: the
link layer has to write `link_ref` somewhere, and until this session there was
no gated routine that could add a field to an existing node. Building the layer
without the floor would have meant `write.py` editing files directly — which
would make it the second write path inside the goal that exists to remove
second write paths.

The scope paragraph is the part most likely to be skipped and is the reason
this hypothesis is modest. The tempting version claims the marker migration
too. That version bets the whole corpus on a layer with no live use, and this
project has a rule about exactly that shape: 807 nodes in, 807 out, rehearsed
four times before the goal:g11 cut. The declared-vs-defaulted distinction
exists precisely so the migration can be a separate, checkable step.

The disproof clause about branching on `type == goal` is the sharpest one. The
owner's answer was that a goal links to itself, and the entire value of that
answer over "goals are exempt" is that no reader learns what a goal is. A
resolver with a type check in it would satisfy the letter and lose the point.
<!-- THOUGHT:END -->
