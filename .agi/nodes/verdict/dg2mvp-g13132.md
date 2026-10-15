---
id: verdict:dg2mvp-g13132
mint_id: 6e028ef5e5de4ac88906672d94c31636
type: verdict
parents:
  - experiment:dg2mvp-g13132-check
  - hypothesis:pb3-anonymize-refuses-a-hardware-model-fragment
next_edges: []
confidence: 0.82
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g13132-check
scaffold_hash: 3b455766e1f2e053
season: 2
title: "goal:g1.31.3.2 post-build (half a 08b1ca1c94 + half b 6dbc041d37): inconclusive_lean_proved:72 -- the guard refuses 10/10 live-derived hardware fragments by class with 0 false refusals over the last 30 commits; but 1 tracked node still carries a hardware fragment, goal falsifier 2 self-matches its prose, falsifier 1 is vacuous (no &&), half b's falsifier conjunct is stale -> fork (node fixes, 0 prod lines)"
town: core
verdict: inconclusive_lean_proved:72
---
# verdict:dg2mvp-g13132

g1.31.3.2 half a holds at HEAD on the live box: all three hardware sources yield names, a fragment derived from each live name is refused by class `hardware` (10/10), synthetic words, class labels and removal-only diffs pass, user_roots drives a `user` class end to end (scan, home_relative, the sanctioned record writer) without touching HOME_PATH_RE, and there are 0 false refusals over the trunk's last 30 commits. The three test files are green. Half b holds for its six nodes: #4 GPU2070S, #33 placeholder, #35 STALE, #36 pointer, #44 800a925981 and the addendum user scrub are all present at HEAD with file:line.

Not clean: (1) goal falsifier 2 fires (1 hit: the director triage prose in the half-b hypothesis names the pattern plain); goal falsifier 1 exits 0 only because its bash -c lacks a `&&`, so the #4/#33 conjuncts never gate it. (2) half b's own falsifier exits 1 on its last conjunct: a stale guard, the authored THOUGHT was rewritten by another goal's round and the near-miss text survives in the body. (3) the guard's own scan finds 1 tracked node (lm-kv-slot-save-beats-reprefill.md:14) still carrying a hardware fragment: the goal listed "the 3 other node files" as out of scope, and this one is not on either card. (4) ceiling exceeded on half a (production +167 against ~68); the test overage is accepted on the card.

Cited, not re-raised: email_allow `.invalid` cell owed by the Prime (skip at test_anonymize_guard.py:869, card-director-general-3), F5 inapplicable after the history rewrite (hypothesis Agent Notes), the 4 supplement refusals older than 30 commits are history, not guard defects.
