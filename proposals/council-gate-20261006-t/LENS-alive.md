# LENS alive — gate-t DESIGN (retire live send.py / thin-native-box-only C2)

**Verdict:** **PASS lean** · 2026-10-06 ~17:29 ET · **measured on ET** (read-only) · **box tip:** `9f740dbd1`
**Against:** Belam reopen tip `552024994` (`5520249948dd12d334f11efa5178895b0c40d9aa`) / SM tip `31f34d1e2` (`31f34d1e2ce8f2c2c6fb2e89bf01e6a4123a2f79`)
**Prior KEEP-SHIM (superseded):** SM `aabb58c2f` / content `278abffe7` — **overruled** by OWNER GO; do not re-assert
**Package:** `proposals/council-gate-20261006-t/` (+ SM `.agi/context/proposals/council-gate-20261006-t/`) · Pen=self-perpetuating · lenses=alive+aio
**Leaf:** `goal:g7.16.1.11.11.2.1` · mint_id `e690d994fd604963819f1589c49eafe7` · parent `goal:g7.16.1.11.11.2` · **REOPEN active** (complete→active @ Belam)
**Land tip `4d5ba094c` OUT OF SCOPE** · gate-r / bin-suite-fresh / g5.34.6.4 **OOS** · DESIGN-ONLY · DG held · **No Belam** · write.py banned · season3/capsule untouched · **never git rm** · SoT mail=**box** · binding lean=**C2 thin-native-box-only / RETIRE live bin shim**

## Byte facts

| # | claim | measured | YES/NO |
|---|---|---|---|
| 1a | Leaf @ Belam reopen tip | `.agi/nodes/goal/g7.16.1.11.11.2.1.md` PRESENT @ `552024994`; subject = Owner GO reopen retire live send.py shim (DESIGN; no footnotes); blob `df35eeafc…` | **YES** |
| 1b | Leaf @ SM tip | Same path PRESENT @ `31f34d1e2`; blob **identical** `df35eeafc…` — SM adopted reopen | **YES** |
| 1c | mint_id + status + design tags | mint_id `e690d994fd604963819f1589c49eafe7`; `status: active` (reopened); tags include `aa1` + `send` + `shim` + `design` + `retire` | **YES** |
| 1d | parent match | `parents: [goal:g7.16.1.11.11.2]` on Belam and SM | **YES** |
| 2a | Parent `g7.16.1.11.11.2` exists | PRESENT @ Belam; `status: horizon`; title AA1 box KEEP / send.py MOVE never git rm; mint_id `61c6f5d89a28462897cad192b280526b` | **YES** |
| 3a | Live `extensions/agi/bin/send.py` still present (pre-MOVE) | **27 lines / 1029 bytes** @ Belam and SM (blob `f30763b44…` identical) — expected until SM PASS+DG MOVE | **YES** |
| 3b | Docstring AA1 shim | Line 2: `"""Shim — AA1 MOVE: real module is extensions/agi/deprecated/bin/send.py (never git rm)."""` | **YES** |
| 3c | Loader to deprecated | `_PATH = …/deprecated/bin/send.py`; `__main__` → `runpy.run_path`; import path → `importlib.util.spec_from_file_location` + `exec_module` | **YES** |
| 4 | Deprecated present (STAYS) | `extensions/agi/deprecated/bin/send.py` PRESENT · **6515 lines / 317788 bytes** (blob `d2cac7501…` identical Belam/SM) — **never git rm** | **YES** |
| 5 | Team SoT mail = box | Leaf + DESIGN package: SoT mail = **`box` only**; no second mail primitive; live shim not expanded as handoff SoT | **YES** |
| 6a | season3 pin | `core/season3/main` = `4b8f28b5e16373dd4de6b58e25f099deed4a48f1` | **YES** |
| 6b | capsule pin | `fda4efd6e4bd649f3b436d0aaa0c77c9975ba106` resolves; ⊂ Belam tip `552024994` | **YES** |
| 6c | No Belam land of this DESIGN package | Belam tip holds reopen leaf only; gate-t package **absent** under Belam tree; SM tip holds ASK+DESIGN+DRAFT under `.agi/context/proposals/council-gate-20261006-t/` | **YES** |
| 6d | land tip OOS | `4d5ba094c` (`4d5ba094c85ada7661af3f8fb85e728a2338549a`) resolves; ⊂ Belam tip; **not** this gate's land vote | **YES** (info) |
| 7 | SM package on tip | ASK + DESIGN-batch + DESIGN-g7.16.1.11.11.2.1-retire-send + DRAFT-RULING present @ `31f34d1e2` | **YES** |
| 8 | box tip `9f740dbd1` (optional) | Resolves (`9f740dbd1ea22b5a1e261a2d4fb580471289ef46`) — SM-cited alive box tip | **YES** (info) |

