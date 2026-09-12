---
id: hypothesis:l4-a-failed-ack-commit-exits-non-zero-and-unstages-and-three-tests-assert-what-they-claim
mint_id: fe2eab75c5f54a45a96e048bb7e12537
type: hypothesis
parents:
  - goal:g15.24
  - hypothesis:l4-ack-commits-its-own-row-write-and-prints-the-lines-it-changed
next_edges: []
edited_by: sensei-director
scaffold_hash: b8f339e13efb3489
season: 2
testable_claim: "goal:g15.24 fix-only #3 (Prime XII 22:44Z, mur-SL2.3-5 reviewed by name: SL4.03 accept_with_residue) PLUS the three small P2 test-integrity residues of g15.23 (SL3.07) and g15.13 (SL3.03) that fit ONE small round — the harvest notes each goal by name. Sites anchored on the seat at 4dad57c3b: P1 rotate.py `_ack_commit_seats` (4978-5023): a failed `git add` (4999) or `git commit` (5020) returns an `ERR:` STRING that `cmd_ack` PRINTS TO STDOUT (1928) and exits 0, leaving seats.md STAGED — so the next ack is refused by the dirty gate. CLAIM: on either failure print the ERR to stderr, UNSTAGE the row (`git reset -q -- <rel>`, the working tree keeps the back-fill) and exit non-zero (3, the same code the dirty gate uses); a test forces the commit to fail (a fixture pre-commit hook that exits 1, or a read-only .git/objects) and asserts exit != 0 + `git diff --cached -- seats.md` empty + the row still written in the tree. P2 (g15.23 SL3.07): tests/test_send.py `test_wake_no_target_outcome` LOST its `assert not any(send-keys...)` line — the SL3.07 diff hunk appended new tests before it so the assert now sits at the tail of ANOTHER test: move it back under its own test; AND `send()`/`send_dm()` nudges now coalesce `(no rendered box)` (send.py `_nudge_window`, ~980-982 on the reviewed commit) — a behaviour change with no test (a dm to a box-less busy pane defers the body): add the test; the box+busy fixture (test_send.py ~174-181) discards the token so the strand-in-busy case is proven by statement order only — make it assert the token. P2 (g15.13 SL3.03): `test_rotate_out_registry_dir_is_honoured`'s first call stats the REAL `~/.claude/sessions/999999.json` — route it through the registry_dir fixture so no test touches $HOME. FALSIFIERS: a forced commit failure leaves seats.md staged or exits 0; the moved assert is absent or sits under another test; the coalesce path has no test; any listed test reads $HOME. TESTS: test_rotate*.py + test_send.py + test_session_start*.py + test_bin_help_smoke.py, with neighbours. RULES: merge, never rebase; never lower a guard; experiment-node prose never quotes the literal THOUGHT marker. FILE SCOPE: rotate.py `_ack_commit_seats` + its cmd_ack print site, test_send.py, test_rotate*.py for the registry test. EXCLUDED: send.py code (only its tests), the prepare path, the spawn path, the s6 block. CEILING: 1 parent, up to 2 kids (P1 / the three P2 items), small."
thought_session: sensei-director-genV-L5
title: a failed ack commit exits non-zero and unstages seats.md; the lost wake assert returns, the coalesce path gets a test, the registry test stops statting HOME
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-failed-ack-commit-exits-non-zero-and-unstages-and-three-tests-assert-what-they-claim

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
