---
id: mvp:grok-bot-row-first-class-land
mint_id: 3cb39dd96ecf45e4b534fa8ca4b1cb78
type: mvp
parents:
  - verdict:grok-bot-row-landable-list-evidence
next_edges: []
edited_by: a00-d1c9f37f
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 0cac0b71f8069c47
season: 2
title: Grok-bot config row lands as a first-class harness cell
town: core
---
<!-- BODY:BEGIN -->
# mvp:grok-bot-row-first-class-land

## Interface

The config row `harnesses."grok-bot"` is fixed as a first-class harness cell,
a sibling of `copilot-cli`, read by `adapters.resolve(cfg, "grok-bot")`:

```json
"grok-bot": {
  "adapter": "grok_bot",
  "bin": "/home/ubuntu/.npm-global/bin/grok-bot",
  "models": { "kid": "grok-4-fast", "parent": "grok-4" },
  "allowed_extra": ["grok-4", "grok-4-fast"]
}
```

`resolve` returns `("grok-bot", row)` with `adapter == "grok_bot"`, either
explicitly or through the dash-to-underscore default.

## Minimum behaviour

- the row is present in the COMMITTED `.agi/config.json`;
- every existing harness (`pi`, `pi-local`, `claude-code`, `copilot-cli`)
  still resolves unchanged.

## Out of scope

- `extensions/agi/bin/adapters/grok_bot_adapter.py` (owned by goal:g17.14.1);
- any `dispatch.py` edit.

## Landing mechanism and falsifier

`cli.py`'s `_round_scope_ok` returns False for `.agi/config.json`, so NO
kid/parent round commit can carry the row; it lands only via a
director-owned commit (the existing helper commit `ca3b2da28` on branch
`season2/loops/goal-g17.14.2-helper-cfg-land`).

Falsifier: a merge-up that drops the row re-breaks `resolve(cfg, "grok-bot")`
with `AdapterError` naming the declared harnesses.
