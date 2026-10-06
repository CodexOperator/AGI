# Council design — goal:g7.16.1.11.11.2.1 (retire live send.py / thin-native-box-only)

**Lens:** all-is-one + alive · **Pen:** self-perpetuating  
**Leaf mint:** `e690d994fd604963819f1589c49eafe7` · parent `goal:g7.16.1.11.11.2` · **REOPEN already on tip `552024994`** (Belam; was complete under gate-s KEEP-SHIM) — SM adopts blob, does not re-reopen  
**Belam reopen tip (SoT):** `552024994` · **Prior SM PASS (superseded lean):** tip `aabb58c2f` / content `278abffe7` KEEP-SHIM complete  
**Land tip `4d5ba094c` OUT OF SCOPE** · season3 `4b8f28b5e` · capsule `fda4efd6e`  
**Trunk:** `core/season2/et-grok-pilot` · posts/sanctuary-master

**Independent measure (host SM wt, 2026-10-06 ~17:25 ET):**

| object | measured |
|---|---|
| goal node (pre-reopen tip) | status was `complete` keep-shim; mint_id `e690d994fd604963819f1589c49eafe7`; parent `goal:g7.16.1.11.11.2` |
| live `extensions/agi/bin/send.py` | **27 lines / 1029 bytes** — AA1 shim → deprecated (still present; **to be MOVE-retired**) |
| deprecated `extensions/agi/deprecated/bin/send.py` | **6515 lines / 317788 bytes** — **PRESENT** (never git rm; **STAYS**) |
| Team mail SoT | **`box` only** — not send.py |
| Related OOS | gate-r · bin-suite-fresh · g5.34.6.4 — **do not mix** |

## OWNER GO (2026-10-06 ~17:23 ET via plan-master), verbatim

> Retire live send.py — box only. Owner overruled keep-shim on g7.16.1.11.11.2.1. Route amend/reopen through usual loop: live bin shim gone; box SoT only; deprecated copy stays (never git rm).

Gate-s RULING already named **C2** thin-native-box-only on explicit SM flip + falsifier. Owner GO = that flip through **council amend/reopen** (not silent SM restamp).

## Disposition (ONE path — binding lean = C2)

### C2 · Binding = thin-native-box-only / RETIRE live bin shim (ACCEPT — OWNER GO)

1. **MOVE** (never git rm) live `extensions/agi/bin/send.py` out of the live bin path — after SM PASS + DG release only.
2. Deprecated bytes **STAY** under `extensions/agi/deprecated/bin/send.py` — **never git rm**.
3. Team SoT mail = **`box` only**; no second mail primitive; prefer box stdin (g5.34.6.4 is a different residue — do not conflate).
4. Optional post-MOVE stub at live path (if any) must **fail closed** pointing to `box` — not load deprecated as a second mail path.
5. Claim language after COMPLETE: live bin shim **gone** (absent or fail-closed stub); SoT=`box`; deprecated archival PRESENT.

### C1 · Prior keep-shim (SUPERSEDED)

Gate-s PASS keep-shim @ `278abffe7` is **overruled** by OWNER GO. Do not re-assert keep-shim as standing path for this amend.

### C3 · Other (named)

Any other disposition must name: (a) what the live path becomes, (b) where deprecated bytes live, (c) falsifier evidence, (d) that SoT mail stays `box`, (e) that OWNER GO retire is honored or explicitly RETURNED with reason.

### C4 · Falsifier (ACCEPT)

1. Leaf **active** under `g7.16.1.11.11.2`; SM/council artifact cites **thin-native-box-only / RETIRE live bin shim (C2)** with OWNER GO.
2. After BUILD (post SM PASS + DG): live path **absent** OR stub that **fails closed** pointing to `box`; deprecated path **PRESENT**; SoT=`box`.
3. **Never git rm** live or deprecated (MOVE/aside only for live; deprecated stays).
4. Negative: silent SM-only restamp without council; keep-shim re-asserted against OWNER GO; `git rm`; expand send.py as SoT; Belam wake from this package; DG BUILD/MOVE before SM PASS; conflate gate-r / bin-suite-fresh / g5.34.6.4; strip pytest; duplicate mint; season3/capsule/Master touch; write.py; re-land `4d5ba094c`.

### C5 · Loop-only · DG held · writer (ACCEPT)

```
council design → SM gate → BUILD/MOVE only if SM PASS names change → climb/MUR → council → land
```

- **DG held now.** This package does **not** MOVE files or start BUILD.
- Writer: **Write/Edit + agi-turn** — **never write.py**.
- **No Belam box.** Land tip `4d5ba094c` OOS. Gate-r / bin-suite-fresh / g5.34.6.4 OOS.

## Out of scope

g5.34.6.4 hang · gate-r N1–N4 · bin-suite-fresh · Belam land/implement · suite waive · season3/capsule/Master · re-land `4d5ba094c` · strip pytest · git rm · invent heads · expand send.py as SoT mail · duplicate mint · silent SM restamp
