---
id: experiment:a00-19ba3ede-a4ce5b
mint_id: 41d2fba08401468da802a19ac99aa9f4
type: experiment
parents:
  - hypothesis:harness-arg-builders-are-templates-only
next_edges: []
confidence: 0.9
edited_by: a00-04243a3a
evidence_runs:
  - experiment:a00-19ba3ede-a4ce5b
line_ceiling: 110
loop: hypothesis:harness-arg-builders-are-templates-only@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe-04.py: load the PRE-CHANGE claude_code_adapter.py and copilot_cli_adapter.py from git 2bfeb12fa as separate modules, run old.build_command vs new over 7 claude cases (output_format, budget, mcp str/list, extra_args, role) + 3 copilot cases, same brief.assemble inputs", "expected": "both dispatch adapters' new template argv byte-identical to the old inline argv", "observed": "10 cases, 0 mismatches; e.g. claude ['claude','-p','--model','m','--output-format','stream-json','--verbose','--strict-mcp-config','--max-budget-usd','2.5','--append-system-prompt-file',...,'--foo','--add-dir'; copilot [bin,'--model','m','--allow-all','--remote','-p',<brief>]", "result": "HELD -- both dispatch-path argv builders are now template-rendered with no byte drift (independent of the kid's own 84-case matrix)"}
  - {"conjunct": 1, "class": "wire", "cmd": "sentinel probe: patch claude_code_adapter.harness_template.render and copilot_cli_adapter.harness_template.render to a sentinel, call each build_command, read the (harness_id, shape) the sentinel saw", "expected": "both builds must reach harness_template.render with shape='dispatch'", "observed": "both returned ['SENTINEL']; render saw ('claude-code','dispatch') and ('copilot-cli','dispatch')", "result": "HELD -- the call sites reach the changed template bytes live, selecting the dispatch shape"}
  - {"conjunct": 2, "class": "gate", "cmd": "render('claude-code', shape='nope', ...) must raise; and render the dispatch shape with every variadic list EMPTY (mcp/tools/allowed/disallowed) to see whether a value-less flag leaks", "expected": "unknown shape is a named error (no silent fallback to the default argv); an empty variadic list emits NEITHER the flag nor a value, or the next positional is swallowed", "observed": "raised HarnessTemplateError \"claude-code: no shape 'nope'; known: ['dispatch']\"; empty lists produced ['claude','-p','--model','m','--output-format','json','--strict-mcp-config','--append-system-prompt-file','PF','--add-dir','R','--','CL'] with no bare --mcp-config/--tools", "result": "HELD -- the shape selector fails closed by name and the variadic flag is skipped cleanly when empty"}
  - {"conjunct": 3, "class": "gate", "cmd": "rotate._known_harnesses() + _validate_harness with the new shape machinery present; a synthetic fourth harness builds its own argv (kid 2's probe, still applied)", "expected": "adding shapes/vocabulary must not regress the fourth-harness property or rotate's refusals", "observed": "rotate still builds a templated harness's own argv and refuses a template-less id by name; the shape additions are additive template data, not a rotate.py branch", "result": "HELD -- conjunct 3 (no rotate.py edit for a fourth harness) is intact after kid 4"}
production_lines: 128
profile: balanced
role: kid
scaffold_hash: c7395522d314dd6e
season: 2
title: claude-code and copilot-cli dispatch argv render from template shapes
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-19ba3ede-a4ce5b

## Experiment

Migrated BOTH remaining dispatch-path argv builders to template data, so no
spawn argv is built inline in an adapter body:

- `extensions/agi/templates/harness/copilot-cli.toml` — new `[shapes.dispatch]`:
  `{spread=model_args} --allow-all --remote {spread=extra_args} -p <prompt>`.
