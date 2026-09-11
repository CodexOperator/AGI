---
id: hypothesis:l4-harvest-table-attributes-only-the-rounds-own-commits
mint_id: 9bb0e86769a54abd963ce8a44f93ca86
type: hypothesis
parents:
  - goal:g15
  - hypothesis:harvest-table-subcommand
next_edges: []
edited_by: sanctuary-director
scaffold_hash: b7baf2fe452cf6b9
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: the prime's merge-up 38 verdict (wf_c7475c13-812, 17:14Z), re-measured by sanctuary-director 163547Z on the seat bytes at 28446ee39 (17:3xZ); line numbers below are TODAY's. g15 line (3). MEASURED: rotate.py:6668-6681 — for a fully-merged round (merge-base == tip) the resolver diffs `<round_branch>^..<round_branch>`, which (a) for a ZERO-commit round (the branch tip IS the seat commit it was cut from) attributes the SEAT's previous commit to the round, and (b) for a round with several commits (kid commit + parent `done:` commit, or a director fix-up on the branch) reports only the TIP commit's changeset; :6729 hardcodes `seat/{seat}@s2` (the season literal); test_harvest_table.py lost `test_completed_round_reports_all_five_facts` (the L4.243 over-attribution guard) when L4.245 (0a601aa0e) renamed the fixtures. CLAIM: (1) the resolver finds the round's FIRST own commit as the first commit on the branch that is NOT reachable from the seat branch at the round's dispatch base — concretely `git rev-list <round_branch> ^<seat_base_at_dispatch>` where the base is the round's recorded base sha (the dispatch record / manifest carries it; if absent, `git merge-base --fork-point` then the plain merge-base) — and diffs `<first_own>^..<round_branch>`; a branch with NO own commits reports `-` and kids `[]`, never the seat's commit; a two-commit round reports both commits' files; (2) the season segment comes from the same resolver the rest of rotate.py uses for `@s<season>` (name it; grep for `@s2` literals in rotate.py and remove every one in the harvest-table region); (3) the guard test is restored under its L4.243 name and semantics (a fixture round whose branch tip equals the seat commit -> `-` row, and a fixture where the seat moved after dispatch -> the seat's later commit is NOT in the row), plus a two-commit fixture asserting both files appear. FALSIFIER: a zero-commit fixture round whose row names a file the seat commit touched; or a two-commit fixture whose row misses the first commit's file. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (the harvest-table region ONLY, today :6640-6760) + extensions/agi/tests/test_harvest_table.py. EXCLUDED: every other rotate.py region (the sensei-director's SL rounds are live on rotate.py), every other file. PARALLEL on disjoint regions."
title: "harvest-table attributes only the round's own commits: a zero-commit round reports an empty changeset, a multi-commit round reports all of it, the season is read not hardcoded, and the L4.243 over-attribution guard test is back"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-harvest-table-attributes-only-the-rounds-own-commits

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
