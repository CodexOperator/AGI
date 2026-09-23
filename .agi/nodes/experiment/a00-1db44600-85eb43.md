---
id: experiment:a00-1db44600-85eb43
mint_id: 3227e43cc5de40d79fffc828cec8fdb5
type: experiment
parents:
  - hypothesis:a-restarted-agent-gets-the-same-render-as-its-first-spawn
next_edges: []
confidence: 0.95
edited_by: a00-39a3b18e
evidence_runs:
  - experiment:a00-1db44600-85eb43
loop: hypothesis:a-restarted-agent-gets-the-same-render-as-its-first-spawn@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "sites", "class": "wire", "cmd": "python3 probe_wire_restore.py: save pi.child_env, pytest.main(restart-render file), assert adapters.load(pi).child_env is the saved real fn", "expected": "PYTEST_RC=0 and CHILD_ENV_RESTORED=True -- monkeypatch undoes the stub in a LIVE session, not just pytest bookkeeping", "observed": "PYTEST_RC=0; CHILD_ENV_RESTORED=True; child_env is the real function", "result": "held"}
  - {"conjunct": "sweep", "class": "gate", "cmd": "probe_gate_ast.py: AST-walk the test file flagging Attribute/Subscript assignment targets, raw setattr, globals(), non-monkeypatch setattr", "expected": "zero remaining module/global mutations; only monkeypatch.setattr writes", "observed": "2 hits (self.kw L75 in _CapturingAdapter, captured[argv] L136 in _capture_popen) -- both instance/local-container writes, zero module/global rebinds", "result": "held"}
  - {"conjunct": "ordered-run", "class": "wire", "cmd": "pytest test_dispatch_restart_render.py test_*adapter*.py test_dispatch_render_thread.py -q IN THAT ORDER", "expected": "all green on the changed bytes; red was 9 failed on the pre-fix bytes", "observed": "154 passed, 3 warnings", "result": "held"}
  - {"conjunct": "hygiene-only", "class": "gate", "cmd": "git diff --numstat 6b5f61ef7c..a19f89326c -- extensions/agi/bin/ ; git diff --name-only 6b5f61ef7c..a19f89326c", "expected": "zero engine bytes; only the test file and the kid node changed", "observed": "numstat empty; name-only = node .md + test_dispatch_restart_render.py", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 1bbb34803fd2b21e
season: 2
title: "Test hygiene: monkeypatch the adapter child_env stub so the restart-render file cannot contaminate later adapter tests"
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1db44600-85eb43

## Experiment

The pre-fix file mutated the loaded adapter module directly at two points:

```
150:    mod.child_env = lambda **kw: {}
171:    mod.child_env = lambda **kw: {}
```

`adapters.load(name)` returns a cached module object, so that assignment outlived the test and the real `child_env` never came back for the rest of the pytest session. Running the restart-render file FIRST, then `test_*adapter*.py`, produced 9 failures on the merged EF.65 tip `6b5f61ef7c` (inherited from round-1 director measurement).

Fix — test hygiene only, no engine bytes:

| Site | Before | After |
|---|---|---|
| `test_adapter_restart_carries_the_render_into_its_argv` | `mod.child_env = lambda **kw: {}` | `monkeypatch.setattr(mod, "child_env", lambda **kw: {})` |
| `test_grok_restart_accepts_the_render_without_dying` | `mod.child_env = lambda **kw: {}` | `monkeypatch.setattr(mod, "child_env", lambda **kw: {})` |

Both tests already took `monkeypatch`, so the stub is now torn down at test end.

### Sweep for other direct mutations

Every other `X = Y` in the file is a local binding or a fixture arg; the only
module/global assignments were the two `mod.child_env` lines above:

```
grep -nE '^\s*[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*\s*=[^=]' \
    extensions/agi/tests/test_dispatch_restart_render.py
# -> all hits are locals (BIN, RENDERED, sess, rec, fake, ...); no other
#    module/global rebind.
```

## Evidence

Order-coverage proof (new file FIRST, then the adapter files) — the exact
scenario the 9 failures came from. `-q`, tail:

```
$ python3 -m pytest extensions/agi/tests/test_dispatch_restart_render.py \
      extensions/agi/tests/test_*adapter*.py -q
........................................................................ [ 48%]
........................................................................ [ 97%]
...                                                                      [100%]
147 passed, 3 warnings in 3.48s
```

Walk-away file alone:

```
$ python3 -m pytest extensions/agi/tests/test_dispatch_restart_render.py -q
............                                                             [100%]
12 passed in 0.10s
```

Round's other tests:

```
$ python3 -m pytest extensions/agi/tests/test_dispatch_render_thread.py -q
.......                                                                  [100%]
7 passed in 0.17s
```

Production-lines measurement (the one allowed git read):

```
$ git diff --numstat -- extensions/agi/bin/
# (empty)  <- zero engine bytes changed, as the brief required
$ git diff --numstat -- extensions/agi/tests/test_dispatch_restart_render.py
2       2       extensions/agi/tests/test_dispatch_restart_render.py
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by parent a00-39a3b18e, EF.65. (1) SAID: "build both through monkeypatch.setattr(mod, child_env, ...); sweep the file for any other direct module/global assignment" and "pytest test_dispatch_restart_render.py test_*adapter*.py IN THAT ORDER -> all green (red on round 1 bytes)". (2) MACHINE: the kid diff 6b5f61ef7c..a19f89326c carries exactly two byte changes -- mod.child_env = lambda **kw: {} becomes monkeypatch.setattr(mod, child_env, lambda **kw: {}), at the two former sites. My probes, not its suite: an in-process restore probe shows adapters.load(pi).child_env is the real function AFTER the file runs (monkeypatch undo reaches live module state); an AST sweep flags only self.kw L75 and captured[argv] L136 -- instance/local-container writes, zero module/global rebinds; the full ordered set is 154 passed; git diff over extensions/agi/bin is empty, name-only is node + test file. (3) NEAR MISS: a fix that only guards the two visible lines and leaves e.g. a monkeypatch-free setattr, a sys.modules write, or a module attribute set through a fixture, would satisfy the words "build both through monkeypatch" and still poison the session -- the AST probe is what closes that. (4) DEVIATION: none from the brief; engine code untouched as ordered. Verdict proved on the kid claim (test hygiene); the target hypotheses restart-carry conjuncts ride on round 1 experiment:a00-3006fda7-3969ab, merged here, not on this kid.
<!-- THOUGHT:END -->

## Agent Notes
Routed both direct mod.child_env assignments through monkeypatch.setattr; swept for other module/global mutations (none); order run now 147 passed where it was 9 failed; 0 production lines.
