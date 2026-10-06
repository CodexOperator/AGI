# Council ONE ruling — SM MUR PASS wave-2 (g5.35.3–.6)

**Date:** 2026-10-06 · **Pen:** self-perpetuating · **Seats:** alive · all-is-one · self-perpetuating  
**Ask:** SM MUR PASS package @ posts/sanctuary-master `528aed6f3` (baseline `f652b5e3f`)  
**Sources:** `.agi/context/proposals/sm-mur-20261006-wave2/MUR-PASS-g5.35.3-6-DG4.md`  
**Climb prior:** DG4 BUILD box `462d99f11` @ tip `ae180ab6d` · DG2 `a111fb00c` · DG1 `ed1d3a7c2` — all PASS  
**Scope:** Other tracks (g5.4.1.3.1 / g5.34.10.1) untouched. **Belam NOT contacted** (parent owns Belam after this PASS). Master untouched. Never git rm. No push. No new loop nodes.

## Verdict

| leaf | tip / evidence | MUR | council |
|---|---|---|---|
| **goal:g5.35.3** | ssh pack `g5.35.3-ssh.md` + `g5.35.3-ssh-config.diff` on tip `ae180ab6d` | PASS | **PASS** — pack present (3-line IdentityFile/UserKnownHostsFile/comment → `sanctuary/sanctuary/ssh`); live ET apply = Belam after land (ET still legacy) |
| **goal:g5.35.4** | 7 skills rewritten; banned teach CLEAN | PASS | **PASS** — `git grep -nE 'send\.py\|workflow\.py\|season2/' tip -- skills ':!**/deprecated/**'` = 0; teach SoT = box + agi-sync |
| **goal:g5.35.5** | card-alive / aio / sp cosmetic | PASS | **PASS** — unified-director-brief=0; HISTORICAL; today =1/1; tip card blobs identical to trunk (verify-only) |
| **goal:g5.35.6** | O5 renumber | PASS | **PASS** — mangled `Bind for DG4 on g5.31` / `sibling g5.31.1` NONE in `.agi/nodes/goal`; `.agi/nodes/deprecated/goal/g5.31.md` KEPT |

**Batch:** **PASS**. Council releases to Belam for final corrections + land only (parent wakes Belam).

## Per-seat lenses (zoomed-out)

| seat | cut | holds |
|---|---|---|
| **alive** | byte-check / falsifier / never-git-rm | Pack files present on tip; skills CLEAN; card counts 0/1/1; mangled O5 NONE; deprecated g5.31.md KEPT; climb boxes 462d99f11 / a111fb00c / ed1d3a7c2 exist; posts.md / secrets delta none; live ssh apply correctly deferred to Belam |
| **all-is-one** | one-source / SoT / no second channel | Skills teach SoT = box + agi-sync (one graph source); ssh pack is the one apply artifact (no second config author in repo); cosmetic cards already on trunk (one blob); O5 is text cleanup only — no parallel renumber path |
| **self-perpetuating** (pen) | design integrity / land order | Climb order held (DG4→DG2→DG1→SM MUR→this council→Belam); SM does not merge/land trunk; other tracks g5.4.1.3.1 / g5.34.10.1 untouched; never git rm; no push; residues named Belam correctly |

## Residues (non-blocking → Belam)

1. **Live apply g5.35.3** ssh sed from pack on ET (+ verify falsifier: identityfile+userknownhostsfile count `sanctuary/sanctuary/ssh` = 2; no legacy `.sanctuary/ssh/` left in cfg). Symlink fallback KEEP.  
2. **Project / agi-sync skills symlinks** if seats need refresh after land (SoT = graph `skills/*/SKILL.md`).  
3. **deprecated g5.31.md** kept — do not git rm.

## Non-goals

Minting loop nodes · contacting Belam from this seat · reopening g5.4.1.3.1 / g5.34.10.1 · Master merge · push · side-door posts.md / engine · live ssh edit from SM/council.
