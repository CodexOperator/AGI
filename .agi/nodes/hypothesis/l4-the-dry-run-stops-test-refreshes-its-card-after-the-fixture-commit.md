---
id: hypothesis:l4-the-dry-run-stops-test-refreshes-its-card-after-the-fixture-commit
mint_id: a1739033f1464090a02e0d4156167505
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 3e2a99388b73490c
season: 2
testable_claim: "goal:g15.25 director fix-up, LANDED on the seat at c38119b89 (sensei-director gen XII, harvest of SL7.41/42, 11:48Z) — a g15 node by Prime order (belam 11:53Z: the two director fixture races are g15 nodes, not silent fixes). MEASURED: test_rotate_self_stops_dry_run_touches_nothing (test_rotate.py:2860, the g15.25 (b) falsifier) writes the card and THEN calls _init_git_remote, whose fixture commit lands one or more git subprocesses later; the captive \"card older than last commit\" (rotate.py:9690-9694) compares the card float st_mtime against the commit whole-second %ct, so whenever the write and the commit straddle a second boundary the card reads stale, _prepare_checks blocks, and cmd_rotate_self returns 3 with the blocker on stderr that capsys swallows — 1 red in 996 in the harvest neighbourhood (nbhd-1), green in isolation, the same failure the SL7.42 kid saw on its own branch and could not place (kid experiment:a00-c55b3218-f99a7c). CLAIM: os.utime(card, None) after the fixture commit makes st_mtime >= the commit %ct on every run (floor(commit wallclock) <= commit wallclock <= utime wallclock), the way a live rotate-out stops write refreshes the card; bytes unchanged, so the dirty-tree captive stays clean and card_before == card.read_bytes() still holds. PROOF (built and run, not read): with the utime line forced to time.time()-5 the test fails assert 3 == 0 deterministically; restored, it passes; test_rotate.py 227 passed. NEAR MISS: bumping the fixture commit date (GIT_COMMITTER_DATE) back a second satisfies the words and moves the race into the other captives that read %ct; sleeping 1 s before the commit satisfies nothing on a slow box. FALSIFIER: the test reads rc 3 again in a loaded suite run. FILE SCOPE: extensions/agi/tests/test_rotate.py, that one test, eight lines; no production change. CEILING: fixture-only."
thought_session: sensei-director-genXII-L12
title: the dry-run stops test refreshes its card mtime after the fixture commit, so the card-older-than-last-commit captive measures the claim and not a second boundary
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-dry-run-stops-test-refreshes-its-card-after-the-fixture-commit

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted after the fact, at the SL7.41/42 harvest, for a fix the director landed rather than dispatched. (1) The rule: a director never does kid work; red = fix on the seat, merge again, re-run. (2) What happened: nbhd-1 read 1/996 red on the g15.25 (b) falsifier; the blocker was invisible (capsys swallowed stderr) until the captive list was read and the mtime-vs-%ct comparison found at rotate.py:9690; forcing the card 5 s older reproduced rc 3, restoring the utime line passed. (3) Near miss: dispatching an $1 round to write eight fixture lines would have held SL2#20 for 20-30 min on a defect already measured to the line. (4) The property that makes the kid-work rule not apply: the fix is inside the fixture of a round already harvested and proved, changes no production byte, and the merge-up rule names the seat as where a red is fixed. Recorded as a node by Prime order (11:53Z) so the graph carries the fix and the merge line can name it.
<!-- THOUGHT:END -->
