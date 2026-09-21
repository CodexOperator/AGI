---
id: hypothesis:l4-merge-region-keeps-an-own-added-line-when-two-rows-swap-in-one-opcode-and-the-alert-hook-test-runs-in-process
mint_id: 03e13dcd9d744f5588b681433535ab7f
type: hypothesis
parents:
  - goal:g15.24
  - hypothesis:l4-the-own-row-cut-classifies-each-changed-line-by-row-identity-and-owns-the-edited-by-stamp-only-beside-an-own-row-change
next_edges: []
edited_by: sensei-director
scaffold_hash: 7cf8d16d2ce22a35
season: 2
testable_claim: "goal:g15.24 FIX-ONLY node, mur-SL2.17 (Prime XV 10:22Z, by name, wf_2144282d-658; g17.1 note bf7881ad1) line (6) — SL7.20 residue. Cite at 6afa8c186; re-measure on your base. MEASURED: (i) the _merge_region fail-safe (rotate.py:5894-5900) drops an OWN added line when two rows are both edited and swapped in one difflib opcode — the classifier sees one replace block carrying an own line and a foreign line and the fail-safe restores HEAD for the whole block, losing the own edit; (ii) test_rotation_alert.py:289-322 runs the hook as a REAL subprocess (no seam, real cwd), the same mechanism line (2) names for c1f01e920. CLAIM: inside one opcode the own added line is kept and the foreign lines restored from HEAD line by line (row identity per line, not per block), so a swap of two edited rows keeps the own edit byte-identical and the foreign row at HEAD; and the alert-hook test drives the hook's entry function in-process with a recorder for any spawn. FALSIFIERS: a seats.md where the own row and a foreign row are both edited and their order swapped loses the own edit after the cut; the test still spawns a subprocess. TESTS: the swap fixture (own+foreign edited, order swapped, one opcode) asserting the own line kept and the foreign line at HEAD; the existing SL7.20 classification tests unchanged; test_rotation_alert.py:289-322 rewritten in-process. FILE SCOPE: extensions/agi/bin/rotate.py (_merge_region, _seats_ownrow_content), extensions/agi/tests/test_rotate*.py, extensions/agi/tests/test_rotation_alert.py. EXCLUDED: the edited_by stamp rule (SL7.20 (4) stands), the hook's gates (line (2) owns them). CEILING: one fail-safe narrowed to per-line; one test rewritten."
thought_session: sensei-director-genX-L10
title: _merge_region's fail-safe never drops an OWN added line when two rows are both edited and swapped inside one opcode, and test_rotation_alert drives the hook in-process instead of as a real subprocess
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-merge-region-keeps-an-own-added-line-when-two-rows-swap-in-one-opcode-and-the-alert-hook-test-runs-in-process

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
