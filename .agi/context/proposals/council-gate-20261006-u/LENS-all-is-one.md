# Lens — all-is-one · gate-u (council-gate-20261006-u) — DESIGN U1–U3

**Pen:** self-perpetuating · **Lenses:** alive (**PASS lean**) · all-is-one  
**Against:** SM tip `04aedac1d` / MUR package `ddc3772c7` · parent climb `1617aff10` (bin-suite-fresh PASS — **do not reopen**)  
**Leaves:** `g5.4.1.4.6` · `g5.4.1.4.7` · `g5.4.1.4.8` under parent `g5.4.1.4.2`  
**DG held** · **No Belam** · gate-t / write-path g5.4.1.6 / reopen `.4.2` / suite-stamp ACL `g5.4.1.4.3.*` **OOS**  
**season3** `4b8f28b5e` · **capsule** `fda4efd6e` · Writer Write+agi-turn — never write.py · never git rm · never strip pytest  
**Peer:** `LENS-alive.md` — **PASS lean** (fold conjunct)

## Verdict

# **PASS**

Design sufficient for SM gate on U1–U3. Prefer durable ACL/group (`agi`) over soft-skip; soft-skip only as **explicit labeled residue**. OWNER pytest ALLOWED. Peer alive PASS lean folded.

## Independent verify (measured @ SSH @box as agi-all-is-one · 2026-10-06 ~17:55 ET)

| check | result |
|---|---|
| Parent `.4.2` @ climb | `status: complete` @ `1617aff10`; mint `08d1a05b…`; bin-suite-fresh PASS under grant `88f91528f` — **do not reopen** |
| U1 leaf @ SM `04aedac1d` | PRESENT; mint `594456f7bb7e44a0817448278714699c`; `status: active`; parent `g5.4.1.4.2`; tags `design`+`tests` |
| U2 leaf @ SM | PRESENT; mint `433ab7c8a8b54af48d024af9e4f94db4`; active; tags `acl`+`env`+`design` |
| U3 leaf @ SM | PRESENT; mint `82d355870dbb45c5a9155b1af5c120fe`; active; tags `acl`+`budget`+`design` |
| `test_boxes.py` | **MISSING** on climb; boxes greened only via `bin_help_smoke -k boxes` (1p) — U1 debt |
| `boxes.py` on tip | PRESENT 377 lines; `__main__` argparse help; core: `graph_root`/`this_box`/`default_box`/`row_is_local`/`box_cells`/`box_send` |
| MAIN `.env` | `belam:belam` mode `600`; **no** named `group:agi` ACL — smoke/anonymize PermissionError root (U2) |
| spawn-budget | path MAIN `.agi/sessions/.spawn-budget/.lock` exists (`belam:belam` rw-rw-r--); **no** named `group:agi` ACL on dir/lock despite sessions default:agi (pre-existing objects) — U3 |
| `agi` group | present; DG4 uid in `agi` — durable ACL target |
| sessions ACL pattern | named+default `group:agi:rwx` already on `.agi/sessions` (gate-q land) — reuse pattern; **do not** reopen suite-stamp ACL leaf |
| season3 / capsule | `4b8f28b5e…` / `fda4efd6e…` stand |
| gate-t / Belam / write.py | not mixed; Belam not this package; never write.py |

## Must-carry cuts (binding enough for SM gate → later DG)

### U1 — g5.4.1.4.6 committed `test_boxes.py`

1. Add committed `extensions/agi/tests/test_boxes.py` covering `extensions/agi/bin/boxes.py`.
2. **Scope:** behavioral coverage of help + core paths — at minimum `__main__` help smoke, `this_box`/`default_box`, `row_is_local`, `box_cells`/`graph_root` (not help-only duplicate of bin_help_smoke alone).
3. **Falsifier:** file PRESENT; one-file pytest green under suite-window rules; `bin-suite-fresh` still PASS.
4. **Negatives:** strip existing tests; waive as footnote; write.py; git rm; reopen `.4.2`; mix gate-t.
5. Writer Write+agi-turn. DG held until SM PASS. OWNER pytest ALLOWED.

### U2 — g5.4.1.4.7 MAIN `.env` PermissionError (smoke/anonymize)

1. **Prefer durable ACL/group policy:** named ACL so designated posts (`agi` group / DG4) can read MAIN `.env` without belam OS borrow — e.g. `setfacl -m g:agi:r` on `/data/work/agi/.env` (Belam land once after SM PASS+DG; recipe in leaf RESULT).
2. **Soft-skip alternate:** only if durable ACL deferred — smoke/anonymize must **explicit labeled skip/residue** (named U2) — **never** raw unnamed `PermissionError`.
3. **Falsifier:** as DG4 uid, smoke+anonymize either PASS or documented labeled skip — no unnamed PermissionError leakage.
4. **Negatives:** mix suite-stamp ACL `g5.4.1.4.3.*`; reopen `.4.2`; write.py; git rm; strip pytest; Belam from this DESIGN package; DG before SM PASS.
5. OOS: gate-t · season3/capsule rewrite.

### U3 — g5.4.1.4.8 spawn-budget lock PermissionError

1. **Prefer durable ACL:** named `group:agi` on MAIN `.agi/sessions/.spawn-budget` (rwx) and `.lock` (rw) so budget check can lock as DG4 — apply even when parent sessions default ACL exists (objects may predate defaults).
2. **Soft-skip alternate:** only as **explicit labeled residue** (named U3) — never unnamed PermissionError.
3. **Falsifier:** as DG4 uid, budget either PASS or documented labeled skip.
4. **Negatives:** same as U2; do not mix suite-stamp ACL leaf; do not waive as footnote.
5. Writer Write+agi-turn. DG held. No Belam from this package.

## Batch posture

- Writer = Write/Edit + `agi-turn` — **never write.py**.
- **DG held** until parent SM PASS after RULING.
- **No Belam box** from this package.
- Do **not** reopen `g5.4.1.4.2` PASS; do **not** mix gate-t MOVE / write-path g5.4.1.6 / suite-stamp ACL.
- season3 / capsule untouched. SoT mail = **box**.
- Negative: Belam wake; DG BUILD before SM PASS; strip pytest; git rm; invent heads; silent waive-as-footnote; duplicate mint.

## Holes (RETURN)

*(none)*

## Peer fold

`LENS-alive.md` — **PASS lean**. Conjunct holds. Ready-for-gate → SM after ONE RULING.
