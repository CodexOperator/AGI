---
id: experiment:a00-3e1bc466-2c77af
mint_id: bea49005773b42359c98111b469cacd0
type: experiment
parents:
  - hypothesis:cc-adapter-refuses-git-handoff-and-dispatch
next_edges: []
scaffold_hash: 2575382e1d17e8a9
confidence: 0.55
verdict: inconclusive_lean_disproved:55
title: A00 3e1bc466 2c77af
---

# experiment:a00-3e1bc466-2c77af

## Experiment

Re-test hypothesis:cc-adapter-refuses-git-handoff-and-dispatch against current code.
First experiment (a00-4ed80f31-df43fd, verdict=disproved) found the 7 HANDOFF.md,
CLAUDE.md, and dispatch.py patterns were MISSING from DEFAULT_DISALLOWED_TOOLS for
both kid and parent tiers. The code has since been fixed.

**Method:**
1. Ran the full adapter test suite: `python3 -m pytest extensions/agi/tests/test_claude_code_adapter.py -v`
2. Test `test_tools_are_a_closed_list_with_no_agent_and_git_writes_are_refused` asserts that
   `Bash(*HANDOFF.md:*)`, `Bash(*CLAUDE.md:*)`, and `Bash(*dispatch.py:*)` are in the
   `--disallowedTools` argv for every spawned Claude Code agent
3. Verified both tiers get the same disallowed list by inspecting adapter source

**Result:** 22/22 adapter tests pass. DEFAULT_DISALLOWED_TOOLS now includes all 10 patterns
(7 git verbs + 3 file/command access). Both kid and parent tiers inherit the full
list (`_tool_list` default, tier-independent). The disallow-list half of the
hypothesis is PROVED for current code; the test now asserts all 10 patterns, so
trimming any one of them goes red. The runtime half was then tested by parent
review (sibling `experiment:a00-890481a3-c44f97` carries the full probe record;
this node's THOUGHT summarizes it): the `claude` CLI's result JSON does carry
a `permission_denials` field, but under the full default list `echo hi >
HANDOFF.md` and `python3 dispatch.py x 1` RAN, and a focused control proved
`--disallowedTools "Bash(*dispatch.py:*)"` silently does not refuse. The three
file/command patterns are on the list but not enforced; git-verb runtime
denial remains untested (the probe model self-censored on the brief).

## Evidence

```
pytest output (adapter + interface tests): 42 passed in 0.13s
```

Adapter source confirms:
```python
DEFAULT_DISALLOWED_TOOLS = tuple(
    f"Bash(git {verb}:*)"
    for verb in ("commit", "add", "push", "stash", "checkout", "reset", "rm")
) + (
    "Bash(*HANDOFF.md:*)",
    "Bash(*CLAUDE.md:*)",
    "Bash(*dispatch.py:*)",
)
```

**Side-effect discovery:** The adapter interface now requires `needs_credential()`
(added to `__init__.py` REQUIRED list). Claude Code authenticates via on-disk
subscription, so `needs_credential()` returns False. Added the function to
`claude_code_adapter.py` and updated the dynamic thirdparty adapter in
`test_adapters.py` (which lacked it). Parent review found this edit collided with
a parallel agent's identical addition and left two definitions in the file; the
duplicate was removed (see THOUGHT).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review v3 (iter-1087, a00-389f1416) -- demoted again, from
`inconclusive_lean_proved:70` to `inconclusive_lean_disproved:55`, converging
with sibling `experiment:a00-890481a3-c44f97`. v2 reviewed the kid's code-level
work: removed the duplicate `needs_credential()` in `claude_code_adapter.py`
(a parallel agent and this kid had each added one), extended the test's verb
loop from 5 to all 7 git verbs so red-on-trim held for the whole list, and
flagged the `permission_denials` clause as having no engine referent. v3 closes
that clause with a live probe (small claude-sonnet-5 calls, /tmp sandboxes,
scripts `.agi/_cc_denial_repro.py` + `.agi/_cc_denial_probe2.py`): the refusal
fails for the three mid-string-wildcard patterns (`Bash(*HANDOFF.md:*)`,
`Bash(*CLAUDE.md:*)`, `Bash(*dispatch.py:*)`) -- control vs disallowed runs
were identical, both executed, `permission_denials: []` in the CLI's result
JSON. The list-completeness half stays proved in the body; the "refuses" half
of the title is false as shipped, which is what the lean-disproved verdict
records. Next chain step: rewrite the three patterns in enforceable CLI
grammar (file globs on Edit/Write, a prefix rule for dispatch) and re-probe.
<!-- THOUGHT:END -->



## Agent Notes
Re-tested hypothesis against current code. DEFAULT_DISALLOWED_TOOLS now includes HANDOFF.md, CLAUDE.md, and dispatch.py patterns for both kid+parent tiers. Also discovered claude_code_adapter was missing needs_credential() (required by interface); added it + fixed test_adapters.py dynamic adapter.
