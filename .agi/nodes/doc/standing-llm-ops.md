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
thought_session: suite-per-batch-2026-09-21
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

Scope: dm · note · card · watch · instruction · profile · handoff · **thought / thought-stream** · user chat · future-self · director↔director · director↔Belam.

```
thought-stream ──▶ same rule as outbound comms
                ──▶ flows / tables / graphs — not essay monologue
                ──▶ keep never/only-if/unless + who/when explicit
```

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

### Zero-residue land gate (owner 2026-09-21 — HARD)

```
MUR
  ├─ accept                ──▶ residues=0 ──▶ [merge-up] allowed
  ├─ accept_with_residue   ──▶ residues>0 ──▶ NO merge-up
  │                            directors KEEP looping pi parents
  │                            → MUR → … until residues=0
  └─ reject / format-fail  ──▶ fix → re-MUR (never land)
```

| Signal | Who loops | Belam sees? |
|---|---|---|
| residues > 0 | directors + pi parents | **NO** `[merge-up]` |
| residues = 0 + format ✓ | — | YES numbers-only `[merge-up]` |
| blocker / red / decision | — | owner ONLY (not Belam routine) |

**Why:** review exists to burn residues on cheap parents — not to spend Belam/owner tokens on half-done batches.

```
WRONG  MUR accept_with_residue ──▶ [merge-up] Belam
RIGHT  MUR accept_with_residue ──▶ spawn parents ──▶ MUR ──▶ … ──▶ residues=0 ──▶ [merge-up]
```

Comms route (owner 2026-09-20/21 — supersedes prior frequent-update habits):

```
directors ──▶ Belam (Prime): [merge-up] ONLY when residues=0
              (numbers-only · tip SHA · goal ids · no essays)
directors ──▶ owner (Shael): blockers ONLY
              (red · decision-needed · stuck — never routine progress)
Belam     ──▶ owner: blockers + land decisions; not in-flight chatter
Belam     ──▶ REJECT [merge-up] that still carries residue
directors ──▶ loop independently (pi parents) until residues=0; do not wait on Belam mid-loop
```


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

---

## 3c. Watches / routines — diagram-max with love (owner 2026-09-20/21)

For every LLM that wakes on a timer: **be kind**. One flow. No essays. Silence when nothing changed.
Install this FORMAT **verbatim** into the live routine prompt (seat pins only differ).

### Shared director watch (ONE only — delete per-wave customs)

```
schedule ──▶ @every 50m   (pi parents run around the clock — stated reason)
name     ──▶ live-parents-workflows
FORMAT   ──▶ shared (below) — MUST mirror §3 zero-residue + §4 routes
pins     ──▶ seat-local TREE / SCOPE / HOST / BRANCH only
```

**Prompt FORMAT (install exactly; substitute seat pins only):**

```
Quiet night watch — love the next LLM ingest. Diagram-max. Batch-max.

SCOPE: this seat only (<ITER>.* parents / this-director MURs / suite).
TREE:  <absolute seat worktree>
BRANCH:<this director's branch role>
HOST:  SSH encryption-town → /data/work/agi  (never /workspace/agi)

STANDING (verbatim — doc:standing-llm-ops)
```
golden · diagram-max · batch-max
land   format ✓ AND residues=0
comms  Belam←[merge-up] residues=0 only · owner←blockers only
routes write·read·send·dispatch/workflow·rotate/spawn
```

ZERO-RESIDUE (HARD)
```
MUR accept              ──▶ residues=0 ──▶ [merge-up] OK (not from this watch)
MUR accept_with_residue ──▶ residues>0 ──▶ NO merge-up · KEEP parent loops
MUR reject/format-fail  ──▶ fix → re-MUR
```

ROUTES (any graph touch)
```
WRITE write.py | READ commands.py | SEND send.py
DISPATCH dispatch.py+workflow.py | ROTATE rotate.py
```

1) Sense
   parents you spawned: alive?
   workflows you spawned: running?
   status=done + no MUR yet → owed (list it)
   MUR accept_with_residue still open → residual loop owed (list it)
2) Emit ONLY on delta
   | id | kind | state | note |
   |----|------|-------|------|
   | <ITER>.* | parent/wf/MUR/residue | up/dead/owed | ≤1 short |
3) Route
   Belam  ← nothing from this watch
   owner  ← blockers ONLY (red/stuck/decision)
   residues>0 → spawn/continue pi parents (NOT [merge-up])
   residues=0 + format ✓ → [merge-up] path outside this watch
4) No delta → silence (no "no change")
5) Never invent. Never new remote head. Never push core/main.
6) Prefer graph routes (§4) over raw tools.
```

