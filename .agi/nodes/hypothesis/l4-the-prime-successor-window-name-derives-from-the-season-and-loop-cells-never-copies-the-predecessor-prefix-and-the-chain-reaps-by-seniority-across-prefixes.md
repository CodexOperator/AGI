---
id: hypothesis:l4-the-prime-successor-window-name-derives-from-the-season-and-loop-cells-never-copies-the-predecessor-prefix-and-the-chain-reaps-by-seniority-across-prefixes
mint_id: 8baaa7dc7fd84d6daeac36edfbf0f7a4
type: hypothesis
parents:
  - goal:g6.11
next_edges: []
edited_by: belam
scaffold_hash: cca9f88ed25e3617
season: 2
testable_claim: "rotate.py step 3 (spawn) names the Prime successor belam-S<season>-L<loop>-<numeral> from the live cells (config:ladder season; the live loop id from the ladder/plan cell), the numeral restarting at I when the S/L token changes and continuing (+1, _split_roman_suffix) when it does not; it never copies the predecessor window prefix. The after_join belam-chain grep in config:rotations matches the pattern belam-S[0-9]+-L[0-9]+ and the tests that pin the literal belam-S1 assert the pattern; the five-window chain reap orders windows by seniority (numeral, then age) ACROSS prefixes so a token change never splits the chain or reaps the wrong window. Measured: gen 31 seated 05:26Z 09-18 as belam-S1-L4-XXXI while the ladder reads season 2 and L5 closed. Falsifier: a successor spawned under season 2 / loop 5 carries S1 or L4; the numeral does not restart at I on a token change; a chain grep or test still pins belam-S1; a token change leaves an older-prefix window unreaped or reaps the newest."
thought_session: dissolve-legacy-2026-09-19
title: "SM.106 (owner 05:2xZ 09-18, added to the finish set): the Prime successor window name derives from the season + loop cells (belam-S<season>-L<loop>-<numeral>) instead of copying the predecessor prefix; the belam-chain grep and the belam-S1 test literals move to a pattern; the chain reaps by seniority across prefixes"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-prime-successor-window-name-derives-from-the-season-and-loop-cells-never-copies-the-predecessor-prefix-and-the-chain-reaps-by-seniority-across-prefixes

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.106 BRIEF (sanctuary-master 09-18 05:3xZ; owner 05:2xZ verbatim via the Prime: "We also need to fix the prime session naming issue I'm guessing sanctuary master is on it."; the Prime's measured cause: rotate.py step 3 copies the predecessor window prefix, _split_roman_suffix at ~781 only increments the numeral; config:rotations after_join belam-chain entry (rotations.md ~131) greps the literal belam-S1; the literal belam-S1 is pinned in 11 test files -- test_write, test_send, test_heal_seats, test_heal_pin_reap, test_rotate_handover, test_rotate_selfreap, test_spawn_name, test_rotate_recover, test_town_cell_write, test_rotate, test_heal_watch -- the kid counts which of those assert the NAME versus merely use it as a fixture string and moves only the asserting ones to the pattern). CLAIM: see testable_claim. SHAPE: one name resolver (prime_window_name(root, predecessor) -> str) that reads season from config:ladder and the loop id from the live loop cell (kid measures where L5/L4 is declared: ladder loop cell or doc:l5-plan; if no cell exists, the resolver reads the ladder season and the loop from config:ladder loop, and the kid adds the missing cell as a template line in-round), computes the numeral from the predecessor ONLY when the S/L token matches, else I; step 3 calls it; the chain grep + reap use the pattern and sort by (token seniority, numeral). CEILING 25 production lines (resolver 12, grep/reap 8, template 5). TESTS (test_prime_window_name.py + the moved asserts): (1) predecessor belam-S1-L4-XXXI under season 2 / loop 5 -> belam-S2-L5-I; (2) predecessor belam-S2-L5-III under the same cells -> belam-S2-L5-IV; (3) the after_join chain grep pattern matches both belam-S1-L4-XXXI and belam-S2-L5-I; (4) reap of a 6-window chain mixing S1-L4-XXX/XXXI and S2-L5-I/II keeps the five newest by seniority across prefixes, never reaps S2-L5-II; (5) no literal belam-S1 assert remains (grep in the test itself). FILE SCOPE: rotate.py, config:rotations (the after_join entry line), the asserting tests, one new test file. Delivery: batch + your mur review in one line; reds fixed in-loop. This round is INSIDE the finish set (owner-added).

ID RELABEL (SM 05:4xZ): the director used SM.106 for its own SM.104 corrective chain (accepted as that label); this node is SM.107 from here.

MUR RECORD (SM 10:2xZ 09-18): the merge-up-review retry on the SM.107+108+109 batch (run key mur-core-season2-posts-sensei-director-main, director-sanctuary) FAILED as tooling, not content -- review:SM.107 hit its 1800 s stage limit, then the runner building the next stage context ran viewport.py --emit llm --depth 3, which timed out at 60 s and raised UNCAUGHT, crashing the run rc=1 with no verdicts. DECISION under delegated authority: the batch stands ACCEPTED on the director direct kid-by-kid review (378+130 / 151 / 10+83 tests green at harvest) plus the SM gate on the merge result (34 green on the delivered tests + two families, merge-tree clean, 0 deletions); already landed on core/season2/main. Residues for the redesign list, not rounds: a review stage on a 59-line diff exceeds 1800 s; a context-build timeout must fail the stage by name, never crash the runner. The successor director may retry the review for SM.107 alone (anchored --args) when seated; the acceptance does not wait on it.
