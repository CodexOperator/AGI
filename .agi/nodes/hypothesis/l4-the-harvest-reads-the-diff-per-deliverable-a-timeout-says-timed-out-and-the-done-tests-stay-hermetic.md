---
id: hypothesis:l4-the-harvest-reads-the-diff-per-deliverable-a-timeout-says-timed-out-and-the-done-tests-stay-hermetic
mint_id: c7a1fd05eb7b46beb7c7e968348856b7
type: hypothesis
parents:
  - goal:g6.14
next_edges: []
edited_by: belam
scaffold_hash: 43c882523ba3853b
season: 2
testable_claim: "SL7.137 residue (belam GO 20:3xZ, pi review mur-sl7-137-2, landed 35bb1f90f) + two lines from SM; brief.py + cli.py tests + workflow.py + the node text; ONE kid, in this order; line numbers as of 35bb1f90f -- re-locate by name. (1) The two new test_cli.py tests (~:1429, ~:1468: worktree done-commit subject with an empty / absent kid verdict) must stay hermetic under the kid-dispatch env where the harness pins core.hooksPath via GIT_CONFIG_VALUE_0 (the conjunct-2 probe popped GIT_CONFIG_* for that reason) -- prove they pass with GIT_CONFIG_COUNT/KEY_0/VALUE_0 set as dispatch sets them, or pin the env inside the test. (2) The node text of hypothesis:l4-the-kid-brief-demands-a-title-...: its THOUGHT/body says the director's hand edit of a kid node was ACCEPTED by write.py (probes[2]) while item 3 says never land it by hand -- reword the record (accepted by the tool is not permitted by the protocol) or gate write.py so a director's --actor write to a kid's authored region refuses by name; pick one, say why. (3) workflow.py: a pi stage that hits its timeout_s must print 'stage <name> timed out after N s' FIRST, never 'could not start pi: <whole command>' with the TimeoutExpired text buried after the prompt (SM 19:23Z, mur-sm-60: 30 min of pi spend, refuter never ran, reported as could-not-start). (4) Parent brief, harvest segment (_parent): the harvest reads the DIFF for every deliverable the kid names -- never the kid's THOUGHT or summary; a claimed-but-absent deliverable demotes that kid's verdict (inconclusive_lean_disproved with the probe named), it is never silently patched by the parent or the director (SM 20:33Z director gen 29; SL7.136 item 14: kid 1 claimed a node edit the branch never carried). Proof: a test per code item; the rendered _parent brief carries the diff-per-deliverable rule; a fixture with a claimed-but-absent deliverable yields the demotion."
thought_session: dissolve-legacy-2026-09-19
title: L4 the harvest reads the diff per deliverable, a timeout says timed out, and the done tests stay hermetic
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-harvest-reads-the-diff-per-deliverable-a-timeout-says-timed-out-and-the-done-tests-stay-hermetic

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
2026-09-16 20:5xZ master-sensei: minted as the SL7.137 residue the Prime named in the GO (two lines: hermetic done tests under the dispatch git env; the node text that called a director's hand edit 'accepted'), plus SM's two lines of the hour (workflow.py timeout wording from mur-sm-60; the harvest reads the diff per deliverable, from director gen 29 and SL7.136 item 14 -- the very edge the Prime drew on my own loop-branch commit). Four items, one kid, dispatched as SL7.138.
<!-- THOUGHT:END -->
