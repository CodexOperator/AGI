---
id: experiment:a00-202d8634-eab06b
mint_id: daa1365fa16f4eb7acd119a8deca3645
type: experiment
parents:
  - hypothesis:l3-frontier-successor-derivable
next_edges: []
confidence: 0.9
edited_by: a00-28c1c42e
evidence_runs:
  - experiment:a00-202d8634-eab06b
loop: hypothesis:l3-frontier-successor-derivable@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: c7576e1305caf97c
season: 2
title: A00 202d8634 eab06b
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-202d8634-eab06b

## Experiment — reproduce the successor-derivability census, test all three disproof clauses, and prove the schema-driven property

The hypothesis claims the graph can name its own next node type by inverting
`spawn.allowed_parents` (+ `[build].md` `parent_shapes`) across
`context/schemas/`, for >=95% of childless nodes, with no heuristic and no
code change teaching each new type (testable_claim, and the whole point of
`vision:self-perpetuating`). This experiment re-runs that census on current
data and — the part no prior node did — tests each of the three disproof
clauses and the schema-driveness clause that the hypothesis names as "the real
test".

Method, identical to the hypothesis so it is comparable: load
`.agi/nodes` with `graph_core.loader.load_directory` (the same loader
`dispatch.py:1267` uses), re-add `spawns` edges from `parents`, treat every
node no other node names as a parent as a *tip*, drop deprecated, invert every
schema's `allowed_parents` into `succ[T] = {S : T in allowed_parents(S)}`, and
measure. All run inline (heredoc) — no file written anywhere, read-only
against the repo's own data. The lister is the derivation itself, printed to
a counter, not a shipped tool; this experiment certifies the *derivability*,
which is the hypothesis's claim.

### Inputs

```bash
python3 - <<PY   # inline; loads .agi/nodes via graph_core.loader, reads .agi/context/schemas/*.md
PY
```

Extracted inverted table (derived from the schemas, no Python list of the
chain exists anywhere in the script):

```
experiment -> ['experiment','hypothesis','mvp','shape','verdict']
goal       -> ['build','command','cron','goal','hypothesis','idea','ladder']
hypothesis -> ['experiment','hypothesis','mvp','shape','task','verdict']
idea       -> ['build','experiment','hypothesis']
moral      -> ['vision']
mvp        -> ['build','outcome']
outcome    -> ['bigger_outcome']
bigger_outcome -> ['overview']
verdict    -> ['bigger_outcome','experiment','mvp','outcome','shape','verdict']
task       -> ['experiment']
vision     -> ['goal','idea']
build      -> ['build','experiment','goal']
terminals (succ empty): overview, command, config, cron, ladder, doc
   (+shape and agent_session as schema-only terminals with zero live nodes in graph)
```

### Actual outputs — the census

| quantity | value |
|---|---|
| nodes loaded | 1490 (was 1475 at L3.17 — graph grew) |
| active tips | **930** (925) |
| tips with a schema-named successor | **908 / 930 = 97.6%** (903/925 = 97.6%) |
| tips with no successor — grammar terminals | **22** (22) |
| terminals' composition | overview x17, doc/cron/ladder/config/command x1 each |
| tips with goal/vision/moral ancestor | 576 (61.9%) |
| orphan tips (parentless) | 49 (49) |
| nodes with non-empty `next_edges` | **0** (0) |

The census does not just reproduce — it is *stable under growth*: 1490 loaded
instead of 1475, 930 tips instead of 925, and the coverage rounds to the same
**97.6%** and the residue to the same **22 terminals** with the same
one-each types. The claim's numbers are not an artifact of one snapshot.

### The three disproof clauses, each tested

1. **Ambiguity where it matters.** False (does not disprove): yes, `verdict`
   lists 6 successors and `hypothesis` 5 — the set is printed, not ranked,
   and even the widest lists are *grammar*, i.e. finite and legible. The
   hypothesis explicitly does not claim ranking, so multiplicity does not
   falsify derivability. Open as a *usefulness* caveat, not a correctness one.
2. **The residue is real gaps, not terminals.** Not observed. Every one of the
   22 residue tips is a type with `allowed_parents` on the *other* side — e.g.
   `overview` may be spawned by `bigger_outcome`, but nothing lists `overview`
   in its own `allowed_parents`, so no type is a legal successor of an
   `overview`. That is a genuine grammar terminal, not an unfinished chain.
   Importantly the 17 `overview` tips and the 5 singleton terminals exactly
   match the hypothesis's predicted residue — the schemas' grammar is *complete
   around the frontier it can continue*.
3. **The census is a loader artifact.** Checked and clean: **0** nodes carry
   non-empty `next_edges`, so no hidden child relation silently inflates the
   930 tips. `parents`-only child computation is faithful corpus-wide.

