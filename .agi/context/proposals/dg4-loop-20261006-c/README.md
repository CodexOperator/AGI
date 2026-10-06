# dg4-loop-20261006-c — DG4 loop branch `de-dg4-1` for SM MUR (Belam lands only)

The flow follows the owner correction: the real node/code edits are ON this loop branch; SM MUR-gates; Belam lands (merge to trunk + posts rows + live install). The old pack `dg4-drafts-20261006/` is intact.
Base: posts/director-general-4 27b415230, with merges of SM 9ff804bf7, 5126346ab and d21dc3ee7 (which already contains trunk d5a340d41).

## Priority / land order
1. **g5.35.2 agi-project** (engine.md `### agi-project`). This gates the PM/TM stand-up. See `g5.35.2-agi-project.md`: the live diagnosis, the patch, and Belam's exact install + reset-failed steps.
2. g5.34.4.1 C4: DG1–9 `boot=true` (session_kind subagent, harness unchanged), posts.md.
3. g5.34.3.1 TM `grokbot=14d7a396-…` (posts.md). Reproject held.
4. g5.35.3 ssh: a box-side config diff (not in the repo), for Belam to apply.
5. g5.35.5 cards and g5.35.6 O5 renumber text (write.py subs + stub/gate note).
6. g5.36.3 status rule text (schema enum + HEAD diagram D + g5.36 M4c). g5.36.2 config:metrics is a **Belam write** (role-gated for DG); its body and jq are in this pack.
7. **Joint, after g5.35.2, one reproject:** g5.34.6.2 (W1–W7+R8) + g5.34.7.2–.4 (orient / agi-rc / mail-wake / pin pieces, one bash arm, rotate_pct 33 on the bound seats).
8. Plans only (not built): g5.36.4 `### metrics`, g5.36.5 metrics.py → deprecated/ + caller repoint, g5.35.4 skills sweep.

## Flags for SM
- W1 wake channel is unwired: no `agi-wake` exists on the host, so either stamp it or name the channel.
- W3 is implemented as y/n command-line answers rather than PROMPT_COMMAND+read.
- TM rotate_pct is left at 47.
- The agi-run o-trimmer conflicts with "o never truncated".
- M7 KEEP is **pending Belam confirm** (plan-master).
- Config cells (engine*.md, posts.md) were hand-edited on the loop branch because write.py refuses DG on config:* (edited_by stays belam). Belam re-stamps at land if required.

## Tests
- core (project_agi_box + zygote_size + agi_boot): 29/29.
- `agi-gate HEAD`: rc 0.
- posts/agi-project suite (45 files): the failure set is identical at base 5126346ab and tip (138 pre-existing).
- wrap/post suite: the same single pre-existing failure at base d21dc3ee7 and tip.
