---
id: hypothesis:g716111-g5-send-treats-a-v5-post-as-a-peer
mint_id: a7b9bbfcae454733b2f4f93c0ebdd5e7
type: hypothesis
parents:
  - goal:g7.16.1.11.3
next_edges: []
edited_by: director-general-3
scaffold_hash: 445272492c7e49cb
season: 2
testable_claim: a send (inbox form) to an engine-v5 row on this box reports delivered-by-mail, a dm-file send says written not delivered, a foreign engine row is refused by name; a send from a v5 post worktree is signed and whois VERIFIED
title: "G5: send.py treats a v5 post as a peer -- delivered-by-mail, signed, whois VERIFIED"
town: core
---
# hypothesis:g716111-g5-send-treats-a-v5-post-as-a-peer

## Measured
- 11:00Z DG3 -> director-general-5 (engine v5): send.py printed "row window @22 is gone ... message written, no wake" and "[undelivered-yet] ... pane busy; the sweep retries" -- yet the post's cccc mail poll took the turn by 11:02Z (card commit 99f4d495d): the sender is told undelivered for a delivered message.
- 11:09Z the post user could not write MAIN's comms tree (belam:belam 775): PermissionError on the dm file -- every send from a v5 post failed. Box half CLOSED 11:10Z by DG3: setfacl -R g:agi:rwX + default on .agi/comms/season-2 and .agi/sessions/inbox (before-ACL /tmp/agi-parity/acl-before-comms.txt; undo setfacl -R -x g:agi -x d:g:agi on both).
- 11:10Z the post's send (AGI_SEAT set, as in its unit) landed but carries NO sig line although the post user reads its seat key (ACL r--).
## CLAIM
send.py treats a v5 post (config:posts row with an engine cell) as a first-class peer: a send TO it reports delivered-by-mail (its cccc poll), never undelivered-yet; a send FROM it is signed with its seat key and whois VERIFIED.
## Dispatch line
Kid answers FIRST: which send.py function decides "no window -> undelivered-yet", and where the signer looks for the seat key when cwd is a post worktree.
## FALSIFIERS
- F1 a send to an engine-v5 row still prints undelivered-yet.
- F2 a send from a post worktree (AGI_SEAT set) writes no sig line, or whois on it is not VERIFIED.
- F3 any send path tries tmux for an engine-v5 row.
## TESTS
test_send.py test_seatsig.py test_sensei.py test_heal.py test_bin_help_smoke.py test_write_self_row.py (the send neighbourhood), --basetemp under /tmp, plus new rows for F1-F3 on a tmp root.
## FILE SCOPE
extensions/agi/bin/send.py · extensions/agi/tests/test_send.py (or test_seatsig.py for F2) · this node.
## CEILING
production NET +30 lines · tests +60 · Sonnet 5.5 subagent (owner lanes 02:26Z) · 0 USD.

## CORRECTIVE G5.2 -- closes mur-de-base-g5 g5-code (review accept_with_residue; the verify stage left no file: the review's items stand)
BASE      de-base-G5 tip bc5b0171b. Never rebase.
1. send_room is unsigned: a room message from a post carries no sig -> sign it like send/dm (the same sig_line path). TRUE WHEN a room block from a post worktree carries env + sig and whois reads VERIFIED (a row).
2. Signed dms make the owner-veto gate reachable (_veto_answer_authorized accepts a dm block with a sig over an owner-role row): add rows proving a dm signed by a NON-owner seat is REFUSED as a veto answer, and an unsigned one too; only an owner-role signature passes.
3. The dm envelope vs readers: one committed row reads a signed dm block back through read_dm / _parse_blocks with the text intact (the cccc poll reads the same file).
4. wake / status for an engine post: report a by-mail verdict (one line, no no-target / reaper-log noise per heal poll).
DEMOTED   _engine_post reads local rows (fails open to the pre-diff behaviour, never worse) · the cccc poll itself lives outside this tree (item 3 covers the file contract).
FILE SCOPE extensions/agi/bin/send.py · extensions/agi/tests/test_send.py (and/or test_seatsig.py) · this node.
CEILING   production net +20 · tests +60 · Sonnet 5.5 subagent · 0 USD.
DONE      8999631f2: rooms signed (F2 room half red on OLD); veto gate PINNED (rows characterise the unchanged role==owner check at send.py ~5437 -- not a fix); signed dm read-back intact; wake/status by-mail; send neighbourhood 495 passed 8 skipped; tests +63 vs 60 (disclosed). mur-de-base-g5b: accept_with_residue.

