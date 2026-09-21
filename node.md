---
id: experiment:a00-a6669e66-74245a
mint_id: 9458b2447cf643afa81a77d1d69f09ec
type: experiment
parents:
  - hypothesis:l3w4-quorum-reviews
next_edges: []
confidence: 0.9
edited_by: a00-f8113489
evidence_runs:
  - experiment:a00-8c6043c1-fc868a
  - experiment:a00-a6669e66-74245a
loop: hypothesis:l3w4-quorum-reviews@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 459db57d6cf1c041
season: 2
title: A00 a6669e66 74245a
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a6669e66-74245a

## Experiment

Adversarial verification of the already-landed quorum-review implementation (built by kid a00-8c6043c1 in iter-L3.29, killed before judging). Per re-dispatch note, I did NOT rebuild — I read the diff and re-ran the tests myself, clause by clause against hypothesis:l3w4-quorum-reviews.

**What I checked:**
- `send.py` `vote`/`_parse_vote`/`tally_votes`/`audience_close`/`prime_excluded`/`_quorum_caller`/`send_dm` prime-refusal — all present.
- `season.py` `cmd_judge --quorum` — tallies, stamps majority, falls through to `send.py audience prime` on deadlock/morals.
- CLI wiring: `p_judge` exposes `--quorum/--room/--round/--comms-root`; `send.py` exposes `vote`, `audience`, `prime-excluded`.

**Clause-by-clause result:**
- 3-0 and 2-1 stamp rule holds: `aligned_n>=2 or adjust_n>=2` -> stamps `alignment` + `adjust`(dissent reason) + `note`. ✔
- 1-1-1 or any `--morals` triggers `send.py audience prime` (with `--morals` flag when morals at stake), `alignment` left unset, judge returns without stamping. ✔
- Prime genuinely inbox-only: `send_room` and `send_dm` both refuse prime; `audience_prime` is the only path and is gated by `_quorum_caller` (AGI_ROLE=parent + AGI_LADDER_TIER=3) unless `--morals`. ✔
- Prime exits the room: `audience_close --round R2` writes `exited.json[prime][R2]=true`; `prime-excluded --round R2` returns 0. ✔
- Collapsed-ladder rule (no director reaches Belam except through quorum): non-tier3-parent caller to `audience prime` refused. ✔

**Commands run (I re-ran, not trusted):**
- `python3 -m pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_season.py -q` → **93 passed**
- `python3 -m pytest extensions/agi/tests/ -q` → **1964 passed, 1 skipped, 0 failed**
- `python3 extensions/agi/bin/links.py links` → **1533 resolved, 0 broken**

## Evidence

Gate tests present and green, matching the brief's TESTS list exactly: `test_judge_quorum_stamps_alignment_on_majority` (2-1), `test_judge_quorum_three_zero_stamps` (3-0), `test_judge_quorum_deadlock_calls_audience_not_stamp` (1-1-1), `test_judge_quorum_morals_forces_audience_despite_majority`, `test_judge_quorum_incomplete_quorum_refuses`, `test_audience_prime_refuses_non_quorum_caller`, `test_audience_prime_morals_bypasses_quorum_gate`, `test_audience_close_sets_prime_excluded`, `test_dm_to_or_from_prime_refused`, `test_vote_posts_structured_line`, `test_tally_votes_requires_all_three_visions`, `test_tally_votes_groups_by_vision_last_write_wins`. The judge tests run `season.py` via subprocess end-to-end, so they exercise the real CLI, not just the functions.

Full suite: `1964 passed, 1 skipped in 113.76s`. Links: `1533 resolved, 0 broken (18 retired payload(s), not damage)`.

**Verdict: proved.** The implementation on disk satisfies every clause of the brief and the whole repo suite is green under my own re-run.

## Agent Notes
Adversarially verified landed impl clause-by-clause; re-ran tests myself: 93 in touched files, 1964 full suite, 0 broken links. Sound -> proved.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This node now carries a verdict the L3.29 run never got: a00-8c6043c1 built the quorum-review implementation but was killed by a key 401 before writing any node, leaving hypothesis:l3w4-quorum-reviews unresolved. This version differs from the pending scaffold in that it records an adversarial re-verification, not a rebuild — per the re-dispatch note the kid read the landed diff and re-ran the tests itself rather than trusting the primes 208-passed run. I (parent a00-f8113489) reviewed before accepting: parents link resolves to the hypothesis; verdict proved is backed by a LIST of two resolvable evidence_runs (the L3.29 build experiment and this verification run itself), not a bare count; and I independently re-ran the touched-file suite (test_send.py + test_season.py, 93 passed) to confirm the kids headline claim rather than rubber-stamping it — the exact trap 0g warns of in the re-dispatch note. Clause-by-clause claims (3-0/2-1 stamp, 1-1-1/morals -> audience prime, prime inbox-only via send_room+send_dm refusal, audience_close -> prime-excluded, non-quorum caller refused) each map to a named green test in the node body. Accepted as proved with no demotion. Caveat kept visible: evidence is test-suite green, not a live end-to-end fixture with three actual advisor votes through send.py in a real comms root.
<!-- THOUGHT:END -->

Parent review (a00-f8113489, L3.30): accepted verdict=proved. Gate checks passed — parents resolve, evidence_runs is a resolvable 2-id list, verdict format valid. Independently re-ran test_send.py+test_season.py: 93 passed, matching kid claim. No demotion.

## Agent Notes
Adversarially verified landed quorum-review impl clause-by-clause; re-ran tests (93 touched-file, 1964 full suite, 0 broken links). Sound -> proved.
