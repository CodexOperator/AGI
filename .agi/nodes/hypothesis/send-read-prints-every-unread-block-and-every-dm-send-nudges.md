---
id: hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges
mint_id: 7009a03160b94e9998f14277a7242e3a
type: hypothesis
parents:
  - goal:g7.33.17
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: b1c52c4c5c82dda8
season: 2
tags:
  - engine
  - send
  - nudge
testable_claim: "(1) send.py read <me> prints every unread block from its inbox file AND every dm file it is party to, and says empty only when both are empty (2) no path advances the inbox read marker past a block read did not print (3) every send that lands in a dm file fires the recipient nudge like an inbox send (assigned: director-engine)"
title: "send.py read prints every unread block (inbox AND dm files) and every dm-file send nudges -- g7.33.17 row 20 (assigned: director-engine)"
town: core
---
# hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges

# hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges

## Measured
- `send.read` (extensions/agi/bin/send.py:3815) scans ONLY the recipient's inbox file (`_scan_messages` :2993, marker `READ_MARKER` :106) and returns at :3825 with `inbox for <me>: empty` when that file has no block past the marker -- it never consults the dm files under `.agi/comms/season-2/dm/`.
- thought-master 02:20-02:3xZ 09-27: `send.py read thought-master` printed `inbox ... empty` twice while director-engine's 01:49Z [red] and 02:16Z [rule] sat in `.agi/sessions/inbox/thought-master.md` with `# read up to here` ALREADY past them (file mtime 02:20:05Z) -- something advanced the marker without printing.
- director-thought's 21:37Z [merge-up] landed in its dm file and never nudged thought-master at all; TMM.271 (02:50Z) landed in director-engine's dm file and its nudge coalesced on a busy pane (relayed by thought-master's session).
- Nudge path: `_nudge_window` (send.py:2250), coalesce gate `_nudge_coalesce_reason` (:2049), marker/pending/lastread sidecars (:1634-1877).

## CLAIM
(1) `send.py read <me>` prints every unread block addressed to <me> -- from its inbox file AND from every dm file it is party to -- and says `empty` only when both are empty; (2) no path advances the inbox read marker past a block that `read` did not print; (3) every `send` that lands a block in a dm file fires the recipient's nudge exactly as an inbox send does (same coalesce/pending rules, never silently skipped).

## Dispatch line
config-max: none (paths already come from `_inbox_path` / `_dm_path`). template-max: none -- the owner's 'check dm file directly' stays an operational line on the cards until this lands. code: the dm-file branch of `read` + the marker-advance fix + the dm-send nudge -- the resolver that does not exist. The hub redesign stays in goal:send-is-hub-only; this round is the smallest fix.

## FALSIFIERS
- RED FIRST (both, on the current bytes, in a tmp comms root): a block appended to a dm file for <me> -> `read <me>` prints `empty`; a `send` whose block lands in a dm file -> no nudge recorded/pending for the recipient.
- A block past which the marker was moved without being printed exists after any read/peek/send sequence in the test.
- After the fix, a dm block is printed twice across two reads (the dm read cursor must advance too).

## TESTS
extensions/agi/tests/test_send_dm_read_and_nudge.py (new; tmp comms + tmp inbox roots only, tmux stubbed -- never the live pane or the live inbox). Neighbourhood (send): test_send.py test_seatsig.py test_sensei.py test_heal.py test_bin_help_smoke.py test_write_self_row.py + test_send_nudge_classes.py test_send_quiet.py test_send_rewind.py test_send_undelivered.py.

## FILE SCOPE
extensions/agi/bin/send.py · extensions/agi/tests/test_send_dm_read_and_nudge.py (new)

## CEILING
2 kids · <= 36 production lines · pi-free tier-0 · 0 USD. No test touches the live inbox, the live dm files or a real tmux pane.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version, minted by director-engine on thought-master's `dispatch now` (TMM.271, 02:50Z 09-27) for goal:g7.33.17 row 20, as its OWN round ahead of the queue (it no longer rides with send-is-hub-only). OWNER in thought-master's pane 02:28:27Z, verbatim: "Check dm file directly nudges have been buggy". OWNER in thought-master's pane 02:49:02Z, verbatim: "DT latest message seems nudges are growing more broken. Luckily the DE is on it we need it bad. If needed we can pause DT work for now to give DE more breathing room to implement quicker with a higher cap given no model container and no docker loader". Scope per TMM.271: a test that reproduces BOTH reds first; the smallest fix; the hub redesign stays in send-is-hub-only.
<!-- THOUGHT:END -->
