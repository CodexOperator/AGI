---
id: hypothesis:l3w4-branch-visibility
mint_id: 0722639346a540aa9a190151945dc638
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: quorum-2
location: source_root
scaffold_hash: 168d6bf31abee0bb
season: 2
testable_claim: After the change, a --branch agent reaped by dispatch.py's _reaper_phase carries a commits_ahead integer field in both agent.json and its manifest.json entry, computed via git rev-list --count base_branch..branch through locations.git_common_root -- present and correct whether the count is zero or positive -- and a non-branch agent's record is unchanged; proved by red-first tests that fail before the change and pass after, plus a full green suite.
thought_session: 4d069885-5b8e-47bd-b4c5-96a5b39ed870
title: A reaped branch agent's commit count is stamped into the round record, not hand-counted
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-branch-visibility

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?