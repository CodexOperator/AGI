---
id: experiment:a00-3d482d17-5d7498
mint_id: a53fb60acc44425fa5c2566b9abf806a
type: experiment
parents:
  - hypothesis:harness-arg-builders-are-templates-only
next_edges: []
confidence: 0.85
edited_by: a00-04243a3a
evidence_runs:
  - experiment:a00-3d482d17-5d7498
  - experiment:a00-2a796f62-9923ec
line_ceiling: 40
loop: hypothesis:harness-arg-builders-are-templates-only@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe-03.py: load the PRE-CHANGE pi_adapter.py from git 253291bac as a separate module, run old.build_command vs new pi_adapter.build_command for an 8-case matrix (provider/model/thinking present/absent x AGI_BRIEF_PROFILE default/survival x skill present/absent), both with AGI_PI_TRAJECTORY_BYPASS=1 to compare the inner argv", "expected": "new template-rendered pi argv byte-identical to the old inline argv", "observed": "8 cases, 0 mismatches; sample head ['<pi-bin>','--provider','openrouter','--model','km','--thinking','medium','-p','--mode','json']", "result": "HELD -- pi's dispatch-path argv is produced by the template with no byte drift (independent of the kid's own frozen matrix)"}
  - {"conjunct": 1, "class": "wire", "cmd": "parent sentinel probe: patch pi_adapter.harness_template.render to a sentinel, call pi_adapter.build_command(harness={'adapter':'pi','models':{'kid':'m'}}, tier='kid', ...) and read the returned argv + the harness id the sentinel saw", "expected": "the production pi build must reach harness_template.render with harness id 'pi', wrapped by the trajectory hook", "observed": "returned ['/usr/bin/python3','.../pi_trajectory.py','--wrapper','SENTINEL','/tmp/trajectory.jsonl','--', '--append-system-prompt', ...] and the sentinel saw harness_id='pi'", "result": "HELD -- the call site reaches the changed bytes live; the wrapper is a named hook around the rendered inner argv"}
  - {"conjunct": 2, "class": "gate", "cmd": "grep -n for pi flag literals in pi_adapter.build_command; plus the sentinel argv above; plus check the only remaining flag strings are inside model_args (kept for dispatch.pi_model_args/heal.py)", "expected": "load-bearing spawn argv flags must come from pi.toml, with any remaining flag-string construction named and justified", "observed": "build_command spells no -p/--mode/--provider/--model/--thinking/--append-system-prompt itself; model_args is untouched and still returns flag STRINGS for its external caller, and _model_values converts them to render slots", "result": "HELD for build_command; model_args remains a named value-deriver outside the template, which is the honest thin-hook boundary, not a hidden inline builder"}
  - {"conjunct": 3, "class": "gate", "cmd": "available(); rotate._known_harnesses(); rotate._validate_harness(None,'pi'); rotate._validate_harness(None,'copilot-cli')", "expected": "pi's template is available to the dispatch adapter but pi.toml's rotate=false keeps pi out of the rotate seat set; rotate still refuses pi and still accepts copilot-cli", "observed": "available()=['claude-code','copilot-cli','pi']; _known_harnesses()=('claude-code','copilot-cli'); validate(None,'pi')=1; validate(None,'copilot-cli')=0", "result": "HELD -- rotate=false is a declarative template field, not a harness-name branch; adding pi.toml did not regress rotate's refusal"}
production_lines: 79
profile: balanced
role: kid
scaffold_hash: 5eb83950bcf6ad20
season: 2
title: pi argv is template-produced; the wrapper and the repeated flag are the two named hooks
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-3d482d17-5d7498

## Experiment

Claim (hypothesis:harness-arg-builders-are-templates-only): for pi, claude-code
and copilot-cli the spawn argv is produced from a template plus, at most, a
named thin hook. Kids 1 and 2 landed claude-code and copilot-cli on the
**rotate.py seat path**; this round is the third harness — **pi** — whose argv
was built inline in `extensions/agi/bin/adapters/pi_adapter.py:build_command`
(the dispatch path, not rotate.py). Per the parent's BUILD order I made the
inner pi argv data (`pi.toml`), added the two render slots it needs, and
isolated the one structure the format cannot express (the trajectory wrapper)
behind a named hook.

## What was built

1. **`extensions/agi/templates/harness/pi.toml`** (new). Expresses pi's
   headless shape as data:

   ```toml
   argv = [
     {flag = "--provider", slot = "provider"},
     {flag = "--model",    slot = "model"},
     {flag = "--thinking", slot = "thinking"},
     "-p", "--mode", "json",
     {spread = "extra_args"},
     {slot = "prompt"},
   ]
   ```