- `extensions/agi/templates/harness/claude-code.toml` — new `[shapes.dispatch]`,
  the whole variadic block in template order: `-p`, model_args, `--output-format`,
  conditional `--verbose`, `--strict-mcp-config`, `--max-budget-usd`,
  `--append-system-prompt-file`, extra_args, `--add-dir`, `--mcp-config`,
  `--tools`, `--allowedTools`, `--disallowedTools`, `--`, closing turn.
- `extensions/agi/bin/harness_template.py` — two vocabulary additions, both
  declarative: `{flag, spread}` (a variadic flag whose values are a caller
  list; empty list emits NEITHER token) and `{const, when}` (a const emitted
  only when a named slot is truthy). Plus `render(..., shape=name)` selecting
  an optional `[shapes.<name>]` argv; an unknown shape is a NAMED error. The
  closed-key refusal still holds and now covers shape argv too.
- `claude_code_adapter.build_command` / `copilot_cli_adapter.build_command`
  now call `harness_template.render(NAME, shape="dispatch", ...)` and only
  fill slots. `model_args()` is untouched (dispatch/heal import it).
  `dispatch.py`'s call site is untouched.

**DATA DECISION — `shape` inside one template file, not a second file per
harness.** One binary genuinely has two invocation shapes here (`-i` seat vs
`-p` dispatch; `--remote-control` seat vs `-p` dispatch), and the shapes not
about WHICH binary — a second `.toml` would mean a second "harness id"
(`copilot-cli-dispatch`) that `available()`/`_validate_harness` would then
have to tolerate as if it were a harness. Keeping both shapes side by side in
one file also lets a reader see that they differ in one token (copilot) or in
the whole head/tail (claude). The alternative, a harness-name branch in code,
was never on the table. pi is unchanged: it has one shape, so its top-level
`argv` is its dispatch argv (`rotate = false` already says so).

Named thin hooks (no scripting escape hatch was added; a template is still
data):

- `claude_code_adapter._mcp_values(harness)` — flattens `mcp_config`
  (str | list) to the `--mcp-config` VALUES; the flag is in the template.
- `harness_template._emit` — `{flag, spread}` + skip-when-empty, which is what
  makes `--tools T...` expressible with the flag in DATA and the dynamic list
  in the caller.
- The `--` closing turn needs NO hook: `"--"` literal + `{slot="closing"}`.

## Evidence

Byte-identity probe — PRE-CHANGE adapter bodies loaded from`git show
HEAD:` (HEAD = `2bfeb12fa`) as separate modules, compared against the NEW
rendered argv with the SAME `brief.assemble()` inputs:

    python3 .agi/sessions/iter-DH.01/a00-19ba3ede/probe/byte_identity.py
    claude: 78/78 byte-identical
    copilot: 6/6 byte-identical
    TOTAL MISMATCHES: 0

claude matrix: output_format {absent, stream-json, json, text} x budget
{absent, 10, "20.5"} x mcp {absent, "srv.json", ["a.json","b.json"]} x
extra_args {[], [--foo bar]} = 72, plus tools{default, [Read], []},
disallowed_tools=[], settings="ultracode", settings={"director":...},
output_format="bogus" (ValueError on both sides). copilot matrix: tier
kid/parent, effort absent/str/per-tier-map, extra_args absent/present, no
models block. Two sample argv:

    claude -p --model claude-sonnet-5 --output-format stream-json --verbose
      --strict-mcp-config --max-budget-usd 5
      --append-system-prompt-file <sess>/system-prompt.md --foo bar
      --add-dir <repo> --tools Bash Read Edit Write Glob Grep
      --allowedTools ... --disallowedTools ... -- <closing>

    /x/copilot --model auto --effort high --allow-all --remote --foo -p <brief>

One live bug the probe caught in the first draft: `{flag, spread}` emitted a
value-less flag for an empty list, so `--mcp-config` appeared with no value
and swallowed `--tools`. Fixed to emit neither; `--tools`/`--allowedTools`/
`--disallowedTools`/`--mcp-config` absent cases are now exact.

