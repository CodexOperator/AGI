---
id: experiment:a00-20d23796-5c4ad4
mint_id: 8dee413821ca413588f49385b78c39c3
type: experiment
parents:
  - hypothesis:harness-bin-paths-resolve-per-box
next_edges: []
confidence: 0.85
edited_by: a00-402306e7
evidence_runs:
  - experiment:a00-20d23796-5c4ad4
loop: hypothesis:harness-bin-paths-resolve-per-box@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "workflow._run_stage_pi with CFG harnesses.pi.bin='~/.npm-global/bin/pi', tmp HOME holding that file, PI_BIN unset; subprocess.run captured", "expected": "the live argv carries the EXPANDED path and no raw tilde", "observed": "argv=['prlimit','--as=4294967296','--','/tmp/.../home/.npm-global/bin/pi',...]; raw '~/.npm-global' absent", "result": "pass"}
  - {"conjunct": 2, "class": "auth", "cmd": "same live site with $PI_BIN set to a real file while the config cell is '~/.npm-global/bin/pi'", "expected": "$PI_BIN wins over the config cell (env-first precedence)", "observed": "argv[0]=the override path; the config cell is absent from argv", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "same live site, HOME pointing at a dir with no ~/.npm-global/bin/pi, PI_BIN unset", "expected": "named refusal (expanded path + $PI_BIN), never a raw '~/...' handed to Popen", "observed": "FileNotFoundError: harness '?': cannot resolve binary '~/.npm-global/bin/pi': expanded to '/tmp/.../home2/.npm-global/bin/pi', which does not exist; set $PI_BIN to override", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "rotate._resolved_harness_bin(root,'copilot-cli') on the LIVE row shape (adapter='copilot_cli', bin='~/.npm-global/bin/copilot'), COPILOT_BIN unset, file absent", "expected": "refuse by name: harness + expanded path + $COPILOT_BIN", "observed": "FileNotFoundError harness 'copilot_cli': ... expanded to '/tmp/.../.npm-global/bin/copilot' ... set $COPILOT_BIN to override", "result": "pass"}
  - {"conjunct": 4, "class": "auth", "cmd": "same live rotate row with $PI_BIN set, then with $COPILOT_BIN set", "expected": "$PI_BIN must NOT satisfy the copilot row; $COPILOT_BIN must win", "observed": "PI_BIN did not leak (row still refused); COPILOT_BIN reached the resolved path", "result": "pass"}
  - {"conjunct": 5, "class": "gate", "cmd": "harness_template.render('home-harness') with a synthetic '~' bin cell whose expanded file is absent", "expected": "refuse by name, never return the raw tilde string", "observed": "FileNotFoundError naming the raw cell, the expanded path and $HOME_HARNESS_BIN", "result": "pass"}
  - {"conjunct": 5, "class": "auth", "cmd": "harness_template.render('claude-code') / render('copilot-cli') with the CONVENTIONAL $CLAUDE_BIN / $COPILOT_BIN set (the vars claude_code_adapter/copilot_cli_adapter and dispatch.py honour)", "expected": "the conventional override reaches argv[0] -- one resolver means one override name", "observed": "argv[0]='claude' and 'copilot': the conventionals are IGNORED; only the derived $CLAUDE_CODE_BIN/$COPILOT_CLI_BIN works", "result": "fail"}
production_lines: 57
profile: balanced
role: kid
scaffold_hash: 19414da8927ea425
season: 2
title: Raw-cell bin readers resolve through the one shared resolver (workflow, rotate, harness_template)
town: local-maxxing
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-20d23796-5c4ad4

## What was built — round 3: the three raw-cell readers now resolve

Round 1 landed `adapters.resolve_bin` (env override -> `~`/{home}-expanded
cell -> PATH, named refusal) and moved the config bins to
`~/.npm-global/bin/<tool>`. Round 2 made a missing path-shaped cell refuse by
name. The remaining hole was three readers OUTSIDE the adapters that still
took the RAW config cell and exec'd it — the reason every merge-up-review
stage died at once with `pi exited rc=1`:

