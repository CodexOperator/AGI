---
id: experiment:dt27-grok-bot-residues-measured-guards
mint_id: 3c3249d741ae40b5851b90bcf7a8cc5f
type: experiment
parents:
  - hypothesis:a00-235b44ae-6a3246
next_edges: []
edited_by: a00-235b44ae
line_ceiling: 40
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 17
profile: balanced
role: kid
scaffold_hash: a9176634a3982f98
season: 2
title: "DT.27 R1/R2/R3 closed: liveness guard red on no-op, non-vacuous binding, AGI_MODEL stamped"
town: core
---
<!-- BODY:BEGIN -->
# experiment:dt27-grok-bot-residues-measured-guards

## Experiment

Run by kid `a00-235b44ae` under `goal:g7.31.1.1`, DT.27, base `f474a2952`.
Corrective round from director-belam after MUR
`mur-g7-31-1-1-dt-23-f474a2952-lean2` (`accept_with_residue`). Scratch dir
`.agi/sessions/iter-DT.27/a00-235b44ae/` (never the repo root). No pane hold
implemented; no new argv path; no `dispatch.py` / `rotate.py` edit.

### R1 — restart certified a measured no-op (PRIMARY)

The old `test_restart_returns_the_new_pid_and_stamps_the_record` asserted
`captured["args"] == [RESTART_HARNESS["bin"]]` — it pinned the bare-bin argv,
which on grok-bot-cli@0.3.1 prints help and exits, as the *correct* restart.

Fix, in three measured parts:

1. `test_restart_passes_through_the_built_argv` monkeypatches `build_command`
   to return a sentinel `["/sentinel/bin", "--dir", "/sentinel"]` and asserts
   Popen received exactly it (and NOT `[bin]`). A restart that hardcodes its
   own argv goes red.
2. `test_restart_spawns_a_live_process_and_is_killable` is the liveness half:
   the injected argv really runs (`sys.executable -c "…time.sleep(30)"`), and
   the pid must be `is_alive` at t=0 AND after a 0.25 s survival window.
3. `test_bare_bin_respawn_is_a_recorded_noop_residue` states the honest fact:
   the bare-bin respawn carries no subcommand from the recorded help, names
   `goal:g7.31.1.2` as the owner, and goes red the day a subcommand lands.

The 0.25 s window is load-bearing and was measured, not assumed
(`.agi/sessions/iter-DT.27/a00-235b44ae/probe_liveness.py`):

```
live argv  (t=0, t=0.25): (True, True)
no-op argv (t=0, t=0.25): (True, False)
```

A t=0-only assert was a race — `sys.executable -c pass` reads ALIVE in the
first scheduling slice. With the window, the guard is red on a no-op argv and
green on a live one: it is able to fail.

The old `[bin]` pin was deleted from the stamping test; it now keeps only the
compositional asserts (spawn detached, cwd = record worktree, pid/status/
restarted_at stamped).

### R2 — recorded-help binding was vacuous (PRIMARY)

`for tok in argv[1:]` never ran: `build_command` returns a one-element list, so
`-p` / `--model` absence was trivially true and the help bound nothing.

Fix: the binding is extracted into a token-aware predicate and exercised on
fabricated multi-token argv.

- `_documented_tokens()` splits the recorded help and strips `[]()|,:` — so
  `[--json]` reduces to `--json`, and `-p` is NOT found inside the documented
  `--path` (a substring test would have accepted the guess).
- `_unbound_tokens(argv)` returns the un-documented flag tokens.
- `test_the_binding_predicate_is_falsifiable` measures the rejection:
  `["--model","grok-kid"] -> ["--model"]`, `["-p","/tmp/ctx.md"] -> ["-p"]`,
  `["--json","--dir","/x"] -> []`.
- `test_argv_is_bound_to_the_recorded_help` keeps the real-argv assert
  (`_unbound_tokens(argv) == []`) plus argv[0] = resolved bin.

There is now at least one token (`--model`, `-p`) whose presence the binding
rejects.

### R3 — configured tier discarded on the grok path (PRIMARY)

`model_args` returned `[]` and `child_env` accepted `tier` but ignored it.
dispatch.py:2542 exports `AGI_MODEL` on the main spawn path, but `restart`
calls `child_env(base=dict(os.environ))` — invoked from heal/rotate that env may
carry no `AGI_MODEL`, and the tier was silently dropped.

**Closed** in the adapter: `child_env` now stamps the ROW's `models[tier]` into
`AGI_MODEL` (the row is authoritative — dispatch has already landed ladder/seat
overrides into that cell — so it wins over a stale inherited value). Measured:

```
restart Popen env[AGI_MODEL]: grok-parent    # tier="parent", row grok-4
```

Tests: `test_configured_tier_reaches_the_spawn_env_not_argv` (kid -> grok-kid,
parent -> grok-parent, stale inherited value overridden, no tier/no models ->
nothing invented) and `test_live_tier_cell_reaches_the_spawn_env` (reads the
REAL `.agi/config.json` row read-only).

**Re-scoped, measured**: `test_recorded_help_names_no_model_selector_so_residual_is_the_cli`
asserts the recorded 0.3.1 help names no `--model` and no model env var; its
only env names are the auth/agents/history/codex ones quoted there. Whether
`grok-bot-cli` CONSUMES `AGI_MODEL` is the CLI's app/profile field — **that is
where the residual now lives**, named, not dropped.

## Evidence

Base tree, before changes:

```
$ python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q
17 passed in 1.16s
```

After changes (test files named, never the bare tests dir):

```
$ python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q
24 passed in 1.09s

$ python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py \
      extensions/agi/tests/test_adapters.py -q
59 passed in 3.01s

$ python3 -m pytest extensions/agi/tests/test_claude_code_adapter.py \
      extensions/agi/tests/test_copilot_cli_adapter.py -q
64 passed in 12.79s
```

Falsifiers of `goal:g7.31.1.1` still hold on the bytes:

```
$ grep -Ein grok extensions/agi/bin/dispatch.py extensions/agi/bin/rotate.py | wc -l
0
$ grep -n -- '"-p"\|"--model"' extensions/agi/bin/adapters/grok_bot_adapter.py
(no output; exit 1)
```

Production lines, measured with the one permitted read-only `git diff`:

```
$ git diff --numstat -- extensions/agi/bin/adapters/grok_bot_adapter.py
17	2	extensions/agi/bin/adapters/grok_bot_adapter.py
```

17 added / 2 removed (ceiling 40, under). No `dispatch.py` / `rotate.py` /
`.agi/config.json` edit. `line_ceiling: 40`, `production_lines: 17`.

Probe kept as evidence (scratch, not committed):
`.agi/sessions/iter-DT.27/a00-235b44ae/probe_liveness.py` plus its transcript
in `probe-liveness.out`.

## Bound

Durable pane hold / a respawn that keeps a live seat process is OUT OF SCOPE
(`goal:g7.31.1.2`); the bare-bin respawn stays a recorded residue with a
tripwire. The recorded help is 0.3.1 (last static-help release) — `latest`
0.9.0 and 0.8.0 print 0 bytes even under a pty (measured DT.23). The box has no
installed `grok-bot` binary, so the liveness guard injects its own live argv
rather than depending on the config `bin` path existing.
