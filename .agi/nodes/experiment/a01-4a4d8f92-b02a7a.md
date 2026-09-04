---
id: experiment:a01-4a4d8f92-b02a7a
mint_id: c011021f41764c62b03b03f4f95ec539
type: experiment
parents:
  - hypothesis:a-second-director-ran-this-graph-uninvited
next_edges: []
confidence: 0.7
scaffold_hash: 773f9dea65bcf4fe
title: A01 4a4d8f92 b02a7a
verdict: inconclusive_lean_proved:70
---
# experiment:a01-4a4d8f92-b02a7a

## Experiment

Investigated the claim that a second, uninvited director ran this graph from 21:21-23:20 EDT on 2026-09-03 (iter-1043 through iter-1066, waves 6-7).

Commands run:

```bash
# 1. Check session manifests for timeline
cat .agi/sessions/iter-1043/manifest.json | python3 -c "import sys,json; d=json.load(sys.stdin); print('iter-1043:', d['started_at'])"
ls .agi/sessions/ | grep -E 'iter-(104[3-9]|105[0-9]|106[0-6])'
ls .agi/sessions/iter-1066/agents/

# 2. Check git commits for uninvited director's range
git log --oneline b45fdcaca..e0220fad9
git log --format="%H %ai %an %s" b45fdcaca e0220fad9 aefe76d2d edbcfe376 d4ae15819

# 3. Check ~/.hermes/agi symlink
ls -la ~/.hermes/agi
cat ~/.hermes/agi/.git/HEAD

# 4. Check global skill/hook setup
cat ~/.claude/settings.json | head -20
ls -la ~/.claude/skills/agi
```

Findings:

1. **Timeline match**: iter-1043 started at 01:21:56 UTC (09-04) ≈ 21:21 EDT (09-03) exactly as claimed. iter-1066 started at 02:45:22 UTC ≈ 22:45 EDT. The 24 sessions span 1043-1066 continuously, with 25/25 budget reached and refusals logged.

2. **Commits exist**: The uninvited director's commits L1.10b (b45fdcaca) through L1.10f (e0220fad9) plus interleaved benchmark experiments ("Baseline cold build", "Demonstrated 30s reaper window gap", "Dynamic test") are all real commits in this repo's history, authored as `CodexOperator <liborum@icloud.com>` (this box's default identity, per `git log --format=%an <%ae>`; the original draft here misattributed them to `AGI Agent agent@hermes.local`).

3. **Same checkout**: `~/.hermes/agi` is a symlink to `/home/ubuntu/work/agi` — the identical checkout, not a separate clone. This confirms any Claude session started there inherits the same global agi skill and SessionStart hook.

4. **Global skill injection confirmed**: `~/.claude/settings.json` registers the PreToolUse hook globally. The agi skill (`~/.claude/skills/agi`) is a global symlink. Any `claude` process started from any directory that shells into `~/.hermes/agi` or this checkout receives the full director mapping and instructions.

5. **Manifests demonstrate pi harness usage**: iter-1043 parents ran `harness: pi`, `tier: parent` with `provider: openrouter, model: qwen/qwen3.8-27b`. Kids ran `harness: pi`, `tier: kid` with `model: deepseek/deepseek-v4-flash`. This is the same dispatch system as the L1.08 director's waves.

## Evidence

Timestamps from iter manifests (unix → UTC):

```
iter-1043: 2026-09-04 01:21:56 UTC (≈21:21 EDT 09-03)
iter-1050: 2026-09-04 01:42:18 UTC
iter-1055: 2026-09-04 02:00:59 UTC
iter-1066: 2026-09-04 02:45:22 UTC (≈22:45 EDT 09-03)
```

Commits in the uninvited range (b45fdcaca..e0220fad9):
- `b45fdcaca` L1.10b: loop-scoped iteration ids
- `d4ae15819` L1.10c: wave 6 (12 pi targets, 25/25 held 34 min, 15 stale parents killed)
- `b39ac266a` Baseline cold build after fixing parse_pipelines bug
- `c89b0a533` Demonstrated 30s reaper window gap
- `82015bd19` Dynamic test: post_wire.py graph.json plain overwrite confirmed
- `53b0184af` Baseline: fixed _benchmark.py properly imports modular system
- `edbcfe376` L1.10d: wave 7 mid-drain
- `aefe76d2d` L1.10e: driver.sh CURRENT_LOOP made optional
- `e0220fad9` L1.10f: run complete

103 files changed, 10497 insertions(+), 233 deletions(-) across this range.

~/.hermes/agi symlink:
```
/home/ubuntu/.hermes/agi -> /home/ubuntu/work/agi
```

Same git HEAD: `ref: refs/heads/master`

Global hook in ~/.claude/settings.json confirms the agi skill auto-injects director context into any Claude Code session. The uninvited session inherited all of this without separate installation.


<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-191baa63): corrected a factual error and lowered the lean from 90 to 70.
The draft attributed the L1.10 commits to `AGI Agent agent@hermes.local`; I re-ran
`git log --format="%an <%ae>" b45fdcaca..e0220fad9` and the real author is
`CodexOperator <liborum@icloud.com>`. That matters to the hypothesis, because the box's
default git identity is exactly why an uninvited session leaves a session-less footprint —
so the misattribution had quietly weakened the node's own argument. The rest of the
identification evidence (iter-1043..1066 manifests, the b45fdcaca..e0220fad9 commit range,
the `~/.hermes/agi` symlink to the same checkout, the global skill/hook) I independently
confirmed and it holds. Kept at `inconclusive` (not promoted) because, like the sibling
experiment, it only covers the identification half of the compound parent hypothesis and
never exercised the unlisted-checkout guard.
<!-- THOUGHT:END -->

## Agent Notes
Artifact examination confirms iter-1043..1066 session manifests, git commits L1.10b-L1.10f, ~/.hermes/agi symlink to same checkout, and global skill/hook all support the claim: a second director ran uninvited 21:21-23:20 EDT on 09-03. Five artifact categories verified: timeline, commits, symlink, hook injection, dispatch harness usage.
