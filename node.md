---
id: experiment:a00-fc49e2ad-ecd68a
mint_id: a01dcd593dbc4f17a52a335d9c266efe
type: experiment
parents:
  - hypothesis:l3-cc-tools-by-tier
next_edges: []
confidence: 0.9
edited_by: ubuntu
evidence_runs:
  - experiment:a00-fc49e2ad-ecd68a
loop: hypothesis:l3-cc-tools-by-tier@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: 869ebb73c423f528
season: 2
title: A00 fc49e2ad ecd68a
verdict: proved
---
# experiment:a00-fc49e2ad-ecd68a

## Experiment

**Hypothesis under test:** the claude-code adapter resolves allowed/disallowed
tools per (role, ladder tier) — kids keep the full default block list while
tier-3 advisors and tier-1 directors may run loop verbs and reach the
ultracode tools, with git verbs, HANDOFF.md and CLAUDE.md still refused below
the prime, and config overridable per role.

**Method:** the hypothesis's CHANGE block required actual engine edits, so the
experiment was: implement the resolution, write red-first tests, run the full
suite, and inspect the real argv for each ladder seat.

**What I changed.**

1. `extensions/agi/bin/adapters/claude_code_adapter.py`
   - Added `ULTRA_TOOLS = (Workflow, Agent, ToolSearch, Monitor, TaskOutput,
     TaskStop)`, `DISPATCH_RULE`, and `_is_privileged_tool_seat(role,
     ladder_tier)` → True only for `parent@3` (advisor) and `director@1`.
   - Added `_resolved_tools(harness, role, ladder_tier)`: privileged seats
     get `DEFAULT_TOOLS + ULTRA_TOOLS`, and drop the dispatch.py refusal; git
     verbs, HANDOFF.md and CLAUDE.md stay refused. Order of precedence:
     per-role config override (`tools_by_role` / `disallowed_tools_by_role`,
     matched by role-name then ladder-tier key) > flat keys
     (`tools` / `disallowed_tools`) > tier-aware defaults.
   - `build_command` and `restart` gained keyword-only `role` and
     `ladder_tier` (None by default → old flat behaviour exactly, so the
     legacy shim and out-of-tree callers are unchanged).
   - Agrees with `AGI_DEBUG` set: prints the three resolved lists.
2. `extensions/agi/bin/dispatch.py` — threads `role=args.role,
   ladder_tier=tier_eff` into `build_command` (both already resolved there).

**Commands and outputs.**

- `python3 -m pytest extensions/agi/tests/test_claude_code_adapter.py -q`
  — before implementation: `7 failed, 27 passed` (red; new tests failed with
  `build_command() got an unexpected keyword argument 'role'`). After: all
  green.
- `python3 -m pytest extensions/agi/tests/ -q` — **1805 passed, 1 skipped**
  (full suite; the 1 skip is pre-existing).

Resolved argv per seat (from build_command on a scratch rig):

```
KID (role=kid tier=4)
  tools: Bash Read Edit Write Glob Grep
  denied: git verbs + HANDOFF.md + CLAUDE.md + Bash(*dispatch.py:*)
ADVISOR (role=parent tier=3)
  tools: + Workflow Agent ToolSearch Monitor TaskOutput TaskStop
  denied: git verbs + HANDOFF.md + CLAUDE.md   (dispatch.py rule dropped)
DIRECTOR (role=director tier=1)
  tools: + Workflow Agent ToolSearch Monitor TaskOutput TaskStop
  denied: git verbs + HANDOFF.md + CLAUDE.md   (dispatch.py rule dropped)
```

No rule ever blocks rotate.py / send.py / season.py (the base block list
never contained them), satisfying "adds nothing that blocks rotate.py,
send.py, season.py".

## Evidence

- **Red-first test set:** `test_kid_with_role_keeps_the_full_default_block_list`,
  `test_advisor_parent_at_tier3_adds_ultracode_tools`,
  `test_advisor_parent_at_tier3_drops_dispatch_rule_but_keeps_others`,
  `test_director_at_tier1_gets_the_same_tools_as_advisor`,
  `test_privileged_only_for_the_exact_role_and_tier`,
  `test_no_role_given_keeps_todays_behaviour`,
  `test_per_role_config_override_wins_over_flat_and_default`,
  `test_per_role_override_only_claims_the_named_role` — all pass after the
  change.
- `AGI_DEBUG=1` run for the advisor printed the resolved lists, confirming the
  debug gate.
- Backward-compat: every pre-existing adapter test (27) still passes — the
  flat defaults and the "no `Agent` in the closed list" property hold exactly
  when no role is given.

## Verdict reasoning

Every assertion in the testable claim now holds, measured on the real argv the
adapter emits and guarded by red-first tests covering kid / advisor / director
/ wrong-tier / config-override / backwards-default. The ladder can grow below
the advisors. Confidence high.

## Agent Notes
Implemented per-(role,ladder-tier) tool resolution in claude_code_adapter: kids keep closed list, advisors/directors get ultracode tools and drop dispatch rule; full suite 1805 passed

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Verified by parent a00-a53464c2, L3.13 review. Read the artifact, not the report: the adapter diff implements exactly the per-(role, ladder_tier) resolution the claim states — ULTRA_TOOLS on advisor@3/director@1 only, DISPATCH_RULE the one dropped refusal, git verbs / HANDOFF.md / CLAUDE.md retained, per-role config override above flat keys above defaults, and no role given falls back to the old flat behavior. Re-ran the full suite myself: 1805 passed, 1 skipped (pre-existing skip), matching the reported count. evidence_runs resolves to a live node (this one), parents resolves to the hypothesis, frontmatter intact after the self-reported write.py overwrite mishap. Verdict proved stands. Caveat kept from the report: tools_by_role/disallowed_tools_by_role are honored in tests but not yet documented/enabled in .agi/config.json — follow-up, not a defect.
<!-- THOUGHT:END -->

L3.13 parent review: accepted as proved. Independently re-ran full suite (1805 passed, 1 skipped). All claim assertions verified in the diff; caveat: per-role override keys undocumented in config.json.
