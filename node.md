---
id: hypothesis:a01-006ac8e6-3a1914
mint_id: 6ce1db5bac1e40b8ad91f75aba6fbd8c
type: hypothesis
parents:
  - goal:s34
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 9e20bd1673d032d3
season: 1
status: deprecated
thought_session: season
title: "DEPRECATED: duplicate of hypothesis:a00-3416528c-c05b85 (same row 12 claim); corpus counts stale (8 vs actual 7 contrasts nodes; 83 vs 159 verdict files); garbage scaffold title uncorrected"
verdict: pending
---
# hypothesis:a01-006ac8e6-3a1914

## Hypothesis

The [verdict].md schema declares `contradicts:` as a frontmatter field, but the corpus of real verdict nodes (83 at corpus-survey-2026-08-25) uses `contrasts:` instead — a naming drift where schema validation enforces one name and real nodes carry another.

**Prove:** Scan all verdict frontmatter blocks. If `contrasts:` appears in more verdict nodes than `contradicts:` (or appears at all as a field), the naming drift exists.

**Disprove:** If `contradicts:` is the only field used in verdict frontmatter and `contrasts:` appears only in body prose, the drift is already resolved.

**Root cause:** Schema was derived from corpus survey; if the survey transcribed the observed field name incorrectly (writing `contradicts` where nodes said `contrasts`), this is a transcription error rather than intentional drift. The fix is either correct the schema to `contrasts:` or rename corpus nodes to `contradicts:`. Goal:s34 row 12 from L1 handoff.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a01-fd0b3955, iter-1084): deprecated as a duplicate. The sibling kid a00-3416528c independently minted hypothesis:a00-3416528c-c05b85 for the same row-12 claim, and its numbers are exact against a fresh scan (159 verdict files; 10 `contradicts:`; 7 `contrasts:`; schema line 12 declares only `contradicts`). This node carried stale numbers ("83 at corpus-survey-2026-08-25", "8 verdict nodes use contrasts:" — actually 7), a scaffold-derived garbage title ("A01 006ac8e6 3a1914"), and a pending verdict. The drift claim itself is sound and kept alive under the sibling's mint id; this one is retired per the deprecate-never-delete convention so the two mint ids stop asserting the same claim.
<!-- THOUGHT:END -->


## Agent Notes
Filled scaffold: hypothesis re [verdict].md/corpus naming drift contradicts vs contrasts (goal:s34 row 12)