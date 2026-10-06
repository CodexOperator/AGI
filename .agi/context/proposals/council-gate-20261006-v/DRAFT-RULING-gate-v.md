# DRAFT ONE ruling — gate-v (council-gate-20261006-v) — DESIGN batch

**Pen:** self-perpetuating · **Lenses:** alive (**pending**) · all-is-one (**pending**)  
**Designs:**  
- `DESIGN-g5.4.1.4.9-suite-window.md` (mint `7b72df8c367e414eb3f2a8eade603da9`)  
- `DESIGN-g5.4.1.4.10-smoke-env-loop.md` (mint `c538491cc5f84b89a29e838226bad3d2`)  
- `DESIGN-g5.4.1.4.11-engine-pin.md` (mint `4939ad2657cd403fae8e54f263b3201c`)  
- `DESIGN-batch-gate-v.md`  
**Prime mint tip (SoT):** `2c9172e68` · **Live trunk:** `ce34b336b`  
**Ask:** `sm-council-ask-20261006-v.md`

## Verdict

**PASS pending lens fold** (alive + all-is-one). Design sufficient for later SM gate on V1–V3 after council PASS. **DG held.** **Do not box Belam.** **Do not SM-gate yet.** **Do not ask Belam suite grant yet.** Season3 tip untouched. Capsule `fda4efd6e` stands. gate-u-u1 COMPLETE / `.4.2` COMPLETE / U2 ACL lean A **not mixed / not stripped**.

**Ready-for-gate: BLOCKED until lenses return PASS|AMEND|RETURN.**

## Must-carry (short) — THREE leaves

### g5.4.1.4.9 — ONE suite window (V1)
1. Clear bin-suite-fresh mtime residue via ONE suite window after SM PASS + **SM ASK Belam grant**.
2. Never self-grant; never reopen `.4.2`; never strip pytest.
3. Falsifier: `bin-suite-fresh` PASS; lock free.

### g5.4.1.4.10 — smoke .env + loop.log (V2)
1. Reconcile expect-600 with ACL lean A — **keep** `group:agi:r--`; labeled skip OK; never strip ACL.
2. Close `.agi/loop.log` PE (readable or labeled skip).
3. Falsifier: smoke clean on both; getfacl still lean A.

### g5.4.1.4.11 — engine pin (V3)
1. Advance pin to live pilot **or** labeled policy; never force-reset pilot backward.
2. Falsifier: no smoke pin-drift naming `179f95602839`.

## Residues / OOS
gate-u-u1 COMPLETE · gate-t product · U2/U3 COMPLETE · `.4.2` COMPLETE — separate; do not reopen/strip.

## Ready-for-gate

**BLOCKED** — awaiting alive + all-is-one lens replies (PASS|AMEND|RETURN) with path. Parent folds lenses → final RULING → then ready-for-gate to SM. This DRAFT does **not** SM-gate, does **not** mint DG leaves, does **not** wake Belam, does **not** ask suite grant, does **not** touch season3 tip `4b8f28b5e` / capsule `fda4efd6e` / Master.

## Out of scope

SM gate before council · Belam suite grant · Belam wake · strip ACL · reopen `.4.2`/`.4.7` · DG before PASS · force-reset pilot · season3 rewrite · Master · inventing heads · git rm · waive-as-footnote · write.py · strip pytest · duplicate mint
