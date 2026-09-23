---
id: hypothesis:l4-nudges-have-classes-service-senders-never-nudge-post-dms-coalesce-into-one-digest-while-busy-and-quiet-system-silences-only-the-system-class
mint_id: a977d75eb13d4cb79846d0478342092b
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: belam
scaffold_hash: 15df5be907790499
season: 2
testable_claim: "(a) SERVICE senders -- heal, watch, wake repair, the after_join self-dm (rotate.py ~14527-14632 composes it with no config knob today) -- never fire a nudge, and skip the inbox copy when the same text was already typed into the pane; (b) a POST dm keeps its inline nudge, but while the pane is busy the deferred post dms coalesce into ONE digest nudge per nudge_stale_after_minutes window instead of one bare token each; (c) a settings token quiet-system on a config:posts row selects (a)+(b) for that row, the existing quiet token stays full silence, no token = today. Measured on the Prime 05:26-06:3xZ: 4 nudges = 1 inline dm + 2 bare tokens (deferred direct dms) + 1 after_join self-dm copy -> under the claim: 1 inline + 1 digest + 0. Falsifier: a service sender still nudges or double-delivers; two deferred post dms in one window produce two tokens; quiet-system silences a direct post dm; quiet lets anything through; a row with no token changes behaviour."
thought_session: dissolve-legacy-2026-09-19
title: "SM.110 (owner 06:3xZ via the Prime, queued after SM.108/109): nudges have CLASSES -- service senders never nudge, post dms keep the inline nudge but coalesce into ONE digest per stale window while the pane is busy, and a quiet-system settings token silences only the system class (quiet stays full silence)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-nudges-have-classes-service-senders-never-nudge-post-dms-coalesce-into-one-digest-while-busy-and-quiet-system-silences-only-the-system-class

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.110 BRIEF (sanctuary-master 09-18 06:1xZ; owner 06:3xZ via the Prime, banked doc:l5-owner-decisions: silence system nudges, keep direct dms, never full quiet). Kid measures first: send.py nudge path (where the inline nudge, the deferred bare token and the busy/coalesce decision live; nudge_stale_after_minutes), the after_join self-dm composer in rotate.py (~14527-14632), and the heal / watch / wake-repair senders. SHAPE (template-first): ONE sender class on the send path -- class = service | post, derived from the sender (a service sender names itself; a post row = post) -- read by the nudge decision; the row token quiet-system is a config cell like quiet ([config].md settings tokens), so a future class or token is a schema/template line. Each of (a) (b) (c) is a conjunct with its negative twin. CEILING 25 production lines (a 8, b 10, c 5, + the schema/template lines). TESTS (one file, test_send_nudge_classes.py, a stub pane/registry): (1) after_join self-dm -> no nudge, no inbox copy when the pane got the text; (2) heal / watch / wake-repair sends -> no nudge, inbox copy kept; (3) two post dms while busy within one stale window -> ONE digest nudge naming both, not two bare tokens; (4) quiet-system row: (1)-(3) hold AND a direct post dm still nudges inline when idle; (5) quiet row: full silence unchanged; (6) no token: today's behaviour byte-for-byte (regression); (7) the Prime's measured sequence (1 inline + 2 deferred + 1 self-dm) replays to 1 inline + 1 digest + 0. FILE SCOPE: send.py, rotate.py (after_join composer only), one shared helper the service senders import, [config].md settings token line, one test file. Queue: after SM.108 + SM.109 land (priority set by the Prime), no dispatch word needed -- drain when a slot frees. Delivery: batch + your mur review in one line; reds fixed in-loop. Inside the finish set (owner-added).
