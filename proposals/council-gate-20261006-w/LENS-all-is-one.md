# Lens — all-is-one · gate-w (council-gate-20261006-w) — DESIGN g5.4.1.4.12

**Pen:** self-perpetuating · **Lenses:** alive (**PASS lean** · `LENS-alive.md`) · all-is-one  
**Against:** SM ASK tip `63562e9f9` (leaf mint) · SM HEAD now `53f6b0128` (unrelated node restamp after ASK) · live pilot `f9515d8fa` · Belam LAND OK cited  
**Leaf:** `g5.4.1.4.12` mint `572ea49faaad42cf848912b8ca27c072`  
**DG held** · **No Belam** · **No suite grant** · **No SM-gate from this lens**  
**season3** `4b8f28b5e` · **capsule** `fda4efd6e` · Writer Write+agi-turn — never write.py · never git rm · never strip pytest · KEEP ACL lean A · never force-reset pilot · pin drift OOS leave alone  
**Peer:** `LENS-alive.md` — **PASS lean** (fold conjunct ready)

## Verdict

# **PASS**

Design sufficient for SM gate on W1 (`g5.4.1.4.12`) after pen fold. **ACCEPT** standing path: reconcile smoke expect-600 with durable ACL lean A (KEEP `group:agi:r--`; adjust expect and/or **explicit labeled soft-skip** — never chmod 600 dropping group ACL) + close `.agi/loop.log` PE durably (readable path **or** labeled skip — never unnamed PE). **Do not reopen** `.4.2` / `.4.7` / `.4.10` / `.4.11`. Pin drift intentional leave alone (V3 OOS). OWNER pytest ALLOWED. DG held. Belam HOLD.

## Independent re-measure (agi-all-is-one @ @box · 2026-10-06 ~19:28 ET)

| check | result |
|---|---|
| ASK / package tip `63562e9f9` | resolves `63562e9f92a0f0561a8f706d29dc143df27048f9` — mint `.4.12` + SM COMPLETE gate-v parents |
| SM HEAD now | `53f6b0128afb488e2254b0aae858c016d11ffb9a` — post-ASK unrelated goal restamps; leaf still present |
| Live pilot | `f9515d8facbc3d946c0dc7f7356330ce6174d7ff` = `core/season2/et-grok-pilot` (advanced from `ce34b336b`; Belam LAND OK scrub) |
| Leaf `g5.4.1.4.12` | PRESENT on SM; mint `572ea49faaad42cf848912b8ca27c072`; `status: active`; parent `g5.4.1.4`; tags design+smoke+env+residue; **MISSING on live MAIN** (not yet landed — expected) |
| Parents `.4.9/.10/.11` (SM) | **complete** (SM COMPLETE @ `63562e9f9`) — **do not reopen** |
| Children `.4.9.1/.10.1/.11.1` | **complete** on SM + live |
| Parents `.4.9/.10/.11` (live MAIN) | still `active` (node lag vs SM COMPLETE) — do not reopen / do not restamp from council |
| U2 `.4.7` / U3 `.4.8` | **complete** — **do not reopen / do not strip ACL** |
| `.4.2` | live MAIN **complete**; SM tip shows `active` stamp churn — **do not reopen** either way |
| MAIN `.env` ACL lean A | `getfacl -p /data/work/agi/.env` → `group:agi:r--`; effective mode **640** (`-rw-r-----+`) — **KEEP** |
| envfile expect-600 | still hard-coded: `if mode != 0o600: notes.append(... expected 600 — chmod 600 it)` @ `extensions/agi/bin/envfile.py:471-473` — **unreconciled on trunk** (gate-v land scrub had **no** envfile delta) |
| simulate | `mode=640 expect_600_fail=True` |
| `.agi/loop.log` | mode **664** (`-rw-rw-r--`) owner belam:belam; **READ_OK** (belam/agi-belam/aio); alive measured **WRITE/tee-append PE** for agi-belam (driver `tee -a`) — close **write** path durably (agi write ACL/group) **or** labeled soft-skip naming write-PE (READ alone not enough) |
| Engine pin | `.agi/config.json` `engine_commit` = `219be1832c258d4847572f2e552d95f5230e2f6d` — V3 product; **leave alone** (OOS) |
| season3 / capsule | `4b8f28b5e…` / `fda4efd6e…` stand |
| posts/belam | tip `18980cc83` — **not contacted** |
| write.py / git rm / Belam / DG / suite | never write.py; no deletes; Belam HOLD; DG held; no suite grant |

