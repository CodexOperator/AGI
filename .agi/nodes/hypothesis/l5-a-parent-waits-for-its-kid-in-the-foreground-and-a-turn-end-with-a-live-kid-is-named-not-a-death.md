---
id: hypothesis:l5-a-parent-waits-for-its-kid-in-the-foreground-and-a-turn-end-with-a-live-kid-is-named-not-a-death
mint_id: 966afda051d74024b3508704169432dc
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 4948febce699d066
season: 2
testable_claim: "(1) cli.py wait <iter> [--agent <id>...] [--max-seconds N, default 540] blocks IN-PROCESS: polls the round's manifest every 20 s, prints one heartbeat line per poll (agent, status, elapsed), returns 0 when every named kid (default: every kid of the iter) is done|failed, returns 2 with 'still running: <agents>' when max-seconds elapses -- never a shell sleep in the parent's harness, never a background job; 540 s because the harness Bash timeout ceiling is 600 s and the call must return before it. (2) brief.py's parent step 1 (~L1884, 'poll its status with ... Sleep 30 seconds between polls') is replaced by the wait call plus this rule verbatim: NEVER end your turn to wait for a background notification -- in headless -p mode a turn-end is process exit (SM.133: 16 of 16 parent deaths); when wait returns 2, call it again. (3) the reaper (dispatch.py ~L3359 and heal.py ~L475): a parent pid gone whose harness output.log ends in a result event subtype=success AND whose kid is still live is recorded fail_reason 'turn-end with live kid <agent> (headless exit, not a death)' with death.evidence=turn-end, so SM.133's count is a manifest query from now on; a killed-mid-turn parent keeps 'pid N died (detected by reaper)'. FALSIFIERS: a wait call that returns before the kid's status is done|failed while max-seconds remain; a rendered parent brief still carrying 'Sleep 30 seconds'; a manifest whose death.evidence stays null on a success-tail parent with a live kid. TESTS, red-first per conjunct: wait -- a fake manifest flipping to done on the 3rd poll returns 0 after 3 heartbeats (poll interval injected), the max-seconds path returns 2 naming the agent; brief -- the rendered parent brief carries the NEVER line and not 'Sleep 30 seconds'; reaper -- success-tail log + live kid gives the turn-end label, a truncated log gives 'died' unchanged. FILE SCOPE: extensions/agi/bin/cli.py, brief.py, dispatch.py, heal.py; tests/test_cli_wait.py (new), test_brief.py, test_dispatch.py, test_heal.py. CEILING: 12 + 6 + 8 = 26 production lines, overage disclosed at rebrief. One kid per parent today (parallel=1), so wait usually names one agent. A kid that is OVERDUE (pid alive past its deadline) is still running for wait -- hypothesis:l4-a-timeout-mark-on-a-live-agent-is-not-terminal holds."
title: "SM.139 (from SM.133's measured cause -- experiment:a00-dd617306-ee4cd1 PROVED: 16 of 16 sanctuary parent deaths 09-18 05:00Z..09-19 02:30Z = the parent ended its harness turn on purpose to wait for a background kid-watcher, and in headless -p mode turn-end IS process exit; goal:g15): a parent waits for its kid in the FOREGROUND -- one blocking cli.py wait call that never ends the turn -- and a turn-end with a live kid is labelled by name in the manifest, never 'died'"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-a-parent-waits-for-its-kid-in-the-foreground-and-a-turn-end-with-a-live-kid-is-named-not-a-death

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
