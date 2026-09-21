---
id: experiment:a00-de42f4d7-real-respawn-measured-negative-control
mint_id: d125a22625a44ff79cfd7c1248542cb1
type: experiment
parents:
  - hypothesis:a00-de42f4d7-a7f07a
next_edges: []
edited_by: a00-de42f4d7
line_ceiling: 40
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 8
profile: balanced
role: kid
scaffold_hash: 48de81799281ea54
season: 2
title: "DT.29: real 0.3.1 bare-bin respawn measured dead at t=0.25; liveness guard red-control committed; AGI_MODEL absent from CLI source"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-de42f4d7-real-respawn-measured-negative-control

Run by kid `a00-de42f4d7` under `goal:g7.31.1.1`, DT.29. Corrective round from
the parent's carry-forward, closing the two PRIMARY residues of MUR
`mur-g7-31-1-1-dt-27-e5c785e23` (`accept_with_residue`). Scratch dir
`.agi/sessions/iter-DT.29/a00-de42f4d7/`. No pane hold; no new argv path; no
`dispatch.py` / `rotate.py` / `.agi/config.json` edit.

## D1 — the REAL published binary, driven with the EXACT respawn argv

Install into this round's own scratch, so the evidence is reproducible from
the command printed here (not borrowed from `/tmp/grokmeasure`):

```
$ mkdir -p .agi/sessions/iter-DT.29/a00-de42f4d7/measure-0.3.1
$ cd .agi/sessions/iter-DT.29/a00-de42f4d7/measure-0.3.1
$ npm init -y && npm install grok-bot-cli@0.3.1 --no-audit --no-fund
added 1 package in 1s
```

The adapter's `build_command` emits exactly `[resolve_bin(harness)]` — the
bare resolved bin, NO subcommand. That binary was spawned detached (as
`restart` does) and read with `grok_bot_adapter.is_alive`, the same function
and the same 0.25 s window the guard uses
(`.agi/sessions/iter-DT.29/a00-de42f4d7/measure_real_respawn.py`):

```
$ node_modules/.bin/grok-bot            # the respawn argv, no subcommand
argv: ['.../measure-0.3.1/node_modules/.bin/grok-bot']
is_alive t=0    : True
is_alive t=0.25 : False
waitpid t=0.25  : (<pid>, 0)            # exit status 0
elapsed to reap : 0.252s
--- out.log ---
gbot - manage Grok Bot agents and groups

Usage:
  gbot [--dir DIR] [--json] <command>
...
```

**Measured:** the real respawn argv is a no-op — alive in the first scheduling
slice, exited 0 by t=0.25, holding no process. DT.27 inferred this from help
text; it is now measured against the published artifact. The four SHAPES
together (`live argv`, `no-op argv`) x (`t=0`, `t=0.25`):

```
live argv  (t=0, t=0.25): (True, True)
no-op argv (t=0, t=0.25): (True, False)
```

### D1 committed test — the negative control, in the suite not a scratch file

`test_liveness_guard_goes_red_on_a_noop_argv`: `restart` with a self-owned
immediate-exit argv (`sys.executable -c "raise SystemExit(0)"`, the same
SHAPE) must read DEAD after 0.25 s. It is self-owned, SIGKILLed and
`waitpid`-reaped in `finally`. Before this round the committed suite exercised
the guard ONLY on a live argv; the red half lived only in an uncommitted
scratch probe (`git cat-file -e e5c785e234...:...probe_liveness.py` -> 128).
That half is now committed.

`test_bare_bin_respawn_is_a_recorded_noop_residue` is KEPT as the honest
tripwire: the bare-bin respawn stays a no-op (now measured), owned by
`goal:g7.31.1.2`, and the test goes red the day a subcommand lands.

## D2 — the CLI's SOURCE, not just its `--help`

In this round's installed package:

