---
id: goal:g7.25.1
mint_id: f41a23b73a4941708bc991009d3a1e2d
type: goal
parents:
  - goal:g7.25
next_edges: []
confidence: 0.9
edited_by: director-belam
goal_id: G7.25.1
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 414f99f953ab50bb
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - grok-bot
  - adapter
thought_session: g7.25.1-body-standing-2026-09-21
title: "G7.25.1: grok_bot_adapter.py REQUIRED surface (stub build_command; needs_credential False)"
town: core
---
# goal:g7.25.1

## Why this exists

**Parent `goal:g7.25` (Grok Bot third-party harness adapter).** Parent needs the adapter *module* before a config row can resolve. This subgoal owns **only** `extensions/agi/bin/adapters/grok_bot_adapter.py` — TODAY's REQUIRED surface — so `adapters.load("grok_bot")` can succeed once g7.25.2 lands the config row.

Practice-run split (owner / Belam): adapter file here; `harnesses.grok-bot` config row is **sibling `goal:g7.25.2`**, not this node.

## Target end-state

- One module `grok_bot_adapter.py` defines the same REQUIRED surface peers use: `NAME`, `resolve_bin`, `model_args`, `build_command`, `child_env`, `is_alive`, `restart`, `needs_credential`.
- `NAME == "grok-bot"`.
- `build_command(...)` returns a **stub measurable argv** (`<bin> [--model M] -p <context_file>`) — CLI flags are not guessed from `--help` yet.
- `restart(...)` is a **real respawn** (rebuild argv → detached Popen → stamp pid), not a stub refuse.
- `needs_credential(...)` is explicitly **False** (Grok Bot auth is its own channel; no OpenRouter mint).
- **Zero** edits to `dispatch.py` for grok / grok-bot / grok_bot.
- Build/test graph nodes sanction the bytes (`write.py` / write-log), with `payload_ref` where required.

## Invariants

- **No `dispatch.py` grok teaching** — grep hits for `grok` / `grok-bot` / `grok_bot` in `dispatch.py` stay zero (comments-about-harnesses-in-the-abstract do not count as teaching).
- Adapter is a named harness module, not a town and not a fork of read/write/dispatch/workflow/send.
- Chain growth for directors stays on **pi parents** via unified dispatch; this adapter does not move parent/kid work onto Grok Bot.
- **No new remote heads. No MAIN push from this seat.**
- Config row `harnesses.grok-bot` is **not** authored here (Belam / `goal:g7.25.2`).

## Falsifier

1. `python3 -c 'from extensions.agi.bin.adapters import adapters; m=adapters.load("grok_bot"); assert all(hasattr(m,n) for n in adapters.REQUIRED)'` — or the project's equivalent `adapters.load("grok_bot")` path — succeeds once a config row exists; **missing any REQUIRED name fails at load** with the existing AdapterError shape. Until g7.25.2 lands the row, prove the module imports and defines every REQUIRED name by direct import of `grok_bot_adapter`.
2. `needs_credential({...}) is False`; `is_alive(os.getpid())` is True; `build_command` returns a list whose first element is the resolved bin and that includes `-p` + context path; `restart` is callable and rebuilds that argv (not `NotImplementedError` for stub-argv reasons).
3. `grep -E 'grok(-bot|_bot)?' extensions/agi/bin/dispatch.py` → **zero** teaching hits (ideally absolute zero).
4. Committed tests under `extensions/agi/tests/test_grok_bot_adapter.py` pass individually (`env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q -p no:cacheprovider`).
5. Build node(s) for the adapter (and tests) exist with sanctioned write provenance / `payload_ref` as required by prior MURs.

## Out of scope

- **`harnesses.grok-bot` config row** → `goal:g7.25.2` (Prime-at-merge / Belam).
- Measured real CLI flags from `<bin> --help` (later).
- Same-harness workflow/message handback; cross-machine mesh messaging.
- Edits to pi / Claude Code / copilot adapters.
- Seating every town on Grok Bot.

## Agent Notes

Assigned to **director-belam** (CORE TOWN). Owner/Prime 2026-09-21: land of tip `8e34ec55d` HOLDs until this body matches standing template; then whole-batch MUR → numbers-only `[merge-up]`. Sibling residue tip `1e9e94b75` add/add on adapter build is Prime/ff at g7.25.2 merge (keep mint `93a56c11`). `spawn.parallel=1`. Do not author config row on this land path.
Why: parent goal:g7.25 needs one adapter module with TODAY REQUIRED surface. This subgoal owns extensions/agi/bin/adapters/grok_bot_adapter.py only — NAME, resolve_bin, model_args, build_command (stub measurable argv), child_env, is_alive, restart, needs_credential=False. Zero dispatch.py. Measured CLI flags later.

standing body fleshed 2026-09-21 for format gate
