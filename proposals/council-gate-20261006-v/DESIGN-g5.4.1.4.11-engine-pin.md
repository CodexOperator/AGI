# Council design — goal:g5.4.1.4.11 — engine HEAD pin drift

**Leaf mint:** `4939ad2657cd403fae8e54f263b3201c` · parent `goal:g5.4.1.4` · **status:** active (DESIGN)  
**Prime mint tip:** `2c9172e68` · **Live trunk:** `ce34b336b` (pilot advanced past gate-t `853090aa1`)  
**Pin named at mint:** config pin `179f95602839` vs HEAD `853090aa1` (gate-t land) — design must reconcile vs **current** live pilot  
**Pen:** self-perpetuating · **Lenses:** alive + all-is-one (pending)  
**DG held** · **No Belam box** · season3 `4b8f28b5e` · capsule `fda4efd6e`  
**Writer:** Write+agi-turn — never write.py

## Problem (measured)

| object | measured (at mint) |
|---|---|
| engine HEAD @ gate-t land | `853090aa1` |
| config pin | `179f95602839` |
| smoke | names engine pin drift |

Live pilot now `ce34b336b` — RULING must name pin advance / policy against **current** tip, not force-reset pilot backward.

## Standing path (ONE lean — ACCEPT)

**Reconcile pin vs HEAD** so smoke pin-drift is gone: advance pin to landed/live tip **or** document labeled pin policy PASS. **Never** force-reset / ff pilot away from gate-t+u-u1 product to old pin.

### Scope (binding)
1. Name exact pin-update path (config cell / writer) or labeled skip policy.
2. Falsifier: verify smoke shows no engine pin drift naming `179f95602839` (pin==HEAD or labeled policy).
3. Never waive as footnote. Never write.py. Never git rm. Never strip pytest.

### Rejected
- Force-reset pilot to old pin.
- Silent leftover pin drift footnote.

## Must-carry
1. Smoke pin-drift closed on live pilot.
2. Pilot product (gate-t + gate-u-u1) preserved.
3. Write+agi-turn; never write.py.

## Falsifiers (for later operate / COMPLETE)
1. `commands.py run verify` smoke: no engine pin drift naming `179f95602839`.
2. **Negative:** force-reset pilot to pin; waive as footnote; write.py; git rm; season3 tip moved; Belam wake from this package; DG before SM PASS.

## Out of scope
Suite grant (V1) · ACL / .env 640 / loop.log (V2) · reopen COMPLETE parents · Master · season3 rewrite