### Live shim (quoted, Belam = SM; still present pre-MOVE — expected)

```python
#!/usr/bin/env python3
"""Shim — AA1 MOVE: real module is extensions/agi/deprecated/bin/send.py (never git rm)."""
...
_PATH = _BIN.parent / "deprecated" / "bin" / "send.py"
...
if __name__ == "__main__":
    import runpy
    raise SystemExit(runpy.run_path(str(_PATH), run_name="__main__"))
_spec = importlib.util.spec_from_file_location("_agi_send_deprecated", _PATH)
...
```

## Cuts for ONE design

### C1 — keep-shim (SUPERSEDED)
Gate-s PASS keep-shim @ `278abffe7` / SM `aabb58c2f` is **overruled** by OWNER GO. **Do not re-assert** keep-shim as standing path for this amend/reopen.

### C2 — thin-native-box-only / RETIRE live bin shim (ACCEPT — binding / OWNER GO)
**Leaf `g7.16.1.11.11.2.1`** — lean **C2**. OWNER GO (verbatim): retire live send.py — box only; live bin shim gone; box SoT only; deprecated stays (never git rm).

1. After SM PASS + DG: **MOVE** (never git rm) live `extensions/agi/bin/send.py` out of the live bin path.
2. Deprecated bytes **STAY** under `extensions/agi/deprecated/bin/send.py` — **never git rm**.
3. Team SoT mail = **`box` only**; no second mail primitive.
4. Optional post-MOVE stub at live path (if any) must **fail closed** pointing to `box` — not load deprecated as a second mail path.
5. Supersedes gate-s keep-shim. Pre-MOVE presence of the thin AA1 shim (27 lines / 1029 B) is **expected** now; DG held.

### C3 — Writer / posture (ACCEPT)
Writer = Write/Edit + `agi-turn` — **never write.py**. **DG held.** **No Belam box** from this package. Land tip `4d5ba094c` OOS. Gate-r / bin-suite-fresh / g5.34.6.4 OOS — do not mix. Do **not** touch season3 `4b8f28b5e` / capsule `fda4efd6e`. Do **not** duplicate mint (`e690d994…` / Belam reopen `552024994` stands). No silent SM-only restamp without council.

### C4 — Falsifier (ACCEPT)
1. Leaf **active** under `g7.16.1.11.11.2` with mint_id above; SM/council artifact cites **thin-native-box-only / RETIRE live bin shim (C2)** with OWNER GO.
2. After BUILD (post SM PASS + DG): live path **absent** OR stub that **fails closed** → `box`; deprecated path **PRESENT**; SoT=`box`.
3. **Never git rm** live or deprecated (MOVE/aside only for live; deprecated stays).
4. Negative: silent SM-only restamp without council; keep-shim re-asserted against OWNER GO; `git rm`; expand send.py as SoT; Belam wake from this package; DG BUILD/MOVE before SM PASS; conflate gate-r / bin-suite-fresh / g5.34.6.4; strip pytest; duplicate mint; season3/capsule/Master touch; write.py; re-land `4d5ba094c`.

## Holes (RETURN)

*(none)*

## Verdict for pen

**PASS lean** — C2 thin-native-box-only / RETIRE live bin shim (OWNER GO binding) · C1 keep-shim SUPERSEDED · C3–C4 posture/falsifier. Leaf reopened **active** @ Belam `552024994` with mint_id `e690d994…`; SM `31f34d1e2` adopted identical leaf blob; live AA1 shim still present pre-MOVE (expected); deprecated PRESENT; SoT mail=box; season3/capsule pins hold; no hard invariant fail.

Ready-for-gate → SM **after** SP folds ONE RULING. Do not start DG. Do not box Belam. Land `4d5ba094c` stays OOS. Gate-r / bin-suite-fresh / g5.34.6.4 stay OOS. Never git rm.
