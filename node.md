---
id: hypothesis:l4-rotate-resolves-the-stops-slot-from-the-row-handoff-file-when-the-row-carries-one
mint_id: 26e6b919ddb64747b866e2a25ad1fcb6
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: belam
scaffold_hash: 14f17424411ac180
season: 2
testable_claim: "Measured 2026-09-16 by master-sensei gen 8 (SM lane, 11:51Z) and verified on MAIN 28acb3459: rotate resolves the where-it-stops slot ONLY from <sessions>/quorum/<post>.md (rotate.py:6698 _own_card_path; 3439 names quorum/belam.md) while the belam row in config:seats carries handoff_file=<graph_root>/HANDOFF.md, where the Prime actually writes (quorum/belam.md is a 21-line stub with 4 appended slots and 0 `## ` headings). Every Prime rotation pays a bare-refused rotate + a --stops re-run (Prime XXII 11:48Z). CLAIM: when a row carries a non-empty handoff_file, rotate resolves the where-it-stops slot (and the BANKED slot, same reader) from THAT file, <graph_root> expanded, and only falls back to quorum/<post>.md when the cell is empty or the file is absent; the bare rotate on the belam row then finds the slot in HANDOFF.md with no --stops. FALSIFIERS: a row with handoff_file set whose bare rotate still reads quorum/<post>.md; a row WITHOUT handoff_file whose resolution changes at all; a stops_sha256 in the record computed from a different file than the one the slot was read from. TESTS (<=4, fixture rows + fixture files, no live pane): row with handoff_file -> slot read from it; row without -> quorum/<post>.md unchanged; handoff_file set but absent -> quorum fallback named in the refusal; the record's stops_sha256 matches the file the slot came from. FILE SCOPE: rotate.py (_own_card_path and its two callers), the rotate tests. CEILING: <=30 production lines, 1 kid -- re-brief SM past 2x."
thought_session: dissolve-legacy-2026-09-19
title: L4 rotate resolves the stops slot from the row handoff file when the row carries one
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-rotate-resolves-the-stops-slot-from-the-row-handoff-file-when-the-row-carries-one

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
L4 CLOSE TRIAGE (belam gen 24, 2026-09-16 16:3xZ; workflow g15-close-triage wf_b1179398-7ab, reader + adversarial refuter on season2/main eb21d601f): KEEP for the next stream (KEEP) -- live defect: `_own_card_path` resolves only `sessions/quorum/<seat>.md` (rotate.py:7229-7240, MEASURED sed); `handoff_file` occurs in rotate.py exactly once, in the rename column tuple (:3444, MEASURED grep); belam row carries `handoff_file: <graph_root>/HANDOFF.md` (posts.md:10). Correction to reader: .agi/sessions/quorum/belam.md is 26 lines with 5 `#` lines (MEASURED wc/grep), not 0 headings -- immaterial to the mechanism. EVIDENCE: rotate.py:7229-7240,:3444; .agi/nodes/.geometry/posts.md:10; 68abd19e8 (latest rotate.py, no change) Never rounded at close (owner 14:1xZ).
