# Council design — goal:g5.4.1.5.1 (stray origin head deletes)

**Lens:** all-is-one · **Pen:** self-perpetuating · **Sibling lens:** alive  
**Leaf mint:** `8fd28a192afe49e9ae483ebc3502fc3f` · parent g5.4.1.5 · ASK tip `85c3924af` · Belam mint tip `e7c96fb2e`  
**Independent measure (agi @ `/data/work/agi`, `git ls-remote origin`, 2026-10-06):**

| ref | SHA (reconfirmed) |
|---|---|
| `refs/heads/season2/main` | `b0608a1f32d3fa8668399e58ba7320280565acad` |
| `refs/heads/belam/capsule-rows` | `1ea2129b51e844f156869e438f69d6b5c3100f75` |
| `refs/heads/core/season3/main` (HOLD — do not touch) | `4b8f28b5e16373dd4de6b58e25f099deed4a48f1` |

Capsule/grid `fda4efd6e` stands · season3 hold untouched · **DG held** · **No Belam box** · never git rm · never invent heads.

## Disposition (ONE path — two stray deletes through the loop)

Owner GO 2026-10-06 (via plan-master): delete both stray remote heads through the **standard loop**. Prime will **NOT** `git push --delete`.

### Exact refs only
Delete **only** these two on origin:
1. `refs/heads/season2/main` (unscoped — not under `core/`)
2. `refs/heads/belam/capsule-rows`

**Never** delete or rewrite: `core/season2/main`, `core/season3/main`, `core/season2/et-grok-pilot`, `core/main`, Master, capsule/grid `fda4efd6e`, or any other graph-described trunk.

### Delete operator
- **DG** (assignee named at SM gate) performs the delete under SM gate:
  - `git push origin --delete season2/main belam/capsule-rows`
  - **or** two single-ref deletes: `git push origin --delete season2/main` then `git push origin --delete belam/capsule-rows`
- **Prime / Belam do not** `git push --delete` these refs (no side door).
- **DG held** until parent SM gate stamps. This design does **not** start DG.

### SHA reconfirm (build-time gate)
Immediately before the delete push, DG must re-run:
```
git ls-remote origin refs/heads/season2/main refs/heads/belam/capsule-rows
```
- Expected tips: `b0608a1f…` / `1ea2129b…` (or still the same two ref names if tip moved only within that stray).
- If either ref is **already gone** → skip that ref (idempotent).
- If tip moved to an **unexpected** value without SM re-GO → **STOP / escalate**; refuse delete. Do not invent heads.

### Belam land = falsifier only
After climb + MUR + council PASS, Belam/Prime **land** verifies empty falsifier only. Land does **not** re-run the delete push.

### Falsifier
```
git ls-remote origin refs/heads/season2/main refs/heads/belam/capsule-rows
```
prints **empty** (no lines) for both. Negative: either stray still present; delete of a graph-described trunk; Prime `--delete` without loop; season3 tip moved; Master touched; inventing heads.

### Loop-only
```
council design → SM gate → DG delete-ops → climb/MUR → council → Belam land (falsifier)
```
No Prime-direct `--delete`. No council-started DG deletes from this leaf.

## Concurrent work (do not interfere)
- DG4 links/suite leaves: g5.4.1.1.7.1 / g5.4.1.4.1 (and any .2 follow-ons) — **out of scope**; do not wake, block, or share suite window.
- Season3 tip `4b8f28b5e` — hold only.
- Capsule `fda4efd6e` — stands.

## Invariants / NO-run now
- Never `git rm` nodes; Master untouched; season3 hold tip untouched.
- Stray deletes go through the loop only.
- Do not box Belam from council.
- Do not start DG deletes from this design package.
- Do not touch season3 / Master / capsule / DG4 links/suite.

## Out of scope
goal:g5.4.1.1.7* · goal:g5.4.1.4* · goal:g5.4.1.2* · season rollover · Master archive · inventing heads · advancing/rewriting season3 · Prime `--delete` · DG deletes before PASS+SM gate