**Seat pins (examples — not a second FORMAT):**

```
director-belam
  SCOPE  DT.* · TREE /data/work/agi/.agi/worktrees/seat-director-belam
  BRANCH core/season2/main (WT pin seat/director-belam@s2)
director-helper
  SCOPE  DH.* · TREE /data/work/agi/.agi/worktrees/seat-director-helper
  BRANCH local-only · never new remote head
  completed batches → director-belam (not helper) · only residues=0
```

### Belam
No standing chatter watch. Belam receives director `[merge-up]` **only at residues=0**; owner gets blockers. Belam **rejects** residue merge-ups.



## 3d. Residue rounds → version the goal node (owner 2026-09-21 — HARD)

Each residue pass must **write the goal** (subgoal / sub-subgoal / …) so the graph keeps history. Nodes are versioned; do not leave residue state only in MUR prose or chat.

```
residue round
  ├─ identify open residues on goal:gN(.M…)
  ├─ update THAT node body sections that track residue progress
  │     (Agent Notes · Target progress · Falsifier status — as fits §6)
  ├─ replace WHOLE per-version rows (not patch-in-place across versions):
  │     thought · feeling · (any sibling versioned block)
  │     → new version carries the new whole block; history keeps the old
  ├─ write.py  (graph route) — never raw edit that skips versioning
  └─ then continue parent loop / re-MUR
```

| Do | Don't |
|---|---|
| `write.py` update on the owning goal id each residue pass | leave residue only in MUR / dm |
| replace entire `THOUGHT` / feeling / versioned row | surgically edit one line of an old version in place |
| keep Why→…→Agent Notes order (§6) | invent a second body shape |
| diagram-max the residue table in Agent Notes | essay dump of residue narrative |

```
WRONG  MUR accept_with_residue ──▶ spawn parents ──▶ (goal body stale)
RIGHT  MUR accept_with_residue ──▶ write.py goal:gN… (residue table + new THOUGHT)
                                 ──▶ spawn parents ──▶ MUR ──▶ … ──▶ residues=0
```

## 3e. Full verify suite after every completed batch (owner 2026-09-21 — HARD)

**Why own branches exist:** each director burns the **full verify suite on THEIR branch tip** after a completed batch (residues=0 + format ✓), before `[merge-up]`. That is the point of seat/worktree isolation — not to skip the suite.

```
batch done (residues=0 · format ✓)
  ├─ on THIS seat branch / worktree only
  ├─ FULL verify suite  (engine suite · F7 lock rules still apply)
  ├─ green ──▶ [merge-up] numbers-only (tip · suite stamp · mur)
  └─ red   ──▶ fix in-loop · re-suite · never merge-up red
```

| Do | Don't |
|---|---|
| full suite on **your** branch tip after each clean batch | skip suite because "touched tests already ran" |
| one suite window per completed batch (diagram-max report) | chatter mid-suite |
| Belam/land path still gates on green suite evidence | merge-up with suite red or unrun |
| helper: suite on local tip before batch → director-belam | push MAIN to "get suite" |

Touched-family pytest at harvest remains for **rounds**. The **batch** gate is the full suite on the branch.