## Reading of "640"

Topic **"smoke .env 640"** = measured **fail symptom** (effective mode 640 vs smoke expect-600), **not** an Owner ask to chmod toward 640 or to loosen ACL. Owner pin: **KEEP ACL lean A** `group:agi:r--`. Any path that chmod 600 drops the group ACL is **REJECT**.

## Why residue after gate-v V2 COMPLETE

Gate-v V2 (`.4.10` / `.4.10.1`) ACCEPT'd the same reconcile lean; DG4 RESULT stamped smoke PASS 13/13 on climb seat. Land scrub `f9515d8fa` carried **docs + nodes + pin only** — **zero** `envfile.py` / smoke-expect delta. Post-land Belam verify on MAIN still sees expect-600 vs durable 640 → SM correctly minted **new** DESIGN leaf `.4.12` rather than footnote or reopen `.4.10`.

## Must-carry cuts (binding enough for SM gate → later DG)

### W1 — g5.4.1.4.12 smoke .env 640 + loop.log PE (residue)

1. **Reconcile** smoke expect-600 with durable ACL lean A — **keep** `group:agi:r--` (adjust `envfile.py` expect to accept effective 640 **when** lean A present, and/or explicit **labeled** soft-skip — **never** strip ACL / chmod 600 dropping group).
2. Close `.agi/loop.log` Permission denied for verify actors: PE is **WRITE/tee-append** (alive measured) — durable agi write ACL/group **or** explicit labeled soft-skip naming write-PE (READ alone not enough; never unnamed PE).
3. Do **not** reopen `.4.10` / `.4.7` / `.4.2` / `.4.11`. Do **not** apply more ACL from this DESIGN package without SM ASK naming it.
4. Pin drift / V3 — **leave alone** (OOS).
5. **Falsifier:** `commands.py run verify` smoke: no unnamed `.env mode 640` fail vs expect-600; no unnamed `.agi/loop.log` PE; `getfacl -p .env` still `group:agi:r--`.
6. Writer Write+agi-turn. DG held until SM PASS. No Belam from this package. Same-seat OK later (prefer not starve idle DGs; DG4 OK).
7. OWNER pytest ALLOWED — never strip. Never write.py. Never git rm. Never force-reset pilot. Never waive as footnote.

## Batch posture

- Writer = Write/Edit + `agi-turn` — **never write.py**.
- **DG held** until parent SM PASS after RULING.
- **No Belam box** · **no suite grant** from this package.
- Do **not** reopen `.4.2` / `.4.7` / `.4.8` / `.4.10` / `.4.11`; KEEP ACL lean A.
- season3 / capsule / Master untouched. SoT mail = **box**.
- Negative: Belam wake; suite grant; SM gate before council PASS; strip ACL / chmod 600 dropping lean A; reopen COMPLETE; DG BUILD before SM PASS; strip pytest; git rm; invent heads; waive-as-footnote; force-reset pilot; reopen V3 pin; duplicate mint; footnote instead of leaf (leaf already minted — honor it).

## Holes (RETURN)

*(none)* — standing path matches Owner lean A KEEP + prior V2 ACCEPT; residue leaf correctly scoped; measures confirm unreconciled expect-600 on trunk.

## Peer fold / ready-for-gate

`LENS-alive.md` — **PASS lean**. This lens = **PASS**. Both lenses folded-ready → pen promotes final RULING → **ready-for-gate UNBLOCKED → SM**. This package does **not** SM-gate, does **not** mint DG, does **not** wake Belam, does **not** ask suite grant.
