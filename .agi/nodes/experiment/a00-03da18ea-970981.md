---
id: experiment:a00-03da18ea-970981
mint_id: 8ce02a06882147cbba4fe2061c05c9a7
type: experiment
parents:
  - hypothesis:pi-bin-precedence-test-is-hermetic-to-ambient-pi-bin
next_edges: []
confidence: 0.95
edited_by: a00-04514f17
evidence_runs:
  - experiment:a00-03da18ea-970981
line_ceiling: 40
loop: hypothesis:pi-bin-precedence-test-is-hermetic-to-ambient-pi-bin@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "PI_BIN=/x python3 -m pytest <copy of the kid test with the delenv byte removed>::test_pi_bin_env_var_wins_over_config -q", "expected": "FAIL, because the delenv is what clears the ambient", "observed": "FAILED: AssertionError: assert /x == /from/config; control env -u PI_BIN on the same mutant -> 1 passed", "result": "the changed byte carries the hermeticity"}
  - {"conjunct": 1, "class": "auth", "cmd": "plant PI_BIN=/ambient-should-not-win after the clear, then the config assertion", "expected": "refusal by name", "observed": "AssertionError: assert /ambient-should-not-win == /from/config", "result": "the config assertion is not vacuous"}
  - {"conjunct": 1, "class": "wire", "cmd": "pi.resolve_bin({\"bin\": \"/from/config\"}) with os.environ PI_BIN unset, then set to /from/env", "expected": "/from/config then /from/env", "observed": "exactly that, in one process, no reload", "result": "the live call site reads the precedence bytes at call time"}
production_lines: 0
profile: balanced
reviewed_by: a00-04514f17
role: kid
scaffold_hash: 2a9aa3d346033ae5
season: 2
title: "test_adapters PI_BIN precedence test is hermetic: delenv before the config assertion"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-03da18ea-970981

## Experiment

G15 BUILD order. Target: `extensions/agi/tests/test_adapters.py`,
`test_pi_bin_env_var_wins_over_config`. `pi_adapter.resolve_bin` is correct
(env `PI_BIN` over `harness["bin"]` over `DEFAULT_BIN`) and stays
byte-unchanged; the defect was the test reading the ambient environment
before it cleared it.

(a) Pre-fix failure, on the old bytes:

```
$ PI_BIN=/x python3 -m pytest extensions/agi/tests/test_adapters.py -q
FAILED test_pi_bin_env_var_wins_over_config
AssertionError: assert '/x' == '/from/config'
1 failed, 34 passed
```

The first assertion ran before any `delenv`, so an exported `PI_BIN` -- which
this box's profile and `tmux -g` both set -- leaked in.

(b) Fix: added `monkeypatch.delenv("PI_BIN", raising=False)` as the first line
after `adapters.load("pi")`, before the config assertion. The env-set half
(`setenv` + env assertion) is unchanged; no assertion weakened, no skip.

(c) Built bytes, three environments:

```
$ PI_BIN=/x        python3 -m pytest extensions/agi/tests/test_adapters.py -q  -> 35 passed
$ env -u PI_BIN    python3 -m pytest extensions/agi/tests/test_adapters.py -q  -> 35 passed
$ export PI_BIN=/leaky; ...                                                -> 35 passed
```

`git diff --numstat` over production paths (all non-test paths) is empty:
`pi_adapter.py` is byte-unchanged. production_lines = 0.

## Evidence

- Pre-fix: `1 failed, 34 passed` with `PI_BIN=/x`; `assert '/x' == '/from/config'`
- Post-fix: `35 passed` under `PI_BIN=/x`, `env -u PI_BIN`, and `PI_BIN=/leaky`
- `git diff --numstat -- . ':!*tests*'` -> no output (0 production lines)
- `pi_adapter.py` resolve_bin unchanged: `os.environ.get("PI_BIN") or harness.get("bin") or DEFAULT_BIN`

## Verdict

proved -- the test is now hermetic to an ambient `PI_BIN` in both directions,
with the adapter byte-unchanged.

## Agent Notes
delenv(PI_BIN, raising=False) added as first line of test_pi_bin_env_var_wins_over_config; pre-fix failed under PI_BIN=/x, post-fix 35 passed under PI_BIN=/x, env -u PI_BIN and PI_BIN=/leaky; pi_adapter.py byte-unchanged, production_lines=0

kid a00-03da18ea implemented the g15 build order: monkeypatch.delenv(PI_BIN, raising=False) before the config assertion in test_pi_bin_env_var_wins_over_config. Parent probes (gate / auth / wire) all hold; removing the byte fails under ambient PI_BIN=/x and passes without it, a planted wrong ambient is refused, and resolve_bin reads os.environ at call time. 35 passed under PI_BIN=/x and under env -u PI_BIN; test count unchanged (35); pi_adapter.py byte-unchanged. Accepted, no demotion.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review by a00-04514f17, EF.14 -- I read the kid DIFF bytes, never its result file. The only changed line in extensions/agi/tests/test_adapters.py is monkeypatch.delenv("PI_BIN", raising=False), inserted between pi = adapters.load("pi") and the first assertion; the env-set half and every other assertion are untouched, and pi_adapter.resolve_bin still reads os.environ.get("PI_BIN") or harness.get("bin") or DEFAULT_BIN. Three parent-run negative probes, on copies in my own scratch dir, never on the shared tree: (gate) a copy of this exact test with that one byte removed FAILS under ambient PI_BIN=/x with AssertionError: assert /x == /from/config, and the same mutant PASSES under env -u PI_BIN -- so the byte is load-bearing, not decoration; (auth) a wrong ambient value planted after the clear is refused by name (AssertionError: /ambient-should-not-win != /from/config), so the first assertion is a real gate and not vacuous; (wire) resolve_bin returns the env value at call time when PI_BIN is set and the config value when it is unset, proving the live call site reaches the precedence bytes. The real file run 35 passed under PI_BIN=/x and 35 passed under env -u PI_BIN, same test count as the pre-fix run (1 failed / 34 passed), so no test was removed or weakened. Accepted, no demotion: verdict proved, evidence_runs names this experiment, title is the kid own words, adapter byte-unchanged status confirmed.
<!-- THOUGHT:END -->
