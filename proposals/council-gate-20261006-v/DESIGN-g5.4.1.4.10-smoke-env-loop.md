# Council design — goal:g5.4.1.4.10 — smoke .env 640 + loop.log Permission denied

**Leaf mint:** `c538491cc5f84b89a29e838226bad3d2` · parent `goal:g5.4.1.4` · **status:** active (DESIGN)  
**Prime mint tip:** `2c9172e68` · **Live trunk:** `ce34b336b` · U2 `g5.4.1.4.7` COMPLETE (ACL lean A) — **do not reopen / do not strip ACL**  
**Pen:** self-perpetuating · **Lenses:** alive + all-is-one (pending)  
**DG held** · **No Belam box** · season3 `4b8f28b5e` · capsule `fda4efd6e`  
**Writer:** Write+agi-turn — never write.py

## Problem (measured)

| object | measured |
|---|---|
| MAIN `.env` after U2 ACL lean A | effective mode **640** with `group:agi:r--`; smoke still expects **600** → unnamed fail note |
| `.agi/loop.log` | **Permission denied** for agi-belam during verify smoke |
| U2 `g5.4.1.4.7` | COMPLETE — ACL applied; **keep lean A** |

## Standing path (ONE lean — ACCEPT)

**Reconcile smoke expect-600 with durable ACL lean A** (keep `group:agi:r--`; adjust expect and/or document labeled soft-skip — **not** strip ACL). **Close loop.log PE** with durable path (readable or labeled skip for agi-belam during verify smoke).

### Scope (binding)
1. Keep ACL lean A (`getfacl -p .env` still shows `group:agi:r--`).
2. Smoke: no unnamed `.env mode 640` fail vs expect-600; no unnamed `.agi/loop.log Permission denied` (PASS or explicit labeled skip).
3. Do **not** apply more ACL from this DESIGN package (Belam already applied U2/U3 window).
4. Never reopen `.4.7` / `.4.2` wrongly. Never chmod 600 that strips group ACL.

### Rejected
- Strip ACL / chmod 600 dropping `group:agi:r--`.
- Reopen U2 COMPLETE as dump.
- More ACL without SM ASK.

## Must-carry
1. Smoke PASS (or labeled skips only) on both residues.
2. ACL lean A kept.
3. Write+agi-turn; never write.py; never git rm.

## Falsifiers (for later operate / COMPLETE)
1. `commands.py run verify` smoke: no unnamed `.env mode 640` fail; no unnamed loop.log PE for agi-belam.
2. `getfacl -p .env` still shows `group:agi:r--`.
3. **Negative:** strip ACL; reopen `.4.7`/`.4.2`; more ACL without SM ASK; write.py; git rm; Belam wake from this package; DG before SM PASS.

## Out of scope
Strip ACL · reopen U2/U3 COMPLETE · bin-suite grant (V1) · engine pin (V3) · Master · season3 rewrite
