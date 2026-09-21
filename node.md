---
id: experiment:a00-440ab5ac-e53139
mint_id: e4d159400a474008a6a0345e313e17d3
type: experiment
parents:
  - hypothesis:l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-claude-code-and-pi
next_edges: []
confidence: 0.8
edited_by: a00-cd9b4aa1
evidence_runs:
  - experiment:a00-440ab5ac-e53139
loop: hypothesis:l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-claude-code-and-pi@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d053d126327371de
season: 2
title: A00 440ab5ac e53139
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-440ab5ac-e53139

**BUILD, not measurement.** The parent hypothesis is a build order: `copilot`
is a third harness that fits the existing adapter seam with no edit to
`dispatch.py`. This node implements it (conjunct 4), proves it on the BUILT
command, and writes the fixture-only tests (conjunct 7). Conjunct 5 (hook
parity) is implemented as the prompt-injection fallback the claim explicitly
allows; the hook-registration route is documented but deliberately NOT
registered, because proving a `sessionStart` hook fires needs a live model
turn and the CLI ships no hook-run subcommand (state plainly, per the brief).

## What changed

| File | Change |
|---|---|
| `extensions/agi/bin/adapters/copilot_cli_adapter.py` | **NEW** — the whole harness: `build_command`, `child_env`, `is_alive`, `restart`, `needs_credential` (the REQUIRED tuple) |
| `.agi/config.json` | adds `harnesses.copilot-cli` |
| `extensions/agi/tests/test_copilot_cli_adapter.py` | **NEW** — 21 fixture-only tests |
| `extensions/agi/bin/dispatch.py` | **NOT edited** — the seam held |

## The CLI shape the adapter had to meet (read from copilot v1.0.83, 2026-09-14)

`copilot --help`, verbatim:

```
    -p, --prompt <text>                   Execute a prompt in non-interactive mode
                                          (exits after completion)
    --allow-all-tools                     Allow all tools to run automatically
                                          without confirmation; required for
                                          non-interactive mode (env:
```

**There is no system-prompt flag.** Grepping the full `--help` for
`prompt|system|instruction` finds `-p`, `--no-custom-instructions`, `--agent`,
`--attachment` and `--additional-mcp-config` — no `--append-system-prompt`,
no `--append-system-prompt-file`. So the brief is assembled through
`brief.assemble` exactly as pi and Claude Code do, written to the session as
`prompt.md`, and handed to the CLI as the `-p` TEXT — a leading instruction
block in the one turn the CLI runs. That is the fallback the parent claim
allowed, and it is stated here because a reader grepping for a system-prompt
flag will not find one.

Auth, measured by kid 1 (`experiment:a00-4e3f8a7b-8edc1e`): the token comes
from the environment (`COPILOT_GITHUB_TOKEN` > `GH_TOKEN` > `GITHUB_TOKEN`),
and `copilot login --with-token` exits 1 with "Login succeeded, but the token
was not saved. Install a system keychain" — so nothing persists and every
spawn must carry a token. `child_env` resolves one (env first, then
`gh auth token`) and injects it as `GH_TOKEN`:

```
$ python3 -c "... cp.child_env(harness={'adapter':'copilot_cli'}, base={}) ..."
GH_TOKEN present: True len 40 prefix gho_
needs_credential: False
resolve_bin no-harness: /home/ubuntu/.npm-global/bin/copilot
```

`needs_credential` returns False for the same reason Claude Code's does:
Copilot authenticates through its own GitHub token, not an OpenRouter key, so
dispatch must not mint one for it.

**The reaper knob needs no adapter line.** `hypothesis:l4-spawn-paths-export-
the-reaper-knob` is satisfied by `dispatch.py` itself, on every harness:

```
$ grep -rn CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP extensions/agi/bin/adapters/ extensions/agi/bin/dispatch.py
extensions/agi/bin/dispatch.py:1220:  env[...] = "1"     # dry-run mirror
extensions/agi/bin/dispatch.py:2327:  spawn_env[...] = "1"   # live spawn, unconditional
grep: adapters/: no matches
```

No adapter sets it, so mirroring it is a no-op for the third harness — the
dispatcher already owns it.

## Evidence

### 1. The BUILT command (conjunct 4) — dry-run, never a spawn

```
$ python3 extensions/agi/bin/dispatch.py . L4.366 --harness copilot-cli --tier kid --dry-run
harness: --harness copilot-cli overrides ladder row harness pi (using copilot-cli models for tier kid)
[dry-run] slot=0 harness=copilot-cli tier=kid role=kid ladder_tier=0 level=big target=- brief_tier=kid
  command: /home/ubuntu/.npm-global/bin/copilot --model auto --allow-all-tools -p '# dry-run context (placeholder, no zoom render)
...
dry-run: nothing spawned, nothing written, no budget slot taken
```

The binary path from the config row appears, `--model auto` is the config
row's model carried verbatim, `--allow-all-tools` is the non-interactive
requirement, and the brief is the `-p` argument. Exit 0.

### 2. Tests (conjunct 7) — 21 new, 245 across the covering files, all green

