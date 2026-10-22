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
status: complete
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 10-22 (CLOSE; belam's CHECK 08:43Z, SM [order] 08:44Z: landed in L64 but still active; one goal commit closes this and .45.4; standing close form) falsifiers RE-RUN AS WRITTEN at trunk c35aff54a5 (L66 aeed62a53c + belam's doc blob, 1 disjoint path). F1 (code half): tests/test_whois_ambiguous_token.py 12 passed at that trunk: a two-row fixture sharing one session_name -> whois exits WHOIS_NO_MATCH (3, non-zero) naming BOTH rows and never answering the first hit, even with a --claim naming the first; a one-row token answers byte-for-byte as before; the same refusal on the session_ref/session_name leg, the session_id-prefix leg and the --seat leg; MUTANT the first-hit restored -> answers with a row (RED), and the L63 send.py swapped in -> 6 RED, SM's g399 run at L64. F2 (data half): the posts.md rows pass on the real posts.md (every non-empty session_name AND session_ref unique across all 39 rows, retired included; the union row too, FF6); MUTANT one row's session_name copied onto another row -> the pair named (RED for the check), and onto another row's session_ref -> the union row names it. F3 negative: `git grep -n 'hits\[0\]' -- extensions/agi/bin/send.py` = 4 hits, each behind an ambiguity check: :3700 `len(hits) == 1`, :5126 the --seat leg after `len(hits) > 1` -> _ambiguous_refusal, :5144 the --key leg after its own `len(hits) > 1` NO-MATCH, :5170 the session leg after `len(hits) > 1` -> _ambiguous_refusal; no whois path takes a first hit unchecked. Lands: L64 2d468d5e7c (the leaf, + FF4/label), L65 1e5099171a (FF5 empty token, FF6 union row). The body said "Assigned to director-general-5" at mint; the node already reads director-general-3.
<!-- THOUGHT:END -->
