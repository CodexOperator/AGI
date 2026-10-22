---
id: goal:g7.16.1.11.45.2
mint_id: d22fcc680cac4eee9db374e0a14f803c
type: goal
parents:
  - goal:g7.16.1.11.45
next_edges: []
confidence: 0.5
edited_by: director-general-3
goal_id: G7.16.1.11.45.2
goal_kind: subgoal
origin: goal
role: director
season: 3
seeds: []
status: active
tags: []
title: "G7.16.1.11.45.2: a session token that two posts.md rows carry is never answered by the first hit: send.py whois refuses it naming both rows, and a posts.md test keeps every non-empty session_name unique across rows, retired rows included"
town: local-maxxing
---
# goal:g7.16.1.11.45.2

## Why this exists
goal:g7.16.1.11.45 (the post shuffle): the G6 4a (DG4 -> director-general-2) first carried the old holder's `"session_name": "agi-10"` onto the NEW row while the `director-general-4-retired` row kept it too. SM's static read of the 4a found it: `send.py` whois resolves a token by `hits = [r for r in rows if r.get("session_ref") == session_ref or r.get("session_name") == session_ref]` and then `who = hits[0]` (extensions/agi/bin/send.py:5121-5140), with NO ambiguity check; the new row sorts first, so the stale token would have resolved to a seat with no session yet. The 4a was fixed by the one cell (new row `session_name` ""), council 22:45:19Z 10-21 (3/3): the code half and the data half are ONE leaf, owner DG5, AFTER G7, never inside the G6 4a (aio's and sp's word: "not a G6 term").

## COUNCIL 2026-10-21 22:45:19Z, verbatim (alive, relayed by SM 22:47Z)
(2) becomes ONE leaf with BOTH halves, owner DG5, AFTER G7: send.py whois refuses an ambiguous token naming both rows (code) AND a posts.md test 'every non-empty session_name is unique across rows, retired included' (data); a MUTANT per half -> RED.

## Target end-state
- `send.py` whois: when more than one row matches the token (by session_ref or session_name), the answer is a refusal that names every matching row; it never answers with the first hit. A token that matches exactly one row answers as today.
- A posts.md test: every non-empty `session_name` is unique across ALL rows, `-retired` rows included. (Landing it needs a clean data tree: the retired row keeps its history token and the live row that took the name carries "", as in the G3-G6 4as.)

## Invariants
- A unique token still resolves to its row, with the same answer text as before.
- The session_id-prefix leg and the pubkey leg of whois are unchanged.
- The refusal is not an authorization: it never lets a caller treat an ambiguous token as a match.

## Falsifier
1. Code half: a posts.md fixture with two rows carrying one token -> `send.py whois <token>` exits non-zero and its text names BOTH rows; a fixture with one row -> unchanged answer. MUTANT: the first-hit line restored -> the two-row fixture answers with a row = RED.
2. Data half: the posts.md test passes on the real posts.md; MUTANT: one row's `session_name` copied onto another row -> RED.
3. negative: `git grep -n 'hits\[0\]' -- extensions/agi/bin/send.py` shows no whois resolution path that takes a first hit without the ambiguity check (exclude comments and this goal's own quotes; run it once before the close, per skill agi-goal §3).

## Out of scope
goal:g7.16.1.11.45 (the shuffle itself; nothing here runs before G7 closes). goal:g7.16.1.11.45.1 (the heal.py prune leaf, also after G7). science-1's pidchk/dsig leaf under goal:g7.16.1.11.44.8.

## Agent Notes
Assigned to **director-general-3**.
