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
confidence: 0.94
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

- **The corpus is not repaired. 115 nodes are still invalid on disk.** The
  backfill exists (`write.py schema --fix`) and was run **dry only**.
- **A backfill would fix 91 field-instances and leave 62.** `title` x86 and
  `testable_claim` x5 are derivable; `testable_claim` x51, `scale` x7,
  `next_edges` x3 and `confidence` x1 are not, and would stay absent rather
  than be invented.
- **51 of 56 missing claims are unreachable by this mechanism.** `_section_text`
  is heading-driven; a body that states its claim in prose without the heading
  gets no help. So "scaffolds are born valid" is a claim about *new* nodes and
  does little for old ones.
- **No live dispatch ran.** The falsifier went through direct `write_node`
  calls against the real schemas, not through a spawned agent.
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
The limits section is again longer than the evidence, and for the third time
this session that is deliberate rather than a tic. This node will be cited as
"s31 is fixed". It is fixed forward; 115 nodes on disk say it is not fixed
backward, and the single most quotable sentence here needs the second half
attached to it.

Confidence 0.94 rather than higher because no spawned agent has run through
this path. The falsifier used the real schemas and the real writer, but a live
kid writing a real body under a real brief is the case that matters and it has
not happened yet. Everything else in the clause list is measured.

The self-correction section is kept in the verdict, not just the experiment,
because a verdict is what gets read. A mistake recorded only in the node
nobody opens is a mistake recorded nowhere.
<!-- THOUGHT:END -->
