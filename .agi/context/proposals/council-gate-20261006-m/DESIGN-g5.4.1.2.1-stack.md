# Council design — goal:g5.4.1.2.1 (vertical grid stack/archive — refresh; NO --apply)

**Lens:** all-is-one · **Pen:** self-perpetuating · **Sibling lens:** alive  
**Leaf mint:** `0235a7a317b743edb3b20a0318a629b1` · SM tip `db3597c32` · Belam mint tip `501144233` (goal also on et-grok-pilot HEAD)  
**Why refresh:** prior SM Design GO @ `bb5a6f3ce` never landed a council RULING — re-queue.  
**Explicit:** **NO `--apply` / no live rollover** under this leaf. Capsule `fda4efd6e` stands · season3 hold `4b8f28b5e` · **DG held** · **No Belam box**.

## Owner 8-point stacking intent (verbatim — must-carry)

1. **Hard-move / hard reset:** chains are moved completely off the season tip — "technically gets deleted" from tip view, but if stat mechanics walk the **grid itself as the graph** (not the overall tip graph), stats do not break.
2. **mint_id is the true link:** other links are filesystem pointers (or town:core board). Collaboration tracking confirmed on town:core.
3. **Stay deprecated** after stack; retire later if that makes more sense.
4. **Bake metrics into the stack node** so they can be read instantly after the fact (ties goal:g5.36 / config:metrics; deprecated COUNT; retired do not).
5. **Collapse stacks into overview nodes** for the season — overviews become the **archive** of previous season activity, carrying all relevant **payload refs** rendered cleanly; the rest of the graph is walked inside that overview node's graph slice.
6. **`core/season2/main` archived as a trunk under `core/main`** (design the cut; executing needs separate owner GO with Shael/plan-master).
7. **No node lost.** Never git rm mint identity.
8. **NO rollover run** under this leaf / under g5.4.1.2 — design PASS only.

## Vertical grid stacking procedure (enough for later DG)

### A. Per-node grid branches (D2 identity)

- Each stacked node keeps durable identity at `refs/grid/<trunk>/node/<mint_id>` (grid.py D2). Tip branch may stop listing the chain; **grid tip blobs remain**.
- Writer: existing `grid.py commit` / `update-ref` CAS per mint — never invent a second mover; never `git rm` node files as identity loss.
- Stats / walkers that today read tip-only must gain a **grid-as-graph** path (walk `refs/grid/<trunk>/node/*` + frontmatter parents) so hard-move does not zero counts.

### B. Hard-move off tip

1. Select season chains to stack (from season overview goal / mint list — DG names selector at build time).
2. Ensure each mint has a current grid tip blob (`grid.py commit` / already on D2).
3. Remove (or stop projecting) those node paths from the **season tip tree** so tip view no longer lists them — hard-move, not soft hide. Prefer engine Write + agi-turn status/`parents` edits that stop tip inclusion; do **not** delete blobs from object store.
4. Set stacked nodes `status: deprecated` (stay deprecated; do not retire-by-default).
5. Falsifier fragment: tip `git ls-tree -r <season-tip> .agi/nodes` no longer contains stacked paths; `git cat-file -t $(git rev-parse refs/grid/<trunk>/node/<mint>)` still blob; mint_id still greppable on grid.

### C. Bake metrics into the stack / overview node (align g5.36.1)

Per `/workspace/council-design/g5.36.1-metrics.md`:
- Defs live in **`config:metrics`** (`.agi/nodes/.geometry/metrics.md`); thin compute emits `METRIC k=v`.
- **deprecated COUNT · retired DO NOT** (frontmatter status, folder-blind).
- Each overview/stack node body carries a short **baked snapshot** block written at stack time, e.g.:
  ```
  ### stack-metrics @ <trunk-short> <ISO-date>
  METRIC scored_node_count=…
  METRIC deprecated_node_count=…
  METRIC retired_count=…
  METRIC outcome_coverage=…
  ```
  Values come from the same thin METRIC emitter (reuse; no second formula layer). Snapshot is documentary; live recompute still walks config:metrics.

### D. Overview archive shape + walkable slice (ties g5.4.1.3.1)

Per `/workspace/council-design/g5.4.1.3.1/g5.4.1.3.1-slice-capsule.md` §4:
1. `slice pack season-<N>-archive --root <season-overview-goal>` (or `--mint` list from stack plan) captures walkable season slice + payload refs as manifest lines.
2. Overview node body gains `slice_ref: refs/slice/season-<N>-archive` (payload refs rendered cleanly; rest of graph walked inside that slice).
3. Grid-as-graph stats keep working via `refs/grid/...`; tip view drops stacked chains.
4. **This leaf does not call** `slice pack`, rollover, or `--apply` — sequence is named for a later DG leaf.

Overview node (shape for DG):
```
id: goal:… / overview:season-<N>-archive
mint_id: <durable>
status: deprecated   # or complete if owner prefers; never retired-by-default under this leaf
slice_ref: refs/slice/season-<N>-archive
payload_refs:          # clean list of archived payload paths / mint_ids
  - mint:<id> path:<optional>
### stack-metrics …
```

### E. `core/season2/main` → trunk under `core/main` (design only)

| step | design binding | execute? |
|---|---|---|
| 1 | Treat `core/season2/main` as an archived trunk named under `core/main` (e.g. `core/main` retains pointer / parent-trunk metadata to season2 tip) | **NO** under this leaf |
| 2 | Separate owner GO with Shael/plan-master required before any ref move | gate outside council |
| 3 | Falsifier when someday executed: season2 tip still reachable; no mint lost; Master not rewritten without GO | n/a now |

## Falsifier (design complete / later land)

1. ONE ruling + this note covers all 8 owner points + vertical procedure A–E + NO-run.
2. Negative for later build: rollover `--apply` invoked; node mint lost / git rm; tip-only metrics with no grid walk; Prime-direct engine; season3 tip moved; capsule reopen.
3. Design-time negative: missing any of the 8 points; inventing metrics outside config:metrics; inventing a second mover beside grid/slice.

## Invariants / NO-run

- **NO `--apply` / no live archive cut / no rollover run** under this leaf.
- Never git rm; mint_id remains durable link.
- Loop: council design → SM gate → (later) DG build → SM MUR → Belam land only. Prime does not build or run rollover.
- Separate from g5.34.8 fan-out / captive-carry; do not reopen g5.4.1.3.2 / g5.34.10.2; do not touch season3 tip `4b8f28b5e`.

## Out of scope

Running rollover · master merge · g5.34.8 pane monitor · inventing metrics outside config:metrics · opening suite window · boxing Belam
