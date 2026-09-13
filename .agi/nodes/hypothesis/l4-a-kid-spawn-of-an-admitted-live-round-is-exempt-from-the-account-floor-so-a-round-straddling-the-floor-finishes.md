---
id: hypothesis:l4-a-kid-spawn-of-an-admitted-live-round-is-exempt-from-the-account-floor-so-a-round-straddling-the-floor-finishes
mint_id: b0d4630336204dac884a10a8a59271f1
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 027240ffb3272e62
season: 2
testable_claim: "goal:g15 SM.19 (OWNER order via SM, cut FIRST after SM.09, ahead of SM.16; floor context: account floor is $5.00, below it no new SM.* round). CLAIM: dispatch.py check_account_floor (around line 1801) is skipped ONLY for a --tier kid spawn whose parent (AGI_AGENT_ID) is present in the iter manifest with a currently live pid -- so a round already admitted and underway can finish its kid even if the account balance drops below floor mid-round. Key floor (per-spawn credential minting) is unchanged. Parent spawns are still refused below floor exactly as today -- only the kid-of-a-live-parent path is exempt. FALSIFIER: a parent spawn succeeding below floor (must still refuse); a kid spawn refused below floor despite its parent being a live, admitted round in the manifest (must NOT refuse). FILE SCOPE: dispatch.py check_account_floor and its kid-tier call site only. CEILING: <=30 lines net, <=4 tests."
title: a kid spawn of an admitted live round is exempt from the account floor so a round straddling the floor finishes
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-kid-spawn-of-an-admitted-live-round-is-exempt-from-the-account-floor-so-a-round-straddling-the-floor-finishes

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
