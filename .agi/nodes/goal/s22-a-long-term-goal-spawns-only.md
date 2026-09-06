---
id: goal:s22
mint_id: e95212d7f04241a7a3f5a90e6b4fff8a
type: goal
parents:
  - goal:g15
next_edges:
  - hypothesis:a00-0d182e77-3f4501
confidence: 0.9
edited_by: director
goal_id: S22
goal_kind: short-term
heading_level: 2
origin: goals-doc
seeds: []
status: complete
tags:
  - goal
  - short-term
thought_session: agi-master-2026-09-06
title: A long-term goal spawns only hypotheses — design is earned
---
**A goal may not shortcut to a design brief.** The route from a goal to an
`mvp` runs through `hypothesis -> experiment -> verdict`, so a design is
written against measured evidence rather than against the goal's own optimism.
Make that mechanical, in the schemas the spawn gate already reads, so it holds
for agents nobody briefed.

**What is actually broken is the gate, not dispatch.** `allowed_parents`
declares who may be a node's parent, and six type schemas name `goal`:

| schema | `allowed_parents` | |
|---|---|---|
| `[mvp].md` | verdict, **goal**, experiment, hypothesis | `goal -> mvp` skips the whole chain |
| `[experiment].md` | hypothesis, verdict, **goal**, task, idea, experiment, build | `goal -> experiment` skips the hypothesis |
| `[hypothesis].md` | idea, **goal**, experiment, hypothesis | the intended route — keep |
| `[idea].md` | **goal** | exploration; still lands on a hypothesis next — keep |
| `[build].md` | idea, **goal**, verdict, mvp, build | minted mechanically by `level3.py` — keep |
| `[cron].md` | **goal** | `goal` is its ONLY legal parent; a blanket strip orphans it |

So the change is two lines, not six: drop `goal` from `[mvp].md` and
`[experiment].md`. `[cron].md` is the trap — a structural node, not a chain
node, and stripping it would leave the type unspawnable.

**The dispatch half already behaves.** `_node_type_for`'s step table has no
`goal` key, so a kid aimed at any goal falls through to the default and is
scaffolded a `hypothesis`. Nothing needs building there; what is missing is the
gate that stops a hand-written or differently-routed node taking the shortcut
anyway.

**The kid contract contradicts this and must change in the same commit.**
`zoom.py:594` and `zoom.py:691` both tell every kid: *"Acceptable: spawn one
child node (hyp from idea, exp from hyp, mvp from exp, outcome from mvp)."*
`mvp from exp` advertises precisely the shortcut this goal closes, and
`verdict` appears nowhere in that list — a kid is never told the verdict step
exists, which is a candidate explanation for why asserting verdicts outnumber
evidence-backed ones better than four to one. Closing the gate while the brief
still advertises the hole is how the two drift, which is `goal:g1.9`'s thesis.
They move together or not at all.

**Not scoped to `long-term` goals specifically, because that cannot be
expressed today.** `spawn_gate._parse_rule` maps `allowed_parents` through
`canonical_type()`, which flattens to bare type names: a schema can say `goal`,
never `goal:long-term`. The variant machinery exists — `_shape_key`,
`canonical_shape_key`, and `[shape].md`'s
`parentless_types: [goal:long-term, goal:short-term, idea]` — but only for a
node's **own** variant via its discriminator, never for its parent's.
Parent-variant resolution means `build_type_index` carrying `goal_kind`, which
is real unbuilt work. This goal therefore lands the blanket rule, correct for
all three goal kinds anyway, and **records variant-qualified `allowed_parents`
as its open item** — deferred rather than guessed.

**What would falsify it.** `spawn_gate`'s CLI rejects an `mvp` whose parents
are `[goal:g13]` and accepts a `hypothesis` with the same parent. No existing
node is invalidated — the rule gates new spawns, and the corpus's current
`goal -> mvp` edges stay resolvable as prior art. `[cron].md` still spawns. The
kid contract and the gate agree, checked by a test that reads both.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Marked complete in the 2026-09-01 sweep, the same day it was minted, because
its falsifiers all pass and it has already shaped an iteration.

`spawn_gate check --type mvp --parent goal:g13` exits 2; `--type experiment
--parent goal:s22` exits 2; `hypothesis` and `cron` still exit 0; no existing
node was invalidated. The kid contract moved in the same commit rather than
drifting behind the gate, and carries a test that reads BOTH the contract
string and the gate rules and asserts every route advertised is a route the
gate approves.

The proof it works is that nobody had to remember it: `goal:g13`'s design brief
was spawned off a verdict because that is the only parent the gate now permits,
not because a parent chose correctly.

Its open item stands and is NOT part of this completion: `allowed_parents`
cannot say `goal:long-term`, because `_parse_rule` flattens through
`canonical_type`. Variant-qualified parents remain unbuilt.
<!-- THOUGHT:END -->