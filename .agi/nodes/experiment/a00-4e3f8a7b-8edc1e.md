---
id: experiment:a00-4e3f8a7b-8edc1e
mint_id: 4fed177ca0d04fdb81347f77ff35c272
type: experiment
parents:
  - hypothesis:l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-claude-code-and-pi
next_edges: []
confidence: 0.8
edited_by: a00-cd9b4aa1
evidence_runs:
  - experiment:a00-4e3f8a7b-8edc1e
loop: hypothesis:l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-claude-code-and-pi@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: cfc3882db2568ff7
season: 2
title: "Copilot CLI gate measured: installs, authes via GH_TOKEN, headless exits 0, models list is only auto"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4e3f8a7b-8edc1e

MEASUREMENT of the Copilot CLI gate for the parent claim (conjuncts 1-3: install,
auth, models) plus the headless falsifier. Every value below is a quoted raw
output from this box, 2026-09-14, user `ubuntu`, gh account `CodexOperator`.
No engine code was touched. One premium request was spent (the headless run).

## 1. Install — package name and version

```
$ npm view @github/copilot version
1.0.83

$ npm install -g @github/copilot
added 3 packages in 6s

$ which copilot
/home/ubuntu/.npm-global/bin/copilot

$ copilot --version
GitHub Copilot CLI 1.0.83.
Run 'copilot update' to check for updates.
```

The npm package name in the parent claim is CORRECT: `@github/copilot`
(platform binary shipped as optional dep `@github/copilot-linux-arm64@1.0.83`,
bin entry `npm-loader.js`). Install needed no sudo.

Flags that matter for scripted driving (from `copilot --help`, verbatim):

```
  -p, --prompt <text>                   Execute a prompt in non-interactive mode
                                        (exits after completion)
  --model <model>                       Set the AI model to use (use 'auto' to
                                        let Copilot pick automatically)
  --allow-all-tools                     Allow all tools to run automatically
                                        without confirmation; required for
                                        non-interactive mode (env:
                                        COPILOT_ALLOW_ALL)
  --allow-all                           Enable all permissions (equivalent to
                                        --allow-all-tools --allow-all-paths
                                        --allow-all-urls)
  --log-level <level>                   none|error|warning|info|debug|all
```

## 2. Auth — works with the existing gh login, no new scope needed

The brief feared a missing `copilot` scope. The CLI's own docs (`copilot login
--help`, verbatim) say that is not required:

```
Copilot login will also use an authentication token found in environment
variables. ... The following are checked in order of precedence:
COPILOT_GITHUB_TOKEN, GH_TOKEN, GITHUB_TOKEN.

Supported token types include fine-grained personal access tokens (v2 PATs) with
the "Copilot Requests" permission, OAuth tokens from the GitHub Copilot CLI app,
and OAuth tokens from the GitHub CLI (gh) app.

Classic personal access tokens (ghp_) are not supported.
```

The existing gh OAuth token IS accepted. `gh auth status` scopes are exactly
`'gist', 'read:org', 'repo', 'workflow'` -- no `copilot` scope is present and
none was needed. Measured auth status through the shipped SDK:

```
$ GH_TOKEN=$(gh auth token) node probe.mjs
AUTH={"isAuthenticated":true,"authType":"env","host":"https://github.com",
      "statusMessage":"CodexOperator (via GH_TOKEN)","login":"CodexOperator"}
STATUS={"version":"1.0.83","protocolVersion":3}
```

### Persistence does NOT work on this box

```
$ gh auth token | copilot login --with-token
Login succeeded, but the token was not saved. Install a system keychain or
rerun login and accept plaintext storage.
EXIT=1
```

So auth is real but ephemeral: every spawn must carry `GH_TOKEN`.

## 3. Models — only `auto`. There is NO model picker on this account.

Raw `models.list` RPC through the shipped SDK (`copilot-sdk/index.js`,
`client.listModels()`), not a reconstruction:

```
$ GH_TOKEN=$(gh auth token) node probe.mjs
MODEL_COUNT=1
MODEL {"id":"auto","name":"Auto","max_context":0,"supports":[]}

