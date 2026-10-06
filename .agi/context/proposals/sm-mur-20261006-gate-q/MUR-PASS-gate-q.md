# SM MUR PASS — gate-q CLOSE tip 565f38b28 (ACL + pytest parent + deploy-key)

**Verdict:** PASS · **Belam:** NOT contacted · **Council:** boxed alive / all-is-one / self-perpetuating after this MUR
**Tip:** `565f38b28` (`565f38b289a683367c705f7e2cbbe53ae6f56bb4`) on `de-dg4-1`
**Date:** 2026-10-06 ~20:20Z · **Post:** sanctuary-master · **Skill:** agi-master-gate
**Climb:** DG4 final `2608892ef` / rotate `8a8b18baf` / pytest-wave `b8bf60732` / BUILD `505e1ef32` · DG2 `37eb01f06` · DG1 `cb53b7e31`
**Trunk note:** trunk `932218a0f` is **OOS** for this merge story (Belam lands later). season3 `4b8f28b5e` / capsule `fda4efd6e` stand. write-path g5.4.1.6 **not mixed**.

## Leaves covered

| leaf | claim | MUR |
|---|---|---|
| **g5.4.1.4.3.1** ACL | committed policy + recipe; host `setfacl` once at Belam land | **PASS** (policy+recipe); live default ACL apply = land |
| **g5.4.1.4.4.1** pytest parent | all children `.1`–`.8` closed; OWNER pytest ALLOWED | **PASS** (status=complete) |
| **g5.4.1.4.4.1.6** rotate | wave-2 suite green | **PASS** 361 passed / 0 failed |
| **g5.4.1.5.3.1** deploy-key | key id `165596965`; ls-remote + dry-run without belam OS gh borrow | **PASS** |

## Owner zero-notes (binding)

1. **pytest ALLOWED** — fix/waive real reds only; **never strip** pytest / Python tests as the fix.
2. **ACL setfacl once** at Belam land (default ACL still empty on MAIN sessions dir) — not forever one-off; not DG4 sudo-as-belam.
3. **Belam** = falsifier-only after council PASS; SM does **not** wake Belam from MUR.
4. Never write.py · never git rm · season3/capsule untouched · trunk OOS for this story.

## Independent measure @ tip 565f38b28

| leaf | check | measured | want |
|---|---|---|---|
| **g5.4.1.4.3.1** | policy file on tip | `.agi/context/proposals/suite-stamp-acl-policy-20261006-q.md` present | present |
| **g5.4.1.4.3.1** | DG4 RESULT | PASS (policy+recipe; ACL apply = Belam land) | PASS |
| **g5.4.1.4.3.1** | MAIN default ACL | still **empty** (prep measure) — land owes `setfacl -d` | empty pre-land |
| **g5.4.1.4.4.1** | status | **complete**; parent CLOSE all `.1`–`.8` | complete |
| **g5.4.1.4.4.1.6** | suite | **361 passed / 1 skipped / 5 xfailed / 0 failed** | 0 failed |
| **g5.4.1.5.3.1** | deploy key | id **165596965**; read_only=false; DG4 RESULT PASS | present + PASS |
| **g5.4.1.5.3.1** | no belam gh borrow | RESULT documents SSH ls-remote + dry-run without belam credential swap | no borrow |
| **strays** | ls-remote season2/main + belam/capsule-rows | **empty** (DG4 probe; tip RESULT) | empty |
| **season3** | local + tip hold | **`4b8f28b5e`** | 4b8f28b5e |
| **capsule** | | **`fda4efd6e`** | fda4efd6e |
| **non-touch** | write.py / git rm / Belam wake | climb used Write+agi-turn; Belam NOT contacted | untouched |

## Climb

| seat | box sha | vs |
|---|---|---|
| DG4 BUILD (ACL+deploy+pytest place) | `505e1ef32` | tip family `d8fba9219` |
| DG4 pytest-wave | `b8bf60732` | tip `2049fe3b1` |
| DG4 rotate wave-2 | `8a8b18baf` | tip `d198dabee` → 361/0 |
| DG4 final CLOSE | `2608892ef` | tip `565f38b28` |
| DG2 correction-review | `37eb01f06` | review-only @ `4c9b41ae4` PASS |
| DG1 correction-review | `cb53b7e31` | review-only @ `f81645626` PASS |

## SM decision stamps

1. **g5.4.1.4.3.1** — **PASS** policy+recipe. Live durable default ACL = **Belam land once** (`setfacl -m/-d` per committed policy).
2. **g5.4.1.4.4.1** — **PASS** parent complete; `.6` rotate 361/0; OWNER pin held (never strip).
3. **g5.4.1.5.3.1** — **PASS** deploy-key primary (165596965); no belam OS gh borrow.
4. **Land** — SM does not merge/ff trunk or posts/belam. Belam lands after council (parent only) = falsifier verify + **setfacl once**. Never git rm. season3/capsule untouched. trunk `932218a0f` OOS.
5. **Belam** — NOT boxed/woken by SM. Council next.

## Decision

**PASS** tip `565f38b28` covering g5.4.1.4.3.1 + g5.4.1.4.4.1 (+ `.6` rotate) + g5.4.1.5.3.1. Council boxed for land review; Belam = parent only after council land PASS (falsifier + setfacl once).
