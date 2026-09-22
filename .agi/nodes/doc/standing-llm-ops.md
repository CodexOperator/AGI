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
thought_session: belam-graph-sot-seat-sync-2026-09-21
title: Standing LLM ops — golden rule, diagram-max, goal template, graph-engine preference
town: core
---
# Standing LLM ops (owner 2026-09-20/21) — graph / diagram / batch / goal contract

**Owner 2026-09-21 GRAPH-ONLY:** directors coordinate via town/geometry **board** (no routine Belam chat). Belam ~once/day: merge · full verify · vision→goals + moral→visions lens · reopen/mint residues. Instant exceptions only (below).

```
source of truth ──▶ doc:standing-llm-ops
cold-start copy ──▶ agent profiles (pointer + spine; node wins on conflict)
applies to      ──▶ ALL posts (Prime · directors · future)
harness golden  ──▶ mirrors ← graph SoT only (§4c)
Grok recipe     ──▶ doc:grok-harness-internals-sync + per-post *-grok-internals
Belam SoT       ──▶ doc:belam-grok-internals
directors SoT   ──▶ doc:director-grok-internals
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

## 2b. town · trajectory · .geometry (Belam 2026-09-21)

```
town:*                 ──▶ OPS home (who / bundle / what's left / location)
trajectory:* (pending) ──▶ KG counterpart (metrics / mini-vision / links→chain)
.geometry/towns/<slug> ──▶ Pass-1 raw .self + formation templates (g7.34.3–.5)
```

| layer | owns | not |
|---|---|---|
| town | ops board, location, who's on it | lasting metrics SoT |
| trajectory | measured progress + chain links | dispatch/ops roster |
| .geometry/towns | self cells + formation render | goal nesting SoT |

Stand-ins live in **town body** until `trajectory:*` type lands (`goal:g7.34.1` / `.2`). Parents on children remain nesting SoT for goals.

---
## 3. Batch-max — compress passes, not meaning

Same ethic as diagram-max: **more meaning per token**, not less meaning.

```
batch-max
  ├─ ONE board row per COMPLETED pass (never per step)
  ├─ fold many deltas into one flow / table
  ├─ idle → wake on local parent/MUR delta · [decision] · [red] · [rule] · [rotation]
  │         (NOT on Belam chat — board is the surface)
  └─ minimize ALL outbound tokens (incl. to owner)
```

### Zero-residue land gate (owner 2026-09-21 — HARD)

```
MUR
  ├─ accept                ──▶ residues=0 ──▶ board complete() allowed
  ├─ accept_with_residue   ──▶ residues>0 ──▶ NO board complete
  │                            directors KEEP looping pi parents
  │                            → MUR → … until residues=0
  └─ reject / format-fail  ──▶ fix → re-MUR (never land)
```

| Signal | Who loops | Belam sees? |
|---|---|---|
| residues > 0 | directors + pi parents | **NO** (board stays in-progress; no daily merge) |
| residues = 0 + format ✓ + §3e suite green | — | YES via **board complete row** (Belam daily pull) |
| blocker / red / decision | — | owner ONLY (not Belam routine) |

**Why:** review exists to burn residues on cheap parents — not to spend Belam/owner tokens on half-done batches.

```
WRONG  MUR accept_with_residue ──▶ message Belam / fake complete
RIGHT  MUR accept_with_residue ──▶ spawn parents ──▶ MUR ──▶ … ──▶ residues=0 ──▶ board complete
```

### Coordination route (owner 2026-09-21 — GRAPH ONLY; supersedes [merge-up] chatter)

**Surface:** `town:core` + `.agi/nodes/.geometry/towns/core.md` (`doc:geometry-towns-core`) — TEMP until g7.34.3.

```
COORD SURFACE (TEMP)  .geometry/towns/core.md  ←→  town:core

DIRECTOR (no Belam chat):
  claim next   → write.py version town/geometry board: claim(goal, seat, tip)
  batch done   → residues=0 + format✓ + §3e suite green → write.py board: complete(goal, tip, suite, mur)
                 also version goal Agent Notes; mark status as fits schema
  claim order  → REOPENED (Prime) first, then open/horizon in bundle order
  talk Belam?  → NEVER for batches. ONLY instant: exposed keys / credential leak
  talk owner?  → credits empty · mesh down · HOLD until owner replies

BELAM (daily, not mid-batch):
  pull town:core + geometry board + closed tips
  merge seat tips w/ residues=0 evidence
  full verify on core/main (or seat as docs say)
  vision-lens on goals · moral-lens on visions↔goals
  residue? → reopen existing OR mint new sub/sub-sub into town bundle (judgment)
  reopen = Prime priority over plain open
```

| Exception | Who | Action |
|---|---|---|
| exposed keys / credential leak / security | Belam **NOW** | instant dm (only Belam exception) |
| credits empty · mesh down | owner ONLY | HOLD work until owner replies |
| routine batch claim/complete | **graph board only** | never Belam chat / never [merge-up] inbox |

```
directors ──▶ graph board: claim / complete (no Belam routine chat)
directors ──▶ owner (Shael): credits empty · mesh down · HOLD; other blockers as needed
Belam     ──▶ daily graph pass (merge · verify · lenses · reopen/mint) — not live merge-up inbox
directors ──▶ loop independently (pi parents) until residues=0; do not wait on Belam mid-loop
```


## 3b. Branch roles (owner 2026-09-21 — graph-board land)

```
Belam (Prime)     ──▶ core/main              (town/main)
                      daily: merge board-complete tips → core/main (+ verify)
director-belam    ──▶ core/season2/main      (town/season2/main)
                      push seat/season2 tip; board complete row (Belam merges daily)
director-helper   ──▶ local worktree ONLY
                      never push a new remote head
                      completed batches → board complete (helper still local-only)
loops             ──▶ merge into core/season2/main then delete loop heads
no season2/loops/* left live as standing remotes
```

Prefer: **directors complete on board + push seat branch; Belam daily merges.**
Keep working batches as-is otherwise. Diagram-max all alignment (on the board).

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
board  write.py claim/complete on town+geometry — NEVER message Belam for batches
routes write·read·send·dispatch/workflow·rotate/spawn
```

ZERO-RESIDUE (HARD)
```
MUR accept              ──▶ residues=0 ──▶ board complete OK (not from this watch)
MUR accept_with_residue ──▶ residues>0 ──▶ NO board complete · KEEP parent loops
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
   Belam  ← NEVER from this watch (board is the surface)
   owner  ← blockers ONLY (red/stuck/decision) · credits empty / mesh down → HOLD
   residues>0 → spawn/continue pi parents (NOT board complete)
   residues=0 + format ✓ + suite → write.py board complete (outside this watch)
4) No delta → silence (no "no change")
5) Never invent. Never new remote head. Never push core/main.
6) Prefer graph routes (§4) over raw tools.
7) Watch still wakes for **local parent loops** — write the board, do not message Belam.
```

**Seat pins (examples — not a second FORMAT):**

```
director-belam
  SCOPE  DT.* · TREE /data/work/agi/.agi/worktrees/seat-director-belam
  BRANCH core/season2/main (WT pin seat/director-belam@s2)
  land   board complete + push season2 tip; Belam daily merges
director-helper
  SCOPE  DH.* · TREE /data/work/agi/.agi/worktrees/seat-director-helper
  BRANCH local-only · never new remote head
  completed batches → board complete (helper stays local-only)
```

### Belam
No standing chatter / merge-up inbox. **Daily graph pass** (not mid-batch): pull `town:core` + geometry board + closed tips → merge residues=0 tips → full verify → vision-lens on goals · moral-lens on visions↔goals → reopen or mint residues into town bundle. Instant exception only: exposed keys / security → Belam NOW.



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

**Why own branches exist:** each director burns the **full verify suite on THEIR branch tip** after a completed batch (residues=0 + format ✓), before **board complete**. That is the point of seat/worktree isolation — not to skip the suite.

```
batch done (residues=0 · format ✓)
  ├─ on THIS seat branch / worktree only
  ├─ FULL verify suite  (engine suite · F7 lock rules still apply)
  ├─ green ──▶ write.py board: complete(goal, tip, suite, mur) + push seat tip
  └─ red   ──▶ fix in-loop · re-suite · never board-complete red
```

| Do | Don't |
|---|---|
| full suite on **your** branch tip after each clean batch | skip suite because "touched tests already ran" |
| one suite window per completed batch (diagram-max on board) | message Belam mid-suite |
| Belam daily merge gates on green suite evidence on board | board complete with suite red or unrun |
| helper: suite on local tip before board complete | push MAIN to "get suite" |

Touched-family pytest at harvest remains for **rounds**. The **batch** gate is the full suite on the branch.

```
round harvest ──▶ touched-family tests
batch close   ──▶ full verify suite on seat branch ──▶ then board complete
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
assigned goal
  → split (mint) MUST stay nested under ASSIGNED goal
  → dispatch pi parents
  → MUR
  → residues? ──yes──▶ format-worthy? ──yes──▶ mint nested goal ──▶ dispatch ──▶ MUR ──┐
       │                      │ keep as residue line                                  │
       │                      └──no───────────────────────────────────────────────────┤
       no (residues=0 + format ✓ + §3e suite)                                         │
       ▼                                                                              │
  whole-batch MUR accept                                                              │
       ▼                                                                              │
  write.py board complete + push seat tip                                             │
       ▼                                                                              │
  Belam daily: merge → verify → lenses                                                │
       ▲                                                                              │
       └──────────────────────── loop until 0 ←───────────────────────────────────────┘
```

Soft ≤7 live parents · `spawn.parallel=1` · no new remote heads.
residue→goal **only** when format-worthy (full Why→Target→Invariants→Falsifier→Out of Scope→Agent Notes).

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

## 4b. Director nested goal authority (owner 2026-09-21 — HARD)

```
Directors continuously nest format-worthy residues as MULTIPLE kids under the yielding goal
  (not one fat same-level sibling).

CLAIM: REOPENED > smallest unclaimed leaf under hot top
  idle: prefer deepen hot top; open second top only when hot has no free leaf

STATUS: claimed/worked=active · rest of town:core bundle=horizon
  maintain status on ALL goals in town:core bundle

NO new g7.N (Belam only) · self-coord via geometry board
```



## 4c. ALL posts — harness mirrors ← graph SoT only (owner 2026-09-21 — HARD)

```
ALL posts (Prime · directors · future): harness mirrors ← graph SoT only
Grok seed = install grok-internals-sync + mint/link per-post *-grok-internals
Claude/pi path same principle; grok leans on bot tools until engine owns it
Graph builds itself

SINGLE-FILE RECIPE (owner 2026-09-21):
  doc:grok-harness-internals-sync  = THE ONE SECTION:ROUTINE_SYNC SoT
  per-post *-grok-internals        = PROFILE (differs) + optional ROUTINE_WATCH (separate)
  grok-internals-sync routine      = pulls recipe ONLY from harness doc
  live-parents-workflows           = DIFFERENT routine (watch) — NEVER paste into sync

per-post SoT     PROFILE (differs) + optional ROUTINE_WATCH (separate) — NO ROUTINE_SYNC body
shared recipe    doc:grok-harness-internals-sync = ROUTINE_SYNC SoT (only place)
grok-internals-sync routine bytes = IDENTICAL all grok posts (from harness)
  NAME / title  grok-internals-sync   (exact — copy identically)
  schedule      */30 * * * *          (copy identically)
  prompt        harness fence body    (copy identically)
live-parents-workflows = DIFFERENT routine (watch)

Pointers:
  Belam/Prime ──▶ doc:belam-grok-internals   (PROFILE + pointer)
  directors   ──▶ doc:director-grok-internals (PROFILE + WATCH + pointer)
  recipe      ──▶ doc:grok-harness-internals-sync  (THE ONE ROUTINE_SYNC file)

Belam/Prime ──▶ write.py graph SoT only (never hand-edit harness mirrors)
Directors   ──▶ */30 sync: pull harness ROUTINE_SYNC + per-post PROFILE → replace placeholders
Routine MAY update_state the same routine that fired (self-rewrite OK from harness doc).

HARD Belam rule diagram-max:
Belam / Prime modify ANY post spine ONLY by editing graph SoT
  (per-post *-grok-internals + this standing + harness recipe)
NEVER hand-edit Grok Bot profile / routines / standing mirrors
*/30 sync applies SoT → bots
Harness offload: grok-bot tools temporary bridge until graph engine drives seats
  (same path as Claude/pi — each harness widens graph compat; graph builds itself)

After ANY graph SoT land → push tips + sync LOCAL
  seat-director-belam · seat-director-helper to tip
  (ff-only / merge keep WIP; local HEAD must show SoT; no ping)
  Detail: doc:belam-grok-internals PROFILE §GRAPH SoT LAND
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
  → suite green ──▶ write.py board complete(goal, tip, suite, mur) + push seat tip
  → Belam daily ──▶ merge board-complete tips · verify · lenses · reopen/mint
  → residues>0 OR format ✗ OR suite red ──▶ parents/fix loop (NO board complete)
```

**Land gates (all required):**
1. Goal body passes §6 format (else format residue → re-MUR).
2. **Residues = 0** (else keep looping — never board complete).
3. **Full verify suite green on the seat branch** (§3e).

`accept_with_residue` is a **continue signal**, not a land signal.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
§4c pointer: after graph SoT land → push tips + sync LOCAL seat-director-belam/helper; detail in doc:belam-grok-internals PROFILE §GRAPH SoT LAND
<!-- THOUGHT:END -->
