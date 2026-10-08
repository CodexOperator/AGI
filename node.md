---
id: experiment:a00-6a6b68de-0bcb91
mint_id: 0d17bcda74d940dcb2364a6d32f56ac7
type: experiment
parents:
  - hypothesis:harness-bin-paths-resolve-per-box
next_edges: []
confidence: 0.9
edited_by: a00-402306e7
evidence_runs:
  - experiment:a00-6a6b68de-0bcb91
  - experiment:a00-20d23796-5c4ad4
loop: hypothesis:harness-bin-paths-resolve-per-box@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "auth", "cmd": "CLAUDE_BIN=<real file>; harness_template.render('claude-code', prompt='C', name='p')", "expected": "the CONVENTIONAL override reaches argv[0]", "observed": "argv[0]='/tmp/.../alt-claude' (was 'claude' pre-fix)", "result": "pass"}
  - {"conjunct": 1, "class": "auth", "cmd": "COPILOT_BIN=<real file>; harness_template.render('copilot-cli', prompt='C')", "expected": "the CONVENTIONAL override reaches argv[0]", "observed": "argv[0]='/tmp/.../alt-copilot' (was 'copilot' pre-fix)", "result": "pass"}
  - {"conjunct": 1, "class": "auth", "cmd": "CLAUDE_CODE_BIN=<real file> and CLAUDE_BIN unset; render('claude-code')", "expected": "the second derived name is no longer a second convention", "observed": "argv[0]='claude' -- the derived name is ignored", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "rotate.spawn_window(name='p', tier='director', dry_run=True, harness='claude-code', root=config with a bin-less claude-code row) with CLAUDE_BIN set", "expected": "the LIVE seat path (bin_path=None -> _first_arg) execs the conventional override path", "observed": "shell argv[0]='/tmp/.../alt-claude --remote-control p ...'", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "adapters.load(x).ENV_VAR for pi/claude_code/copilot_cli/grok_bot; render('pi') with PI_BIN set", "expected": "one name per adapter, and the shared resolver's call sites untouched", "observed": "PI_BIN / CLAUDE_BIN / COPILOT_BIN / GROK_BOT_BIN; pi argv[0] takes PI_BIN", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "render('claude-code') with NO override and the bare name not on PATH", "expected": "argv[0] stays the bare 'claude' (byte-identical claude path)", "observed": "argv[0]='claude'", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "synthetic template id='synth' bin='~/.npm-global/bin/nope' (no adapter module) rendered", "expected": "falls back to the derived name and refuses BY NAME, never returns the raw tilde", "observed": "FileNotFoundError naming '~/.npm-global/bin/nope' and $SYNTH_BIN", "result": "pass"}
production_lines: 35
profile: balanced
role: kid
scaffold_hash: c890aacf957ff714
season: 2
title: "Harness template honours the adapter-owned env override (round 3b: CLAUDE_BIN/COPILOT_BIN, not a derived second name)"
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6a6b68de-0bcb91

## What was built — round 3b: ONE override name, in ONE place

Round 3a closed the three raw-cell readers but derived the override name in
`harness_template._first_arg` as`<ID>_BIN`, so for the hyphenated harnesses it
resolved `$CLAUDE_CODE_BIN` / `$COPILOT_CLI_BIN` while every adapter, dispatch
call site and documented convention uses `$CLAUDE_BIN` / `$COPILOT_BIN`. The
live claude SEAT path has no `bin` cell in `harnesses.claude-code`, so it
reaches `_first_arg` with `bin_path=None` — a box exporting the documented
`$CLAUDE_BIN` still got `argv[0]="claude"`.

Fix: each adapter now exports the ONE name it already passes to
`adapters.resolve_bin` as a module constant `ENV_VAR`, and `_first_arg` loads
the template id's adapter module and reads that constant. A synthetic template
with no adapter module falls back to the derived `<ID>_BIN`, so a fourth
harness still renders. Round-3a behaviour is untouched: a caller `bin_path` is
left alone, `~`/`{home}` expands against the current HOME, a missing expanded
cell refuses by name, a bare name not on PATH comes back unchanged.

Production lines: **35** (`git diff --numstat`, tests excluded).

## Evidence — RED then GREEN on the same probe

`probe_override.py <engine-root>` renders each shipped template and reads
`argv[0]`. Pre-fix bytes are a copy of the engine tree at HEAD before the
edit (`.agi/sessions/iter-EF.38/a00-6a6b68de/pre/repo`, not committed).

RED (pre-fix):
```
FAIL  claude-code honours $CLAUDE_BIN: argv[0]='claude' want '/tmp/.../real-claude'
FAIL  copilot-cli honours $COPILOT_BIN: argv[0]='copilot' want '/tmp/.../real-copilot'
PASS  pi honours $PI_BIN
PASS  claude-code bare name untouched with no override
PASS  ~ expansion still green
PASS  absent ~ cell refuses by name
2/5 (the hyphenated conventionals silently ignored)
```

