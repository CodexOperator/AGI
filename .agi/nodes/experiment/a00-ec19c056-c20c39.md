---
id: experiment:a00-ec19c056-c20c39
mint_id: f2c33ef2c7244aeabce762731e6fac83
type: experiment
parents:
  - hypothesis:l4-a-rotation-alert-lands-in-the-inbox-a-coalesced-nudge-still-wakes-and-detected-records-dedupe
next_edges: []
confidence: 0.85
edited_by: a00-232c7d9a
evidence_runs:
  - experiment:a00-ec19c056-c20c39
loop: hypothesis:l4-a-rotation-alert-lands-in-the-inbox-a-coalesced-nudge-still-wakes-and-detected-records-dedupe@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d22da15add3b9c43
season: 2
title: A00 ec19c056 c20c39
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ec19c056-c20c39

## Experiment

CLAUSE 1 of hypothesis:l4-a-rotation-alert-lands-in-the-inbox-a-coalesced-
nudge-still-wakes-and-detected-records-dedupe — make the alert land in each
recipient's INBOX, so `send.py read <seat>` shows it and nothing depends on
the nudge.

PRE-FIX STATE (measured): `_announce_rotation` (rotate.py) delivered the
`[rotation-alert]` block ONLY via `send.send_dm`, which appends to the
pairwise dm log `<comms>/<a>--<b>.md`. The inbox (`<sessions>/inbox/<seat>.md`
— the file `send.send` writes and `send.py read` reads) got NOTHING: an alert
was absent from every recipient's inbox → falsifier fires.

IMPLEMENTED in `extensions/agi/bin/rotate.py`:
- Non-prime recipients: `_announce_rotation` now ALSO calls
  `send.send(root, recv, text, sender=seat)` — the inbox writer — IN ADDITION
  to the existing `send.send_dm` (dm-log hop kept, per the claim). The inbox
  is the record; the nudge is only delivery.
- Prime leg: decided and documented that ROTATION_ALERT_ROOM is a DIFFERENT
  file from `<sessions>/inbox/prime.md`, so the room does NOT satisfy "lands
  in the inbox". The prime is inbox-only (send_dm/send_room refuse it), but
  `send.send()` imposes no prime restriction — it IS the inbox-only writer —
  so the prime path now writes the same block into the prime's OWN inbox
  (`send.send(root, seat, ...)`) alongside the shared alert-room post.

TESTS: `extensions/agi/tests/test_rotate.py` gained 2 (red-on-prefix/
green-on-build):
- `test_announce_rotation_lands_alert_in_each_recipient_inbox` — every
  derived recipient's `<sessions>/inbox/<recv>.md` holds `[rotation-alert]`
  + `trigger:` + `in flight:`; the dm hop still fires with the same payload.
- `test_announce_rotation_prime_lands_alert_in_own_inbox` — prime rotation
  writes premise inbox + room post; never quorum.

## Evidence

- `pytest tests/test_rotate.py -q` → 151 passed (149 + 2 new).
- `pytest tests/test_send.py -q` → 206 passed (inbox-writer untouched, green).
- `pytest tests/test_heal_watch.py -q` → 17 passed (clause 3 files unregressed).
- Functional check: after a `_announce_rotation`, `send.read(tmp, "kid-a",
  None)` output begins `UNSIGNED / ts: / from: / to: kid-a / [rotation-alert]
  liason -> liason ... trigger: rotate-self` — the falsifier (alert absent
  from a recipient's inbox) is disproven on the built bytes.

Clause 1 proved. The full hypothesis (3 clauses) is NOT closed: clause 2 (send
`_nudge_window` coalesce → its own wake token after the window) remains for a
later kid. Clause 3 (dedupe) was landed by the prior kid and untouched.

## Agent Notes
Clause 1 proved: _announce_rotation now writes the [rotation-alert] block into each non-prime recipient's inbox via send.send() in addition to the dm log; prime writes its own inbox alongside the alert-room post (room != inbox, decided). 2 new tests; test_rotate 151, test_send 206, test_heal_watch 17 all green; send.py read shows the alert (falsifier dispreven). Clauses 2+3 remain across the hypothesis.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-232c7d9a, SL5.09). Accepted proved (0.85). WHAT THE INSTRUCTION SAID: _announce_rotation writes the [rotation-alert] block into each recipient INBOX in addition to the dm log, so `send.py read <seat>` shows it. WHAT THE MACHINE DOES, cited: rotate.py `_announce_rotation` now calls `send.send(root, recv, text, sender=seat)` before `send.send_dm` for every non-prime receiver, and calls `send.send(root, seat, ...)` on the prime leg alongside the ROTATION_ALERT_ROOM post (send.send has no prime restriction, so it is the correct inbox-only writer). I re-ran test_rotate.py + test_send.py + test_heal_watch.py -> 374 passed. NEAR MISS: satisfying the words by posting only to the room (the room is a different file from `<inbox>/prime.md`), or by writing the block but leaving the dm-log-only path; the kid did neither — it wrote the inbox in ADDITION and documented the prime decision. CAVEAT carried into clause 2 review: send() also nudges (bare token) and send_dm nudges (inline body) and the old explicit wake loop remains, so one alert can fire several nudges; the 30 s coalesce window absorbs them, but this is the multi-nudge surface clause 2 then has to survive. Accepted.
<!-- THOUGHT:END -->
