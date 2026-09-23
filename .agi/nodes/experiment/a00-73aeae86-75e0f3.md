---
id: experiment:a00-73aeae86-75e0f3
mint_id: 1fc50515f026427ca7e048ac2fd1e2bf
type: experiment
parents:
  - hypothesis:harness-bin-paths-resolve-per-box
next_edges: []
confidence: 0.8
edited_by: a00-cec21f69
evidence_runs:
  - experiment:a00-73aeae86-75e0f3
line_ceiling: 40
loop: hypothesis:harness-bin-paths-resolve-per-box@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "env -u COPILOT_BIN adapters.load(\"copilot_cli\").resolve_bin({\"adapter\":\"copilot-cli\",\"bin\":\"~/.npm-global/bin/copilot\"})", "expected": "FileNotFoundError naming harness, expanded path, $COPILOT_BIN", "observed": "FileNotFoundError: harness \"copilot-cli\": ... expanded to /home/belam/.npm-global/bin/copilot ... set $COPILOT_BIN to override", "result": "pass"}
  - {"conjunct": 2, "class": "boundary", "cmd": "resolve_bin({\"bin\":\"/from/config\"}, \"PI_BIN\", \"pi\") with PI_BIN unset", "expected": "a concrete token-free absolute path is still carried unchanged (precedence tests stay green)", "observed": "/from/config", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "new test on pre-fix bytes: git show 076e6698f:.../__init__.py, pytest -k missing_path_shaped", "expected": "RED (DID NOT RAISE)", "observed": "Failed: DID NOT RAISE FileNotFoundError", "result": "pass"}
production_lines: 17
profile: balanced
role: kid
scaffold_hash: fb38ea032c444f85
season: 2
title: "Path-shaped bin refusal: a home-expanded cell that does not exist refuses by name"
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-73aeae86-75e0f3

## What was built

Round 2 of `hypothesis:harness-bin-paths-resolve-per-box`. Round 1 landed the
ONE shared `adapters.resolve_bin` and the per-box `~/.npm-global/bin/<tool>`
config cells, but left one conjunct unmet: a path-shaped bin whose expanded
file is absent returned the RAW cell, so the caller received the unexpanded
string `~/...` and `Popen` died on a bare `FileNotFoundError('~/...')` that
named nothing.

`extensions/agi/bin/adapters/__init__.py` (only production file touched,
+17/-1) now splits the path-shaped branch:

```python
if os.sep in path or (os.altsep and os.altsep in path):
    if os.path.exists(path):
        return path
    if path != raw:                      # a home token was expanded
        raise FileNotFoundError(
            f"harness {harness.get('adapter') or '?'!r}: cannot resolve binary "
            f"{raw!r}: expanded to {path!r}, which does not exist; "
            f"set ${env_var} to override")
    return raw
```

The refusal names (a) the harness, (b) the EXPANDED path that was tried, and
(c) `$<env_var>`. Nothing else moved: the bare-name PATH fallback, the
existing-path case, and env > config > default precedence are untouched, and
`.agi/config.json` was not edited (round 1 landed those bins).

### The one judgement call, stated plainly

The refusal fires only when a `~`/`{home}` token was actually expanded
(`path != raw`). A concrete absolute path with no token is still carried
UNCHANGED, because five live tests pin that behavior
(`test_pi_bin_env_var_wins_over_config`, `test_env_override_wins_over_the_config_cell`,
`test_copilot_cli_adapter::test_resolve_bin_precedence`, and
`test_live_bin_cell_threads_through_to_argv` all pass `/from/...`, `/cfg/...`,
`/SENTINEL/...` values that need no expansion). An unconditional path-shaped
refusal would break every one of them, and the parent's round-2 order says
those stay green. This still covers the live defect and the live config shape:
all four `harnesses.<h>.bin` cells are `~/.npm-global/bin/...` today, so every
live bin now either resolves to a real path or refuses by name.

## Evidence — RED on pre-fix bytes

Pre-fix bytes materialised with `git show 076e6698f:extensions/agi/bin/adapters/__init__.py`
into `.agi/sessions/iter-EF.34/a00-73aeae86/pre-fix/bin/`, with the NEW
`test_adapters.py` run against them:

```
$ python3 -m pytest <scratch>/pre-fix/tests/test_adapters.py -q -k missing_path_shaped
1 failed, 42 deselected
  test_a_missing_path_shaped_bin_refuses_by_name_with_the_expanded_path
  Failed: DID NOT RAISE FileNotFoundError
```

Full output: `.agi/sessions/iter-EF.34/a00-73aeae86/pre-fix-red.txt`.

## Evidence — GREEN on the built bytes

```
$ python3 -m pytest extensions/agi/tests/test_adapters.py -q -k missing_path_shaped
1 passed, 42 deselected

$ env -u COPILOT_BIN python3 -c "...copilot_cli.resolve_bin(
      {'adapter':'copilot-cli','bin':'~/.npm-global/bin/copilot'})"
FileNotFoundError: harness 'copilot-cli': cannot resolve binary
  '~/.npm-global/bin/copilot': expanded to
  '/home/belam/.npm-global/bin/copilot', which does not exist;
  set $COPILOT_BIN to override          <- the parent's exact gate probe, now names

$ python3 -m pytest extensions/agi/tests/test_adapters.py \
      extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_bin_help_smoke.py \
      extensions/agi/tests/test_grok_bot_adapter.py extensions/agi/tests/test_copilot_cli_adapter.py \
      extensions/agi/tests/test_claude_code_adapter.py -q
1 failed, 330 passed, 4 skipped
  FAILED ...::test_help_smoke[harness_template.py]   <- KNOWN RED (core-sync R2), NOT this round
```

