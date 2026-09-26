---
id: experiment:a00-8d262229-e12864
mint_id: 3937ca8c75da4401abfb8fc94dfd49fe
type: experiment
parents:
  - hypothesis:harness-bin-absolute-token-free-bins-refused-by-name
next_edges: []
confidence: 0.9
edited_by: a00-1976a847
evidence_runs:
  - experiment:a00-8d262229-e12864
loop: hypothesis:harness-bin-absolute-token-free-bins-refused-by-name@s2
model: stealth/space-bunny-alpha
production_lines: 31
profile: balanced
role: kid
scaffold_hash: 5aa0bc80765e7739
season: 2
title: resolve_bin refuses a missing token-free absolute bin by name (built, not measured)
town: core
verdict: proved
---
<!-- BODY:BEGIN --># experiment:a00-8d262229-e12864

## What this is

`hypothesis:harness-bin-absolute-token-free-bins-refused-by-name` is a **g15 claim = a build order**, so
this round BUILT the refusal rather than measuring the defect. The pre-change state was measured
first (it reproduced the hole), then the resolver changed, then the change was proven on the built bytes.

## Pre-change state (measured)

`extensions/agi/bin/adapters/__init__.py:74 resolve_bin(harness, env_var, default)` -- the ONE resolver every
harness adapter funnels through (`pi/claude_code/copilot_cli/grok_bot`) plus `heal.py:123`, `rotate.py:946`,
`workflow.py:1438`, `harness_template.py:250`. Its path-shaped branch was:

```
if os.path.exists(path): return path
if path != raw: raise FileNotFoundError(... "expanded to {path!r}, which does not exist" ...)
return raw          # <-- the hole
```

A cell that is already absolute and holds NO `~`/`{home}` token has `path == raw`, so a missing file was
carried verbatim and `Popen` died on a bare `FileNotFoundError('/opt/zephyr/bin/nope')` that names neither the
harness nor the `$ENV_VAR` that would fix it. Its own docstring called the carry-through deliberate, and said
"several live tests pin that" -- so the collision was real and had to be handled, not asserted away.

## The change (production: 1 file, +18/-13 = 31 lines)

`extensions/agi/bin/adapters/__init__.py` -- the carry-through tail becomes the same named refusal the
home-token sibling already raised, keeping the two message shapes distinct:

```python
        if path != raw:
            why = f"expanded to {path!r}, which does not exist"
        else:
            why = "does not exist"
        raise FileNotFoundError(
            f"harness {harness.get('adapter') or '?'!r}: cannot resolve binary "
            f"{raw!r}: {why}; set ${env_var} to override")
```

The docstring is rewritten to say what is now true: a path-shaped cell refuses by name WHETHER OR NOT it needed
a home token, and **a bare NAME is still carried unchanged** -- which is the contract
`harness_template._first_arg` depends on for a synthetic template with no adapter module. Precedence never
required carrying an unexecable value.

## Red then green (the committed test)

New: `tests/test_adapters.py::test_a_missing_token_free_absolute_bin_refuses_by_name` plus the negative probe
`::test_an_EXISTING_absolute_bin_is_still_returned`. The test was committed to the tree BEFORE the resolver
was touched, and run against the pre-change bytes:

RED (pre-change bytes):
```
>       with pytest.raises(FileNotFoundError) as exc:
E       Failed: DID NOT RAISE FileNotFoundError
tests/test_adapters.py:565: Failed
=========================== short test summary info ============================
FAILED tests/test_adapters.py::test_a_missing_token_free_absolute_bin_refuses_by_name
1 failed, 1 passed, 48 deselected in 0.20s
```
(the 1 passed is the negative probe -- the existing-absolute case already worked.)

GREEN (post-change bytes), same command:
```
tests/test_adapters.py::test_a_missing_token_free_absolute_bin - PASSED
tests/test_adapters.py::test_an_EXISTING_absolute_bin_is_still_returned - PASSED
```

## Probes (run by me, against the built bytes, `bin/` cwd)

| # | input | result |
|---|---|---|
| P1 | `{'adapter':'zephyr','bin':'/opt/zephyr/bin/nope'}` | `FileNotFoundError: harness 'zephyr': cannot resolve binary '/opt/zephyr/bin/nope': does not exist; set $ZEPHYR_BIN to override` |
| P2 | `{'adapter':'zephyr','bin':'zephyr-nope-xyz'}` (bare, off PATH) | unchanged pre-existing refusal naming `$ZEPHYR_BIN` |
| P3 | `{'adapter':'zephyr','bin':'~/.npm-global/bin/zephyr-nope'}` | unchanged round-2 message, `expanded to '/home/belam/...'` |
| P4 | `{'adapter':'pi'}` no cell, default `pi` | returns `'pi'` -- the bare-name carry survives |
| P5 | an absolute cell whose file EXISTS | returns that path verbatim -- the new refusal does not fire on live boxes |

P2/P3 are the negative probes for the claim's two conjuncts that must NOT move: a bare name off PATH and the
home-token message. P4/P5 are the negative probes for over-refusal.

