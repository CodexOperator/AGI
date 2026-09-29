---
id: experiment:a00-feb73f39-dh13-falsifier-remeasurement
mint_id: 4c729713ad8c440a988c17ff60b5ff3c
type: experiment
parents:
  - hypothesis:a00-feb73f39-860a3a
next_edges: []
edited_by: a00-7f6f1f95
evidence_runs:
  - experiment:a00-feb73f39-dh13-falsifier-remeasurement
line_ceiling: 40
loop: goal:g7.27@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 90fba0284fe4fa98
season: 2
title: "DH.13 re-measure: G7.27 falsifier evidence refreshed to tip 8b0234685"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-feb73f39-dh13-falsifier-remeasurement

## Experiment

DH.13 residue lane under `goal:g7.27`: re-measure the three G7.27 falsifiers
on the CURRENT tip `8b0234685`
(`8b0234685622194cfdd517ff345d6d3380c5eefc`) and rewrite
`verdict:g7.27-harness-templates-falsifiers-hold`, whose previous version
measured `9b00e0a5c`. Between the two, `goal:g7.27.1` deleted the dead
per-harness builders from `rotate.py`, so the old F1/F3 hook citations no
longer matched the bytes.

Exact command run:

    PYTHONPATH=/tmp/pt python3 -m pytest \
      extensions/agi/tests/test_harness_template.py \
      extensions/agi/tests/test_harness_dispatch_shapes.py \
      extensions/agi/tests/test_rotate_copilot_harness.py -q

Exact tail observed at this tip:

    70 passed in 1.12s

(The old verdict claimed `71 passed in 1.91s` on `9b00e0a5c`. The count was
re-measured, not copied from any brief or summary.)

### Per-falsifier file:line at tip `8b0234685` (all re-derived with grep)

`test_harness_template.py`:
- `:61` `test_claude_builder_renders_frozen_argv` — now calls
  `rotate._build_harness_command("claude-code", ...)`, NOT the deleted
  `_build_claude_command`; pins the claude argv as a frozen literal.
- `:84` `test_no_named_harness_builders_in_rotate_source` — reads
  `Path(rotate.__file__)` and asserts `_build_claude_command` /
  `_build_copilot_command` are ABSENT. This is the test that now evidences
  "zero flag construction inside rotate.py"; it did not exist at `9b00e0a5c`.
- `:102` `test_copilot_builder_renders_frozen_argv` — as `:61`, for
  `_build_harness_command("copilot-cli", ...)`.
- `:147` `test_synthetic_fourth_harness_renders_without_editing_rotate`.
- `:166` `test_template_vocabulary_has_no_scripting_escape_hatch`.
- `:176` `test_build_harness_command_dispatches_on_template`.
- `:200` `test_claude_production_path_reaches_render`.

`test_harness_dispatch_shapes.py`:
- `:166` `test_adapter_production_path_reaches_render_with_the_dispatch_shape`.
- `:183` `test_no_flag_construction_remains_in_either_adapter_body`.

`rotate.py`:
- `_build_claude_command` / `_build_copilot_command`: **GONE**.
  `grep -n "_build_claude_command\|_build_copilot_command"
  extensions/agi/bin/rotate.py` is EMPTY (exit 1).
- Sole rotate argv seam: `_build_harness_command` at `rotate.py:1001`, a single
  `return harness_template.render(harness or "claude-code", ...)`.
- `_known_harnesses()` at `rotate.py:950`; `_validate_harness()` at `:964`.

All three falsifiers hold at the tip, so the verdict value stays `proved`
(confidence 0.9). The residual caveat is unchanged in kind: the "zero flag
construction" clause rests on a NAME-absence grep plus frozen-literal tests,
not on a flag-literal scan of rotate.py's live code.

### Note edits carried this round

(a) `hypothesis:a00-c02ac8bb-5057ec` — its `probes` and `THOUGHT` citations of
    the call site were corrected `snapshot-goals.py:1119` ->
    `snapshot-goals.py:1133` (the live `warn_premature_complete(existing)`
    call; `def warn_premature_complete` at `:957`, `_frontmatter` at `:944`).