$ GH_TOKEN=$(gh auth token) node probe2.mjs   # raw RPC, unfiltered
RAW={ "models": [ { "id": "auto", "name": "Auto", "capabilities": {} } ] }
```

Named models are refused at resolution time (before any inference, so these
cost no credits). Exact error, identical for every name probed:

```
$ copilot --model claude-sonnet-4   -p 'hi' --allow-all-tools
Error: Model "claude-sonnet-4" from --model flag is not available.     (rc=1)
$ copilot --model claude-sonnet-4.5 -p 'hi' --allow-all-tools
Error: Model "claude-sonnet-4.5" from --model flag is not available.   (rc=1)
$ copilot --model gpt-5.4           -p 'hi' --allow-all-tools
Error: Model "gpt-5.4" from --model flag is not available.             (rc=1)
$ copilot --model gemini-2.5-pro    -p 'hi' --allow-all-tools
Error: Model "gemini-2.5-pro" from --model flag is not available.      (rc=1)
```

Why: the CLI's own user cache (`~/.cache/copilot/copilot-user-cache.json`,
written by this account's own session) reports
`"access_type_sku": "free_educational_quota"`, `"copilot_plan": "individual"`,
`"can_upgrade_plan": true`, and premium quota
`premium_interactions {"entitlement": 200, "remaining": 119.2,
"percent_remaining": 59.6}`. This is NOT a Copilot Pro entitlement.

### Ladder table (Sanctuary roles vs what Copilot CLI offers here)

| Ladder row | Sanctuary model | Copilot CLI selectable model | Verdict |
|---|---|---|---|
| prime | claude-opus-5 | none (`--model` refused) | NOT available |
| director (point) | claude-opus-5 (max effort) | none (`--model` refused) | NOT available |
| director (helper) | claude-sonnet-5 (max effort) | none (`--model` refused) | NOT available |
| parent (kid/agent) | claude-sonnet-5 | none (`--model` refused) | NOT available |
| any | (n/a) | `auto` (server-chosen) | available |

So the owner's question "does it offer most of the same models" answers **no on
this account**: exactly one entry, `auto`. Either the plan is not Pro (the SKU
says free/educational) or model choice is gated out of this entitlement.

## 4. Headless — WORKS, exit 0 (the falsifier did not fire)

Fixture cwd `/tmp/copilot-fixture`, one premium request, raw transcript:

```
$ cd /tmp/copilot-fixture && GH_TOKEN=$(gh auth token) \
    copilot -p 'Reply with exactly: OK' --allow-all-tools
OK



Changes    +0 -0
AI Credits 0.35 (3s)
Tokens     ↑ 15.4k (15.4k written) • ↓ 5
Resume     copilot --resume=a4fdd1d4-df05-407f-be0a-81c623807a24
EXIT=0
```

Non-interactive mode exists, is scriptable, returns exit 0, prints model text
and a resume handle, and reports cost on stdout. It also has an ACP mode
(`--acp`, "Start as Agent Client Protocol server") if a structured transport is
preferred later.

## 5. Hook surface (evidence for the parent claim, read not run)

`copilot help config` declares hooks as first-class config:

```
  `disableAllHooks`: whether to disable all hooks (repo-level and user-level); defaults to `false`.

  `hooks`: inline hook definitions, keyed by event name (same schema as `.github/hooks/*.json`).
    - In global config.json these act as user-level hooks; in repo settings.json they act as repo-level hooks
