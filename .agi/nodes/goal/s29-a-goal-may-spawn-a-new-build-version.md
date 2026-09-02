---
confidence: 1.0
goal_id: S29
goal_kind: short-term
heading_level: 2
id: "goal:s29"
mint_id: 59a9f401fda54dcdac9368e2349c4801
origin: goals-doc
seeds: []
status: complete
tags:
  - goal
  - root
  - short-term
title: "S29: A goal may spawn a new version of a build node, but never a new one"
type: goal
---

**The owner's rule, 2026-09-02.** A build node may be parented **only** by:

```
parents: [mvp:<id>]                    a NEW build node, specified by an mvp
parents: [build:<id>, goal:<id>]       a NEW VERSION of an existing build node
```

**A goal alone must never mint a build node.** It can motivate a new version of
a file that has already earned its place; it cannot conjure a file. The owner's
framing: an existing build node *"already proved its empirical worth by
existing"*, so a goal may extend it — and only it.

**Why an mvp for anything new.** An `mvp` states the minimum a subsequent
`build` must satisfy plus its falsifier (`[mvp].md`, revised 2026-09-01). A
build node with an mvp behind it is a file someone argued for; one without is a
file someone wrote.

**Why both halves of `[build, goal]`.** The `build` parent says *which* file
this is a new version of; the `goal` says *why this version differs*, which is
the one thing a diff cannot tell you. A lone `build` parent is a version with
no motive.

## It needed a new kind of rule, and that is the interesting part

`spawn_gate` could express **AND across kinds** (`min_parents_by_type`, added
for `bigger_outcome`) but not **OR across whole shapes**. `allowed_parents:
[mvp, build, goal]` alone under-constrains: it would also permit a lone `goal`,
which is precisely the case this rule exists to forbid.

**`spawn.parent_shapes`** is the new key — a list of exact permitted
parent-type multisets. **Exact, not superset**, because "one mvp" and "one mvp
plus a goal" are different claims about where a file came from, and silently
permitting the second makes the first unenforceable. It refuses an
unsatisfiable declaration at parse time (a type outside `allowed_parents`, or a
shape outside `min_parents..max_parents`), for the reason `min_parents_by_type`
already does: a schema declaring an impossible rule rejects its whole type
forever, loudly and uselessly.

**Every type that does not declare `parent_shapes` is unaffected** — empty
tuple means no shape restriction.

## The 216 existing build nodes are grandfathered, and it is mechanical

192 parented by an `idea` (the `level3.py` census parent), 19 with no parents
at all, 5 by a goal. **None is retro-invalid.** Their empirical worth is
established by existing and by the engine running on them.

Two facts checked *before* the change, because tightening a schema a generator
writes through would have broken every scan:

- **`spawn_gate` is creation-time only** — it already tolerates 51 nodes that
  violate `min_parents`.
- **`level3.py` does not route through `node_writer`/`spawn_gate` at all**, so
  the rescan that re-mints all 216 with their census parents is untouched.

`idea` and `verdict` left `allowed_parents` for the same reason they are in
neither shape: they were the census-era answer, and the census is what is being
grandfathered rather than continued.

## Falsifier

Six shapes through `check_spawn`. `[mvp]` and `[build, goal]` approve; `[goal]`,
`[build]`, `[idea]` and `[mvp, goal]` reject. Then re-run `level3.py` and
confirm the 216 census-parented build nodes still re-derive unchanged.

**Status: first clause verified** — all six behave as specified, asserted in
`test_lifecycle_guards.py`. **The level3 re-derivation was reasoned, not run**:
`level3.py` was confirmed by grep to make no call into `node_writer` or
`spawn_gate`, which is why the change is safe, but a full rescan has not been
executed since. That is the residual and it is cheap to close.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Filed `complete` rather than as a plan, because the rule was small enough to
build in the session it was asked for -- but the honest half of that is written
into the falsifier: the gate behaviour is tested and the level3 rescan is only
argued. Grep is good evidence that a generator does not call a gate; it is not
the same as watching 216 nodes re-derive.

The design judgement worth keeping is that `allowed_parents` was the wrong
shape of rule rather than the wrong contents. It is a flat set, and the owner's
rule is a disjunction of shapes; widening the set to cover both shapes
necessarily permits their mixtures, including the exact case -- a lone goal
minting a file -- that the rule exists to forbid. Recognising that saved
inventing a discriminator, which was the other way out and would have collided
with `build_kind`.
<!-- THOUGHT:END -->
