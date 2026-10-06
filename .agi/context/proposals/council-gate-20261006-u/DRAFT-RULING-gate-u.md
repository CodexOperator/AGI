# DRAFT ONE ruling — gate-u (council-gate-20261006-u) — DESIGN batch U1–U3

**Pen:** self-perpetuating · **Lenses:** alive (**PASS lean** · `LENS-alive.md` · box tips `8c72767f3` / peer relay `6faf241e8`) · all-is-one (**pending**)  
**Designs:**  
- `DESIGN-g5.4.1.4.6-test-boxes.md` (mint `594456f7bb7e44a0817448278714699c`)  
- `DESIGN-g5.4.1.4.7-env-perm.md` (mint `433ab7c8a8b54af48d024af9e4f94db4`)  
- `DESIGN-g5.4.1.4.8-spawn-budget-lock.md` (mint `82d355870dbb45c5a9155b1af5c120fe`)  
- `DESIGN-batch-gate-u.md`  
**SM mint tip (U leaves SoT):** `04aedac1d` · **climb parent PASS:** `1617aff10` (bin-suite-fresh — **do not reopen**)  
**Ask:** `sm-council-ask-20261006-u.md`  
**Land binsuite / tip `04aedac1d` land-stream OUT OF SCOPE** (separate land pen — cite mint only)

## Verdict

**PASS pending lens fold** (alive PASS lean in; all-is-one owed). Design sufficient for SM gate on U1–U3 residues of bin-suite-fresh. **Binding leans:**  
- **U1** = committed `test_boxes.py` (help + behavioral; never strip)  
- **U2** = durable MAIN `.env` `group:agi:r` + policy (lean A; labeled skip only on SM flip)  
- **U3** = durable `.agi/sessions/.spawn-budget` + `.lock` `group:agi:rw` + policy (lean A; labeled skip only on SM flip)  

**DG held** until parent SM gate. **Do not box Belam.** Season3 tip untouched. Capsule `fda4efd6e` stands. Gate-t / write-path g5.4.1.6 / `.4.3.*` reopen / land-binsuite **not mixed**.

**Ready-for-gate: BLOCKED until all-is-one returns PASS|AMEND|RETURN and pen/parent folds ONE RULING.**

## Must-carry (short) — THREE leaves

### U1 · g5.4.1.4.6 — test_boxes.py
1. Add `extensions/agi/tests/test_boxes.py` covering `boxes.py` (help + behavioral floor).  
2. One-file pytest green under suite-window; `bin-suite-fresh` still PASS.  
3. **Never strip** existing tests. Writer Write+agi-turn — never write.py. Never git rm.  
4. **Falsifier:** file PRESENT + one-file green + bin-suite-fresh PASS. Negative = waive footnote / strip / write.py / Belam / DG-before-PASS / mix OOS.

### U2 · g5.4.1.4.7 — .env perm
1. Measured: `.env` = `belam:belam` 600; DG4 READ_FAIL → smoke/anonymize PE.  
2. **Lean A:** `setfacl -m g:agi:r-- .env` + committed policy (Belam/host after SM PASS).  
3. **Falsifier:** as DG4, smoke+anonymize PASS or labeled skip — no unnamed PE. Do not reopen `.4.3.*`.

### U3 · g5.4.1.4.8 — spawn-budget lock
1. Measured: `.agi/sessions/.spawn-budget/.lock` belam-owned; DG4 append → PE (read OK).  
2. **Lean A:** named+default `group:agi:rwx` on budget dir + `group:agi:rw` on lock + policy.  
3. **Falsifier:** as DG4, budget PASS or labeled skip — no unnamed PE. Do not reopen `.4.3.*`.

## Residues / streams (keep separate)
- Land binsuite (tip `1617aff10` / MUR `04aedac1d` land ASK) = **separate pen** — not this DESIGN fold.  
- Gate-t send.py MOVE = **OOS**.  
- Suite-stamp ACL `.4.3.*` = closed/adjacent — do not reopen to absorb U2/U3.

## Ready-for-gate

**BLOCKED** — awaiting all-is-one lens (PASS|AMEND|RETURN) with path. Alive **PASS lean** already filed. Parent folds lenses → final RULING → then ready-for-gate to SM. This DRAFT does **not** mint DG leaves, does **not** wake Belam, does **not** land binsuite, does **not** touch season3 `4b8f28b5e` / capsule `fda4efd6e` / Master / gate-t / `.4.3.*`.

## Out of scope

Prime build · DG before PASS+SM gate · Belam wake · land-binsuite · gate-t MOVE · reopen `.4.2`/`.4.3.*` · write-path g5.4.1.6 · git rm · invent heads · season3 rewrite · Master · write.py · strip pytest · waive-as-footnote · new land vote from this package
