---
id: experiment:a00-8e139c40-e048c6
mint_id: e048c6912d2e47c4b625940f9f67fd0b
type: experiment
parents:
  - goal:g7.25.2
next_edges: []
confidence: 0.85
edited_by: belam
evidence_runs:
  - experiment:a00-8e139c40-e048c6
line_ceiling: 40
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 12
profile: balanced
role: kid
scaffold_hash: 158606546566e673
season: 2
thought_session: parent-residue-g14-g17-remap
title: grok-bot row added to harnesses; adapters.resolve accepts it and no other row changes
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-8e139c40-e048c6

## Experiment

Add exactly one entry `"grok-bot"` to the `harnesses` object in
`.agi/config.json` — config row ONLY, per `goal:g17.14.2`. Zero edits to
`extensions/agi/bin/dispatch.py`; the `grok_bot_adapter.py` module is owned
in parallel by `goal:g17.14.1` and was NOT created here; no test file added
(`goal:g17.14.3`). The only production path touched is `.agi/config.json`.

The row added, immediately after `copilot-cli` (the closest peer: a harness
with its own auth channel and no OpenRouter key):

```json
"grok-bot": {
  "adapter": "grok_bot",
  "bin": "/home/ubuntu/.npm-global/bin/grok",
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

## Acceptance — commands and output

Scratch script
`.agi/sessions/iter-DT.02/a00-8e139c40/accept.py` (NOT committed), run from
the worktree:

```
python3 .agi/sessions/iter-DT.02/a00-8e139c40/accept.py
1. grok-bot grok_bot
2. grok-bot grok_bot
3. pi OK
3. copilot-cli OK
bin: /home/ubuntu/.npm-global/bin/grok
provider: None
models: {'kid': 'grok-4-fast', 'parent': 'grok-4'}
exit=0
```

1. `adapters.resolve(cfg, "grok-bot")` -> `("grok-bot", row)` with
   `row["adapter"] == "grok_bot"` — PASS.
2. On a deep copy with the row's `"adapter"` key deleted,
   `adapters.resolve(cfg2, "grok-bot")[1]["adapter"] == "grok_bot"` — the
   dash-to-underscore default in `adapters/__init__.py::resolve`
   (`harness.setdefault("adapter", chosen.replace("-", "_"))`) — PASS.
3. `adapters.resolve(cfg, "pi")` and `adapters.resolve(cfg, "copilot-cli")`
   still succeed — no other row broken — PASS.

Config validity and the hard constraint:

```
python3 -c "import json;json.load(open('.agi/config.json'));print('valid json')"
valid json
grep -Ein 'grok' extensions/agi/bin/dispatch.py
(no output; grep exit=1 => zero matches, constraint held)
```

No repo test files were changed, so no repo pytest run was owed for this
config-only row; the acceptance above is the test and it is run live against
the live node (never a copied list).

## MEASURE basis for every value

- **`adapter: "grok_bot"`** — required by the brief and the seam; matches the
  neighbour style (`copilot_cli`, `claude_code`). Verified resolvable (1+2).
- **`bin`** — MEASURED ABSENT, PATTERN USED. Probes run on this box:
  `ls /home/ubuntu/.npm-global/bin/ | grep -i grok` -> no output,
  `ls /home/belam/.npm-global/bin/ | grep -i grok` -> no output,
  `which grok` -> exit 1, `find /home/belam /usr/local /opt -maxdepth 4
  -iname '*grok*'` -> no output, `env | grep -iE 'xai|grok'` -> empty.
  No grok binary and no grok CLI package exist on this box. The value
  `/home/ubuntu/.npm-global/bin/grok` is **the peer path pattern**, not a
  measured path: every peer row uses `/home/ubuntu/.npm-global/bin/<name>`
  (`pi`, `pi-local`, `copilot`), and note that directory does not exist on
  this box either — those rows are written for the deploy box, so the pattern
  is the honest analogue, explicitly UNVERIFIED here.
- **`provider`** — OMITTED ON PURPOSE, exactly like `copilot-cli`.
  `adapters.assert_model_in_provider_namespace` returns early unless
  `provider == "openrouter"`; with no `provider` key there is no namespace to
  cross, so a dash-free Grok model name (`grok-4`) cannot trip the fail-closed
  OpenRouter-slug check. `goal:g17.14.1`'s adapter returns
  `needs_credential(harness) == False` (grok-bot auths through its own
  channel), so an OpenRouter provider would also be wrong in kind. Namespacing
  it `openrouter` is the one thing the brief forbids.
- **`models.kid` / `models.parent`** — both keys present, as required, so
  `model_args` can raise by name on a missing tier (`goal:g17.14.3`'s test).
  Values are DOCUMENTED Grok API model ids, **UNVERIFIED here** (no binary,
  no key, no live endpoint): `grok-4-fast` for the kid tier and `grok-4` for
  the parent tier. `allowed_extra` carries the same two names so the derived
  allowlist (`adapters.derived_allowed_models`) covers them without a ladder
  row, which this config does not have (`roles` key absent).

## Scope proof

Production lines: 1 file changed, `.agi/config.json`, 12 lines added (`git diff --numstat`)
(`git diff --numstat`) — well under the 40-line ceiling. No git state was
mutated by this agent (one read-only numstat only).

## Agent Notes
grok-bot row added: adapter grok_bot, bin=/home/ubuntu/.npm-global/bin/grok (peer pattern, unverified), no provider, models kid=grok-4-fast/parent=grok-4 (documented, unverified). resolve() accepts it, dash-default works, pi & copilot-cli intact, dispatch.py untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version of this node. The deliberate choices: (a) no `provider` key, because `assert_model_in_provider_namespace` only fires on `openrouter` and a Grok name without a slash would fail closed there; (b) the bin path is the peer PATTERN and is stated as unverified rather than presented as measured, because the box has no grok binary at all — a guessed path asserted as measured is exactly the defect the brief names; (c) models are documented ids flagged unverified for the same reason. Nothing in dispatch.py was touched; the adapter module is another subgoal's file and is intentionally absent, so `adapters.load("grok_bot")` would still raise today — that is expected and belongs to goal:g17.14.1, not to this row.
<!-- THOUGHT:END -->