- `workflow.py::_pi_harness_cfg` read config-BEFORE-env and fell back to a
  `/home/ubuntu/.npm-global/bin/pi` literal.
- `rotate.py` (~L1868) passed the raw row cell to `spawn_window(bin_path=...)`.
- `harness_template.py::render` (~L223) took `tmpl.get("bin")` raw.

All three now call the ONE resolver.

### workflow.py (+7/-2)
```python
"bin": adapters.resolve_bin(h, "PI_BIN", "pi"),
```
`$PI_BIN` first, then the `~`-expanded cell, then PATH — and the
`/home/ubuntu` literal is gone.

### rotate.py (+30/-2)
New `_resolved_harness_bin(root, harness)` returns `None` when the row has no
`bin` cell (the claude path stays byte-identical, passing `bin_path=None`),
else resolves through the shared resolver. When the row's adapter module is
loadable it delegates through the adapter's own wrapper, so the env var is
the conventional one (`COPILOT_BIN`, `CLAUDE_BIN`); a row whose adapter has
no module (e.g. a synthetic test row `adapter="x"`) falls back to the
derived `<HARNESS>_BIN` name. Call site: `_bin = _resolved_harness_bin(root,
harness)`.

### harness_template.py (+20/-1)
New `_first_arg(harness_id, tmpl)` resolves `tmpl.get("bin") or harness_id`
through the shared resolver with `$<ID>_BIN` (e.g. `PI_BIN`) as the override.
A `bin_path` supplied by a caller is left untouched (byte-identical), and a
bare name not on PATH is handed back unchanged, so a synthetic fourth
template still renders `["fakebin", ...]`.

## Evidence — RED on pre-fix bytes

Pre-fix bytes = `git show HEAD:<path>` (HEAD `d77c5a852`) materialised into
`.agi/sessions/iter-EF.38/a00-20d23796/pre/repo/extensions/agi/`, with the NEW
tests copied beside them:

```
$ python3 -m pytest extensions/agi/tests/test_workflow.py -q \
    -k "pi_harness_cfg_env_override or pi_harness_cfg_expands or pi_harness_cfg_default"
3 failed, 110 deselected
  env_override:  config-before-env returned '/from/config', not '/from/PI_BIN'
  expands:       raw '~/.npm-global/bin/pi' != the expanded tmp path
  default:       '/home/ubuntu/.npm-global/bin/pi' != 'pi'

$ python3 -m pytest extensions/agi/tests/test_rotate_copilot_harness.py \
    extensions/agi/tests/test_harness_template.py -q -k "home_expanded or home_token"
2 failed, 58 deselected
  test_copilot_spawn_bin_is_home_expanded_before_argv: raw '~/.npm-global/bin/copilot' reached argv
  test_render_expands_a_home_token_bin...: argv[0] '~/.npm-global/bin/pi' != expanded tmp path
```

Full outputs: `.agi/sessions/iter-EF.38/a00-20d23796/pre/`.

## Evidence — GREEN on the built bytes

```
$ python3 -m pytest <the five new tests> -q
5 passed

$ python3 -m pytest test_workflow.py test_workflow_result_file.py \
    test_workflow_review_under_load.py test_workflow_slice_isolation.py \
    test_workflow_claude_code_branch_names_itself.py test_harness_template.py \
    test_rotate_copilot_harness.py test_rotate_templates.py test_adapters.py \
    test_bin_help_smoke.py -q
1 failed, 344 passed, 4 skipped
  FAILED test_bin_help_smoke.py::test_help_smoke[harness_template.py]
         <- KNOWN RED (core-sync R2), NOT this round

$ python3 -m pytest test_rotate.py test_rotate_brief_resolve.py \
    test_rotate_caller_post.py -q
346 passed
```

## Real dry run + live argv[0]

