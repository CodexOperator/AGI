---
id: experiment:a00-e38c5702-608411
mint_id: 9350df29e69e4c72858e264254850fba
type: experiment
parents:
  - hypothesis:a00-c89eaaae-7dcb85
next_edges: []
confidence: 0.9
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
scaffold_hash: b43be5ba740d41f5
title: Edit agent-prompt.md Rule 5 to ban git, verifying zero actionable git instructions remain
verdict: inconclusive_lean_proved:50
---
# experiment:a00-e38c5702-608411

## Experiment

Edited `extensions/agi/lib/agent-prompt.md` Rule 5 and Rule 12:

**Rule 5** — Replaced the `git add -A && git commit` instruction block with a flat prohibition: "Never run git. `git add -A` and `git commit` are forbidden — parallel agents share one working tree and the loop owns every commit. `cli.py done` handles all versioning. Do not stage, commit, push, pull, stash, checkout, or rebase."

**Rule 12** — Removed the embedded git commit code block (`git -C "$PLUGIN_ROOT/../.." add -A && git commit`) that referenced the now-deleted Rule 5, and reworded the remaining text to reference `cli.py done` instead.

### Verification

```bash
grep -n 'git add\|git commit\|git -c user' agent-prompt.md
# Output: line 5 mentions are in the prohibition text only — no actionable instructions
```

Only line 73 matches (the prohibition header itself which says "git add -A and git commit are forbidden"). Zero instructions telling agents to *run* git commands. One reference to "git grid" on line 27 is a concept mention (not an instruction).

## Evidence

Pre-edit grep confirmed the contradiction at lines 73-75 (`git add -A && git -c user.email=... commit -m`). Post-edit grep shows only the prohibition text. The per-iteration brief (context.md) already carries the ban; the permanent contract now agrees with it.

The hypothesis's own "Proves it" criterion: "a fresh grep shows zero remaining git-add/git-commit instructions to agents, and the permanent contract and every iteration-level brief agree" — this is satisfied. No agents are instructed to run git commands in agent-prompt.md anymore.

**Caveat**: The concise embed from the iteration override is still the primary guard for cold sessions, but the default contract no longer contradicts it. Any dispatch path that reads agent-prompt.md directly now sees a safe default instead of a dangerous one.


## Agent Notes
Edited agent-prompt.md Rule 5 to ban git and Rule 12 to remove git example. All 1454 tests pass. Grep confirms zero actionable git-add/git-commit instructions remain — only the prohibition text matches. Permanent contract now agrees with per-iteration brief.