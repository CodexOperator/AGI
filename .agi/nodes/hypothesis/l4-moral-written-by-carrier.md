---
id: hypothesis:l4-moral-written-by-carrier
mint_id: ab8cafa5f47b42e087066f5e23850361
type: hypothesis
parents:
  - goal:g13
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 1df54467ea6a260a
season: 2
status: pending
tags:
  - l4
  - g13
  - schema
testable_claim: "`.agi/context/schemas/[moral].md` carries the owner-only write rule as a `written_by` field (DATA, read by the writer), and BOTH hardcoded literals in `extensions/agi/bin/write.py` are deleted: `edit.node_id.startswith(\"moral:\") and actor != \"owner\"` at L524, and `node_type == \"moral\" and actor != \"owner\"` at L926. The refusal is derived from the schema instead. PROVED BY: a moral edit without `--actor owner` still refuses WITH THE SAME MESSAGE; the existing owner-only tests in `extensions/agi/tests/test_write.py` (from L2.08) pass UNCHANGED — they are the gate and must not be edited to fit the refactor; `grep -n 'moral' extensions/agi/bin/write.py` shows no owner-rule literal left; and no other node type's write rule changes. This is a PURE REFACTOR: behaviour identical, rule relocated from code to data. HARD CEILING: 2 kids. 🔴 Do NOT run the full pytest suite — the prime may be running it; run `pytest extensions/agi/tests/test_write.py -q` only, and say so in your report."
thought_session: sanctuary-director-genVI-L4
title: The moral owner-only rule is hardcoded twice in write.py, so the rule lives in code instead of in the type that owns it
---
<!-- BODY:BEGIN -->
# hypothesis:l4-moral-written-by-carrier

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
