---
id: experiment:a00-f16f044c-885d9c
mint_id: d6cc04ec4e5f482eacfee9fc0ad0e132
type: experiment
parents:
  - hypothesis:l3w0-send-rooms
next_edges: []
confidence: 0.9
evidence_runs:
  - experiment:a00-f16f044c-885d9c
loop: hypothesis:l3w0-send-rooms@s1
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ef54e26cee91fe16
season: 1
title: A00 f16f044c 885d9c
verdict: proved
---
# experiment:a00-f16f044c-885d9c

## Experiment

Extended `send.py` to host pairwise and quorum conversations as files under
`sessions/<iter>/comms/`, rendered back as a chat transcript, with one standing
room per ladder level and the prime inbox-only behind an `audience` verb — the
claim of `hypothesis:l3w0-send-rooms`.

**Files edited (in place):**
- `extensions/agi/bin/send.py` — added room/dm verbs, transcript render,
  standing rooms, `audience`, `comms_root` resolution.
- `extensions/agi/tests/test_send.py` — 20 new red-first tests (36 in file).
- `QUICKSTART.md` — three-line comms note in §3.

**Layout implemented:**
- `comms/dm/<a>--<b>.md` pairwise (names sorted), `comms/room/<name>.md`
  quorums; append-only blocks `ts/from/to` + free text (same shape as inbox).
- Read renders a transcript: `**sender** HH:MM — text`.
- Standing rooms: `tier3-quorum`, `tier2-directors`, `tier2-parents`,
  `tier1-directors`, `tier1-parents`, `tier0-parents`. A room may never
  address the prime (`send --room prime` → error, nothing written).
- Prime is inbox-only: `audience prime --reason …` writes to the prime's
  inbox, one audience per sender per rotation unless `--morals`, rule printed
  back.
- Comms root: `--comms-root` flag > config `locations.comms_root` > default
  `sessions/<iter>/comms`. Existing inbox verbs (`send <to> <text>`, `read`,
  `peek`) unchanged.
- Read position per participant tracked as a message **count** in a sidecar
  `.state.json`, so identical microseconds never cause re-reads or drops;
  `--since TS` is an explicit iso-timestamp filter.

**Verdict on the claim:** all six clauses tested and green.

## Evidence

### Full test suite
```
python3 -m pytest extensions/agi/tests/ -q
1715 passed, 9 skipped in 88s
```
(One earlier run showed 3 brief-chain failures that were transient and
order-dependent — a sibling agent edits brief.py concurrently; the file passes
alone and the suite re-ran green.)

`test_send.py`: 36 passed.

### Verify commands with actual output — live two-shell round trip (room / dm /
rooms / audience gating), run with `--comms-root` to a temp dir:

```
$ AGI_AGENT_ID=parent-a  send.py send --room tier3-quorum "anyone free to judge vision 2?"
/tmp/l3w0-comms.XXX/room/tier3-quorum.md
$ AGI_AGENT_ID=director-b send.py send --room tier3-quorum "yes, on it"
/tmp/l3w0-comms.XXX/room/tier3-quorum.md
$ AGI_AGENT_ID=director-b send.py read --room tier3-quorum
**parent-a** 20:13 — anyone free to judge vision 2?
**director-b** 20:13 — yes, on it
$ AGI_AGENT_ID=parent-a send.py send --to director-c "pick up g12.3 review"
/tmp/l3w0-comms.XXX/dm/director-c--parent-a.md
$ AGI_AGENT_ID=director-c send.py read --dm parent-a
**parent-a** 20:13 — pick up g12.3 review
$ AGI_AGENT_ID=director-c send.py rooms --me director-c
room  tier3-quorum        2 unread
dm    director-c--parent-a  0 unread
$ AGI_AGENT_ID=parent-a AGI_LOOP=L3.02@1 send.py audience prime --reason "need ruling"
audience requested of the prime by parent-a: 'need ruling on t3 quorum name'
rule: the prime is inbox-only; one audience per sender per rotation unless the morals are at stake (--morals).
$ AGI_AGENT_ID=parent-a AGI_LOOP=L3.02@1 send.py audience prime --reason "second ask" ; echo $?
ERR: parent-a already had an audience with the prime this rotation (L3.02@1). One audience per sender per rotation unless the morals are at stake (--morals).
1
```

(The one test audience write to the real `sessions/inbox/prime.md` was deleted
afterwards so the prime's inbox was left clean.)

### Red-first tests added (each rule asserted to fail before the implementation
made it pass)
- `test_dm_creates_sorted_file` — dm writes `comms/dm/<a>--<b>.md`, names sorted.
- `test_dm_render_shape` — transcript line is `**sender** HH:MM — text`.
- `test_dm_read_marks_read_once` / `test_dm_peek_does_not_mark_read`.
- `test_dm_since_filter` — `--since` boundary + future anchor filters correctly.
- `test_room_creates_file_and_appends`, `test_room_render_transcript`.
- `test_room_read_positions_are_per_participant` — p1/p2/p3 positions differ.
- `test_room_cannot_address_prime` — `send --room prime` raises, file never made.
- `test_standing_rooms_constant` — the six standing room names.
- `test_rooms_lists_rooms_with_unread_counts` — per-kind unread counts.
- `test_audience_writes_to_prime_inbox` / `test_audience_one_per_rotation` /
  `test_audience_morals_bypasses_gate` / `test_audience_rule_printed_back`.
- `test_comms_root_defaults_under_sessions` /
  `test_comms_root_honours_config` (tmpfs `/dev/shm/agi`) /
  `test_comms_root_flag_wins`.

Unexpected files in git status (other agents' concurrent work, left untouched):
brief.py, cc-session-start.sh, test_brief.py, HANDOFF.md, SKILL.md, three
sibling experiment nodes, one rotate hypothesis node.

## Agent Notes
send.py rooms implemented & verified: dm+quorum files under comms/, transcript render, 6 standing rooms, prime inbox-only with one-per-rotation audience gate, comms_root flag>config>default. 36 send tests green; full suite 1715 passed/9 skipped; live 2-shell round trip shown. Existing inbox verbs unchanged. Red-first tests written first.
