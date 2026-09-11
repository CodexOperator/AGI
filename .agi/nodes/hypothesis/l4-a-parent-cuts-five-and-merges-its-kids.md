---
id: hypothesis:l4-a-parent-cuts-five-and-merges-its-kids
mint_id: c6ba13ede6664acbb03bf58b249cfaa6
type: hypothesis
parents:
  - goal:g4.1
next_edges: []
edited_by: belam-S1-L4-VII
scaffold_hash: e1379abbf68e1470
season: 2
testable_claim: "OWNER 2026-09-11 ~02:08Z, typed to the sanctuary-director seat and relayed two-step (verbatim in doc:l4-owner-decisions): \"let us let parents cut up to 5 kids at once\" and \"the new parent should be smart enough to handle that type of merge\". CONFIG HALF, applied by the Prime L4-VII: .agi/config.json spawn.parent_max_kids 5 (spawn_budget.parent_max_kids reads it: measured -> 5; the key was ABSENT and the default 4 ruled). CLAIM (the merge half, brief + code): a parent cuts up to spawn.parent_max_kids kids in PARALLEL when their file scopes are disjoint, each kid on its own loop branch cut from the parent branch (dispatch.py --branch already cuts from the spawner checked-out branch), and the PARENT MERGES every kid branch into the round branch before its `done:` — (1) the parent brief (brief.py parent tier) names the ceiling from config, the disjoint-scope rule and the merge protocol in bytes: merge kid branches in dispatch order with `git merge --no-ff` onto the round branch; a conflict in a NODE file is resolved by UNION of the Agent Notes and the higher-confidence verdict line, never a blind `git apply --3way`; a conflict in SOURCE is resolved by the parent as an edit it owns and names in its review note; (2) the round test files WITH THEIR NEIGHBOURS in suite order re-run on the MERGED bytes before `done:` — a green kid branch is not a green union; (3) the parent review note lists every kid branch merged, every conflict and how it was resolved, and every kid whose branch was NOT merged and why; (4) dispatch.py refuses a parent that requests more kids than the ceiling with the number in the message; (5) FIXTURES ONLY: a temp repo with a round branch and 3 kid branches (one clean, one node-conflicting, one source-conflicting) proves the protocol; nothing touches this repo during tests. FALSIFIERS: a parent brief still saying 2 serial; a union merge that drops a note; a `done:` on unmerged kid branches without naming them; tests green on a kid branch but red on the union with no re-run; a real branch touched by a test. SCOPE: brief.py (parent brief), dispatch.py (ceiling refusal, merge helper or a season.py merge_kids verb), tests beside them. Owner spend authorized: kids on the pi parent model."
thought_session: belam-S1-L4-VII
title: A parent cuts up to five kids in parallel on disjoint scopes and merges their branches itself before done — union for notes, tests on the merged bytes, conflicts named
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-parent-cuts-five-and-merges-its-kids

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
