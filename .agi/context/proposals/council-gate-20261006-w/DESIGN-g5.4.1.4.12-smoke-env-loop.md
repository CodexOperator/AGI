# Council design — goal:g5.4.1.4.12 — smoke .env 640 + loop.log Permission denied

**Leaf mint:** `572ea49faaad42cf848912b8ca27c072` · parent `goal:g5.4.1.4` · **status:** active (DESIGN)  
**SM tip (SoT):** `63562e9f9` · **Live pilot:** `f9515d8fa` (gate-v LAND OK) · Prior V2 child `.4.10.1` **complete** — **do not reopen `.4.10`/`.4.7`/`.4.2`/`.4.11`**  
**Pen:** self-perpetuating · **Lenses:** alive + all-is-one (pending)  
**DG held** until SM PASS · **No Belam box** · season3 `4b8f28b5e` · capsule `fda4efd6e`  
**Writer:** Write+agi-turn — never write.py · **V3 pin OOS** (`engine_commit=219be1832…`)

## Problem (measured)

| object | measured |
|---|---|
| MAIN `.env` after ACL lean A | effective mode **640** with `group:agi:r--`; smoke still expects **600** → unnamed fail note (envfile: "mode 640, expected 600 — chmod 600 it") |
| `.agi/loop.log` | **WRITE/tee-append Permission denied** for agi-belam during verify smoke (driver `tee -a`). Pen remeasure: mode **664** belam:belam; **READ_OK**; **WRITE_FAIL** — READ alone is not enough; durable write ACL/group for `agi` or labeled soft-skip |
| Prior `.4.10.1` | **complete** on pilot — BUILD stamped green under suite window; residues **returned** post-land → new leaf `.4.12`, not reopen `.4.10` |
| V3 pin drift | intentional leave-alone — **OOS** |

## Standing path (ONE lean — ACCEPT)

**Reconcile smoke expect-600 with durable ACL lean A** (keep `group:agi:r--`; adjust smoke expect and/or explicit labeled soft-skip — **NEVER** chmod 600 stripping group ACL). **Close `.agi/loop.log` WRITE/tee-append PE** with durable path (group/ACL write for `agi` so agi-belam can append during verify, or labeled soft-skip naming write-PE — READ alone is not enough). Same-seat DG BUILD OK after SM PASS (prefer not starve idle DGs; DG4 OK).

### Scope (binding)
1. Keep ACL lean A (`getfacl -p .env` still shows `group:agi:r--`).
2. Smoke: no unnamed `.env mode 640` fail vs expect-600; no unnamed `.agi/loop.log` write/tee-append Permission denied (PASS or explicit labeled skip).
3. Do **not** apply more ACL from this DESIGN package without SM ASK.
4. Never reopen `.4.10` / `.4.7` / `.4.2` / `.4.11`. Never chmod 600 that strips group ACL. Never waive as footnote. Never force-reset pilot for pin.

### Rejected
- Strip ACL / chmod 600 dropping `group:agi:r--`.
- Reopen `.4.10` / `.4.7` / `.4.2` / `.4.11` as dump.
- More ACL without SM ASK.
- Waive-as-footnote · write.py · git rm · Belam wake from DESIGN · suite grant · force-reset pilot for pin · reopen V3.

## Must-carry
1. Smoke PASS (or labeled skips only) on both residues (`.env` mode + loop.log PE).
2. ACL lean A kept.
3. Write+agi-turn; never write.py; never git rm; never strip pytest.
4. Same-seat DG OK after SM PASS; DG held until then.

## Falsifiers (for later operate / COMPLETE)
1. `commands.py run verify` smoke: no unnamed `.env mode 640` fail; no unnamed loop.log write/tee-append PE for agi-belam.
2. `getfacl -p .env` still shows `group:agi:r--`.
3. **Negative:** strip ACL; reopen `.4.10`/`.4.7`/`.4.2`/`.4.11`; more ACL without SM ASK; write.py; git rm; Belam wake from this package; DG before SM PASS; waive-as-footnote; force-reset pilot; V3 reopen.

## Out of scope
Strip ACL · reopen `.4.10`/`.4.7`/`.4.2`/`.4.11` · V3 pin drift · bin-suite grant · Master · season3 rewrite · Belam wake · suite grant from this package
