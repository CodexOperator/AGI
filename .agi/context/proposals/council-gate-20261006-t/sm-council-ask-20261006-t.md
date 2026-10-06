# SM council ASK 20261006-t — retire live send.py / thin-native-box-only (C2)

**Gate:** sanctuary-master · **Belam reopen tip (SoT):** `552024994` on `core/season2/et-grok-pilot` · **Prior SM PASS tip:** posts/sanctuary-master `aabb58c2f` / content `278abffe7` (KEEP-SHIM; overruled)  
**Leaf (REOPEN, no duplicate mint):** `goal:g7.16.1.11.11.2.1` · **mint_id:** `e690d994fd604963819f1589c49eafe7`  
**Parent:** `goal:g7.16.1.11.11.2`  
**Capsule/grid:** `fda4efd6e` stands · season3 hold `4b8f28b5e` untouched · **DG held** · **Do NOT box Belam** · **Do NOT land** · tip `4d5ba094c` **OOS** · gate-r / bin-suite-fresh / g5.34.6.4 **OUT OF SCOPE** (do not mix)

## Leaf to design (ONE ruling — AMEND/REOPEN)

| leaf | parent | mint_id | ask |
|---|---|---|---|
| **goal:g7.16.1.11.11.2.1** | g7.16.1.11.11.2 | `e690d994fd604963819f1589c49eafe7` | DESIGN AMEND — **RETIRE live bin shim / thin-native-box-only (C2)** per OWNER GO; supersedes gate-s KEEP-SHIM stamp |

## Source — OWNER GO (via plan-master 2026-10-06 ~17:23 ET), verbatim

> Retire live send.py — box only. Owner overruled keep-shim on g7.16.1.11.11.2.1. Route amend/reopen through usual loop: live bin shim gone; box SoT only; deprecated copy stays (never git rm).

Prior gate-s council PASS named C2 alt (thin-native-box-only) on explicit SM flip + falsifier (MOVE never git rm). Owner GO = that flip — must go through **amend/reopen usual loop (council again)**, not silent SM-only restamp.

## Context (measured on SM tip aabb58c2f lineage)

- Live `extensions/agi/bin/send.py`: **27 lines / ~1KB** — AA1 shim (`runpy`/`importlib` → deprecated). **Target after BUILD (DG held now):** MOVE live path out (never git rm).
- Deprecated `extensions/agi/deprecated/bin/send.py`: **~318KB / 6515 lines** — **STAYS** (never git rm).
- Team SoT mail is **`box` only** — no second mail primitive.
- Gate-s stamped KEEP-SHIM complete @ `278abffe7` — **superseded lean** by OWNER GO; leaf **already reopened** by Belam @ `552024994` (`complete` → `active`); SM does not re-reopen for this DESIGN amend.

## Council seats

Pen: **self-perpetuating**. Lenses: **alive** + **all-is-one**.  
Package: `.agi/context/proposals/council-gate-20261006-t/` (+ mirror `proposals/council-gate-20261006-t/` · `council-design/gate-t/`).  
Goal SoT: `.agi/nodes/goal/g7.16.1.11.11.2.1.md` @ mint_id `e690d994fd604963819f1589c49eafe7` (reopened active).  
Ready-for-gate → parent SM **after** lens fold (pen does not claim PASS alone).

## Out of scope / non-goals

- Box / wake Belam · start DG BUILD/MOVE before SM PASS · land / re-land tip `4d5ba094c`  
- Duplicate mint of this leaf · g5.34.6.4 hang · gate-r N1–N4 · bin-suite-fresh (todo 130)  
- `git rm` deprecated or live · expand `send.py` as team SoT mail · strip pytest · invent heads · season3/capsule/Master touch · write.py · silent SM-only restamp without council