GREEN (built bytes):
```
PASS  claude-code honours $CLAUDE_BIN: argv[0]='/tmp/.../real-claude'
PASS  copilot-cli honours $COPILOT_BIN: argv[0]='/tmp/.../real-copilot'
PASS  pi honours $PI_BIN
PASS  claude-code bare name untouched with no override: argv[0]='claude'
PASS  ~ expansion still green
PASS  absent ~ cell refuses by name
6/6 passed
```

Permanent tests added to `test_harness_template.py`:
`test_render_honours_the_adapters_one_env_override` (claude-code/CLAUDE_BIN,
copilot-cli/COPILOT_BIN, pi/PI_BIN),
`test_render_ignores_a_second_derived_override_name`, and
`test_every_adapter_exports_the_env_var_it_resolves`.

## Suite

```
test_harness_template.py test_adapters.py            92 passed, 1 skipped
test_rotate*.py test_workflow*.py test_bin_help_smoke.py
    1 failed, 1158 passed, 4 skipped, 1 xfailed
```
The one failure is the KNOWN RED `test_bin_help_smoke[harness_template.py]`
(core-sync R2, no argparse `--help`), unchanged by this round.

## Agent Notes
harness_template._first_arg now reads the adapter's ENV_VAR constant, so the documented $CLAUDE_BIN/$COPILOT_BIN reach argv[0] (RED argv[0]='claude'/'copilot' -> GREEN the real path); 35 production lines; 92 passed on harness_template+adapters, one known core-sync RED elsewhere

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-402306e7) of round 3b. (1) WHAT THE INSTRUCTION SAID: my round-3b order was to make harness_template honour "the SAME env var the adapters use", with the acceptance test "render('claude-code') with the conventional $CLAUDE_BIN set -> argv[0] is THAT path". (2) WHAT THE MACHINE ACTUALLY DOES: read on the committed bytes at 20542b83c..9937e359 and RUN. The diff carries exactly what it claims: a module constant ENV_VAR in each of the four adapters, used inside each resolve_bin and read by _first_arg through adapters.load(hid.replace('-','_')).ENV_VAR, falling back to the derived <ID>_BIN only when no adapter module exists. My probes, on the built bytes: render('claude-code') with $CLAUDE_BIN -> argv[0]='/tmp/.../alt-claude' (pre-fix was 'claude'); render('copilot-cli') with $COPILOT_BIN -> the override path; the second derived name $CLAUDE_CODE_BIN is now correctly IGNORED; and the WIRE probe -- rotate.spawn_window(dry_run=True, harness='claude-code', root with a bin-less claude-code row) with $CLAUDE_BIN set -- prints argv[0]='/tmp/.../alt-claude --remote-control p ...', so the live SEAT path (the exact path where bin_path is None because harnesses.claude-code has no bin cell, which is what round 3a got wrong) now reaches the conventional override. Round-3a behaviour is preserved: no override + bare name not on PATH -> argv[0]='claude'; a synthetic '~' cell with no adapter module still refuses by name naming the derived $SYNTH_BIN; $PI_BIN still wins for pi; the four adapters' resolve_bin still take one name each. The delivered test names exist in the diff (test_render_honours_the_adapters_one_env_override, test_render_ignores_a_second_derived_override_name, test_every_adapter_exports_the_env_var_it_resolves) and the production-line count matches the measured numstat (4+4+4+4+19 = 35). (3) THE NEAR MISS: an implementation that added ENV_VAR to the adapters but kept the derived name as the FIRST choice would satisfy the words ("one name in one place") and lose the mechanism -- the conventional var would still be shadowed; this kid reads the adapter constant FIRST and only falls back, which is why the auth probe now passes. A second near miss avoided: falling back to the derived name silently instead of refusing for a synthetic template, which would have broken the existing 'fakebin' render tests. (4) VERDICT: kept proved for this kid's stated, narrow claim -- my seven probes (auth, wire, gate) hold on the built bytes, including the live seat path. The parent-found defect from round 3a is closed. The hypothesis's remaining known narrowing is inherited, not this kid's: a token-free absolute cell is still carried unchanged, and the ~user mis-expansion flagged by round 2's push_further is untouched.
<!-- THOUGHT:END -->

Round 3b reviewed by parent a00-402306e7 on the 20542b83c..9937e359 diff. All seven parent probes hold on the built bytes: the conventional $CLAUDE_BIN/$COPILOT_BIN now reach harness_template.argv[0] (RED was 'claude'/'copilot'), the derived $CLAUDE_CODE_BIN is correctly ignored, and the WIRE probe through the live rotate.spawn_window seat path (bin_path=None) prints argv[0]=the $CLAUDE_BIN path. Round-3a behaviours preserved (bare name unchanged, ~ cell refuses by name, $PI_BIN wins); the four adapters each export ENV_VAR and the delivered test names and 35-line count match the diff. Round 3a's failed auth probe is closed; verdict kept proved.
