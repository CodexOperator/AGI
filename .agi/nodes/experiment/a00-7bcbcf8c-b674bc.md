---
id: experiment:a00-7bcbcf8c-b674bc
mint_id: f146d26438c045098950f2489ba864af
type: experiment
parents:
  - hypothesis:harness-arg-builders-are-templates-only
next_edges: []
confidence: 0.85
edited_by: a00-7bcbcf8c
evidence_runs:
  - experiment:a00-7bcbcf8c-b674bc
line_ceiling: 40
loop: hypothesis:harness-arg-builders-are-templates-only@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: f52f2ea8ac8e2386
season: 2
title: Seat builders pinned to a frozen literal argv, killing the render==render tautology
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-7bcbcf8c-b674bc

## Experiment

Killed the tautological seat test. `test_harness_template.py` compared the
production builders to `harness_template.render` — but `rotate._build_claude_command`
(rotate.py:896) and `rotate._build_copilot_command` (rotate.py:973) ARE exactly
that render call, so both asserts were `render(...) == render(...)` and could
never fail. A mutation of `claude-code.toml` would have sailed through them.

Rewrote both against a FROZEN LITERAL argv — the old hand-built shape read from
`git show 8b6dcea1f:extensions/agi/bin/rotate.py`:

- `test_claude_builder_renders_frozen_argv` (was `..._matches_build_claude_command`)
  now asserts `_build_claude_command("N","CARD","D.LOG", ...)` == a literal
  `["claude","--remote-control","N","--permission-mode","bypassPermissions",
  "--debug-file","D.LOG", (--model m), (--effort e), (--settings <json>),
  "CARD"]` across the 5 CLAUDE_MATRIX cases.
- `test_copilot_builder_renders_frozen_argv` (was
  `test_copilot_builder_is_now_template_backed`) now asserts
  `_build_copilot_command(...)` == the same literal shape frozen in
  `test_copilot_template_renders_frozen_argv`, across all 6 COPILOT_MATRIX cases.

Scope: `extensions/agi/tests/test_harness_template.py` only. Production diff
(`git diff --numstat` excluding tests) = **0 lines**. Test diff = 39 added /
18 removed.

## Evidence

Green suite:
```
$ PYTHONPATH=/tmp/pytestenv python3.12 -m pytest extensions/agi/tests/test_harness_template.py -q
...........................                                              [100%]
27 passed in 0.30s
```

MUTATION CHECK (claude): copy `claude-code.toml` to a tmp dir with the
`--debug-file` argv entry deleted, monkeypatch both `template_dir` references,
run the new test — it must FAIL:
```
5 failed, 22 deselected in 0.27s
FAILED ...::test_claude_builder_renders_frozen_argv[None-None-None]
FAILED ...::test_claude_builder_renders_frozen_argv[m1-None-None]
FAILED ...::test_claude_builder_renders_frozen_argv[None-e1-None]
FAILED ...::test_claude_builder_renders_frozen_argv[m1-e1-settings3]
FAILED ...::test_claude_builder_renders_frozen_argv[m1-e1-ultracode]
  At index 5 diff: '--model' != '--debug-file'
```

MUTATION CHECK (copilot): drop `--remote` from `copilot-cli.toml` — the new test
FAILS all 6 cases:
```
6 failed, 21 deselected in 0.24s
FAILED ...::test_copilot_builder_renders_frozen_argv[None-None-extra0] ... (all 6)
```

CONTROL — the OLD tautology survives the same claude mutation, proving it
measured nothing:
```
old tautology survives mutation: True
  got: ['claude', '--remote-control', 'N', '--permission-mode', 'bypassPermissions', 'CARD']
```

Probe files: `.agi/sessions/iter-DH.03/a00-7bcbcf8c/{mutplug,mutplug2}.py`,
`claude-code.mutated.toml`, `copilot-cli.mutated.toml`, `{green,mutation,
mutation_copilot}.txt`. Real templates untouched.

## Verdict rationale

This proves the GUARD is real — the seat argv is now pinned by a literal that a
dropped/renamed template flag breaks. It does NOT prove the parent hypothesis
(the builders being template-only), which was measured by the sibling
experiments. Hence `inconclusive_lean_proved:85`.

## Agent Notes
Rewrote both tautological seat tests to compare production builders to a frozen literal argv (old hand-built shape at 8b6dcea1f); mutation of claude --debug-file and copilot --remote each make the new tests fail, while the old render==render tautology survives mutation. 27 passed; production diff 0 lines.
