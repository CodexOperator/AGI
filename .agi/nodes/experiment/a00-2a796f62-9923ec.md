---
id: experiment:a00-2a796f62-9923ec
mint_id: 1fb5e742a5e7446a90ac2fde16541970
type: experiment
parents:
  - hypothesis:harness-arg-builders-are-templates-only
next_edges: []
confidence: 0.8
edited_by: a00-04243a3a
evidence_runs:
  - experiment:a00-2a796f62-9923ec
line_ceiling: 40
loop: hypothesis:harness-arg-builders-are-templates-only@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 probe-02.py PROBE-1: patch BOTH agi.bin.harness_template.render and rotate.harness_template.render to a sentinel; call rotate._build_harness_command(None,...), rotate._build_claude_command(...), rotate._build_harness_command('copilot-cli',...)", "expected": "claude-code and copilot-cli production builds must reach harness_template.render; pi, named in the claim, must have a template", "observed": "all three calls returned ['SENTINEL']; render was called with ('claude-code',...) twice and ('copilot-cli',...) once; available() == ['claude-code','copilot-cli'] -- pi has NO template", "result": "HELD for claude-code and copilot-cli (rotate build path is template-driven); conjunct 1 remains OPEN for pi"}
  - {"conjunct": 2, "class": "gate", "cmd": "grep -n -- '--remote-control|--permission-mode|--debug-file|--allow-all|--settings|--append-system-prompt' extensions/agi/bin/rotate.py", "expected": "zero harness argv-construction hits in rotate.py outside comments/help", "observed": "remaining hits are the module docstring usage block (L11/28/29), a README comment (L139/152), argparse help (L20364/20939/21019/...), the console `--settings` argument, a settings-mismatch guard (L1906) and a copilot help-string (L20952) -- no inline argv construction", "result": "HELD -- no harness flag is constructed inline in rotate.py"}
  - {"conjunct": 3, "class": "gate", "cmd": "python3 probe-02.py PROBE-3: fake-harness.toml in a tmp dir + patch template_dir; rotate._validate_harness(None,'fake-harness'); rotate._build_harness_command('fake-harness',...); and _build_harness_command('no-such-harness',...)", "expected": "a fourth harness with a template BUILDS from that template; an unknown id raises by name, never a silent claude argv", "observed": "validate=0; build returned ['fakebin','--fake','CARD']; unknown id raised UnknownHarnessError naming the template dir", "result": "HELD -- separate test now asserts the BUILT argv, not just validate's return code; the silent-claude hole kid 1 left is closed"}
production_lines: 23
profile: balanced
role: kid
scaffold_hash: 864d9fe1ac5b46bf
season: 2
title: rotate argv is template-dispatched, claude-code migrated, silent-claude hole closed
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-2a796f62-9923ec

Claim (hypothesis:harness-arg-builders-are-templates-only): every harness's
rotate.py spawn argv comes from a template plus a thin hook, with no harness
flag construction and no harness-name branch left in the build path. This round
is the BUILD order the parent (`a00-04243a3a`) cut after kid 1's round was
demoted: make the dispatcher template-generic, migrate claude-code's production
path, and close the silent-claude hole.

## What was built

1. `_build_harness_command` now renders `harness_template.render(harness or
   "claude-code", ...)` for EVERY harness. The `if harness == "copilot-cli"`
   branch is gone. A harness id with no template raises
   `UnknownHarnessError` (named), never a silent claude argv.
2. `_build_claude_command` is now a thin hook: it calls `render("claude-code",
   ...)`. Its six-positional-arg signature and output are unchanged.
3. `rotate.py` no longer constructs any harness flag inline. The only
   remaining hits for `--remote-control / --permission-mode / --allow-all` are
   comments and help text (`grep -n`, below).
4. The `_bin` resolution and the config-row model/effort/settings resolution
   branches were generalised from the literal `harness == "copilot-cli"` to
   `harness and harness != "claude-code"`, so a fourth harness reads ITS OWN
   `config.json` row (bin, models, effort) rather than borrowing claude's.

## Acceptance probes (measured)

`git diff --numstat -- extensions/agi/bin/rotate.py` = **23 added, 31 removed**
(production_lines 23, ceiling 40).

Byte-identity, claude-code (probe `.agi/sessions/iter-DH.01/a00-2a796f62/
probe-argv.py`, old hand-built shape reconstructed literally and compared):

```
claude m1 e1 {'a':1} MATCH ['claude','--remote-control','N',
  '--permission-mode','bypassPermissions','--debug-file','D.LOG',
  '--model','m1','--effort','e1','--settings','{"a": 1}','CARD']
claude None None None MATCH ['claude','--remote-control','N',
  '--permission-mode','bypassPermissions','--debug-file','D.LOG','CARD']
```

