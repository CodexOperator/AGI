---
id: experiment:the-falsifier-and-the-corpus-census
mint_id: 5f1f90fce155431788a151cb726880e9
type: experiment
title: The falsifier and the corpus census
parents:
  - hypothesis:born-valid-without-touching-frontmatter
next_edges:
  - verdict:scaffolds-are-born-valid-now
scaffold_hash: 01d5d56d4030d1a7
verdict: proved
confidence: 0.94
evidence_runs:
  - experiment:the-falsifier-and-the-corpus-census
---

# experiment:the-falsifier-and-the-corpus-census

## Experiment

### Part 1 — `goal:s31`'s falsifier, run against the real schemas

A scratch graph carrying **this project's actual `context/schemas/`**, four
node types scaffolded through the normal `write_node` path, no parent touching
anything:

| type | seeded `title` | still missing at scaffold |
|---|---|---|
| hypothesis | `Bounded population holds` | `testable_claim` |
| experiment | `Mint latency` | — |
| verdict | `Per spawn wins` | `verdict`, `confidence` |
| idea | `One write path` | `scale` |

Then the kid's half — a body written under the heading its brief asks for:

```
untouched scaffold   is_complete: False      <- must be False
filled body          is_complete: True       <- must be True
derive status:       updated
testable_claim:      'The live population never exceeds the declared bound.'
after fill           is_complete: True       <- must STILL be True
FINAL missing required: []
```

**Both falsifier clauses hold.** The node reaches schema-validity with no
parent intervention, and completion detection is unchanged before and after
the fill. `verdict`/`confidence` are supplied by `cli.py done`'s own flags on
the real path, which is why the verdict row above is not a gap.

`test_seeding_required_fields_does_not_move_the_scaffold_hash` asserts the
mechanism that makes this safe rather than assuming it: two identical
scaffolds, one under a schema requiring `title` and one not, produce the same
`scaffold_hash`. **The hash is over the body**, so frontmatter cannot move it.

### Part 2 — the corpus census, and a bug in the first census

First run reported **203** invalid nodes, led by `goal: seeds x86`.

**That was wrong, and the way it was wrong is the goal's own thesis turned on
its author.** The check was `not fm.get(k)` — a truthiness test — and
`seeds: []` is exactly what a goal with no seeds is supposed to carry. The
registry's own rule is `None` or an empty *string*; an empty *list* is present
and legal. A hand-rolled emptiness test is precisely the "agrees with the
schema by convention" that `goal:s31` gives as its reason not to patch
locally. Replaced with a delegation to `schema_registry.validate`.

Corrected census, **115 nodes** of 900:

| type | nodes | missing |
|---|---|---|
| hypothesis | 56 | `testable_claim` x56, `title` x33 |
| verdict | 26 | `title` x25, `confidence` x1 |
| experiment | 20 | `title` x20 |
| idea | 8 | `scale` x7, `title` x3 |
| outcome | 3 | `next_edges` x3, `title` x3 |
| mvp | 2 | `title` x2 |

The 86 goal nodes and 2 task nodes in the first count were **entirely** the
false positive.

### Part 3 — what a backfill would and would not repair

`write.py schema --fix` exists and was run **dry only**:

(Since `L1.07` / `ab07ec980`: the backfill ran for real — 118 → 62
invalid, 90 filled, residual exactly the set predicted below — and the
schema command was then removed from `write.py`, whose mechanically-
checked invariant is that the verb layer performs no file write.)

```
WOULD FIX   : title 86, testable_claim 5
WOULD REMAIN: testable_claim 51, scale 7, next_edges 3, confidence 1
```

91 field-fills are derivable — `title` from the node's own address, and five
bodies that already state a claim under a heading. **62 are not derivable and
would stay absent**, because the alternative is inventing them.

### What this experiment does NOT show

- **Nothing in the corpus was repaired at the time this ran.** Part 3 is a
  dry run; 115 nodes were still invalid on disk. Since: `L1.07` ran the
  backfill for real (90 field-instances; residual 62, matching the
  prediction) and removed the schema command from `write.py`.
- **Only `title` is derivable at scaffold time.** Every other required field is
  either supplied by a caller's flags or must come from a body.
- **`_section_text` is heading-driven and shallow.** A kid that states its
  claim in prose without the heading its brief names is not helped, and 51 of
  the 56 missing `testable_claim`s are exactly that case.
- **No live dispatch ran.** The falsifier was executed against the real
  schemas but through direct `write_node` calls, not through a spawned agent.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, iteration 1007. The experiment's record of what it ran
stands untouched — this version only corrects two present-tense claims
that the tree has since made false, and adds no new finding.

The first census mistake (203 → 115, the falsey `seeds: []`) stays as the
node's centerpiece. It is still the most instructive part of it: the exact
failure mode `goal:s31` names as its reason not to want a local patch,
committed by the person implementing the fix for `goal:s31`.

The corrections: Part 3 named `write.py schema --fix` as a standing tool
and "What this experiment does NOT show" said nothing had been repaired.
Both were true on 2026-09-02. On 2026-09-03, `L1.07` (`ab07ec980`) ran
the backfill for real — 118 → 62 invalid, 90 filled, residual exactly the
predicted set — and removed the command from `write.py`, because that
file's no-file-write invariant is mechanically checked. A node that is
cited as the falsifier of record must not keep naming a tool the next
reader cannot find and must not keep asserting a state the corpus no
longer has, so the two sentences carry parenthetical since-notes rather
than being rewritten: the dry-run numbers were real measurements at the
time, and the record of what this experiment did is not mine to re-date.

Part 3's dry-run-only decision stands on its own terms. Rewriting ~91
nodes is reversible and probably right, and it in fact did happen — a
day later, by the director, with the predicted residual. The bank-then-
do sequence is the honest reading of this node's caution: the experiment
said "dry only, banked"; the owner's session then decided the run was
safe enough to make real.
<!-- THOUGHT:END -->