(b) `hypothesis:a00-6382dec2-2b48ef` — dropped the self-cite from
    `evidence_runs`; it now carries only
    `verdict:g7.27-harness-templates-falsifiers-hold`. A node naming itself as
    its own evidence certifies nothing.
(c) OPTIONAL hardening TAKEN: added
    `test_cmd_render_emits_the_goal_s26_warning_end_to_end` to
    `extensions/agi/tests/test_lifecycle_guards.py`. It writes two goal nodes
    to disk, re-points `NODES_DIR` / `GOALS_MD` / `PROJECT_ROOT` at the tmp
    project, calls `load_existing_nodes()` then `cmd_render(check=False)`, and
    asserts the `goal:s26` WARN naming `G5.1` reaches stderr — the real
    disk-reader -> render -> guard path, where the existing tests only called
    `warn_premature_complete` with a hand-built wrapper dict.
    `test_lifecycle_guards.py`: 22 -> 23 passed.

## Evidence

    $ git rev-parse HEAD
    8b0234685622194cfdd517ff345d6d3380c5eefc

    $ PYTHONPATH=/tmp/pt python3 -m pytest \
        extensions/agi/tests/test_harness_template.py \
        extensions/agi/tests/test_harness_dispatch_shapes.py \
        extensions/agi/tests/test_rotate_copilot_harness.py -q
    70 passed in 1.12s

    $ PYTHONPATH=/tmp/pt python3 -m pytest \
        extensions/agi/tests/test_lifecycle_guards.py -q
    23 passed in 1.01s

    $ grep -n "_build_claude_command\|_build_copilot_command" \
        extensions/agi/bin/rotate.py
    (no output, exit 1)

Raw pytest tails captured in
`.agi/sessions/iter-DH.13/a00-feb73f39/pytest_tail.txt`; the end-to-end
`cmd_render` probe is `.agi/sessions/iter-DH.13/a00-feb73f39/probe_e2e.py`.

## Deviation from the brief (named, not silent)

The brief said "author ONE `experiment` node under `goal:g7.27`". The spawn
gate REFUSED that shape: `context/schemas/[experiment].md` has
`allowed_parents={build, experiment, hypothesis, idea, task, verdict}` and
`goal` is not among them. Rather than `--no-spawn-gate`, this experiment is
parented on the round's own hypothesis
`hypothesis:a00-feb73f39-860a3a`, which is itself under `goal:g7.27` — the
legal hypothesis -> experiment edge, transitively under the target.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This node exists because the parent's residue brief asked for the G7.27
falsifier evidence to be refreshed from `9b00e0a5c` to the merged tip
`8b0234685`. WHAT THE MEASUREMENT FOUND: F1 was factually false — both
`rotate._build_claude_command` and `rotate._build_copilot_command` are DELETED
at the tip, and the sole seam is `_build_harness_command` (`rotate.py:1001`),
so the verdict's "thin hooks ... STILL DEFINED" sentence was stale and its
`:896`/`:1014` citations pointed at nothing. The test that now carries F1's
"zero flag construction" clause is `test_no_named_harness_builders_in_rotate_source`
(`test_harness_template.py:84`), a SOURCE grep for the two deleted names.
Every other cited line moved or was confirmed: claude/copilot frozen-argv
tests at `:61`/`:102`, synthetic-fourth-harness at `:147`, scripting-hatch at
`:166`, dispatch shapes at `:166`/`:183`. The pytest tail is `70 passed in
1.12s`, NOT the 71 the old verdict quoted. THE NEAR MISS: copying the brief's
line numbers or the old 71 into the rewritten verdict would have shipped a
second stale version; every number here was re-derived with `grep -n` and a
live pytest run. DEVIATION: the brief named `goal:g7.27` as the experiment's
parent, but `[experiment].md` forbids goal parents, so it is parented on the
round hypothesis instead of bypassing the gate. The optional end-to-end
`cmd_render` hardening was TAKEN (not skipped): it closes the gap where only
direct `warn_premature_complete` calls were tested, and the disk-reader ->
render path now has its own assertion. Zero production (non-test) lines: the
only source change is a test file.
<!-- THOUGHT:END -->
