---
forbidden_keys:
  - ANTHROPIC_API_KEY
  - ANTHROPIC_AUTH_TOKEN
  - ANTHROPIC_BASE_URL
  - CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST
id: "config:secrets"
locations:
  env_file:
    role: "provider credentials for this project — the VALUES"
    derivation: relative-to-source-root
    path: "<source_root>/.env"
    gitignored: true
    mode: "600"
    declared_in:
      - "extensions/agi/bin/envfile.py :: resolve"
      - "extensions/agi/driver.sh :: AGI_ENV_FILE"
      - "extensions/agi/bin/env-get.sh :: ENV_FILE"
  env_template:
    role: "the committed SHAPE of env_file — which keys, and what each is for"
    derivation: relative-to-source-root
    path: "<source_root>/.env.example"
    gitignored: false
    declared_in:
      - "extensions/agi/bin/envfile.py :: resolve"
mint_id: eba3708aa2ce4642a394a3646f6e2a26
optional_keys:
  - MINIMAX_API_KEY
  - OPENAI_API_KEY
  - OPENROUTER_PROVISIONING_KEY
parents:
  - goal:g1.8
  - goal:g10.2
required_keys:
  - OPENROUTER_API_KEY
status: active
tags:
  - geometry
  - config
  - secrets
  - structural
title: "Where credentials live, and which keys this project requires"
type: config
---

**One file holds this project's secrets, and this node says which file it is.**
Before it existed the answer was a literal `.env` written into a shell script,
a second `.env` written into another shell script, and prose in a third place —
the shape that drifts. `bin/envfile.py` reads this node; `driver.sh` and
`bin/env-get.sh` read `envfile.py`. The path is now a fact the graph states
once (**goal:g10.2**), not a constant three files agree on by luck.

## The two halves, and why only one of them has history

| | committed | build node | grid ref |
|---|---|---|---|
| `env_template` — `.env.example` | yes | yes | yes |
| `env_file` — `.env` | **never** | no | no |

Changing a **value** is invisible to git and to the grid by construction. That
is deliberate: a version history of a secret is a leak with a changelog.
Changing the **shape** — adding a key, retiring one, restating what a key is
for — edits `.env.example`, which is an ordinary tracked file and gets an
ordinary version. **Shape is versioned; value is not** (**goal:g1.8**).

## Per project, not per box

Both paths resolve against `source_root`, so a project with the engine cloned
in gets its own pair rather than sharing the engine's — `fantasia/.env` for
fantasia, `fantasia/agi/.env` for the engine's own loop, resolved by the same
nearest-enclosing rule as everything else and with no flag (**goal:g8.2**).
The cost is real and worth stating: a key needed by two projects is typed
twice. That is the price of not having a machine-global secret store that no
project's graph describes.

## `forbidden_keys` is a floor, not a preference

`dispatch.py` scrubs the `ANTHROPIC_*` and `CLAUDE_CODE_*` variables from pi
child environments so that spawned subagents cannot silently bill the
interactive Claude Code subscription and compete with the session for its
quota. An env file is read *below* that scrub — `driver.sh` sources it into the
environment `dispatch.py` then filters — so a key set here would be re-added at
exactly the layer where nothing checks. `envfile.py` enforces the three
`ANTHROPIC_*` names regardless of what this node says, so editing the list
above cannot lower the floor.

## `OPENROUTER_PROVISIONING_KEY` is a different kind of key, and is optional

**It mints and revokes runtime keys; it is not one.** `OPENROUTER_API_KEY`
buys inference. A provisioning key calls OpenRouter's key-management API, so it
can create keys, revoke them, set per-key credit limits and read spend. Losing
it is strictly worse than losing a runtime key, which is why three things
follow rather than being a matter of taste:

- **It is `optional`, permanently.** The loop must run without it — a project
  with no provisioning key uses the one runtime key it has and nothing
  degrades except per-spawn isolation. Making it required would turn a
  hardening feature into a hard dependency for every clone.
- **It is never handed to a child process.** `OPENROUTER_API_KEY` is inherited
  by every pi agent by design; this one must not be. A kid that can mint keys
  can mint keys with no limit, and a kid that can revoke them can end the run.
  The scrub list that protects the Claude subscription is the shape to copy.
- **The keys it mints are the things that get spent.** Short-lived, credit-
  capped, one per spawn or per batch, revoked at the end of the loop. That is
  `goal:g1.11` and it is what this key exists for.

## What reads this

- `bin/envfile.py` — five fields: both `locations.*.path` entries,
  `required_keys`, `optional_keys`, `forbidden_keys`.
- `driver.sh` — resolves `env_file`, sources it before any dispatch, and runs
  the check so a missing key is reported by `--smoke` rather than discovered
  later inside pi.
- `bin/env-get.sh` — resolves the same file for `~/.pi/agent/auth.json`'s
  `"!command"` key form, so pi holds a pointer and not a second copy.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. The immediate need was an OpenRouter key on this box, and the
shortest path was to hardcode `.env` in `driver.sh` and move on — which is what
the first pass of `goal:g1.8` actually did, and it worked. It was rejected on
the second pass for the reason G10.2 exists: a path that only code knows is a
path the graph cannot answer questions about, and this repo already carries the
scar of the same class of fact — the ancestor walk — being restated eleven
times until nobody could change the rule once.

The `[config]` schema had been sitting with zero nodes minted against it and an
explicit note that minting one waited on "a code path that reads more than one
field". That note is what settled the shape: rather than invent a `secrets`
type, this is the first real `config` node, and `envfile.py` is that code path.
The schema's `validation.required` had to drop `config_marker_names` to allow
it — written speculatively against no nodes, it would have forced a declaration
about credentials to restate an unrelated list about project discovery.

Per-project rather than per-box was the owner's call and it has a real cost: a
key needed by two projects gets typed twice. Recorded here rather than argued,
because the alternative — one machine-global secret file — is exactly the kind
of unowned state no project's graph describes, and the whole point of this node
is that the location is owned.
<!-- THOUGHT:END -->
