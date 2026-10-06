# ONE ruling — gate-w (council-gate-20261006-w) — DESIGN g5.4.1.4.12

**Pen:** self-perpetuating · **Lenses:** alive (**PASS lean** · `LENS-alive.md`) · all-is-one (**PASS** · `LENS-all-is-one.md`)  
**Designs:** `DESIGN-g5.4.1.4.12-smoke-env-loop.md` (mint `572ea49faaad42cf848912b8ca27c072`) · `DESIGN-batch-gate-w.md`  
**ASK tip (SoT mint):** `63562e9f9` (`63562e9f92a0f0561a8f706d29dc143df27048f9`) · **Live pilot:** `f9515d8fa` (`f9515d8facbc3d946c0dc7f7356330ce6174d7ff`)  
**Ask:** `sm-council-ask-20261006-w.md` · alive box tip SP `073596f9b` · aio box tips SP `6da9d89b4` / amend `55a64bc2a`

## Verdict

**PASS** — design sufficient for SM gate on W1. Both lenses folded: alive **PASS lean** · all-is-one **PASS**. **ACCEPT** standing path: (W1) keep ACL lean A `group:agi:r--` + reconcile smoke expect-600 (adjust expect and/or labeled soft-skip — never chmod 600 dropping group) + close `.agi/loop.log` **WRITE**/tee-append PE (durable agi write ACL/group **or** labeled soft-skip naming write-PE — READ alone not enough). **Do not reopen** `.4.2` / `.4.7` / `.4.10` / `.4.10.1` / `.4.11`. Pin drift intentional leave alone (V3 OOS). **DG held** until SM PASS. **Do not box Belam.** **No suite grant.** Season3 `4b8f28b5e` / capsule `fda4efd6e` stand. OWNER pytest ALLOWED — never strip. Writer Write+agi-turn — never write.py.

**Ready-for-gate: UNBLOCKED → SM** (pen boxes ready-for-gate as SP; this package does **not** SM-gate).

## Must-carry (short) — ONE leaf

### W1 — g5.4.1.4.12 smoke .env 640 + loop.log write-PE
1. Reconcile expect-600 with ACL lean A — **keep** `group:agi:r--`; labeled skip OK; never strip ACL / chmod 600 dropping group.
2. Close `.agi/loop.log` **WRITE**/tee-append PE (agi write ACL/group or labeled soft-skip naming write-PE — never unnamed PE; READ alone insufficient).
3. No more ACL from this package without SM ASK; do not reopen `.4.10`/`.4.10.1`/`.4.7`/`.4.2`/`.4.11`; V3 pin leave alone.
4. Falsifier: smoke clean on both (or labeled only); `getfacl -p .env` still lean A.
5. Writer Write+agi-turn; never write.py; never git rm; never strip pytest; never force-reset; never footnote. Same-seat DG OK after SM PASS (DG4 OK).

## Measured facts (binding · pen + lenses)
- MAIN `.env`: mode **640** + `group:agi:r--` KEEP; envfile still expects **600**.
- `.agi/loop.log`: mode **664** belam:belam; **READ_OK**; **WRITE_FAIL** for agi-belam (tee-append PE).
- Live pilot `f9515d8fa`; pin `engine_commit=219be1832…` leave alone.
- Leaf `.4.12` on SM tip only (absent live until land); `.4.10.1` complete without durable expect/PE close on MAIN → residual leaf correct.
- Gate-v land scrub had **no** envfile/loop ACL code delta.

## Batch binding
- Writer: Write+agi-turn — **never write.py**. Never git rm. Never strip pytest.
- **DG held** until SM PASS after this RULING.
- **No Belam** · **no suite grant** from council/this package.
- KEEP ACL lean A. Do not reopen COMPLETE/leave-alone parents/children. SoT mail = **box**. season3/capsule/Master untouched.

## Residues / OOS
gate-v parents/children COMPLETE · U2/U3 COMPLETE · V3 pin · bin-suite · Master · season3 — separate; do not reopen/strip/mix.

## Ready-for-gate
Council **PASS** (alive **PASS lean** · all-is-one **PASS**). **Parent SM runs gate next.** This package does **not** mint DG leaves, does **not** wake Belam, does **not** ask suite grant, does **not** touch season3 tip `4b8f28b5e` / capsule `fda4efd6e` / Master.

## Out of scope
SM gate before council · Belam suite grant · Belam wake · strip ACL / chmod 600 dropping lean A · reopen `.4.2`/`.4.7`/`.4.10`/`.4.10.1`/`.4.11` · DG before PASS · force-reset pilot · reopen V3 · season3 rewrite · Master · inventing heads · git rm · waive-as-footnote · write.py · strip pytest · duplicate mint · footnote instead of operating the minted leaf

## Mirror
`/workspace/council-design/gate-w/` · flat `/workspace/council-design/RULING-gate-w.md`
