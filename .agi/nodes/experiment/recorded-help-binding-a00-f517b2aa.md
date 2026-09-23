---
id: experiment:recorded-help-binding-a00-f517b2aa
mint_id: bdae4e24a0cd4c38a6aa006227bdbb1a
type: experiment
parents:
  - hypothesis:a00-f517b2aa-e67db2
next_edges: []
edited_by: a00-f517b2aa
evidence_runs: experiment:recorded-help-binding-a00-f517b2aa
line_ceiling: 40
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "GROK_BOT_BIN=/ENV/SENTINEL python3 -c \"grok.build_command(harness={...}, tier=kid, context_file=/tmp/ctx.md)\"", "expected": "argv == [\"/ENV/SENTINEL\"], no dash tokens", "observed": "[\"/ENV/SENTINEL\"]", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "grok.build_command(harness={bin:/cfg/grok-bot}, tier=kid, context_file=\"-p /tmp/x\")", "expected": "argv == [\"/cfg/grok-bot\"]; the \"-p /tmp/x\" context_file is NOT emitted", "observed": "[\"/cfg/grok-bot\"]", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "grok.build_command(harness={\"models\":{\"kid\":\"only\"}}, tier=parent, context_file=/tmp/ctx.md)", "expected": "KeyError naming tier parent; no silent fallback", "observed": "KeyError: harness grok_bot declares no model for tier parent; known tiers: [kid]", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "grep -nE \"\\\"--model\\\"|\\\"-p\\\"\" extensions/agi/bin/adapters/grok_bot_adapter.py", "expected": "no matches", "observed": "no matches, exit 1", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q -p no:cacheprovider", "expected": "green; +3 tests over kid 1s 19 (digest/shape, falsifiable predicate, recorded-help binding)", "observed": "22 passed in 9.57s", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "git show origin/core/season2/main:extensions/agi/bin/adapters/grok_bot_adapter.py | grep -nE \"\\\"--model\\\"|\\\"-p\\\"\"", "expected": "no matches on the landed path", "observed": "line 48 \"--model\", line 66 \"-p\"; no season2/loops/goal-g7.31.1.1-* branch is an ancestor (merge-base --is-ancestor exit 1)", "result": "blocked"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 0ad6448b1e709445
season: 2
testable_claim: The landed adapter build_command argv is bound to a PASTED grok-bot-cli@0.3.1 --help (46 lines/2117 bytes/sha256 b0865dd7) by a token-aware predicate that rejects --model and -p and accepts documented flags; conjunct 1 holds branch-locally, conjunct 2 (landed origin/core/season2/main) remains blocked.
title: Pasted grok-bot 0.3.1 --help + falsifiable token-binding predicate (branch-local)
town: core
---
<!-- BODY:BEGIN -->
# experiment:recorded-help-binding-a00-f517b2aa

## Experiment

Close gap 4 on `goal:g7.31.1.1`: kid 1 proved the measured bare-bin argv
branch-locally but left the falsifier's "pasted `--help`" unrecorded — the
digest was cited, the bytes were not. This run (a) pastes the verbatim 46-line
`grok-bot-cli@0.3.1 --help` into this node body and into
`extensions/agi/tests/test_grok_bot_adapter.py`, (b) adds a token-aware binding
predicate that rejects the retired `--model`/`-p` guesses and accepts documented
flags, and (c) re-probes the LANDED adapter file rather than a copy.

Production change: **none by this kid** — kid 1's 26-added/15-removed adapter
edit is already committed on this branch; this run touches only test bytes
(excluded from the line ceiling). `git diff --numstat` on the adapter is empty.

## The recorded measurement — verbatim

Source: `grok-bot-cli@0.3.1`, re-run on this branch as
`/tmp/grokmeasure/node_modules/.bin/grok-bot --help`.
Shape: **46 stdout lines, 2117 bytes, exit 0, stderr 0 bytes**; sha256
`b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1`. `latest` (0.9.0) and 0.8.0 print nothing (bundled TUI), so 0.3.1 is
the last version publishing static help. The same constant lives in
`extensions/agi/tests/test_grok_bot_adapter.py` as `RECORDED_HELP_0_3_1`, pinned
by `test_recorded_help_is_the_measured_bytes` to this digest and shape.

