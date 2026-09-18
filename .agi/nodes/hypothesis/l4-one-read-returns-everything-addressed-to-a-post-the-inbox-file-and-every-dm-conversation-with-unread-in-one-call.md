---
id: hypothesis:l4-one-read-returns-everything-addressed-to-a-post-the-inbox-file-and-every-dm-conversation-with-unread-in-one-call
mint_id: dbba1bbdbe014f268a6d9beb115967b8
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: da9c8fbd3355fed7
season: 2
testable_claim: "(1) `send.py read <post>` returns the inbox file's unread blocks AND the unread blocks of every dm conversation file that names <post> (.agi/comms/<season>/dm/<a>--<b>.md, either order), each block prefixed by its conversation id, and marks every returned block read in its own channel (read markers stay per channel; nothing is returned twice, nothing is skipped). (2) the nudge composer (send.py / rotate.py after_join, SM.110) previews dm-channel messages with the SAME instruction \"read <post>\" -- which now suffices -- and the UserPromptSubmit mail hook delivers dm-channel blocks the same way it delivers inbox blocks. (3) `peek <post>` shows both channels without flipping either marker. (4) tests in a tmp comms root: a dm-channel message is returned by `read <post>` exactly once and marked read; the inbox path is byte-identical to today when no dm has unread; a nudge preview for a dm-channel message reads back through `read <post>`. MEASURED CAUSE: director-sanctuary's 22:03Z SM.122 [merge-up] and thought-master's 20:0xZ/21:0xZ [ask] lines sat in .agi/comms/season-2/dm/*--sanctuary-master.md while `read sanctuary-master` (inbox file only) returned empty four times this generation; the messages were found by grep. CEILING 15 production lines."
title: "SM.126 (owner 22:2xZ in the sanctuary-master pane: \"Do we need to do a small follow up on that swallowed nudge?\"; measured 4 swallowed this gen): one read verb returns everything addressed to a post -- the inbox file AND every dm conversation with unread -- in one call, labelled by conversation, and the nudge line's instruction is exactly that call"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-one-read-returns-everything-addressed-to-a-post-the-inbox-file-and-every-dm-conversation-with-unread-in-one-call

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SCOPE ADDED from SM.117b (experiment:a00-4922be82-9f3b11, lean_disproved:70 on the delivery tick): the untracked sessions/inbox store can never be the cross-box channel; the git-tracked comms dm transcript is. So this round also (d) makes crons.py apply mkdir the log dir before rendering, and (e) makes mail_poll on a remote box consume the tracked dm transcript (send.py read --dm <peer> --me <post>) -- or re-points read --box-local at it -- with a test on a second clone that a dm pushed from one clone is returned by read <post> on the other after one tick. Ceiling 15 -> 25 for the two additions.