2. **`harness_template.render` gained two slots** — `provider` and `thinking`
   (the two the parent named as expected). Additive only; claude-code and
   copilot-cli templates are untouched and byte-identical (`git diff` on
   `claude-code.toml`/`copilot-cli.toml` is empty).

3. **`pi_adapter.build_command` now renders the inner argv** via
   `harness_template.render("pi", prompt=<closing line>,
   bin_path=resolve_bin(harness), extra_args=prompt_args,
   **_model_values(harness, tier))`. It no longer spells `-p`, `--mode json`,
   `--provider`, `--model`, `--thinking`, or `--append-system-prompt`. The
   ONLY remaining pi flag literals in the file are inside `model_args`, which
   is the compatibility flag-string deriver kept for `dispatch.pi_model_args`
   and `heal.py` (0 added lines there — original body untouched);
   `_model_values` parses its flag pairs into the render slots.

### The two named thin hooks

- **`_append_prompt_args(*, context_file, segs, skill_prompt)`** — the repeated,
  dynamic `--append-system-prompt <text>` list, pre-interleaved and spliced by
  `{spread = "extra_args"}`. This is the **NAMED LIMIT** of the vocabulary: an
  element emits a flag once or spreads a pre-flattened list, but cannot repeat
  a flag over a runtime-sized list. Preserved exactly: context entry omitted
  under survival, plain path (no `@`), skill entry only when it exists.
- **`_wrap_trajectory(inner, *, sess_dir)`** — the isolated
  `inner_argv -> wrapped_argv` transform
  (`python pi_trajectory.py --wrapper <bin> <traj> -- <inner[1:]>`, unless
  `AGI_PI_TRAJECTORY_BYPASS`). This is conjunct 3's structure: **no element can
  reorder an argv AROUND its bin** — every element emits tokens for the harness
  itself — so the wrapper is code, named, and the TOML vocabulary gained no
  wrapper verb.

### `rotate = false` — a declarative, not a name branch

Adding `pi.toml` to the shared template dir would otherwise make
`rotate.py::_known_harnesses() == available()` treat pi as a **rotate seat**,
whose interactive tmux argv is a different shape (name/debug-file/settings).
That would regress `test_declared_but_unbuildable_harness_refused` AND spawn a
headless one-shot as a seat. `pi.toml` therefore declares the top-level
boolean `rotate = false`, and `_known_harnesses()` filters on the template's
own data — a generic rule, no harness-name branch. rotate still refuses `pi`
(probe 3) and still builds every template that does not opt out.

## Evidence

### Byte-identity (probe `.agi/sessions/iter-DH.01/a00-3d482d17/probe-identity.py`)

The OLD inline shape is reconstructed verbatim and compared against the NEW
rendered argv **using the same `brief.assemble()` output**, so live brief
drift cannot mask a code difference. Matrix: provider/model/thinking present &
absent × `AGI_BRIEF_PROFILE` default/survival × skill present/absent ×
`AGI_PI_TRAJECTORY_BYPASS` unset/`=1`:

```
16 cases, 0 mismatches
```

Two matrix points, before == after:

```
A) provider+model+thinking, default, no skill, BYPASS=1 (inner argv)
   ['<pi-bin>', '--provider','openrouter','--model','kid-m','--thinking',
    'medium','-p','--mode','json',
    '--append-system-prompt','<ctx>', '--append-system-prompt','<seg>', ...,
    'Begin iteration 1 as agent a00-x. ...']

B) bare harness, survival, skill present, wrapper on
   ['/usr/bin/python3','<bin>/pi_trajectory.py','--wrapper','<pi-bin>',
    '<sess>/trajectory.jsonl','--','--model','kid-m','-p','--mode','json',
    '--append-system-prompt','<seg>', ...,
    '--append-system-prompt','<skill>', 'Begin iteration 1 ...']
```

### Acceptance probes (`probe-render.py`)

```
PROBE-1 sentinel argv: ['...pi_trajectory.py','--wrapper','SENTINEL','/tmp/trajectory.jsonl','--']
         | render saw harness_id: {'harness_id': 'pi'}
PROBE-2 available(): ['claude-code', 'copilot-cli', 'pi']
PROBE-3 rotate _known_harnesses(): ('claude-code', 'copilot-cli')
PROBE-3 _validate_harness(None,'pi') rc: 1
PROBE-3 _validate_harness(None,'copilot-cli') rc: 0
PROBE-3 pi.toml raw: False
```

### Tests

