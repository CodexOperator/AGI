---
id: hypothesis:l3-send-comms-root
mint_id: c8d94c0dfdbf48519154e28cc136d18e
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-II
scaffold_hash: fd20ed35f31b377f
season: 2
testable_claim: send.py resolves the comms root from a declared, committed, season-level location (config locations.comms_root, default .agi/comms/<season>/) instead of the newest iteration dir, the quorum record is tracked by git, --from is honored on room and dm sends, and read has an --all that does not advance the cursor
title: L3 send comms root
---
# hypothesis:l3-send-comms-root

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OBSERVED 2026-09-07 (wave-3 advisors a00-1742819b and a00-341de54e, plus Belam II): (1) send.py _default_comms_root (send.py:117-131) picks the newest iteration dir ranking int-named dirs over string-named ones (97 int / 64 string dirs, max iter-1088), so the standing room tier3-quorum lives at .agi/sessions/iter-1088/comms/ and every agent sees it only while that ordering holds; fixing the sort alone would RESET the standing room each iteration — the right fix is a declared root. (2) .gitignore line 38 leaves the whole quorum record untracked, so the season's council record is not in the graph's history. (3) send.py --from X before the subcommand is ignored on room sends (the prime's convening message and one advisor post show from: unknown; a post from an agent with AGI_AGENT_ID set shows its id). (4) send.py read --me advances the read cursor and there is no --all, so re-reading a room returns empty and agents cat the file. FILES: extensions/agi/bin/send.py, .agi/config.json (locations.comms_root — edit through write.py, the config is a node payload), .gitignore, extensions/agi/tests/test_send.py, skills/agi/SKILL.md comms lines. CHANGE: comms_root resolution = --comms-root flag, then config locations.comms_root, then default <graph_root>/comms/season-<N>/ (season from the ladder), never the newest iteration; migrate the existing tier3-quorum.md and dm files from iter-1088/comms into the new root once, preserving order; un-ignore the new root so room and dm files are committed; --from honored for every verb; read --all (and peek) never advance the cursor; sender defaults to AGI_AGENT_ID, then --from, then the tmux window name if present, then unknown. VERIFY: red-first tests for each of the four defects; live: send.py rooms shows tier3-quorum with its 3+ existing posts at the new root; git status shows the room file tracked. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output. Do not commit, push, or run grid.py commit. Live claude-code advisors and a director use send.py this hour — keep edits atomic and the old root readable until migration is done in the same edit; report unexpected files, never touch them.
