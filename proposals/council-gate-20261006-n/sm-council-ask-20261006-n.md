# SM council ASK 20261006-n — stray origin head deletes DESIGN

**Gate:** sanctuary-master · **SM posts tip:**  (design leaf place)  
**Belam mint tip:** `e7c96fb2e` on `core/season2/et-grok-pilot` (merged into SM posts)  
**Capsule/grid:** `fda4efd6e` stands · season3 hold `4b8f28b5e` untouched (owner reset done — do not touch further) · **No Prime `--delete`** · **No DG deletes yet**  
**Sibling in flight (do not interfere):** DG4 on g5.4.1.1.7.2 (links) + g5.4.1.4.2 (bin-suite under Belam suite grant)

## Leaf to design

| leaf | parent | mint_id | ask |
|---|---|---|---|
| **goal:g5.4.1.5.1** | g5.4.1.5 (`d3d4b1da6d4340f3b0fab318c0a0c154`) | `8fd28a192afe49e9ae483ebc3502fc3f` | DESIGN — delete origin `season2/main` + `belam/capsule-rows` through loop; name DG as delete operator; Prime does not push `--delete` |

## Owner (verbatim)
> Owner GO 2026-10-06 (via plan-master): delete both stray remote heads (unscoped season2/main + belam/capsule-rows) through the standard loop.

## Measured strays (reconfirm before any later delete push)
- `refs/heads/season2/main` @ `b0608a1f32d3fa8668399e58ba7320280565acad` (unscoped — not under `core/`)
- `refs/heads/belam/capsule-rows` @ `1ea2129b51e844f156869e438f69d6b5c3100f75`

## g5.4.1.5.1 — must name in ONE design
1. **Exact refs only** — `refs/heads/season2/main` + `refs/heads/belam/capsule-rows`. Never `core/season2/main`, `core/season3/main`, `core/season2/et-grok-pilot`, `core/main`, or any graph-described trunk.
2. **Delete operator** — **DG** under SM gate performs `git push origin --delete …`. **Prime / Belam will not** `git push --delete` these refs.
3. **Land** — Belam/Prime land verifies falsifier empty only (no delete push on land).
4. **SHA reconfirm** — `git ls-remote` immediately before delete push; STOP/escalate on unexpected drift.
5. **Falsifier** — `git ls-remote origin refs/heads/season2/main refs/heads/belam/capsule-rows` prints empty.
6. **Loop-only** — council design → SM gate → DG ops → climb → council → Belam land. DG held until SM gate.

## Council seats
Pen: **self-perpetuating**. Lenses: **alive** + **all-is-one**.  
Package under `proposals/council-gate-20261006-n/` (and council-design/gate-n/). Ready-for-gate → parent SM.  
**Do NOT box Belam. Do NOT start DG deletes. Do NOT touch season3 tip / Master / capsule fda4efd6e. Do NOT interfere with DG4 suite/links.**

## Non-goals
Prime `--delete` · DG deletes before PASS+SM gate · season3 tip rewrite · Master archive · inventing heads · reopen g5.4.1.1.7 / g5.4.1.4 / g5.4.1.2 · waive-as-footnote · git rm nodes
