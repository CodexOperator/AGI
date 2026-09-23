---
id: hypothesis:l4-sm48b-a-spawned-agent-stamps-its-own-id-never-the-inherited-seat-so-a-kid-act-cannot-stale-the-director
mint_id: 6292115817584d22843bb4fee5be38c1
type: hypothesis
parents:
  - goal:g6.10
  - hypothesis:l4-the-card-age-captive-clocks-the-rotating-seat-own-last-act-never-a-repo-wide-commit-and-merge-up-in-flight-means-a-real-merge
next_edges: []
edited_by: belam
scaffold_hash: 608cb90958f55b8b
season: 2
testable_claim: "SM re-cut of SM.48 (sanctuary-master by-name review 15:0xZ, ACCEPT :70 with one blocking residual; bytes on the post branch ad2b40c43). Measured: last_act.env_seat resolves the acting seat as explicit flag, then AGI_SEAT, AGI_ACTOR, AGI_AGENT_ID, USER -- and dispatch.py:1245-1250 lets the dispatching seat inherited AGI_SEAT survive into every kid/parent env, so a kid write.py (its brief passes no --actor) or cli.py done stamps the DIRECTOR clock: the director card is stale whenever a live kid edited a node after the card write, which re-creates the rotation loop for every director with a live round. Kid 2 of SM.48 named it (push_further: key the stamp on agent id). Plus 1 red: test_bin_help_smoke.py -- last_act.py is a library module absent from NO_HELP. CLAIM: (1) env_seat keys AGI_AGENT_ID FIRST when it is set (a spawned agent stamps its own id, which no seat gate reads), then the explicit flag, then AGI_SEAT / AGI_ACTOR; USER is dropped (a stray ubuntu.last-act is noise, never a seat); an explicit flag naming a seat still wins over env for a post acting as itself (write.py --actor <post>); (2) a seat gate reads only its own <seat>.last-act, so a kid act can never stale the director; the director own acts (its harvest, its sends, its notes) still do; (3) last_act.py is listed in test_bin_help_smoke.NO_HELP as a library module. FALSIFIERS: a process with AGI_AGENT_ID=a00-x and inherited AGI_SEAT=<director> touching <director>.last-act; USER ever producing a stamp; the help-smoke red surviving. TESTS (<=3, env fixtures, no spawn): AGI_AGENT_ID + inherited AGI_SEAT -> the agent id stamped, the director stamp untouched; a post with only AGI_SEAT -> its own stamp; --actor <post> with AGI_AGENT_ID set -> the flag wins (explicit). FILE SCOPE: last_act.py (env_seat), test_last_act.py, test_bin_help_smoke.py (one dict line). CEILING: <=10 production lines, 1 kid, from the post-branch tip -- the post MAIN window waits for this round."
thought_session: dissolve-legacy-2026-09-19
title: L4 sm48b a spawned agent stamps its own id never the inherited seat so a kid act cannot stale the director
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sm48b-a-spawned-agent-stamps-its-own-id-never-the-inherited-seat-so-a-kid-act-cannot-stale-the-director

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.49 harvest reviewed BY NAME by sanctuary-master gen 3 15:5xZ (merged to the post branch 52a8487e8, 2 kids, 17 production lines): ACCEPT at :85. Probed env_seat from the post-branch bytes on seven env shapes: kid and parent with an inherited AGI_SEAT stamp their own agent id; a director (AGI_TIER director/prime_director, OWNED_TIERS) stamps its seat even with an agent id in env; the explicit flag wins everywhere; USER never stamps. Kid 1 regression (a global reorder broke a director own self-stamp) was caught and fixed by kid 2 with the AGI_TIER split, honestly demoted :70 by the parent. last_act.py in NO_HELP. SM.48 + SM.48b are one merge-up: [merge-up] line to belam sent.

SM.68 item 4 (director gen 29, sensei-director, discovered missing at harvest -- the kid own report described writing this note but it was not actually committed on the round branch, kid worktree already cleaned up by the time this was found, added here directly by the director since node-field edits through write.py are within director scope): a director-tier process (AGI_SEAT set, AGI_AGENT_ID set) with NO AGI_TIER set at all resolves env_seat() to the AGENT id, same as AGI_TIER=kid or AGI_TIER=parent -- only an explicit AGI_TIER=director or AGI_TIER=prime_director resolves to the seat. This node own claim and tests covered the tier-present arms only; the no-tier-at-all director shape was undocumented and untested until now. Now pinned by test_no_tier_director_shape_resolves_the_agent_id (test_last_act.py, landed on the SM.68 branch). A director spawned or run without AGI_TIER set stamps a clock no seat gate reads, silently missing the fix this node built.
