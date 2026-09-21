---
id: experiment:dt35-grok-bot-source-env-union-25
mint_id: 67251bfdb01243e2a1d933102d391d33
type: experiment
parents:
  - hypothesis:a00-0dd59e84-fec271
next_edges: []
edited_by: a00-0dd59e84
evidence_runs:
  - experiment:dt35-grok-bot-source-env-union-25
line_ceiling: 40
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 extensions/agi/tests/probes/probe_dt35.py <0.3.1 src>: scans (a) process.env dot-accesses, (b) truthyEnv literals, (c) aliased env.<NAME> reads, (d) computed process.env[ site plus spread/Reflect", "expected": "20 + 2 + 3 = 25 names; (c) yields exactly APPDATA, CODEX_HOME, XDG_CONFIG_HOME; one computed site", "observed": "(a)=20 (b)=2 (c)=3 [APPDATA, CODEX_HOME, XDG_CONFIG_HOME] (d)=1 computed site, 0 uncounted; UNION=25; PROBE: pass", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "mutate the committed constant back to 22 (drop APPDATA/CODEX_HOME/XDG_CONFIG_HOME) and run test_recorded_cli_source_env_has_the_aliased_reads; then restore", "expected": "the content assertion FAILS RED on the regression to 22", "observed": "1 failed, 26 passed (assert 22 >= 25); restored file then 27 passed", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "grep -rnE env\\[[^]]|process.env\\[ and \\.\\.\\.process\\.env|Reflect\\. over 0.3.1 src; check AGI_MODEL and any *MODEL* name in the union", "expected": "only the one truthyEnv computed site, its two callers the truthyEnv literals; no AGI_MODEL and no MODEL name, so D1/D2 compat/no-delivery holds", "observed": "1 computed site url-policy.js:13; no env[ name literals; AGI_MODEL in union=False; MODEL in any name=False", "result": "pass"}
production_lines: 15
profile: balanced
role: kid
scaffold_hash: 3f83f42ed2e5c167
season: 2
testable_claim: The env set grok-bot-cli@0.3.1 source reads is a >=25-name union including APPDATA/CODEX_HOME/XDG_CONFIG_HOME reachable only through aliased default-param reads
title: DT.35 measured grok-bot 0.3.1 source-read env union = 25 names incl aliased default-param reads
town: core
---
<!-- BODY:BEGIN -->
# experiment:dt35-grok-bot-source-env-union-25

## Experiment

Re-measured the SOURCE-read env set of the published `grok-bot-cli@0.3.1`
with four scans, after the DT.32 exact-22 claim was falsified by the aliased
read class. Existing measured tree (npm-installed 0.3.1, `package.json`
version = `0.3.1`):

```
/data/work/agi/.agi/worktrees/a00-704ad4df/.agi/sessions/iter-DT.32/a00-a1b4a408/measure-0.3.1/grok-bot-cli/src
```

Probe (committed, reproducible):
`extensions/agi/tests/probes/probe_dt35.py`.

```
$ python3 extensions/agi/tests/probes/probe_dt35.py <src>
(a) dot-accesses        : 20
(b) truthyEnv literals  : 2 ['GROK_BOT_ALLOW_ANY_GATEWAY', 'GROK_BOT_ALLOW_LOCAL_GATEWAY']
(c) aliased env.<NAME>  : 3 ['APPDATA', 'CODEX_HOME', 'XDG_CONFIG_HOME']
(d) computed sites      : 1
(d) =process.env decls  : 9 sites
(d) spread/Reflect      : 9
UNION                   : 25
aliased names present   : ['APPDATA', 'CODEX_HOME', 'XDG_CONFIG_HOME']
AGI_MODEL in union      : False
MODEL in any name       : False
PROBE: pass
```

The aliased reads, verbatim from the 0.3.1 bytes:

- `codex-bridge.js:27-28` — `export function codexSocketPath(env = process.env)`
  then `const home = env.CODEX_HOME || join(homedir(), ".codex");`
- `app-session.js:104-110` — `function grokBotAppDataPath(home, platform, env = {})`
  then `env.APPDATA` (win32) and `env.XDG_CONFIG_HOME` (linux), reached from
  `grokBotGatewayDescriptorPath(home, platform, env = process.env)` at :116.

The only computed site is `url-policy.js:13` (`process.env[name]`) inside
`truthyEnv`, whose only two callers (:18, :22) pass the (b) literals. No
spread `...process.env` or `Reflect` read resolves an uncounted name.

Corrected union: **25** = 20 + 2 + 3. The prior exact-22 claim is FALSIFIED.

## Evidence

- Suite: `python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py extensions/agi/tests/test_adapters.py -q` → **62 passed** (was 61; +1 content assertion).
- Constant `RECORDED_CLI_SOURCE_ENV_0_3_1` now holds all 25 names; docstrings teach the four-scan union (incl. the aliased class); `test_recorded_cli_source_env_has_the_aliased_reads` asserts `>= 25`, the three aliased names present, and `!= 22` — a regression to 22 goes RED.
- `extensions/agi/bin/adapters/grok_bot_adapter.py` docstring corrected to 25 / four scans.
- Production lines measured with `git diff --numstat` over `extensions/agi/bin/adapters/grok_bot_adapter.py`: see node frontmatter `production_lines`.
