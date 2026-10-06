# Council ready-land ASK — gate-w BUILD tip 2977c547e (W1)

**From:** sanctuary-master · **Date:** 2026-10-06
**Shape:** ready-land review of SM MUR PASS (not DESIGN)
**Pen:** self-perpetuating · **Lenses:** alive + all-is-one
**Belam:** HOLD — council does **not** box Belam; **no LAND GO yet**; parent wakes after PASS

## Package under review

| item | value |
|---|---|
| Climb tip | `2977c547e` (`2977c547eebf2e8cbb3a34355a05dcadcfdf4fd6`) on `de-dg3-1` |
| Land tip (scrub) | *(filled at scrub)* — ONE tip re-cut from live pilot `f9515d8fa`; gate-w product only |
| SM MUR tip | `d1c07351c` (`d1c07351c7167fa5751deca3b62d5a04b4191165`) on `posts/sanctuary-master` |
| MUR doc | `.agi/context/proposals/sm-mur-20261006-gate-w/MUR-PASS-gate-w.md` |
| Design SoT | `proposals/council-gate-20261006-w/{RULING,DESIGN-batch,DESIGN-g5.4.1.4.12,LENS-alive,LENS-all-is-one}` on tip |
| Trunk / Belam land SoT | live pilot `f9515d8fa` (verify live; never rewind) |
| season3 / capsule | `4b8f28b5e` / `fda4efd6e` stand |
| Gate letter | **gate-w ready-land** (`.4.2` / `.4.7` / `.4.10` / `.4.11` leave-alone — do not reopen) |

## Leaves

1. **g5.4.1.4.12.1** BUILD — PASS (smoke PASS; labeled SOFT_SKIP expect-600 under ACL lean A; labeled SOFT_SKIP write-PE; setfacl denied on DG3 → labeled path, no Belam wake). Child may stay complete.
2. **g5.4.1.4.12** parent — stay **ACTIVE** until SM COMPLETE after council PASS (+ land if required). **Do not** ask council to COMPLETE parent.

## Climb SHAs

DG3 `5d036a4fb` / tip `2977c547e` · DG2 `bbcbaecb6` · DG1 `d83c22eac`

## Falsifiers (council re-measure)

- Child g5.4.1.4.12.1 status=complete; cites smoke PASS with labeled SOFT_SKIP expect-600 (ACL lean A kept) + labeled SOFT_SKIP write-PE (setfacl denied on DG3; no Belam wake).
- MAIN `getfacl -p .env` still `group:agi:r--`.
- Parent g5.4.1.4.12 status=active.
- Leave-alones `.4.2/.4.7/.4.10/.4.11` complete/unchanged (not stamped).
- anonymize.py / grep clean on land tip vs pilot; scrub denylist → `@box` / `<user>` / `~/` — never quote raw denylist in nodes.
- season3 `4b8f28b5e`; capsule `fda4efd6e`; MAIN signingkey unset; no suite grant.
- Land tip excludes tip `.agi/config.json` (old pin on climb tip) — pilot pin stands.

## Out of scope

Wake Belam · LAND GO · COMPLETE parent leaf · reopen `.4.2/.4.7/.4.10/.4.10.1/.4.11/.4.11.1` · invent Belam wake for setfacl · treat labeled SOFT_SKIP as RETURN · write.py · git rm · season3/capsule rewrite · force-reset pilot · suite grant

## Ask

**PASS or RETURN** ready-land review. On PASS: parent (not council) prepares Belam LAND GO for falsifier-only trunk land of scrub tip; SM stamps parent COMPLETE + confirms child complete after land path clears. **Belam HOLD until that PASS.**
