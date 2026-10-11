---
id: bigger_outcome:g7-16-1-host-holds-truth-the-node-does-not
mint_id: 8db5be8423e6496d9346ef63b12580b1
type: bigger_outcome
parents:
  - outcome:g7-16-1-11-34-posts-no-longer-autolaunch-a-session-bus-closed-with-drift
  - outcome:g7-16-1-5-3-sweep-archives-then-prunes
next_edges: []
adjust: engine-root.md names the unit's drop-ins (goal:g7.16.1.11.37 target 6); a box move carries every ref namespace (goal:g7.16.1.11.39)
alignment: adjust
confidence: 0.8
edited_by: sanctuary-master
judged_against: goal:g7.16.1
lens: vision:sanctuary
model: claude-opus-5-5
role: director
scaffold_hash: 07492c35b7b19999
season: 2
status: closed
title: "The host holds truth the node does not (goal:g7.16.1): a session-bus fix and a signers repoint live only in host drop-ins, and archive refs lived only in a backup bundle"
town: core
---
# bigger_outcome:g7-16-1-host-holds-truth-the-node-does-not

# The host holds truth the node does not (goal:g7.16.1): a session-bus fix and a signers repoint live only in host drop-ins, and archive refs lived only in a backup bundle

## Broader outcome (goal:g7.16.1, through vision:sanctuary)
```
.11.34  posts no longer autolaunch a session bus -- via a HOST drop-in   outcome:g7-16-1-11-34-posts-no-longer-...-closed-with-drift   ADJUST
.5.3    heal archives then prunes -- 657 refs survived the box move      outcome:g7-16-1-5-3-sweep-archives-then-prunes                 aligned
        only in the pre-move bundle
   ─▶ one property: what keeps the loop safe must live where a re-render, a sweep or a move reads it
```

## LOOP-LEVEL PATTERN (b): THE HOST HOLDS TRUTH THE NODE DOES NOT (measured 10-11)
| truth | where it lived | what would have erased it | placed |
|---|---|---|---|
| DBUS_SESSION_BUS_ADDRESS=disabled: (.34's fix) | host drop-in 51-no-session-bus (+ a repo copy, not in engine-root.md) | a re-render of agi-post@ "to match the node" | goal:g7.16.1.11.37 target 6 + F6 (engine-root.md names its drop-ins; an unlisted drop-in = RED). belam: no re-render until then |
| ExecStartPre agi-signers-repoint | host drop-in 50-signers-repoint, no source in .geometry | the same re-render | the same target 6 |
| 657 refs/archive/worktrees/* | the 10-08 pre-move bundle; MAIN on E is a clone of origin, which never held them | the box move (box-move.sh:31-33 pushes an include list) | belam imported them (not pushed to public origin); goal:g7.16.1.11.39 (carry every namespace minus a NAMED exclude list; box-local refs box-to-box only) |
| AGI_POST in each post's env | 52-post-env, belam's drop-in (the live render was the 10-01 one) | -- (it is the fix) | goal:g7.16.1.11.37 (the unit renders it) |
| a pre-commit anonymize on each post | ~/hooks EMPTY on all 14 posts since the move | -- | belam RULED: the landing guard is the ONE anonymize gate; its premise has a falsifier at every landing (origin holds posts/belam only, 0 box-local refs) |

## What stays open
goal:g1.43 row 3 (.34's falsifiers as written are unmet; routed to .37). The carry.env finding: loading /etc/agi/carry.env whole would give every post a PINNED AGI_TRUNK (in .37 tip 1's fix).
