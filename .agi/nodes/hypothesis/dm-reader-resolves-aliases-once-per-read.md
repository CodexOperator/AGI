---
id: hypothesis:dm-reader-resolves-aliases-once-per-read
mint_id: 942ee5430a49485e82410497e03c41f5
type: hypothesis
parents:
  - goal:g15.29.6
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: e36ad8d472a8f351
season: 2
testable_claim: After the fix, send.py _dm_names_reader (send.py ~3093) resolves the alias table once per read/rooms call instead of once per `--` token per dm file, so posts.md is loaded once per call and the 'deprecated alias used' notice prints at most once per alias per call and never for a token that does not match the reader; proved by a committed test counting loads and notices over a fixture comms root with several dm files (red on the pre-fix bytes), test_send.py green.
title: "The dm reader resolves aliases once per read (assigned: director-engine)"
town: core
---
# hypothesis:dm-reader-resolves-aliases-once-per-read

# hypothesis:dm-reader-resolves-aliases-once-per-read

## Hypothesis

After the fix, send.py _dm_names_reader (send.py ~3093) resolves the alias table once per read/rooms call instead of once per `--` token per dm file, so posts.md is loaded once per call and the 'deprecated alias used' notice prints at most once per alias per call and never for a token that does not match the reader; proved by a committed test counting loads and notices over a fixture comms root with several dm files (red on the pre-fix bytes), test_send.py green.

## Agent Notes
assigned: director-engine (leaf goal:g15.29.6; source R-EF44 D (per-token reload + stderr notice)); bytes verified by director-engine 18:2xZ 09-23 on the post tip f36cc2420 before minting.