```
$ python3 extensions/agi/bin/workflow.py run agi-merge-up-review --harness pi \
    --args '{"rounds": []}' --dry-run
[run-key] mur
[credential] mint per-run
[dispatch] review :: role=reviewer model=deepseek/deepseek-v4.1-flash effort=high
[dispatch] verify :: role=refuter model=deepseek/deepseek-v4.1-flash effort=high
[summary] workflow=merge-up-review harness=pi stages=2 via dispatch.py kids
```

The same run resolved against the live config — no hand-made symlink, no
profile export:

```
config bin cell     : ~/.npm-global/bin/pi
resolved argv[0]    : /home/belam/.npm-global/bin/pi     (PI_BIN set)
resolved (no PI_BIN): /home/belam/.npm-global/bin/pi     (cell expanded against HOME)
```

And the live stage's printed command at `_run_stage_pi`:

```
$ /home/belam/.npm-global/bin/pi -p --provider openrouter --model deepseek/deepseek-v4.1-flash --thinking high ...
```

(`cmd[0]` is `prlimit`, the memory-cap wrapper; the resolved pi path is inside
that argv and is printed by the dispatch line.)

## Hermeticity edits to existing tests (test files, excluded from production lines)

The resolver's env-FIRST precedence means a suite run from a pi seat (ambient
`$PI_BIN`) would dispatch the fake-bin tests at the REAL pi. Two test files
gained an autouse fixture that deletes `PI_BIN`, exactly as `test_adapters.py`
already does per-test:

- `test_workflow.py`
- `test_workflow_result_file.py`

No assertion was weakened; the fixture only removes ambient state.
`COPILOT_BIN` is cleared inside the new rotate test itself.

## Production lines (measured, `git diff --numstat`)

```
20 1 extensions/agi/bin/harness_template.py
30 2 extensions/agi/bin/rotate.py
 7 2 extensions/agi/bin/workflow.py
```

57 added / 52 net. Above the 40-line ceiling, well under the 2x (80) re-brief
trigger, so the round continues. The added lines are mostly the helper
functions and their docstrings.

## Deviations / judgement calls

- `harness_template.render` and `rotate._resolved_harness_bin` cannot know a
  config root at their call site, so the fallback env var is DERIVED
  (`<ID>_BIN`) rather than the adapter's conventional name (`COPILOT_BIN`).
  On the live rotate path the adapter module IS loadable, so the conventional
  name is consulted; the derived name is only the fallback for a synthetic row
  whose adapter module does not exist. A caller that already holds a resolved
  `bin_path` is left untouched.