copilot-cli dry-run argv (unchanged from kid 1's migration):

```
['/x/copilot','--model','auto','--allow-all','--remote','-i','CARD']
```

Sentinel probe (the parent's acceptance): monkeypatch
`rotate.harness_template.render` to return `['SENTINEL']`; calling
`_build_harness_command(None, name='N', prompt_text='C', debug_file='D')`
returns `['SENTINEL']` and the sentinel saw `harness_id == 'claude-code'`. The
claude production path reaches the template.

Silent-claude hole CLOSED: a synthetic `fake-harness.toml` (bin `fakebin`,
`--tier <model>`, `--static`, prompt) now BUILDS through
`_build_harness_command`:
`['fakebin','--tier','strong','--static','CARD']` — not claude. The new test
asserts the BUILT argv, not `_validate_harness`'s return code (that gap is what
let kid 1's conjunct 3 be falsely claimed).

## Tests

```
$ PYTHONPATH=/tmp/pytestenv python3 -m pytest \
    extensions/agi/tests/test_harness_template.py \
    extensions/agi/tests/test_rotate_copilot_harness.py \
    extensions/agi/tests/test_claude_code_adapter.py -q
74 passed

$ PYTHONPATH=/tmp/pytestenv python3 -m pytest \
    extensions/agi/tests/test_rotate.py \
    test_rotate_copilot_harness.py test_harness_template.py \
    test_copilot_cli_adapter.py test_claude_code_adapter.py -q
423 passed
```

Added three tests to `test_harness_template.py`: built-argv dispatch for a
fourth harness, unknown-id refusal (no claude fallback), and the
claude-reaches-render sentinel.

## pi assessment (measured by reading, not guessed)

pi's argv is built in `extensions/agi/bin/adapters/pi_adapter.py`
(`build_command`, dispatch path — not rotate.py). Its shape:

```
[bin, (--provider P)?, (--model M)?, (--thinking T)?, -p, --mode, json,
 (--append-system-prompt <context_file>)?,
 (--append-system-prompt <seg>)* , (--append-system-prompt <skill>)?,
 <closing_line>]
```

wrapped, unless `AGI_PI_TRAJECTORY_BYPASS=1`, by
`[python, pi_trajectory.py, --wrapper, <bin>, <traj>, --, *inner_argv[1:]]`.

Finding: the closed vocabulary CAN express the FLAG SHAPE, with two named
limits, and CANNOT express the wrapper.

- `-p` and `--mode json` are expressible as two `const` entries.
- `--append-system-prompt <seg>` repeated over a DYNAMIC list is expressible
  only by pre-interleaving the list into `extra_args` and using
  `spread = "extra_args"`, which pushes a little argv knowledge back into the
  adapter (the design's tolerated "thin hook").
- `--provider` and `--thinking` have NO render slot: `harness_template.render`
  accepts `prompt/model/effort/bin_path/settings/extra_args/name/debug_file`
  only. Expressing pi needs two new slots (a thin addition to the loader, not
  a scripting escape hatch).
- **Not expressible: the trajectory wrapper.** Every template emits the harness
  bin as the FIRST token; there is no element that wraps or reorders an argv
  *around* its bin (`python <wrapper> --wrapper <bin> <traj> -- <args[1:]>`).
  That is a command WRAPPER, not a flag, and it is the named thin hook
  candidate: `wrap_argv(inner: list[str], *, bin, traj) -> list[str]` in the pi
  adapter, consuming the rendered inner argv. Adding a wrapper verb to the TOML
  vocabulary is exactly the scripting escape hatch the format forbids.

pi migration was NOT attempted this round: it touches the dispatch-path adapter
(`pi_adapter.py`) and two new render slots, which would exceed the 40-line
ceiling. It is recorded here as the round-3 first step.

## Falsifier verdict

After this round: conjunct 1 (only copilot) is now measured true for BOTH
claude-code and copilot-cli — the claude production build reaches
`harness_template.render`, proven by the sentinel; conjunct 2 (fourth harness
needs no rotate.py argv edit) is measured true by the synthetic-harness
built-argv test; conjunct 3 (no silent claude fallback) is measured true — an
unknown id raises, a templated id builds its own argv. The pi conjunct is still
open, so the hypothesis is a strong lean, not proved.

## Agent Notes
Made rotate.py's build path template-generic: _build_harness_command renders harness_template.render(harness or claude-code) for every harness (no if harness==... branch), _build_claude_command is a thin render('claude-code') hook, _bin and config-row resolution generalised off the literal copilot name. Proven on built bytes: claude dry-run argv byte-identical to the old hand-built shape; copilot unchanged; a synthetic fake-harness BUILDS ['fakebin','--tier','strong','--static','CARD'] (silent-claude hole closed); monkeypatch render -> sentinel and the claude path returns it. 74 targeted + 423 rotate tests pass. pi assessed but NOT migrated: its flag shape is expressible (two new render slots, pre-interleaved extra_args) but its trajectory wrapper [python pi_trajectory.py --wrapper <bin> <traj> -- <args[1:]>] is not -- named thin hook candidate; left for round 3, so lean not proved. 23 production lines, ceiling 40.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-04243a3a, DH.01): ACCEPTED, verdict unchanged at inconclusive_lean_proved:80 -- none of the kid's claims could be refuted. Three parent-run negative probes recorded in frontmatter `probes`: (1) wire -- patching BOTH module objects (rotate.py does a bare `import harness_template`, so patching only agi.bin.harness_template would have produced a false negative; this is the trap kid 1's PROBE-2 hit) shows claude-code and copilot-cli builds both return the sentinel, i.e. the production path reaches render; (2) gate -- grep of rotate.py shows no inline harness flag construction outside docstrings/argparse; (3) gate -- a synthetic fourth harness validates AND builds its own argv, and an unknown id raises UnknownHarnessError instead of silently building claude. The kid's own node is honest: it declares pi still open and scopes its claim to rotate.py. The `_bin` generalisation (all harnesses now read their own config row bin) is a small behaviour widening -- this repo's claude-code.bin is None so claude stays byte-identical, but a downstream config that sets a claude bin would now have it honoured where the old code ignored it; recorded as a caveat, not a refutation. This review is the parent's; the kid's authored body remains.
<!-- THOUGHT:END -->
