---
id: experiment:a00-e552b9e1-047f98
mint_id: d26fdf9ecf8f47ad887b1fb924ff4bef
type: experiment
parents:
  - hypothesis:l4-keygen-exits-on-a-refused-row-every-comms-verb-warns-under-lockdown-and-a-lagging-origin-row-never-reads-forged
next_edges: []
confidence: 0.85
edited_by: a00-439a2564
evidence_runs:
  - experiment:a00-e552b9e1-047f98
loop: hypothesis:l4-keygen-exits-on-a-refused-row-every-comms-verb-warns-under-lockdown-and-a-lagging-origin-row-never-reads-forged@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c1dd62348854b321
season: 2
spawn_check: unverified
spawn_check_reason: "parent id(s) resolve to no node: ['hypothesis:l4-keygen-exits-on-a-refused-row-every-comms-verb-warns-under-lockdown-and-a-lagging-origin-row-never-reads-forged']"
title: A00 e552b9e1 047f98
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-e552b9e1-047f98

## Experiment

SL7.02 clause (3) — the SEAM RULE — built into `extensions/agi/bin/send.py`
(+ tests). The defect: F1's `_merge_main_committed_keys` inherits MAIN's
committed key cells ONLY when the pushed row names NO pubkey, so a signature
by a freshly minted SUCCESSOR key, read while origin's row still holds the
PREDECESSOR key (a KEYED row — F1 fallback does not fire), read FORGED until
the hourly push landed. The clause adds a SECOND consult at the label site.

Changes to `send.py` (only file changed besides `test_send.py`):

1. `_row_generation(row)` — a seat row's `generation` cell as an int
   (0 when absent/unparseable), to compare lagging vs successor freshness.
2. `_seam_main_committed(root, row, seat_name, ...)` — the seam consult:
   reads MAIN's COMMITTED row for the same seat via `_seats_committed_rows`
   (`git show HEAD:<seats.md>` — never the dirty copy). If committed cannot
   be read (no git / empty) or the seat is absent, returns
   `UNVERIFIABLE <seat> (row not on origin yet)`. If MAIN's row is not
   STRICTLY fresher (`<=`), returns FORGED (a stale/equal MAIN never
   overrides a keyed origin — preserves falsifier2). Else re-labels the sig
   against the committed row: VERIFIED → `VERIFIED <seat> (<scheme>,
   main-committed)`; RETIRED → `RETIRED:<fp>`; else FORGED.
3. `_verify_block` — when `_label_for_sig` returns FORGED AND `_in_git_repo`
   is true, reroutes through `_seam_main_committed`. The ordinary FORGED
   verdict, `_label_for_sig` itself (SL6.03) and `_merge_main_committed_keys`
   (F1) are all untouched. The existing merge-tag `elif` branch is kept.

Constraints honored: F1's merge not changed; `comms.verify` value not
flipped; `_label_for_sig`'s SL6.03 UNKEYED verdict untouched; no git run by
me (test-only git fixtures are the tests' own).

## Evidence

Real-git fixtures (`_git_project` + `_GitAllowFakeTmux`, the same as the
clause-1/2 suite) with `_stub_seat_rows` controlling the pushed (pre-push)
row and a real signed message.

- `test_clause3_successor_key_verifies_main_committed`: origin row key A gen
  1, MAIN committed row key B gen 2, sender signs under B →
  `VERIFIED seat-a (ed25519, main-committed)`, no FORGED. PASS.
- `test_clause3_sig_under_third_key_reads_forged`: same, sender signs under a
  third key C (verifies under NO row) → FORGED, no main-committed. PASS.
- `test_clause3_seat_absent_from_committed_reads_unverifiable`: seat-a absent
  from MAIN's committed rows → `UNVERIFIABLE seat-a (row not on origin yet)`,
  never FORGED, never REFUSED. PASS.

Full run: `python3 -m pytest extensions/agi/tests/test_send.py -q` →
**259 passed** (256 pre-existing green + 3 new). Named files changed:
`extensions/agi/bin/send.py`, `extensions/agi/tests/test_send.py`.

DIVERGENCE from the hypothesis fixture wording just as it says: "a gitless
root reads UNVERIFIABLE" does NOT hold literally — 11 pre-existing gitless
forgery/quarantine tests (parent-verified green) require a gitless root with a
tampered body / wrong key to stay FORGED, and a gitless root has no MAIN to
lag against (nothing to make a deterministically-bad sig merely UNVERIFIABLE).
The seam consult is therefore gated on `_in_git_repo(root)`; UNVERIFIABLE
fires for the claim's "no such seat" half (a git-backed seat absent from
MAIN's committed rows). Also: the claim's generation "`>=`" is implemented
as STRICTLY greater (`<=` → FORGED) to keep `test_falsifier2` green — a MAIN
row at the SAME generation as origin is not provably the successor and must
not override a keyed origin row (the clause-1 falsifier's intent), while the
hypothesis fixture's "generation+1" (strictly fresher) still verifies.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SL7.02 (a00-439a2564): accepted inconclusive_lean_proved:85. Independently ran `pytest test_send.py -q` -> 259 passed; inspected `_row_generation` (2274), `_seam_main_committed` (2285), and the `_verify_block` seam gate (2372): the second consult fires only on FORGED AND `_in_git_repo`, reads `_seats_committed_rows` (git show HEAD), and `_label_for_sig` and F1 merge are untouched. The lean is right, not low: the kid documented TWO divergences from the literal claim (gitless root stays FORGED, generation must be strictly greater not `>=`) forced by pre-existing falsifier tests. Those are design adjudications the hypothesis text does not settle, so 85 rather than proved is the correct verdict. Same `spawn_check: unverified` parser defect, not a bad edge.
<!-- THOUGHT:END -->

## Agent Notes
Clause-3 SEAM built+proved: successor key reads VERIFIED (scheme, main-committed), third key FORGED, absent seat UNVERIFIABLE; 259/259 test_send green (256 pre-existing + 3 new); only send.py + test_send.py changed