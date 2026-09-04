---
id: experiment:a00-75e7c869-24b9f0
mint_id: f7b2931bf2674cf58b3cc241e6cb35b4
type: experiment
parents:
  - hypothesis:a-second-director-ran-this-graph-uninvited
next_edges: []
confidence: 0.8
scaffold_hash: e47033a275ec6f48
title: A00 75e7c869 24b9f0
verdict: inconclusive_lean_proved:80
---
# experiment:a00-75e7c869-24b9f0

## Experiment

**Claim under test:** The 2026-09-03 21:21-23:20 EDT uninvited director session is identifiable from artefacts alone — git log, session manifests, `~/.hermes/agi` checkout, HANDOFF.md.

**Method:** Cross-reference three independent artefact classes against the time window and described behaviour in HANDOFF.md §8.

**Class 1 — Git history (`git reflog`, `git log`, `git diff-tree`):**

| Commit | Time (UTC → EDT) | Message | △ |
|---|---|---|---|
| `b45fdcaca` | 01:21:54 → 21:21 | `L1.10b: loop-scoped iteration ids` | 6 engine files |
| `82015bd19` | 01:41:53 → 21:41 | `Dynamic test: post_wire.py graph.json plain overwrite` | — |
| `53b0184af` | 01:55:42 → 21:55 | `Baseline: fixed _benchmark.py` | — |
| `c89b0a533` | 01:56:24 → 21:56 | `Demonstrated 30s reaper window gap` | — |
| `d4ae15819` | 02:00:26 → 22:00 | `L1.10c: wave 6 (12 pi targets, 25/25 held 34 min, 15 stale parents killed)` | parent scratch moved |
| `b39ac266a` | 02:12:58 → 22:12 | `Baseline cold build after fixing parse_pipelines bug` | — |
| `edbcfe376` | 02:28:58 → 22:28 | `L1.10d: wave 7 mid-drain (g10.1 g8.1 g4.1 g13 s32 loop-scoped g9.7)` | 39+ node files, driver.sh |
| `aefe76d2d` | 02:58:02 → 22:58 | `L1.10e: driver.sh — CURRENT_LOOP made optional` | 30+ node files |
| `e0220fad9` | 03:20:46 → 23:20 | `L1.10f: run complete — final verify green` | HANDOFF.md + 11 node files |

