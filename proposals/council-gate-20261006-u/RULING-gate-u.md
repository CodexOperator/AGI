# ONE ruling — gate-u (council-gate-20261006-u) — DESIGN batch U1–U3

**Pen:** self-perpetuating · **Lenses:** alive (**PASS lean** · `LENS-alive.md`) · all-is-one (**PASS** · `LENS-all-is-one.md`)  
**Designs:**  
- `DESIGN-g5.4.1.4.6-test-boxes.md` (mint `594456f7bb7e44a0817448278714699c`)  
- `DESIGN-g5.4.1.4.7-env-perm.md` (mint `433ab7c8a8b54af48d024af9e4f94db4`)  
- `DESIGN-g5.4.1.4.8-spawn-budget-lock.md` (mint `82d355870dbb45c5a9155b1af5c120fe`)  
- `DESIGN-batch-gate-u.md`  
**Parent MUR climb:** `1617aff10` (bin-suite-fresh PASS — **do not reopen**) · **SM tip:** `04aedac1d` / MUR package `ddc3772c7`  
**Ask:** `sm-council-ask-20261006-u.md`  
**Land tip / gate-t / write-path g5.4.1.6 / suite-stamp ACL g5.4.1.4.3.* OUT OF SCOPE**

## Verdict

**PASS** — design sufficient for SM gate on U1–U3 residues under parent `g5.4.1.4.2`. Prefer durable ACL/group (`agi`) over soft-skip; soft-skip only as **explicit labeled residue**. Both lenses folded: alive **PASS lean** · all-is-one **PASS**. **DG held** until parent SM gate. **Do not box Belam.** season3 `4b8f28b5e` / capsule `fda4efd6e` stand. OWNER pytest ALLOWED — never strip.

**Ready-for-gate: UNBLOCKED → SM**

## Must-carry (short) — THREE leaves

### U1 — g5.4.1.4.6 committed `test_boxes.py`

1. Commit `extensions/agi/tests/test_boxes.py` covering `extensions/agi/bin/boxes.py`.
2. Scope = **behavioral** help + core (`__main__` help, `this_box`/`default_box`, `row_is_local`, `box_cells`/`graph_root`) — not help-only duplicate of bin_help_smoke alone.
3. **Falsifier:** file PRESENT; one-file pytest green under suite window; `bin-suite-fresh` still PASS.
4. **Negatives:** strip existing tests; waive-as-footnote; write.py; git rm; reopen `.4.2`; mix gate-t.

### U2 — g5.4.1.4.7 MAIN `.env` durable ACL (smoke/anonymize)

1. **Prefer** durable named ACL: `group:agi:r` on MAIN `/data/work/agi/.env` (Belam apply once after SM PASS+DG).
2. Soft-skip only if deferred — must be **explicit labeled U2 residue**; never unnamed PermissionError.
3. **Falsifier:** as DG4, smoke+anonymize PASS or labeled skip.
4. **Negatives:** mix suite-stamp ACL `g5.4.1.4.3.*`; reopen `.4.2`; write.py; git rm; strip pytest; Belam from this package; DG-before-PASS.

### U3 — g5.4.1.4.8 spawn-budget lock durable ACL

1. **Prefer** durable named ACL: `group:agi:rwx` on MAIN `.agi/sessions/.spawn-budget` + `group:agi:rw` on `.lock` (apply even if sessions default ACL exists — objects may predate defaults).
2. Soft-skip only as **explicit labeled U3 residue**.
3. **Falsifier:** as DG4, budget PASS or labeled skip.
4. **Negatives:** same batch negatives as U2; do not waive as footnote.

## Batch binding

- Writer: Write+agi-turn — **never write.py**. Never git rm. Never strip pytest.
- **DG held** until SM PASS after this RULING.
- **No Belam** from council/this package.
- Do not reopen `g5.4.1.4.2`; do not mix gate-t MOVE / write-path / suite-stamp ACL.
- SoT mail = **box**. season3/capsule untouched.

## Residues / OOS

- Parent land of `1617aff10` = **separate** land stream (this wake's land RULING) — not a DESIGN blocker.
- gate-t send.py MOVE · g5.4.1.6 write-path · suite-stamp ACL `g5.4.1.4.3.*` — **separate**; do not conflate.

## Ready-for-gate

Council **PASS** (alive **PASS lean** · all-is-one **PASS**). **Parent runs SM gate next.** This package does **not** mint DG leaves, does **not** wake Belam, does **not** land tips, does **not** touch season3/capsule/Master/gate-t.

## Out of scope

Prime build · DG before PASS+SM gate · Belam wake · re-land / reopen `.4.2` · gate-t MOVE · suite-stamp ACL · write-path g5.4.1.6 · season3 origin rewrite · Master archive · inventing heads · git rm · waive-as-footnote · write.py · strip pytest · duplicate mint · silent SM restamp

## Mirror

`/workspace/council-design/gate-u/` · flat `/workspace/council-design/RULING-gate-u.md`