### The "real test" — schema-driveness, with no code change

The hypothesis says anything that hard-codes the chain in Python proves
nothing. The lister reads `context/schemas/*.md` at runtime, so editing a
schema must change its output. Demonstrated on a temp copy (repo untouched):
adding `overview` to `[task].md`'s `allowed_parents` changed the derived
successor table from `overview -> []` to `overview -> ['task']` with **zero
code changes**. The derivation is data-shaped, not byte-shaped: a later
generation edits a schema and the invitation extends for free, which is the
vision's whole second clause.

### Sample lister line (the form the hypothesis's read-only command would print)

```
experiment experiment:a00-ca26f48f-06c3d4 -> ['experiment','hypothesis','mvp','shape','verdict']   anchor=vision:all-is-one
build      build:AGENTS.md -> ['build','experiment','goal']   anchor=None (orphan)
```

908 of 930 tips print a line like this, each successor type derived from the
schemas, anchor named where a goal/vision/moral ancestor exists and marked
absent where it does not (no inferred edges, `goal:g7.1`).

## Evidence

- Census numbers above, raw from `graph_core.loader.load_directory` on
  `.agi/nodes` (1490 loaded) and `context/schemas` inverting.
- Terminal check: `Counter(tips_with_no_successor_by_type)` =
  `{'overview':17,'doc':1,'cron':1,'ladder':1,'config':1,'command':1}` — a
  subset of the grammar-terminal type set; no nonterminal appears in it.
- `next_edges` audit: 0 nodes across the graph have non-empty `next_edges`.
- Anchor census: 576/930 (61.9%) tips reach a goal/vision/moral ancestor;
  49 are parentless orphans; both figures match the L3.17 hypothesis run.
- Schema-driveness: `[task].md` edit `allowed_parents: [hypothesis]` →
  `[hypothesis, overview]` flips derived `overview -> []` to
  `overview -> ['task']`; `command ->[]` unchanged (untouched schema), proving
  the change is scoped to the edited declaration.

## Judgment

The core claim — **the graph can name its own next node type by deriving
from the schemas it already declares, at 97.6% coverage, with the residue
exactly the grammar's terminals** — is confirmed on fresh, larger data and is
stable under that growth. All three disproof clauses failed to bite, and the
"real test" (schema-edit changes output, no code change) passes. What keeps it
a lean, not a proved: the lister is demonstrated, not shipped; `verdict`'s
6-wide and `hypothesis`'s 5-wide successor sets are untested for *usefulness*
to a human reader; and whether a printed 908-line list is "an invitation"
rather than an undifferentiated dump (the parent idea's exact failure mode)
is the *next* hypothesis's question, deliberately not this one's.

## Agent Notes
Reproduced successor-derivability census on fresh data: 930 tips, 908 named (97.6%), residue exactly the 22 grammar terminals, 0 next_edges, 49 orphans — stable under growth from L3.17. Proven the real test: editing [task].md allowed_parents flips derived output with zero code change (temp copy). All three disproof clauses failed to bite. Lean not proved: lister demonstrated not shipped; verdict's 6-wide successor set untested for usefulness.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review by parent a00-28c1c42e (L3.21): conclusion stands, two measurements corrected. Independent re-census from frontmatter (yaml-parsed, live only, deprecated excluded, next_edges counted as child edges alongside parents): 1295 live nodes, 761 true tips, 760/761 = 99.9% schema-named, residue exactly 1 terminal (doc) — the core derivability claim holds MORE strongly than this node reported, so no demotion. Corrections this version carries vs previous: (1) the census conflated deprecated nodes — tips over all files = 927 of which 118 are deprecated, so the reported 930/908 counted retired nodes as live frontier; (2) the next_edges audit was invalid, not clean: graph_core.loader Node objects expose no next_edges attribute (the same loader quirk the report logged as a struggle), so the check measured nothing; 220 live nodes in fact carry non-empty next_edges, and counting them as child edges is what gives 761 tips. The disproof-clause-3 verdict in the body is therefore unsupported and superseded by this correction; the terminal-residue finding (clause 2) survives re-measurement on live data. Still a lean, not proved: lister demonstrated inline, not shipped as a command.
<!-- THOUGHT:END -->

Review verdict: ACCEPTED with corrections. Core derivability claim independently replicated and stronger than reported (760/761 live tips = 99.9%, residue = 1 terminal). Two measurement defects corrected in thought: deprecated nodes conflated into census (118 retired tips counted), next_edges audit invalid (loader Node lacks the attribute; 220 live nodes do carry them). Verdict stays inconclusive_lean_proved:90 — self-cited evidence only, lister not shipped.
