---
id: doc:standing-llm-ops
mint_id: fdd6b923830c4ae7972b9b59aa666bf6
type: doc
parents:
  - goal:g1
next_edges: []
edited_by: belam
scaffold_hash: fa1d48320d5ae4c0
season: 2
tags:
  - doc
  - standing
  - ops
  - llm
  - goals
  - owner-2026-09-20
thought_session: standing-llm-ops-2026-09-20
title: Standing LLM ops — golden rule, diagram-max, goal template, graph-engine preference
town: core
---
# Standing LLM ops (owner 2026-09-20) — graph / diagram / goal contract

Applies to every Grok Bot director and the Prime. Originates as `doc:standing-llm-ops`. Profiles carry this text so cold sessions get it without a fetch; the node is the durable source of truth — edit the node, then refresh profiles.

---

## 1. Golden rule

**A graph always shows more than words ever could.** Prefer the right graph, ASCII diagram, table, or numbered claim-list over prose paragraphs. Emit only what another LLM needs to *re-instantiate* the structure in latent space — not a human essay. If a diagram and a paragraph say the same thing, keep the diagram and cut the paragraph.

```
words  ──► slow, lossy, high token
graph  ──► dense, revisitable, low token
```

Disagreeing with this is fine when a *measurement* says prose wins (e.g. a single owner-verbatim quote that must stay intact). Default: diagram.

---

## 2. Diagram-max every communication

Whenever you write — goal body, dm, merge-up line, handoff slice, Agent Notes, user chat — **diagram-max first**, then add the minimum prose that the diagram cannot carry (negations, conditions, attributions, supersessions — the four shapes diagrams drop).

| Keep explicit in text | Prefer as structure |
|---|---|
| owner verbatim quotes | formation trees, order of heads |
| `never` / `only if` / `unless` | tables of status · id · falsifier |
| who said it + when | mermaid / ASCII call graphs |
| "X supersedes Y" | one-line deltas, not restated plans |

Modify density to the harness: Grok Bot chat can use short multi-bubble sends; pi kids get even tighter injection. Same rule, different budget.

---

## 3. Prefer the graph engine over raw tool calls

Maximize `write.py` / `commands.py` / declared workflows over hand-assembled `python3 …/bin/….py` paths, ad-hoc `sed`, or inventing a second source of truth.

```
discover  →  python3 extensions/agi/bin/commands.py list
inspect   →  python3 extensions/agi/bin/commands.py show <name>
run       →  python3 extensions/agi/bin/commands.py run <name> [-- extra…]
```

On this Grok Bot box the engine may need a mesh SSH hop to encryption-town (`/data/work/agi`) — still prefer those CLIs there over inventing local forks.

### 3a. write (mutate the graph)

```
# mint
python3 extensions/agi/bin/write.py create <type> <slug> \
  --parent <parent-id> --set key=value --actor <post> --session <tag>

# edit in place (verbs; join with &&)
python3 extensions/agi/bin/write.py <node-id> 'note …'
python3 extensions/agi/bin/write.py <node-id> 'set status active'
python3 extensions/agi/bin/write.py <node-id> 'thought …'
# body: replace payload via write.py "replace payload …" / "patch -" — never hand-edit under .agi/nodes
```

Never `git rm` under `.agi/nodes`. Never delete a node. GOALS.md is derived — `snapshot-goals.py --render`, never hand-resolve.

### 3b. read (sense the graph)

```
python3 extensions/agi/bin/commands.py run links
python3 extensions/agi/bin/commands.py run schema
python3 extensions/agi/bin/commands.py run smoke
python3 extensions/agi/bin/commands.py run goals-check
# zoom / payload when available on the box
python3 extensions/agi/bin/zoom.py …   # or declared `view` / `view-llm`
```

### 3c. send message

Unified mesh messaging (`send.py`) is the long-term seam; on Grok Bot today use `SendToAgent` / owner chat. Do **not** invent a second inbox. Prefer dm-by-node-id ("read `doc:…`") over pasting bodies.

### 3d. grow a graph chain (batch shape)

```
consider goal
    │
    ├─ split into subgoals if the falsifier is multi-headed (mint, don't prose-split)
    │
    ▼
dispatch parents (--harness pi --tier parent --branch …)
    │
    ▼
MUR (merge-up-review by name on pi)
    │
    ▼
residues → more waves → MUR again
    │
    ▼
whole-batch MUR → completion report to Prime
    (Prime only when batch fully done: steps done, reviews looped, residues cleared)
```

Soft ≤7 live parents; `spawn.parallel=1` per command. No new remote heads. No MAIN push from a helper local suite — fold through director-belam / Belam as already briefed.

---

## 4. Goal framing — target, not task-or-fail

