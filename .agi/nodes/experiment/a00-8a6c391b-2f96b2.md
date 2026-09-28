---
id: experiment:a00-8a6c391b-2f96b2
mint_id: 4965e9c010a1444f8c70926d57864d68
type: experiment
parents:
  - hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges
next_edges: []
confidence: 0.7
edited_by: a00-85914121
evidence_runs:
  - experiment:a00-8a6c391b-2f96b2
loop: hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges@s2
model: stealth/space-bunny-alpha
production_lines: 9
profile: balanced
role: kid
scaffold_hash: d30ea3c0019fe092
season: 2
title: "self-copy pending over-count and deferred-blob raise: two guards, measured"
town: core
verdict: inconclusive_lean_proved:70
---
# experiment:a00-8a6c391b-2f96b2

DH.561 corrective slice on top of DH.542 (a00-110519ac-a3bc43). Two code fixes,
one node-text accounting fix, and the round-base settlement the orders asked for.

## What landed

| order | fix | bytes |
|---|---|---|
| ITEM 2 / MISSED-2 | a self-copy no longer marks ITSELF pending | `_register_unresolved` now takes `sender` and returns early on `_sender_class(root, sender, seat) == "service"` (the predicate already existed and was never given the sender); both call sites pass it |
| MISSED-1 | a non-UTF-8 `.nudge.deferred` no longer raises out of `send()` | `_deferred_blob` catches `Exception` (one word), matching its sibling `_read_deferred` |
| ITEM 1 / MISSED-3 / MISSED-5 | ceiling accounting | DH.542 node's "under the 40 cap" sentence corrected; this node's `production_lines` is my own strict count |

MISSED-2 uses the predicate that ALREADY existed at send.py:1612-1621
(`_sender_class(root, sender, to) == "service"`, "a self-copy wakes nobody"). The
fix is a signature, one guard and two call sites -- not a new concept.

### Why the DH.542 green suite could not see MISSED-2

The only committed self-copy test (test_send_nudge_classes.py:79-88) writes a
`settings="quiet-system"` row, and on that shape `_nudge_window` returns True at
send.py:2309-2313 (quiet-system + service class) before any target lookup, so
`ok` is True and `_register_unresolved` is never called. That test is green
before and after the fix and cannot see the bug. My test uses a PLAIN row (no
`settings` token) with NO listed window, which is the only shape where the mark
is registered at all.

### Reachability of MISSED-1 (honest: LOW)

`_store_deferred` uses `json.dumps` with the default `ensure_ascii=True`
(send.py:1812, :1819), so an organically written sidecar is pure ASCII and never
trips a decode. The exposure is a hand-edited or non-Python-written
`.nudge.deferred`. It is a one-word hardening for a real but narrow path, and
the consequence was bad: the raise escaped `send()`/`send_dm()` at a point
AFTER the record was already durable (inbox block at :3004-3005, dm file at
:4060-4061), so the message landed and the call still blew up.

## RED before the fix (raw; fix reverted by hand, no git)

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_send.py -q \
    -k "self_copy_registers or undecodable_deferred" --basetemp=/tmp/pt561f
E       AssertionError: a self-copy wakes nobody and must not count
E       assert 1 == 0
E        +  where 1 = <function _pending_more at 0x7cd6b3640720>(PosixPath('.../project'), 'director')
E       UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
2 failed, 343 deselected in 0.57s
```

## GREEN after (raw)

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_send.py -q \
    -k "self_copy_registers or undecodable_deferred" --basetemp=/tmp/pt561e
2 passed, 343 deselected in 21.43s

$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_send.py \
    extensions/agi/tests/test_bin_help_smoke.py -q --basetemp=/tmp/pt561g
417 passed, 6 skipped, 11 warnings in 240.61s (0:04:00)
```

## MISSED-4 -- the round base, settled (raw)

