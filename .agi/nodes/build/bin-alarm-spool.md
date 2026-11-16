---
id: build:bin-alarm-spool
mint_id: 3e003e6dbca74f82bc2526c25879a5a5
type: build
parents:
  - goal:g7.16.1.11.20.2.1
  - mvp:unified-spawn-path
next_edges: []
build_kind: code
confidence: 0.8
link_ref: extensions/agi/bin/alarm_spool.py
location: source_root
model: claude-sonnet-5-5
origin: build-version
payload_ref: extensions/agi/bin/alarm_spool.py
role: director
scaffold_hash: 37dc196ae6b424e3
season: 3
status: active
tags:
  - build
  - code
  - alarm
  - spool
title: "alarm_spool.py -- one spool per sending seat: append a JSON line, drain signed as the seat, a 16-hex alarm id, a bounded could-not-read HOLD"
town: local-maxxing
---

# build:bin-alarm-spool


`extensions/agi/bin/alarm_spool.py` -- ONE SPOOL PER SENDING SEAT: every alarm is a signed box message, and only the seat signs it. `append` writes a plain JSON line `{id, job, to, text, ts}` to this uid's `~/alarm.spool` (a 16-hex id, `token_hex(8)`; bounded by `--max-lines`); `drain` runs in the sending seat's own uid and mails each line through the box tool with the trailers `Alarm-job:` and `Alarm-id:`. L595 (goal:g7.16.1.11.20.2.1) added the 16-hex id, the one skip line, a three-valued `already_sent`, and a could-not-read HOLD bounded by `rec['holds']` / `--max-holds`, reset on a good read, with an `[alarm-unverified]` tag. Its test file is `extensions/agi/tests/test_alarm_spool.py`.

LIVE (belam [done] 21:13:24Z 11-16, via SM): `/opt/agi/bin/alarm_spool.py` installed as root from ee1e7c9e9a and read back, sha256 44e0118d027e (== L595), line 68 mints `token_hex(8)`; the seat drain crons run MAIN's copy, already L595's bytes at the land. NOT SEEN: a real alarm through the installed copy.
