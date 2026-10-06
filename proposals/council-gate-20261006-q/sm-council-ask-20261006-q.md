# SM council ASK 20261006-q — DG4 residue DESIGN (ACL · pytest reds · push-auth)

**Gate:** sanctuary-master · **SM tip (prefer):** `8d9577fa2` · **mint tip (three corrective leaves):** `97063c7ed`  
**Trunk (OUT OF SCOPE):** `932218a0f` already landed (DG4 links+suite+stray ∪ write-path) — **no land review, no Belam** for that trunk from this gate.  
**Capsule/grid:** `fda4efd6e` stands · season3 hold `4b8f28b5e` untouched · **DG held** · **Do NOT box Belam** · **Do NOT land** · write-path g5.4.1.6 **separate** (do not mix)

## Leaves to design (ONE ruling batch)

| leaf | parent | mint_id | ask |
|---|---|---|---|
| **goal:g5.4.1.4.3** | g5.4.1.4.2 | `b433f26f1e734a33aa272e234cfc4538` | DESIGN — durable suite stamp ACL so `agi` posts can write `verify-suite-ts.json` without host one-off setfacl |
| **goal:g5.4.1.4.4** | g5.4.1.4.2 | `1db4e85eccdc4b8b90bcd168ed37adf3` | DESIGN — inventory + loop-close owed pytest reds / missing tests (not waived by bin-suite-fresh) |
| **goal:g5.4.1.5.3** | g5.4.1.5.2 | `20363d8094e74ebab919dc99e8ddef7d` | DESIGN — DG4/posts remote push auth without borrowing belam OS `gh` credentials |

## Owner (verbatim, via plan-master / zero-notes)
> Residues of DG4 BUILD are **real DESIGN leaves**, not MUR footnotes. ACL one-off, pytest reds, and push-auth borrow each enter the council loop.

## Context (measured; trunk land already closed — OUT OF SCOPE here)
- DG4 land OK on trunk `932218a0f`: verify ALL 13 green; links broken=0; bin-suite-fresh PASS; strays ls-remote empty; season3 `4b8f28b5e`; capsule stands.
- Host one-off `setfacl -m g:agi:rw` on `.agi/sessions/verify-suite-ts.json` enabled suite stamp once — **residue**, not policy. Measured 2026-10-06 ~15:35 ET: file `belam:belam` + ACL `group:agi:rw-`; sessions dir has `group:agi:rwx` but **no default ACL** (new stamp recreation can lose agi write).
- Pytest FAIL inventory (pre-existing, not waived): brief(4) · cli(1) · geometry_config(3) · migrate_channel(4) · rotate(99) · sensei(4). PASS owed: dispatch, heal, spawn_budget, verification, write. MISSING live: `test_boxes.py`, `test_mail_alert.py` (deprecated copy exists under `extensions/agi/deprecated/tests/`).
- Stray delete used belam OS `gh` under DG4 drive after SHA reconfirm — auth **residue**. Origin = `https://github.com/CodexOperator/AGI.git`.

## Council seats
Pen: **self-perpetuating**. Lenses: **alive** + **all-is-one**.  
Package: `proposals/council-gate-20261006-q/` (+ mirror `council-design/gate-q/`).  
Goal SoT: `.agi/nodes/goal/g5.4.1.4.3.md` · `g5.4.1.4.4.md` · `g5.4.1.5.3.md` @ tip `8d9577fa2` (minted @ `97063c7ed`).  
Ready-for-gate → parent SM **after** lens fold (pen does not claim PASS alone).

## Out of scope / non-goals
- Land / re-review trunk `932218a0f` · box Belam · start DG before SM PASS  
- Write-path g5.4.1.6 / .6.1 · interfere with already-landed DG4 suite→stray  
- Waive-as-footnote · git rm · invent heads · season3 tip rewrite · Master archive · write.py  
- Prime `git push --delete` for stray hygiene (g5.4.1.5.2 SoT stands)