```
$ python3 -m pytest extensions/agi/tests/test_copilot_cli_adapter.py -q
21 passed in 0.49s

$ python3 -m pytest extensions/agi/tests/test_copilot_cli_adapter.py \
    extensions/agi/tests/test_adapters.py extensions/agi/tests/test_claude_code_adapter.py \
    extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_dispatch_dry_run.py \
    extensions/agi/tests/test_dispatch_model_allowlist.py -q
245 passed, 2 warnings in 15.55s
```

The new tests are fixture-only: a fake `copilot` shell script on PATH records
its argv and is executed (asserting the argv is a valid invocation); no test
calls a live `copilot`. They assert: the binary/env/tier routing, that EVERY
brief segment (context, kid brief, skill prompt, closing line) lands in the
one `-p` prompt in order, that a missing context file is an error not a quiet
omission, that a missing tier is a named KeyError, that `child_env` injects a
token from `gh auth token` when none is set and never invents one, that
`needs_credential` is False, and that `restart` rebuilds the same argv and
re-enters the recorded worktree (Popen faked, no process started).

A separate live-config test reads the REAL `.agi/config.json` and asserts the
shipped `copilot-cli` row resolves through the same `adapters.resolve` the
dispatcher calls — a copied model list would certify nothing.

### 3. Conjunct 5 — hooks parity: the documented route, and why it is not wired

`copilot help config`, verbatim:

```
  `disableAllHooks`: whether to disable all hooks (repo-level and user-level); defaults to `false`.

  `hooks`: inline hook definitions, keyed by event name (same schema as .github/hooks/*.json).
    - In global config.json these act as user-level hooks; in repo settings.json they act as repo-level hooks
```

The event vocabulary kid 1 measured is the Claude Code one (`sessionStart`,
`userPromptSubmitted`, `preToolUse`, ...), so the parity route exists in
principle. It is NOT registered here, and not faked: the CLI has no hook-run
subcommand (only `-p` starts a session), so proving a `sessionStart` hook
fires would cost a live premium turn against the live repo. The claim allows
the fallback, so the fallback is what shipped:

- **SessionStart map injection** — the zoom context and every brief segment
  are in the `-p` prompt. Proven by
  `test_every_brief_segment_lands_in_the_one_prompt` and by the dry-run
  command above.
- **UserPromptSubmit meter line** — NOT wired. The named source for a later
  round is the CLI's own session log (`--log-dir`, default `~/.copilot/logs/`)
  or `--usage-output-file`; the adapter sets neither today.

**Prime line:** the third harness is one config row plus one file —
`copilot_cli_adapter.py` — with `dispatch.py` untouched, 21 new fixture-only
tests green, and the brief carried in `-p` because Copilot has no system-prompt
flag.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version exists because the parent is a BUILD ORDER that four previous
kids had answered by measuring (`hypothesis:l4-a-g15-claim-is-a-build-order-
not-a-measurement`). It differs from kid 1's node in kind, not degree: kid 1
proved the binary installs, authes and exits 0; this node makes the engine
able to spawn it.

One deliberate deviation from the brief's literal config: it asked for
`allowed_models: ["auto"]`, I shipped `allowed_extra: ["auto"]`. The
allowlist is now DERIVED (`adapters.derived_allowed_models`, union of ladder
rows + `allowed_extra` + legacy `allowed_models`), and the legacy key prints a
stderr warning on EVERY dispatch naming itself a non-input. `allowed_extra`
is the post-migration spelling of the same census, so the model is allowed
silently and the row says what it means. The observable behaviour is
identical (`--model auto` reaches the command, proven above).

A false warning surfaced on this path and is NOT fixed here, because the fix
is in `dispatch.py`, which the brief told me to leave alone: the
`harnesses.<h>.models is/are NON-INPUTS` warning fires whenever a ladder row
was matched, but an explicit `--harness` beats the row's harness and THEN the
config row's `models` ARE the input. Dispatch printed "harnesses.copilot-cli.
models ... NON-INPUTS" while emitting `--model auto` from exactly that block.
Pre-existing for any third harness; named in the node so the next reader does
not trust the line.
<!-- THOUGHT:END -->

## Agent Notes
Built the third harness: new adapters/copilot_cli_adapter.py + config row, dispatch.py untouched; dry-run prints /home/ubuntu/.npm-global/bin/copilot --model auto --allow-all-tools -p '<brief>'; 21 new fixture-only tests, 245 green across covering files; hooks parity ships as the allowed prompt-injection fallback.

PARENT REVIEW PROBES (a00-cd9b4aa1, 2026-09-14): wire — live dry-run "dispatch.py . L4.366 --harness copilot-cli --tier kid --dry-run" independently emits "/home/ubuntu/.npm-global/bin/copilot --model auto --allow-all-tools -p ..." (config row reaches the built argv; dispatch.py untouched). gate — unknown tier raises KeyError "declares no model for tier nonesuch"; missing context file raises FileNotFoundError (refuses a spawn without its map). auth — needs_credential({}) False (no OpenRouter key minted). Test bytes inspected: fake copilot shell script on PATH, Popen faked, no live copilot call. ACCEPTED conjuncts 4+7. Conjunct 5 is the claim-allowed fallback (prompt injection + no meter wired) and is stated plainly. Remaining: conjunct 6 rotate shape -> kid 3.