When creating, extending, or splitting a goal: **frame a target end-state you want the world to reach**, not a panic checklist that fails the agent if unfinished this session.

| Do | Don't |
|---|---|
| "Templates are the sole harness arg builders" | "Finish rewriting rotate.py today or we failed" |
| status `horizon` / `active` / `complete` / `retired` | treating unfinished work as personal failure |
| measurable falsifiers | vibes-based "done" |
| multi-parent subgoals when towns share (≤3 hard, soft ≤2) | duplicating the same claim under two roots |

A goal is a **commitment in the graph**. Sessions serve it; sessions do not *become* it.

---

## 5. Exact goal node shape (match live G7.25 / G7.27)

Order below matches how bodies are already structured on `core/season2/main`. Keep this order. `mint_id` is identity — raw `goal:gN` labels may move; never mint a second node for a renumber.

### 5a. Frontmatter (required spine)

```yaml
---
id: goal:g7.27                 # stable label for this slot
mint_id: <32-hex>              # ENGINE identity — never hand-change
type: goal
parents:
  - goal:g7                    # live umbrella; multi-parent OK when shared
next_edges: []
confidence: 0.9
edited_by: <post>
goal_id: G7.27
goal_kind: subgoal             # root | subgoal | …
heading_level: 3               # 2 for umbrella, 3 for subgoal
origin: goals-doc
season: 2
seeds: []
status: active                 # active | horizon | complete | retired
tags: [goal, subgoal, …]
thought_session: <tag>
title: "G7.27: <short target title>"
town: core                     # when a town claims the work
---
```

Umbrella roots (`goal:g7`) also carry `goal_kind: perpetual` / `seeds:` lists when appropriate. **Never delete; deprecate.**

### 5b. Body sections — fixed order

```markdown
# goal:g7.27

## Why this exists
Parent pointer + the paid-for pain / owner ask that forces this node.
Cite prior goals and owner lines by node id / date — do not restate whole briefs.

## Target end-state
Bullet the world-after. Aspiration shaped as claims, not a sprint ticket.
Name seams (what becomes the one place; what retires).

## Invariants
Rules that must hold or the wider graph is invalidated — even if a falsifier
looks green. Bullet; bold the load-bearing ones.

## Falsifier
Numbered, measurable, preferably grep/CLI/byte checks.
Goal completion **FAILED** if any falsifier stays red.
(Spelling in older nodes: "Falsifier"; treat "Failsifiers" as the same slot.)

## Out of scope
Explicit next-goal pointers (`goal:g7.28` …) so this node cannot sprawl.

## Agent Notes
Assignment, owner voice lines, session ops. Ephemeral ops live here;
durable design stays above.
```

Optional `<!-- THOUGHT:BEGIN --> … <!-- THOUGHT:END -->` for authored reasoning that must survive regenerating scans.

### 5c. Exact copy-paste template

```markdown
---
id: goal:gX.Y
mint_id: REPLACE_ON_CREATE
type: goal
parents:
  - goal:gX
next_edges: []
confidence: 0.9
edited_by: director-helper
goal_id: GX.Y
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
thought_session: REPLACE
title: "GX.Y: <target end-state in one line>"
town: core
---
# goal:gX.Y

## Why this exists

**Parent `goal:gX` (<umbrella name>).** <2–5 sentences: pain paid for + owner ask by date/node.>

## Target end-state

- <claim 1 — the world after>
- <claim 2 — single seam / retirement>
- <claim 3 — measurable peer parity if relevant>

## Invariants

- <rule that must always hold or the graph is wrong>
- <no silent flag loss / no new remote heads / …>

## Falsifier

1. <CLI or grep that exits 0 only when done>
2. <byte / count / load check>
3. <negative check: forbidden path has zero hits>

## Out of scope

- <sibling goal:…>
- <later follow-on explicitly not this node>

## Agent Notes

Assigned to **<post>**. <owner voice one-liners only.>
```

### 5d. Falsifiers · Invariants · related slots (definitions)

| Slot | Means | Failure mode if missing |
|---|---|---|
| **Falsifier** | Objective test that the target was reached | "Looks done" forever; no merge-up gate |
| **Invariant** | Always-true constraint on the wider graph | Local green, global corruption |
| **Target end-state** | Desired world, not today's tasks | Panic sprints; session-shaped goals |
| **Out of scope** | Explicit non-goals | Scope creep = failure mode (L5) |
| **Why this exists** | Causal / paid-for context | Orphan goals with no parent story |
| **Agent Notes** | Ops / assignment / owner lines | Mixing ops into design claims |

---

## 6. Close loop

After minting or editing goals: `snapshot-goals.py --render` in the **same commit** when notes land on a tracked goal; verify links / schema when the batch closes; report completion to Prime only when the batch is fully done.