## CORRECTIVE G5.3 -- closes mur-de-base-g5 verify missed (a)(b) + mur-de-base-g5b missed
BASE      de-base-G5 tip 8999631f2 + this node commit. Never rebase.
1. The by-mail announcement over-claims on the send_dm path (_announce_nudge ~1789-1796): print [delivered] by mail ONLY when the post's own poll will see the message (the inbox line its mail poll reads); otherwise say written, not delivered. TRUE WHEN a row covers send and dm to an engine row.
2. The engine short-circuit (~2489) returns BEFORE the foreign-box refusal (~2490): refuse a foreign-box row first. TRUE WHEN a row with an engine cell on another box prints the FOREIGN refusal, never by-mail.
3. wake's by-mail branch (~3017) prints a bare 'by-mail': name the seat and log one reaper record like its sibling outcomes (_wake_outcome).
4. wake vs status for an engine row with a live window: one order for both (engine first, or resolve first) -- they agree.
5. (belam 12:39Z [decision], measured DG3 12:40Z on thought-master-new) the agi-run mail poll -- .agi/nodes/.geometry/engine-wrap.md:25 -- with the post's inbox file ABSENT both stat calls print to the pane and return empty, so the test collapses to a one-argument test, always true: every 5 s it types the mail line + CR into the pane (it answered No-exit on a trust dialog). TRUE WHEN a missing inbox reads as size 0 with no stderr in the pane (stat ... 2>/dev/null || echo 0, both calls) and a row proves no line is typed while the inbox is absent or unchanged.
DEMOTED   room signatures not rendered by read_room/peek_room (a reader design item, not this claim) · the veto-via-room-line claim (refuted by the g5b verify).
FILE SCOPE send.py · test_send.py · .agi/nodes/.geometry/engine-wrap.md (item 5, one line) + its test row · this node.  CEILING production net +15 · tests +40 · Sonnet 5.5 subagent · 0 USD.

## CORRECTIVE G5.4 -- closes mur-de-base-g5c g5c-code (verify accept_with_residue: R1 R3 confirmed + missed M1 M2)
BASE      CUT FROM de-base-G5 tip cfa9b3e27 + this node commit (worktree /mnt/agi-ram/worktrees/de-base-G5). No merge. Never rebase.
1. The sibling stat in agi-run -- .agi/nodes/.geometry/engine-wrap.md:24 (the log-trim loop, stat -c%s ~/o) -- same class as G5.3 item 5. TRUE WHEN it reads an absent ~/o as 0 with no stderr (2>/dev/null||echo 0) and the item-5 regression row (or its sibling) covers line 24 too.
2. A FOREIGN engine row is announced as pane busy, the sweep retries -- send.py _announce_nudge (~1794-1805) -- a refusal that never retries. TRUE WHEN a send to an engine row on another box prints the FOREIGN refusal outcome by name (no pane-busy, no sweep-retries wording); a row proves it.
3. heal._repair_stranded_wakes (heal.py ~2338-2351) walks EVERY loaded row with no foreign-box gate, unlike send.wake_all_local (send.py ~3148-3150). TRUE WHEN it skips non-local rows the same way and a row proves a foreign engine row gets no wake call.
4. PIN the boxless design (review R2 + verify M2, demoted as a change): a row proves an engine row WITHOUT a box cell on a box-declaring graph is not an engine post (FOREIGN refusal, per boxes.row_is_local: every live row carries its own box), and on a box-less graph stays an engine post.
DEMOTED   R2 as a change (design per boxes.row_is_local + belam 09-27: an unset box is refused; all 6 engine rows carry box) · R4 fixed by the director in this commit (testable_claim) · M3 (tests run on the NEW checkout by rule) · M4 refuted · notes (reaper row per pass, poll env, double _engine_post).
FILE SCOPE .agi/nodes/.geometry/engine-wrap.md (line 24 only) · extensions/agi/bin/send.py · extensions/agi/bin/heal.py (_repair_stranded_wakes only) · extensions/agi/tests/test_send.py · this node.  CEILING production net +12 · tests +40 · Sonnet 5.5 subagent · 0 USD.

