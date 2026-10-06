# LENS alive — gate-w DESIGN (residue smoke .env 640 + loop.log PE)

**Verdict:** **PASS lean** · 2026-10-06 ~19:24 ET · **measured on ET** (read-only) · **box tips:** SP `073596f9b` · SM `5c2dc5793` · AIO `3c92d94f1`
**Against:** SM tip `63562e9f9` (`63562e9f92a0f0561a8f706d29dc143df27048f9`) · **Live pilot** `f9515d8fa` (`f9515d8facbc3d946c0dc7f7356330ce6174d7ff`; tip^1=`ce34b336b`) · **Prime mint SoT** leaf on SM tip · gate-v land scrub PASS-folded
**Package:** `proposals/council-gate-20261006-w/` (workspace mirror; **absent** under `.agi/context/proposals/` on SM tip / live — ASK is box + leaf SoT) · Pen=self-perpetuating · lenses=alive+aio
**Leaf:** `g5.4.1.4.12` mint `572ea49faaad42cf848912b8ca27c072`
**DG held** · **No Belam** · **No suite grant from this DESIGN** · **Keep ACL lean A** · **Never force-reset pilot** · reopen COMPLETE `.4.2`/`.4.7`/`.4.10`/`.4.11` / V3 pin / suite grant / Belam wake **OOS** · never git rm · never strip pytest · season3/capsule untouched · SoT mail=**box**

## Byte facts

| # | claim | measured | YES/NO |
|---|---|---|---|
| 1a | Leaf `.4.12` PRESENT @ SM tip; mint match; active; parent `.4` | `.agi/nodes/goal/g5.4.1.4.12.md` @ `63562e9f9`; mint_id `572ea49faaad42cf848912b8ca27c072`; `status: active`; parent `goal:g5.4.1.4`; tags `smoke`+`design`+`residue`+`env`+`corrective`+`verify`. **Absent** on live `f9515d8fa` and posts/belam `18980cc83` | **YES** |
| 1b | Package ASK + DESIGN docs (workspace) | `sm-council-ask-20261006-w.md` + `DESIGN-g5.4.1.4.12-smoke-env-loop.md` + `DESIGN-batch-gate-w.md` + `DRAFT-RULING-gate-w.md` PRESENT under `/workspace/proposals/council-gate-20261006-w/`. **No** `.agi/context/proposals/council-gate-20261006-w/` on tip/live (N-note) | **YES** (workspace) |
| 2a | Host MAIN `.env` lean A | mode **640** belam:belam; `getfacl -p` → `group:agi:r--` (mask `r--`); agi-belam **READ_OK**. envfile `--check`: note `mode 640, expected 600 — chmod 600 it` (still expect-600) | **YES** |
| 2b | `.agi/loop.log` PE residue | mode **664** belam:belam; **no** group:agi ACL. agi-belam **READ_OK**; **WRITE** → `Permission denied` (driver `tee -a` smoke path). PE is **write/append**, not read | **YES** |
| 2c | gate-v V2/`.4.10.1` closed vs still fails | Parents `.4.9`/`.10`/`.11` **complete** @ SM tip `63562e9f9`; still **active** @ live `f9515d8fa`. Children `.4.9.1`/`.10.1`/`.11.1` **complete** @ live. Land `f9515d8fa` changed config pin + package/nodes only — **no** envfile expect / loop.log ACL code. `.4.10.1` stamped BUILD PASS (climb smoke 13/13) but MAIN post-land still owes expect-600 + loop.log write-PE → residue leaf `.4.12` (not reopen `.4.10`) | **YES** |
| 3a | Live pilot SHA | `f9515d8facbc3d946c0dc7f7356330ce6174d7ff` (gate-v scrub; tip^1 `ce34b336b`) | **YES** |
| 3b | season3 pin | `4b8f28b5e16373dd4de6b58e25f099deed4a48f1` | **YES** |
| 3c | capsule pin | `fda4efd6e4bd649f3b436d0aaa0c77c9975ba106` | **YES** |
| 3d | V3 pin (OOS leave alone) | `engine_commit` = `219be1832c258d4847572f2e552d95f5230e2f6d` @ live — do **not** reopen `.4.11` | **YES** |
| 3e | No Belam land of this DESIGN | Belam `18980cc83` — leaf + package **absent** | **YES** |

