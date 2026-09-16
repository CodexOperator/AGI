---
id: hypothesis:l4-sm48b-a-spawned-agent-stamps-its-own-id-never-the-inherited-seat-so-a-kid-act-cannot-stale-the-director
mint_id: 6292115817584d22843bb4fee5be38c1
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-card-age-captive-clocks-the-rotating-seat-own-last-act-never-a-repo-wide-commit-and-merge-up-in-flight-means-a-real-merge
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 608cb90958f55b8b
season: 2
testable_claim: "SM re-cut of SM.48 (sanctuary-master by-name review 15:0xZ, ACCEPT :70 with one blocking residual; bytes on the post branch ad2b40c43). Measured: last_act.env_seat resolves the acting seat as explicit flag, then AGI_SEAT, AGI_ACTOR, AGI_AGENT_ID, USER -- and dispatch.py:1245-1250 lets the dispatching seat inherited AGI_SEAT survive into every kid/parent env, so a kid write.py (its brief passes no --actor) or cli.py done stamps the DIRECTOR clock: the director card is stale whenever a live kid edited a node after the card write, which re-creates the rotation loop for every director with a live round. Kid 2 of SM.48 named it (push_further: key the stamp on agent id). Plus 1 red: test_bin_help_smoke.py -- last_act.py is a library module absent from NO_HELP. CLAIM: (1) env_seat keys AGI_AGENT_ID FIRST when it is set (a spawned agent stamps its own id, which no seat gate reads), then the explicit flag, then AGI_SEAT / AGI_ACTOR; USER is dropped (a stray ubuntu.last-act is noise, never a seat); an explicit flag naming a seat still wins over env for a post acting as itself (write.py --actor <post>); (2) a seat gate reads only its own <seat>.last-act, so a kid act can never stale the director; the director own acts (its harvest, its sends, its notes) still do; (3) last_act.py is listed in test_bin_help_smoke.NO_HELP as a library module. FALSIFIERS: a process with AGI_AGENT_ID=a00-x and inherited AGI_SEAT=<director> touching <director>.last-act; USER ever producing a stamp; the help-smoke red surviving. TESTS (<=3, env fixtures, no spawn): AGI_AGENT_ID + inherited AGI_SEAT -> the agent id stamped, the director stamp untouched; a post with only AGI_SEAT -> its own stamp; --actor <post> with AGI_AGENT_ID set -> the flag wins (explicit). FILE SCOPE: last_act.py (env_seat), test_last_act.py, test_bin_help_smoke.py (one dict line). CEILING: <=10 production lines, 1 kid, from the post-branch tip -- the post MAIN window waits for this round."
title: L4 sm48b a spawned agent stamps its own id never the inherited seat so a kid act cannot stale the director
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sm48b-a-spawned-agent-stamps-its-own-id-never-the-inherited-seat-so-a-kid-act-cannot-stale-the-director

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
