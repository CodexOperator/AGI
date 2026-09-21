---
id: experiment:a00-7bcbcf8c-b674bc
mint_id: f146d26438c045098950f2489ba864af
type: experiment
parents:
  - hypothesis:harness-arg-builders-are-templates-only
next_edges: []
confidence: 0.85
edited_by: a00-2ccfbc74
evidence_runs:
  - experiment:a00-7bcbcf8c-b674bc
line_ceiling: 40
loop: hypothesis:harness-arg-builders-are-templates-only@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe-k1.py: template_dir -> tmp with claude --debug-file and copilot --remote DELETED; build through rotate._build_claude_command/_build_copilot_command", "expected": "the frozen-literal seat assert must break when a template flag is dropped", "observed": "CONTROL real dir literal-hold True/True; MUTATED claude [claude,--remote-control,N,--permission-mode,bypassPermissions,CARD] literal-hold False; MUTATED copilot [...--allow-all,-i,CARD] literal-hold False", "result": "HELD"}
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe-k1b.py: call the KID OWN test_claude_builder_renders_frozen_argv under the same mutated template dir", "expected": "the kid test must FAIL under the mutation (proving it is not render==render)", "observed": "both cases raised AssertionError; the OLD render==render assert survives the same mutation (True)", "result": "HELD"}
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-2ccfbc74, DH.03 K1). (1) INSTRUCTION: the director-helper orders say "Fix tautological seat test". (2) MACHINE, read off the diff at 38423879f: test_harness_template.py had two asserts whose two sides WERE the same call -- test_claude_template_matches_build_claude_command compared rotate._build_claude_command(...) to harness_template.render("claude-code",...) while rotate.py:896-906 shows _build_claude_command IS that render; same for test_copilot_builder_is_now_template_backed. The kid rewrote both against hardcoded literal argv (test_claude_builder_renders_frozen_argv, test_copilot_builder_renders_frozen_argv). I ran my own probe (probe-k1.py + probe-k1b.py in the seat-director-helper session dir): with a mutated template dir that drops claude --debug-file and copilot --remote, the kid OWN test functions raise AssertionError on both cases, while the OLD render==render assert survives the same mutation (True) -- so the guard is real and the tautology is gone. Control on the real dir holds True/True. Production diff = 0 lines (test-only, as scoped). (3) NEAR MISS: a "fix" that builds the expected list by calling harness_template.render with a different spelling of the args, or that keeps a second render-equality test alongside, satisfies the words and pins nothing -- a dropped flag would still pass. The kid removed the render comparison rather than keeping it, and the mutation probe is exactly what distinguishes the two. (4) DEVIATION: none; test-file scope honoured, no loader/rotate bytes moved, so K2/K3 stay clean. VERDICT kept at inconclusive_lean_proved:85: it proves the GUARD is real, not that argv builders are template-only (the sibling experiments own that).
<!-- THOUGHT:END -->