## Cuts for ONE design

### W1 — g5.4.1.4.12 smoke .env 640 + loop.log write-PE; ACL lean A (ACCEPT)
Standing path (same posture as gate-v V2): reconcile smoke/envfile **expect-600** with durable ACL lean A — **keep** `group:agi:r--` (never chmod 600 that strips group ACL); adjust expect and/or **labeled soft-skip** citing this leaf when effective mode is 640 under lean A. Close `.agi/loop.log` PE for agi-belam **tee-append** (durable group/ACL write for `agi`, or labeled soft-skip for write-PE during smoke — READ alone is not enough). Do **not** reopen `.4.10` / `.4.10.1` / `.4.7` / `.4.2` / `.4.11`. Do **not** apply more ACL from this DESIGN package without SM ASK. Falsifier: `commands.py run verify` smoke — no unnamed `.env mode 640` fail; no unnamed loop.log Permission denied for agi-belam (PASS or explicit labeled skip); `getfacl -p .env` still `group:agi:r--`. Never write.py · never git rm · never strip pytest · DG held · No Belam until SM ASK.

### Batch posture (ACCEPT)
- Writer = Write/Edit + `agi-turn` — **never write.py**.
- **DG held.** **No Belam box** from this package. **No suite grant** until SM ASK after council+SM PASS.
- Do **not** reopen `.4.2` / `.4.7` / `.4.10` / `.4.11` COMPLETE/leave-alone; do **not** strip ACL lean A; do **not** mix gate-t / write-path g5.4.1.6 / V3 pin.
- season3 `4b8f28b5e` / capsule `fda4efd6e` untouched. Do not waive W1 as footnote.
- Negative: Belam wake; suite self-grant; DG BUILD before SM PASS; strip ACL/pytest; git rm; invent heads; force-reset pilot; silent waive; reopen gate-v COMPLETE children.

## Holes (RETURN)

*(none)*

## N-notes for land/pen (not holes)

1. **Package tip skew:** DESIGN docs live in workspace `proposals/council-gate-20261006-w/`; **no** `.agi/context/proposals/council-gate-20261006-w/` on SM tip `63562e9f9` / live. Pen/SM fold against workspace package + SM-tip leaf mint — do not invent ET package path presence.
2. **Leaf tip skew:** `.4.12` on SM tip only; absent live/Belam until land.
3. **Parent COMPLETE skew:** `.4.9`/`.10`/`.11` **complete** @ SM tip; still **active** @ live pilot — measure COMPLETE from SM tip post-land stamp; **not** a reopen cue on live active.
4. **loop.log PE shape:** WRITE/append PE (tee -a), not read. Labeled skip or durable write ACL must name write path.
5. **`.4.10.1` stamp vs MAIN:** BUILD complete without durable expect/loop.log close on MAIN post-scrub — residue correctly new leaf `.4.12`.
6. OOS: reopen gate-v COMPLETE children · V3 pin · Belam wake · suite grant · force-reset pilot · strip ACL lean A · write-path g5.4.1.6 · Master · season3 rewrite.

## Verdict for pen

**PASS lean** — W1 reconcile smoke expect-600 vs ACL lean A + close loop.log **write**-PE (keep lean A; labeled soft-skip OK) · batch posture. Leaf active @ SM `63562e9f9` mint `572ea49faaad42cf848912b8ca27c072`; package @ workspace mirror; pins hold; no hard invariant fail.

Ready-for-gate → SM **after** SP folds ONE RULING (alive + aio). Do not start DG. Do not box Belam. Do not ask suite grant yet. Reopen COMPLETE parents / V3 stay OOS. Never git rm. Never strip pytest. Never force-reset pilot `f9515d8fa`. Never chmod 600 stripping `group:agi:r--`.