## CORRECTIVE G5.5 -- closes mur-de-base-g5d g5d-code (verify accept_with_residue: R1-R6 confirmed + missed M1 M2 M4)
BASE      CUT FROM de-base-G5 tip 7dad3b4d4 + the node commits after it (worktree /mnt/agi-ram/worktrees/de-base-G5). No merge. Never rebase.
1. (R2 + M4) send.py _announce_nudge (~1799-1810): the FOREIGN branch tests row.get("engine") only, so a foreign NON-engine row with a window/pid is still told pane busy / the sweep retries; its comment claims a locality check that does not run. TRUE WHEN the branch gates on boxes.row_is_local (the same guard as _nudge_target ~2496) for ANY row, the comment is true, and a row proves a foreign non-engine row gets the refusal, never pane-busy.
2. (M2) send ~3303: a foreign refusal still calls _register_unresolved, so the sender is told no retry while a pending mark waits forever. TRUE WHEN a refused-as-foreign send registers no unresolved/pending mark (same for the dm path if it pairs the same way); a row proves it.
3. (R4) one send to a foreign row prints the refusal TWICE (the memoised nudge line ~2504 + the [refused] line ~1801) and the (unset) label expression exists twice: ONE label source (a small helper or the memo's own) and ONE refusal line per send to the sender.
4. (R3 + M1) tests: the trim-loop row gets a positive control (AGI_PANE_MAX_MB=0 + a sized ~/o -> the trim happened); the foreign-row G5.4 row asserts calls == [] on its tmux recorder like its G5.3 sibling.
5. (R5 + R6) heal._repair_stranded_wakes uses heal's own module-level boxes import (not _send.boxes); the _announce_nudge and _repair_stranded_wakes docstrings name the FOREIGN outcome / the local-only walk.
DEMOTED   M3 (tests run on the NEW checkout by rule, the same as G5.4) · R7 the (NNNN B) size headers: a findings row (no reader; drift on every edit), proposed to SM with G6 · R1 (testable_claim written as a new key testable_claim=a): FIXED by the director in this node version (unset + set); write.py set accepted an invented key: a findings row.
FILE SCOPE extensions/agi/bin/send.py · extensions/agi/bin/heal.py (_repair_stranded_wakes only) · extensions/agi/tests/test_send.py · this node.  CEILING production net +10 · tests +30 · Sonnet 5.5 subagent · 0 USD.

## DONE (director record, closes mur-de-base-g5e missed M1)
G5.3 DONE cfa9b3e27 (mur-de-base-g5c) · G5.4 DONE 7dad3b4d4 (mur-de-base-g5d) · G5.5 DONE 3315ac438 (mur-de-base-g5e: review 11/11 MET, verify ACCEPT) -- item-to-test binding lives in the test docstrings (test_g53_* / test_g54_* / test_g55_* in test_send.py).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective G5.5: mur-de-base-g5d verify confirmed R1-R6 + missed M1 M2 M4; R1 was the director own slip (set testable_claim=a wrote a NEW key: set takes key SPACE value), fixed here by unset + set
<!-- THOUGHT:END -->
