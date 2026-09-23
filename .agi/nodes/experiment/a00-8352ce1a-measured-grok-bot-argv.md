---
id: experiment:measured-grok-bot-argv
mint_id: d39e5696202440e1a65565096694e5f1
type: experiment
parents:
  - hypothesis:a00-8352ce1a-20fa43
next_edges: []
confidence: 0.97
edited_by: a00-5b01c7ca
evidence_runs:
  - experiment:measured-grok-bot-argv
line_ceiling: 40
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 -c 'import adapters; g=adapters.load(\"grok_bot\"); print(g.build_command(harness={\"adapter\":\"grok_bot\",\"bin\":\"/SENTINEL/grok-bot\"}, tier=\"kid\", context_file=\"/tmp/x\"))'", "expected": "['/SENTINEL/grok-bot'] (bare bin; matches recorded grok-bot --help)", "observed": "['/SENTINEL/grok-bot']  is_bare=True", "result": "pass"}
  - {"conjunct": 1, "class": "measurement", "cmd": "/tmp/grokmeasure/node_modules/.bin/grok-bot --help > help.txt; echo exit=$?; wc -l < help.txt; sha256sum help.txt; grep -nE '(^| )-p( |$)|--model' help.txt; echo grep_exit=$?", "expected": "exit=0; 46 lines; sha256 b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1; grep_exit=1 (no -p, no --model)", "observed": "exit=0; 46; b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1; grep_exit=1", "result": "pass"}
  - {"conjunct": 2, "class": "grep", "cmd": "grep -nE '\"--model\"|\"-p\"' extensions/agi/bin/adapters/grok_bot_adapter.py; echo grep_exit=$?", "expected": "grep_exit=1 (no guessed flag literals on the landed adapter path)", "observed": "grep_exit=1", "result": "pass"}
production_lines: 25
profile: balanced
role: kid
scaffold_hash: 87827931e2eb280f
season: 2
title: "Measured grok-bot CLI argv: bare resolved bin, stub -p/--model retired"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:measured-grok-bot-argv

## Experiment

Built `goal:g7.31.1.1`: the stub `build_command` in
`extensions/agi/bin/adapters/grok_bot_adapter.py` is replaced with the argv
measured against `grok-bot --help`. Falsifier conjuncts from the target:
(1) `build_command` argv matches a pasted `--help` measurement;
(2) stub-only guessed flags (lone `-p`, `--model`) are gone from the landed
adapter path.

### Raw measurement (`grok-bot --help`)

```
$ /tmp/grokmeasure/node_modules/.bin/grok-bot --help > help.txt ; echo exit=$?
exit=0
$ wc -l < help.txt
46
$ sha256sum help.txt
b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1  help.txt
$ grep -nE '(^| )-p( |$)|--model' help.txt ; echo grep_exit=$?
grep_exit=1
```

Full 46-line output, verbatim:

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

The help names no brief flag and no model flag; brief delivery is
`send <bot-or-group> <message...>` (`goal:g7.31.4`).

### Wire probe (fresh interpreter)

```
$ python3 - <<'PY'
import sys, pathlib
sys.path.insert(0, "extensions/agi/bin")
import adapters
g = adapters.load("grok_bot")
argv = g.build_command(harness={"adapter":"grok_bot","bin":"/SENTINEL/grok-bot"}, tier="kid", context_file="/tmp/x")
print("argv =", argv)
print("is_bare =", argv == ["/SENTINEL/grok-bot"])
print("model_args =", g.model_args({"adapter":"grok_bot","models":{"kid":"only"}}, "kid"))
try:
    g.model_args({"adapter":"grok_bot","models":{"kid":"only"}}, "parent")
except KeyError as e:
    print("KeyError names tier:", "parent" in str(e), "--", e)
PY
argv = ['/SENTINEL/grok-bot']
is_bare = True
model_args = []
KeyError names tier: True -- "harness 'grok_bot' declares no model for tier 'parent'; known tiers: ['kid']"
```

### Gate: guessed flags gone

```
$ grep -nE '"--model"|"-p"' extensions/agi/bin/adapters/grok_bot_adapter.py ; echo grep_exit=$?
grep_exit=1
```

### Pytest tail

```
$ python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q -p no:cacheprovider
.................                                                        [100%]
17 passed in 7.85s
```

### Artifact

`extensions/agi/bin/adapters/grok_bot_adapter.py`
sha256 `6c5b44fa13566d5f9256ba2a14269d6f330979f80e053d892e4584f108b286c0`,
170 lines. `build_command` returns `[resolve_bin(harness)]`;
`model_args` is validation-only (missing tier still raises `KeyError`
naming the tier) and returns `[]`. `context_file` stays in the signature
for seam compatibility and is not emitted. `dispatch.py` / `rotate.py`
untouched (0 `grok` hits).
Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review DH.139, a00-5b01c7ca. Read the bytes, not the result file: extensions/agi/bin/adapters/grok_bot_adapter.py sha256 6c5b44fa13566d5f9256ba2a14269d6f330979f80e053d892e4584f108b286c0, 170 lines; build_command runs model_args for validation then returns [resolve_bin(harness)]; the quoted flag literals are gone (grep exits 1). Ran one parent probe per falsifier conjunct. (1) WIRE: fresh interpreter, adapters.load(grok_bot).build_command(harness={adapter:grok_bot,bin:/SENTINEL/grok-bot}, tier=kid, context_file=/tmp/SECRET_CONTEXT.md) returned [/SENTINEL/grok-bot] -- the context path did not leak and no -p/--model token appears; three harness shapes each emit exactly [resolve_bin(h)]. (2) GATE: grep -nE '"--model"|"-p"' adapter.py exits 1; a missing tier still raises KeyError naming the tier (validation preserved); dispatch.py and rotate.py each carry 0 grok hits. WHAT THE INSTRUCTION SAID: falsifier conjuncts (1) build_command argv matches a pasted --help measurement and (2) stub-only guessed flags gone from the landed adapter path. WHAT THE MACHINE ACTUALLY DOES: the recorded 46-line 0.3.1 help (sha256 b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1, re-measured this round, /tmp/grokmeasure) names no -p and no --model and drives gbot by subcommands with send <bot-or-group> <message...> for the brief, so the bare resolved bin is the measured argv. NEAR MISS: a test asserting only quoted-literal absence would stay green while an unquoted or aliased -p re-entered argv; my probe scans the emitted argv itself, not just the source text. CAVEAT: the falsifier names core/season2/main; the measured bytes are landed on THIS loop branch season2/loops/goal-g7.31.1.1-a00-5b01c7ca, so merge-up to main remains the director step. Build node BODY still claims the old stub sha 66b7891f while its THOUGHT and Agent Notes carry 6c5b44fa; BODY is derived and will be regenerated, but until then it is stale.
<!-- THOUGHT:END -->
