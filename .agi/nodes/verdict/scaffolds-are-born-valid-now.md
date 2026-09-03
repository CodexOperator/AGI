---
id: verdict:scaffolds-are-born-valid-now
mint_id: e649c1bb0f1a4ee69047d94a2db535cf
type: verdict
title: Scaffolds are born valid now
parents:
  - experiment:the-falsifier-and-the-corpus-census
next_edges: []
scaffold_hash: 4ff580407a6d89fd
verdict: proved
confidence: 0.97
evidence_runs:
  - experiment:the-falsifier-and-the-corpus-census
---

# verdict:scaffolds-are-born-valid-now

## Verdict

proved

## Evidence

`experiment:the-falsifier-and-the-corpus-census`, against this project's real
schemas:

- A hypothesis scaffolded through the normal path is born with
  `title: Bounded population holds` and reaches **`FINAL missing required: []`**
  after its kid writes a body — **no parent intervention**.
- `completion.is_complete` reads `False` untouched, `True` filled, and
  **`True` after the frontmatter fill**. The fix did not buy validity with the
  completion check.
- Two identical scaffolds under schemas that differ only in whether `title` is
  required produce the **same `scaffold_hash`**. The hash is over the body.
- Corpus census: **115 of 900** nodes invalid, read through
  `schema_registry.validate`.
- **Live dispatch has now run.** Iteration 1007's kids were scaffolded by the
  fixed writer: `hypothesis:a01-8e09cdf2-6c63ec` was born with the seeded
  title, had a real title set through the gated update path, and its
  `testable_claim` lifted from its own body at `cli.py done`. The parent of
  this review cycle verified the mechanism in code (68/68 tests in
  `test_node_writer`/`test_completion` green) and re-ran the census:
  **71 of 956** invalid, every gap in the predicted non-derivable set,
  zero `title` gaps.

## What is proved

**`goal:s31`'s vice is dissolved for new nodes.** The two rules that
contradicted each other now partition the required fields instead: the engine
seeds what it can derive at write time, the kid writes what only it holds into
the **body** under a briefed heading, and the gated write path lifts it into
frontmatter at completion. **No agent ever touches frontmatter**, so the
`scaffold_hash` hazard that made rule 2 correct is untouched.

A field in neither population stays absent and is named on stderr as
`SCHEMA-WARNING`. That is `goal:s31`'s third candidate shape doing its actual
job: it fixes nothing, and it converts a silent defect into a visible one.

## What is NOT proved — read this before citing it

- **The corpus is repaired only for the derivable half, and the repair
  already happened.** `L1.07` (`ab07ec980`) ran the backfill for real:
  **118 → 62 invalid, 90 field-instances filled**, residual exactly this
  node's predicted set (`testable_claim` x51, `scale` x7, `next_edges` x3,
  `confidence` x1). The iter-1007 census reads 71 of 956: the 62 plus nine
  in-flight kids of the current iteration, and still nothing else. The
  `write.py schema [--fix]` command that did the backfill was **removed from
  `write.py` in the same commit** — the verb layer's mechanically-checked
  no-file-write invariant did not survive a backfill carved an exception. The
  residual needs `goal:g1.9` (model or brief change), not a command.
- **51 of 56 missing claims are unreachable by this mechanism.** `_section_text`
  is heading-driven; a body that states its claim in prose without the heading
  gets no help. So "scaffolds are born valid" is a claim about *new* nodes and
  does little for old ones.
- **Only `title` is derivable at scaffold time.** Everything else needs a
  caller's flags or a body.

## The correction this iteration made to itself

The first census reported **203** invalid nodes because the check was
`not fm.get(k)`, and `seeds: []` — what a goal with no seeds correctly carries
— is falsey. The registry's rule is `None` or an empty *string*. 88 of those
203 were that false positive. It is recorded rather than quietly fixed because
it is `goal:s31`'s own thesis committed by s31's implementer: a hand-rolled
predicate agreeing with the schema by convention instead of reading it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, iteration 1007. The kid's verdict stands and is stronger
than when it was written; this version updates two of the "NOT proved"
clauses because the world moved, not because the review found the kid
wrong.

**Clause "No live dispatch ran" is now false, and it was the one that
capped the confidence.** The kid wrote: "Confidence 0.94 rather than
higher because no spawned agent has run through this path. … a live kid
writing a real body under a real brief is the case that matters and it
has not happened yet." It has. Iteration 1007's kids are being scaffolded
by the fixed writer, and `hypothesis:a01-8e09cdf2-6c63ec` is the cleanest
example: born with the seeded title, real title set through the gated
update path, `testable_claim` lifted from its own body at `cli.py done`,
completion detected. The parent verified the mechanism in code — 68/68
in the two relevant test files — and re-ran the census: 71 of 956
invalid, all in the predicted non-derivable set, zero title gaps. That is
the clause's own success condition, met. Confidence 0.94 → 0.97; it does
not go higher because the lift fires at `cli.py done`, so a kid killed
between body-fill and done leaves a heading-bearing body with the field
still absent — nine such nodes are on disk right now, and the brief
should be the durable fix, which is `goal:g1.9`'s, not this verdict's.

**Clause "The corpus is not repaired" is also stale, and its staleness is
worth recording.** The backfill ran for real in `L1.07` (`ab07ec980`):
118 → 62 invalid, 90 filled, residual exactly the set this node predicted
— the falsifier of `mvp:the-corpus-becomes-schema-valid` passing on its
predicted number rather than on 0. The same commit then **removed**
`write.py schema [--fix]`, because the verb layer's no-file-write
invariant is mechanically checked and the backfill did not survive an
exception. This node cited that command as existing; a verdict that gets
cited as "s31 is fixed" must not name a tool the next reader cannot
find. The correction is in the body, not a footnote, because the body is
what gets quoted.

What did not change, and was re-checked rather than assumed: the hash-
is-over-the-body mechanism, the delta-not-state validation rule, and the
"nothing is invented" invariant — `L1.07`'s node diff carries +2 THOUGHT
lines net across 93 files, so the backfill lost nothing it was supposed
to carry.
<!-- THOUGHT:END -->
