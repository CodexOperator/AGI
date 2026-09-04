---
id: hypothesis:a01-0df1f63a-ee41c7
mint_id: 282eea874c26416d974929ecc5b1547c
type: hypothesis
parents:
  - goal:g13
next_edges: []
confidence: 0.0
scaffold_hash: 8bd74c9e38ed6299
title: Generator preserve-keys are already provided by update_node's merge semantics
verdict: pending
---
# hypothesis:a01-0df1f63a-ee41c7

## Hypothesis

**Claim.** The three generators (`snapshot-goals.py`, `snapshot-build-site.py`,
`level3.py`) each maintain an explicit `preserve=` list of frontmatter keys to
carry forward across a full-body rewrite *because* no gated write path existed
when they were written. `node_writer.update_node` already provides this
contract by construction: its `set_fm` is a **merge** over the existing
frontmatter, so keys not in `set_fm` survive without anyone listing them.
Routing a generator through `update_node` removes the need for a separate
preserve-keys mechanism — `update_node`'s merge behavior IS the mechanism,
and no extra parameter is needed.

**Why this is falsifiable in a way the join hypothesis is not.** The join
hypothesis (a01-721930d9-d34989) asks whether read + write compose into one
engine.py — a structural claim about three modules. This hypothesis asks a
simpler, narrower question: whether the generator's own `preserve` parameter
(some 48 lines of YAML-aware, sorted-key frontmatter serialization) can be
eliminated entirely, replaced by the merge that the gated writer already
performs. That would mean the preserve-keys "mechanism the write path must
grow" (quote from the join hypothesis's own falsification criteria) is already
there — it just needs callers.

### What would prove it

1. **`snapshot-goals.py --render` re-routed** to call `update_node` (with a
   `set_fm` of only the keys the generator means to set) produces output
   byte-identical to the current `write_frontmatter` path — verified by
   running both to separate temp dirs and `diff -rq`.

2. **The generator's `preserve=` argument is structurally redundant:**
   every field it carries forward is already carried by `update_node`'s merge,
   because no value in `preserve` is a key the generator's own `set_fm`
   touches. (Static property: check each generator's `preserve` set against the
   keys it writes; `isdisjoint` is the right assertion.)

3. **`snapshot-goals.py --render --check`** (round trip byte-identical with
   GOALS.md) still passes after the re-route — proving the generator's external
   interface is unchanged.

### What would disprove it

- **A `preserve` key that protects a field the body rewrite would strip.**
  If a generator's `preserve` list contains a key like `origin` or `goal_id`
  that the generator computes but that `update_node`'s body path would drop,
  merge semantics alone are insufficient: the body replacement loses authored
  content that frontmatter merge never touches. This would mean the generators
  need a preserve mechanism the write path does not yet provide — exactly the
  gap the join hypothesis names.

- **A generator whose `set_fm` overlaps its `preserve` set.** If a field
  appears in both sets, `write_frontmatter` lets `fm` win (the generator's
  computed value overrides the preserved one). `update_node`'s merge does the
  same (later wins), so the output is identical, but the preserve clause is
  *structurally* unnecessary — proving the mechanism existed only because
  `write_frontmatter` serialized the entire frontmatter from a single dict.
  Finding this is evidence for the hypothesis, not against it, but the
  generator's preserve parameter was misleading.

- **`update_node`'s delta-validation gate rejects a generator's write.**
  The gate rejects keys that would BREAK a required field. If a generator
  produces a node that is already schema-invalid on a key `update_node` must
  now protect, routing through `update_node` would fail where the current
  unsanctioned `write_frontmatter` would succeed — proving the gated write
  path is stricter than the generator's existing path and generators require a
  bypass or a relax.

### Scope — what this deliberately does NOT claim

- **It does not claim all three generators can be re-routed.** Proving one
  is the test; the others are follow-on experiments.
- **It does not claim `snapshot-goals.py` should in fact be re-routed.** Whether
  a generator should route through the write path is a design choice. The
  hypothesis is about whether the `preserve` mechanism is structurally
  necessary given `update_node`'s merge — a property of the existing code, not
  a prescription.
- **It does not claim the read path is unified.** The join hypothesis covers
  that. This covers only the write half, and only for generators.

### Relationship to the g13 chain

| Prior finding | Tells this hypothesis |
|---|---|
| Write-floor proved (905/905, 0 broken) | `update_node` exists, is the one update path, preserves thought. This tests whether generators can use it as-is. |
| Join hypothesis pending (0.65 conf) | Flags preserve-keys gap as open. This tests whether the gap is real or already closed by `update_node`'s merge design. |
| `write_frontmatter` in snapshot-goals.py | Self-contained YAML serialization with own `preserve=` parameter. The primary subject. |
| `update_node` merge semantics | `set_fm.update()` merges over existing frontmatter — keys not in `set_fm` survive. This is the hypothesis's core claim. |

**What falsifies `goal:g13` itself, through this hypothesis.** If the
preserve mechanism is structurally unnecessary, the remaining gap between
generators and the gated write path is smaller than the existing hypotheses
state — generators can use `update_node` as-is, without growing a new
preserve-keys parameter. This would raise the join hypothesis's confidence by
removing one of its falsification criteria. If the preserve mechanism IS
structurally needed (because `update_node`'s merge alone does not protect keys
the body rewrite touches), then the write-floor verdict's "update_node has no
production caller" gap is deeper than stated — it requires an extension to the
merge model, not just a caller.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Kid a01-0df1f63a wrote this on iteration 1072, filling a scaffold against goal:g13. The join hypothesis (a01-721930d9-d34989) names the generator preserve-keys gap as one of its falsification criteria, treating it as an open design problem. But `update_node`'s `set_fm` is already a merge, not a replacement — this hypothesis claims the gap was never a gap: the merge semantics provide the preserve contract for free, and the generators' explicit `preserve=` lists exist only because `write_frontmatter` rebuilds the entire frontmatter from a dict, which naturally drops unlisted keys. Testing this would either prove the g13 chain's write-path gap is already closed by design, or expose a real edge case where merge alone is insufficient.

Parent review, iteration 1072 (a01-23e7224e): both load-bearing code facts re-checked — `node_writer.update_node`'s docstring and body do state `set_fm` is merged over existing frontmatter (node_writer.py L608+), and `snapshot-goals.py` really carries `write_frontmatter(..., preserve=)` (L326+, used at L769/L1011). One defect found and fixed: the Agent Notes below mangled `goal:g13` into `$/g13`. Otherwise accepted as-is; the kid's own caveat — claim is theoretical until a generator is actually re-routed and diffed — is the right next experiment, not a demotion.
<!-- THOUGHT:END -->

## Agent Notes
Hypothesis: generator preserve-keys are provided by update_node's merge semantics, making the preserve= parameter structurally unnecessary. The join hypothesis flags this as an open gap; this hypothesis claims the gap is already closed by design — update_node's set_fm merge preserves unlisted keys for free. Two prior determinations of the 'preserve-keys gap' (goal:g13 write-floor verdict: `declared: 0` across the corpus; the join hypothesis flags the gap as open design) are brought together by testing whether the generator's own mechanism (write_frontmatter preserve=) is redundant against the merged-write semantics of update_node.
