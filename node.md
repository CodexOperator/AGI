---
id: exp:spawn-gate-falsifier
mint_id: a59b1cf86c7e4d50b2cdbb75c0440f8a
type: experiment
parents:
  - hyp:spawn-check-on-writer-path
next_edges:
  - verdict:spawn-gate-lands-on-writer-path
confidence: 0.9
edited_by: season.py
season: 1
subgraph: false
tags:
  - s17
  - schema
  - falsifier
thought_session: season
title: "Pre-registered falsifier: two illegal spawns rejected by name, legal spawns approved out loud"
---
# exp:spawn-gate-falsifier

The falsifier was registered in `GOALS.md` §S17 **before** the gate existed:
write a `verdict` with no parent and a `task` with three parents — both must
be rejected with a message naming the rule and the schema file. Attempt one
legal spawn and get an explicit approval line. **If any of the three is
silent, this is not done.**

All output below is verbatim from `payloads/extensions/agi/bin/cli.py`, the
real writer path, in `/home/ubuntu/work/agi-tree` on 2026-08-25.

## 1. `verdict` with no parent — REJECTED

```
$ cli.py scaffold 9010 kid-schema --type verdict --slug s17-falsifier-orphan
!! SPAWN-GATE REJECTED: verdict:s17-falsifier-orphan — rule 'min_parents' (1) from context/schemas/[verdict].md: verdict declares 0 parent(s). Schema: context/schemas/[verdict].md (shape 'verdict'). Fix: give verdict:s17-falsifier-orphan at least 1 parent of type {experiment, hypothesis, verdict}. Only goal:long-term, goal:short-term, idea may be parentless (context/schemas/[shape].md). Do not invent a parent to satisfy this — pick the node this one actually follows from.
ERR: spawn rejected for verdict:s17-falsifier-orphan: rule 'min_parents' (1) from context/schemas/[verdict].md: verdict declares 0 parent(s). Fix: ... (--no-spawn-gate bypasses this, loudly.)
SPAWN-GATE REJECTED verdict:s17-falsifier-orphan type=verdict parents=0 schema=context/schemas/[verdict].md
exit=2
```

Rule named (`min_parents`), schema file named (`[verdict].md`), node named,
fix stated, **and the whitelist cited from its own file** so the reader learns
why `idea` gets away with it and `verdict` does not.

## 2. `task` with three parents — REJECTED

```
$ cli.py scaffold 9010 kid-schema --type task --slug s17-falsifier-triple \
    --parent hyp:t-001-node-primitive --parent hyp:t-002 --parent hyp:t-003
!! SPAWN-GATE REJECTED: task:s17-falsifier-triple — rule 'max_parents' (1) from context/schemas/[task].md: task declares 3 parents ['hyp:t-001-node-primitive', 'hyp:t-002', 'hyp:t-003']. Schema: context/schemas/[task].md (shape 'task'). Fix: drop 2 parent(s) from task:s17-falsifier-triple, or raise max_parents in context/schemas/[task].md AND the ceiling in context/schemas/[shape].md. The budget is 1 because 1 is what the corpus has ever used; raising it is a deliberate act, not a default.
exit=2
```

**This one could not even be attempted before the change.** `--parent` was a
single *required* flag, so argparse — not the schema — decided every type had
exactly one parent, and its error named no rule and no file. The flag now
collects and the gate is the authority. `task` was also absent from
`NODE_TYPES` entirely: the tool whose job is creating nodes could not create
the type with 91 of them.

**Nothing was written by either rejection:**

```
$ ls nodes/verdict/s17-falsifier-orphan.md nodes/task/s17-falsifier-triple.md
ls: cannot access 'nodes/verdict/s17-falsifier-orphan.md': No such file or directory
ls: cannot access 'nodes/task/s17-falsifier-triple.md': No such file or directory
```

## 3. Legal spawns — APPROVED, out loud

This chain's own six nodes were created through the gated path. Verbatim:

