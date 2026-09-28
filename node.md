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


## CORRECTIVE DH.657 -- closes mur-director-engine-40 DH.637-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-send-read-prints-ever-a00-3e020c98 tip 3dd7348c5 (branch de-base-657; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. RESIDUE 1 — send.py:1810, the round's new docstring re-asserts the refuted 'kept for ever, pinning that seat to count-only' claim
2. RESIDUE 2 — a00-ea09e5b6-1db479.md:137 the false 'undecodable bytes forever' sentence survives in an in-scope node body
3. RESIDUE 3 — a00-143f92b1-0696a2.md:117 diff provenance is false (all 32/7 is this round's own two hunks; cap is not 40; true net is +25)
4. RESIDUE 4 — send.py:1816 a 0-BYTE sidecar is classified 'unreadable' and kept, pinning the seat to count-only though it strands nothing
5. MECHANISM the round's stated premise gets half right, and its new test pins the wrong half: 'bodyless but carrying queued dms' (send.py:1819-1821) keeps a shape whose queued bodies NO code path can ever read. The only reader of `others` is _notify_undelivered (send.py:2876), reached solely from wake_all_local's `rec = _read_deferred(root, name)` (send.py:2917 -> :2926), and _read_deferred returns None for a falsy body (send.py:1779) -- so for this shape rec is None and no undelivered notice is ever sent. The next successful typed nudge then _clear_deferred UNLINKS THE WHOLE FILE (send.py:1872-1875 via :2623), destroying the queued bodies rather than delivering them. The docstring's premise '`others` is the only field that carries an undelivered dm' (send.py:1811) is true of the FIELD and false of the delivery: test_bodyless_sidecar_with_queued_dms_is_kept (test_send.py:8024-8038) pins bytes that are guaranteed lost, which is a green test that requires a defect. Not a regression (the pre-fix guard kept this shape too) -- but the honest shape here is the same one the round used for the 0-byte case: keep the BYTES, release the seat.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_send.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/send.py · extensions/agi/tests/test_send.py · .agi/nodes/experiment/a00-143f92b1-0696a2.md · .agi/nodes/experiment/a00-ea09e5b6-1db479.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 3dd7348c5 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE EG.22 -- closes mur-eg-7 DH.657-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-send-read-prints-ever-a00-52e8835e tip 48ef5a79b (branch de-base-EG.22; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 2. Carried `others` still die to a premature clear — send.py:2645 — read (:3979-3981) and the successful-typed nudge (:2643-2645) both _clear_deferred (unlink, :1890-1899) before wake_all_local can reach _notify_undelivered (:2948)
2. 3. HARD CAP breach — send.py:1884 — 35/13 = +22 net production over 3dd7348c5 against the orders' '<= 15 ... a byte or kid over it = the round is cut'
3. Stale file:line citations across the round's central evidence table — a00-5e3cfa03-650288.md cites send.py:2870 `_notify_undelivered` (actual :2892), :2917 `rec = _read_deferred` (actual :2939), :2926 `elif rec is not None` (actual :2947), :2623 `_clear_deferred` (actual :2645), and `_deferred_queued send.py:1823` (actual :1828); the same drift repeats in the PARENT REVIEW and THOUGHT ('send.py:2917 -> :2926', 'the takeover are IN scope ... send.py:1823', 'send.py:4043'). Every pointer past :1833 is the 3dd7348c5 line number, off by exactly this diff's +22 net. The table IS the round's proof, and a reader who follows it lands 22 lines early. Not a mechanism defect, but it is the one thing in the diff that a later reader will actually use.
4. The disproven sentence was replaced but not retracted — a00-143f92b1-0696a2.md:147 (THOUGHT: 'the 32/7 worktree numstat is DH.602's +11 net plus this kid's +14') and :153 (Agent Notes: 'the WORKTREE over base c8f5b36fa reads 32/7 send.py because DH.602 left its own +11 net uncommitted in this shared tree') are now demonstrably false against the base commit c8f5b36fa (which carries DH.602's 15/4), and the round rewrote only the SUITE paragraph. The file now asserts both a true and a false provenance in one document; the fix is a one-line retraction in each.
5. The evidence for the fix is thinner than the SUITE line implies — on the exact reviewed tree (`git archive 48ef5a79b` extracted to /tmp, `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_send.py -q`) the result is 353 passed, 6 skipped-equivalent absent, and `test_undecodable_deferred_bytes_are_still_kept` also passes on the PRE-fix bytes (pre-fix returned 'unreadable' for every shape) — it is a guard against over-reach, not a red-first control. The node says so honestly at the probes list; naming it so the +22 helper is not read as covered by a discriminating test.
6. No real-resource touch and no demotion, re-checked fresh: all three new tests use the `project` tmp fixture plus `_plain_seats` and `_fake_tmux_pane`, which monkeypatches `send_mod.subprocess.run` wholesale (test_send.py:320-345) over `_FixturePane` (:200-216) — no live pane, seat, inbox or crontab; and the diff deletes nothing under .agi/nodes (numstat shows 0 deletions in all three node files), so there is no demotion by deletion.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_send.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/send.py · extensions/agi/tests/test_send.py · .agi/nodes/experiment/a00-143f92b1-0696a2.md · .agi/nodes/experiment/a00-5e3cfa03-650288.md · .agi/nodes/experiment/a00-ea09e5b6-1db479.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 48ef5a79b · <= 40 test lines net over 48ef5a79b · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 48ef5a79b <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE EG.41 -- closes mur-eg-12 EG.22-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-send-read-prints-ever-a00-6107c92f tip 38fa6e926 (branch de-base-EG.41; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
ORDERS    THIS text is the order set; the loop branch's copy of the hypothesis node does not carry the director's CORRECTIVE sections (the post branch does) -- never report that as a defect.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 2. The item-3 citation correction leaves one pointer stale -- .agi/nodes/experiment/a00-5e3cfa03-650288.md:133 (asserts `1816-1817` is the 0-byte guard)
2. 3. New node's evidence table cites `_print_deferred_block` at 3895-3898 -- .agi/nodes/experiment/a00-c3bf7379-8e12ed.md:42
3. 4. Clear drops falsy-body queued entries while the takeover carries them -- extensions/agi/bin/send.py:1904 (two preservation rules for `others`, undocumented)
4. 6. Retraction preserves a 17/3 production count numstat cannot reproduce -- .agi/nodes/experiment/a00-143f92b1-0696a2.md:155
5. A FOURTH stale pointer of the same class as #3, and the worst-placed one: .agi/nodes/experiment/a00-c3bf7379-8e12ed.md:45 cites `_notify_undelivered` at `send.py:2935-2957` under a table headed '(post-fix numbering)'. On the post-fix tree (38fa6e926 and the kid's own 057d478a8) the def is at send.py:2906 and the function ends at 2943; 2935-2957 is the notice f-string through `wake_all_local`'s `rec = _read_deferred(root, name)` at 2953. This is the ONLY reader of `others` (2906-2943, reachable only from wake_all_local:2953) -- i.e. the exact reader the node's central claim rests on, and the one the node's own 'Honest limits' says it did not exercise.
6. The retraction's SECOND surviving falsehood (sharper than #6): because `git show 1cf2b3665`'s two hunks are entirely the kid's own ITEM 1 work, the surviving claim at .agi/nodes/experiment/a00-143f92b1-0696a2.md:155 -- 'the over-cap number is real and lives in the EARLIER rounds residue, not in this kid' -- is false as well as the 17/3 figure. The node therefore still asserts an under-cap round that its own commit shows at +25 net against a stated cap of 15. One paragraph, one write.py edit; nobody should have to re-derive it.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_send.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/send.py · extensions/agi/tests/test_send.py · .agi/nodes/experiment/a00-143f92b1-0696a2.md · .agi/nodes/experiment/a00-5e3cfa03-650288.md · .agi/nodes/experiment/a00-c3bf7379-8e12ed.md · .agi/nodes/verdict/experiment_a00-c3bf7379-8e12ed.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 38fa6e926 · <= 40 test lines net over 38fa6e926 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 38fa6e926 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE DH.EG.77 -- closes mur-eg-21 EG.41-k1 accept_with_residue (no verify)
BASE      CUT FROM season2/loops/hypothesis-send-read-prints-ever-a00-c526a7da tip ecaab9920 (branch de-base-EG.77; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
The parent's own harvest dm (07:40Z) measured item 1-2's shipped numbers as 3911-3927 / 2920-2957 (one call site 2976) / def read( 3970 -- RE-MEASURE with `git show <your tip>:extensions/agi/bin/send.py | grep -n ...` and paste; never copy these. For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. ITEM 5 -- the round's own +14 docstring re-staled the pointer it was ordered to de-stale -- .agi/nodes/experiment/a00-c3bf7379-8e12ed.md:45 -- The diff adds 14 lines at send.py:1899-1913, so on the tip it ships _notify_undelivered is 2920-2957 (call 2976), _print_deferred_block is 3911 (print 3921-3927) and the read call site is 4008 -- while the node text, at :42, :45 and :154, certifies 2906-2943, 3897-3913, 2962 and 3995 against 'tip 38fa6e926', now one commit stale. The parent review already demoted this item in the same file (:242), so the chain is honest, but the wrong numbers still ship under a node the merge promotes.
2. Second stale pointer shipped on the sibling node (def read 3956) -- .agi/nodes/experiment/a00-5e3cfa03-650288.md:135 -- The EG.41 note certifies 'send.py:4043 for def read(, which is 3956 at this tip'; at ecaab9920 def read( is send.py:3970. The other numbers in the same note (1779, 1806-1825, 1818-1819, 1828, 1841, 1890) sit above the docstring and are correct.
3. One node, two verdicts: frontmatter proved beside an embedded parent review at 55 -- .agi/nodes/experiment/a00-cf800c23-1459e5.md:40 -- Frontmatter reads 'verdict: proved' (what the graph queries, and what commit bc82f0a14 'a00-c526a7da done: ... verdict=proved' set), while the THOUGHT at :242 records the same parent's own judgement as 'ITEM 5 DEMOTED, verdict inconclusive_lean_proved:55'. A reader taking the frontmatter gets a stronger claim than the review on the file supports.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE .agi/nodes/experiment/a00-143f92b1-0696a2.md · .agi/nodes/experiment/a00-5e3cfa03-650288.md · .agi/nodes/experiment/a00-c3bf7379-8e12ed.md · .agi/nodes/experiment/a00-cf800c23-1459e5.md (write.py) · the kid's own node
CEILING   HARD CAP: this kid only (claude-code text-fix, skill agi-corrective §3a) · 0 production lines · 0 test lines · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat ecaab9920 <your final tip>` on your node (an empty range is not a measurement)
COMMIT    every node edit on your loop branch before you exit (cli.py done; g7.33.19 row 13)


## CORRECTIVE DH.EG.120 -- INTEGRATION RED: the EG.77 chain meets the landed EG.72 box rule (director-measured at merge)
BASE      CUT FROM de-base-EG.120 tip 42b212b06 = the director's merge of the post (which carries the landed EG.72 box rule) into the EG.77 chain tip 39b1b37fd; merge-tree clean. No further merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number).
1. RED AT THE CUT, measured: `pytest extensions/agi/tests/test_send_dm_read_and_nudge.py test_box_identity.py test_box_guard.py` = 1 FAILED, test_box_local_row_does_not_print_empty_before_the_dm_sweep ('the row's dm block never printed', output EMPTY); it PASSES alone on the chain tip 39b1b37fd. Its fixture rows carry box 'local', and the landed EG.72 rule (boxes.py this_box + row_is_local: an unset AGI_BOX is refused, an empty or unknown row box is NOT local) now drops that row. FIND which reader drops it (send.py mail_poll --box-local branch, _locally_loaded_rows, row_is_local) and PASTE the proof.
2. DECIDE AND STATE, on your node: is the defect in the TEST (its fixture predates the box rule: a local row must carry this box's alias and the test must set AGI_BOX via monkeypatch) or in the CODE (the --box-local branch must still sweep a row the rule keeps)? The landed EG.72 rule is the contract -- never weaken it to make this test pass. Fix exactly one side; the D5 assertion (no false 'empty' before the dm sweep) must still discriminate.
3. At your tip: the three files above + test_send.py GREEN, pasted; never delete or weaken an assert.
DIRECTOR (anchor rule): cite a function / heading / cell key; a line number only where the claim IS the line; paste a git grep -n hit for each name at your tip.
DIRECTOR (numstat self-reference): measure `git diff --numstat 42b212b06 <tip BEFORE your paste commit>`, paste it, label it so.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_send_dm_read_and_nudge.py test_box_identity.py test_box_guard.py test_send.py + test_bin_help_smoke.py once (timeout 900, --basetemp under a fresh mktemp -d, env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_send_dm_read_and_nudge.py · extensions/agi/bin/send.py (the --box-local read branch ONLY, if item 2 finds the defect there) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 10 production lines net over 42b212b06 · <= 12 test lines net over 42b212b06 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE DH.EG.137 -- closes mur-eg-42 EG.120-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-send-read-prints-ever-a00-a603ca83 tip 007221c02 (branch de-base-EG.137; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Foreign-box leg asserts only stdout absence, not the naming contract — test_send_dm_read_and_nudge.py:430; stderr is never inspected, so a silent drop of foreign rows (the branch's own contract at send.py:5889) passes green
2. The round's own conjunct was never negatively probed. The base red at :411 was the box gate dropping the row, so at the base the D5 assert about the pre-sweep `empty` line (test:417, 'inbox for' not in out) was never reached, and neither the kid's nor the parent's probes touch it -- both probes delete/weaken an ADDED line. UNVERIFIED (I did not run it: it needs a modified copy of the tree under test, and this review may not author a probe that drives send.main): drop the single `quiet_empty=True` keyword at send.py:5876 in a scratch copy of the tip and run `pytest extensions/agi/tests/test_send_dm_read_and_nudge.py -k box_local`; by reading it must go red at :417 because read() prints 'inbox for {me}: empty' at send.py:4126-4129 whenever quiet_empty is false. Worth a one-line record, not a demote.
3. The two evidence records of the same call disagree on the exception class and nobody reconciled them: the kid's Item 1 quotes the RuntimeError from boxes.py:167, the parent's probe 2 (node:16) records 'this_box() with AGI_BOX unset RAISED SecretsError' (SecretsError originates only in envfile.py:141-150, :172, i.e. a different root/env-file shape). My own first-hand run raises RuntimeError. The gate outcome is identical either way (bare `except Exception` at boxes.py:186 -> `return not own` -> False), so nothing in the verdict turns on it -- but one of the two records is inaccurate as written.
KIDBRIEF  (mur-eg-31 EG.97 parent finding: the corrective reached the parent only, so the kid wrote code over a 0 cap) -- PARENT: dispatch your kid with --orders pointing at a file holding THIS WHOLE SECTION, and paste its FILE SCOPE + CEILING into the kid prompt; verify the kid's context carries the word CORRECTIVE before it starts.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_send_dm_read_and_nudge.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_send_dm_read_and_nudge.py · .agi/nodes/experiment/a00-1ac2dd28-c29fe1.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 007221c02 · <= 40 test lines net over 007221c02 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 007221c02 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.137: mur-eg-42 EG.120-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
