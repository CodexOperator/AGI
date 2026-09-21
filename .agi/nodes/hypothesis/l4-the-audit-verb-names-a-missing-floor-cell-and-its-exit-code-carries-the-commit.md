---
id: hypothesis:l4-the-audit-verb-names-a-missing-floor-cell-and-its-exit-code-carries-the-commit
mint_id: 93d23868c7c043be822fa50cf79943a4
type: hypothesis
parents:
  - goal:g6.12
next_edges: []
edited_by: belam
scaffold_hash: 73a6311a43a7bef6
season: 2
testable_claim: "SL7.134 residue (belam review wf_8421303d-685, GO 15:33Z, landed 6be85f707), ONE kid, sensei.py + cli.py + tests, in this order. (1) The audit floors fall back SILENTLY to FALLBACK_AUDIT_FLOOR when the config:rotations floor_wake/floor_out cell is absent or malformed (sensei.py:1496/:1507/:1548/:1700): name the miss on the verb's one line (or refuse by name) -- the 'cell nothing reads' trap. (2) A commit REFUSED/FAILED by _commit_audit_record still exits 0 from the verb (finish_audit :1706): the exit code must carry it, the printed line unchanged. (3) Untested: the commit helper's FAILED branch, and exact-path commit with a SECOND dirty file in the tree (writeback :617) -- one test each. (4) Untracked live rotation records in MAIN (git status ?? belam.20260913T013315Z.json + others): the verb writes the audit, the commit is REFUSED by name ('not tracked'), the record is left dirty -- decide whose commit: git add + commit the audited record (one path, one commit) or refuse BEFORE writing; never a dirty record. (5) cli.py done prints ERR 'tier kid may not commit' to a kid whose frontmatter landed (outside SL7.134's diff, unverified): verify first, then make the line say what happened. (6) The wake excess counts the cut (d) call: belam 20260916T151713Z scanned 4, a=1 b=1 c=1 d=1, reported excess 4 over floor 0 -- the verb's own note says only a/b/c span the wake window, so excess = a+b+c - floor; the out side keeps calls - floor (its floor 1 IS the rotate). Proof: a test per item; one live run on a tracked success record."
thought_session: dissolve-legacy-2026-09-19
title: L4 the audit verb names a missing floor cell and its exit code carries the commit
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-audit-verb-names-a-missing-floor-cell-and-its-exit-code-carries-the-commit

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
2026-09-16 15:5xZ master-sensei: minted as the SL7.134 residue the Prime named in the GO (wf_8421303d-685: 9/9 MET, accept with residue; the 'no suite-lock refusal' defect REFUTED as this round's), plus item (6) measured on the first live run of the landed verb (belam 20260916T151713Z wake, commit 9ad54d5ee: the verb committed its own record -- (c) proven live -- but reported excess 4 where a+b+c = 3). One kid, my lane; dispatch when the stamp window closes.
<!-- THOUGHT:END -->
