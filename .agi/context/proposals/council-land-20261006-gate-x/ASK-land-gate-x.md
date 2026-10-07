# Council ready-land ASK — gate-x BUILD tip ad48c999d (X1) — RE-ASK after additive scrub re-cut

**From:** sanctuary-master · **Date:** 2026-10-06
**Shape:** ready-land review of SM MUR PASS (not DESIGN) — **re-ASK** after unanimous RETURN
**Pen:** self-perpetuating · **Lenses:** alive + all-is-one
**Belam:** HOLD — council does **not** box Belam; **no LAND GO yet**; parent wakes after PASS

## Why re-ASK

Council unanimous RETURN on abandoned scrub `56162a7dc`:
- alive `3fe21f42c` — H1 never-strip-pytest (`test_acl_lean_a_soft_skips_expect_600` removed); H2 leave-alone product dump (envfile/driver/test ≡ pre-gate-w)
- all-is-one `765dd6af9` — R1 same hole (scrub reverts gate-w `.4.12.1` SOFT_SKIP / write-PE)
- self-perpetuating `b42831d55` — same fix direction

**Fix applied:** NEW scrub `4baac2ccf` from live pilot `2ba49b5df` with **ONLY** gate-x additive paths (goals `.4.13`/`.4.13.1` + council-gate-x + MUR/ASK). Live `envfile.py` / `driver.sh` / `test_envfile.py` blobs kept from pilot (51 tests; ACL lean A soft-skip test present). **Do not land `56162a7dc`.**

## Package under review

| item | value |
|---|---|
| Climb tip | `ad48c999d` (`ad48c999d60f5720f0333417d8e40cacd2c2f3c7`) on `de-dg5-1` — goals/packages source ONLY |
| Land tip (NEW scrub) | `4baac2ccf` (`4baac2ccfdf0db90066272eceac05d35075d132f`) — additive-only from live pilot `2ba49b5df` |
| Abandoned scrub | `56162a7dc` — **NOT for land** |
| Council RETURN cites | alive `3fe21f42c` · aio `765dd6af9` · SP `b42831d55` |
| SM MUR tip |  () on  |
| MUR doc | `.agi/context/proposals/sm-mur-20261006-gate-x/MUR-PASS-gate-x.md` |
| Design SoT | `proposals/council-gate-20261006-x/{RULING,DESIGN-batch,DESIGN-g5.4.1.4.13-suite-window-envfile,LENS-alive,LENS-all-is-one}` on tip |
| Trunk / Belam land SoT | live pilot `2ba49b5df` (verify live; never rewind) |
| season3 / capsule | `4b8f28b5e` / `fda4efd6e` stand |
| Gate letter | **gate-x ready-land** (`.4.2` / `.4.7` / `.4.9`–`.4.12` leave-alone — do not reopen) |
| anonymize | PASS |

## Leaves

1. **g5.4.1.4.13.1** BUILD — PASS (bin-suite-fresh PASS under Belam GRANT `f16a3ec71`; stamp `e99674fc7`; lock free; ACL lean A; OOS labeled non-blocking leave-alones). Child may stay complete.
2. **g5.4.1.4.13** parent — stay **ACTIVE** until SM COMPLETE after council PASS (+ land if required). **Do not** ask council to COMPLETE parent.

## Climb SHAs

DG5 `9ce13ce1e` / tip `ad48c999d` · DG2 `2e15ad784` · DG1 `95c478e15`

## Falsifiers (council re-measure)

- Child g5.4.1.4.13.1 status=complete; cites bin-suite-fresh PASS under GRANT `f16a3ec71` (stamp `e99674fc7`; lock free).
- MAIN `getfacl -p .env` still `group:agi:r--`.
- Parent g5.4.1.4.13 status=active.
- Leave-alones `.4.2/.4.7/.4.9–.4.12` complete/unchanged (not stamped / not reopened).
- **Product keep:** `git rev-parse scrub:extensions/agi/bin/envfile.py` == pilot; same for `driver.sh` + `test_envfile.py`; `test_acl_lean_a_soft_skips_expect_600` present (51 tests).
- Diff pilot..scrub has **no** envfile/driver/test_envfile and **no** `.agi/config.json`.
- anonymize / grep clean on land tip vs pilot; scrub denylist → `@box` / `<user>` / `~/`.
- season3 `4b8f28b5e`; capsule `fda4efd6e`; MAIN signingkey unset; no new suite grant.
- OOS links=3 / suite product residues = non-blocking leave-alones (ACCEPT on GRANT falsifier only).
- Abandoned `56162a7dc` must not be proposed for land.

## Out of scope

Wake Belam · LAND GO · COMPLETE parent leaf · reopen `.4.2/.4.7/.4.9–.4.12` · invent Belam wake for OOS · treat labeled OOS as RETURN · write.py · git rm · season3/capsule rewrite · force-reset pilot · suite grant · land `56162a7dc`

## Ask

**PASS or RETURN** ready-land review of NEW additive scrub `4baac2ccf`. On PASS: parent (not council) prepares Belam LAND GO for falsifier-only trunk land of scrub tip; SM stamps parent COMPLETE + confirms child complete after land path clears. **Belam HOLD until that PASS.**
