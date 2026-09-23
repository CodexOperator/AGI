---
id: experiment:a00-1cb228fe-grok-adapter-landed-measured
mint_id: 807e59b60aeb49268720289720888f8f
type: experiment
parents: hypothesis:a00-1cb228fe-9f2418
next_edges: []
edited_by: a00-a1658c96
line_ceiling: 40
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
probes: "parent a00-a1658c96 ran 4 negative probes on the landed bytes: (1) WIRE adapters.load(grok_bot).build_command(H,tier=kid,context_file=/tmp/ctx.md) == [/SENTINEL/grok-bot] and resolve_bin precedence env>row>default; (2) GATE build_command tier=ghost raises KeyError naming ghost, no silent fallback; (3) GATE grep of the adapter source finds no quoted --model/-p emission; (4) GATE RECORDED_HELP_0_3_1 byte-identical to live 0.3.1 --help (46 lines, 2117 bytes, sha256 b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1) and the token predicate is falsifiable: a tampered help carrying -p flips -p into the documented set. NEAR MISS measured: a naive substring check would false-positive because -p is a substring of --path; the landed predicate is token-aware. All four PASS."
production_lines: 76
profile: balanced
role: kid
scaffold_hash: 616e9f44f5a75003
season: 2
testable_claim: landed grok_bot adapter build_command returns bare bin, no --model/-p; RECORDED_HELP_0_3_1 byte-identical to live 0.3.1 --help (sha256 b0865dd7...); KeyError for unknown tier
title: "Measured grok_bot argv landed: bare bin, --model/-p gone, recorded --help byte-matches live 0.3.1; 28 tests green"
town: core
---
# experiment:a00-1cb228fe-grok-adapter-landed-measured

## What ran

Landed the MEASURED `grok_bot_adapter.py` and its hermetic test suite from
read-only `git show` of `season2/loops/goal-g7.31.1.1-a00-a3782a91`, then
re-measured the live `--help` and re-ran the suite on this base
(`core/season2/main` tip `42e742b56`). No git add/commit/merge was run.

Production diff (`git diff --numstat HEAD -- extensions/agi/bin/adapters/grok_bot_adapter.py`):
`59  17  extensions/agi/bin/adapters/grok_bot_adapter.py` = **76 production
lines**, ceiling 40, under 2x (80) → no re-brief owed.

## 1. Before / after argv

Live harness row `{"adapter":"grok_bot","bin":"/SENTINEL/grok-bot","models":{"kid":"grok-kid","parent":"grok-parent"}}`:

```
BEFORE (stub, HEAD 42e742b56):
  build_command(harness=H, tier="kid", context_file="/tmp/ctx.md")
  -> ["/SENTINEL/grok-bot", "--model", "grok-kid", "-p", "/tmp/ctx.md"]

AFTER (landed):
  build_command(harness=H, tier="kid", context_file="/tmp/ctx.md")
  -> ["/SENTINEL/grok-bot"]
```

```
$ grep -n '"--model"\|"-p"' extensions/agi/bin/adapters/grok_bot_adapter.py
(no output, exit 1)
```

Tier validation is kept without a flag:

```
$ build_command(harness=H, tier="unknown", ...)
KeyError: "harness 'grok_bot' declares no model for tier 'unknown'; known tiers: ['kid', 'parent']"
```

## 2. `--help` re-measured, not trusted

```
$ /tmp/grokmeasure/node_modules/.bin/grok-bot --help   # grok-bot-cli@0.3.1, exit 0
lines: 46   bytes: 2117
sha256: b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1
```

The pasted `RECORDED_HELP_0_3_1` constant in the landed test file was compared
byte-for-byte against that live capture:

```
recorded bytes: 2117   live bytes: 2117
recorded lines: 46     live lines: 46
byte-identical: True
sha256 rec == sha256 live == b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1
```

The help documents NO `--model` and NO `-p`; `send <bot-or-group> <message...>`
is how a brief travels. So the bare bin is the whole measured argv.

## 3. Suite

```
$ python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q
28 passed in 4.14s
```

Hermetic: no real process spawn. The previously flaky live-process test stays
DROPPED (DT.79) — the durable count is 28.

## 4. Residues from the DT.35 MUR

| # | Residue | Status on these bytes |
|---|---|---|
| 1 | scan-(c) aliased-env docstring must name the subtraction of scan-(a) dot-accesses | **CLOSED.** The `RECORDED_CLI_SOURCE_ENV_0_3_1` docstring now states that raw `\benv\.` returns 23 (it also matches the tail of `process.env.`) and that the 3 are raw MINUS scan (a) — the subtraction `probe_dt35.py` performs. |
| 2 | `probe_dt35.py` printed `spread/Reflect: 9` with zero actual spread/Reflect reads | **CLOSED.** Landed `extensions/agi/tests/probes/probe_dt35.py` splits the counter into `spread sites` / `Reflect sites` / `destructure sites` and gates `ok` on them. Re-measured on 0.3.1: spread 0, Reflect 0, destructure 0 (the old 9 were all `= process.env` default-parameter DECLARATIONS, already reported separately). PROBE: pass, exit 0. |
| 3 | in-scope test spawned a real process (~50% flake); hermetic suite drops it | **CLOSED by keeping it dropped.** Durable count re-measured: 28 passed. |
| 4 | node `experiment/a00-de42f4d7-real-respawn-measured-negative-control.md` misattributed `url-policy.js:13`; claimed true site `headers.js`/`truthyEnv` | **NOT CLOSED — outside my landed bytes, and the stated correction does not reproduce.** That node file is absent from this tree. Measured here: `grep -rn 'process.env\[' src` finds exactly ONE site, `url-policy.js:13`, inside `truthyEnv` (defined `url-policy.js:12`); its only callers are `url-policy.js:18,22`. `headers.js` contains no `truthyEnv` and no computed `process.env[...]` read (its only env touch is `process.env.GROK_BOT_GATEWAY_HEADERS` at `headers.js:29`, a dot-access already in scan (a)). So the landed test docstring's "exactly ONE dynamic site, url-policy.js:13" is CORRECT on these bytes, and the residue's proposed "true site = headers.js / truthyEnv callers" is itself a misattribution. Flagged for the parent to reject or carry. |

## 5. What this proves, and what it does not

Proves the falsifier's two conjuncts on the landed path: argv matches the
recorded `--help`, and the guessed flags are gone. Does NOT claim a live seat
(`goal:g7.31.1.2`, the restart/pane hold) — the bare-bin respawn prints help
and exits, pinned as a named residue by
`test_bare_bin_respawn_is_a_recorded_noop_residue`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-a1658c96 (DH.82). Instruction: review the kid DIFF, not its result file; run one negative probe per claim conjunct; a kid that passes its own tests but fails a probe is lean_disproved. Machine: the commit 24c3a2d5d carries the adapter blob 9e10bfa1 (76 production lines), the hermetic 516-line test file, probe_dt35.py, and both nodes; git status clean. I ran 4 probes on the landed bytes (recorded in probes:) and all pass, so no demotion. Near miss: the help token -p is a substring of --path, so a naive --p not in help -- check would false-positive; the landed predicate is token-aware and I verified it flips when a tampered help carries -p. Caveats recorded on the hypothesis node: the claim says on core/season2/main but the bytes are on the loop branch season2/loops/goal-g7.31.1.1-a00-a1658c96 and main still carries the stub until the director merges up; context_file is silently dropped with no send-brief wiring yet; a duplicate deprecated hypothesis node was minted and deprecated in the same round.
<!-- THOUGHT:END -->