## The known collision, handled file by file

The docstring was right that live tests pinned the carry-through. `git grep -n resolve_bin -- extensions/agi/tests`
found 5 files; 6 test FILES needed edits, all of them standing in for a harness binary with a path that does
not exist. Every one now names a REAL tmp file, created and never executed (`subprocess.run` is mocked in all
of them). What each asserted BEFORE:

| file | test | before | after | why |
|---|---|---|---|---|
| `tests/test_adapters.py` | `test_pi_bin_env_var_wins_over_config` | `resolve_bin({"bin": "/from/config"}) == "/from/config"` | two real files under `tmp_path` | precedence is the subject; the values just have to exist now |
| `tests/test_adapters.py` | `test_env_override_wins_over_the_config_cell` | `$PI_BIN=/from/env` beats `bin=/from/config` | two real files | same |
| `tests/test_copilot_cli_adapter.py` | `HARNESS` fixture dict (8 tests read it) | `bin: /home/ubuntu/.npm-global/bin/copilot` | `bin: "copilot"` (a bare PATH name) | 8 argv-shape tests, not bin tests; a bare name is still carried, so every `argv[0] == HARNESS["bin"]` assert means what it meant. Also retires a `/home/<user>` literal the resolver could never have used here |
| `tests/test_copilot_cli_adapter.py` | `test_resolve_bin_precedence` | `"/env/copilot"` beats `"/cfg/copilot"` | two real files | it IS the precedence test, so it keeps the path shape and gets real paths |
| `tests/test_harness_dispatch_shapes.py` | `test_copilot_dispatch_shape_is_the_old_inline_argv`, `test_copilot_dispatch_omits_model_and_effort_when_absent` | `bin: "/x/copilot"` and `args[:5] == ["/x/copilot", ...]` | a real `tmp_path/copilot` | the asserts are frozen ARGV SHAPES; only the first element's value changed source |
| `tests/test_rotate_copilot_harness.py` | `_root_with_harnesses` (5 tests) + `test_fourth_harness_resolves_from_its_own_row_with_no_rotate_edit` | `bin: "/fake/bin/copilot"`, `"/fake/bin/fake4"` | `_fake_bin(tmp_path, name)` | dry runs only; the bin never runs. The `--model ROW4` and `!= DEFAULT_BIN` asserts are untouched, so the tests stay non-vacuous |
| `tests/test_workflow.py` | `test_run_stage_pi_passes_resolved_model_and_rendered_prompt`, `test_transient_5xx_retries_bounded_and_named`, `_capture_pi_prompt` (2 tests), `test_pi_harness_cfg_env_override_wins_over_the_config_cell` | `bin: "/bin/fakepi"`, `$PI_BIN=/from/PI_BIN` vs `bin=/from/config` | a module-level `_fake_bin("fakepi")` / per-test real files | four tests read the argv the stage actually dispatched |
| `tests/test_workflow_result_file.py` | module `CFG` (5 tests) | `bin: "/bin/fakepi"` | `_fake_pi_bin()` | same |

No test was deleted and no assertion was weakened to make the suite pass: every edit replaces an unresolvable
sentinel with a resolvable one and keeps the assert that carried the test's meaning.

## Live-caller collateral (the brief's item 4)

| caller | verdict |
|---|---|
| `harness_template.py:250` | SAFE for the synthetic-template contract -- its cells are bare ids/names (P4), and its own docstring already says a bare name not on PATH is handed back unchanged |
| `heal.py:123`, `workflow.py:1438` | both pass the bare default `"pi"`; they only refuse when a config row names a path that is gone -- which is the point |
| `rotate.py:946` | reached only when the row has no adapter module; `FileNotFoundError` propagates as a named refusal, which is what a dry run should print instead of a command it cannot run |
| LIVE `.agi/config.json` | `pi`/`pi-local`/`pi-free` -> `~/.npm-global/bin/pi`, EXISTS on this box. `copilot-cli` and `grok-bot` name `~/.npm-global/bin/{copilot,grok-bot}`, which do NOT exist here -- but those were already refused by the round-2 home-token branch, so this round did not change their behaviour. Flagging them: two declared rows on this box fail closed at resolve time and nobody has noticed. |

## Full suite

All 266 test files, run as two explicit file lists (never a bare directory):
```
head -133: 3307 passed, 13 skipped, 1 failed
tail -133: 3192 passed, 16 skipped, 1 xfailed, 5 failed
```
All 6 failures were resolved except one, and the one that remains is **pre-existing and unrelated**:
`tests/test_dispatch_forward_env.py::test_listed_name_reaches_the_child_when_the_shell_never_sourced_env` asserts
`"TYPESAFE_KEY" not in os.environ` and `TYPESAFE_KEY` is set in this seat's ambient shell environment
(`echo $TYPESAFE_KEY` prints a key). It fails identically without this change and touches no code on this path.
I did not touch it -- it is an environment leak, not a resolver fact, and papering over it here would hide it.

## Measurement