New (in `test_harness_template.py`, tests excluded from the line ceiling):
`test_pi_template_renders_the_flag_shape`,
`test_pi_adapter_production_path_reaches_render`,
`test_pi_template_is_dispatch_only_not_a_rotate_seat`.

```
$ PYTHONPATH=/tmp/pytestenv python3 -m pytest \
    extensions/agi/tests/test_adapters.py extensions/agi/tests/test_brief.py \
    extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_pi_trajectory.py -q
328 passed

$ ... test_harness_template.py test_rotate_copilot_harness.py \
      test_pi_edit_forgiveness.py test_claude_code_adapter.py \
      test_copilot_cli_adapter.py -q
101 passed, 1 skipped

$ ... test_rotate.py -q        # first run: 1 flaky order failure
328 passed                   # isolated: passed; full rerun: 328 passed

$ ... test_adapters.py test_harness_template.py test_rotate_copilot_harness.py \
      test_edit_tool_forgiveness.py test_dispatch_scaffold_unregistered.py -q
76 passed, 1 skipped
```

## Which harnesses are template-produced now

| Harness | Path | argv from template? |
|---|---|---|
| claude-code | rotate.py seat (`_build_claude_command`) | **yes** (kid 2) |
| copilot-cli | rotate.py seat (`_build_copilot_command`) | **yes** (kid 1/2) |
| pi | `pi_adapter.build_command` (dispatch) | **yes** (this round) |

Still building argv inline, measured not guessed (grep of flag literals):
`claude_code_adapter.build_command` (8+ `args += ["--..."]`) and
`copilot_cli_adapter.build_command` — the **dispatch-path** twins of the
rotate seat harnesses. Not migrated this round, per the parent's instruction;
recorded as the next step.

## Falsifier verdict

All three harnesses named in the hypothesis now have their argv rendered from
a template: pi's production build reaches `harness_template.render` (sentinel,
harness id `pi`), its inner argv is byte-identical across a 16-case matrix, and
the one structure the format cannot express (the command wrapper) is isolated
behind a named hook rather than smuggled in as a verb. The two dispatch-path
`*_adapter.build_command` bodies still build argv inline, so the hypothesis is
a strong lean, not proved.

Production lines: **79** (pi_adapter 58, harness_template 4, rotate 4, pi.toml
13), ceiling 40 — landed and recorded, not a halt (below the 2x=80 stop).

## Agent Notes
pi's inner argv is now rendered from templates/harness/pi.toml: added provider+thinking render slots, pi_adapter.build_command renders the template with a pre-interleaved --append-system-prompt list (named hook _append_prompt_args, the vocabulary's one NAMED LIMIT) and the trajectory command-wrapper isolated as named hook _wrap_trajectory. Byte-identity proven on a 16-case matrix (provider/model/thinking x survival x skill x trajectory-bypass, old inline shape reconstructed and compared using the SAME brief.assemble output): 0 mismatches. Sentinel probe: pi build reaches render with harness id pi. pi.toml declares rotate=false so rotate.py still refuses pi as a seat (generic data filter, no name branch). All three named harnesses are template-produced on their production paths; claude_code_adapter and copilot_cli_adapter (dispatch-path twins) still build argv inline -- not migrated, the next step, so lean not proved. 79 production lines, ceiling 40 (under 2x=80).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-04243a3a, DH.01): ACCEPTED at inconclusive_lean_proved:85; none of the kid's claims survived-unrefuted across four parent-run probes (recorded in frontmatter `probes`). The strongest is independent of the kid's own evidence: I loaded the PRE-CHANGE pi_adapter.py straight out of git 253291bac as a separate module and byte-compared old vs new build_command over an 8-case matrix -- 0 mismatches. A sentinel probe shows pi build_command actually reaches harness_template.render with harness_id "pi". The `rotate = false` opt-out is a declarative template field, so `pi.toml` joining the shared dir does not smuggle pi into the rotate seat set: _known_harnesses() is (claude-code,copilot-cli) and _validate_harness(None,pi) still refuses. CAVEAT recorded rather than demoted: production_lines=79 against line_ceiling=40 (under the 2x=80 stop, and the kid recorded it, but this round was ~2x its declared budget -- the parent had not raised the ceiling for a three-file migration). Also: model_args remains a flag-STRING deriver for dispatch.pi_model_args/heal.py, so "pi flag construction" is not literally zero in the adapter -- it is a named value-deriver feeding render slots, which I judge inside the "thin hook" allowance but which a stricter reader could count. The kid's own table naming claude_code_adapter/copilot_cli_adapter as still-inline is honest; that gap is the round-4 target.
<!-- THOUGHT:END -->
