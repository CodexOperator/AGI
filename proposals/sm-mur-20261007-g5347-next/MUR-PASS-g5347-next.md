# SM MUR PASS — g5347-next (g5.34.7.5 o-trimmer bypass)

**Verdict:** PASS · **Belam:** HOLD (no LAND GO) · **Council:** ready-land ASK boxed after this MUR
**Climb tip (goals/geometry SOURCE ONLY — NOT land parent):** `417185e19` (`417185e19042a3071638245ed41c5041af6f537f`) on `de-dg5-1` — descendant of live pilot; merge-tree onto SM posts **CONFLICTS** (leave-alone / Phase B COMPLETE stamps) → additive scrub path (gate-x / Phase B pattern).
**Land tip (additive scrub):** `a252f0509` (`a252f0509cec687c39f54d543d726719ca10856d`) — parent live pilot `e7aeb9314` (`e7aeb931401bf91183ed5b2a35cc0e0e3adcd45f`) · `refs/tips/sm-g5347-next-scrub`
**Date:** 2026-10-07 · **Post:** sanctuary-master · **Skill:** agi-master-gate (Write+agi-turn; never write.py)
**SM base:** `2cce1b7b1` (`2cce1b7b11f70f08be539da00201009c4ad7c234`) · **SM PASS cite:** `649550d11` · content `65ccf4454` · DESIGN `7155cc6d4`
**DG5 box:** `97639ec18` · **TM box:** `1d413736e`
**Stands:** season3 `4b8f28b5e` / capsule `fda4efd6e` · ACL lean A · MAIN signingkey UNSET · lock FREE
**Cite:** RULING `proposals/council-design-20261007-g5347-next/RULING-g5347-next.md` · mint `73a87f5b241a4586b11cf952bc11208b` · MUR residue `c63205cd9` · Phase B COMPLETE `6a57d93bd` · lenses alive `3cc17ad06` · aio `5c736e024` · SP `71b423115`

## Leaf covered

| leaf | verdict |
|---|---|
| g5.34.7.5 | PASS — lean N1 bypass/disable `AGI_PANE_MAX_MB` ring trimmer removed from engine-wrap `### agi-run` (754 B; count=0). Honor v7 O3 never-truncate; **NOT** ACCEPT-exception. Status **active** (not COMPLETE until after Belam LAND OK). Parent `g5.34.7` stays **ACTIVE**. |

## Additive scrub contract

- Climb tip IS descendant of pilot (`git merge-base --is-ancestor e7aeb9314 417185e19` = YES) but merge-tree(SM,`417185e19`) rc≠0 → scrub from live pilot only.
- Scrub parent = live pilot `e7aeb9314` only. **Never** force-reset / ff pilot. N1 merge-onto-live at Belam land later.
- Carry: `.agi/nodes/.geometry/engine-wrap.md` (trimmer removed) + `.agi/nodes/goal/g5.34.7.5.md` + MUR/ASK packages.
- **Never** dump climb envfile/driver/test (already ≡ pilot). Never dump `.agi/config.json`. Never touch leave-alones `.4.2/.4.7/.4.9–.4.13` or COMPLETE skips `.7.2–.4/.7.6/.8/.8.1–.4` / `g5.35.2` / `g5.34.6.2` or parent `g5.34.7`.

## Falsifiers (measured on scrub)

- `AGI_PANE_MAX_MB` count on scrub engine-wrap = 0; no `tail -c … ~/o` rewrite; sleep-300 trimmer absent on `### agi-run`.
- `exec bash --rcfile` count = 1 (bash arm kept).
- envfile/driver/test_envfile blobs ≡ pilot.
- Leave-alones / COMPLETE skips / parent / g5.34.6.2 / g5.35.2 blob ≡ pilot.
- Leaf status=active; mint `73a87f5b…` present; no child `.7.5.1`.
- anonymize / denylist grep clean; season3/capsule stand; MAIN_SK unset; ACL lean A; no suite GRANT; no deletes.

## Holds

- Belam HOLD — no LAND GO this turn · no Belam box
- SEQ-1 only · ONE same-seat DG5 · parent stays ACTIVE · leaf not COMPLETE
- leave-alones + COMPLETE skips untouched · never redesign `.7.1`/`.7.6`/`.8.*` · never restamp `.6.2` · `.6.3` OOS
- ACL lean A; never git rm; never suite GRANT invent; never write.py; never force-reset pilot
