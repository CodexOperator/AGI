---
id: hypothesis:l5-drift-refusal-prints-its-message-once-not-twice
mint_id: b14d3f6bdf514c7081a5f4dfecba5d1e
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 2df4b56994742ced
season: 2
testable_claim: "rotate.py's _apply_staged drift-refusal branch (rotate.py:3967-3970, landed with L5.02) prints \"rename-post REFUSED: staged plan drifted\" to stderr TWICE on every drift refusal -- once at line 3967 with the drifted surfaces named, once at line 3970 as a bare unnamed duplicate left over from the round's own editing. The fix deletes the line-3970 duplicate, leaving exactly one refusal line (the named one). Purely cosmetic: return code 2 and the refusal semantics (stage left intact, nothing applied) are unaffected either way; no test currently asserts line count so none would need to change beyond an assertion added for this."
title: L5 drift refusal prints its message once not twice
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-drift-refusal-prints-its-message-once-not-twice

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
