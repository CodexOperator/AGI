---
id: hypothesis:a00-da41e117-c79b5e
mint_id: dbce00991a16465d8d794e7a03216a99
type: hypothesis
parents:
  - goal:g7.25.2
next_edges: []
edited_by: a00-11ad274b
loop: goal:g7.25.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 32439ae30a363b3c
season: 2
testable_claim: The `harnesses."grok-bot".bin` config cell carries the box path `~/.npm-global/bin/grok-bot` (no per-box /home/<user> literal), while `extensions/agi/bin/adapters/grok_bot_adapter.py:30` `DEFAULT_BIN` is the BARE PATH fallback `"grok-bot"`; the cell must DIFFER from `DEFAULT_BIN`, as the committed test asserts (`extensions/agi/tests/test_grok_bot_adapter.py:248` `assert live_bin != grok.DEFAULT_BIN`).
thought_session: parent-residue-g14-g17-remap
title: grok-bot config bin carries the box path and must DIFFER from the adapter bare DEFAULT_BIN
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:a00-da41e117-c79b5e

## Hypothesis

The `harnesses."grok-bot"` row must agree with the sibling adapter as it
actually landed (`extensions/agi/bin/adapters/grok_bot_adapter.py`):
`NAME = "grok-bot"`, `DEFAULT_BIN = "grok-bot"` (a **bare PATH fallback**,
`grok_bot_adapter.py:30`) and `resolve_bin` precedence `$GROK_BOT_BIN >
harness['bin'] > DEFAULT_BIN`. The config `bin` cell carries the box path
(`~/.npm-global/bin/grok-bot`, no `/home/<user>` literal) and WINS over the
bare fallback, so the two MUST DIFFER — the committed test asserts exactly
`assert live_bin != grok.DEFAULT_BIN` (`test_grok_bot_adapter.py:248`). The
earlier claim that the cell must EQUAL `/home/ubuntu/.../grok-bot` was the
opposite of the bytes: `DEFAULT_BIN` is bare, not that path.

The testable claim: the ONE config cell carries the box path
`~/.npm-global/bin/grok-bot` (no per-box `/home` literal), it DIFFERS from the
bare `DEFAULT_BIN`, and
1. `adapters.resolve(cfg, "grok-bot")` still returns
a row with `adapter == "grok_bot"` and `bin ==
"~/.npm-global/bin/grok-bot"`;
2. `adapters.resolve(cfg, "pi")` and `adapters.resolve(cfg,
"copilot-cli")` still succeed (no other row broken);
3. `.agi/config.json` is still valid JSON; and
4. `grep -Ein 'grok' extensions/agi/bin/dispatch.py` prints nothing.

Disproof: the probe assertions fail, the JSON becomes invalid, another row
stops resolving, or a `grok` token appears in `dispatch.py`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
R13 correction applied in place by EF.53 a00-11ad274b under hypothesis:pass2-engine-rows-corrected-in-place. Re-checked live bytes: grok_bot_adapter.py:30 is DEFAULT_BIN = "grok-bot" (bare PATH fallback); .agi/config.json:113 is "bin": "~/.npm-global/bin/grok-bot"; the committed test at test_grok_bot_adapter.py:248 asserts live_bin != grok.DEFAULT_BIN. The node title and body said the opposite (config bin must EQUAL DEFAULT_BIN = /home/ubuntu/.npm-global/bin/grok-bot); title, claim and body are re-versioned to the real precedence and the test gate. The config correction itself already landed (G-row); this round rewrites node text only and touches no verdict/lean/confidence field.
<!-- THOUGHT:END -->
