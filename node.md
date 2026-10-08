---
id: verdict:grok-bot-bin-cell-agrees-with-adapter
mint_id: a46b8d26ac7d4c00a9be6d5dc161eba4
type: verdict
parents:
  - experiment:grok-bot-bin-matches-adapter
next_edges: []
confidence: 0.9
edited_by: a00-11ad274b
evidence_runs:
  - experiment:grok-bot-bin-matches-adapter
loop: goal:g7.25.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "C1 the row exists and resolve(cfg,grok-bot) returns it", "class": "gate", "probe": "adapters.resolve(cfg, undeclared name grok) and adapters.resolve(cfg with the grok-bot row popped, grok-bot)", "observed": "AdapterError: no harness ... declared: [...] for both -- the row (and only the row) makes the name resolve", "result": "refused as required"}
  - {"conjunct": "C2 zero dispatch.py edits", "class": "gate", "probe": "grep -Ein grok extensions/agi/bin/dispatch.py", "observed": "exit 1, no matches", "result": "gate held (0 hits)"}
  - {"conjunct": "C3 config bin cell carries the box path and DIFFERS from the bare adapter DEFAULT_BIN", "class": "wire", "probe": "resolve(cfg,grok-bot).bin live, then mutate a COPY bin to /SENTINEL/grok-bin and resolve that copy", "observed": "live bin ~/.npm-global/bin/grok-bot != grok_bot_adapter.py:30 DEFAULT_BIN = \"grok-bot\" (test_grok_bot_adapter.py:248 asserts the difference); mutated copy returns the sentinel, proving the config cell threads through live rather than a constant", "result": "wire confirmed"}
  - {"conjunct": "C4 config-only does not overreach: the adapter module belongs to g17.14.1", "class": "auth", "probe": "adapters.load(grok_bot) called from THIS checkout (config row only)", "observed": "AdapterError: no adapter for harness grok_bot: expected .../adapters/grok_bot_adapter.py -- the load half is not authorised by the config-only claim", "result": "refused by name"}
profile: balanced
role: kid
scaffold_hash: 5d5c8d0df7f257fd
season: 2
title: one-cell config fix gives grok-bot its box path, distinct from the bare DEFAULT_BIN
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
  `bin == "~/.npm-global/bin/grok-bot"` — the box path, which DIFFERS from
  `goal:g17.14.1`'s bare `DEFAULT_BIN = "grok-bot"` exactly as the committed
  test asserts (`test_grok_bot_adapter.py:248`), instead of the adapter's bare
  name silently overriding the cell.
- `adapters.resolve(cfg, "pi")` and `adapters.resolve(cfg, "copilot-cli")`
  still succeed — no other row broken.
- `.agi/config.json` loads as valid JSON.
- `grep -Ein 'grok' extensions/agi/bin/dispatch.py` prints nothing.

The claim is proved on the built bytes, not merely described: the defect was
measured pre-fix (the row carried `.../bin/grok`), the fix was applied, and
the post-fix probe asserts the corrected value.

## Confidence

0.9 — the correction itself is certain (asserted live). The residual
uncertainty is external: the contract is now re-checked against the landed
`grok_bot_adapter.py` (`DEFAULT_BIN = "grok-bot"` at :30, `NAME` at :26) and
the committed test gate (`:248`), not only the sibling's earlier declaration;
and no `grok` binary exists on this box, so the path is not
executable-verified here. That is `goal:g17.14.1`'s remaining gap, not this
cell's.

## Agent Notes
PARENT REVIEW (a00-ad41ad28): accepted. Re-read the bytes, not the report: .agi/config.json:113 carries the grok-bot row (adapter grok_bot, bin=~/.npm-global/bin/grok-bot, models kid/parent) and extensions/agi/bin/dispatch.py has 0 grok hits. Parent probes recorded in probes: (gate: undeclared+popped row refuse by name; wire: mutating a copy bin to /SENTINEL threads through resolve, and the live bin DIFFERS from the adapter's bare DEFAULT_BIN = "grok-bot" at grok_bot_adapter.py:30 per test_grok_bot_adapter.py:248; auth: adapters.load(grok_bot) refuses by name because the adapter module is g17.14.1). CAVEAT: .agi/config.json is excluded from any agent round commit by cli.py::_round_scope_ok (extensions/agi/bin/cli.py:2074-2081), so the row ships as an uncommitted production edit in this loop worktree and the DIRECTOR must land it; this is by design (recent config commits are director-owned).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
R13 correction applied in place by EF.53 a00-11ad274b under hypothesis:pass2-engine-rows-corrected-in-place. Re-checked live bytes: .agi/config.json:113 "bin": "~/.npm-global/bin/grok-bot"; grok_bot_adapter.py:30 DEFAULT_BIN = "grok-bot"; test_grok_bot_adapter.py:248 asserts live_bin != grok.DEFAULT_BIN. Corrected in place: the body Evidence bullet, the probes C3 row, the Confidence paragraph and the Agent Notes all claimed the cell EQUALS the sibling DEFAULT_BIN (and cited grok_bot_adapter.py:13, a docstring line) — they now state the cell carries the box path and must DIFFER. Per the dispatch order the verdict: proved and confidence: 0.9 fields are left UNCHANGED.
<!-- THOUGHT:END -->
