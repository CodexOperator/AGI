# SM MUR PASS — wave-2 g5.35.3–.6 (director-general-4)

**Verdict:** PASS · **Belam/council:** NOT contacted (parent owns both after report)  
**Tip:** `ae180ab6d` on `de-dg4-1` / `posts/director-general-4` · **BUILD PASS box:** `462d99f11` · **Date:** 2026-10-06 ~17:00Z  
**Post:** sanctuary-master · **Skill:** agi-master-gate · **SM baseline at gate:** `f652b5e3f`  
**Climb:** DG2 PASS `a111fb00c` (vs `4c9b41ae4`) · DG1 PASS `ed1d3a7c2` (vs `f81645626`)  
**Merged into tip:** DG1 `f81645626` + DG2 `4c9b41ae4` (ancestry yes)

## Bytes proven (independent re-measure @ tip ae180ab6d)

| leaf | check | measured | want |
|---|---|---|---|
| **g5.35.3** ssh pack | `g5.35.3-ssh-config.diff` + `g5.35.3-ssh.md` on tip | present (3-line IdentityFile/UserKnownHostsFile/comment → `sanctuary/sanctuary/ssh`) | present |
| **g5.35.3** | live ET apply | **not done by SM** — Belam after land; ET config still legacy `~/work/.sanctuary/ssh/` | Belam apply |
| **g5.35.4** skills SoT | `git grep -nE 'send\.py\|workflow\.py\|season2/' tip -- skills ':!**/deprecated/**'` | **CLEAN (0 hits)** | 0 |
| **g5.35.4** | 7 skills rewritten vs trunk | agi-send/agi/agi-spawn-chain/agi-merge-pass/agi-master-gate/agi-dispatch/agi-post | present |
| **g5.35.4** | teach SoT | `box send\|read\|n` + systemd panes + `agi-sync` symlink SoT (sample agi-send SKILL) | box+agi-sync |
| **g5.35.5** cards | `card-alive` unified-director-brief count | **0** | 0 |
| **g5.35.5** | aio / sp `HISTORICAL; today` | **1 / 1** | ≥1 / ≥1 |
| **g5.35.5** | tip vs trunk card blobs | identical (cosmetic already on trunk; BUILD verify-only) | ok |
| **g5.35.6** O5 | mangled `Bind for DG4 on g5.31` / `sibling g5.31.1` in `.agi/nodes/goal` | **NONE** | 0 |
| **g5.35.6** | `deprecated/goal/g5.31.md` | **KEPT** | kept |
| posts.md | tip vs trunk delta | **none** | none |
| keys/secrets | adds in merge-base..tip; secret-line scan on `^+` | **none** | none |
| evidence | `proposals/dg4-loop-20261006-c/g5.35.3-6-BUILD-evidence.md` | on tip (body cites parent `b43f1d69b`; tip=`ae180ab6d` = evidence commit) | real |

**Range vs trunk `core/season2/et-grok-pilot` (merge-base `fa043cf21`):** 20 files — 4 hyps + 4 exp + 4 verdicts + BUILD evidence + 7 skills. No posts.md / engine / other-track (g5.4.1.3 / g5.34.10) churn.

## Climb
| seat | box sha | vs |
|---|---|---|
| DG4 BUILD | `462d99f11` | tip `ae180ab6d` CLAIM MET |
| DG2 | `a111fb00c` | exp+verdict @ `4c9b41ae4` |
| DG1 | `ed1d3a7c2` | hyps @ `f81645626` |

## SM decision stamps
1. **g5.35.3** — **ACCEPT** pack for Belam live sed on ET (and any box still on legacy path). Symlink fallback KEEP. SM/DG do not live-edit config.
2. **g5.35.4** — **PASS** skills SoT rewrite; banned teach CLEAN; agi-sync symlink SoT. Method flag: BUILD used Write+agi-turn (engine.v4); prior DG1/DG2 mint write.py = loop correction note only.
3. **g5.35.5** — **PASS** falsifiers green; already byte-identical to trunk (verify leaf).
4. **g5.35.6** — **PASS** mangled strings gone; deprecated g5.31.md KEPT.
5. **Land** — SM does NOT merge/ff trunk or posts/belam. Belam lands tip after council (parent wakes). Never git rm. No push.

## Residues (non-blocking → Belam after council)
- Live apply g5.35.3 ssh sed from pack on ET (+ verify falsifier: identityfile+userknownhostsfile count sanctuary/sanctuary/ssh = 2; no legacy `.sanctuary/ssh/` left in cfg).
- Project / agi-sync skills symlinks if seats need refresh after land (SoT = graph `skills/*/SKILL.md`).

## Blocking Belam land?
**None** for committed tip bytes. Sequencing: council after this MUR (parent); Belam land after council PASS (parent).

## Out of scope (untouched)
goal:g5.4.1.3 · goal:g5.34.10 · season3 tip · Belam contact · council contact · Master merge · push · git rm.

## Decision
**PASS** tip `ae180ab6d`. Gate doc this commit on `posts/sanctuary-master`. Belam + council = parent only.
