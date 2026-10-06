# Council design — goal:g5.4.1.4.8 — spawn-budget lock durable perm

**Leaf mint:** `82d355870dbb45c5a9155b1af5c120fe` · parent `goal:g5.4.1.4.2` · **status:** active (DESIGN)  
**SoT (mint / SM):** `04aedac1d` · climb parent PASS `1617aff10` (**do not reopen**)  
**Pen:** self-perpetuating · **Lenses:** alive (PASS lean) · all-is-one (pending)  
**DG held** · **No Belam box** · suite-stamp ACL `g5.4.1.4.3.*` **adjacent — do not reopen** · gate-t / write-path / land-binsuite **OOS**  
**Capsule** `fda4efd6e` · season3 `4b8f28b5e` · writer: **Write+agi-turn — never write.py** · never strip pytest

## Problem (measured ET 2026-10-06 ~17:53)

| object | measured |
|---|---|
| Canonical path | `.agi/sessions/.spawn-budget/.lock` (via `spawn_budget` → `locations.SESSIONS_DIR_NAME / ".spawn-budget"`) — **not** top-level `/.spawn-budget` |
| dir `.agi/sessions/.spawn-budget` | `belam:belam` **775**; ACL = owner/group/other only — **no** `group:agi` named ACL |
| `.lock` | `belam:belam` **664** empty file; no `group:agi` ACL |
| sessions parent | already has `group:agi:rwx` + **default:** `group:agi:rwx` (gate-q / `.4.3.1` apply) — but `.spawn-budget` predates inherit / lacks named ACL on existing objects |
| DG4 | `test -r .lock` → READ_OK; `open(...,"a")` → **PermissionError** |
| residue | budget check PE during Belam ONE grant verify; non-blocking for bin-suite-fresh |

## Standing path (ONE lean — ACCEPT)

**Preferred A — durable ACL on budget dir + lock + committed policy (ACCEPT lean).** Same class as suite-stamp ACL, **distinct objects** — do not reopen `.4.3.*`.

1. **Host/Belam OS apply once after SM PASS:**
   ```bash
   # from MAIN /data/work/agi
   setfacl -m g:agi:rwx .agi/sessions/.spawn-budget
   setfacl -d -m g:agi:rwx .agi/sessions/.spawn-budget
   setfacl -m g:agi:rw .agi/sessions/.spawn-budget/.lock   # if exists
   ```
2. **Committed policy bytes** (BUILD-named path, e.g. `.agi/context/proposals/spawn-budget-lock-acl-policy-20261006-u.md`) stating required ACL, apply seat = Belam/host, posts must not belam-borrow.
3. **Alt B — explicit labeled skip** for budget when lock unwritable — only on SM/Owner GO; default lean remains A.

### Rejected as sole fix
- Waive footnote on `.4.2`
- DG belam-borrow setfacl
- Reopening `.4.3.*` as the close vehicle (sessions defaults help *new* files; existing `.spawn-budget` still broken — this leaf owns that residue)
- Moving budget dir without named BUILD

### Loop / writer
```
council DESIGN → SM gate → Belam/host ACL apply (+ optional thin BUILD for policy) → climb/MUR → council → land
```
**DG held now.**

## Must-carry
1. As DG4: budget check **PASS** or **documented labeled skip** — no unnamed PE.
2. Policy/skip bytes committed per lean.
3. Do not reopen `.4.3.*` / `.4.2` PASS; do not mix gate-t.
4. Write+agi-turn; never write.py; never git rm; never strip pytest.

## Falsifiers (for later BUILD / land)
1. As DG4: open/append `.agi/sessions/.spawn-budget/.lock` succeeds without setfacl redo **or** labeled skip contract active.
2. `getfacl -p .agi/sessions/.spawn-budget` shows named + default `group:agi:rwx` (lean A); lock shows `group:agi:rw`.
3. Policy/skip bytes on tip.
4. ZERO unnamed PE leftover notes on `.4.2`.
5. **Negative:** belam-borrow from DG; reopen `.4.3`/`.4.2`; write.py; git rm; Belam wake from this DESIGN package; strip pytest; season3/capsule/Master touch.

## Out of scope
Reopen `g5.4.1.4.2` · suite stamp ACL `g5.4.1.4.3.*` · U1/U2 · gate-t · write-path g5.4.1.6 · Belam land from council · invent heads
