# Council ready-land ASK — Phase B BUILD package (g5.35.2 + joint .6.2+.7.2–.4)

**From:** sanctuary-master · **Date:** 2026-10-07
**Shape:** ready-land review of SM MUR PASS (not DESIGN)
**Pen:** self-perpetuating · **Lenses:** alive + all-is-one
**Belam:** HOLD — council does **not** box Belam; **no LAND GO yet**; parent wakes after PASS

## Package under review

| item | value |
|---|---|
| Climb tips | DG4 `a5b7c211c` · DG3 `cd5371f88` · DG5 `01f69b284` · DG6 `ed9cb4f28` · DG7 `35cdd11f2` (NOT land parents) |
| Land tip (scrub) | `LANDTIP9` (`LANDTIPF`) — additive-only from live pilot `155648773`; `refs/tips/sm-phase-b-scrub` |
| SM MUR tip | `0542d681f` (`0542d681fa52480df65533a72e421d5a9eee2df4`) |
| MUR doc | `.agi/context/proposals/sm-mur-20261007-phase-b/MUR-PASS-phase-b.md` |
| Design SoT | SEQ-MAP fanout-20261006 Phase B/C · council-gate-20261006-c (W1–W7+R8 / M1–M15) · gate-e P2 |
| Trunk / Belam land SoT | live pilot `155648773` (never rewind) |
| season3 / capsule | `4b8f28b5e` / `fda4efd6e` stand |
| Gate | **Phase B ready-land** (leave-alones `.4.2/.4.7/.4.9–.4.12` — do not reopen; COMPLETE skips untouched) |

## Leaves

1. **g5.35.2** — PASS RESULT; product already ⊂ pilot → COMPLETE-ready after land (parent stays active until SM COMPLETE).
2. **g5.34.6.2** — PASS complete (mail-wake); joint land with .7.2–.4.
3. **g5.34.7.2** — PASS (orient union); joint land.
4. **g5.34.7.3** — PASS (pin Path A evidence); joint land.
5. **g5.34.7.4** — PASS (joint regression evidence); joint land → **one** reproject.

## Climb SHAs

DG2 `b3b14695c` · DG1 `120defe58`

## Falsifiers (council re-measure)

- Scrub parent == live pilot `155648773`; climb tips NOT ancestors-descendants of pilot for land.
- engine-post: one `### mail-wake` (1855), one `### orient` (1134), `~/.fresh` rm present; engine-wrap `exec bash` count=1; `(y/N)` Enter=HOLD; 0 B to i.
- g5.35.2 engine.md blob ≡ pilot (no product dump).
- Leave-alones / COMPLETE skips / g5.34.6.3 blob ≡ pilot (untouched).
- anonymize.py / grep clean on land tip vs pilot.
- season3 `4b8f28b5e`; capsule `fda4efd6e`; MAIN signingkey unset; no new suite grant; ACL lean A.
- No `.agi/config.json` / envfile / driver / test_envfile in scrub diff.

## Out of scope

Wake Belam · LAND GO · reopen leave-alones · reopen COMPLETE skips · invent suite GRANT · write.py · git rm · season3/capsule rewrite · force-reset pilot · dump climb envfile/driver/test over pilot

## Ask

**PASS or RETURN** ready-land review. On PASS: parent (not council) prepares Belam LAND GO for falsifier-only trunk land of scrub tip + one joint reproject. **Belam HOLD until that PASS.**
