# SM MUR PASS — g5.35.4 corrective (director-general-4)

**Verdict:** PASS · **Belam:** NOT contacted (parent owns Belam after council) · **Council:** re-queued after this MUR  
**Tip:** `96a85aeea` (`96a85aeea1fff421da1702a56d619d2d467f0748`) on `de-dg4-1` / `posts/director-general-4`  
**Parent wave-2 BUILD:** `ae180ab6d` (prior MUR PASS `528aed6f3` / council RULING `e1912a41d` RETURNED g5.35.4 SoT only)  
**Date:** 2026-10-06 ~17:10Z · **Post:** sanctuary-master · **Skill:** agi-master-gate  
**SM baseline at gate:** `8c69c6f02`  
**Climb:** DG4 BUILD PASS `5562f3c9b` · DG2 PASS `6bcb9c9a8` (vs `4c9b41ae4`) · DG1 PASS `dabd13471` (vs hyps `f81645626`)  
**Against RETURN:** `/workspace/council-design/RETURN-g5.35.4-tmux-soT.md` (one pane SoT; tmux live teach scrubbed)

## Bytes proven (independent re-measure @ tip 96a85aeea)

| leaf | check | measured | want |
|---|---|---|---|
| **g5.35.4** tmux live falsifier | `git grep -nE 'tmux (kill-window\|new-session\|send-keys\|attach)\|tmux agi-rc' tip -- skills` | **CLEAN (0 hits)** | 0 live |
| **g5.35.4** banned teach | `git grep -nE 'send\.py\|workflow\.py\|season2/' tip -- skills ':!**/deprecated/**'` | **CLEAN (0 hits)** | 0 |
| **g5.35.4** ET pane SoT | skills/agi + skills/agi-post | systemd `agi-post@` + fifo `/run/agi-<post>/i` + out `/var/lib/agi/<post>/o` only; HISTORICAL fences for old-engine tmux | one SoT |
| **g5.35.4** range vs parent | `git diff --name-only ae180ab6d tip` | **3 files only:** skills/agi, skills/agi-post, g5.35.4-CORRECTIVE-evidence.md | skills+evidence |
| **g5.35.3** ssh pack (non-reg) | `g5.35.3-ssh-config.diff` + `g5.35.3-ssh.md` on tip | **present** | present |
| **g5.35.5** cards (non-reg) | card-alive in unified-director-brief; aio/sp `HISTORICAL; today` | **0 / 1 / 1** | 0/1/1 |
| **g5.35.6** O5 (non-reg) | mangled `Bind for DG4 on g5.31` / `sibling g5.31.1` in `.agi/nodes/goal` | **NONE** | 0 |
| **g5.35.6** | `.agi/nodes/deprecated/goal/g5.31.md` | **KEPT** | kept |
| season3 tip | `core/season3/main` | **`4b8f28b5e`** (unchanged) | 4b8f28b5e |
| other tracks | g5.4.1.3 / g5.34.10 in ae180ab6d..tip | **not in range** | untouched |
| posts.md / keys | tip vs parent delta | **none** (skills+evidence only) | none |
| evidence | `proposals/dg4-loop-20261006-c/g5.35.4-CORRECTIVE-evidence.md` | on tip; body cites intermediate `820f20f43` (ancestor of tip) | real |

**Parent ancestry:** `ae180ab6d` is ancestor of `96a85aeea`. Leaves .3/.5/.6 bytes hold from prior PASS.

## Climb
| seat | box sha | vs |
|---|---|---|
| DG4 CORRECTIVE | `5562f3c9b` | tip `96a85aeea` CLAIM MET |
| DG2 | `6bcb9c9a8` | exp+verdict @ `4c9b41ae4` (review-only) |
| DG1 | `dabd13471` | hyps @ `f81645626` (review-only) |

## SM decision stamps
1. **g5.35.4 corrective** — **PASS** one pane SoT; live tmux spawn/kill/attach/send-keys/agi-rc teach CLEAN; agi-rotate left alone (no matching live teach); HISTORICAL fences only. Method: Edit+agi-turn (engine.v4); never git rm.
2. **g5.35.3 / .5 / .6** — **PASS stands** (non-reg; bytes hold from ae180ab6d).
3. **Land** — SM does NOT merge/ff trunk or posts/belam. Belam lands tip after council (parent wakes). Never git rm. No push. season3 tip untouched.

## Residues (non-blocking)
- Evidence body tip SHA = `820f20f43` (ancestor); final tip = `96a85aeea` (evidence file rides on tip). Cosmetic doc drift only.
- Live apply g5.35.3 ssh sed + agi-sync skills refresh → Belam after council (unchanged from wave-2 MUR).

## Blocking Belam land?
**None** for committed tip bytes after this MUR. Sequencing: council re-review vs prior RETURN (this gate boxes seats); Belam land after council PASS (parent only — SM does not box Belam).

## Out of scope (untouched)
goal:g5.4.1.3 · goal:g5.34.10 · season3 tip · Belam contact · Master merge · push · git rm.

## Decision
**PASS** tip `96a85aeea`. Gate doc this commit on `posts/sanctuary-master`. Council re-queued; Belam = parent only.
