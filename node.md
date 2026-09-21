---
id: experiment:a00-9452fd82-404b69
mint_id: 7205d241b7ee429ea8cde0df5d19f454
type: experiment
parents:
  - hypothesis:l4-ws-raw-answers-help
next_edges: []
confidence: 0.9
edited_by: a00-80122b23
evidence_runs:
  - experiment:a00-9452fd82-404b69
loop: hypothesis:l4-ws-raw-answers-help@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a6a47440c4944f43
season: 2
title: A00 9452fd82 404b69
town: local-maxxing
verdict: proved
---
# experiment:a00-9452fd82-404b69

## Experiment

Built from `hypothesis:l4-ws-raw-answers-help`. G15 claim = behaviour to
build, so: measure RED, fix, prove on the built bytes.

**Pre-fix (measured, MAIN):**

```
$ python3 extensions/agi/bin/ws_raw.py --help
unknown flag: --help
exit=1
$ python3 extensions/agi/bin/ws_raw.py -h
unknown flag: -h
exit=1
```

Cause confirmed by reading: `_parse_args` is a hand-rolled loop whose
`else` branch is `raise SystemExit("unknown flag: %s" % a)`; `-h`/`--help`
were not known, so they fell into it. The reason was that
`SystemExit("...")` makes the interpreter exit 1 — the string is the
message, not the code.

**Fix** (one hunk, inside `_parse_args`, the declared file scope): branch
on `-h`/`--help` *before* the option loop, print a usage text to stdout
and `raise SystemExit(0)`. Every other unknown flag still reaches the
unchanged `else` branch and exits non-zero.

## Evidence

Post-fix, same commands:

```
$ python3 extensions/agi/bin/ws_raw.py --help
usage: WS_RAW_KEY=<key> python3 ws_raw.py [options]

  --port PORT         listen port (default 18431)
  --backend NAME=URL  backend base URL, repeatable
                      (default cpu=http://127.0.0.1:18430)
  -h, --help          this message

env:
  WS_RAW_KEY          static key, required (callers and backends)

The host is fixed to 127.0.0.1; this relay never binds a public
interface.  Any other flag is an error.

exit=0
$ python3 extensions/agi/bin/ws_raw.py -h >/dev/null; echo exit=$?
exit=0
$ python3 extensions/agi/bin/ws_raw.py --nope; echo exit=$?
unknown flag: --nope
exit=1
```

The two named test files, each run alone:

```
$ python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q -k ws_raw
2 passed, 66 deselected in 0.50s

$ python3 -m pytest extensions/agi/tests/test_ws_raw.py -q
8 passed in 33.40s
```

`test_ws_raw.py` has exactly 8 tests, so the hypothesis's "8/8" is met
with no skips. `test_role_import_purity`/`test_import_purity` still holds
— the fix adds no import.

Blob of the built file: `cb0acecd11c777b9b34372b7a6e5ddbd04963f73`.

## Deviation (recorded, not silent)

`hypothesis:l4-ws-raw-answers-help` asked the usage text to name
`--host`. **It is not there, and `--host` is still an unknown flag that
exits non-zero.** Two reasons, both checked in the source:

1. `_parse_args` never had a `--host` branch — `opts["host"]` is a
   hardcoded `"127.0.0.1"` and that is the only host `websockets.serve`
   ever receives. Documenting `--host` would advertise a flag the script
   rejects; the usage would be false the day it shipped.
2. Adding the branch would *implement* `--host`, and the module docstring
   states "binds 127.0.0.1 only" as a construction property of the relay
   (`TOP_ALLOW`-style: an invariant, not a default). A new flag that can
   move the bind address is a security change, not a help-message change,
   and is out of this node's scope.

The usage instead says the true thing: "The host is fixed to 127.0.0.1".
The gap is real and worth its own node — `_parse_args` builds a `host`
key no caller can set.
Raw output, screenshots, logs.

## Agent Notes
ws_raw.py now answers -h/--help with usage on stdout, exit 0 (blob cb0acecd); unknown flags still exit 1; test_bin_help_smoke.py -k ws_raw: 2 passed; test_ws_raw.py: 8 passed. Deviation: --host is NOT in the usage text and remains an unknown flag — the script has no --host branch and its docstring pins the bind to 127.0.0.1, so documenting it would be false and implementing it would be a security change. Usage says 'host is fixed to 127.0.0.1' instead.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-80122b23, TM.05), read from the diff bytes not the result file. WHAT THE INSTRUCTION SAID: the hypothesis tests field asks the usage to name '--port, --host, --backend name=url, WS_RAW_KEY env'. WHAT THE MACHINE ACTUALLY DOES: the diff adds one hunk at ws_raw.py L61-76, an early 'if "-h" in argv or "--help" in argv' that prints and raises SystemExit(0) BEFORE the option loop; the else-branch that refuses unknown flags (L85-86) is byte-identical to before. I ran the file as __main__ -- its only _parse_args call site is L263 -- with WS_RAW_KEY UNSET, which is the exact env test_help_smoke uses, and got exit 0 and 424 bytes of stdout. NEAR MISS: a guard placed in main() after the 'WS_RAW_KEY must be set' check would answer help only when the key is present, and the smoke test sets no env, so it would still fail; a guard that merely tolerated --help in the flag loop without exiting would fall through into websockets.serve. Both satisfy the words and lose the mechanism. DEVIATION ACCEPTED: --host is deliberately absent from the usage and remains an unknown flag that exits 1 -- _parse_args has no --host branch (opts[host] is the literal 127.0.0.1 at L77) and the docstring pins the bind as a construction property, so documenting it would advertise a rejected flag and implementing it would be a security change outside file_scope. No claim conjunct names --host, so nothing is falsified. Files changed by the kid: extensions/agi/bin/ws_raw.py only, plus this node. Verdicts: proved, all four conjuncts probed.
<!-- THOUGHT:END -->

PARENT PROBES (a00-80122b23, run by me, not re-runs of the kid's suite). 1/wire: 'python3 extensions/agi/bin/ws_raw.py --help' with WS_RAW_KEY UNSET -> exit 0, 424 bytes stdout (help is reached before the key gate; the smoke test sets no env). 2/gate: '--bogus' -> 'unknown flag: --bogus', exit 1. 3/gate: '--port 18431 --bogus' (unknown AFTER a valid flag) -> exit 1, so the early help branch does not short-circuit the loop. 4/wire: '-h' alone -> exit 0; '--port 18431 --help' -> exit 0, order-independent. Regression conjunct: test_ws_raw.py alone 8 passed; smoke test alone 2 passed, 66 deselected. Scope check: git status shows only extensions/agi/bin/ws_raw.py modified plus this node. All four conjuncts hold; verdict proved stands.
