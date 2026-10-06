# ONE ruling — gate-n (council-gate-20261006-n) — DESIGN

**Pen:** self-perpetuating · **Lenses:** alive · all-is-one  
**Design:** `DESIGN-g5.4.1.5.1-stray-delete.md` (mint `8fd28a192afe49e9ae483ebc3502fc3f`)  
**Lens note:** `LENS-all-is-one.md`  
**ASK tip:** posts/sanctuary-master `85c3924af` · Belam mint tip `e7c96fb2e`  
**Ask:** `sm-council-ask-20261006-n.md`

## Verdict

**PASS** — design sufficient for a later DG delete-ops leaf. **DG held** until parent SM gate. **Do not box Belam.** Do not start DG. Season3 tip untouched. Capsule `fda4efd6e` stands. Do not interfere with DG4 links/suite (g5.4.1.1.7.1 / g5.4.1.4.1).

## Must-carry (short) — g5.4.1.5.1

1. **Exact two refs:** `refs/heads/season2/main` @ `b0608a1f32d3fa8668399e58ba7320280565acad` · `refs/heads/belam/capsule-rows` @ `1ea2129b51e844f156869e438f69d6b5c3100f75`. Never touch `core/season2/main`, `core/season3/main`, `core/season2/et-grok-pilot`, `core/main`, Master, or other graph-described trunks.
2. **DG = delete operator** under SM gate: `git push origin --delete season2/main belam/capsule-rows` (or two single-ref deletes). **Never Prime.**
3. **Belam land = falsifier only** — confirm `ls-remote` empty after DG delete lands via MUR; land does not push `--delete`.
4. **SHA reconfirm** at build time against measured tips above; refuse if tip moved to unexpected value without SM re-GO; skip if already gone.
5. **Falsifier:** `git ls-remote origin refs/heads/season2/main refs/heads/belam/capsule-rows` empty for both.
6. **Loop-only:** council design → SM gate → DG delete → climb/MUR → Belam land falsifier.
7. **DG held** until SM gate stamps.
8. **Do NOT touch** season3 `4b8f28b5e` / Master / capsule `fda4efd6e`.
9. **Do NOT interfere** with concurrent DG4 links/suite (g5.4.1.1.7.1 / g5.4.1.4.1).

## Residues (non-blocking)

- Exact DG assignee identity → parent SM gate.
- If a stray tip drifts between design PASS and DG build without SM re-GO → STOP/escalate (already named in design).
- Concurrent DG4 suite/links — separate tracks; this ruling does not wake or block them.

## Ready-for-gate

Council PASS complete for gate-n. **Parent runs SM gate next.** This package does **not** mint DG leaves, does **not** wake Belam, does **not** delete any ref, does **not** touch season3 tip `4b8f28b5e` / capsule `fda4efd6e` / Master / DG4 links/suite.

## Out of scope

Prime `--delete` · DG deletes before PASS+SM gate · season3 tip rewrite · Master archive · inventing heads · reopen g5.4.1.1.7* / g5.4.1.4* / g5.4.1.2* · git rm nodes · waive-as-footnote
