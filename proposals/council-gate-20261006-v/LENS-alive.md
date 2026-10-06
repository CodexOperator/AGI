# LENS alive — gate-v DESIGN (verify-red residues V1–V3)

**Verdict:** **PASS lean** · 2026-10-06 ~18:28 ET · **measured on ET** (read-only) · **box tips:** SP `ef2d5d43b` · SM `bbd94a332` · AIO `95a8f6eb7`
**Against:** SM tip `72d4da5a8` (`72d4da5a8690679a7de0f32d7c38fd0503f7bf9c`) · **Prime mint SoT** `2c9172e68` (`2c9172e6838cd82d02a7b7c6c8714fa356aaeeca`) · **Live pilot** `ce34b336b` (`ce34b336b9ab9ff77967d137a61e7ce6f9991416`) · parent climb `.4.2` COMPLETE @ `1617aff10` — **do not reopen**
**Package:** `proposals/council-gate-20261006-v/` (+ SM `.agi/context/proposals/council-gate-20261006-v/`) · Pen=self-perpetuating · lenses=alive+aio
**Leaves:** `g5.4.1.4.9` · `g5.4.1.4.10` · `g5.4.1.4.11`
**DG held** · **No Belam** · **No suite grant from this DESIGN** · **Keep ACL lean A** · **Never force-reset pilot** · gate-t / write-path g5.4.1.6 / reopen COMPLETE parents / U1 land stream **OOS** · never git rm · never strip pytest · season3/capsule untouched · SoT mail=**box**

## Byte facts

| # | claim | measured | YES/NO |
|---|---|---|---|
| 1a | Parent `.4.2` COMPLETE @ climb (do not reopen) | `status: complete` @ climb `1617aff10` + live `ce34b336b` + Prime `2c9172e68`; mint_id `08d1a05b053c4a2d98965f5a46bd98bb`. **N:** SM tip `72d4da5a8` still shows `status: active` (lag — not a reopen signal) | **YES** |
| 1b | V1 leaf `@ Prime/live` | `.agi/nodes/goal/g5.4.1.4.9.md` PRESENT @ `2c9172e68`/`ce34b336b`; mint_id `7b72df8c367e414eb3f2a8eade603da9`; `status: active`; parent `g5.4.1.4.2`; tags `bin-suite`+`design`+`suite`. **Absent** on SM tip `72d4da5a8` (package-only there) | **YES** |
| 1c | V2 leaf `@ Prime/live` | `g5.4.1.4.10` PRESENT @ Prime/live; mint_id `c538491cc5f84b89a29e838226bad3d2`; active; parent `g5.4.1.4`; tags `smoke`+`acl`+`env`+`design`. Absent on SM tip | **YES** |
| 1d | V3 leaf `@ Prime/live` | `g5.4.1.4.11` PRESENT @ Prime/live; mint_id `4939ad2657cd403fae8e54f263b3201c`; active; parent `g5.4.1.4`; tags `smoke`+`pin`+`engine`+`design`. Absent on SM tip | **YES** |
| 2a | SM package present | ASK + DESIGN-batch + DESIGN V1/V2/V3 + DRAFT-RULING PRESENT @ `72d4da5a8` under `.agi/context/proposals/council-gate-20261006-v/` | **YES** |
| 2b | No suite grant in this DESIGN | Batch + V1 DESIGN: SM ASK → Belam grant **after** council+SM PASS; never self-grant / never grant from this package | **YES** |
| 2c | ACL lean A stands (V2) | Host MAIN `.env`: mode **640**; `getfacl -p` shows `group:agi:r--`. U2 `.4.7` `status: complete` @ SM `72d4da5a8` (node absent on live/Prime — ACL host-applied). DESIGN keeps lean A; never strip | **YES** |
| 2d | Never force-reset pilot (V3) | DESIGN+batch reject force-reset/ff pilot to old pin; live pilot `ce34b336b` = gate-t+u-u1 product; `2c9172e68` and `853090aa1` ancestors of live | **YES** |
| 3a | Engine pin `179f95602839` | `.agi/config.json` `engine_commit` = full `179f9560283936fae421e08002ef9db38d7f1e25` @ live+Prime. Short `179f95602839` is that cell. `git rev-parse --verify …^{commit}` **fails** in `/data/work/agi` (string pin, not resolvable object here). Drift named vs HEAD `853090aa1` at mint; live now `ce34b336b` | **YES** |
| 3b | season3 pin | `4b8f28b5e16373dd4de6b58e25f099deed4a48f1` | **YES** |
| 3c | capsule pin | `fda4efd6e4bd649f3b436d0aaa0c77c9975ba106` | **YES** |
| 3d | No Belam land of this DESIGN | Belam tip `18980cc83` — package + V leaves **absent** | **YES** |
| 3e | Owner verify residue (named) | Leaves quote FAIL 2/13: smoke (.env 640 / loop.log PE / engine pin drift) + bin-suite-fresh SUITE REQUIRED (boxes/rotate/send mtime). Host now: `.env` 640+lean A; `.agi/loop.log` `-rw-rw-r--` belam:belam (PE residue still DESIGN-owed) | **YES** |