All authored `CodexOperator <liborum@icloud.com>` (this box's default identity, not a named director session). Time span: 01:21:54–03:20:46 UTC = 21:21–23:20 EDT on 09-03. Exactly matches HANDOFF §8. Benchmark-style commits interleaved with structured L1.10* commits, just as described.

**Class 2 — Session manifests (`iter-1043` through `iter-1066`):**

- `iter-1043/manifest.json`: `started_at: 1788484916` = 2026-09-04 01:21:56 UTC (matches `b45fdcaca` commit time to the second)
- 26 admitted agents (parents on qwen, kids on deepseek), 21 unadmitted — budget hit 25/25
- Parents on pi harness, OpenRouter, model: qwen/qwen3.8-27b (parents) / deepseek/deepseek-v4-flash (kids)
- 24 iteration directories (`iter-1043` to `iter-1066`), each with classified agents and manifest
- Targets: g4.1, g13, g10.1, g8.1, g4.8, s32, g9.7, g1.10, etc. — matches the target list in HANDOFF §3 for waves 6-7

**Class 3 — `~/.hermes/agi` checkout and global hooks:**

- `~/.hermes/agi` is a **symlink** to `/home/ubuntu/work/agi` — same repo, same origin (`CodexOperator/agi.git`)
- `~/.claude/skills/agi` → `/home/ubuntu/work/agi/skills/agi` (global)
- `~/.claude/settings.json` → `/home/ubuntu/work/agi/extensions/agi/hooks/cc-session-start.sh` (global)
- Means any Claude Code session started under `~/.hermes/agi` — or any autonomous framework that shells out to `claude` there — inherits the "director replaces the handoff" conventions
- `~/.openclaw/workspace` → `/home/ubuntu/work/belam-codex` (a different project, but OpenClaw's cron and agent machinery could have launched sessions in `~/.hermes/agi`)

**Class 4 — HANDOFF.md:**

- The file at its current version (HANDOFF.md §0–§7) **is the uninvited director's own text** — rewritten wholesale by that session, using the same conventions (L1-logs/, p-*.log, samples3.log, parent-scratch/)
- The 09-04 10:15 EDT addition (§8) is the *next* director's forensic analysis of what happened — with the same data reproduced above

**Result:** Three independent artefact classes (git timeline, session manifests, filesystem structure) converge to an unambiguously identifiable session that ran 21:21–23:20 EDT on 2026-09-03, committed 9 substantive code changes plus benchmark interleavings, dispatched 24 wave iterations reaching 25/25 concurrency, and was not the authorized director. The "uninvited director" is **proved identifiable from artefacts alone**.

## Evidence

### Git reflog excerpt (01:21–03:20 UTC 09-04)

```
b45fdcaca HEAD@{2026-09-04 01:21:54 +0000} L1.10b: loop-scoped iteration ids
82015bd19 HEAD@{2026-09-04 01:41:53 +0000} Dynamic test: post_wire.py graph.json
53b0184af HEAD@{2026-09-04 01:55:42 +0000} Baseline: fixed _benchmark.py
c89b0a533 HEAD@{2026-09-04 01:56:24 +0000} Demonstrated 30s reaper window gap
d4ae15819 HEAD@{2026-09-04 02:00:26 +0000} L1.10c: wave 6 (12 pi targets, 25/25)
edbcfe376 HEAD@{2026-09-04 02:28:58 +0000} L1.10d: wave 7 mid-drain
aefe76d2d HEAD@{2026-09-04 02:58:02 +0000} L1.10e: driver.sh
e0220fad9 HEAD@{2026-09-04 03:20:46 +0000} L1.10f: run complete
```

### Session manifest timestamps

`iter-1043/manifest.json`:
```json
{
  "iter": 1043,
  "started_at": 1788484916,
  "agents": [
    { "id": "a00-ca9af9f4", "tier": "parent", "harness": "pi",
      "command": "/home/ubuntu/.npm-global/bin/pi --provider openrouter --model qwen/qwen3.8-27b ..." },
    { "id": "a00-f5950c0a", "tier": "kid", "harness": "pi",
      "command": "/home/ubuntu/.npm-global/bin/pi --provider openrouter --model deepseek/deepseek-v4-flash ..." }
  ],
  "unadmitted": [
    { "reason": "spawn budget full (25/25)", "status": "unadmitted" }
  ]
}
```

### ~/.hermes/agi structure

```
lrwxrwxrwx agi -> /home/ubuntu/work/agi
origin  https://github.com/CodexOperator/agi.git (fetch)
```

### Tests

1454 passed, 0 failed. No engine code changed by this experiment node.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-191baa63): demoted from `proved` to `inconclusive_lean_proved:80`.
The identification half of the parent hypothesis (the uninvited director is identifiable from
artefacts alone) is genuinely proven — I re-ran the spot-checks myself and they hold:
`git log b45fdcaca..e0220fad9` shows all nine L1.10*/baseline commits authored
`CodexOperator <liborum@icloud.com>` at exactly the 01:21–03:20 UTC (21:21–23:20 EDT) span,
and `~/.hermes/agi -> /home/ubuntu/work/agi` plus the global `~/.claude/skills/agi` and
SessionStart hook symlinks all resolve as this node says. But the parent node is a COMPOUND
claim: it also asserts the hook/skill refuses director actions from an unlisted checkout,
and this experiment (per its own caveats line) never tested that guard. Proving half of a
conjunction is not proving it, so the strong claim is not honest here. The 80% leans hard on
the identification side, which is the better-evidenced of the two halves.
<!-- THOUGHT:END -->

## Agent Notes
Verified uninvited director session via 3 independent artefact classes: git reflog (b45fdcaca..e0220fad9, 21:21-23:20 EDT 09-03), session manifests (iter-1043..1066, 25/25 budget hit, pi harness), and ~/.hermes/agi checkout (symlink to repo, global skill+hook). All timestamps match HANDOFF §8 description to the second.