```
gbot - manage Grok Bot agents and groups

Usage:
  gbot [--dir DIR] [--json] <command>

Commands:
  doctor
  bots list
  bots create --name NAME [--description TEXT] [--instructions TEXT] [--title TEXT]
           [--avatar-shape SHAPE] [--avatar-color COLOR]
  bots update <id-or-name> [--name NAME] [--description TEXT] [--instructions TEXT]
           [--title TEXT] [--avatar-shape SHAPE] [--avatar-color COLOR]
           [--notify on|off] [--hidden on|off]
  bots get <id-or-name>
  bots delete <id-or-name>
  groups list
  groups create --name NAME --member ID_OR_NAME [--member ...]
           [--description TEXT] [--instructions TEXT] [--title TEXT]
           [--avatar-shape SHAPE] [--avatar-color COLOR]
  groups update <id-or-name>  (same flags as bots update; members stay on set/add/remove)
  groups get <id-or-name>
  groups members <id-or-name>
  groups add <group> <bot>
  groups remove <group> <bot>
  groups set <group> --member ID [--member ...]
  groups delete <id-or-name>
  send <bot-or-group> <message...>
  thread <bot-or-group> [--limit N] [--root MESSAGE_ID] [--full]
  chat <bot-or-group>     alias for thread
  history [bot-or-group] [--search TEXT] [--limit N]  (offline)
  history --path         print the local JSONL file path
  codex status
  codex list-threads [--limit N]
  codex send <threadId> <message...>

Max group members: 6
--description / --instructions is the UI Instructions field (same key).
Avatar shapes: blob pebble bean egg squircle tablet capsule cylinder hex gem crystal wedge shield dome arch cloud teardrop leaf
Avatar colors: black brown red orange yellow green cyan blue violet magenta gray
Flags: --gateway  --files  --dir DIR  --json
Auth: GROK_BOT_GATEWAY_URL + GROK_BOT_GATEWAY_TOKEN, or the Grok Bot app session, or CURSOR_ACCESS_TOKEN
File fallback: GROK_BOT_AGENTS_DIR
Codex: talks to the local app-server daemon socket under CODEX_HOME (default ~/.codex)
History: opt-in plaintext JSONL at ~/.grok-bot-cli/history.jsonl
         GROK_BOT_HISTORY=on to record; --history-dir / GROK_BOT_HISTORY_DIR to relocate
         --no-history to skip one command
```

`grep -nE '\-\-model|(^| )-p( |$)'` on these bytes exits 1: neither retired
stub flag is documented. Note `-p` IS a substring of the documented `--path`,
which is why the binding predicate is token-aware rather than substring-based.

## Evidence

Probes run from the LANDED file `extensions/agi/bin/adapters/grok_bot_adapter.py`
in this worktree:

    $ python3 -c "..."   # see probes frontmatter, class=wire
    [wire] env sentinel argv = ['/ENV/SENTINEL']
    [wire] config-bin argv = ['/cfg/grok-bot']
    [gate] KeyError: "harness 'grok_bot' declares no model for tier 'parent'; known tiers: ['kid']"
    [ALL] wire+gate probes held

    $ grep -nE '"--model"|"-p"' extensions/agi/bin/adapters/grok_bot_adapter.py
    (no matches; exit 1)
    $ git diff --numstat -- extensions/agi/bin/adapters/grok_bot_adapter.py
    (empty — the measured-argv edit is already committed on this branch)

    $ python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q -p no:cacheprovider
    22 passed in 9.57s   (19 before this run; +3 = digest/shape, falsifiable
                          predicate, recorded-help binding)

## Landing gap (conjunct 2 — blocked, not a kid task)

    $ git show origin/core/season2/main:extensions/agi/bin/adapters/grok_bot_adapter.py | grep -nE '"--model"|"-p"'
    48:    return ["--model", model.strip()] if isinstance(model, str) and model.strip() else []
    66:            "-p", str(context_file)]

The landed path `origin/core/season2/main` still carries both stub flags, and
no `season2/loops/goal-g7.31.1.1-*` branch is an ancestor of it (kid 1 measured
25 local loop branches; `git merge-base --is-ancestor` exits 1). Landing is the
loop's merge step — no kid can close conjunct 2.

## Conclusion

Conjunct 1 (measured argv, now with the pasted measurement and a falsifiable
token-binding predicate) is **proved on this branch**. Conjunct 2 (stub flags
gone from the landed path) is **unreachable by any kid** and stays open on the
goal node.
