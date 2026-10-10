---
id: goal:g4.6.1
mint_id: 80ab597b92c74704b9397d0406345f54
type: goal
parents:
  - goal:g4.6
  - build:bin-adapters-claude-code-adapter
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G4.6.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 7f54b26dddca4a46
season: 2
seeds: []
status: complete
tags:
  - goal
  - g4
  - adapter
  - claude-code
title: "G4.6.1: the claude-code adapter deny rules match -- no rule mixes * with the :* prefix form"
town: core
---
# goal:g4.6.1

# goal:g4.6.1

## Why this exists
goal:g4.6 (one spawn path; a harness is an adapter named in config) is the parent because the defect is inside that adapter: `DEFAULT_DISALLOWED_TOOLS` in `extensions/agi/bin/adapters/claude_code_adapter.py:108-116` and `DISPATCH_RULE` (:127) spell three deny rules as `Bash(*HANDOFF.md:*)`, `Bash(*CLAUDE.md:*)`, `Bash(*dispatch.py:*)`. MEASURED 2026-09-30 01:1xZ by belam-S2-L5-XIX: a headless `claude -p` built from `_resolved_tools(role="kid")` (PASS B3 override smoke test) printed, for each of the three, "mixes * with the trailing :* prefix syntax, so it is matched as a literal prefix (the * is not expanded) and will likely never match". So every claude-code kid could run dispatch.py and write HANDOFF.md / CLAUDE.md through Bash, though the tests assert the rules are present (they checked the string, never the match).
build:bin-adapters-claude-code-adapter is the second parent: the file this leaf versions (`[build, goal]` shape).

## Target end-state
- The three rules are spelled in the form Claude Code expands (`Bash(*HANDOFF.md*)`, `Bash(*CLAUDE.md*)`, `Bash(*dispatch.py*)`); a headless `claude -p` built from the kid tool list prints no "will likely never match" line.
- No deny rule the adapter emits mixes a `*` with the trailing `:*` prefix form; a test asserts it over every default list.

## Invariants
- The git-verb rules `Bash(git <verb>:*)` stay as they are (pure prefix form, they match).
- The privileged seats (advisor tier 3, director tier 1) still drop exactly the dispatch rule and nothing else.

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_claude_code_adapter.py -q` passes, including the no-mixed-glob test.
2. Negative: `git grep -nE 'Bash\(\*[^)]*:\*\)' -- extensions/agi/bin` has zero hits.

## Out of scope
goal:g4.6 (the adapter seam itself) · the headless claude-code stage executor in workflow.py (PASS B3 residue, routed separately).

## OWNER 2026-09-30 01:1xZ, verbatim
"You may fill in a gap yourself with a node version plus an idea node as parent of its quick like this" · "Or a goal node rather than" · "So goal sub ode or subside plus idea" · "All S goals should have been retired in favor of nested sub sub goals or whatever that fit under the umbrella goals."

## Agent Notes
Assigned to **belam**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
complete at mint+15 min: falsifier 1 = test_claude_code_adapter.py 47 passed (4 new parametrized no-mixed-glob cases); falsifier 2 = git grep for Bash(*...:*) under extensions/agi: 0 hits; live: a headless kid was denied dispatch.py --help with 0 never-match warnings.
<!-- THOUGHT:END -->
