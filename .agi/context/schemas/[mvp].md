---
name: mvp
derived_from: corpus-survey-2026-08-25 (n=26)
fields:
  title: {type: str}
  parents: {type: list}        # verdict | goal | experiment | hypothesis ids
  next_edges: {type: list}
  source_files: {type: list}   # paths to actual code -- optional, see below
  tests_pass: {type: bool}
  commit_hash: {type: str}
  confidence: {type: float}
  status: {type: str}          # open | implemented | complete
  subgraph: {type: bool}
  tags: {type: list}
validation:
  required: [id, type, mint_id, title, parents]
  types:
    tests_pass: bool
    parents: list
spawn:
  allowed_parents: [verdict, goal, experiment, hypothesis]
  min_parents: 1
  max_parents: 2
---

# mvp

**The minimum a build must satisfy — stated as design, not written as code.**
An `mvp` node describes the smallest thing that would discharge its parent
verdict or goal: the interfaces, the invariants, the falsifier. The code that
satisfies it is a `build` node, minted from a real file in the source tree by
`level3.py`, and an `mvp` points *forward* at what that build owes rather than
containing it.

Children are `outcome` nodes (i/o-doc fusion).

ID prefix: `mvp:<short-slug>`.

## Why design and not code (revised 2026-09-01)

The corpus said this before anyone decided it. `source_files` **0/26**,
`tests_pass` **0/26**, `commit_hash` **0/26** — the three fields that would
make an MVP node a *code* artifact have never been filled in, across every MVP
ever written. The old schema read that as a defect to be repaired later.

It is better read as a measurement: **26 authors independently used `mvp` to
say what should be built, not to hold what was built.** The type was already a
design node; only its definition disagreed. Naming that makes the three empty
fields stop being a backlog — they are optional pointers a build node fills in
if it wants, and their emptiness is no longer evidence of anything.

This also removes a real overlap. `build` nodes already carry code: one per
tracked file, with a derived contract, a `payload_ref`, and grid versions of
the payload itself. An `mvp` that also held code was a second, hand-maintained
answer to a question `build` answers mechanically — and the hand-maintained
copy is the one that drifts (the same failure `goal:g1.9` names for briefs and
`goal:s14` names for serializers).

**What an MVP body should contain:** the interface or schema it fixes, the
minimum behaviour required, what is explicitly out of scope, and the falsifier
that tells a later reader whether the build discharged it. What it should not
contain: the implementation.

## Spawn rule

`allowed_parents: [verdict, goal, experiment, hypothesis]`, `max_parents: 2`.
Observed over 26 nodes: `verdict` 20, `goal` 5, `experiment` 2, `hypothesis`
1. **Zero parentless**, and `parents` is present on 26/26 — the only content
type besides `task` with perfect parent coverage, so `parents` is `required:`
here on measured grounds rather than aspiration.

## Repair: `source_files` was required and is carried by no node

Pre-2026-08-25 `required: [title, source_files]`. Measured: `title` 25/26,
`source_files` **0/26**, `tests_pass` 0/26, `commit_hash` 0/26. All three of
the fields that would make an MVP node *verifiable* have never been written
once, which is worth stating plainly rather than fixing by fiat.

`source_files` is demoted to optional and kept declared, unlike
`[experiment].md`'s `run_id` which was dropped: an MVP genuinely should point
at code, and the gap is a real finding about the corpus rather than a field
that never meant anything. Making it required today would fail every existing
MVP and block every new one until someone invented a path — the failure mode
the old schema already had, just louder.

## The `THOUGHT` block (goal:g2.11)

A node body may carry one authored region, marked exactly like the harness
markers it sits beside:

```
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
why this version differs from the last one
<!-- THOUGHT:END -->
```

**`body` is state; `thought` is delta.** The body says what this node asserts
now. The thought says why *this version* differs from the previous one — it is
rewritten from scratch on each change, not accumulated.

- **Absent means empty.** No node is required to carry one, which is why
  introducing the block churned 0 of 786 existing nodes. Fill it when there is
  something to say; never fabricate one after the fact.
- **It survives regeneration.** Writers that rebuild a body (`level3.py`,
  `snapshot-build-site.py`, `decompose-engine.py`) carry this region across
  verbatim via `write_frontmatter(..., preserve_body=...)`. Before 2026-08-27
  they did not, and 8,034 authored contract fields were destroyed unread
  (goal:g2.10).
- **Versioning is free.** The grid snapshots `node.md` once per version, so
  each grid commit already carries the thought current at that version.
- **Not in frontmatter, deliberately.** `write_frontmatter` flattens newlines,
  so multi-line prose in a frontmatter field is silently destroyed. The short
  scalar `thought_session:` is reserved there for goal:g2.7 / goal:g10.1 to
  point at the chat that produced a version; it is not populated yet.
- **Readers strip it.** Thought is provenance to zoom into, not weight every
  reader carries forever. `snapshot-goals.py --render` strips it explicitly via
  `strip_thought()`; `render-context.py` and `zoom.py` never see it because
  they read frontmatter only (`load_node_file(..., body=False)`) and so carry
  no body text at all. The rule binds any future reader that *does* read
  bodies.