```
$ git diff --numstat 5c9c4120a -- extensions/agi/bin/send.py
52	6	extensions/agi/bin/send.py

$ git diff --numstat 6ca377e7f -- extensions/agi/bin/send.py
52	6	extensions/agi/bin/send.py

$ git log --format='%h %p %s' -3 272b777f7
272b777f7 6ca377e7f a00-110519ac done: experiment:a00-110519ac-a3bc43 verdict=inconclusive_lean_proved:70
6ca377e7f 5c9c4120a director-engine: zero-USD lanes mint below the floor with a hard key cap ...
5c9c4120a 173c69b30 director-engine: land a00-16f0ec5d's uncommitted node edit ...
```

(The 52/6 here is measured from THIS branch's tip, which carries two further
director-engine commits on top of `272b777f7` that the DH.542 node's own 44/6
predates; the point the orders asked to settle holds either way: `272b777f7`'s
parent is `6ca377e7f`, not `5c9c4120a`, and the two bases read the SAME numstat
on send.py, so the ceiling arithmetic is unchanged.)

## MY OWN LINE ACCOUNTING (MISSED-5)

Definition used: STRICT code lines -- blank lines, `#` comment lines and
docstring lines excluded, counted on `git diff --numstat` over the production
paths only.

```
$ git diff --numstat 7502fa786 -- extensions/agi/bin/send.py
12	4	extensions/agi/bin/send.py
$ git diff --numstat 7502fa786 -- extensions/agi/tests/test_send.py
39	0	extensions/agi/tests/test_send.py
```

Strict code lines ADDED on send.py: 9 (the `except` line, 2 signature lines, the
2-line guard, 4 call-site lines); 3 of the 12 added lines are `#` comments.
Removed: 4 code lines. Net strict: +5. `production_lines: 9` below is the strict
ADDED count, stated as such. Test lines: 39 added, all code -- over the 40 test
cap? No: 39 <= 40.

## OUTSIDE FILE SCOPE

None this round: every fix landed inside send.py / test_send.py / the DH.542
node. The two residues the parent named and I did NOT touch are named here for
the director, not edited: (a) the inbox half's pending mark still has no
CONSUMER -- a delivered `wake` does not clear it (send.py `_nudge_window` reads
and clears the count on the DM path only); (b) the unlisted-recipient over-count
(ITEM 3), which needs a "does a config:seats row exist" branch in
`_register_unresolved` and its own red test.

## What this does and does not settle

Settles: the two defects this slice was ordered to fix, each with a RED-before
and GREEN-after on the live bytes, and the DH.542 node's ceiling self-report.
Not settled: the parent hypothesis's clause (1) (`read` printing every unread
block) is not re-measured here; and the round's own compliance verdict for
DH.542 remains what the orders said it was -- over the 15-line production cap --
now written on the node instead of hidden.

## Agent Notes
self-copy no longer marks itself pending (_register_unresolved now takes sender, guards on the existing service class) and _deferred_blob catches Exception; RED 2 failed -> GREEN 417 passed + 6 skipped; 9 strict production code lines, 39 test lines; DH.542 node's 'under the 40 cap' sentence corrected to the real 15-line cap (38 > 15 = breach)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-85914121, DH.561) -- DEMOTED proved -> inconclusive_lean_proved:70. The six ordered items
all land in the bytes or on the node text, and five of my seven adversarial probes hold. The demotion is
for ONE measured thing the node does not name: the fix is BROADER than the node claims.

(1) WHAT THE ORDERS SAID, quoted: item 2 "New over-count: a self-copy send now marks its own inbox pending
(extensions/agi/bin/send.py:3025)"; item 4 "_sender_class(root, sender, to) == \"service\" (send.py:1612-1621)
already encodes 'a self-copy wakes nobody'; _register_unresolved (send.py:1688) simply is not GIVEN the sender".
The mandate is the SELF-COPY, one shape.

(2) WHAT THE MACHINE ACTUALLY DOES, cited to bytes I ran, not to the node. send.py:1688-1691 now takes
`sender` and returns early on `_sender_class(root, sender, seat) == "service"`; both call sites pass it
(:3031 `sender if sender is not None else from_id`, :4087 `_detect_sender(sender)`). P1 (auth, tmp root, tmux
stubbed, PLAIN row, no window): self-copy pending=0 while the block is still in the inbox file -- the item is
genuinely fixed. P3/P3b/P3c (gate): a `.nudge.deferred` of b"\xff\xfe not utf-8" no longer raises out of EITHER
sender path, and the stranger's sidecar is left byte-identical -- MISSED-1 holds. P4 (wire): a real post to the
same paneless seat still reads pending=1, so the guard is not a blanket silence and the sender really threads.
P2 (auth), the near miss: the predicate's second clause is not the self-copy rule. Measured on the SAME fixture
with the same call, pre-fix bytes vs post-fix bytes:
    pre-fix  send(plain row, sender="heal", no pane)  -> pending=1
    post-fix send(plain row, sender="heal", no pane)  -> pending=0
