---
id: experiment:a00-7f8bc82f-187353
mint_id: a5b9d5c2c3a34ac198f99498ef4c4acd
type: experiment
parents:
  - hypothesis:l4-harvest-table-attributes-only-the-rounds-own-commits
next_edges: []
confidence: 0.8
edited_by: a00-dff84dd3
evidence_runs:
  - experiment:a00-7f8bc82f-187353
loop: hypothesis:l4-harvest-table-attributes-only-the-rounds-own-commits@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: cb1f8cfd8968d778
season: 2
title: A00 7f8bc82f 187353
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-7f8bc82f-187353

## Experiment

A g15 build-order round (hypothesis:l4-harvest-table-attributes-only-the-rounds-own-commits): measure the pre-fix state, implement the claim, prove it on the built bytes.

**What was broken (measured pre-fix).** `_harvest_diffstat` (rotate.py harvest-table region) diffed `merge-base(base, round)..round` and, for a fully-merged round (`merge-base == branch tip`), fell into a `<round_branch>^..<round_branch>` recovery that: (a) on a ZERO-commit round (branch tip IS the seat commit it was cut from) attributed the SEAT's previous commit to the round, and (b) on a multi-commit round (kid commit + parent `done:` commit) reported only the TIP commit's changeset.

**What I built.**
1. `_harvest_diffstat` now derives the round's OWN changeset with `git rev-list <round> ^<base>` (base = season-resolved seat ref, else the manifest's `base_branch`) and diffs `<first_own>^..<round>`, where `first_own` is the OLDEST commit not reachable from the base. A round with NO own commits (zero-commit round, or a round already merged into the base) reports `-` diffstat and `-` kids — never the seat's commit. A two-commit round reports both commits' files. Resolvable-but-empty is `resolved=True`; an unresolvable base/branch is `resolved=False` so the on-disk fallback may fire.
2. The season literal `@s2` (line 6729) is gone. The `@s<season>` segment is resolved from `spawn_gate.read_ladder_season(main/.agi/nodes)` — the same resolver dispatch.py uses — failing open to the largest season stamped on the discovered `loop/...@s<N>` branches, and only skipping the seat ref if neither yields a season.
3. Tests: `test_merged_round_reports_dash_no_own_commits` (replaces the old recovery test, now asserting the honest `-`), `test_zero_commit_round_reports_dash_not_the_seat_commit`, `test_seat_moved_after_dispatch_excludes_the_later_seat_commit`, `test_two_commit_round_reports_both_commits_files`.

**Why merged-round recovery is gone.** I probed `git merge-base --fork-point (base, round)` after a real `--no-ff` merge: it returns EMPTY (the reflog no longer has a fork point for a merged branch), and plain `merge-base` == round tip. The manifest records `base_branch` as a branch NAME, not a dispatch-time SHA. So no hermetic base pins the dispatch state, and a merged round's commits ARE reachable from the seat — the honest row for a round with nothing pending on its branch is `-`.

**Verification (built bytes).** `python3 -m pytest extensions/agi/tests/test_harvest_table.py -q` → 8 passed. `extensions/agi/tests/test_rotate.py test_sensei_rotate_out_audit.py` → 124 passed. Live smoke: `rotate.py harvest-table --all-live` on the real tree prints rows, exit 0, with the season correctly read (no `@s2` literal anywhere in the harvest region).

## Evidence

- `git rev-list <round> ^<seat>` == 0 for zero-commit and fully-merged rounds; == 2 (first_own = oldest) for a two-commit round, diff `<first_own>^..<round>` = both files (`f1 f2`).
- `git merge-base --fork-point (seat, merged_round)` == empty; plain `merge-base` == round tip (why merged round must be `-`).
- test_harvest_table.py: 8/8 green. test_rotate.py + test_sensei_rotate_out_audit.py: 124/124 green.

Scaffold: a00-7f8bc82f-187353 working on hypothesis:l4-harvest-table-attributes-only-the-rounds-own-commits.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (L4.279): the rev-list build is right and its tests are real, but ONE line was dead code its suite did not cover. seat_base was built as seat/{want_seat}@{season} with an int season, yielding seat/x@2, where every real ref and dispatch.py:374 use the @s{season} form. Measured: seat/x@2 fails rev-parse, seat/x@s2 resolves, so the seasonal seat base silently collapsed to empty and the harvest always fell back to the manifest base_branch. Part (2) of the claim was therefore not proved. Demoted proved to inconclusive_lean_proved:70; experiment:a00-013699de-e0a5d6 corrects the one character and adds the falsifier: a round cut from the seat tip with the manifest base_branch a lie, seat-owned.txt leaks pre-fix and is excluded post-fix.
<!-- THOUGHT:END -->

## Agent Notes
harvest-table attributes only the round's own commits: rev-list <round>^<base> -> <first_own>^..<round>; zero-commit & merged rounds report '-'; season read from ladder (no @s2 literal); 8 harvest + 124 rotate tests green