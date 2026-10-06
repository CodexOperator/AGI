# Council design — goal:g5.4.1.4.7 — MAIN .env durable perm (smoke/anonymize)

**Leaf mint:** `433ab7c8a8b54af48d024af9e4f94db4` · parent `goal:g5.4.1.4.2` · **status:** active (DESIGN)  
**SoT (mint / SM):** `04aedac1d` · climb parent PASS `1617aff10` (**do not reopen**)  
**Pen:** self-perpetuating · **Lenses:** alive (PASS lean) · all-is-one (pending)  
**DG held** · **No Belam box** · suite-stamp ACL `g5.4.1.4.3.*` **adjacent — do not reopen** · gate-t / write-path / land-binsuite **OOS**  
**Capsule** `fda4efd6e` · season3 `4b8f28b5e` · writer: **Write+agi-turn — never write.py** · never strip pytest

## Problem (measured ET 2026-10-06 ~17:53)

| object | measured |
|---|---|
| Path | MAIN `/data/work/agi/.env` |
| ownership / mode | `belam:belam` **600** (`user::rw-`, `group::---`, `other::---`) — **no** `group:agi` ACL |
| DG4 (`agi` member, not belam) | `test -r .env` → **READ_FAIL** |
| residue | smoke + anonymize hit `PermissionError` during Belam ONE grant verify; **non-blocking** for bin-suite-fresh falsifier |
| anonymize path | `envfile.read_env(envfile.resolve(root).env_file)` — needs readable `.env` (or fixture) |

## Standing path (ONE lean — ACCEPT)

**Preferred A — durable read ACL + committed policy (ACCEPT lean).**

1. **Host/Belam OS apply once after SM PASS** (not DG invent; not forever one-off):
   ```bash
   # from MAIN root /data/work/agi — READ for agi posts; write stays belam-only
   setfacl -m g:agi:r-- .env
   # optional: keep owner write exclusive; do not grant group write
   ```
2. **Committed policy bytes** (path named at BUILD, e.g. `.agi/context/proposals/env-acl-policy-20261006-u.md` or sibling under proposals) stating:
   - path: MAIN `.env` (resolved via envfile)
   - required: `group:agi:r` (read); write remains owner/belam
   - apply seat: **Belam/host OS**
   - posts must not need belam OS borrow / sudo for smoke+anonymize read
3. **Alt B — explicit soft-skip** (only if SM/Owner forbids broadening `.env` read): verification/anonymize/smoke emit a **named labeled skip** residue id (cite this leaf) — never raw unnamed `PermissionError`. Soft-skip requires its own falsifier wording at SM gate; **default lean remains A**.

### Rejected as sole fix
- Permanent waive / leftover note on `.4.2`
- DG4 `sudo -u belam` / credential borrow to chmod
- Reopening suite-stamp ACL leaf `g5.4.1.4.3.*` as the vehicle (different path; sessions defaults already applied — do not conflate)
- Granting world-readable `.env`

### Loop / writer
```
council DESIGN → SM gate → Belam/host ACL apply (+ optional thin BUILD for policy doc) → climb/MUR → council → land
```
**DG held now.** No setfacl from this package.

## Must-carry
1. As DG4 uid: smoke + anonymize either **PASS** or **documented labeled skip** — no unnamed PermissionError.
2. Policy bytes committed if lean A; skip contract explicit if lean B.
3. Do not mix `g5.4.1.4.3.*` reopen; do not reopen `.4.2` PASS.
4. Write+agi-turn; never write.py; never git rm; never strip pytest.

## Falsifiers (for later BUILD / land)
1. As DG4 (in `agi`, not belam): `test -r /data/work/agi/.env` succeeds **or** skip path documented and exercised without raw PE leakage.
2. `getfacl -p .env` shows `group:agi:r--` (lean A) **or** SM-recorded skip contract active (lean B).
3. Policy/skip bytes present on cited tip.
4. ZERO leftover unnamed PE notes on `.4.2`.
5. **Negative:** world-readable secrets; belam-borrow chmod from DG; reopen `.4.3` / `.4.2`; write.py; git rm; Belam wake from this DESIGN package; strip pytest; season3/capsule/Master touch.

## Out of scope
Reopen `g5.4.1.4.2` · suite stamp ACL `g5.4.1.4.3.*` · U1/U3 · gate-t · write-path g5.4.1.6 · Belam land from council · invent heads
