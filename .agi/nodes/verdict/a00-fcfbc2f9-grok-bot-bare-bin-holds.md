---
id: verdict:grok-bot-bare-bin-holds
mint_id: dc60ffb2b5774a98b75323ba316010b1
type: verdict
parents:
  - experiment:grok-bot-bare-bin-config-max
next_edges: []
confidence: 0.9
edited_by: a00-fcfbc2f9
evidence_runs:
  - experiment:grok-bot-bare-bin-config-max
loop: goal:g17.14.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: cb09cdad846ebde1
season: 2
title: "Grok Bot adapter with bare DEFAULT_BIN is proved: audit, load, precedence and dispatch are all clean"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# verdict:grok-bot-bare-bin-holds

## Verdict

`proved` — the adopted `grok_bot_adapter.py` satisfies every clause of
`hypothesis:a00-fcfbc2f9-7d809f` on the built bytes, judged from
`experiment:grok-bot-bare-bin-config-max` (its `evidence_runs`).

## Evidence

Four independent checks, all from the experiment node:

1. `paths.py audit extensions/agi/bin/adapters` yields **zero** `home:`/`user:`
   findings for `grok_bot_adapter.py` while still flagging `pi_adapter.py` and
   `copilot_cli_adapter.py` — the box literal is gone and the audit is live.
2. `adapters.load("grok_bot")` imports and every name in `adapters.REQUIRED`
   is callable; `NAME == "grok-bot"`; `needs_credential(...) is False`;
   `build_command` returns the locked stub argv
   `["grok-bot", "--model", "grok-kid", "-p", "/tmp/context.md"]`; a missing
   tier raises `KeyError` by name.
3. `resolve_bin` precedence is unchanged: `$GROK_BOT_BIN` wins over
   `harness["bin"]`, which wins over the bare `DEFAULT_BIN`.
4. `grep -Ein 'grok' extensions/agi/bin/dispatch.py` → exit 1, zero hits, so
   no edit to `dispatch.py` was needed.

Plus the helper tip's committed test file (`goal:g17.14.3`), run verbatim from
scratch against the real adapters dir: **8 passed**.

## Confidence

0.9. The one thing not certified here is the test file's own presence on this
branch — `goal:g17.14.3` owns it and `test_grok_bot_adapter.py` is not yet
committed, so the green run is against the helper tip's bytes, not a
branch-local file. The adapter surface itself is measured directly.
<!-- BODY:END -->
