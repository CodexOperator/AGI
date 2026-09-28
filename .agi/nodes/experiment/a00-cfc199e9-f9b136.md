---
id: experiment:a00-cfc199e9-f9b136
mint_id: 3de00915802c4bfc928977024addf572
type: experiment
parents:
  - hypothesis:harness-argv-refuses-unknown-encoding-and-unresolved-user-bin
next_edges: []
confidence: 0.9
edited_by: a00-99b0e554
evidence_runs:
  - experiment:a00-cfc199e9-f9b136
loop: hypothesis:harness-argv-refuses-unknown-encoding-and-unresolved-user-bin@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "tmp template bad.toml with encoding=\"json5\"; harness_template.render(\"bad\", bin_path=\"b\", settings={\"a\":1}) -- render->load->_check_parts", "expected": "HarnessTemplateError naming the unknown encoding at CHECK time (load), not at emit", "observed": "raised: <tmp>/bad.toml: argv[0] unknown encoding 'json5'; known: ['json', 'str']", "result": "HOLD"}
  - {"conjunct": 1, "class": "wire", "cmd": "same bad template inside [shapes.d]; and a known encoding=\"json\" template rendered", "expected": "unknown encoding refused in a shape too; the one live encoding still emits json bytes (no regression)", "observed": "shapes.d[0] unknown encoding 'yaml' raised; encoding=\"json\" rendered ['b','--s','{\"a\": 1}']", "result": "HOLD"}
  - {"conjunct": 2, "class": "gate", "cmd": "HOME=/tmp/probehome, PI_BIN unset: pi_adapter.resolve_bin({\"adapter\":\"pi\",\"bin\":\"~nosuchuser_xyz/bin/pi\"})", "expected": "the named FileNotFoundError naming the harness, the raw cell and $PI_BIN -- never a bare Popen error", "observed": "harness 'pi': cannot resolve binary '~nosuchuser_xyz/bin/pi': no such user's home directory; set $PI_BIN to override", "result": "HOLD"}
  - {"conjunct": 2, "class": "wire", "cmd": "the adapter entry pi_adapter.py:52 -> adapters.resolve_bin (the real spawn path); plus an EXISTING user whose file is absent, and an existing user whose file exists", "expected": "changed bytes live on the adapter path; no false positive for a real user; existing ~/ file still expands", "observed": "existing user absent file -> named refusal naming the EXPANDED path; ~/.probe_bin_xyz -> resolved to the real path", "result": "HOLD"}
  - {"conjunct": 3, "class": "gate", "cmd": "tmp template bad.toml with spread=\"extra\"; harness_template.load(\"bad\")", "expected": "the R-EF50 M4 pin: an unknown spread is refused BY NAME", "observed": "arg[0] unknown spread 'extra'; known: [19-name vocabulary]", "result": "HOLD"}
  - {"conjunct": 4, "class": "gate", "cmd": "pre-fix red: git show ef92688bd4:extensions/agi/bin/{harness_template.py,adapters/__init__.py}", "expected": "the new committed tests are RED on the pre-fix bytes", "observed": "base _check_parts loops (slot,when,spread) only (no encoding); base resolve_bin ends `if path != raw: raise ...; return raw` so ~nosuch returns raw", "result": "HOLD"}
production_lines: 20
profile: balanced
role: kid
scaffold_hash: 91c3afa4df447754
season: 2
title: Unknown encoding refused by name at check time; unresolvable ~user bin refused by name (goal:g15.29.12 conjuncts)
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-cfc199e9-f9b136

## Experiment

Two conjuncts of `hypothesis:harness-argv-refuses-unknown-encoding-and-unresolved-user-bin`, built test-first on the checkout `a00-99b0e554` (post tip).

| # | Seam | Pre-fix bytes | Fix |
|---|---|---|---|
| 1 | `harness_template.py:_check_parts` | validated `slot`/`when`/`spread` only; `_emit` turned ANY non-`json` encoding into plain `str()`, so `encoding = "json5"` emitted the wrong bytes silently | new closed `ENCODINGS = ("json", "str")` vocabulary, checked by name at load time, top-level argv AND shapes |
| 2 | `adapters/__init__.py:resolve_bin` | `~nosuchuser/bin/x` -> `os.path.expanduser` hands the raw token back -> `path == raw` -> `return raw`; `Popen` died on a bare `FileNotFoundError('~nosuchuser/...')` | `~`-prefixed raw that expands to itself now raises the named `FileNotFoundError` (harness, raw cell, `$ENV_VAR`) |

Plus the R-EF50 M4 pin: the unknown-`spread` refusal was already enforced by `_check_parts` but no test named it; a pin now does.

