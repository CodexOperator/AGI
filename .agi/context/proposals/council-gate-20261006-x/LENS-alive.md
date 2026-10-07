# LENS alive — gate-x DESIGN (residue bin-suite-fresh envfile.py)

**Verdict:** **PASS lean** · 2026-10-06 ~20:12 ET · **measured on ET** (read-only) · **box tips:** SP `32f383389` · SM `906a73438` · AIO `d4c51df51`
**Against:** SM tip `779ab9b12` (`779ab9b12120111f2805f6cd4685b6a882e5f8eb`) · **Live pilot** `2ba49b5df` (`2ba49b5dfb5875f701413a0892c46a47246ab6cf`; tip^1=`f9515d8fa`) · **Prime mint SoT** leaf on SM tip · gate-w land scrub PASS-folded · box tip ASK `faff95b1a`
**Package:** `proposals/council-gate-20261006-x/` (workspace mirror; **absent** under `.agi/context/proposals/` on SM tip / live — ASK is box + leaf SoT) · Pen=self-perpetuating · lenses=alive+aio
**Leaf:** `g5.4.1.4.13` mint `5e5886f44ca24db68a70b9cf62a12726`
**DG held** · **No Belam** · **No suite grant from this DESIGN** · **Keep ACL lean A** · **Never force-reset pilot** · reopen COMPLETE `.4.2`/`.4.7`/`.4.9`/`.4.10`/`.4.11`/`.4.12` / V3 pin / suite grant / Belam wake **OOS** · never git rm · never strip pytest · season3/capsule untouched · SoT mail=**box**

## Byte facts

| # | claim | measured | YES/NO |
|---|---|---|---|
| 1a | Leaf `.4.13` PRESENT @ SM tip; mint match; active; parent `.4` | `.agi/nodes/goal/g5.4.1.4.13.md` @ `779ab9b12`; mint_id `5e5886f44ca24db68a70b9cf62a12726`; `status: active`; parents `goal:g5.4.1.4`; tags `corrective`+`verify`+`bin-suite`+`design`+`suite`+`residue`+`envfile`. **Absent** on live `2ba49b5df` and posts/belam `18980cc83` | **YES** |
| 1b | Package ASK + DESIGN docs (workspace) | `sm-council-ask-20261006-x.md` + `DESIGN-g5.4.1.4.13-suite-window-envfile.md` + `DESIGN-batch-gate-x.md` + `SENDTO-lens-asks.txt` + `ready-for-gate-body.txt` PRESENT under `/workspace/proposals/council-gate-20261006-x/`. **No** `.agi/context/proposals/council-gate-20261006-x/` and **no** `council-design/gate-x/` on SM tip `779ab9b12` / live (N-note). Contrast: gate-w package **is** on SM tip | **YES** (workspace) |
| 2a | bin-suite-fresh SUITE REQUIRED = envfile.py mtime > suite stamp | Host MAIN: `extensions/agi/bin/envfile.py` mtime `1791331157.07` (~2026-10-06 23:59:17Z / **19:59 ET**); `.agi/sessions/verify-suite-ts.json` `suite_ran_at` `1791326730.63` (~22:45:30Z / **18:45 ET**) on `512f066c…`; **delta ≈4426s (~73.8 min newer)**. Last commit touching envfile.py = land `2ba49b5df`. No suite grant on land — SUITE REQUIRED binding without inventing GRANT | **YES** |
| 2b | Relation to prior `.4.9` / `.4.9.1` suite-window | `.4.9` **complete** @ SM `779ab9b12` (mint `7b72df8c…`); `.4.9.1` **complete** @ SM+LAND. New residue is **sibling under `.4`**, not reopen `.4.9`. Same standing posture as V1: council→SM→**SM ASK Belam ONE suite grant**→operate | **YES** |
| 2c | gate-w COMPLETE / leave-alones OOS | `.4.12` **complete** @ SM `779ab9b12` (mint `572ea49f…`); `.4.12.1` **complete** @ SM+LAND. `.4.7`/`.4.10`/`.4.11` **complete** @ SM. Live LAND still shows `.4.12`/`.4.9` **active** (tip skew — not reopen). Smoke .env/loop.log closed by `.4.12.1` — **OOS** this package | **YES** |
| 2d | ACL lean A still held | Host MAIN `.env`: mode **640** belam:belam; `getfacl -p` → `group:agi:r--` (mask `r--`). KEEP — never chmod 600 stripping group ACL | **YES** |
| 3a | Live pilot SHA | `2ba49b5dfb5875f701413a0892c46a47246ab6cf` (gate-w scrub; tip^1 `f9515d8fa`) | **YES** |
| 3b | season3 pin | `4b8f28b5e16373dd4de6b58e25f099deed4a48f1` (`core/season3/main`); ancestor of live HEAD | **YES** |
| 3c | capsule pin | `fda4efd6e4bd649f3b436d0aaa0c77c9975ba106`; ancestor of live HEAD | **YES** |
| 3d | V3 / engine pin (OOS leave alone) | `engine_commit` = `219be1832c258d4847572f2e552d95f5230e2f6d` @ live — do **not** reopen `.4.11` | **YES** |
| 3e | No Belam land of this DESIGN | Belam `18980cc83` — leaf + package **absent** | **YES** |
| 3f | SM tip vs LAND ancestry | Neither ancestor of the other (SM COMPLETE tip carries mint after land scrub) — fold against SM-tip leaf + live pilot measure | **YES** |

