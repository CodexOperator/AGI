---
id: goal:g7.16.1.9
mint_id: 8136c243e6844df1ab6a974d194d7bd9
type: goal
parents:
  - goal:g7.16.1
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.9
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: b2044afcc56dccb7
season: 2
seeds: []
status: horizon
tags:
  - magic-pane
  - tool-call
  - council-loop
title: "G7.16.1.9: one magic pane per post is the tool-call-turn anchor -- every engine event (docs, alarms, messages, rotations, write commits) reaches a post as one render tool-call turn"
town: core
---
# goal:g7.16.1.9

## OWNER 2026-09-30 01:1xZ, verbatim (Prime pane)
"Make sure we apply the same "tool call turns that pop into agent pane/session for all engine functions" philosophy. This includes memory alarms, message receipt, etc. it's all delivered through a unified tool call turn ran by the tmux pane. Why don't we merge some of the magic pane work from core and use that as the tool call turn anchor. Then one magic pane does send and receive for messages and takes care if rotations and write commits. Could have a poll built into it to keep messaging instant outside of busy panes"

## Why this exists
goal:g7.16.1 (the council loop): a next-bundle candidate minted by the Prime so the owner's line is not lost while the council rewrites goal:g7.16.1.7 (the first turn is a render tool call); the council folds or nests it there. It generalizes .7's first-turn render to EVERY engine event reaching a post, and it lands on the transport goal:g7.32.6 re-shaped (wake = an adapter verb). The magic pane system is being built by the owner on core/season2/main ("That branch is working on the magic pane system", 09-29); today an engine event reaches a post by at least four separate routes: the SessionStart hook's pasted text, the UserPromptSubmit meter line, a send.py nudge typed into the pane, and a CC SendMessage.

## Target end-state
- Every engine event a post must see (its first-turn docs, a memory alarm, a message receipt, a rotation prompt, a write-commit result) reaches it as ONE kind of turn: a tool-call turn whose result is a render, delivered by the post's own pane.
- ONE magic pane per post (merged from core's magic pane work, the tool-call-turn anchor) sends and receives its messages, runs its rotations and its write commits. From core, take ONLY the magic pane as it attaches to posts (the post anchor); NOT core's messaging integration -- the transport stays goal:g7.32.6 (owner 01:2xZ: "I just wanted to mention we strictly want the magic pane system as it attaches to posts. We don't need whatever messaging integration the other branch is doing. Just the magic pane anchor part to use as post anchor in system").
- A built-in poll keeps messaging instant for an idle pane; a busy pane receives at its next turn boundary, never mid-turn.

## Invariants
- A post never learns of an engine event by a second route once the pane route exists (one route per event kind).
- Nothing typed into a pane by a script lands as if the user typed it.

## Falsifier
1. A memory alarm, a message receipt and a rotation prompt each arrive in an idle post's session as a tool-call turn from its magic pane, within the poll interval.
2. Negative: zero engine events delivered by a send-keys nudge, a hook's pasted text or a second messaging route after the cutover.

## Out of scope
goal:g7.16.1.7 (fold target) · goal:g7.32.6 (the conversation-node transport this delivers) · engine CLIs as MCP tools (later, the owner: "not needed right now").

## Agent Notes
Assigned to **the council** (placement; fold into goal:g7.16.1.7 or nest under it).
