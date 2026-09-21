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
thought_session: standing-branch-roles-2026-09-20
title: Standing LLM ops — golden rule, diagram-max, goal template, graph-engine preference
town: core
---
# Standing LLM ops (owner 2026-09-20) — graph / diagram / batch / goal contract

```
source of truth ──▶ doc:standing-llm-ops
cold-start copy ──▶ agent profiles (pointer + spine; node wins on conflict)
applies to      ──▶ Prime · director-belam · director-helper
                    (directors identical except self-name + report-to)
```

---

## 1. Golden rule

**A graph always shows more than words ever could.**

```
words  ──▶ slow · lossy · high token
graph  ──▶ dense · revisitable · low token
```

Default: diagram. Exception: owner-verbatim quotes (protected, stay prose).

---

## 2. Diagram-max — every token emitted

Scope: dm · note · card · watch · instruction · profile · handoff · thought · user chat · future-self.

```
emit ──▶ one flow OR table
      ──▶ prose ONLY where diagram drops meaning
      ──▶ keep EXPLICIT:
            never / only-if / unless
            conditions
            who + when (attribution)
            X supersedes Y
      ──▶ owner verbatim stays verbatim
```

| Prefer structure | Keep as text |
|---|---|
| formation trees · head order | owner quotes |
| status · id · falsifier tables | negations / conditions |
| ASCII / mermaid call graphs | attributions / supersessions |

This doc itself must obey the rule (and be re-trimmed when parts finish).

---

## 3. Batch-max — compress passes, not meaning

Same ethic as diagram-max: **more meaning per token**, not less meaning.

```
batch-max
  ├─ ONE report per COMPLETED pass (never per step)
  ├─ fold many deltas into one flow / table
  ├─ idle → wake ONLY on [merge-up] · [decision] · [red] · [rule] · [rotation]
  └─ minimize ALL outbound tokens (incl. to owner)
```

Comms route (owner 2026-09-20 23:1x ET — supersedes prior "user may get frequent updates"):

```
directors ──▶ Belam (Prime): routine batch updates ONLY
              (completed pass / numbers-only [merge-up])
directors ──▶ owner (Shael): blocker updates ONLY
              (red · decision-needed · stuck — never routine progress)
Belam     ──▶ owner: blockers + land decisions; not in-flight chatter
```

---

---

## 3b. Branch roles (owner 2026-09-20 23:2x ET — core-town)

```
Belam (Prime)     ──▶ core/main              (town/main)
director-belam    ──▶ core/season2/main      (town/season2/main)
director-helper   ──▶ local worktree ONLY
                      never push a new remote head
                      completed batches → director-belam (merge-up)
loops             ──▶ merge into core/season2/main then delete loop heads
no season2/loops/* left live as standing remotes
```

Keep working batches as-is otherwise. Diagram-max all alignment comms.

## 4. Prefer graph engine over raw tools

```
discover  →  commands.py list
inspect   →  commands.py show <name>
run       →  commands.py run <name>
mutate    →  write.py create|note|set|replace body|…
```

### write

```
write.py create <type> <slug> --parent … --set k=v --actor … --session …
write.py <id> 'note …' | 'set status active' | 'replace body 1: <path>'
```

Never `git rm` under `.agi/nodes`. Never delete nodes. GOALS.md derived only.

### read

```
commands.py run links|schema|smoke|goals-check
```

### send

Prefer dm-by-node-id over pasting bodies. Grok Bot: `SendToAgent` / owner chat until `send.py` is the one seam.

### chain growth

```
goal → split (mint) → dispatch pi parents → MUR → residues → MUR →
  whole-batch MUR → completion report to Prime
```

Soft ≤7 live parents · `spawn.parallel=1` · no new remote heads.

---

## 5. Goal framing — target, not task-or-fail

| Do | Don't |
|---|---|
| target end-state | "finish today or failed" |
| measurable falsifiers | vibes-done |
| multi-parent ≤3 (soft ≤2) | duplicate claims under two roots |

---

## 6. Exact goal node shape (live G7.25 / G7.27)

`mint_id` = identity. Raw `goal:gN` may move; never second mint for a renumber.

### frontmatter spine

```yaml
---
id: goal:gX.Y
mint_id: <engine>
type: goal
parents: [goal:gX]
goal_id: GX.Y
goal_kind: subgoal
status: active   # active|horizon|complete|retired
title: "GX.Y: <target one-liner>"
---
```

### body order (fixed)

```
# goal:gX.Y
## Why this exists
## Target end-state
## Invariants
## Falsifier          # FAILED if any red
## Out of scope
## Agent Notes
```

### copy-paste template

```markdown
---
id: goal:gX.Y
mint_id: REPLACE_ON_CREATE
type: goal
parents: [goal:gX]
next_edges: []
confidence: 0.9
edited_by: <post>
goal_id: GX.Y
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 2
seeds: []
status: active
tags: [goal, subgoal]
thought_session: REPLACE
title: "GX.Y: <target end-state in one line>"
town: core
---
# goal:gX.Y

## Why this exists
**Parent `goal:gX`.** <pain paid for + owner ask by date/node.>

## Target end-state
- <world-after claim>
- <single seam / retirement>

## Invariants
- <always-true or graph is wrong>

## Falsifier
1. <CLI/grep exit 0 only when done>
2. <negative: forbidden path zero hits>

## Out of scope
- <sibling goal:…>

## Agent Notes
Assigned to **<post>**. <owner one-liners only.>
```

| Slot | Means | If missing |
|---|---|---|
| Falsifier | objective done-test | forever "looks done" |
| Invariant | always-true graph rule | local green / global wrong |
| Target | desired world | session-shaped panic |
| Out of scope | explicit non-goals | scope creep |
| Why | paid-for cause | orphan goals |

---

## 7. Close loop

```
mint/edit → snapshot-goals --render (same commit as notes)
         → links/schema when batch closes
         → Prime only when batch fully done
```

**Land gate:** tip may not land if the goal body fails §6 format — format residue first, then re-MUR.

<!-- THOUGHT:BEGIN --> … <!-- THOUGHT:END -->
