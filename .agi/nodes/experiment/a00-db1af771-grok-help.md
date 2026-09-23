---
id: experiment:a00-db1af771-grok-help
mint_id: 9730a3a3da5d4808be848933ba99e765
type: experiment
parents:
  - hypothesis:a00-db1af771-f25152
next_edges: []
edited_by: a00-081f0854
evidence_runs:
  - experiment:a00-db1af771-grok-help
line_ceiling: 40
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "GROK_BOT_BIN=/ENV/SENTINEL build_command(harness bin=/ROW/SENTINEL)", "expected": "argv[0] is the env sentinel", "observed": "['/ENV/SENTINEL']", "result": "PASS"}
  - {"conjunct": 1, "class": "gate", "cmd": "build_command(models={kid:m}, tier=parent)", "expected": "KeyError naming the tier, never a fallback", "observed": "KeyError: \"harness 'grok_bot' declares no model for tier 'parent'; known tiers: ['kid']\"", "result": "PASS"}
  - {"conjunct": 2, "class": "gate", "cmd": "build_command(context_file='-p /tmp/x')", "expected": "bare bin; the retired literal never reaches argv", "observed": "['grok-bot']", "result": "PASS"}
  - {"conjunct": 2, "class": "wire", "cmd": "build_command(harness, tier=kid, context_file=/tmp/x)", "expected": "no dash-prefixed argv token", "observed": "argv=['grok-bot'], dash_tokens=[]", "result": "PASS"}
production_lines: 18
profile: balanced
role: kid
season: 2
title: "Measured grok-bot-cli@0.3.1 --help: argv is the bare bin; -p and --model retired"
town: core
verdict: proved
---
# experiment:a00-db1af771-grok-help

Spec: `goal:g7.31.1.1` conjuncts 1 and 2 — `build_command` argv bound to a
recorded `grok-bot --help`, and the stub-only guessed flags (`-p`, `--model`)
gone from the landed adapter path.

## What was measured

`grok-bot-cli@0.3.1` installed fresh (npm, 16s, network up) into the session
scratch dir and its own bin invoked. Raw capture:
`.agi/sessions/iter-DH.170/a00-db1af771/measure/help.txt`.

- command: `./node_modules/.bin/grok-bot --help`
- exit: **0**
- stdout: **46 lines**, stderr: 0 bytes
- installed version: `0.3.1`

**Version drift noted:** prior rounds measured `0.8.0` / `0.9.0` printing 0
bytes for `--help`. `0.3.1` prints 46 lines and exits 0, so the drift this
round is *downward in semver and upward in usefulness* — the brief's expected
46-line capture reproduces exactly.

**Bound stated, not hidden:** this box has no installed `grok-bot` binary
(`/home/ubuntu/.npm-global/bin/grok-bot` from the config `bin` cell does not
exist; the box user is `belam`). The measurement surface is the published npm
package's own bin, not a box-installed harness binary. That is the same surface
the adapter's argv has to match, since the adapter emits a bare resolved bin.

### Verbatim `--help` (46 lines, exit 0)

```
gbot - manage Grok Bot agents and groups

Usage:
  gbot [--dir DIR] [--json] <command>

Commands:
  doctor
  bots list
  bots create --name NAME [--description TEXT] [--instructions TEXT] [--title TEXT]
           [--avatar-shape SHAPE] [--avatar-color COLOR]
  bots update <id-or-name> [--name NAME] [--description TEXT] [--instructions TEXT]
           [--title TEXT] [--avatar-shape SHAPE] [--avatar-color COLOR]
           [--notify on|off] [--hidden on|off]
  bots get <id-or-name>
  bots delete <id-or-name>
  groups list
  groups create --name NAME --member ID_OR_NAME [--member ...]
           [--description TEXT] [--instructions TEXT] [--title TEXT]
           [--avatar-shape SHAPE] [--avatar-color COLOR]
  groups update <id-or-name>  (same flags as bots update; members stay on set/add/remove)
  groups get <id-or-name>
  groups members <id-or-name>
  groups add <group> <bot>
  groups remove <group> <bot>
  groups set <group> --member ID [--member ...]
  groups delete <id-or-name>
  send <bot-or-group> <message...>
  thread <bot-or-group> [--limit N] [--root MESSAGE_ID] [--full]
  chat <bot-or-group>     alias for thread
  history [bot-or-group] [--search TEXT] [--limit N]  (offline)
  history --path         print the local JSONL file path
  codex status
  codex list-threads [--limit N]
  codex send <threadId> <message...>

Max group members: 6
--description / --instructions is the UI Instructions field (same key).
Avatar shapes: blob pebble bean egg squircle tablet capsule cylinder hex gem crystal wedge shield dome arch cloud teardrop leaf
Avatar colors: black brown red orange yellow green cyan blue violet magenta gray
Flags: --gateway  --files  --dir DIR  --json
Auth: GROK_BOT_GATEWAY_URL + GROK_BOT_GATEWAY_TOKEN, or the Grok Bot app session, or CURSOR_ACCESS_TOKEN
File fallback: GROK_BOT_AGENTS_DIR
Codex: talks to the local app-server daemon socket under CODEX_HOME (default ~/.codex)
History: opt-in plaintext JSONL at ~/.grok-bot-cli/history.jsonl
         GROK_BOT_HISTORY=on to record; --history-dir / GROK_BOT_HISTORY_DIR to relocate
         --no-history to skip one command
```

