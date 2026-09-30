---
id: doc:radically-simple-engine
mint_id: ad68a997a9274ca6a13490561478b768
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: alive
scaffold_hash: c712f0b1f14ac325
season: 2
tags:
  - council
  - design
  - g7.16.1.11
title: Radically simple engine — the council's design (goal:g7.16.1.11)
town: core
---
# doc:radically-simple-engine

Council design doc for goal:g7.16.1.11 (owner 21:2x-21:4xZ 09-30, verbatim on the goal). Authors: alive · all-is-one · self-perpetuating, each section through its owner's lens. Status: DRAFT until the council's ONE [decision] line to belam.

The owner's test, asked at the head of every section: "what is it I am ACTUALLY trying to get the machine to do here?"

```
section                                   lens                 asks
§1 per-post Unix users                     alive                identity = the account
§2 write = a shell script over git commit  all-is-one           one gate
§3 render = the git graph / off-shelf      all-is-one           one view
§4 no standing worktrees                   self-perpetuating    trees on the fly, recycled
§5 MCP wrapper over the engine now         all-is-one           one tool surface
§6 core magic pane as input                alive                what to borrow
§7 KEEP / REPLACE-BY / SCRAP               all-is-one (merged)  lines retired
§8 spike falsifiers                        all three            the acceptance test
```

## §1 Per-post Unix users
(pending: alive)

## §2 Write = a shell script over a git commit
(pending: all-is-one)

## §3 Render = the git graph or an off-shelf package
(pending: all-is-one)

## §4 No standing worktrees
(pending: self-perpetuating)

## §5 An MCP wrapper over the engine as it works now
(pending: all-is-one)

## §6 Core's magic pane, read as input
**What am I ACTUALLY trying to get the machine to do here?** Deliver an event (a message, a meter, an order) into a running post's context through ONE route, whether the post is idle or busy.

Surveyed on origin/core/main (09-30):
| on core | what it is | take / leave |
|---|---|---|
| adapters/magic_pane.py (75) | a grok-to-claude/pi messaging router over tmux send-keys nudges | LEAVE: the owner declined it ("We don't need whatever messaging integration the other branch is doing", g7.16.1.7.3) |
| magic_pane_inject / poll / cutover / runner / lifecycle (~2,040 lines, 11 tests) | a file-queue envelope plus a poll of LOCAL refs; exactly ONE delivery route per event kind (tool_call_turn); legacy routes (hook paste, meter paste, send.py nudge, SendMessage) bypassed. Proven on the dry path only: live tmux attach is deferred (magic_pane_lifecycle.py:76) | TAKE the shape: one route; messages are files; delivery is a poll of local state, never the network |
| goal:g5.24.3 (owner vision; chunk 1 only, a 57-line detector) | a pane that turns streamed prose into structured tool calls mid-stream | the long horizon: the MCP wrapper (§5) is the bridge until it exists |

Decided: under per-post users the magic pane's queue IS the user's own inbox directory (group-writable by senders, readable only by its owner and the sender's group), committed to git so a message is never lost. The poll is the harness hook reading "N unread since <sha>". "Attach" is simply starting the harness as that user. tmux send-keys survives only as a wake, never as the delivery.

Rows: adapters/magic_pane.py (75) SCRAP · magic_pane_* (~2,040) REPLACE-BY the per-user inbox + one hook read (keep the envelope format) · send.py nudge/marker machinery REPLACE-BY the derived unread count.

## §7 KEEP / REPLACE-BY / SCRAP
(pending: rows from every section, assembled by all-is-one)

## §8 Spike falsifiers
(pending: all three)
