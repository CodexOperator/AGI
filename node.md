---
id: hypothesis:l3w0-send-rooms
mint_id: fd8e0884c51d43b380b72a5ca03144b5
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: ubuntu
scaffold_hash: cd485f6cb75fd5dd
season: 1
testable_claim: send.py hosts pairwise and quorum conversations as files under the iteration's sessions/<iter>/comms/ directory, renders them back as a chat transcript, keeps one standing room per ladder level for free horizontal comms, and makes the prime director inbox-only with an audience verb
title: L3w0 send rooms
---
# hypothesis:l3w0-send-rooms

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILES: extensions/agi/bin/send.py, tests, QUICKSTART.md (three lines). LAYOUT: sessions/<iter>/comms/dm/<a>--<b>.md for pairwise (names sorted), sessions/<iter>/comms/room/<name>.md for quorums; append-only blocks with ts, from, text as the inbox uses today. VERBS: send --to X TEXT (dm), send --room R TEXT, read --room R [--since TS] and read --dm X, peek likewise, rooms (list rooms with unread counts), audience prime --reason TEXT (the only way to reach the prime: writes to the prime's inbox with the reason, one audience per sender per rotation unless --morals is given, and the rule is printed back). RENDER: reading prints a transcript, one message per paragraph: bold sender, time, dash, text, so a model reads it like a chat channel. STANDING ROOMS: create on first use, names tier3-quorum, tier2-directors, tier2-parents, tier1-directors, tier1-parents, tier0-parents; a room may not address the prime. LOCATION: comms root defaults to sessions/<iter>/comms and honours locations.comms_root in config so a project may point it at tmpfs; default stays on disk (owner decision: provenance). Do not change the existing inbox verbs. VERIFY: red-first tests for dm, room, render shape, rooms listing, audience gating; a live round trip on this repo between two shells. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Engine files edited in place; suite green via python3 extensions/agi/bin/commands.py run tests; every new rule gets a test that was red first. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them. Design source: .agi/context/l3-command-ladder-brief.md
