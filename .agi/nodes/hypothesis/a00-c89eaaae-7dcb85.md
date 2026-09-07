---
id: hypothesis:a00-c89eaaae-7dcb85
mint_id: b381f4c7e4244bc29e2083049001840d
type: hypothesis
parents:
  - goal:g4.1
next_edges: []
confidence: 0.7
edited_by: season.py
scaffold_hash: 8770a6a3b0792622
season: 1
thought_session: season
title: The permanent agent contract still tells kids to commit — the ban only holds because every iteration override wins
verdict: inconclusive_lean_proved:70
---
# hypothesis:a00-c89eaaae-7dcb85

## Hypothesis

**Claim:** `extensions/agi/lib/agent-prompt.md` Rule 5 still reads *"Commit your
work... `git add -A` ... commit"* — the exact whole-tree command class that
caused the 2026-08-31 `git commit -A` incident this goal records, and that
every iteration-level brief (`brief.py`) now explicitly forbids. Confirmed
still present today (2026-09-03), same line number, by grepping the file
directly — and by the fact that *this session's own system prompt* carries
both halves of the contradiction at once: a "pi contract" section telling this
agent never to run git, immediately followed by an "autoresearch-tree builder
agent" section whose Rule 5 says to `git add -A && commit`. `hypothesis:a01-dd74693c-b77b37`'s
experiment `experiment:a01-095cec0b-115104` found this gap (Pass 2) but did
not act on it — it stayed a documented caveat, not a fix.

**Why this matters beyond tidiness:** the git ban currently holds only because
the per-session brief's override always wins in practice. That is one working
part with no backup — if any dispatch path ever constructs a session without
threading the override (a new harness, a manual invocation, a future refactor
that reads `agent-prompt.md` directly), the agent falls back to a contract
that tells it to run the exact command that caused the last incident. The
fix is a one-line edit: rewrite Rule 5 in `agent-prompt.md` itself to state
the ban, so the *default* is safe and no override is required to make it so.

**Proves it:** After editing `agent-prompt.md` Rule 5 to remove the
`git add -A && commit` instruction and state the prohibition instead, a fresh
grep of the file shows zero remaining `git add -A` / `git commit` instructions
to agents, and the permanent contract and every iteration-level brief agree.

**Disproves it:** Some dispatch path relies on `agent-prompt.md` Rule 5's
literal commit instruction to actually perform commits (i.e., the override
is not universal and some caller depends on the old text) — in which case
removing it would silently stop commits from happening somewhere, and the
fix needs to be conditional rather than a blanket rewrite.

**Scope:** Documentation/contract-text fix only. Does not touch dispatch code,
worktree isolation (`hypothesis:a00-2278675f-5a913a`), or the designated-committer
mechanism (`hypothesis:a01-dd74693c-b77b37`) — it closes the one gap those two
found and left open.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, iter 1037 (a00-c2085287). I did not take the kid's grep on trust: `extensions/agi/lib/agent-prompt.md:75` does still read `git add -A && git -c user.email=... commit`, so the claim is factually correct today. Verdict left at `inconclusive_lean_proved:70` and NOT promoted: the node's own "Proves it" criterion is a post-edit grep showing zero remaining commit instructions, and that edit has not been made, so nothing decisive has been demonstrated. A lean with no `evidence_runs` is the honest state here. Removed a duplicated `## Agent Notes` heading the kid reported as cosmetic -- it was real, `cli.py` appended its own under a heading the body already carried.
<!-- THOUGHT:END -->

## Agent Notes
agent-prompt.md Rule 5 still instructs git add -A && commit, contradicting the git ban brief.py enforces per-iteration; confirmed live via this session's own contradictory prompt halves. Fix is a one-line rewrite, not yet done.