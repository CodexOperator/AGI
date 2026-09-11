---
id: hypothesis:l4-the-rotation-alert-hook-says-what-it-measures
mint_id: 83caeee3e6b5479cae54021c059f4233
type: hypothesis
parents:
  - goal:g15.18
next_edges: []
edited_by: sensei-director
scaffold_hash: 436206880f4c71ee
season: 2
testable_claim: "PRIME 16:22Z dm (owner-ordered): L4.94's rotation-reminder hook INSTALLED 16:21Z under UserPromptSubmit; residue in extensions/agi/hooks/rotation_alert.py. Goal goal:g15.18 (parents + '## Why this exists' there). MEASURED on this seat's own firing 16:3xZ: 'Approaching rotation (0.2098 of the line). Crossed band 18% of threshold.' — 0.2098 is of the WINDOW (= 0.446 of the line), 18 = int(0.40 × 0.47 × 100) (pct at :373 multiplies the band fraction by the threshold while the label says 'of threshold'; the Prime's 'band 25% at 0.63 of threshold' is the same formula at the 0.55 band). BUILD: (1) the registration block (:11, :41-44) prescribes UserPromptSubmit in the exact shape the Prime installed in ~/.claude/settings.json (READ the live file, copy the shape; NEVER edit it); (2) pct prints int(b_frac × 100) — the band as a fraction of the threshold — and the fraction line prints both by name: '<f> of the window = <f/threshold> of the line'; (3) verify the 'first firing reports the LOWEST crossed band' report on the bytes — the loop :325-329 picks the HIGHEST crossed band; if the report was the pct formula, say so in the verdict with the arithmetic; if a real path exists (stale state file with a reused session_id suppressing the higher band; the state file keyed by session only), fix it; (4) the line: read the seat's OWN rotate_at from its config:seats row when the seat is identifiable (env AGI_SEAT when present; else the cwd equals a row's worktree — this seat's row: rotate_at 0.4, worktree .agi/worktrees/seat-sensei-director), fall back to ladder.director_rotate_at (0.47) and SAY which source in the message; (5) RED-FIRST TESTS in test_rotation_alert.py: the registration text names UserPromptSubmit; pct at 0.63 × threshold prints 55; the wording line; a fixture worktree matching a seats row with rotate_at 0.4 is measured against 0.4 and the message names the row; the existing tests stay green. FALSIFIERS: a firing whose printed band is not b_frac × 100; a registration block naming SessionStart; a seat with rotate_at 0.4 measured against 0.47. FILE SCOPE: extensions/agi/hooks/rotation_alert.py, extensions/agi/tests/test_rotation_alert.py. EXCLUDED: ~/.claude/settings.json (the Prime's live install), rotate.py, config:*, every other hook. CEILING: up to 2 kids, the parent merges every kid branch into the round branch before done:. Disjoint from every other L1 round."
thought_session: sensei-director-genI-L1
title: rotation_alert.py registers under UserPromptSubmit, prints the band as a fraction of the threshold, names window vs line, and measures a seat against its own rotate_at
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-rotation-alert-hook-says-what-it-measures

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
