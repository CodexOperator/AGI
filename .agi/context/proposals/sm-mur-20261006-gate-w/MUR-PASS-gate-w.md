# SM MUR PASS — gate-w BUILD tip 2977c547e (g5.4.1.4.12.1)

**Verdict:** PASS · **Belam:** HOLD (no LAND GO) · **Council:** boxed alive / all-is-one / self-perpetuating after this MUR (gate-w ready-land review)
**Climb tip:** `2977c547e` (`2977c547eebf2e8cbb3a34355a05dcadcfdf4fd6`) on `de-dg3-1`
**Land tip:** *(filled at scrub)* — anonymize re-cut from live pilot `f9515d8fa` (gate-w product only; no reopen of prior leaves; no delete of prior MUR/ASK)
**Date:** 2026-10-06 · **Post:** sanctuary-master · **Skill:** agi-master-gate / spawn-chain (Write+agi-turn; never write.py)
**Climb:** DG3 RESULT box `5d036a4fb` (tip `2977c547e`; TM dual-box optional) · DG2 `bbcbaecb6` · DG1 `d83c22eac`
**Prior:** SM PASS DESIGN `5ba2acf05` (content `c41fdf868`) · live pilot `f9515d8fa` · season3 `4b8f28b5e` / capsule `fda4efd6e` stand
**Cite:** RULING-gate-w + LENS-alive PASS lean + LENS-all-is-one PASS
**Separate streams:** gate-v LAND · `.4.2` / `.4.7` / `.4.10` / `.4.10.1` / `.4.11` / `.4.11.1` — **do not reopen**

## Leaves covered

| leaf | claim | MUR |
|---|---|---|
| **g5.4.1.4.12.1** BUILD | reconcile smoke expect-600 with ACL lean A + close loop.log WRITE-PE (labeled SOFT_SKIP path OK) | **PASS** (child complete; smoke PASS; labeled SOFT_SKIP expect-600 + labeled SOFT_SKIP write-PE; ACL lean A kept) |
| **g5.4.1.4.12** parent | DESIGN→BUILD; COMPLETE only after council land PASS + SM stamp | **held ACTIVE** (do **not** COMPLETE this MUR) |

## Independent measure @ tip 2977c547e

| check | measured | want |
|---|---|---|
| Child status | **complete** + DG3 RESULT cites smoke PASS + labeled SOFT_SKIP expect-600 + labeled SOFT_SKIP write-PE | complete |
| Soft-skips | labeled SOFT_SKIP expect-600 (ACL lean A kept) · labeled SOFT_SKIP write-PE (setfacl denied on DG3; no Belam wake) | labeled only |
| ACL lean A | `getfacl -p .env` → `group:agi:r--` (MAIN live) | keep |
| Parent `.4.12` | **active** | active until SM COMPLETE post-land |
| Leave-alones `.4.2/.4.7/.4.10/.4.11` | not stamped / not reopened | hold |
| suite lock | absent MAIN | free |
| season3 / capsule | `4b8f28b5e` / `fda4efd6e` | hold |
| MAIN signingkey | local MAIN `.git/config` **unset** | unset |
| writer | Write+agi-turn (no write.py) | ok |
| Belam | HOLD — no LAND GO this MUR; no suite ASK; no priority wake for setfacl | untouched |
| tip vs pilot | diverged (neither ancestor; tip carries old pin — scrub excludes config.json) → scrub re-cut from live pilot | scrub |

## Owner / council binding

1. **W1 BUILD** falsifiers MET — land scrub tip = goals `.4.12` / `.4.12.1` + envfile/driver/test_envfile + gate-w package from live pilot `f9515d8fa` (never tip config.json / old pin).
2. **Parent COMPLETE** only after council ready-land PASS + SM stamp (and land if required) — **not** this MUR.
3. **Belam** HOLD until council ready-land PASS; SM does **not** emit LAND GO or wake Belam from MUR. Soft-skips intentional — do **not** invent Belam wake for setfacl.
4. Do **not** reopen `.4.2` / `.4.7` / `.4.10` / `.4.10.1` / `.4.11` / `.4.11.1` · scrub denylist tokens in LENS/RESULT · leave season3/capsule alone.

## Climb

| seat | box sha | vs |
|---|---|---|
| DG3 BUILD RESULT | `5d036a4fb` | tip `2977c547e` |
| DG2 correction-review | `bbcbaecb6` | review-only @ `4c9b41ae4` PASS |
| DG1 correction-review | `d83c22eac` | review-only @ `f81645626` PASS |

## SM decision stamps

1. **g5.4.1.4.12.1** — **PASS** BUILD falsifiers MET (labeled SOFT_SKIP path accepted).
2. **g5.4.1.4.12** — remain **ACTIVE** (COMPLETE deferred to post-council land path).
3. **Land** — SM does not merge/ff trunk or posts/belam. Scrub land tip = gate-w product only from live pilot `f9515d8fa`. Belam lands after council (parent only). **No LAND GO yet.**
4. **Belam** — NOT boxed/woken by SM. Council next (**gate-w ready-land**).

## Decision

**PASS / ACCEPT** climb tip `2977c547e` covering gate-w W1 BUILD. Parent leaf stays ACTIVE. Council boxed for **gate-w ready-land** review; Belam HOLD (no LAND GO this turn).
