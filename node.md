---
id: experiment:a00-936378a1-2d2ec5
mint_id: f25a49ea1ddf474a8ff52122bf0abb24
type: experiment
parents:
  - hypothesis:harness-bin-paths-resolve-per-box
next_edges: []
confidence: 0.95
edited_by: a00-db124f0c
evidence_runs:
  - experiment:a00-936378a1-2d2ec5
loop: hypothesis:harness-bin-paths-resolve-per-box@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "pre-fix bytes (adab78a2d9) of test_launch_memory_cap.py, ambient PI_BIN=/home/belam/.npm-global/bin/pi; pytest the one red test", "expected": "RED -- the real pi runs, 'pi exited rc=1', no memory-cap", "observed": "1 failed, 6 passed: AssertionError: 'memory-cap' not in 'pi exited rc=1'; stderr 'No API key found for openrouter'", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "fixed bytes, PI_BIN=/home/belam/.npm-global/bin/pi (the REAL pi); pytest test_launch_memory_cap.py", "expected": "7 passed -- the autouse delenv reaches the live call site, so the config-cell fake is exec'd and the cap death is named", "observed": "7 passed in 0.85s", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "env -u PI_BIN; pytest test_launch_memory_cap.py", "expected": "7 passed -- hermetic both ways", "observed": "7 passed in 0.84s", "result": "pass"}
  - {"conjunct": 2, "class": "auth", "cmd": "kid diff stat is the test file only; test_pi_harness_cfg_env_override_wins_over_the_config_cell still asserts $PI_BIN beats the config cell", "expected": "resolver + env-first precedence untouched, and still explicitly exercised", "observed": "git show --stat = test_launch_memory_cap.py only (+11); adapters/__init__.py:63 still 'os.environ.get(env_var) or harness.get(\"bin\")'; that test green under the poisoned run", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "all four *_BIN (PI/CLAUDE/COPILOT/GROK) poisoned to /nonexistent/...; pytest the five named workflow files", "expected": "no named test relies on the config cell alone -- all green under a hostile ambient", "observed": "19 passed (3 files, 33s) + 119 passed (2 files, 128s) = 138 passed", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: d7c290cd07ccea44
season: 2
title: test_launch_memory_cap is hermetic to ambient PI_BIN (EF.14 autouse delenv)
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-936378a1-2d2ec5

# experiment:a00-936378a1-2d2ec5

**Verdict: proved.** The gate red on `test_launch_memory_cap.py::test_stage_cap_death_is_named_memory_cap` is caused by the ambient `PI_BIN`; the fix is one autouse fixture that makes the file hermetic, and the resolver's env-first precedence is untouched.

## Build (dispatch order EF.46 round 4)

| item | change |
|---|---|
| hermeticise | added autouse `_no_ambient_pi_bin(monkeypatch)` to `test_launch_memory_cap.py` — `monkeypatch.delenv("PI_BIN", raising=False)`, the EF.14 pattern already in `test_workflow.py` and `test_workflow_result_file.py` |
| resolver | NOT changed — `adapters.resolve_bin` keeps env override (`$PI_BIN`) > config `bin` cell > default |
| sweep | ran all five named workflow test files under `PI_BIN`, `CLAUDE_BIN`, `COPILOT_BIN`, `GROK_BOT_BIN` EXPORTED and UNSET: 138 passed both ways; no other test needed a fix (the other files either already carry the fixture or mock `subprocess.run`) |

Production lines: 0 (test file only; `git diff --numstat` = `11 0 extensions/agi/tests/test_launch_memory_cap.py`). Well under the 40-line ceiling.

## Evidence

RED on the pre-fix bytes, ambient `PI_BIN` exported (copy of the file before the edit, run at the same path):
```
E       assert 'memory-cap' in 'pi exited rc=1'
.../test_launch_memory_cap_prefix_evidence.py:92: AssertionError
Captured stderr: workflow.py: stage draft:a pi exited rc=1
  No API key found for openrouter.
FAILED ...::test_stage_cap_death_is_named_memory_cap
1 failed, 6 passed in 1.34s
```
FIXED, `PI_BIN` EXPORTED: `7 passed in 0.77s`
FIXED, `PI_BIN` UNSET:    `7 passed in 0.81s`
Swept five workflow test files, all four `*_BIN` exported: `138 passed in 186.35s`
Swept five workflow test files, all four `*_BIN` unset:    `138 passed in 163.89s`

Raw logs: `.agi/sessions/iter-EF.46/a00-936378a1/{prefix_red,fixed_exported,fixed_unset,swept_exported,swept_unset}.txt`

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review edit, EF.46 a00-db124f0c, on the round-4 gate-red fix.
WHAT THE INSTRUCTION SAID (dispatch orders, verbatim): 'make the test hermetic to the ambient PI_BIN ...; KEEP the env-first precedence; sweep test_launch_memory_cap.py and test_workflow*.py'.
WHAT THE MACHINE ACTUALLY DOES: git show b641a78861 --stat carries exactly extensions/agi/tests/test_launch_memory_cap.py (+11) and the node; the added bytes are an autouse fixture calling monkeypatch.delenv('PI_BIN', raising=False). adapters/__init__.py:63 is unchanged, so resolve_bin still reads os.environ.get(env_var) first. I RAN the falsifying case myself: pre-fix bytes + PI_BIN=/home/belam/.npm-global/bin/pi fail with 'pi exited rc=1'; the fixed bytes pass 7/7 with PI_BIN exported and unset; poisoning all four *_BIN to /nonexistent leaves 138 named tests green.
NEAR MISS: a fixture that monkeypatch.setenv('PI_BIN', str(fake)) would also turn the one red test green while permanently masking the env-first precedence in this file -- and the sweep would still pass, because no other file's test would notice. The delenv spelling is what keeps the file honest: the test reaches the CONFIG cell, which is the behaviour under test; the precedence is exercised elsewhere in test_workflow.py:3215.
DEVIATION: none. The kid changed no resolver bytes, ran both PI_BIN signs, and the sweep covered the named files, exactly as ordered.
<!-- THOUGHT:END -->

## Agent Notes
Added an autouse PI_BIN delenv fixture to test_launch_memory_cap.py (EF.14 pattern); pre-fix RED with PI_BIN exported (1 failed/6 passed), fixed 7 passed both with PI_BIN exported and unset; swept 5 workflow test files under all four *_BIN signs: 138 passed both ways; resolver untouched.

parent accepted experiment:a00-936378a1-2d2ec5 proved: the bytes carry an autouse monkeypatch.delenv('PI_BIN') fixture (+11 test lines, production 0); I re-measured the red on pre-fix bytes under ambient PI_BIN and the green on the fixed bytes both exported and unset; the resolver and its env-first precedence are untouched and still explicitly exercised; the full five-file sweep is green under all four *_BIN poisoned to a nonexistent path (138 passed).
