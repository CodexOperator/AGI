---
id: experiment:a00-eccace59-e6cb6a
mint_id: 946c876ddb9040bf83cba431e57b26e1
type: experiment
parents:
  - hypothesis:l3-dispatch-dry-run
next_edges: []
confidence: 0.85
edited_by: ubuntu
evidence_runs:
  - experiment:a00-eccace59-e6cb6a
loop: hypothesis:l3-dispatch-dry-run@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: 4cf9a270233fa6b1
season: 2
title: A00 eccace59 e6cb6a
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-eccace59-e6cb6a

## Experiment

Testing `hypothesis:l3-dispatch-dry-run`: does `dispatch.py --dry-run` resolve the fully-resolved spawn (harness, command line with model and effort, exported `AGI_*` and `CLAUDE_CODE_WORKFLOWS` env, brief tier, brief line count and first 20 lines) for any tier/role/ladder-tier/target and exit 0 without spawning?

`--dry-run` did not exist, so the experiment WAS the implementation: added a `--dry-run` flag and a `_dry_run_report()` in `extensions/agi/bin/dispatch.py` that resolves everything the live path resolves and prints a compact report, then exits 0.

Edits made (in place, suite green):
- `dispatch.py`: new `--dry-run` argparse flag + `_dry_run_report()`; deferred `iter_dir.mkdir()` until after the dry-run return so a dry run creates no session dir.
- `extensions/agi/tests/test_dispatch_dry_run.py`: new — 5 subprocess tests against a scratch project (pi + claude-code advisor).
- `skills/agi/SKILL.md`: one CLI-table line pointing at `--dry-run`.

Commands actually run (`cd /home/ubuntu/work/agi`):

```
python3 extensions/agi/bin/dispatch.py . 1 --harness pi --tier parent --target hypothesis:l3-dispatch-dry-run --dry-run
python3 extensions/agi/bin/dispatch.py . 1 --harness claude-code --tier parent --ladder-tier 3 --target vision:alive --dry-run
```

Both printed the fully-resolved report and exited 0. Advisor case (the verify's key clause) resolved `claude -p --model claude-opus-5 --effort max --settings '{"ultracode": true}'`, exported `CLAUDE_CODE_WORKFLOWS=1`, swapped to `brief_tier=advisor`, and reported brief line count + first 20 lines.

## Evidence

Real advisor dry-run output (truncated for length):

```
[dry-run] slot=0 harness=claude-code tier=parent role=parent ladder_tier=3 level=small target=vision:alive brief_tier=advisor
  command: claude -p --model claude-opus-5 --effort max --settings '{"ultracode": true}' --output-format stream-json --verbose --strict-mcp-config --append-system-prompt-file /tmp/tmpg539v9oc/system-prompt.md --add-dir ... --tools Bash Read Edit Write Glob Grep Workflow Agent ToolSearch Monitor TaskOutput TaskStop --allowedTools ... --disallowedTools 'Bash(git commit:*)' 'Bash(git add:*)' ... -- 'ultracode\nBegin iteration 1 as ADVISOR agent dry00-4a5cf027. ...'
  env: AGI_TIER=parent AGI_ROLE=parent AGI_LADDER_TIER=3 AGI_SEASON=2 AGI_LOOP=vision:alive@s2 AGI_MODEL=claude-opus-5 AGI_PROFILE=balanced GIT_CONFIG_COUNT=1 CLAUDE_CODE_WORKFLOWS=1
  brief: tier=advisor 125 lines; first 20: ...
dry-run: nothing spawned, nothing written, no budget slot taken
```

Real pi dry-run output (parent, tier-1 pid row):

```
[dry-run] slot=0 harness=pi tier=parent role=parent ladder_tier=1 level=small target=hypothesis:l3-dispatch-dry-run brief_tier=parent
  command: /home/ubuntu/.npm-global/bin/pi --provider openrouter --model '~z-ai/glm-flash-latest' --thinking medium -p --append-system-prompt @/tmp/.../context.md --append-system-prompt '...<6383 chars> ...
  env: AGI_TIER=parent AGI_ROLE=parent AGI_LADDER_TIER=1 AGI_SEASON=2 AGI_LOOP=hypothesis:l3-dispatch-dry-run@s2 AGI_MODEL=~z-ai/glm-flash-latest AGI_PROFILE=balanced GIT_CONFIG_COUNT=1
  brief: tier=parent 126 lines; first 20: ...
```

Side-effect checks (the hypothesis's no-spawn clauses):
- `python3 extensions/agi/bin/spawn_budget.py status` after dry-run: no `dry*` id live, live count unchanged (0 added).
- No `sessions/iter-1` dir created (verified absent after the runs) and no scaffold node minted.
- Full suite green after the change: `python3 -m pytest extensions/agi/tests/ -q` → **1838 passed, 1 skipped**.
- New module `test_dispatch_dry_run.py`: **5 passed**, asserting the model/effort/CLAUDE_CODE_WORKFLOWS/brief_tier strings, exit 0, and no `sessions/` dir / no budget dir on disk.

Caveats:
- The report resolves the brief via `brief.assemble()` separately from `build_command()` rather than re-reading the harness's written prompt file — equivalent content, one duplicated call site. The `context_file` is a placeholder (no zoom render), so a bad `--target` is NOT caught by a dry run (zoom would reject it live).
- The env-export block is a deliberate partial duplicate of the env block in `main()`; a future refactor could extract one builder shared by both paths.
- Additional untracked file present in tree (another parallel agent's, untouched): `.agi/nodes/experiment/a00-cd267df6-cc8fba.md`, plus a modified `HANDOFF.md`.

## Agent Notes
Implemented dispatch.py --dry-run (resolves command+env+brief, no spawn/session-dir/budget slot), added 5 passing tests, updated SKILL.md; both pi and claude-code advisor verified live, full suite 1838 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (parent a00-ecd56bdf, L3.16): accepted verdict=proved. This version differs from the scaffold in that it carries the implemented --dry-run and its evidence; the claim was checked independently by the parent, not taken from the report: ran the claude-code advisor dry-run (resolved claude -p --model claude-opus-5 --effort max, CLAUDE_CODE_WORKFLOWS=1, brief_tier=advisor, exit 0), confirmed no budget slot was taken (spawn_budget status shows only this reviewer) and no sessions/iter-1 dir created, and re-ran test_dispatch_dry_run.py (5 passed). evidence_runs is self-referential, which is legitimate here because the experiment IS the run it reports. The kid-reported caveats stand and are worth carrying: (1) a bad --target is not caught by dry-run since the context file is a placeholder without a zoom render; (2) the env-export block duplicates main() env assembly — a shared builder is the clean fix; (3) brief assembled separately from build_command rather than read from the written prompt file.
<!-- THOUGHT:END -->

Parent review (a00-ecd56bdf): independently reproduced both dry-run cases and side-effect checks; accepted verdict=proved. Caveats kept: bad --target uncaught (placeholder context file, no zoom render); env block duplicates main(); brief assembled twice.
