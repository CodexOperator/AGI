---
id: experiment:cold-seat-brief-five-routes-a00-2438baed
mint_id: f2ebb7b2973f4dd49f357af25af3ea06
type: experiment
parents:
  - hypothesis:a00-2438baed-6bd901
next_edges: []
confidence: 0.95
edited_by: a00-2438baed
evidence_runs:
  - experiment:cold-seat-brief-five-routes-a00-2438baed
line_ceiling: 40
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 13
profile: balanced
role: kid
scaffold_hash: 6882cbfa57063011
season: 2
testable_claim: agent-prompt.md section names the five routes each beside its seam, and no sixth route row
title: Universal cold-seat brief lists five pane-facing routes with seams
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:cold-seat-brief-five-routes-a00-2438baed

## Experiment

Built the universal-surface listing and its scoped falsifier.

- Inserted `## The five pane-facing routes` into
  `extensions/agi/lib/agent-prompt.md`, lines 66-77 (table rows 70-74).
- Added `extensions/agi/tests/test_agent_prompt_routes.py`: a section-scoped
  parse from the heading to the next `\n## `; it asserts exactly five numbered
  route rows and each route name beside its engine seam. Env override
  `COLD_SEAT_BRIEF_PATH` (deliberately NOT `AGI_`-prefixed) points it at a
  broken copy for the non-vacuity check.
- Wire note: `dispatch.py:821` sets `skill_prompt` to
  `PLUGIN_ROOT/lib/agent-prompt.md`; it is passed into a seat's argv at
  `dispatch.py:1306` / `:2529`, so the changed bytes reach every pi cold seat.

## Evidence

Green run:

```
$ python3 -m pytest extensions/agi/tests/test_agent_prompt_routes.py -q
6 passed in 7.63s        # exit 0
```

Non-vacuous negative — same file with the `send` row deleted (scratch
`broken-agent-prompt.md`, diff `75d74 < | 3 | send | `send.py` |`):

```
$ COLD_SEAT_BRIEF_PATH=$PWD/.agi/sessions/iter-DH.152/a00-2438baed/broken-agent-prompt.md \
    python3 -m pytest extensions/agi/tests/test_agent_prompt_routes.py -q
FAILED ...::test_section_present_with_exactly_five_route_rows
FAILED ...::test_route_name_and_seam_in_section[send-seams3]
2 failed, 4 passed in 6.32s   # exit 1
```

`AGI_COLD_SEAT_BRIEF_PATH` was tried FIRST and proved VACUOUS: the parent
`extensions/agi/conftest.py` `_agi_env_stripped` session-autouse fixture
deletes every `AGI_*` key before collection, so the broken copy was never read
and the run still passed 6/6. The override is now `COLD_SEAT_BRIEF_PATH`.

Director surfaces re-read on this tip (`grep -n`):

```
extensions/agi/briefs/director-belam-duties.md:14:routes: write·read·send·dispatch/workflow·rotate/spawn
.agi/nodes/doc/unified-director-brief.md:36:routes write·read·send·dispatch/workflow·rotate/spawn
.agi/nodes/doc/director-grok-internals.md:152:routes: write.py · read · send · dispatch/workflow · rotate/spawn
```

Drift recorded (deliberate old→new, NOT normalized):
`director-grok-internals.md:152` writes the CLI spelling `write.py` where the
route name is `write`. Route names are contract; `.py` spellings are seams:
`write` → `write.py` is the deliberate alias. The first two briefs already use
the bare names.

No sixth route — special-case grep returns nothing:

```
$ grep -n grok extensions/agi/bin/dispatch.py extensions/agi/bin/rotate.py
(no output; grep exit 1)
```

Production lines: 13 added to `extensions/agi/lib/agent-prompt.md`
(`git diff --numstat` → `13 0`), ceiling 40.

## Agent Notes
agent-prompt.md (dispatch skill_prompt) gains a scoped five-route+seam section; new test passes, broken-copy run fails exit 1; no sixth grok route