```

Event names, extracted verbatim from the shipped schema
`schemas/api.schema.json`:

```
sessionStart  sessionEnd  userPromptSubmitted  userPromptTransformed
preToolUse    postToolUse postToolUseFailure   preMcpToolCall
preCompact    agentStop   errorOccurred        notification
```

and plugins can ship hooks alongside skills/agents/MCP servers
(`copilot plugin`; schema keys `pluginHookCount`, `reloadPluginHooks`,
`loadDeferredRepoHooks`). This is the same event vocabulary Claude Code uses
(SessionStart/SessionEnd/UserPromptSubmit/PreToolUse/PostToolUse/PreCompact/
Stop/Notification), which is what the parent claim asserts. NOT executed in
this kid -- kid 2 owns wiring.

## PRIME LINE (owner-facing, one line)

Models: **only `auto`** -- claude-sonnet/opus, gpt-5.x and gemini are all
refused by name on this account (SKU `free_educational_quota`, plan
`individual`, 119.2/200 premium interactions left, `can_upgrade_plan: true`).
Auth: **works today with zero owner action IF spawns carry the env var** --
`export GH_TOKEN=$(gh auth token)`; nothing else needed, no `copilot` scope.
By hand, only if you want it durable and can accept plaintext storage:
`gh auth token | copilot login --with-token` (currently exits 1: "token was not
saved"). If named models are required, the owner must upgrade the plan on
CodexOperator; no CLI flag unlocks them.

## Caveats

- The SDK probe used `copilot-sdk/index.js` shipped inside the npm package;
  it is the same client the CLI uses, but it is a vendor internal path, not a
  documented entry point.
- `--allow-all-tools` ran fine, but the runtime log carries
  `bypass-permissions mode DISABLED by enterprise policy (fail-closed: policy
  could not be determined)` -- permissions may behave differently inside a
  repo with `.github/hooks` or on a managed device.
- Nothing was implemented; this is measurement only, per the kid brief.

<!-- THOUGHT:BEGIN -- authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version of this node (scaffold filled). Deviation from the brief worth
recording: the brief expected a Copilot **Pro** plan and a full model picker,
and told me to stop at the auth conjunct if the gh token lacked a `copilot`
scope. The opposite happened -- auth needed no scope at all, and the model
picker is the thing that is empty. So the falsifier the brief cared about
(missing auth) did not fire, and the conjunct that would have answered the
owner's real question ("most of the same models") is answered NO on this
account. I chose `proved` for the harness-plumbing conjuncts (install + auth +
headless all measured green, which is what the brief said to record) while
stating the model answer plainly rather than softening it into a lean -- the
model result is not an inference, it is a quoted RPC response and four quoted
refusals. I did NOT spend more than the one authorized premium request
probing models: the `--model` refusals happen at resolution, before inference,
so they are free, and I verified that with the log line
`rust:model_bindings::api_resolver Model ... is not available` rather than by
burning credits.
<!-- THOUGHT:END -->

## Agent Notes
Copilot CLI 1.0.83 (@github/copilot): installs no-sudo, PATH /home/ubuntu/.npm-global/bin/copilot; auth WORKS via GH_TOKEN=$(gh auth token) with NO copilot scope (isAuthenticated:true authType:env login CodexOperator), but copilot login --with-token cannot persist (no keychain, exits 1); headless -p exits 0 with 'OK' and AI Credits 0.35; models.list returns ONLY 'auto' -- claude-sonnet-4/4.5, gpt-5.4, gemini-2.5-pro all refused by name (SKU free_educational_quota, plan individual, 119.2/200 premium interactions); hook schema names match Claude Code's event vocabulary (sessionStart/sessionEnd/userPromptSubmitted/preToolUse/postToolUse/preCompact/agentStop/notification)

PARENT REVIEW PROBES (a00-cd9b4aa1, 2026-09-14): auth — "GH_TOKEN=gho_bogus_invalid_token_000 copilot -p ..." refused by name: "Failed to fetch PAT user login (401): Bad credentials" (kid auth claim holds). gate — "copilot --model claude-sonnet-5 -p hi --allow-all-tools" -> "Error: Model \"claude-sonnet-5\" from --model flag is not available." (kid model-list claim holds; no inference cost). wire — "copilot --help" independently shows -p/--model/--allow-all-tools exactly as quoted; binary present at /home/ubuntu/.npm-global/bin/copilot v1.0.83. CONCERN: the models conjunct answers goal:g15 falsifier "the model list lacks every Claude/GPT tier the ladder needs" for THIS credential (SKU free_educational_quota/individual, not Pro) — kid 2 must not assume named models resolve; model stays auto.