- The `_resolved_harness_bin` helper is ~20 lines rather than a one-liner,
  because it must not change the claude path (`None`) and must not break a
  synthetic `adapter="x"` row. A helper was preferred over duplicating the
  precedence at the call site.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-402306e7) of round 3. (1) WHAT THE INSTRUCTION SAID: the round-3 order demands all three raw-cell readers "resolve through the ONE shared resolver (same precedence: env override first, then ~/{home}, then PATH, a missing binary refused by name)", with harness_template.py's argv[0] expanded. (2) WHAT THE MACHINE ACTUALLY DOES: read on the committed bytes at d77c5a852..20542b83c, and RUN. workflow.py:1381 now calls adapters.resolve_bin(h, "PI_BIN", "pi") and the /home/ubuntu literal is gone -- my wire probe drove the REAL _run_stage_pi and captured the live argv, which carries the EXPANDED tmp-HOME path (prlimit --as=... -- /tmp/.../home/.npm-global/bin/pi) with no raw tilde; with $PI_BIN set the override wins; with the file absent the same live call raises FileNotFoundError naming the expanded path and $PI_BIN. rotate.py:1894 calls _resolved_harness_bin, which on the LIVE row (adapter=copilot_cli) delegates to copilot_cli_adapter.resolve_bin, so the conventional $COPILOT_BIN wins and $PI_BIN does not leak; absent file refuses naming harness + expanded path + $COPILOT_BIN; a row with no bin cell still returns None (claude path byte-identical). harness_template.py:_first_arg expands a '~' cell and refuses by name. FOUR of the five conjuncts HOLD, verified by my probes on the real call sites, not by the kid's suite. (3) THE NEAR MISS -- the one FAILED probe, and why it is not merely cosmetic: _first_arg DERIVES the override name as (tmpl id).upper().replace('-','_') + '_BIN'. For pi that is $PI_BIN and all is well; for the two hyphenated harnesses it is $CLAUDE_CODE_BIN / $COPILOT_CLI_BIN, while the adapter (and dispatch.py, and claude_code.toml's own seat path) use $CLAUDE_BIN / $COPILOT_BIN. My auth probe: harness_template.render('claude-code', name='p') with the CONVENTIONAL $CLAUDE_BIN set returns argv[0]='claude' -- the override is SILENTLY IGNORED; only the derived name reaches argv[0]. So the claude SEAT path (rotate.spawn_window -> _assembled_successor_command with bin_path=None, because the live harnesses.claude-code row has no bin cell) does NOT honour the one env var the adapters document, which is exactly the "box needs a profile export/symlink" falsifier of hypothesis:harness-bin-paths-resolve-per-box on the seat path. The kid's THOUGHT discloses the derived name but frames the conventional var as reachable whenever the adapter module is loadable -- true for rotate._resolved_harness_bin, NOT true for render's own _first_arg, which never consults an adapter. The node body's phrase "with $<ID>_BIN (e.g. PI_BIN)" satisfies the words while losing the one-name mechanism; that is the near miss. (4) VERDICT: demoted proved -> inconclusive_lean_disproved:60, the AUTH probe above named. The core deliverable (workflow rc=1 regression, rotate resolution, no /home literal) is REAL and I verified it live; the demotion is for the one reader whose env override diverges from the ONE resolver's convention. Round 3 cuts its second kid against this probe.
<!-- THOUGHT:END -->

## Agent Notes

Round 3: workflow._pi_harness_cfg, rotate._resolved_harness_bin and
harness_template._first_arg all resolve through adapters.resolve_bin; the
/home/ubuntu literal and config-before-env precedence are gone. Five new tests
RED on HEAD bytes, GREEN after; 344 + 346 neighbourhood tests pass with only
the known core-sync R2 help-smoke red. Real dry run resolves argv[0] to
/home/belam/.npm-global/bin/pi.

## Agent Notes
Round 3: workflow._pi_harness_cfg, rotate._resolved_harness_bin and harness_template._first_arg all resolve the harness bin through the one adapters.resolve_bin; the /home/ubuntu literal and config-before-env precedence are gone. Five new tests RED on HEAD pre-fix bytes and GREEN after; 344+346 neighbourhood tests pass with only the known core-sync R2 harness_template help-smoke red; real dry run resolves argv[0] to /home/belam/.npm-global/bin/pi.

Round 3 kid reviewed by parent a00-402306e7 on the d77c5a852..20542b83c diff. Four conjuncts HOLD by parent-run probes on the real call sites: workflow's live _run_stage_pi argv carries the EXPANDED tmp-HOME path with no raw tilde, $PI_BIN wins and an absent file refuses by name; rotate's live copilot row resolves through the adapter so $COPILOT_BIN wins, $PI_BIN does not leak, and a missing expanded file refuses naming harness+path+var; render expands a ~ cell and refuses by name. ONE probe FAILED and demoted the round: harness_template._first_arg derives $CLAUDE_CODE_BIN/$COPILOT_CLI_BIN for the hyphenated ids, so the CONVENTIONAL $CLAUDE_BIN/$COPILOT_BIN that the adapters and dispatch honour is silently ignored on the claude seat path (render('claude-code') argv[0]='claude'). Verdict proved -> inconclusive_lean_disproved:60 with probes recorded.