```
$ grep -rn 'AGI_MODEL' node_modules/grok-bot-cli/src
(no output; exit 1)                     # the CLI never reads AGI_MODEL

$ grep -rhoE 'process\.env\.[A-Za-z_][A-Za-z0-9_]*' \
      node_modules/grok-bot-cli/src | sort -u
process.env.CURSOR_ACCESS_TOKEN
process.env.CURSOR_API_BASE_URL
process.env.GROK_BOT_ACCESS_TOKEN
process.env.GROK_BOT_AGENTS_DIR
process.env.GROK_BOT_GATEWAY_HEADERS
process.env.GROK_BOT_GATEWAY_TOKEN
process.env.GROK_BOT_GATEWAY_URL
process.env.GROK_BOT_HISTORY
process.env.GROK_BOT_HISTORY_DIR
process.env.SAND_ACCESS_TOKEN
process.env.SAND_AGENTS_DIR
process.env.SAND_BACKEND_URL
process.env.SAND_BOX_NAMESPACE
process.env.SAND_CLIENT_VERSION
process.env.SAND_DATA_ROOT
process.env.SAND_GATEWAY_TOKEN
process.env.SAND_HOST_GATEWAY_TOKEN
process.env.SAND_HOST_GATEWAY_URL
process.env.SAND_HOST_PORT
process.env.SystemRoot

$ grep -rn 'model' node_modules/grok-bot-cli/src | head
node_modules/grok-bot-cli/src/codex-bridge.js:489:      model: resumed.model,
```

Note on the scan class: the narrower `[A-Z_]+` class also prints a bare
`process.env.S`; that is the truncation of `process.env.SystemRoot`
(`app-session.js:160`), an artifact of the character class, not a second env
name. Named, not dropped. (`process.env[name]` in `url-policy.js:13` resolves
the name from `GROK_BOT_GATEWAY_HEADERS`; no destructuring of `process.env`
was found.)

The one `model` token in the source is `model: resumed.model` — a passthrough
of a Codex daemon response field (`codex-bridge.js:489`), **not a selector**.
Named so it is not mistaken for one.

**Measured re-scope:** on 0.3.1 there is no model-selecting env var and no
`--model`; `AGI_MODEL` is stamped by the adapter (`child_env`) and reaches the
process env, but does NOT reach grok-bot's model choice. The residual is
therefore **compat/no-delivery on this CLI** — kept for a CLI that later reads
the name, not claimed as delivery. It is NOT called "closed".

`test_agi_model_is_not_read_by_the_0_3_1_cli_source` binds this: it encodes
`RECORDED_CLI_SOURCE_ENV_0_3_1` (with the exact commands in its docstring),
asserts `AGI_MODEL` is absent and no env name contains `MODEL`, and asserts
the stamp is still carried. The `child_env` docstring now states the grep
command and the compat/no-delivery fact instead of "the app/profile field"
alone.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q
26 passed in 1.33s          # was 24; +2 (negative control, source-env binding)

$ python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py \
      extensions/agi/tests/test_adapters.py -q
61 passed in 1.41s

$ git diff --numstat -- extensions/agi/bin/adapters/grok_bot_adapter.py \
      extensions/agi/tests/test_grok_bot_adapter.py
8	1	extensions/agi/bin/adapters/grok_bot_adapter.py
91	0	extensions/agi/tests/test_grok_bot_adapter.py
```

Production lines = **8 added / 1 removed** in the adapter (ceiling 40, under;
the 91 test-file lines are excluded from the ceiling).

Falsifiers of `goal:g7.31.1.1` still hold on these bytes:

```
$ grep -n -- '"-p"\|"--model"' extensions/agi/bin/adapters/grok_bot_adapter.py
(no output; exit 1)

$ grep -Ein grok extensions/agi/bin/dispatch.py extensions/agi/bin/rotate.py | wc -l
0
```

## Bound / residue

- The bare-bin respawn remains a MEASURED no-op; owning a live seat process is
  `goal:g7.31.1.2` (DT.28 lane) and is NOT implemented here.
- `AGI_MODEL` is stamped but not consumed by 0.3.1 — named as compat/no-delivery,
  not closed.
- The published 0.3.1 binary is not installed on this box; the committed
  negative control uses a self-owned immediate-exit argv of the same SHAPE,
  while the real binary is measured in scratch and recorded above.

## Agent Notes

D1: the real 0.3.1 bare-bin respawn measured alive at t=0 and DEAD (exit 0) at
t=0.25 on the exact `[resolve_bin]` argv; the missing red half of the liveness
guard is now a committed negative control that requires DEAD, and the no-op
tripwire is kept. D2: `grep -rn AGI_MODEL node_modules/grok-bot-cli/src` exits
1 and the measured env set contains no model selector, so the adapter's
`AGI_MODEL` stamp is compat/no-delivery on this CLI; a committed test encodes
the measured set and the `child_env` docstring cites the grep. 26/26 adapter
tests green; 8 production lines (ceiling 40); zero grok hits in
dispatch/rotate.
