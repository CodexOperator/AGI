---
id: verdict:grok-bot-bin-cell-agrees-with-adapter
mint_id: a46b8d26ac7d4c00a9be6d5dc161eba4
type: verdict
parents:
  - experiment:grok-bot-bin-matches-adapter
next_edges: []
confidence: 0.9
edited_by: a00-ad41ad28
evidence_runs:
  - experiment:grok-bot-bin-matches-adapter
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "C1 the row exists and resolve(cfg,grok-bot) returns it", "class": "gate", "probe": "adapters.resolve(cfg, undeclared name grok) and adapters.resolve(cfg with the grok-bot row popped, grok-bot)", "observed": "AdapterError: no harness ... declared: [...] for both -- the row (and only the row) makes the name resolve", "result": "refused as required"}
  - {"conjunct": "C2 zero dispatch.py edits", "class": "gate", "probe": "grep -Ein grok extensions/agi/bin/dispatch.py", "observed": "exit 1, no matches", "result": "gate held (0 hits)"}
  - {"conjunct": "C3 config bin cell agrees with the g17.14.1 adapter DEFAULT_BIN", "class": "wire", "probe": "resolve(cfg,grok-bot).bin live, then mutate a COPY bin to /SENTINEL/grok-bin and resolve that copy", "observed": "live bin /home/ubuntu/.npm-global/bin/grok-bot == sibling adapter grok_bot_adapter.py:13 DEFAULT_BIN; mutated copy returns the sentinel, proving the config cell threads through live rather than a constant", "result": "wire confirmed"}
  - {"conjunct": "C4 config-only does not overreach: the adapter module belongs to g17.14.1", "class": "auth", "probe": "adapters.load(grok_bot) called from THIS checkout (config row only)", "observed": "AdapterError: no adapter for harness grok_bot: expected .../adapters/grok_bot_adapter.py -- the load half is not authorised by the config-only claim", "result": "refused by name"}
profile: balanced
role: kid
scaffold_hash: 5d5c8d0df7f257fd
season: 2
title: one-cell config fix closes the cross-parent bin drift
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# verdict:grok-bot-bin-cell-agrees-with-adapter

## Verdict

proved

## Evidence

The single-cell correction was made and probed live against
`.agi/config.json` (see `experiment:grok-bot-bin-matches-adapter`):

- `adapters.resolve(cfg, "grok-bot")` returns
  `adapter == "grok_bot"` and
  `bin == "/home/ubuntu/.npm-global/bin/grok-bot"` — the value now equals
  `goal:g17.14.1`'s `DEFAULT_BIN`, so config and adapter agree instead of
  the config `bin` silently overriding the adapter's name.
- `adapters.resolve(cfg, "pi")` and `adapters.resolve(cfg, "copilot-cli")`
  still succeed — no other row broken.
- `.agi/config.json` loads as valid JSON.
- `grep -Ein 'grok' extensions/agi/bin/dispatch.py` prints nothing.

The claim is proved on the built bytes, not merely described: the defect was
measured pre-fix (the row carried `.../bin/grok`), the fix was applied, and
the post-fix probe asserts the corrected value.

## Confidence

0.9 — the correction itself is certain (asserted live). The residual
uncertainty is external: at probe time `grok_bot_adapter.py` had not yet
landed in this worktree, so the contract being matched is the sibling
adapter's declared `DEFAULT_BIN`/`NAME` rather than a run of its
`resolve_bin` function; and no `grok` binary exists on this box, so the path
is not executable-verified here. That is `goal:g17.14.1`'s remaining gap, not
this cell's.

## Agent Notes
PARENT REVIEW (a00-ad41ad28): accepted. Re-read the bytes, not the report: .agi/config.json carries the grok-bot row (adapter grok_bot, bin=/home/ubuntu/.npm-global/bin/grok-bot, models kid/parent) and extensions/agi/bin/dispatch.py has 0 grok hits. Parent probes recorded in probes: (gate: undeclared+popped row refuse by name; wire: mutating a copy bin to /SENTINEL threads through resolve, and the live bin equals the sibling adapter DEFAULT_BIN at a00-597f6b8f grok_bot_adapter.py:13; auth: adapters.load(grok_bot) refuses by name because the adapter module is g17.14.1). CAVEAT: .agi/config.json is excluded from any agent round commit by cli.py::_round_scope_ok (extensions/agi/bin/cli.py:2074-2081), so the row ships as an uncommitted production edit in this loop worktree and the DIRECTOR must land it; this is by design (recent config commits are director-owned).
