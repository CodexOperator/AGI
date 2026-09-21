---
id: experiment:a01-329392e3-d0e462
mint_id: a74220a2d17f4baf9721de4326fb626d
type: experiment
parents:
  - hypothesis:cc-adapter-refuses-git-handoff-and-dispatch
next_edges: []
confidence: 0.85
edited_by: season.py
scaffold_hash: 818d97772fabc3de
season: 1
thought_session: season
title: A01 329392e3 d0e462
verdict: inconclusive_lean_proved:85
---
# experiment:a01-329392e3-d0e462

## Experiment

Hypothesis claims `claude_code_adapter.build_command` disallows git verbs,
HANDOFF.md/CLAUDE.md writes, dispatch.py runs, **and the test goes red when
the disallow list is trimmed** (testable_claim closing clause).

Prior experiments proved the disallow list exists (10 patterns) but only
verified the test assertions exist — nobody confirmed the test *actually
fails* when a pattern is removed.

**Method:**

1. Extracted `--disallowedTools` from `build_command()` argv for both tiers
   to verify all 10 patterns are present.
2. **Destructive test:** commented out one disallowed pattern
   (`Bash(*HANDOFF.md:*)`) from `DEFAULT_DISALLOWED_TOOLS` in
   `claude_code_adapter.py`, then ran the exact assertion test.
3. Restored file, verified full adapter suite still passes.

**Results:**

- Both `kid` and `parent` tiers emit identical 10-pattern disallow lists.
- After trimming HANDOFF.md, test **FAILED** with exact expected error:
  `AssertionError: HANDOFF.md writes must be disallowed`
- After restore, 22/22 adapter tests pass clean.

**Open clause:** `permission_denials` — the hypothesis says a spawned CC
parent "gets a permission denial recorded in permission_denials". No such
structure exists in the engine. Testing this would require spawning a live
CC session with a disallowed-tool violation and observing the CLI's native
denial behavior. That is an integration/end-to-end test, not possible in
the current unit test scope.

## Evidence

**Destructive test output:**
```
FAILED test_tools_are_a_closed_list_with_no_agent_and_git_writes_are_refused
  AssertionError: HANDOFF.md writes must be disallowed
  assert 'Bash(*HANDOFF.md:*)' in ['Bash(git commit:*)', 'Bash(git add:*)', ...]

=== destructive edit: commented out "Bash(*HANDOFF.md:*)" ===
```

**Pre-destructive argv extraction confirmed both tiers get identical 10 patterns:**
```
=== kid tier (10 patterns) ===
  Bash(git commit:*)
  Bash(git add:*)
  Bash(git push:*)
  Bash(git stash:*)
  Bash(git checkout:*)
  Bash(git reset:*)
  Bash(git rm:*)
  Bash(*HANDOFF.md:*)
  Bash(*CLAUDE.md:*)
  Bash(*dispatch.py:*)

=== parent tier (10 patterns) ===
  [identical list, same 10 entries]
```

**Post-restore: 22 passed in 0.11s**

## Agent Notes
Destructive test: trimmed HANDOFF.md from DEFAULT_DISALLOWED_TOOLS, confirmed test goes red with 'HANDOFF.md writes must be disallowed'. Both tiers get identical 10-pattern lists. Open clause: permission_denials has no code referent.