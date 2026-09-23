---
id: experiment:grok-bot-bin-matches-adapter
mint_id: f12bfb13afbb4bc28c3059ca0842517b
type: experiment
parents:
  - hypothesis:a00-da41e117-c79b5e
next_edges: []
confidence: 0.9
edited_by: a00-da41e117
evidence_runs:
  - experiment:grok-bot-bin-matches-adapter
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 60f110276256e7b9
season: 2
title: grok-bot row bin cell corrected to adapter DEFAULT_BIN; resolve pi and copilot-cli intact
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:grok-bot-bin-matches-adapter

## Experiment

Corrected ONE cell in `.agi/config.json`: the `harnesses."grok-bot".bin`
value, from `/home/ubuntu/.npm-global/bin/grok` to
`/home/ubuntu/.npm-global/bin/grok-bot`. Nothing else was touched: no
`adapter`, `models`, `allowed_extra` or any other row; no `dispatch.py`
edit; no `grok_bot_adapter.py` created (owned by `goal:g17.14.1`); no test
file added (`goal:g17.14.3`). Only `.agi/config.json` and this agent's own
nodes are changed.

### MEASURE basis — the sibling adapter's own contract

The authoritative value is not invented here. `goal:g17.14.1`
(`extensions/agi/bin/adapters/grok_bot_adapter.py`, owned in parallel by
parent `a00-597f6b8f`) declares `NAME = "grok-bot"` and the `resolve_bin`
precedence:

    $GROK_BOT_BIN > harness['bin'] > DEFAULT_BIN = /home/ubuntu/.npm-global/bin/grok-bot

Sibling parent `a00-597f6b8f` replied verbatim: *"resolve_bin precedence:
$GROK_BOT_BIN > harness['bin'] > default
/home/ubuntu/.npm-global/bin/grok-bot — so your config row needs a 'bin' cell
if it is elsewhere"*. The config `bin` cell WINS over that default, so the
pre-existing `grok` value forced a binary name the adapter author did not
choose — a cross-parent drift that would break the spawn once g17.14.1 lands.
The corrected value is the adapter's own `DEFAULT_BIN`, so config and adapter
agree. (At probe time `grok_bot_adapter.py` was not yet present in this
worktree — g17.14.1 runs in parallel — so the contract is cited from the
sibling's own declaration, which is the MEASURE, not a guess.)

### Acceptance — exact commands and output

Scratch probe in this agent's session dir (NOT committed), run from the
worktree root:

```
python3 - <<'EOF'
import json, sys
sys.path.insert(0,'extensions/agi/bin')
from adapters import resolve
cfg=json.load(open('.agi/config.json'))
n,row=resolve(cfg,'grok-bot')
print("resolve grok-bot ->", n, json.dumps(row,sort_keys=True))
assert row["adapter"]=="grok_bot", row
assert row["bin"]=="/home/ubuntu/.npm-global/bin/grok-bot", row
for other in ("pi","copilot-cli"):
    on,orow=resolve(cfg,other)
    print("resolve",other,"->",on,orow["adapter"])
    assert on==other
print("ACCEPTANCE OK")
EOF
```

Output:

```
resolve grok-bot -> grok-bot {"adapter": "grok_bot", "allowed_extra": ["grok-4", "grok-4-fast"], "bin": "/home/ubuntu/.npm-global/bin/grok-bot", "models": {"kid": "grok-4-fast", "parent": "grok-4"}}
resolve pi -> pi pi
resolve copilot-cli -> copilot-cli copilot_cli
ACCEPTANCE OK
```

1. `adapters.resolve(cfg, "grok-bot")` -> row with `adapter == "grok_bot"`
   and `bin == "/home/ubuntu/.npm-global/bin/grok-bot"` — PASS (asserted).
2. `adapters.resolve(cfg, "pi")` and `adapters.resolve(cfg,
   "copilot-cli")` still succeed — PASS.
3. Config validity and the hard constraint:

```
python3 -c "import json;json.load(open('.agi/config.json'));print('json OK')"
json OK

grep -Ein 'grok' extensions/agi/bin/dispatch.py
(no output; grep exit=1 => zero matches, constraint held)
```

4. The corrected row verbatim from the file (`sed -n '113,124p'
   .agi/config.json`):

```json
    "grok-bot": {
      "adapter": "grok_bot",
      "bin": "/home/ubuntu/.npm-global/bin/grok-bot",
      "models": {
        "kid": "grok-4-fast",
        "parent": "grok-4"
      },
      "allowed_extra": [
        "grok-4",
        "grok-4-fast"
      ]
    }
```

Live config read: the probe loads the live `.agi/config.json` from disk at
run time, never a copied list.

### Scope proof

`git diff --numstat -- .agi/config.json extensions/agi/bin/dispatch.py`
(read-only measurement, the only git run) shows `12 0 .agi/config.json` and
nothing for `dispatch.py`. The 12 added lines are kid 1's whole uncommitted
`grok-bot` row vs HEAD, inherited by this correction pass; this pass itself
is a one-cell edit. Well under the 40-line ceiling. `.agi/config.json` is
excluded from an agent round's own commit (`cli.py::_round_scope_ok`,
`extensions/agi/bin/cli.py:2074-2081`), so it is left as an uncommitted
production edit for the director to land.

## Evidence

See Acceptance above. No repo test files were changed, so no repo pytest run
was owed; the acceptance probe is the test and it ran live against the live
node.

## Agent Notes
Corrected harnesses.grok-bot.bin from .../bin/grok to .../bin/grok-bot so config agrees with goal:g17.14.1's adapter DEFAULT_BIN; resolve(grok-bot).bin asserted, pi & copilot-cli intact, json valid, dispatch.py grok-free.
