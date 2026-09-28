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

## CORRECTIVE DH.561 -- closes mur-director-engine-24 DH.542-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-send-read-prints-ever-a00-e7cea940 tip 7502fa786 (branch de-base-561; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Hard ceiling breached 2.5x and the self-report cites the wrong cap (.agi/nodes/hypothesis/send-read-prints-every-unread-block-and-every-dm-send-nudges.md:72)
2. 2. New over-count: a self-copy send now marks its own inbox pending (extensions/agi/bin/send.py:3025)
3. MISSED-1 (_deferred_blob is a new raise path in the send hot path): send.py:1681-1685 catches ONLY `OSError`, while its immediate sibling `_read_deferred` at send.py:1765-1772 catches `Exception` (noqa BLE001) and returns None. A non-UTF-8 or hand-edited `.nudge.deferred` makes `p.read_text()` raise UnicodeDecodeError, which is a ValueError, not an OSError -- so the exception escapes `send()`/`send_dm()` at a point AFTER the record is already durable (the inbox block is written at send.py:3004-3005, the dm file at :4060-4061). The old bytes could not raise here, because the guard used the Exception-swallowing reader. Fix is one word (`except Exception`). Low reachability and honestly labelled: `_store_deferred` uses json.dumps with the default ensure_ascii=True (:1812,:1819), so an organically written sidecar is pure ASCII and never trips it; the exposure is a hand-edited or non-Python-written sidecar.
4. MISSED-2 (the self-copy fix predicate already exists and is not passed): `_sender_class(root, sender, to) == "service"` (send.py:1612-1621) already encodes 'a self-copy wakes nobody'; `_register_unresolved` (send.py:1688) simply is not GIVEN the sender, which is why defect 2 reproduces. Both reviewers described the hole but neither named the ready-made predicate, and neither observed WHY the round's green suite cannot see it: the only committed self-copy test (test_send_nudge_classes.py:79-88) writes a `settings="quiet-system"` row, and that is precisely the shape where `_nudge_window` returns True at send.py:2309-2313 and no mark is ever registered.
5. MISSED-3 (the round repeats on its OWN node the accounting error it diagnosed as item 4): node:143-144 states that a node's `production_lines` field is `git diff --numstat` counting prose as production, and leaves that node's field alone -- yet the kid writes `production_lines: 38` (node:24) and 'Net production lines 38 (44 - 6)' (node:133) by the same prose-inclusive arithmetic on its own node. Measured over the 44 added send.py lines: 4 blank, 3 `#` comment, 14 docstring, so ~23 real code lines. This corroborates defect 1 (over 15 on the strictest reading too) rather than excusing it, and the field is wrong under the definition the round itself published.
6. MISSED-4 (the orders' ROUND BASE is one commit behind the real branch point): hypothesis:...md:62 says 'CUT FROM season2/loops/hypothesis-send-read-prints-ever-a00-16f0ec5d tip 5c9c4120a' and :72 measures 'over the ROUND BASE (git diff --numstat <tip above>)', but the kid commit 272b777f7's parent is 6ca377e7f, not 5c9c4120a (272b777f7 is a single-parent commit; 6ca377e7f is itself a child of 5c9c4120a and is a director-engine provisioning commit). The ceiling arithmetic is unchanged because 6ca377e7f touches no send.py line (both numstats read 44/6), so defect 1 stands -- but the node's pasted numstat command (node:128) measures against a base one commit off the branch point, and a director reading it cannot see that the two happen to agree.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_send.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/send.py · extensions/agi/tests/test_send.py · .agi/nodes/experiment/a00-110519ac-a3bc43.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 7502fa786 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.637 -- closes mur-director-engine-36 DH.602-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-send-read-prints-ever-a00-5e28072a tip c8f5b36fa (branch de-base-637; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 2. The keep-bytes branch (send.py:1815) also fires on a DECODABLE bodyless sidecar, mislabels it 'unreadable', and leaves that seat permanently count-only (the node's own THOUGHT names this degradation only for the undecodable case).
2. No committed test covers the POSITIVE side of the new rows guard (send.py:1708-1710): a LISTED seat, in a table the reader actually sees, must still register its mark. `test_unlisted_recipient_registers_no_pending` (test_send.py:7979-7986) asserts the negative only, and the green siblings that seed a table use `_plain_seats` (test_send.py:7910-7911), which writes to `project/nodes/.geometry/seats.md` — a different root, per the node's own ITEM 2 — so `_locally_loaded_rows` sees no table and the branch is inert in all of them. The real half of the first reviewer's defect 1, stated correctly, is this test gap; the node names the risk (P5) and follows it with neither a test nor a fix.
3. The parent's P1-P5 evidence carrying `verdict: proved` lives in a /tmp script (node body: `/tmp/agi-probe-602/test_parent_probe.py`) and in prose; nothing in the repo can re-run it. The [experiment] schema's additive `probes:` field (.agi/context/schemas/[experiment].md — 'the parent-run negative probes, one per claim conjunct of the target hypothesis; each = {conjunct, class, cmd, expected, observed, result}. Recorded by cli.py done like evidence_runs') is the sanctioned home for exactly this and is unused on the node. (The kid's own P4 control IS reproducible and I reproduced it: with 35d9465c1's send.py the three new tests go red and the sidecar is clobbered.)
4. The harness trap the round itself discovered — the two seats roots, where `_plain_seats`'s path made the author's first version of the test green for the wrong reason (node ITEM 2, final paragraph) — is recorded only in a per-round node body, with no comment at test_send.py:7979-7981 or on the helper at :7910. Per 'notes land in templates or configs, then individual role docs, then town board node', that standing truth belongs where the next author meets it, and it will otherwise be re-tripped.
5. The node's THOUGHT overstates its own cost: 'an undecodable sidecar is kept FOREVER — every later dm on that seat is only ever counted, never carried, because _clear_deferred only runs when a body was typed.' `_clear_deferred` at send.py:2598 runs on the general successfully-typed-nudge path without that condition (and at send.py:2539 on the stranded-ownership path), so the stall ends at the first nudge that types into the pane. The honest recovery decision the round defers to 'the next round' is scoped against an overstated cost.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_send.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/send.py · extensions/agi/tests/test_send.py · .agi/nodes/experiment/a00-ea09e5b6-1db479.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over c8f5b36fa · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    IN PROGRESS, not landed: DH.657 QUEUED (not yet dispatched); round work so far on loop branch season2/loops/hypothesis-send-read-prints-ever-a00-3e020c98 tip 3dd7348c5.
ROUNDS    this post's rounds on this node: DH.602 DH.637 DH.657; the open round's bytes live on its loop branch, never on the post branch, until its mur clears.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.637: mur-director-engine-36 DH.602-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
