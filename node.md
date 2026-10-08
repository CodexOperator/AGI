---
id: hypothesis:l2w15-rotate
mint_id: 4b207716d99e4152951a2d58deeb8423
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: season.py
scaffold_hash: 70ed34aad7119837
season: 1
testable_claim: A rotate.py exists whose meter reports this director session's fraction of context used and whose spawn subcommand launches a named successor as a remote-control session in tmux from a dry-run-testable command line
thought_session: season
title: "L2 wave 1.5: l2w15-rotate"
---
# hypothesis:l2w15-rotate

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILES: extensions/agi/bin/rotate.py (new) and extensions/agi/briefs/prime-director-successor.md (new, the successor's first prompt); tests in extensions/agi/tests/test_rotate.py. Section 6, Director rotation, is the design. SUBCOMMANDS. rotate.py meter [--session-log PATH]: print used tokens, window tokens and the fraction, one line, plus exit 0; the fraction is the newest request's input_tokens plus cache_read_input_tokens plus cache_creation_input_tokens divided by the director context window. Sources, try in order and say which one was used: the newest Claude Code transcript under ~/.claude/projects/-home-ubuntu-work-agi/*.jsonl (each assistant message carries a usage object with real numbers) or the remote-control debug log .agi/sessions/remote-control.log (its usage lines may be redacted; detect that and fall back). The window size is read from .agi/nodes/.geometry/ladder.md field director_context_tokens if present, else default 1000000 with a warning that the default is a guess to be corrected on the ladder node; the threshold is the ladder node's director_rotate_at, default 0.35 with the same warning. rotate.py meter --check exits 1 when fraction is at or above the threshold, so a shell can gate on it. rotate.py spawn --name NAME [--prompt-file PATH] [--tmux-session agi-rc] [--dry-run]: builds exactly this command and runs it in a new tmux window named NAME inside the tmux session, with a TTY and no pipe (a pipe makes claude print-mode and it exits; measured 2026-09-06): claude --remote-control NAME --permission-mode bypassPermissions --debug-file .agi/sessions/NAME.log PROMPT where PROMPT is the prompt file's text with the placeholder {name} replaced; refuses if a window of that name already exists; prints the tmux window and the claude.ai hint; --dry-run prints the command and touches nothing. rotate.py status: list tmux windows in the session whose name starts with agi-master, with their age. PROMPT FILE contents, in this order: you are {name}, prime director successor, a remote-control session the owner watches from claude.ai; read HANDOFF.md whole before any action, a rotation successor always reads before replacing; then continue its live checklist; standing rules: dispatch parents through dispatch.py and never do kid work, write HANDOFF.md live, push after every iteration while crons are off, and when rotate.py meter --check trips, write the handoff, run rotate.py spawn --name for the next number, and stop. TESTS: meter parses a small fake transcript and a fake ladder node (fraction and threshold, --check exit codes, redacted-log fallback); spawn --dry-run prints the exact command with the prompt substituted and refuses a duplicate window name, using a fake tmux (monkeypatch subprocess). Do not launch a real claude session from a test. REPORT: write one experiment node whose parents is this hypothesis, with a verdict on the testable claim; evidence_runs must be a list of node ids, your own experiment node counts once it exists; list every verify command and its actual output in the body. Engine files are edited in place; a new engine file is created directly under extensions/agi/bin/ (level3.py mints its build node later). Run the suite through python3 extensions/agi/bin/commands.py run tests, green before you report; every new rule gets a test that was red first. Do not commit, do not push, do not run grid.py commit. If git status shows files you did not create, report them and never touch them. Design source: .agi/context/season-ladder-and-morals-brief.md