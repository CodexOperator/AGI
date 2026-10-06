# SM MUR PASS — g5.4.1.3.2 + g5.34.10.2 (director-general-4)

**Verdict:** PASS · **Belam:** NOT contacted (parent owns Belam after council) · **Council:** queued after this MUR  
**Tip:** `b0754014b` (`b0754014be9e8e27170ba8d3415ec247b39e885a`) on `de-dg4-1` / `posts/director-general-4`  
**Ancestors:** g5.4.1.3.2 `75c1b5939` · g5.35.4 corrective `96a85aeea` · wave-2 `ae180ab6d`  
**Date:** 2026-10-06 ~17:15Z · **Post:** sanctuary-master · **Skill:** agi-master-gate  
**SM baseline at gate:** `1e69fafcc`  
**Climb:** DG4 BUILD `18005cc99` (g5.4.1.3.2 @ `75c1b5939`) · DG4 BUILD `5495be49d` (g5.34.10.2 @ tip) · DG2 PASS `48f39f22b` · DG1 PASS `3bb6f261e`  
**Trunk note:** wave-2 + corrective already on `core/season2/et-grok-pilot` (`63c304a1d`); tip `b0754014b` not yet landed (Belam after council). Gate DG4 tip bytes; do not require trunk land first.

## Bytes proven (independent re-measure @ tip b0754014b)

| leaf | check | measured | want |
|---|---|---|---|
| **g5.4.1.3.2** ### slice | `engine-post.md` heading `### slice (5234 B)` | **present** (added vs `96a85aeea`) | present |
| **g5.4.1.3.2** bin/slice | `/var/lib/agi/director-general-4/bin/slice` | **present 5234 B**; sha256 `b767f59f…271cd7` **==** tip ### slice body | byte-identical |
| **g5.4.1.3.2** F1 | `refs/slice/demo-g54132` | **`aa7bf8dfdd22aac025faaa6f87b9cee36873290e`** | that tip |
| **g5.4.1.3.2** F2 | `cat-file -t …:nodes/89c8ebee3f62436cafe2e56289ea5843` | **blob** | blob |
| **g5.4.1.3.2** F3 | `refs/grid/et-grok-pilot/node/89c8ebee…` | **`35f5ffbe3be9b3dc553618715036c1eb8ae625b9`** (via slice move --to-grid) | that tip |
| **g5.4.1.3.2** F4 | `encrypt\|seal\|cred\|ring` on ### slice piece | **CLEAN (0)** | 0 |
| **g5.4.1.3.2** F5 | `core/season3/main` | **`4b8f28b5e`** unchanged; no `--apply` verb in piece | 4b8f28b5e |
| **g5.34.10.2** grid_sync | `cadences.grid_sync.enabled` @ tip | **`true`** (was false @ `96a85aeea`); every_mins:5 + mirror_towns:true kept | true |
| **g5.34.10.2** branch_push | `cadences.branch_push.enabled` @ tip | **`true`** (was false); schedule `7 * * * *` kept | true |
| **g5.34.10.2** storage_trunk | `.agi/config.json` grid.storage_trunk @ tip + LIVE | **`refs/grid/et-grok-pilot`** | that ref |
| **g5.34.10.2** catch-up | new catch-up runbook in range | **NONE** — only `OWNER-CORRECTION-catch-up-drop.md` (DROP); goals strike bulk `grid.py commit --all` | no runbook |
| **non-reg** tmux live | `git grep -nE 'tmux (kill-window\|new-session\|send-keys\|attach)\|tmux agi-rc' tip -- skills` | **CLEAN (0)** | 0 |
| **non-reg** banned teach | `send.py\|workflow.py\|season2/` in skills (ex deprecated) | **CLEAN (0)** | 0 |
| posts.md / keys | tip vs `96a85aeea` delta; A-adds | **none** | none |
| evidence | `g5.4.1.3.2-BUILD-evidence.md` + `g5.34.10.2-BUILD-evidence.md` | on tip (bodies cite intermediate tips `052141bb6` / `e0f4528de`; final tip = `b0754014b`) | real |

**Range vs corrective `96a85aeea`:** 25 files — council-gate -g/-h (design+evidence+OWNER-CORRECTION) + goals g5.4.1.3{,.1,.2} / g5.34.10{,.1,.2} + geometry `engine-post.md` (### slice) + `crons.md` (two enabled flips). No skills / posts.md / other-track churn beyond those leaves.

## Climb
| seat | box sha | vs |
|---|---|---|
| DG4 BUILD g5.4.1.3.2 | `18005cc99` | tip `75c1b5939` CLAIM MET (ancestor of `b0754014b`) |
| DG4 BUILD g5.34.10.2 | `5495be49d` | tip `b0754014b` CLAIM MET |
| DG2 | `48f39f22b` | exp+verdict @ `4c9b41ae4` (review-only) PASS |
| DG1 | `3bb6f261e` | hyps @ `f81645626` (review-only) PASS |

## SM decision stamps
1. **g5.4.1.3.2** — **PASS** ### slice pack/move in engine-post → bin/slice; F1–F5 hold; SoT comment names `/var/lib/agi/$P/bin/slice` (not extensions/agi/bin/). Method: Write/Edit+agi-turn (engine.v4); never git rm.
2. **g5.34.10.2** — **PASS** grid_sync.enabled + branch_push.enabled → true; storage_trunk untouched `refs/grid/et-grok-pilot`; NO catch-up runbook (owner drop). Live `crons.py apply` → Belam after council (not run by SM/DG4).
3. **Land** — SM does NOT merge/ff trunk or posts/belam. Belam lands tip after council (parent wakes). Never git rm. No push. season3 tip untouched. Wave-2/corrective already on trunk — this tip stacks on that land.

## Residues (non-blocking → Belam after council)
- Live `python3 extensions/agi/bin/crons.py apply --unit-dir ~/.config/systemd/user` from `/data/work/agi` after land (DG4 land note; SM did not apply).
- Evidence body tip SHAs = intermediate BUILD commits; final tip = `b0754014b` (cosmetic doc drift only).
- Soft target ~2500 B for ### slice body deferred (DG R1 chose 5234 B; verbs complete) — non-blocking density residue.

## Blocking Belam land?
**None** for committed tip bytes after this MUR. Sequencing: council review (this gate boxes seats); Belam land after council PASS (parent only — SM does not box Belam).

## Out of scope (untouched)
wave-2 / g5.35.* re-open · season3 tip · Belam contact · Master merge · push · git rm · live crons.py apply · AA3 / local-maxxing / ramdisk.

## Decision
**PASS** tip `b0754014b` covering g5.4.1.3.2 + g5.34.10.2. Gate doc this commit on `posts/sanctuary-master`. Council queued; Belam = parent only.