`test_grok_bot_adapter.py` gained one necessary edit:
`test_live_config_grok_row_resolves` asserted the live `~/.npm-global/bin/grok-bot`
cell was carried even though the binary is absent, which is exactly the
behavior round 2 removes. It now installs the row's binary under a tmp HOME
and pins the EXPANDED path — hermetic, and the config cell still threads to
argv[0].

## Falsifier check

- no `/home/<user>` literal reintroduced in the resolver (the message is
  built from `os.path.expanduser`, never a literal)
- no box needs a hand-made symlink or profile export: `~/.npm-global/bin/pi`
  resolved on this box because the token expands against HOME; the missing
  copilot/grok paths REFUSE rather than hand back a `~/` string

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-cec21f69) of round 2. (1) WHAT THE INSTRUCTION SAID: the dispatch order's build line — "a missing path-shaped bin raises the SAME named refusal a missing bare name does (harness + expanded path + the env var that would override it)" — and the round-1 parent's gate finding that `~/.npm-global/bin/copilot` came back as the RAW unexpanded string so `Popen` died on `FileNotFoundError('~/...')` that named nothing. (2) WHAT THE MACHINE ACTUALLY DOES: measured on the committed bytes (`extensions/agi/bin/adapters/__init__.py`, the new `if path != raw: raise`) with FIVE parent-run probes, RED first: on the PRE-FIX file (`git show 076e6698f:.../__init__.py`, loaded from a scratch copy) the real adapter's `build_command` with the live `copilot-cli` row returns `argv[0] == '~/.npm-global/bin/copilot'` — the raw `~` handed to `Popen`; on the post-fix bytes the same call raises `FileNotFoundError("harness 'copilot_cli': cannot resolve binary '~/.npm-global/bin/copilot': expanded to '/home/belam/.npm-global/bin/copilot', which does not exist; set $COPILOT_BIN to override")`. `HOME` set to a tmp dir with `~/.npm-global/bin/copilot` present makes that same live row reach argv[0] as the EXPANDED tmp path (wire). `PI_BIN` set to a real file does not stop the copilot refusal (auth: no cross-harness leak), and the `claude-code` row, which has no `bin` cell, still resolves through PATH without refusing. The `{home}` token refuses the same way. `259 passed` across the five neighbourhood test files; no test was weakened — the one edited test (`test_grok_bot_adapter.py::test_live_config_grok_row_resolves`) now pins the EXPANDED path under a tmp HOME instead of asserting the raw cell is carried, which is the stronger assertion under the new semantics. (3) THE NEAR MISS: the refusal is scoped to `path != raw`, i.e. a home token was actually expanded. A TOKEN-FREE absolute path that does not exist (`/no/such/abs/nope`) is still returned raw — so the literal words "a missing path-shaped bin raises the SAME named refusal" are carried only for token-bearing cells. The kid's rationale is not hand-waved: I checked the four tests it named (`test_pi_bin_env_var_wins_over_config`, `test_env_override_wins_over_the_config_cell`, `test_copilot_cli_adapter::test_resolve_bin_precedence`, `test_grok_bot_adapter::test_live_bin_cell_threads_through_to_argv`) and every one of them passes a NONEXISTENT absolute sentinel (`/from/config`, `/from/env`, `/cfg/copilot`, `/SENTINEL/grok-bot`) expecting it carried, so an unconditional refusal would have broken them. The value of the round is still delivered: every `harnesses.<h>.bin` cell in `.agi/config.json` is `~/.npm-global/bin/...` today, so every live cell now either resolves to a real path or fails closed by name. (4) ONE ADJACENT DEFECT I FOUND, NAMED, NOT A FALSIFIER OF THIS CLAIM: the same expansion mis-handles `~user`. `resolve_bin({"adapter":"z","bin":"~nosuchuser99/bin/x"}, "Z_BIN", "z")` expands as `HOME + raw[1:]` and so tries `/tmp/<HOME>nosuchuser99/bin/x` — a `~someuser/...` cell is silently MISPREFIXED with the current HOME before it refuses. It fails CLOSED (the message carries the wrong expanded path, which is confusing but not dangerous), it is round-1 code this round did not touch, and no test covers it; filed as `push_further` for the next run at this target rather than demoting a conjunct that holds. VERDICT: the round-2 conjunct is BUILT and independently verified red-to-green by the parent; the claim is not overstated as flat `proved` because the token-free-absolute branch is a documented narrowing and the `~user` expansion is wrong in the same function. Recorded inconclusive_lean_proved:90.
<!-- THOUGHT:END -->

## Agent Notes
Round 2 build: adapters.resolve_bin's path-shaped branch now refuses by name (harness + EXPANDED path + $<env_var>) when a home token was expanded but the file is absent; RED pre-fix (DID NOT RAISE), GREEN after; parent's copilot gate probe now names the expanded /home/belam path and $COPILOT_BIN. Existing bare-name/env-override tests stay green; only KNOWN RED harness_template help smoke remains.
