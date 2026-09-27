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

## CORRECTIVE DH.524 -- closes mur-director-engine-17 DH.506-k1 + k2 (review accept_with_residue; verify failed / unstructured) + TMM.283
BASE      CUT FROM season2/loops/hypothesis-send-read-prints-ever-a00-907d12c6 tip 5cf6b511e (worktree a00-907d12c6). No merge. Never rebase.
1. send.py:3925 -- when cut < len(content) the marker write `content[:cut].rstrip("\n")+"\n"+READ_MARKER+content[cut:].lstrip("\n")` drops the file's trailing newline -> keep it byte-exact; one test: a partial read leaves unread blocks behind the marker AND the file still ends in exactly one newline.
2. TMM.283 (belam 04:31Z): dm-FILE sends to thought-master at 04:00:03Z and 04:03:09Z sit in the dm file but never registered pending -- the SENDER skipped the pending mark, not only read's cursor -> one test: a --to dm-file send registers pending for its recipient (send.py status shows pending >= 1 before any read); fix the sender path if the test is red.
3. experiment:a00-db001065-4d153e frontmatter says verdict proved / confidence 0.9 (:8, :21) while its body's PARENT DEMOTION (:115) demotes it -> set both fields to what the demotion says (write.py only).
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_send.py test_seatsig.py test_sensei.py test_heal.py test_bin_help_smoke.py test_write_self_row.py once (timeout 900, --basetemp under /tmp)
FILE SCOPE extensions/agi/bin/send.py (the read-marker write + the dm-file send's pending mark only) · extensions/agi/tests/test_send.py · experiment:a00-db001065-4d153e (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · net <= 12 production lines · <= 60 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

## CORRECTIVE DH.542 -- closes mur-director-engine-20 DH.524-k1 (verify: accept_with_residue; every unrefuted defect + missed item below)
BASE      CUT FROM season2/loops/hypothesis-send-read-prints-ever-a00-16f0ec5d tip 5c9c4120a (branch de-base-542). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Stale deferred sidecar suppresses the pending mark for a new no-pane dm — extensions/agi/bin/send.py:4040 — `not _read_deferred(root, other)` tests for ANY deferred body, so when a seat has a stale deferred body and its pane is gone the new unresolved dm is neither counted nor deferred (TMM.283 symptom returns for that seat).
2. Inbox half of TMM.283 (an unread sender-side record): an inbox `send()` to a seat with no resolvable pane still leaves pending=0 — send.py:2986 calls `_nudge_window(body=None)` and the no-target return at send.py:2288-2289 registers nothing; only send_dm was patched, so the sibling sender path keeps the same hole. The parent records it in experiment:a00-a46d3b83's THOUGHT as residue (a)/next-round target, but the first reviewer did not list it.
3. `_bump_pending` at send.py:4042 accrues a `.nudge.pending` sidecar for a seat that has no config:seats row at all (`_row_is_quiet` returns False for a missing row), so a recipient the graph never listed is counted. Parent probe P2 residue (b); a note, not a falsification.
4. a00-a46d3b83 `production_lines: 21` is `git diff --numstat` and counts the diff's comment/prose lines as production lines (the node itself admits this, residue (c)); note only.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_send.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat or worktree
FILE SCOPE extensions/agi/bin/send.py · extensions/agi/tests/test_send.py · .agi/nodes/experiment/a00-a46d3b83-8fc296.md · .agi/nodes/experiment/a00-db001065-4d153e.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over the ROUND BASE (git diff --numstat <tip above>) · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit on the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.542: mur-director-engine-20 DH.524-k1 verify residues + missed items, batched into one corrective (orders above, generated from the verify file; each item fixed or settled by a pasted command).
<!-- THOUGHT:END -->
