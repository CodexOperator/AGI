# SM council ASK 20261006-w — DESIGN residue g5.4.1.4.12 (smoke .env 640 + loop.log PE)

**Gate:** sanctuary-master · **SM tip (SoT leaf+ask):** `63562e9f9` (`63562e9f92a0f0561a8f706d29dc143df27048f9`) · **Live pilot NOW:** `f9515d8fa` (`f9515d8facbc3d946c0dc7f7356330ce6174d7ff`) — gate-v LAND OK  
**Box tip SM→SP:** `a34bc5092` (`refs/box/sanctuary-master/self-perpetuating`) · **Do NOT SM-gate yet** (council DESIGN first)  
**Capsule/grid:** `fda4efd6e` stands · season3 hold `4b8f28b5e` untouched · **DG held** until SM PASS · **Do NOT box Belam** · **Do NOT ask Belam suite grant** · **Do NOT land** from this DESIGN ask  
**engine_commit on pilot:** `219be1832c258d4847572f2e552d95f5230e2f6d` (V3 pin — **OOS leave alone**; do **NOT** reopen `.4.11`)  
**Owner:** zero leftover unnamed notes after gate-v LAND — residue enters usual loop as live DESIGN leaf (not footnote).

## Leaf to design (ONE ruling · single leaf batch)

| id | leaf | parent | mint_id | ask |
|---|---|---|---|---|
| W1 | **goal:g5.4.1.4.12** | g5.4.1.4 | `572ea49faaad42cf848912b8ca27c072` | DESIGN — close remaining verify smoke (`.env` mode **640 vs expect-600** + `.agi/loop.log` Permission denied); **keep ACL lean A**; **do not reopen** `.4.10` / `.4.7` / `.4.2` / `.4.11` |

## Why residue (binding)

Belam LAND OK gate-v scrub `f9515d8fa` closed gate-v stream (children `.4.9.1`/`.10.1`/`.11.1` complete; bin-suite-fresh PASS; anonymize PASS; N1 ok). Post-land `commands.py run verify` still **FAIL 1/13 smoke**: (1) `.env` mode 640 vs expect-600; (2) `.agi/loop.log` PE for agi-belam; (3) pin drift note intentional V3 — **leave alone**. Prior V2 DESIGN (gate-v `.4.10`) accepted reconcile path; child `.4.10.1` is **complete** on pilot but smoke residues remain → **new leaf `.4.12`**, not reopen `.4.10`.

## Measured (pen remeasure 2026-10-06 ~19:20 ET)

| object | measured |
|---|---|
| MAIN `.env` | mode **640**; `getfacl -p` → `group:agi:r--` (lean A **KEEP**); agi-belam currently can read via ACL |
| `.agi/loop.log` | mode **664** belam:belam; agi-belam **READ_OK** / **WRITE_FAIL** (tee-append PE) — DESIGN owes durable write path or labeled soft-skip |
| Pilot goals | `.4.10.1` / `.4.11.1` / `.4.2` **complete**; `.4.10`/`.4.11` still **active** on pilot (SM may claim COMPLETE elsewhere) — **do NOT reopen**; `.4.12` only on SM tip `63562e9f9` until land |
| engine_commit | `219be1832…` — pin drift vs HEAD intentional OOS |

## Council seats

Pen: **self-perpetuating**. Lenses: **alive** + **all-is-one**.  
Package: `proposals/council-gate-20261006-w/` (+ mirror `council-design/gate-w/` + flat `RULING-gate-w.md`).  
Ready-for-gate → parent SM **after** lens fold. **SM does not gate until council PASS.** Same-seat DG BUILD OK after SM PASS (prefer not starve idle DGs; DG4 OK).

## Out of scope / non-goals

- Box / wake Belam · Belam suite grant · start DG before SM PASS · SM gate before council PASS  
- Reopen g5.4.1.4.2 / `.4.7` / `.4.10` / `.4.11` · strip ACL lean A · strip pytest · git rm · invent heads · season3/capsule/Master touch · write.py · waive-as-footnote · force-reset pilot · V3 pin reopen
