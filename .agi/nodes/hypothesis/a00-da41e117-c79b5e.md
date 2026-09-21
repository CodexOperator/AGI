---
id: hypothesis:a00-da41e117-c79b5e
mint_id: dbce00991a16465d8d794e7a03216a99
type: hypothesis
parents:
  - goal:g17.14.2
next_edges: []
edited_by: a00-da41e117
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 32439ae30a363b3c
season: 2
title: grok-bot config bin must equal the sibling adapter DEFAULT_BIN grok-bot
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:a00-da41e117-c79b5e

## Hypothesis

The `harnesses."grok-bot"` row must agree with the sibling adapter
`goal:g17.14.1` will land (`extensions/agi/bin/adapters/grok_bot_adapter.py`,
`NAME = "grok-bot"`, `resolve_bin` precedence `$GROK_BOT_BIN >
harness['bin'] > DEFAULT_BIN = /home/ubuntu/.npm-global/bin/grok-bot`).
Because the config `bin` WINS over the adapter's default, the row's current
value `/home/ubuntu/.npm-global/bin/grok` silently overrides the adapter's
chosen binary name and would break the spawn once g17.14.1 lands.

The testable claim: changing that ONE cell to
`/home/ubuntu/.npm-global/bin/grok-bot` makes the row agree with the
sibling contract, while
1. `adapters.resolve(cfg, "grok-bot")` still returns
a row with `adapter == "grok_bot"` and now `bin ==
"/home/ubuntu/.npm-global/bin/grok-bot"`;
2. `adapters.resolve(cfg, "pi")` and `adapters.resolve(cfg,
"copilot-cli")` still succeed (no other row broken);
3. `.agi/config.json` is still valid JSON; and
4. `grep -Ein 'grok' extensions/agi/bin/dispatch.py` prints nothing.

Disproof: the probe assertions fail, the JSON becomes invalid, another row
stops resolving, or a `grok` token appears in `dispatch.py`.