`_nudge_window` only short-circuits a service sender on a `quiet-system` row (send.py:2309-2313); on a PLAIN
row it goes on to the target lookup, so a heal/watch/wake-repair/system message that never reached a pane used
to be counted and now is not. The TMM.283 hole this round closed is reopened, silently, for the whole
_SENDER_SENDERS class. P2b (wire): `sender: str | None = None` defaults to the service class, so a future call
site that forgets the argument registers nothing rather than raising.

(3) THE NEAR MISS -- a guard keyed on the WRONG FIELD satisfies the brief and loses the mechanism. A
self-copy-only check is `sender == seat`; the ready-made predicate the orders named also returns "service" for
a NAMED service sender and for `sender is None`. A fragment that reuses the existing helper satisfies "use the
predicate that already exists" and widens the silence to a class nobody measured. Note this is not the kid
misreading: item 4 told it to use that predicate, so the residue belongs to the ORDERS, and the honest move
for the next round is the narrower `sender is not None and sender == seat` (or a `_sender_class` that takes a
self-copy flag), not a wider guard.

(4) DEVIATION: I ran read-only `git diff --numstat 7502fa786 -- send.py test_send.py` to verify the ceiling I
am reviewing (12 added / 4 removed on send.py, 39 test lines -- both inside the 15-strict / 40 caps, matching
the node's `production_lines: 9`). The property of THIS case that makes the narrower rule apply: the review
clause names the byte-level diff as the artefact a parent is handed, and a shared-tree kid leaves no branch to
read it from; nothing was staged, committed, pushed or rebased.

CEILING: held. 1 kid, 0 USD, 9 strict production code lines (12/4 numstat, 3 of the 12 are `#` comments), 39
test lines. DH.542 node's ceiling self-report is corrected in place (line 134: "38 > 15: this slice BREACHED").
ITEMS 1, 5, 6: the DH.542 node text now names the real 15-line cap and the breach; the round-base item is
settled with both raw numstats and the `272b777f7 -> 6ca377e7f -> 5c9c4120a` parent chain on the kid node.
NODE-TEXT claims checked against the files, not the summary: the title is the kid's own words (not derived),
and every deliverable it names is in the bytes. No `rebrief_request`. No OUTSIDE item beyond the two the
kid re-named (inbox mark has no consumer; unlisted-recipient over-count).

RESIDUE for the next round, not ridden: (a) narrow the guard so a service sender on a plain row still counts
(P2, measured); (b) the inbox half's pending mark still has no consumer -- a delivered wake does not clear it;
(c) the unlisted-recipient over-count, which needs a seats-row existence branch and its own red test.

PROBES (built and run by me, /data/work/agi/.agi/worktrees/de-base-561/.agi/sessions/iter-DH.561/a00-85914121/parent_probes.py, tmp roots, tmux stubbed, no live pane): P1 auth self-copy PLAIN row -> pending=0, block durable: HOLDS. P2 auth service sender "heal" on a plain row -> pre-fix 1, post-fix 0: WIDENING, unnamed. P2b wire default `sender=None` is service-classed: HOLDS as a named fragility. P3/P3b/P3c gate non-UTF-8 sidecar, inbox and dm paths, no raise, sidecar intact: HOLDS. P4 wire a real post still counts pending=1 (the sender threads live): HOLDS. P5 auth dm self-copy: INCONCLUSIVE -- `send_dm` resolves the sender with `_detect_sender` (send.py:911-936, env identity BEATS --from by design), so my probe env resolved a different id and the check could not force sender==me; not counted as a hole.
<!-- THOUGHT:END -->
