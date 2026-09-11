---
id: goal:g15
mint_id: ce522c18672a4ecc9ab7250aeffa10ec
type: goal
parents: []
next_edges: []
confidence: 1.0
edited_by: ubuntu
goal_id: G15
goal_kind: perpetual
heading_level: 2
origin: goals-doc
scaffold_hash: 666a1052f3c2d519
season: 1
seeds: []
status: active
tags:
  - goal
thought_session: iter-L3.14
title: "G15: Bugfix and optimization"
---
# goal:g15

## Agent Notes
Long-term, always active, exempt from max_goals_active. Parent of every short-term (S) goal: ids never renumbered, goal_kind stays short-term, they stop being roots. Its bigger_outcome each season is the hazard ledger, goal:s34's home. Bugfixes, edge-case hardening, security fixes, optimization and hazard removal are done in-loop under this goal or under the S goal beneath it that fits. Design: .agi/context/season-ladder-and-morals-brief.md section 2.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
L3.14, first round of the live g15 director (a00-4ad19971, Fable max, tier 1, lens vision:alive), spawned by the Alive advisor. The ladder ran end to end below this goal with no human hand: tier-0 GLM parent a00-bc4a4111 → DeepSeek kid a00-a4a9db7e → outcome:a00-a4a9db7e-ec4e27 under mvp:the-corpus-becomes-schema-valid → judged --against goal:s31 → ADJUST (s31 narrowed to the testable_claim residual; round-2 brief hypothesis:l3-done-lifts-testable-claim). Gate (one ST subgoal CLOSED) not yet met. Blocker found and fixed in the tree this round: every pi dispatch had crashed since iter-L3.13 (hypothesis:l3-pi-adapter-role-kwarg) — the director applied the two-kwarg fix itself because no pi path could carry a kid to it; deviation recorded on that node. Briefs banked here: l3-pi-adapter-role-kwarg, l3-commit-guard-inert-under-g11 (advisor finding, safety first), l3-scaffold-stamps-spawner-env (+ the no-AGI_AGENT_ID / edited_by=ubuntu sibling), l3-done-lifts-testable-claim (under s31). Director state for a successor lives at .agi/sessions/iter-L3.14/a00-4ad19971/director-scratchpad.md, not HANDOFF.md (the prime owns that file and the adapter refuses it below prime).
<!-- THOUGHT:END -->

OWNER 2026-09-11 05:1xZ (verbatim in doc:l4-owner-decisions): bugfix and optimization findings from merge-up reviews live HERE as hypothesis nodes fixed in-loop, proposed by the point director in his merge-up report — not as residue prose under goal:g17.1. RE-FILED from g17.1 (merge-up 26, 8e27dbcbb): (a) SEVENTH 0a fix-only on rotate.py — own window + own chain kill gated OFF on a numeral-chain seat (:4083, :4045-4070); belam_cap reaps the OLDEST by PID, records pid/reaped (:3885) — the chain is FIFO (owner 05:0xZ); model_confirm after the ack or argv-only (:3832); row session_ref = the ListAgents ref never the uuid (:3818); fixture chain 3 pids; dry-run 'ps -o pid,ppid' text; (b) heal.py:317-336 (pid alive at reap, dead by the timeout check) has no test; (c) crons.py: disable --now on an absent unit logs a FAILED action every 5 min under crons_live:false. Each becomes a g15 hypothesis node minted by the point.

MERGE-UP 27 (8e27dbcbb -> d1ff9b169) REVIEWED BY NAME 05:2xZ (wf_6699487e-b72, 6 agents, 15.8 min) — FINDINGS TO MINT AS g15 NODES (the point proposes/mints; the Prime accepts). L4.124 (L4.117b) ACCEPTED WITH RESIDUE, 13 MET / 4 NOT MET, three kids DEMOTED (a00-68243737 :60, a00-ceddf220 :50, a00-818fe8b1 :70; reasons on the nodes): (g15-1) spawn_gate.py:1160 write-path vision cap keys on the parents' town, ignores the new vision's own town cell — every live moral-parented vision is judged core; (g15-2) season.py:1242 _town_base precedes the recorded base_branch — a core round with a --round/agent.json record merges straight into season/s2, skipping its rung (regression on the l3w4 one-rung rule); (g15-3) season.py:992 cmd_rollover counts per_town before the ladder bump at :1033 — the s2->s3 rollover refuses every new vision (reproduced end-to-end); (g15-4) commands.stream.fragment.md:33 argv[0] <stub> resolves to a DIRECTORY — the HELD stream group cannot run; rewrite to ~/bin/sb-status, <stub>/bin/hold.sh brb|back, <stub>/bin/panic.sh (owner-only; the test must not monkeypatch the exec away). L4.126 (L4.120b) ACCEPTED WITH RESIDUE, 9 MET / 1 NOT MET, :78 stands; the Prime's real-pane measurement PASSED (helper @248 busy: region starts at the ❯ box, 'pane busy (spinner)'): (g15-5) test_send.py:152-160 busy fixture drops the ❯ box the real pane keeps — paste a REAL capture into the fixture so a narrower region cannot stay green. L4.125 (0b) ACCEPTED WITH RESIDUE as the declared PARTIAL, 8 MET / 5 NOT MET, kid verdicts stand; two NEW defects beyond 0b-b (i)-(iii): (g15-6, FIRST — a guard that can be bypassed certifies) rotate.py:3740 the first_turn allowlist splits only on | and ; then runs shell=True — the double-ampersand, `$()`, backticks and redirects bypass it (reproduced); (g15-7) the hook copy keys on AGI_SEAT which no spawn path exports, and the bootstrap record is written after the spawn (rotate.py:4660 vs :4299) — the SessionStart injection cannot fire at turn one on the live path; the Prime DEFERS the hook install to 0b-b's merge-up (one install, one fresh-session proof, when it can fire); (g15-8) config:rotations `## facts` bounds have no reader; default {} makes any HEAD move stale. OWNER 05:4xZ (verbatim in doc:l4-owner-decisions): (g15-9) send.py nudge carries the DM body inline — `[nudge: <from>]: <DM body>` — no `send.py read` round-trip; constraints listed on the ruling. Priority: g15-6, then 9, then 2/3 (season correctness), then 1, 4, 5, 7, 8.
