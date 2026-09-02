---
id: experiment:link-scan-and-the-thought-guarantee
mint_id: 894bad469adf49bc9eaa9ef2ea0bb84e
type: experiment
title: "Scan every node's link; try to destroy a thought through the writer"
parents:
  - hypothesis:one-gated-edit-in-place
next_edges:
  - verdict:the-write-half-has-a-floor
scaffold_hash: 87923ea9b46b9fc4
verdict: proved
confidence: 0.93
evidence_runs:
  - experiment:link-scan-and-the-thought-guarantee
---

# experiment:link-scan-and-the-thought-guarantee

## Experiment

### Part 1 — the corpus scan

`write.py links` over every live and deprecated node in this graph, resolving
each one's link the way a reader would:

```
links: 905 resolved, 0 broken
  declared       0
  payload_ref  220
  defaulted    685
```

**905 nodes, zero broken links, and not one node edited to get there.** The
220 already carrying `payload_ref` resolve through it as the predecessor field
it is, which is what makes `link_ref` a generalisation rather than a rival.

`declared: 0` is the honest reading of where the migration stands: nothing has
opted in yet, and the resolver says so rather than reporting 685 nodes as
though they had chosen `self`. Same distinction `envfile.Resolution.from_node`
makes — *"the graph said so"* and *"the fallback guessed"* are different
claims.

`metrics.py` now emits `broken_links=0` on every `--smoke`, in the same shape
as `unevidenced_decisive_verdicts`: a number whose only healthy value is zero.

### Part 2 — trying to destroy an authored thought

`goal:g2.10` is the standing proof that a writer which rewrites a body
destroys authored content and nobody notices — 8,034 fields read `TODO(model)`
because a generator rewrote the whole body each run. So the test is adversarial
rather than confirmatory: **replace the body entirely and check what survives.**

| attempt | result |
|---|---|
| replace body, old thought present | thought **carried across** into the new body |
| replace body, new body brings its own thought | new kept, old dropped, **exactly one** block |
| update that changes nothing | `UNCHANGED`, file not rewritten, **mtime unchanged** |
| update a node that does not exist | `REJECTED`, **no file created** |
| update an unparseable node | `REJECTED`, original bytes intact |

The unchanged case is checked by `st_mtime_ns`, not by content, because a
rewrite producing identical bytes still mints a grid version — and versions
record change, not time.

The unparseable case matters more than it looks: rewriting a node from a
partial read turns an *unreadable* node into a *wrong* one, which is strictly
worse and much harder to notice.

### Part 3 — the resolver does not know what a goal is

`test_self_resolves_to_the_nodes_own_body_without_branching_on_type` resolves
`goal:g1` with `link_ref: self` through the same code path as every other
node. There is no `type == goal` branch in `write.py` — `grep` confirms the
string does not appear. That is the entire difference between the owner's
answer (an exception **with a name**) and the alternative it beat (goals are
exempt, i.e. a hole every caller handles its own way).

### Counts

15 new tests in `test_write.py`; suite 1279 → **1294**, all passing.

### What this experiment does NOT show

- **No node in this corpus has been migrated.** `declared: 0`. The layer
  resolves what is already there; nothing yet depends on it.
- **`broken_links` has never been nonzero here.** The counter is verified by
  unit tests against a synthetic missing file, not by this corpus, which has
  no broken link to find.
- **`update_node` has no production caller yet** beyond `write.set_link`. That
  it *can* carry every in-place edit is argued from its interface and tested
  in isolation; that it *does* is the next increment.
- The schema check on update is deliberately weaker than the spawn gate: it
  verifies `validation.required` only, because re-running the spawn gate on a
  field edit would make the 216 grandfathered build nodes unwritable
  (`goal:s29`).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Part 2 is written as an attack rather than a demonstration because that is the
only way this claim is worth anything. "The writer preserves thoughts" tested
by updating frontmatter proves nothing — the interesting case is the one where
a caller hands over a whole new body, which is exactly what the generator in
goal:g2.10 was doing when it destroyed 8,034 fields.

The mtime assertion in the unchanged case was added after the content
assertion, on noticing that identical bytes rewritten still produce a grid
version. The rule this project already holds is that versions record change,
not time; a writer that rewrites unconditionally quietly breaks it, and the
content check would have passed.

`declared: 0` is reported as a headline number rather than buried, because it
is the most misreadable result here. A reader skimming "905 resolved, 0
broken" could conclude the migration landed. It has not started. The counter
exists to make that difference legible, and the experiment should not undo its
own instrument by reporting the total alone.
<!-- THOUGHT:END -->
