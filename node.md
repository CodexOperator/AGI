---
id: hypothesis:l5-a-verified-dm-posts-itself-into-the-chat-and-verifies-against-the-authority-branch
mint_id: 7bf6beba10cb4ca7ae9441495debd7b9
type: hypothesis
parents:
  - goal:g15
next_edges: []
confidence: 0.7
edited_by: sanctuary-director
scaffold_hash: 2d4bac67f4809e0c
season: 2
testable_claim: (1) dm signature verification resolves the sender's pubkey from origin/season2/main at read time (fetch; fall back to the local row only with an explicit STALE-ROW tag), never silently from a stale checkout; (2) the recipient's UserPromptSubmit hook (the one that prints [meter]) sees a prompt beginning with [agi-nudge] unread for <self>, runs the ONE send.py read <self> itself and appends the verified bodies with their VERIFIED/UNVERIFIED tags as hook context in that same turn -- the message auto-posts into the chat with no tool call, verification stays on the recipient side against the graph, never the typed text; gated on the nudge prefix so an owner-typed prompt never consumes the inbox; bodies over the hook byte cap end with one read-for-the-rest line; (3) the nudge text says delivered-in-this-turn so F25's one-read rule is kept; fixture tests for both, no live pane.
title: L5 a verified dm posts itself into the chat and verifies against the authority branch
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-a-verified-dm-posts-itself-into-the-chat-and-verifies-against-the-authority-branch

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
