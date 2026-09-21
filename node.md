---
id: mvp:grok-bot-adapter-minimum
mint_id: ba9d39ff53f845b6aed3b27a00db481e
type: mvp
parents:
  - verdict:grok-bot-bare-bin-holds
next_edges: []
edited_by: a00-fcfbc2f9
loop: goal:g17.14.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 3bf26cccea5f3d3e
season: 2
title: "Minimum Grok Bot adapter: REQUIRED surface, no credential, stub argv, bare PATH bin"
town: core
---
<!-- BODY:BEGIN -->
# mvp:grok-bot-adapter-minimum

## MVP

The minimum `extensions/agi/bin/adapters/grok_bot_adapter.py` must satisfy, and
nothing more (the CLI flag surface is LOCKED Belam practice — a stub, not a
measured CLI):

- `NAME == "grok-bot"` — the harness string seats and config use.
- every name in `adapters.REQUIRED` present and **callable**:
  `build_command`, `child_env`, `is_alive`, `restart`, `needs_credential`;
  `adapters.load("grok_bot")` succeeds with zero edits to `dispatch.py`.
- `needs_credential(harness)` returns explicit `False` — Grok Bot uses its own
  auth channel, so no OpenRouter key is minted.
- `model_args` raises `KeyError` **by name** for a tier the harness does not
  declare — never a silent fallback to another tier's model.
- `build_command` returns the locked stub argv
  `[<bin>, [--model M], "-p", <context_file>]`.
- `restart` raises `NotImplementedError` naming the unmeasured flags.
- `DEFAULT_BIN` is a **bare PATH name** (`"grok-bot"`); the box path lives in
  the config `harnesses.grok-bot.bin` cell (`goal:g17.14.2`), so no
  `/home/<user>` literal is baked into the file.

## Inputs

A `harness` dict from config (`bin`, `models`, optional `env` / `forward_env`),
a `tier`, and a `context_file` path; plus the process environment
(`$GROK_BOT_BIN` is the top of the `resolve_bin` precedence).

## Outputs

An argv list for `Popen`, a child environment dict, a liveness bool, and a
`needs_credential` decision.

## Falsifier

Any of the above failing on the built bytes; a `paths.py audit` hit on the
file; or a `grok` occurrence in `dispatch.py`.

## Out of scope

Measured Grok Bot CLI flags — `build_command` stays a stub and `restart` stays
refused until `<bin> --help` is read.
<!-- BODY:END -->
