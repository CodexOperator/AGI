---
id: hypothesis:l3w0-rotate-roles
mint_id: dd66aedd52f1487ab471c7223b7af289
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: ubuntu
scaffold_hash: f5728c0c2524efb3
season: 1
testable_claim: rotate.py spawn takes --model --effort --settings --tier with defaults from the ladder roles table, assembles the successor prompt through brief.py so the constitution head precedes the prompt text, and rotate.py loop --role runs the super-ralph rotation where a successor answers the single word continue when the handoff needs no change
title: L3w0 rotate roles
---
# hypothesis:l3w0-rotate-roles

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OBSERVED: agi-master-2 was spawned by rotate.py spawn with no head and no --model (ran on Sonnet 5 instead of Fable 5.1 max) because spawn reads briefs/prime-director-successor.md, substitutes the name and launches without brief.py assemble. FILES: extensions/agi/bin/rotate.py, extensions/agi/bin/brief.py (only if assemble needs a prompt-file hook), extensions/agi/briefs/prime-director-successor.md, tests/test_rotate.py. CHANGE: spawn resolves model, effort, settings from the ladder roles row for --tier (default prime_director) unless overridden by flags; builds the claude --remote-control command with --model, --effort, and --settings when the row has one; the prompt is brief.py assemble for that tier with the successor file as the body so the head (prayers, then the Michael line, then the readings by role) comes first. Add the standing rule to the successor template: conserve context at all costs, work to the 0.35 cap, witness as much total progress as possible, think of the offspring first (brief section 1.5, owner wording). LOOP: rotate.py loop --role R --name-prefix P: meter, and when over director_rotate_at write nothing itself (the handoff is the director's), spawn the successor, then read the successor's first reply from its log; the word continue alone means the handoff stood. Depends on l3w0-ladder-roles-table for the table; until it lands, read harnesses.claude-code from config.json. VERIFY: red-first test that the built command contains --model claude-fable-5-1, --effort max, the ultracode settings, and that the prompt text begins with the head and contains the Michael line; a dry spawn on this repo prints the command. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Engine files edited in place; suite green via python3 extensions/agi/bin/commands.py run tests; every new rule gets a test that was red first. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them. Design source: .agi/context/l3-command-ladder-brief.md

ADDENDUM 2026-09-06 (owner): default successor name is belam-N (rotate.py derives N from the highest existing belam-* tmux window plus one; --name still overrides); the successor template's first line names the mantle: You are Belam, prime director of the agi graph; the mantle is in your head above. Also the branch rule changed with the adopted seasons-as-branches mapping: the prime works on season/sN, not master; the template says so and the meter/spawn refuse to run on master once a season/* branch exists (print the branch to check out).

ADDENDUM 2026-09-06 (belam, prime, at L3 open): (1) the live prime's tmux window is named belam-S1-L3, so the belam-N derivation must treat a belam-* window with no trailing integer as N=1 (successor = belam-2); rotate.py status must list belam-* windows as well as agi-master-*. (2) spawn takes --prompt-file to override the successor body: the owner wants the gate proved live right after this lands with a throwaway successor (rotate.py spawn --name belam-test --prompt-file X where X says: answer the single word continue, then stop) so the head, --model claude-fable-5-1, --effort max and the ultracode settings are witnessed in a real window; the parent may run that proof itself only with --dry-run, the prime runs the live one. (3) rounds are two parents, not three; the successor template's round line says two.

OWNER RULE 2026-09-07 (verbatim): Any time you need to rotate use Roman numerals for the next session. So the next is belam-S1-L3-II and the next prime is Belam II aka belam the second. FOLLOW-UP for rotate.py: derive the successor name as <prefix>-<ROMAN> where the prefix is the current window name stripped of any trailing -<ROMAN> (belam-S1-L3 -> belam-S1-L3-II -> belam-S1-L3-III), replacing the belam-N integer scheme; --name still overrides; the successor template's first line names the prime Belam II, Belam III accordingly. Belam ran the first rotation by hand with --name belam-S1-L3-II.