## Evidence

RED on the pre-fix bytes, before either source edit:

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_harness_template.py -q -k "encoding or spread"
FAILED test_unknown_encoding_is_refused_by_name_at_check_time  -- Failed: DID NOT RAISE HarnessTemplateError
FAILED test_unknown_encoding_inside_a_shape_is_refused          -- Failed: DID NOT RAISE HarnessTemplateError
2 failed, 2 passed, 55 deselected

$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_adapters.py -q -k "tilde_user"
FAILED test_an_unresolvable_tilde_user_refuses_by_name -- Failed: DID NOT RAISE FileNotFoundError
1 failed, 1 passed, 43 deselected
```

GREEN after the fix, the two named files plus every consumer:

```
python3 -m pytest extensions/agi/tests/test_harness_template.py -q   -> 58 passed, 1 skipped
python3 -m pytest extensions/agi/tests/test_adapters.py -q           -> 45 passed
python3 -m pytest test_harness_dispatch_shapes.py test_rotate_copilot_harness.py \
  test_claude_code_adapter.py test_copilot_cli_adapter.py test_grok_bot_adapter.py -q -> 109 passed
```

The four new red-then-green tests: `test_unknown_encoding_is_refused_by_name_at_check_time`, `test_unknown_encoding_inside_a_shape_is_refused`, `test_known_json_encoding_still_renders` (regression guard for the one live encoding), `test_unknown_spread_is_refused_by_name_at_check_time` (the M4 pin), `test_an_unresolvable_tilde_user_refuses_by_name`.

## Production lines

`git diff --numstat` over the two source files: `harness_template.py` +11/-0, `adapters/__init__.py` +9/-0 = **20 lines**, under the 40-line ceiling; tests excluded. No file outside FILE SCOPE touched.

## Agent Notes
Built both conjuncts test-first on a00-99b0e554: closed ENCODINGS=(json,str) validated by name in _check_parts (top-level and shapes); resolve_bin now raises the named FileNotFoundError when a ~-prefixed raw cannot expand. New tests red pre-fix, green post-fix (harness_template 58p/1s, adapters 45p, consumers 109p). 20 production lines, under the 40 ceiling.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-99b0e554, EF.77, target hypothesis:harness-argv-refuses-unknown-encoding-and-unresolved-user-bin).

(1) WHAT THE INSTRUCTION SAID. "an unknown encoding is refused by name at check time and a ~user/... bin whose user does not exist raises the named FileNotFoundError, proved by committed tests red on the pre-fix bytes (plus a pin for the spread refusal)".

(2) WHAT THE MACHINE DOES — read from the committed DIFF ef92688bd4..9fb9a09b7f, not the report. harness_template.py +11: new ENCODINGS = ("json","str") at :64; _check_parts at :172-176 raises HarnessTemplateError "unknown encoding {enc!r}" in top-level argv AND shapes. adapters/__init__.py +9: resolve_bin at :73-80 raises the named FileNotFoundError when a ~-prefixed raw does not expand (path == raw). Tests +68. Scope is exactly harness_template.py, adapters/__init__.py and their two test files; nothing outside FILE SCOPE moved.

(3) THE NEAR MISS. A fix that validated `encoding` only in _emit (raising at render) would satisfy "refused" but not "at check time": load() would still accept the bad template, so load_all()/_known_harnesses() would advertise it and only the first render would die. This fix puts the check in _check_parts (load), which is the check time. Likewise a `~user` fix that raised only inside the generic `path != raw` branch would never fire, because expanduser returns the token unchanged so path == raw.

(4) DEVIATION. None from FILE SCOPE. Parent re-read the pre-fix bytes directly (git show ef92688bd4): base _check_parts loops over (slot,when,spread) only, and base resolve_bin ends `if path != raw: raise ...; return raw` — so the two new tests are red on the pre-fix bytes exactly as the claim requires. Probes run by the parent (recorded in `probes:`), one gate per conjunct plus wire, all HOLD. Verdict accepted: proved.
<!-- THOUGHT:END -->

Parent review EF.77: diff ef92688bd4..9fb9a09b7f read (source +11/+9, tests +68, scope clean). Named files green: test_harness_template.py test_adapters.py -> 103 passed, 1 skipped. Pre-fix bytes re-read from git show ef92688bd4: no encoding check in _check_parts, resolve_bin returns raw when path==raw -- so both new tests are red on pre-fix as claimed. Five parent-run negative probes (gate per conjunct + wire + the M4 spread pin) all HOLD; recorded in probes:. Accepted proved.
