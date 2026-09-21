---
id: experiment:a00-f5950c0a-999cc8
mint_id: c636c28f13ca433dbe78c35d1b8d118e
type: experiment
parents:
  - hypothesis:a00-c89eaaae-7dcb85
next_edges: []
edited_by: season.py
scaffold_hash: c267c2a97c7b6bbd
season: 1
thought_session: season
title: "Grep confirmation: agent-prompt.md Rule 5 still carries git commit instruction"
---
# experiment:a00-f5950c0a-999cc8

## Experiment

**What I did:** Grepped `extensions/agi/lib/agent-prompt.md` for git-add/commit instructions to verify the hypothesis claim that Rule 5 still tells agents to `git add -A && commit`.

**Command:** `grep -n 'git add\|git commit\|git -c\|COMMIT YOUR WORK\|Commit your work' extensions/agi/lib/agent-prompt.md`

**Result:** Exact match found at lines 73–75:

```
73:5. **Commit your work.** Before signaling done, run:
75:   git add -A && git -c user.email=auto@autoresearch -c user.name=autoresearch \
```

**What this proves:** The hypothesis's factual premise is confirmed — `agent-prompt.md` Rule 5 still instructs agents to `git add -A && commit`, which is the exact whole-tree `git commit -A` pattern that caused the 2026-08-31 incident. The contradiction between this and the per-iteration brief's git ban (from `brief.py`) is live and unresolved. The claim that "the ban only holds because every iteration override wins" is structurally supported by this evidence: the default contract still mandates the forbidden action, so any dispatch path that fails to inject the override would produce an agent that follows the unsafe rule.

## Evidence

Raw grep output with line numbers:
```
$ grep -n 'git add\|git commit\|git -c\|COMMIT YOUR WORK\|Commit your work' /home/ubuntu/work/agi/extensions/agi/lib/agent-prompt.md
73:5. **Commit your work.** Before signaling done, run:
75:   git add -A && git -c user.email=auto@autoresearch -c user.name=autoresearch \
```

Confirmed on 2026-09-04. The text reads verbatim as the hypothesis described.



## Agent Notes
Grepped agent-prompt.md — found git add -A && commit instruction at lines 73-75, confirming hypothesis's factual premise. The default contract still mandates the forbidden action. Any dispatch path failing to inject the per-iteration override would produce an agent that follows the unsafe rule.