```
round harvest ──▶ touched-family tests
batch close   ──▶ full verify suite on seat branch ──▶ then [merge-up]
```

## 4. Prefer graph engine over raw tools

Every graph touch goes through the **five pane-facing routes** (see also `goal:g7.31.3`). Raw shell/git under `.agi/nodes` is last resort.

```
                    ┌──────────── pane / seat ────────────┐
                    │                                     │
   discover  ──▶  commands.py list                        │
   inspect   ──▶  commands.py show <name>                 │
   run       ──▶  commands.py run <name>                  │
                    │                                     │
        ┌───────────┼───────────┬───────────┬─────────────┤
        ▼           ▼           ▼           ▼             ▼
     WRITE        READ         SEND      DISPATCH      ROTATE
     write.py   commands.py   send.py   dispatch.py   rotate.py
                + viewport              + workflow.py  (+ spawn)
        │           │           │           │             │
        └───────────┴───────────┴───────────┴─────────────┘
                              │
                              ▼
                         graph SoT
```

| Route | CLI | Use for |
|---|---|---|
| write | `write.py create\|note\|set\|replace body\|…` | mint/edit nodes |
| read | `commands.py run links\|schema\|smoke\|goals-check` | verify / viewport |
| send | `send.py` (Grok: `SendToAgent` until seam) | dm-by-node-id |
| dispatch\|workflow | `dispatch.py` + `workflow.py` | pi parents · MUR · review |
| rotate\|spawn | `rotate.py` | seat lifecycle · pane hold |

### write

```
write.py create <type> <slug> --parent … --set k=v --actor … --session …
write.py <id> 'note …' | 'set status active' | 'replace body 1: <path>'
```

Never `git rm` under `.agi/nodes`. Never delete nodes. GOALS.md derived only.

### read

```
commands.py list | show <name> | run links|schema|smoke|goals-check
```

### send

Prefer dm-by-node-id over pasting bodies. Grok Bot: `SendToAgent` / owner chat until `send.py` is the one seam.

### chain growth (residue loop is the point)

```
goal
  → split (mint)
  → dispatch pi parents
  → MUR
  → residues? ──yes──▶ dispatch more parents ──▶ MUR ──┐
       │                                              │
       no (residues=0 + format ✓)                     │
       ▼                                              │
  whole-batch MUR accept                              │
       ▼                                              │
  [merge-up] → director-belam → Belam                 │
       ▲                                              │
       └────────────── loop until 0 ←─────────────────┘
```

Soft ≤7 live parents · `spawn.parallel=1` · no new remote heads.

### Lean MUR / review file lists (owner 2026-09-21 — HARD)

```
MUR / overall-review context
  stacked too thick (context-build timeout risk)
    ──▶ thin file list (lean ≤8–12 files; tip + falsifier + residue targets)
    ──▶ raise ctx timeout only after lean
    ──▶ NEVER ship fat context hoping it fits
permission: directors MAY thin anytime without re-asking owner
still: graph routes only (dispatch/workflow) · no route bypass
```

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
mint/edit
  → snapshot-goals --render (same commit as notes) when goals changed
  → links/schema as needed
  → whole-batch MUR
  → residues=0 AND format ✓
  → FULL verify suite on THIS seat branch  (§3e)
  → suite green ──▶ [merge-up] Belam
  → residues>0 OR format ✗ OR suite red ──▶ parents/fix loop (NO Belam)
```

**Land gates (all required):**
1. Goal body passes §6 format (else format residue → re-MUR).
2. **Residues = 0** (else keep looping — never `[merge-up]`).
3. **Full verify suite green on the seat branch** (§3e).

`accept_with_residue` is a **continue signal**, not a land signal.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
owner 2026-09-21: directors MAY thin MUR/overall-review file lists when context stacks too thick (ctx-build timeout risk); lean first (≤8–12: tip+falsifier+residue), raise timeout only after; never ship fat context; graph routes only
<!-- THOUGHT:END -->
