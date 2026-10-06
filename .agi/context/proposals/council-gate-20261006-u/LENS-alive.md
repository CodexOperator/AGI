# LENS alive — gate-u DESIGN (bin-suite residues U1–U3)

**Verdict:** **PASS lean** · 2026-10-06 ~17:54 ET · **measured on ET** (read-only) · **box tip:** `8c72767f3`
**Against:** SM tip `04aedac1d` (`04aedac1d248f6fd35bba4f16c5bc57ea1c83a5d`) · parent MUR climb `1617aff10` (bin-suite-fresh PASS — **do not reopen**)
**Package:** `proposals/council-gate-20261006-u/` (+ SM `.agi/context/proposals/council-gate-20261006-u/`) · Pen=self-perpetuating · lenses=alive+aio
**Leaves:** `g5.4.1.4.6` · `g5.4.1.4.7` · `g5.4.1.4.8` under parent `g5.4.1.4.2`
**DG held** · **No Belam** · gate-t / write-path g5.4.1.6 / reopen `.4.2` **OOS** · never git rm · never strip pytest · season3/capsule untouched · SoT mail=**box**

## Byte facts

| # | claim | measured | YES/NO |
|---|---|---|---|
| 1a | Parent `.4.2` complete @ climb | `status: complete` @ `1617aff10`; mint_id `08d1a05b…`; bin-suite-fresh PASS under grant `88f91528f` | **YES** |
| 1b | U1 leaf `@ SM` | `.agi/nodes/goal/g5.4.1.4.6.md` PRESENT @ `04aedac1d`; mint_id `594456f7bb7e44a0817448278714699c`; `status: active`; parent `g5.4.1.4.2`; tags include `design`+`tests` | **YES** |
| 1c | U2 leaf `@ SM` | `g5.4.1.4.7` PRESENT; mint_id `433ab7c8a8b54af48d024af9e4f94db4`; active; tags `acl`+`env`+`design` | **YES** |
| 1d | U3 leaf `@ SM` | `g5.4.1.4.8` PRESENT; mint_id `82d355870dbb45c5a9155b1af5c120fe`; active; tags `acl`+`budget`+`design` | **YES** |
| 2a | `test_boxes.py` missing (U1 debt) | Absent on climb `1617aff10`; boxes greened only via `test_bin_help_smoke.py -k boxes` (1p) | **YES** |
| 2b | SM package present | ASK + DESIGN-batch + DESIGN U1/U2/U3 present @ `04aedac1d` | **YES** |
| 3a | season3 pin | `4b8f28b5e16373dd4de6b58e25f099deed4a48f1` | **YES** |
| 3b | capsule pin | `fda4efd6e` resolves | **YES** |
| 3c | No Belam land of this DESIGN | Leaves minted on SM; Belam @ `18980cc83` not this package | **YES** |

## Cuts for ONE design

### U1 — g5.4.1.4.6 committed `test_boxes.py` (ACCEPT)
Standing path: add committed `extensions/agi/tests/test_boxes.py` covering `extensions/agi/bin/boxes.py` (help smoke **and** behavioral coverage — DESIGN may bound scope but must not leave boxes uncovered except via this file). Falsifier: file PRESENT; one-file pytest green under suite-window rules; `bin-suite-fresh` still PASS. **Never strip** existing tests (Owner pin). Writer Write+agi-turn — never write.py. DG held until SM PASS.

### U2 — g5.4.1.4.7 MAIN `.env` PermissionError (ACCEPT)
Standing path: durable ownership/ACL/group **or** explicit documented soft-skip policy so smoke + anonymize as DG4 uid either PASS or labeled skip — **no raw unnamed PermissionError residue**. Do not mix suite-stamp ACL leaf `g5.4.1.4.3.*`. Falsifier: as DG4, smoke+anonymize PASS or documented skip. Never write.py · never git rm · never strip pytest · DG held.

### U3 — g5.4.1.4.8 spawn-budget lock PermissionError (ACCEPT)
Standing path: durable lock-path ownership/ACL **or** explicit documented skip so budget check as DG4 either PASS or labeled skip — no unnamed PermissionError. Falsifier: as DG4, budget PASS or documented skip. Never write.py · never git rm · never strip pytest · DG held.

### Batch posture (ACCEPT)
- Writer = Write/Edit + `agi-turn` — **never write.py**.
- **DG held.** **No Belam box** from this package.
- Do **not** reopen `g5.4.1.4.2` PASS; do **not** mix gate-t MOVE / write-path g5.4.1.6.
- season3 `4b8f28b5e` / capsule `fda4efd6e` untouched. Do not waive U1–U3 as footnotes.
- Negative: Belam wake; DG BUILD before SM PASS; strip pytest; git rm; invent heads; silent waive.

## Holes (RETURN)

*(none)*

## Verdict for pen

**PASS lean** — U1 committed `test_boxes.py` · U2 durable `.env` ACL/skip · U3 durable spawn-budget lock ACL/skip · batch posture. Parent `.4.2` bin-suite-fresh stays PASS (land stream separate). Leaves active @ SM `04aedac1d` with mint_ids above; pins hold; no hard invariant fail.

Ready-for-gate → SM **after** SP folds ONE RULING. Do not start DG. Do not box Belam. gate-t / reopen `.4.2` stay OOS. Never git rm. Never strip pytest.