## Cuts for ONE design

### V1 — g5.4.1.4.9 ONE suite window clear bin-suite-fresh (ACCEPT)
Standing path: child under `.4.2` lineage — council DESIGN → SM gate → **SM ASK Belam for ONE suite grant** → operate (`verification.py window` → one-file pytest under grant → `commands.py run verify`) until `bin-suite-fresh` PASS. **Never** open suite window from this DESIGN/mint. **Never** reopen `.4.2` COMPLETE as dump. Falsifier: `bin-suite-fresh` PASS; lock absent MAIN + all post worktrees. Never strip pytest · never write.py · never git rm · DG held · No Belam until SM ASK.

### V2 — g5.4.1.4.10 smoke .env 640 + loop.log PE; ACL lean A (ACCEPT)
Standing path: reconcile smoke expect-600 with durable ACL lean A — **keep** `group:agi:r--` (never chmod 600 that strips group ACL); adjust expect and/or labeled soft-skip. Close `.agi/loop.log` PE for agi-belam (readable or labeled skip). Do **not** reopen U2 `.4.7` COMPLETE / `.4.2`. Do **not** apply more ACL from this package. Falsifier: smoke no unnamed `.env mode 640` fail; no unnamed loop.log PE; `getfacl -p .env` still `group:agi:r--`. Never write.py · never git rm · DG held.

### V3 — g5.4.1.4.11 engine pin drift `179f95602839` (ACCEPT)
Standing path: reconcile pin vs HEAD — advance `engine_commit` in `.agi/config.json` to **current live pilot** (now `ce34b336b`, not stale gate-t `853090aa1`) **or** document labeled pin policy PASS. **Never force-reset / ff pilot backward** to old pin. Falsifier: verify smoke shows no engine pin drift naming `179f95602839` (pin==HEAD or labeled policy). Never waive as footnote · never write.py · never git rm · DG held.

### Batch posture (ACCEPT)
- Writer = Write/Edit + `agi-turn` — **never write.py**.
- **DG held.** **No Belam box** from this package. **No suite grant** until SM ASK after council+SM PASS.
- Do **not** reopen `.4.2` / `.4.7` COMPLETE; do **not** strip ACL lean A; do **not** mix gate-t / gate-u-u1 / write-path g5.4.1.6.
- season3 `4b8f28b5e` / capsule `fda4efd6e` untouched. Do not waive V1–V3 as footnotes.
- Negative: Belam wake; suite self-grant; DG BUILD before SM PASS; strip ACL/pytest; git rm; invent heads; force-reset pilot; silent waive.

## Holes (RETURN)

*(none)*

## N-notes for land/pen (not holes)

1. **Leaf tip skew:** V1–V3 nodes live on Prime `2c9172e68` / live `ce34b336b`; SM tip `72d4da5a8` carries **package only**. Pen/SM fold against package + Prime/live leaf mint_ids — do not invent SM-tip leaf presence.
2. **`.4.2` SM lag:** COMPLETE on climb/live/Prime; SM tip still `active`. Measure COMPLETE from climb `1617aff10` / live — **not** a reopen cue.
3. **`.4.7` node skew:** COMPLETE stamp on SM tip; node absent on live/Prime. Host ACL lean A applied — binding for V2.
4. **Pin object:** `179f95602839…` is config string cell; not resolvable as commit in `/data/work/agi` today. Advance-to-live or labeled policy — never rewind pilot to that string.
5. OOS: gate-t product reopen · U1 land stream · write-path g5.4.1.6 · Belam wake · Master · season3 rewrite.

## Verdict for pen

**PASS lean** — V1 ONE suite window (SM ASK→Belam grant; no grant here) · V2 reconcile smoke vs ACL lean A + close loop.log PE (keep lean A) · V3 advance pin to live / labeled policy (never force-reset pilot) · batch posture. Leaves active @ Prime `2c9172e68` / live `ce34b336b` with mint_ids above; package @ SM `72d4da5a8`; pins hold; no hard invariant fail.

Ready-for-gate → SM **after** SP folds ONE RULING (alive + aio). Do not start DG. Do not box Belam. Do not ask suite grant yet. gate-t / reopen COMPLETE parents stay OOS. Never git rm. Never strip pytest. Never force-reset pilot `ce34b336b`.
