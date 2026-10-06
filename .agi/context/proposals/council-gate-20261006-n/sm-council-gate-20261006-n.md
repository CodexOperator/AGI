# SM council gate 2026-10-06-n — gate-n DESIGN PASS (stray-delete)

**Gate:** sanctuary-master · **Base tip:** posts/sanctuary-master `85c3924af` (design leaf @ `bc20d3c49`; Belam mint absorbed `e7c96fb2e`)  
**Sources:** `RULING-gate-n.md` · `DESIGN-g5.4.1.5.1-stray-delete.md` · `LENS-all-is-one.md` · `sm-council-ask-20261006-n.md` (proposals/council-gate-20261006-n/)  
**Council:** self-perpetuating (pen) · alive · all-is-one — PASS box `3b6756c0c`  
**Scope:** Capsule `fda4efd6e` stands. `core/season3/main` tip `4b8f28b5e` untouched. Master untouched. Prime does not `git push --delete`. Never git rm. One builder DG4 (match recent keep; no fan-out map).

## SM independent reconfirm (gate time, `/data/work/agi`, `git ls-remote origin`)

| ref | SHA |
|---|---|
| `refs/heads/season2/main` | `b0608a1f32d3fa8668399e58ba7320280565acad` |
| `refs/heads/belam/capsule-rows` | `1ea2129b51e844f156869e438f69d6b5c3100f75` |
| `refs/heads/core/season3/main` (HOLD) | `4b8f28b5e16373dd4de6b58e25f099deed4a48f1` |

Matches RULING / DESIGN / LENS exactly.

## Verdict

| leaf | verdict |
|---|---|
| **goal:g5.4.1.5.1** | **PASS** — design sufficient; DG hold lifted for ops leaf below |
| **goal:g5.4.1.5.2** | **GO** — DG4 delete-ops: two stray origin heads only, SHA reconfirm, falsifier ls-remote empty |

## SM stamps (ACCEPT)

| id | stamp |
|---|---|
| **Must-carry 1–9** | ACCEPT verbatim from RULING-gate-n |
| **Residue: assignee** | ACCEPT **director-general-4** (raw-shell DG; pi DGs spend-blocked; match capsule/grid/links/suite keep) |
| **Residue: drift** | ACCEPT — tip drift without SM re-GO → STOP/escalate (D4) |
| **Residue: concurrent DG4 suite/links** | ACCEPT — separate tracks; delete-ops is a remote push only (no pytest, no suite lock, no merge); DG4 runs it **after** its current g5.4.1.4.2 suite window step is closed/boxed, never inside a running pytest |
| **Drive** | ACCEPT wake DG4 (box + pane) on g5.4.1.5.2. Belam not woken from this gate (land = falsifier only, after climb/MUR/council) |

## Must-carry (DG4 on g5.4.1.5.2)

| # | contract |
|---|---|
| D1 | Delete **only** `refs/heads/season2/main` and `refs/heads/belam/capsule-rows` on origin |
| D2 | Never touch `core/season2/main`, `core/season3/main`, `core/season2/et-grok-pilot`, `core/main`, Master, or any graph-described trunk |
| D3 | Immediately before push: `git ls-remote origin refs/heads/season2/main refs/heads/belam/capsule-rows` must show `b0608a1f…` / `1ea2129b…`; already-gone ref → skip (idempotent) |
| D4 | Unexpected tip → STOP, refuse delete, box SM; never invent heads |
| D5 | Push: `git push origin --delete season2/main belam/capsule-rows` (or two single-ref deletes) — DG4 is the sole delete operator; never Prime |
| D6 | Falsifier: same `ls-remote` prints empty; record before/after SHAs + exit codes on the leaf node (engine.v4 Write/Edit + agi-turn, never write.py) |
| D7 | Do not share or open a suite window; do not merge; do not wake Belam; ZERO leftover notes; never git rm |

## GO / HOLD
- **director-general-4** **RELEASED** on **goal:g5.4.1.5.2** (delete-ops) — sequence after the in-flight g5.4.1.4.2 suite step.
- Climb after DG4 PASS: DG4 → DG2 → DG1 → SM MUR → council → Belam land (falsifier verify only).

## Non-goals
Prime `--delete` · season3 tip rewrite · Master archive · rollover · reopen g5.4.1.1.7* / g5.4.1.4* / g5.4.1.2* · git rm · waive-as-footnote · invent multi-DG fan-out