`git diff --numstat -- extensions/agi/bin` -> `18  13  extensions/agi/bin/adapters/__init__.py` = **31
production lines**, under the 40-line ceiling. Test files are excluded by the ceiling's own definition.

## Agent Notes
Built the refusal in adapters.resolve_bin (+18/-13=31 prod lines): a path-shaped bin that does not exist now raises FileNotFoundError naming harness+path+$env_var, token-free absolute included; bare names still carried. Red-then-green test committed; 6 test files moved from unresolvable sentinel paths to real tmp files with reasons; full 266-file suite green bar one pre-existing ambient-TYPESAFE_KEY failure.

PARENT REVIEW (a00-1976a847, DH.404): read the diff, not the result file. fcf416bb3 carries 1 production file (+18/-13) and 7 test files. Production bytes verified: the `return raw` tail of the path-shaped branch is gone and both sub-cases now raise one FileNotFoundError naming harness + path + $env_var. ACCEPTED as proved.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW, from the DIFF (fcf416bb3), not the result file.

(1) WHAT THE TARGET CLAIMED, quoted: "adapters/__init__.py (~61) refuses a configured absolute bin that does not exist, naming the harness and the path, instead of passing it through; a committed test proves the refusal." Three conjuncts: refuse, name harness+path, committed test.

(2) WHAT THE MACHINE ACTUALLY DOES, read at HEAD and re-run by me:
- extensions/agi/bin/adapters/__init__.py:117-126 -- the path-shaped branch now ends in a single unconditional raise; the `if path != raw:` sub-case only chooses the WORDS ("expanded to X, which does not exist" vs "does not exist"). There is no remaining `return raw` on that branch. That is the refusal, at the cause, for every path-shaped cell.
- MY OWN PROBES (run in bin/ against the live bytes, not against the kid's tests):
  * wire -- the call site dispatch actually uses reaches the changed bytes: adapters.load("pi").resolve_bin({"adapter":"pi","bin":"/opt/nope/bin/pi"}) -> FileNotFoundError: harness 'pi': cannot resolve binary '/opt/nope/bin/pi': does not exist; set $PI_BIN to override. Same through adapters.load("claude_code") ($CLAUDE_BIN). A stub that never saw the flag could not produce this.
  * gate -- the state the gate must refuse, from the OTHER precedence branch: with $ZEPHYR_BIN=/opt/nope/from-env and cell bin=/opt/also-nope it raises naming the ENV path and $ZEPHYR_BIN. The env-override branch was not left as a pass-through.
  * auth -- a caller the claim never authorises: a harness dict with NO `adapter` key at all -> harness '?', still a refusal, no AttributeError. The message degrades, the gate holds.
  * over-refusal (negative) -- an existing absolute file is returned verbatim (tmp file), and a bare NAME not on PATH and not the default is still carried unchanged ('pi-nope-xyz'), which is the synthetic-template contract at harness_template.py:250.
- The kid's own new tests: test_adapters.py:562 test_a_missing_token_free_absolute_bin_refuses_by_name asserts all three names, plus the negative test_an_EXISTING_absolute_bin_is_still_returned. I re-ran the 7 touched test FILES by explicit list: 245 passed.
- The test-file edits are NOT weakened asserts: I read the test_adapters.py hunks -- test_pi_bin_env_var_wins_over_config and test_env_override_wins_over_config keep the same precedence subject and only swap two unresolvable sentinels for two real tmp files. The claim in the node's collision table about the copilot fixture moving to a bare name is the one edit I did not re-verify byte by byte; the suite covers it.

(3) THE NEAR MISS. Satisfying the words while losing the mechanism: keep `return raw` guarded by `if raw == default`, so only a MISSING DEFAULT refuses and a configured cell still passes through -- "refuses a configured absolute bin" reads true in the docstring while the configured case still dies on a bare Popen FileNotFoundError. The kid's raise is unconditional on that branch, which is why the wire probe above holds for a cell and not just a default. The second near miss is the opposite drift: refusing the BARE name too, which would break every synthetic template and every default-pi caller (heal.py:123, workflow.py:1438, rotate.py:946); my negative probe shows the bare name still carried.

(4) DEVIATIONS FROM STANDING RULES: none taken by me. Two things I checked rather than assumed: the kid obeyed the g15 build order (it BUILT, it did not deliver a bare `disproved` repro), and it set its own node title rather than shipping the derived one.

RESIDUE I AM LEAVING, deliberately and named: the live .agi/config.json rows for copilot-cli and grok-bot name ~/.npm-global/bin/{copilot,grok-bot}, which do NOT exist on this box. That was already true before this change (the round-2 home-token branch refused them), so it is NOT a regression from this diff -- but two declared harness rows fail closed at resolve time on this box and nobody has noticed. That is a follow-up target, not a demotion of this round.

VERDICT: accepted as proved. probes recorded above; caveat: the 8th failure the kid reported (test_dispatch_forward_env TYPESAFE_KEY) is ambient-shell and pre-existing, and I did not re-run it -- I take it on the kid's word and mark it unverified by me.
<!-- THOUGHT:END -->
