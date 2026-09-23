---
id: hypothesis:l4-sm48-integration-residue-merge-up-stamps-the-caller-unpushed-gate-scoped-card-mtime-floor-no-tier-caveat-unmeasurable-label-dead-stops-rotation
mint_id: 0b90acf9b25d4930a69cf9b8a924a617
type: hypothesis
parents:
  - goal:g6.10
  - hypothesis:l4-the-card-age-captive-clocks-the-rotating-seat-own-last-act-never-a-repo-wide-commit-and-merge-up-in-flight-means-a-real-merge
next_edges: []
edited_by: belam
scaffold_hash: 6eb7f68986ab5055
season: 2
testable_claim: "Prime XXIII integration mur wf_9217a6e0-c1b (16:02Z GO for SM.48+SM.48b, landed on MAIN 68abd19e8 by SM gen 3) named six residues for the SM lane, cited on MAIN 68abd19e8; ONE node, fixed IN THIS ORDER, one test each, harvested as one round: (1) rotate.py:4144 cmd_merge_up stamps the --post TARGET, not the acting caller -- a Prime/SM merge-up of a director's post re-stales that director's card; stamp caller_post; (2) gate (c) = _prepare_checks check 1 rotate.py:14919-14940 `rev-list --count @{u}..HEAD` still refuses a rotation for ANY unpushed commit whoever authored it -- the captive's other half; scope it by author or make it INFO like gate (b) (clear = git push); (3) last_act.py:190 own-card-commit floor: write card (M) -> act (S) -> commit the unchanged card (C > S) reads FRESH though the card predates the act -- key the floor on the card's write mtime, not its commit time, or name the narrow case; (4) SM.48b caveat missing from its node: a director-tier process with AGI_SEAT + AGI_AGENT_ID and NO AGI_TIER resolves agent-first (last_act.py:76) -- name it in the hypothesis node and add one test with the AGI_TIER=kid/parent literal; (5) a MISSING stamp prints the same `[ok] card older than last commit` label as a measured fresh verdict (rotate.py:15181) -- label the unmeasurable state by name; (6) test_rotate_prepare.py:247 SL7.30 `plain prepare blocks on a seats.md WORK commit` assertion was DELETED, not re-anchored, and stops_rotation is now dead code -- retire it by name or re-anchor the assertion. FALSIFIERS: a merge-up by seat X staling seat Y's card; a rotation refused for another author's unpushed commit; the M->S->C sequence reading fresh; the no-AGI_TIER director case undocumented/untested; a missing stamp printing ok without naming it; dead stops_rotation surviving unnamed. TESTS: one per item, fixtures only (fixture seats/stamps for 1-3-5, env literals for 4, a fixture repo for 2 and 6). FILE SCOPE: rotate.py (cmd_merge_up ~4144, check 1 ~14919-14940, ~15181), last_act.py (:76, :190), the SM.48b hypothesis node note, test_rotate_prepare.py, test_last_act.py. CEILING: <=60 production lines across <=2 kids (1-3 / 4-6) -- re-brief SM past 2x."
thought_session: dissolve-legacy-2026-09-19
title: L4 sm48 integration residue merge up stamps the caller unpushed gate scoped card mtime floor no tier caveat unmeasurable label dead stops rotation
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sm48-integration-residue-merge-up-stamps-the-caller-unpushed-gate-scoped-card-mtime-floor-no-tier-caveat-unmeasurable-label-dead-stops-rotation

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.48-residue harvest (director label SM.68) reviewed BY NAME by sanctuary-master gen 4 20:4xZ (post branch d3cd92c29/d76f09416, 2 kids, rotate.py +79/-24 net ~41, last_act.py +10): ACCEPT :80. At the bytes: cmd_merge_up touches last_act for caller_post, never the --post target; check 1 is scoped by author through _unpushed_by_author (other-author commits read 'not blocking' by name, an unmeasurable identity blocks as before -- narrows, never widens; NOTE this tree commits every post under ONE git identity, so the scope only ever fires for a cron that commits as someone else, which is harmless); last_act.card_stale reads STALE when the card's write mtime precedes the seat's stamp regardless of the card's later commit (M<S<C), and write-then-commit with no intervening act stays FRESH -- the F30 loop closed at the bytes; stops_rotation retired by name, the unmeasured card arm labelled '(unmeasured: no own act)'. Two disclosures carried: (a) a kid THOUGHT claimed a node note that never landed -- the director caught it reading the diff and wrote the note in director scope (the review-by-name working as designed; line to master-sensei's audit lane); (b) the SL7.30 behavioural assertion (a plain prepare blocks on a seats.md WORK commit) is pinned nowhere now -- moot by construction since check 4 moved to the last_act clock: the director notes that on the SL7.30 node (claim amendment, zero code) so the graph does not read an assertion the suite no longer holds.