Tests (named, run):

    PYTHONPATH=/tmp/pytestenv python3 -m pytest \
      extensions/agi/tests/test_claude_code_adapter.py \
      extensions/agi/tests/test_copilot_cli_adapter.py \
      extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_brief.py \
      extensions/agi/tests/test_harness_template.py \
      extensions/agi/tests/test_harness_dispatch_shapes.py \
      extensions/agi/tests/test_rotate_templates.py \
      extensions/agi/tests/test_rotate_copilot_harness.py -q
    431 passed

New: `extensions/agi/tests/test_harness_dispatch_shapes.py` (13 tests) freezes
the OLD inline shapes as literals, checks empty variadic lists emit no flag,
checks an unknown shape and a bad shape key are NAMED errors, checks both
adapters actually reach `render(shape="dispatch")` (sentinel probe), and
greps both builder bodies for leftover flag literals.

Which argv producers remain inline (grep of `extensions/agi/bin/`):

- `*_adapter.model_args()` in pi/claude-code/copilot — flag STRING derivers
  feeding render slots (`--provider/--model/--thinking/--effort/--settings`).
  They are the deliberate exception (dispatch/heal import them); no spawn argv
  is built from them without passing through a template.
- `pi_adapter._append_prompt_args` and `pi_adapter._wrap_trajectory` — the two
  named hooks kid 3 landed; still the only pi flag construction.
- `rotate.py` builds NO harness argv itself: seat argv renders through
  `harness_template.render` (`_build_claude_command`, `_build_copilot_command`,
  `_build_harness_command`, `_successor_command`).
- No other `.py` in `bin/` contains a harness flag literal.

Budget: `production_lines: 128` against `line_ceiling: 110` (added lines over
the production paths per `git diff --numstat`; 24 of the claude template's are
the argv itself). Under the 2x stop (220) and both halves landed, so this is a
recorded overage rather than a re-brief: the round was budgeted for 110 but the
second vocabulary pair (`when`, `flag+spread`) and the shape selector are what
made the claude variadic head expressible without a scripting hatch.

## Agent Notes
claude-code and copilot-cli dispatch argv now render from [shapes.dispatch] template shapes; pre-change bodies loaded from git HEAD byte-match 84/84 probe cases, 431 named tests pass; model_args() remains the sanctioned flag-string deriver, production_lines 128 vs ceiling 110.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-04243a3a, DH.01): ACCEPTED at inconclusive_lean_proved:90; four parent-run probes recorded in frontmatter `probes`, none refuted the kid. The decisive one is independent of the kid's own 84-case matrix: I loaded the PRE-CHANGE claude_code_adapter.py and copilot_cli_adapter.py from git 2bfeb12fa as separate modules and byte-compared old vs new build_command over 10 cases -- 0 mismatches. A sentinel probe shows both adapters reach harness_template.render with shape="dispatch"; an unknown shape raises by name; and an empty variadic list emits neither flag nor value (the bug the kid found in its own first draft, now fixed and probed). CAVEATS recorded, not demoted: (1) production_lines=128 against line_ceiling=110 -- under the 2x stop and recorded, but another overage; I raised the ceiling for this round and it still ran 16% over, which is a signal that two thick adapters were more than one budget. (2) `model_args()` in all three adapters remains a Python flag-STRING deriver that constructs --provider/--model/--thinking/--effort/--settings and splices them via `{spread="model_args"}` or feeds render slots; so "argv produced ONLY from a template" is true of the SHAPE while the model flags still come from a named hook. I judge that inside the hypothesis's explicit "optional thin adapter hook" allowance, but it is the honest boundary a strict reader will push on. (3) claude/copilot use the spread-hook for model flags while pi uses provider/model/thinking SLOTS -- an inconsistency the next round could unify. This review is the parent's; the kid's authored body remains.
<!-- THOUGHT:END -->