## Cuts for ONE design

### X1 — g5.4.1.4.13 ONE suite window clear bin-suite-fresh (envfile.py) (ACCEPT)
Standing path (same posture as gate-v V1 `.4.9`): child under `.4` lineage — council DESIGN → SM gate → **SM ASK Belam for ONE suite grant** → operate (`verification.py` window → one-file / named pytest under grant **citing `envfile.py`** → `commands.py run verify`) until `bin-suite-fresh` PASS. **Never** open suite window from this DESIGN/mint. **Never invent GRANT**. **Never** reopen `.4.9` / `.4.12` / `.4.2` / `.4.7` / `.4.10` / `.4.11` COMPLETE as dump. Falsifier: `bin-suite-fresh` PASS; lock absent MAIN + all post worktrees. Never strip pytest · never write.py · never git rm · DG held · No Belam until SM ASK · KEEP ACL lean A.

### Batch posture (ACCEPT)
- Writer = Write/Edit + `agi-turn` — **never write.py**.
- **DG held.** **No Belam box** from this package. **No suite grant** until SM ASK after council+SM PASS.
- Do **not** reopen `.4.2` / `.4.7` / `.4.9` / `.4.10` / `.4.11` / `.4.12` COMPLETE/leave-alone; do **not** strip ACL lean A; do **not** mix gate-w smoke / V3 pin / write-path g5.4.1.6.
- season3 `4b8f28b5e` / capsule `fda4efd6e` untouched. Do not waive X1 as footnote.
- Negative: Belam wake; suite self-grant; DG BUILD before SM PASS; strip ACL/pytest; git rm; invent heads; force-reset pilot; silent waive; reopen gate-w/v COMPLETE children.

## Holes (RETURN)

*(none)*

## N-notes for land/pen (not holes)

1. **Package tip skew:** DESIGN docs live in workspace `proposals/council-gate-20261006-x/`; **no** `.agi/context/proposals/council-gate-20261006-x/` / `council-design/gate-x/` on SM tip `779ab9b12` / live. Pen/SM fold against workspace package + SM-tip leaf mint — do not invent ET package path presence. (gate-w package **is** present on SM tip — x is not yet.)
2. **Leaf tip skew:** `.4.13` on SM tip only; absent live/Belam until land.
3. **Parent COMPLETE skew:** `.4.12`/`.4.9` **complete** @ SM tip; still **active** @ live pilot — measure COMPLETE from SM tip post-land stamp; **not** a reopen cue on live active. `.4.2` reverse: **complete** @ LAND, still **active** @ SM tip — still do not reopen.
4. **Suite evidence without GRANT:** mtime vs `verify-suite-ts.json` proves envfile.py newer (~73.8 min); DESIGN/ASK prose naming SUITE REQUIRED is consistent. Do **not** run suite or invent window from this DESIGN to "confirm" further.
5. **SM tip ⟂ LAND tip:** neither ancestor — SM COMPLETE minted residue after gate-w land scrub; fold leaf@SM + measure@live.
6. OOS: reopen gate-w/v COMPLETE children · V3 pin · Belam wake · suite grant · force-reset pilot · strip ACL lean A · write-path g5.4.1.6 · Master · season3 rewrite · smoke .env/loop.log (closed `.4.12.1`).

## Verdict for pen

**PASS lean** — X1 ONE suite window citing `envfile.py` (SM ASK→Belam grant; no grant here) · batch posture. Leaf active @ SM `779ab9b12` mint `5e5886f44ca24db68a70b9cf62a12726`; package @ workspace mirror; pins hold; ACL lean A held; suite mtime evidence measured; no hard invariant fail.

Ready-for-gate → SM **after** SP folds ONE RULING (alive + aio). Do not start DG. Do not box Belam. Do not ask suite grant yet. Reopen COMPLETE parents / V3 stay OOS. Never git rm. Never strip pytest. Never force-reset pilot `2ba49b5df`. Never chmod 600 stripping `group:agi:r--`. Never invent GRANT.