```
$ cli.py scaffold ... --type idea --slug schema-declared-spawn-gate --parent goal:s17
-- SPAWN-GATE APPROVED: idea:schema-declared-spawn-gate checked against context/schemas/[idea].md [idea] — min_parents>=0; max_parents<=1; allowed_parents={goal}. parents=['goal:s17']
scaffolded: /home/ubuntu/work/agi-tree/nodes/idea/schema-declared-spawn-gate.md

$ cli.py scaffold ... --type verdict --slug spawn-gate-lands-on-writer-path \
    --parent exp:node-type-corpus-survey --parent exp:spawn-gate-falsifier
-- SPAWN-GATE APPROVED: verdict:spawn-gate-lands-on-writer-path checked against context/schemas/[verdict].md [verdict] — min_parents>=1; max_parents<=2; allowed_parents={experiment, hypothesis, verdict}. parents=['exp:node-type-corpus-survey', 'exp:spawn-gate-falsifier']

$ cli.py scaffold ... --type mvp --slug spawn-gate --parent verdict:spawn-gate-lands-on-writer-path
-- SPAWN-GATE APPROVED: mvp:spawn-gate checked against context/schemas/[mvp].md [mvp] — min_parents>=1; max_parents<=2; allowed_parents={experiment, goal, hypothesis, verdict}. parents=['verdict:spawn-gate-lands-on-writer-path']
```

The approval states **which schema file** and **which rules passed**, so
"approved" is distinguishable from "not checked" without reading any code.
Note the verdict node exercises the 2-parent budget exactly.

## 4. Two unregistered outcomes, both real

**Wrong parent type is rejected too** — not in the pre-registration, run
because it is the third rule and it would have been dishonest to leave it
untested:

```
$ spawn_gate.py check --type verdict --parent idea:schema-declared-spawn-gate --id verdict:wrong-parent-type
!! SPAWN-GATE REJECTED: verdict:wrong-parent-type — rule 'allowed_parents' from context/schemas/[verdict].md: verdict may not be parented by 'idea' (parent 'idea:schema-declared-spawn-gate'); allowed: ['experiment', 'hypothesis', 'verdict']. Fix: reparent verdict:wrong-parent-type onto a node of type {experiment, hypothesis, verdict}, or add 'idea' to spawn.allowed_parents in context/schemas/[verdict].md if the corpus really uses that shape.
exit=2
```

**The fail-open path fired on a real mistake of mine**, which is the best
evidence it works:

```
$ cli.py scaffold ... --type experiment --slug node-type-corpus-survey --parent hyp:spawn-check-on-writer-path
-- SPAWN-GATE UNVERIFIED: exp:node-type-corpus-survey — parent(s) ['hyp:spawn-check-on-writer-path'] name no node in the corpus, so their type could not be checked against context/schemas/[experiment].md. The node is written. Fix the reference, or drop it — never infer one (G7.1).
```

I typed `hyp:` because that is what `[hypothesis].md` documents as the id
prefix; `cli.py scaffold` had minted `hypothesis:`. The corpus carries **both**
— `hyp:` 73 vs `hypothesis:` 33, and `exp:` 70 vs `experiment:` 5 — so neither
is wrong, and the gate correctly declined to guess which node I meant. It
wrote the node, said exactly what it could not check, and stamped
`spawn_check: unverified`. I fixed the reference by hand; no parent was
inferred.

## 5. Test suite

```
$ python3 -m pytest payloads/extensions/agi/tests/test_spawn_gate.py -q
37 passed in 1.07s

$ python3 -m pytest payloads/extensions/agi/tests/ -q
668 passed, 1 skipped in 26.58s
```

37 new tests; both falsifiers are among them, so they cannot silently regress.

## 6. Two bugs the run itself caught, recorded because they generalise

- **`---` inside YAML frontmatter truncates it.** A comment banner of dashes
  in `[shape].md` silently emptied the geometry under the cheap
  `text.split("---", 2)` parser that every writer path uses (`build_corpus`,
  `_read_frontmatter`, `cli.py`). The schemas still "loaded"; the fields were
  just gone. Pinned by a test.
- **Over-eager canonicalisation.** Mapping `-` → `_` across a whole shape key
  turned `goal:long-term` into `goal:long_term`, matched nothing, and
  disabled the entire `[goal].md` schema — while reporting a confident-looking
  error. Fixed by canonicalising the *type half only*: a discriminator value
  legitimately contains a hyphen. Pinned by a test.

## 7. What did NOT happen — the negative control

`node_count` rose 769 → 778 and never fell. All 53 rule-violating nodes are
untouched: the gate runs on the writer path, so history is out of its reach by
construction, not by policy.