**Reading of the capture:** it names no seat argv flag at all — no `-p`, no
`--model`, no prompt/context flag. It is a group/agent management CLI whose
per-command flags (`--name`, `--member`, `--limit`, …) are not the harness
spawn argv. So the honest measured argv is the **bare resolved bin**, and any
flag beyond `argv[0]` would be a guess the capture does not support.

## What changed

`extensions/agi/bin/adapters/grok_bot_adapter.py` (only this file):

- `build_command` -> `[resolve_bin(harness)]`. It still calls
  `model_args(harness, tier)` for validation, so a missing tier raises on the
  spawn path; `context_file` stays in the signature for seam compatibility but
  is not emitted (the seat brief travels over `send`, separate goal).
- `model_args` -> validation only, always returns `[]`, emits no flag.
- Module docstring updated from "stub argv" to "MEASURED argv".

## Before / after grep proof (adapter path only)

```
$ grep -n '"-p"\|"--model"' extensions/agi/bin/adapters/grok_bot_adapter.py
(no match, exit 1)          # emitted literals are gone

$ grep -nE '(^|[^[:alnum:]_-])-p([^[:alnum:]_-]|$)' extensions/agi/bin/adapters/grok_bot_adapter.py
(no match, exit 1)

$ grep -nE '(^|[^[:alnum:]_-])--model([^[:alnum:]_-]|$)' extensions/agi/bin/adapters/grok_bot_adapter.py
(no match, exit 1)
```

Before the edit, `build_command` literally held `"-p", str(context_file)` and
`model_args` held `["--model", model.strip()]`. A naive `grep -- '-p'` has a
false positive on doc prose ("is-provider-gated"); the token-level regex above
is the clean statement and is the one recorded.

## Test

`extensions/agi/tests/test_grok_bot_adapter.py` (only this file): the verbatim
46-line capture is embedded as `RECORDED_HELP` and bound to the emitted argv by
`test_argv_is_bound_to_the_recorded_help` (argv[0] == `resolve_bin`, every
dash token must appear in the capture, `-p`/`--model` absent), plus three probe
tests (env sentinel -> argv[0], missing tier still raises, `context_file="-p
/tmp/x"` never leaks). The restart test's "stub argv today" comment is updated.

```
$ python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q
19 passed
```

Scratch receipt: `.agi/sessions/iter-DH.170/a00-db1af771/probes.json` (probes
run: 4/4 PASS), `probes.py`, `measure/help.txt`, `measure/help.err` (empty).

## Production lines

`git diff --numstat -- extensions/agi/bin/adapters/grok_bot_adapter.py`
-> `18 14`; production_lines = 18 additions, ceiling 40.

## Caveat

The binding test is necessarily **vacuous on flags today**: the measured argv
carries zero dash tokens, so "every emitted flag appears in the capture" holds
trivially. The non-vacuous guards are the capture itself (46 lines, `--dir`
present, real text) and the explicit `-p`/`--model` absence asserts. A future
adapter that emits a flag must now add it to `RECORDED_HELP` or fail.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT a00-081f0854 review of kid a00-db1af771 (DH.170), read from the diff not the result file. The adapter diff is exactly what the goal asks: build_command -> [resolve_bin(harness)], model_args kept as validation-only (no emitted -p/--model), context_file accepted but not emitted. The test diff embeds the capture verbatim and binds argv to it. Independent checks I ran: the measure bin re-run reproduces help.txt identically (46 lines, empty stderr); the RECORDED_HELP literal in the test is byte-identical to .agi/sessions/iter-DH.170/a00-db1af771/measure/help.txt (2117 chars, 46 lines); node_modules/grok-bot-cli/package.json declares 0.3.1. Parent probes: GROK_BOT_BIN sentinel wins argv[0]; harness bin sentinel threads; declared models with the tier absent still raises KeyError naming the tier; context_file that looks like the retired flag plus --model still returns bare [bin]; token grep of emitted literals clean (rc 1). pytest extensions/agi/tests/test_grok_bot_adapter.py -> 19 passed. What keeps this a lean and not a bare proved: conjunct 2 names core/season2/main, and main still carries the stub (sha 66b7891f...) until the loop merges this branch; that merge is the loop owner, not a kid. The binding assertion is vacuous while the argv carries zero dash tokens, which the kid named honestly; the non-vacuous guards are the real 46-line capture and the explicit absence asserts.
<!-- THOUGHT:END -->

## Agent Notes
PARENT REVIEW (a00-081f0854, DH.170): accepted, lean_proved 90. Diff read: adapter emits bare resolved bin, -p/--model retired, tier KeyError preserved; test binds argv to a byte-identical 46-line grok-bot-cli@0.3.1 capture. Parent probes all hold (env/bin threading, missing-tier KeyError, context_file=-p no leak, grep clean); 19 tests pass. Residue: conjunct 2 names core/season2/main and main is still the stub — the fix lands only when this loop branch merges; the loop owns that merge.
