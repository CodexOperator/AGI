---
id: hypothesis:l3-pi-install-patch-not-durable
mint_id: 8673d4c5b17d4070bdc9c960044640dc
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-IX
scaffold_hash: d44f906a82340dd4
season: 2
testable_claim: "After the change, an installed pi whose edit tool lacks the forgiveness normalisation cannot pass unnoticed: either the repo re-applies it at spawn or adapter load, or a preflight assertion fails loudly and early naming the fix; proven by a red-first test that simulates an install missing the normalisation and asserts the loud failure or the re-application, rather than asserting only that the patch is present today."
thought_session: belam-S1-L3-IX
title: The edit-tool forgiveness patch lives in the untracked pi install, so a pi upgrade silently reverts it and every kid quietly pays the turn again
---
<!-- BODY:BEGIN -->
# hypothesis:l3-pi-install-patch-not-durable

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done.

THE KID THAT CREATED THIS HAZARD IS THE ONE THAT REPORTED IT, WHICH IS EXACTLY THE BEHAVIOUR THIS PROJECT WANTS AND EXACTLY WHY IT MUST NOT BE LEFT AS PROSE. At L3.38 the `l3-pi-edit-tool-edits-array` kid fixed both roots of the edit-call defect and then wrote, unprompted, in its own caveats: "the tool-side forgiveness patch lives in the shared pi install outside this repo — a pi upgrade silently drops it; the brief segment plus repo test are the durable half."

WHY THIS IS WORSE THAN AN ORDINARY REGRESSION RISK. The patch sits in `dist/core/tools/edit.js` inside the shared pi install, which is NOT tracked by this repo, NOT versioned by the grid, and NOT covered by any test this repo runs — `test_edit_tool_forgiveness.py` drives the INSTALLED tool, so on the day a `pi` upgrade reverts the file that test goes red with no other signal, and every kid silently starts losing a turn again to the same defect. The failure is silent in the direction of looking fine: rounds keep completing, kids keep working, and the only symptom is a tax nobody attributes. This project has a name for that shape — a verify command that passes while the declared one dies at import launders a broken tree as a checked one (§6 item 39). Same family.

WHAT TO BUILD — one of these, argued in the node, not all of them: (a) a repo-owned patch or shim that re-applies the forgiveness at spawn time or at adapter load, so an upgrade cannot silently drop it; (b) a startup or preflight assertion that fails LOUDLY and early when the installed tool lacks `_normalizeEditsShapes`, naming the fix, rather than letting kids discover it one wasted turn at a time; or (c) a durable upstream path if one exists. **The bar is not "the patch is present today", it is "an upgrade that removes it cannot pass unnoticed."** If you conclude the repo genuinely cannot own this and a loud preflight check is the honest ceiling, say so plainly with the reason — that is a real result and it is better than a fragile fix that pretends to more.

NOTE THE HALF THAT IS ALREADY DURABLE and do not redo it: the `brief.py` kid-template segment teaching the correct call shape, and its content-pinning test in `test_brief.py`, are inside this repo and are already safe. Only the tool-side half is at risk. Scope to that half.

DO NOT: vendor the whole pi install into this repo; touch `.agi/nodes/.geometry/seats.md`; or start any seat (owner gate, HANDOFF §6 item 47).
