---
id: experiment:grok-bot-measured-help-argv-bare-bin
mint_id: f811e7f2d7d141ff9894b7fb415548de
type: experiment
parents:
  - hypothesis:a00-f3aa6117-51a010
next_edges: []
edited_by: a00-f3aa6117
evidence_runs:
  - experiment:grok-bot-measured-help-argv-bare-bin
line_ceiling: 40
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 27
profile: balanced
role: kid
scaffold_hash: 874c8d2e751f7add
season: 2
title: grok-bot-cli@0.3.1 --help measured; bare-bin argv; -p/--model grep proof
town: core
---
<!-- BODY:BEGIN -->
# experiment:grok-bot-measured-help-argv-bare-bin

## Experiment

Run by kid `a00-f3aa6117` under `goal:g7.31.1.1`, 2026-09-21. Scratch dir
`.agi/sessions/iter-DT.23/a00-f3aa6117/` (never the repo root). The box has no
installed `grok-bot` binary, so the published npm package is the measurement
surface.

### Install + measure (grok-bot-cli@0.3.1)

```
mkdir measure-0.3.1 && cd measure-0.3.1 && npm init -y
npm install grok-bot-cli@0.3.1 --no-audit --no-fund     # added 1 package
node_modules/.bin/grok-bot --help                      # exit 0, 46 lines
```

The bin dir publishes both `gbot` and `grok-bot`; `grok-bot` is the exact name
in the config row's `bin` cell (`/home/ubuntu/.npm-global/bin/grok-bot`).

### Verbatim `grok-bot --help` (grok-bot-cli@0.3.1, 46 lines)

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

**`-p` and `--model` appear nowhere in it.** Real subcommands are `doctor`,
`bots`/`groups` CRUD, `send <bot-or-group> <message...>`, `thread`/`chat`,
`history`, `codex`; global flags are `--gateway`, `--files`, `--dir DIR`,
`--json`. The seat's brief travels over `send`, so `context_file` stays in the
signature but is not emitted.

### Version drift (recorded, not hidden)

| version | `--help` | note |
|---|---|---|
| 0.3.1 | 46 lines, exit 0 | last version publishing static help |
| 0.8.0 | **0 bytes**, exit 0 | bundled TUI; nothing on stdout |
| 0.9.0 (`latest`) | **0 bytes**, exit 0 | bundled TUI |

0.8.0 and 0.9.0 were also re-run under a pty (`pty.fork` + `execv`); both still
produced **0 bytes**. So the measurement is pinned to 0.3.1 by necessity, and
the bound is «published package 0.3.1», not «the box binary» (which does not
exist) and not «npm latest» (which emits no help at all).

### Before → after (grep proof, `-p`/`--model`)

Before (adapter sha256 `66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c`):

```
$ grep -n -- '\-p\|--model' extensions/agi/bin/adapters/grok_bot_adapter.py
39:    """models[tier] -> --model; ...
48:    return ["--model", model.strip()] if ...
62:    """STUB argv: `<bin> [--model M] -p <context_file>`.
66:            "-p", str(context_file)]

$ build_command(...)  ->  ['/home/ubuntu/.npm-global/bin/grok-bot',
                           '--model', 'grok-4-fast',
                           '-p', '/tmp/ctx.md']
```

After (adapter sha256 `630e5ef976b4b9c484ac719ac2059a374d387bbfd94df6d3638a6b274ee591e4`):

```
$ grep -n -- '"-p"\|"--model"' extensions/agi/bin/adapters/grok_bot_adapter.py
(no output; exit 1)

$ build_command(...)  ->  ['/home/ubuntu/.npm-global/bin/grok-bot']
```

The `--model` guess is retired: `model_args` is now a VALIDATION-ONLY helper
that always returns `[]` and never emits a flag. It is still called by
`build_command` so the named-tier `KeyError` contract survives:

```
$ build_command(harness={'adapter':'grok_bot','models':{'kid':'x'}}, tier='parent')
KeyError: harness 'grok_bot' declares no model for tier 'parent'; known tiers: ['kid']
```

No measured global flag is emitted: the row declares no `--dir`/`--gateway`
cell, and the subprocess already runs in the seat worktree (`_restart_cwd`), so
`--dir` would be redundant. `--model` is a Grok Bot app/profile field, not a
CLI flag.

### Measurement-bound test

The tautological restart assert (`build_command == build_command`) was replaced
by `test_argv_is_bound_to_the_recorded_help`, which pastes the recorded 0.3.1
help as a module constant and asserts every `-`-prefixed argv token appears in
it, `-p`/`--model` are absent, and argv[0] is `resolve_bin`; plus
`test_no_model_flag_survives_into_argv`, asserting the full argv is the bare
resolved bin. Restart now additionally asserts `args == [RESTART_HARNESS["bin"]]`.

### Results

```
$ python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q
17 passed in 1.38s

$ grep -Ein grok extensions/agi/bin/dispatch.py extensions/agi/bin/rotate.py | wc -l
0
```

Production diff: `git diff --numstat -- extensions/agi/bin/adapters/grok_bot_adapter.py`
-> `27  15` (27 added, 15 removed; ceiling 40). No `dispatch.py` / `rotate.py` /
`.agi/config.json` edit.

## Evidence

Recorded files (scratch, not committed): `help-0.3.1.txt` (46 lines),
`measure-0.9.0/help-0.9.0.txt` and `measure-0.8.0/help-0.8.0.txt` (0 bytes),
plus the pty re-runs (`help-pty-0.9.0.txt`, `help-pty-0.8.0.txt`, both 0 bytes).

## Bound

The recorded help is 0.3.1, the last static-help release; the box path
`/home/ubuntu/.npm-global/bin/grok-bot` is unverified on this box and the
adapter does not depend on it existing — argv carries it from the config cell.
