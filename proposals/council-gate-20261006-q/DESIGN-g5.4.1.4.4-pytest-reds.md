# Council design — goal:g5.4.1.4.4 (owed pytest reds / missing tests)

**Lens:** all-is-one · **Pen:** self-perpetuating · **Sibling lens:** alive  
**Leaf mint:** `1db4e85eccdc4b8b90bcd168ed37adf3` · parent `goal:g5.4.1.4.2` · SM tip `8d9577fa2` · mint tip `97063c7ed`  
**Independent measure (agi-all-is-one @ `/data/work/agi`, 2026-10-06 ~15:36 ET):**

| object | measured |
|---|---|
| goal node @ `97063c7ed` | status `active`; tags include `design`; mint_id `1db4e85eccdc4b8b90bcd168ed37adf3`; parent `goal:g5.4.1.4.2` |
| posts/sanctuary-master | `8d9577fa2a60675ee4e2907d315fbf3403e479d7` |
| trunk | `932218a0f` OUT OF SCOPE |
| Capsule / season3 | `fda4efd6e` stands · `4b8f28b5e` HOLD |

**Residue inventory (ASK / DG4 measured under ONE suite grant — cited, not re-run; full suite = CPU out of scope for this design):**

| row | kind | count / note | disposition owed |
|---|---|---|---|
| brief | FAIL | 4 | child BUILD **or** explicit retire/skip node + falsifier |
| cli | FAIL | 1 | child BUILD **or** explicit retire/skip node + falsifier |
| geometry_config | FAIL | 3 | child BUILD **or** explicit retire/skip node + falsifier |
| migrate_channel | FAIL | 4 | child BUILD **or** explicit retire/skip node + falsifier |
| rotate | FAIL | 99 | child BUILD **or** explicit retire/skip node + falsifier |
| sensei | FAIL | 4 | child BUILD **or** explicit retire/skip node + falsifier |
| dispatch | PASS owed | — | keep in suite surface; child verify if drift |
| heal | PASS owed | — | keep in suite surface; child verify if drift |
| spawn_budget | PASS owed | — | keep in suite surface; child verify if drift |
| verification | PASS owed | — | keep in suite surface; child verify if drift |
| write | PASS owed | — | keep in suite surface; child verify if drift |
| `test_boxes.py` | MISSING | — | child BUILD restore **or** explicit skip node + falsifier |
| `test_mail_alert.py` | MISSING | mail_alert deprecated — bytes under `extensions/agi/deprecated/` | **retire vs restore designed** (see C2) |

Capsule `fda4efd6e` stands · season3 hold untouched · **DG held** · **No Belam box** · never git rm · **no blanket waive** of bin-suite-fresh.

## Disposition (ONE path — per-row close, never a footnote)

Owner zero-notes: pre-existing reds are **real DESIGN → BUILD/retire leaves**, not MUR footnotes on g5.4.1.4.2.

### C1 · Per-row disposition rule (ACCEPT)

For **each** FAIL and MISSING row above, later SM-gated work must mint **exactly one** of:

1. **Child BUILD** under `goal:g5.4.1.4.4` (or named subleaf) that drives the test(s) green under Prime suite grant; **or**
2. **Explicit retire/skip node** with its own falsifier (what is retired, where bytes live, why suite no longer owes that file/assert).

Never close a row by language on `goal:g5.4.1.4.2` alone. MUR/council cite leaf ids only.

PASS-owed rows (dispatch, heal, spawn_budget, verification, write): remain on the bin-suite surface; if any later go red, open a child under this parent — do not silent-waive.

### C2 · mail_alert — retire vs restore (ACCEPT)

`test_mail_alert.py` is MISSING; mail_alert bytes sit under deprecated/ (prior links leaf g5.4.1.1.7.1 retargeted payload). Design binds:

- **Retire path (default lean — ACCEPT):** explicit retire/skip node stating suite does **not** owe `test_mail_alert.py` while implementation remains deprecated; falsifier = suite inventory + verify surface omit that file **and** retire node active.
- **Restore path (alt):** child BUILD restores test against deprecated or re-homed implementation under separate SM GO — not silent.

**Default lean = retire.** SM may flip to restore at gate; choice must be **explicit** (child node), never a footnote on g5.4.1.4.2.

**rotate(99):** may wave-split into multiple child BUILDs at mint (SM names batches); still one disposition per assert-cluster — never a single waive footnote.

### C3 · bin-suite-fresh stays meaningful (ACCEPT)

- Freshness stamp ≠ suite all-green. Closing reds is **this leaf’s job**.
- **No blanket waive** of failures because freshness PASS.
- Suite grant / window rules from g5.4.1.4.1 / .4.2 still bind (Prime grants; DG operates; lock contract).

### C4 · Falsifier (ACCEPT)

1. Inventory table above **closed**: every FAIL/MISSING row maps to a green test result **or** an active documented retire/skip node with falsifier.
2. MUR/council cite `goal:g5.4.1.4.4` (+ child ids) only — no “pre-existing reds non-blocking” waive language on `.4.2`.
3. `bin-suite-fresh` still enforced independently (sibling ACL leaf `.4.3` owns stamp write durability).
4. Negative: footnote waive; git rm of tests/nodes; season3 tip moved; capsule touched; write.py; Belam boxed; full-suite re-run inventing new counts without SM GO.

### C5 · Loop-only · DG held · writer (ACCEPT)

```
council design → SM gate → DG child BUILD/retire wave(s) → climb/MUR → council → land
```

- **DG held now.** No pytest edits from this package.
- Writer: **engine.v4 Write/Edit + agi-turn** — **never write.py**.
- **No Belam box. No land.** Trunk `932218a0f` OUT OF SCOPE.
- Do not touch season3 `4b8f28b5e` / Master / capsule `fda4efd6e`.

## Out of scope

ACL stamp (→ g5.4.1.4.3) · push auth (→ g5.4.1.5.3) · write-path g5.4.1.6 · running full suite from council · Belam wake · inventing heads · git rm · reopen g5.4.1.4.2 as waive vehicle

## AMEND 2026-10-06-q — OWNER pin (pytest ALLOWED)

**OWNER (via plan-master; Belam confirmed), verbatim:** pytest/Python test scripts are ALLOWED (convenience + logging). Fix/waive real reds only — do NOT design toward stripping pytest or Python tests.

**Belam confirm:** pytest = runner not ban on Python; fix/waive real failures; do NOT remove Python tests as the fix. **Prime: no build / no strip.**

Binding on C1–C5: per-row BUILD (green) or explicit named-row waive/skip with falsifier — never close by deleting the pytest runner or mass-removing Python tests. mail_alert retire lean is row-scoped only. See .

