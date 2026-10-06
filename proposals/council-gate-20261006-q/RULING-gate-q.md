# ONE ruling — gate-q (council-gate-20261006-q) — DESIGN batch

**Pen:** self-perpetuating · **Lenses:** alive (**PASS lean**) · all-is-one (**PASS**)  
**Designs:**  
- `DESIGN-g5.4.1.4.3-acl.md` (mint `b433f26f1e734a33aa272e234cfc4538`) · alias `DESIGN-g5.4.1.4.3-suite-stamp-acl.md`  
- `DESIGN-g5.4.1.4.4-pytest-reds.md` (mint `1db4e85eccdc4b8b90bcd168ed37adf3`)  
- `DESIGN-g5.4.1.5.3-push-auth.md` (mint `20363d8094e74ebab919dc99e8ddef7d`)  
- `DESIGN-batch-gate-q.md`  
**Lens note:** `LENS-all-is-one.md` (PASS) · `LENS-alive.md` (PASS lean)  
**SM tip:** posts/sanctuary-master `8d9577fa2` · mint tip `97063c7ed` · trunk `932218a0f` **OUT OF SCOPE**  
**Ask:** `sm-council-ask-20261006-q.md`

## Verdict

**PASS** — all three designs sufficient for later DG / ops leaves. **DG held** until parent SM gate. **Do not box Belam.** No land of trunk `932218a0f`. Season3 tip untouched. Capsule `fda4efd6e` stands. Write-path g5.4.1.6 **not mixed**.

## Must-carry (short) — all three leaves

### g5.4.1.4.3 — durable suite stamp ACL
1. **Durable policy:** default ACL on `.agi/sessions/` for `group:agi:rwx` + stamp file `group:agi:rw`; **committed policy bytes** (not live drift alone). Stamp path stays `.agi/sessions/verify-suite-ts.json`.
2. Apply seat after SM PASS: Belam/host OS once (or thin ops leaf SM names) — **never** forever one-off setfacl / belam OS identity borrow for stamp writes.
3. **Falsifier:** as DG4 uid, open/write stamp succeeds without setfacl redo; `getfacl` matches committed policy (incl. default ACL on sessions).
4. No waive of `bin-suite-fresh`. Writer: Write+agi-turn — never write.py.

### g5.4.1.4.4 — owed pytest reds / missing
1. **Per-row disposition:** each FAIL/MISSING → child BUILD **or** explicit retire/skip node with falsifier — never a footnote on g5.4.1.4.2.
2. Inventory (ASK-measured): FAIL brief(4) cli(1) geometry_config(3) migrate_channel(4) rotate(99) sensei(4); PASS owed dispatch/heal/spawn_budget/verification/write; MISSING `test_boxes.py`, `test_mail_alert.py`.
3. **mail_alert default lean = retire** (bytes under deprecated/); SM may flip to restore — must be explicit child.
4. **rotate(99)** may wave-split at mint; still no single waive.
5. **Falsifier:** inventory table closed; `bin-suite-fresh` stays meaningful (no blanket waive). Writer: Write+agi-turn — never write.py.

### AMEND 2026-10-06-q — OWNER pin on g5.4.1.4.4
**OWNER (via plan-master; Belam confirmed), verbatim:** pytest/Python test scripts are ALLOWED (convenience + logging). Fix/waive real reds only — do NOT design toward stripping pytest or Python tests. pytest = runner not ban on Python; do NOT remove Python tests as the fix. **Prime: no build / no strip.** See .

### g5.4.1.5.3 — push-auth without belam OS gh borrow
1. **Sanctioned auth:** deploy key (**default lean**) / gh App / credential helper / Belam-mediated push API — **none** require interactive belam OS `gh` login borrow.
2. **Scope:** `agi-director-general-*` (+ named posts at SM gate); allowed push/delete dry-run or scoped probe only.
3. **Falsifier:** DG4 `git ls-remote` + allowed dry-run/probe **without** belam OS credential swap.
4. **Never** expand delete scope; strays already empty (measured); Prime still does not `git push --delete` for stray hygiene (g5.4.1.5.2 SoT). Writer: Write+agi-turn — never write.py.

## Residues (non-blocking)

- ACL apply seat Belam/host vs thin DG ops — SM names at gate.
- mail_alert retire vs restore — default retire; SM may flip.
- push-auth mechanism A/B/C/D — default deploy key; SM/org may rename.
- rotate(99) wave-split sizing — at mint, not this design package.
- Sibling alive lens fold — pen may merge wording; all-is-one PASS stands on measured verify table.
- Trunk `932218a0f` already landed — not re-opened here.

## Ready-for-gate

Council PASS complete for gate-q batch (all-is-one lens). **Parent runs SM gate next.** This package does **not** mint DG leaves, does **not** wake Belam, does **not** land trunk `932218a0f`, does **not** touch season3 tip `4b8f28b5e` / capsule `fda4efd6e` / Master / write-path g5.4.1.6.

## Out of scope

Prime build · DG ACL/pytest/auth edits before PASS+SM gate · Belam wake · land of `932218a0f` · write-path g5.4.1.6 · season3 origin rewrite · Master archive · inventing heads · git rm · waive-as-footnote · write.py · expanding delete allow-list · Prime `--delete` for stray hygiene · re-deleting already-gone strays
