---
id: verdict:spawn-gate-lands-on-writer-path
mint_id: 9a84308c787f492d9bc9359672f52dee
type: verdict
parents:
  - exp:node-type-corpus-survey
  - exp:spawn-gate-falsifier
next_edges:
  - mvp:spawn-gate
verdict: proved
confidence: 0.85
evidence_runs:
  - exp:node-type-corpus-survey
  - exp:spawn-gate-falsifier
supports:
  - hyp:spawn-check-on-writer-path
contradicts: []
tags:
  - s17
  - schema
  - gate
title: "Proved: the spawn rule is derivable, expressible and enforceable on the writer path — for 2 of ~6 writers"
---

# verdict:spawn-gate-lands-on-writer-path

**`proved`, on the core claim, at the level it actually holds.**

## The claim that is proved

A spawn rule read from `context/schemas/[<type>].md` and applied inside
`cli.py` rejects an illegal spawn with a message naming **the rule, the schema
file, the node and the fix**; announces an explicit approval naming the schema
on a legal spawn; and leaves every historical violation in place.

All three registered falsifier points fired, with verbatim output in
`exp:spawn-gate-falsifier`:

| registered check | outcome |
|---|---|
| `verdict` with no parent | REJECTED, `min_parents` from `[verdict].md`, exit 2, no file |
| `task` with three parents | REJECTED, `max_parents` from `[task].md`, exit 2, no file |
| legal spawn | APPROVED, schema file + every rule that passed, on stdout and stderr |

Plus two unregistered runs: wrong parent type rejects by name, and the
fail-open path fired on a genuine typo of mine and declined to guess.

The three sub-claims of the hypothesis each resolve:

1. **Derivable** — the survey reproduces §S17's table exactly, and 721/778
   nodes (92.7%) already conform to the rules derived from it. Zero unresolved
   parent references corpus-wide, so parent types are always knowable.
2. **Expressible** — `goal`'s three shapes needed a discriminator, and one
   schema with `discriminator: goal_kind` expresses it. Forced, not chosen:
   `SchemaRegistry.resolve()` keys on `type:`, every goal is `type: goal`, so a
   `[g-goal].md` would never be reached and would be dead data that looked
   authoritative.
3. **Enforceable at the right moment** — the check runs before any write, so a
   rejection leaves nothing behind. Verified by `ls`.

## What is explicitly NOT proved — read this before citing the above

**Coverage is 2 of roughly 6 node-writing paths.** Gated: `cli.py scaffold`,
`cli.py done`'s fallback verdict node, and `post_wire.py`'s verdict creation.
**Not gated:**

- `dispatch.py` — carries a *duplicated, un-gated copy* of the whole scaffold
  routine, including its own `NODE_TYPES` (still hyphenated) and its own
  prompts dict. It is the pi-runtime path, so CC-native dispatch does not hit
  it, but a pi run writes nodes past this gate entirely. Not owned by this
  change; the duplication is the real defect and deleting it in favour of
  `cli.py scaffold` is the fix.
- `snapshot-goals.py`, `snapshot-build-site.py`, `level3.py` — generators.
  Arguably they should be gated *last*, since a generator that trips the gate
  is a generator bug and failing the loop over it is worse than reporting it.
  Undecided, deliberately.

**The rule table is a description, not a justification.** It is transcribed
from 778 nodes. If the corpus embodies a bad habit, the table now blesses it.
The one place corpus and rule disagree is `min_parents`, and 53 nodes lose
that argument — see below.

**No claim about node quality.** The gate checks `type` and `parents`. It says
nothing about whether a node is worth having, and it does not run the
`validation:` block (`required`/`types`/`regex`) at write time — that engine
exists (`schema_registry/validation.py`) and is still unwired. Wiring it would
fail a large share of the corpus immediately; that is a separate decision.

**`[config].md` is one-field-read.** `spawn_gate.resolve_nodes_root` consults
`locations.nodes_root`, which clears G10.2's bar for a geometry declaration.
The other five locations — `engine_root` above all, still defined twice in
Python and once in shell — are **documented, not collapsed**. Collapsing them
means editing `level3.py` and `grid.py`. Residual, named, not claimed.

## The 53 — a report, not a purge

| type | violations | rule |
|---|---|---|
| hypothesis | 24 | `min_parents: 1` |
| verdict | 21 | `min_parents: 1` |
| experiment | 4 | `min_parents: 1` |
| level3 | 4 | `min_parents: 1` |

Every violation is the same rule. **Zero** nodes exceed `max_parents`; **zero**
name a disallowed parent type. So two of the three rules are pure description
and only `min_parents` is a claim the corpus contradicts.

None of the 53 was touched. `node_count` went 769 → 778 across this work and
never fell. G7's first invariant holds, and G7.1's policy — a bad reference is
fixed or dropped, never the node, and never inferred — is written into the
gate's own reject text and into its fail-open path.

Four further nodes are `unverified` rather than approved or rejected: three
carry **no `type:` field at all**, and `doc:goals-preamble` is a type minted
this session with no schema. The typeless three are a genuine hole — nothing
keyed on `type:` can ever apply to them.

## Why `proved` rather than a lean

`evidence_runs` names two experiment nodes that both exist. Every registered
falsifier point produced observed terminal output, not a description of
expected output. The claim is narrow enough to be checked in one command and
was checked. Confidence 0.85 rather than higher because the coverage gap
above is real: on a pi run, `dispatch.py` still writes nodes this gate never
sees.
