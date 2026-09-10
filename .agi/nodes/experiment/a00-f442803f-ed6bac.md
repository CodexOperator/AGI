---
id: experiment:a00-f442803f-ed6bac
mint_id: 265001b4d5374a59936e63c427203ace
type: experiment
parents:
  - hypothesis:l4-dispatch-echoes-less-than-it-knows
next_edges: []
confidence: 0.75
edited_by: a00-1890b72a
evidence_runs:
  - experiment:a00-f442803f-ed6bac
loop: hypothesis:l4-dispatch-echoes-less-than-it-knows@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b39aa44412e653f7
season: 2
title: "Real-spawn observation: spawn.json exists and is redacted (pillar d)"
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-f442803f-ed6bac

## Experiment

Observed the real-spawn redaction artifact for
`hypothesis:l4-dispatch-echoes-less-than-it-knows` without spending a fresh
paid spawn: my own session dir IS the real Popen spawn the hypothesis's (c)(d)
pillars require.

Input: `.agi/sessions/iter-L4.109/a00-f442803f/spawn.json` (written by the
parent's dispatch call on this very spawn).

Checks run: file exists and parses as JSON; carries the four fields
{agent_id, argv, env, brief}; agent_id matches `a00-f442803f`; `brief` is the
full brief text (not a `<spawn.json brief assemble failed: ...>` string); every
env key name-matching KEY/TOKEN/SECRET/PASSWORD has a value of exactly
`"..." + last4` (length 7); a value-shape scan for raw `sk-` across ALL env
keys, named or not, finds zero leaks.

## Evidence

```
spawn.json keys: ['agent_id', 'argv', 'brief', 'env']
agent_id: a00-f442803f
OPENROUTER_API_KEY         => ...6dfe
GIT_CONFIG_KEY_0           => ...Path
CLAUDE_CODE_MESSAGING_TOKEN => ...ecf3
brief: str, 9347 bytes, head "─── CONSTITUTION HEAD ───"
argv entries: 39
```

Parent-side observation of pillar (c): the parent's real dispatch stdout for
this spawn was the single line

```
spawned a00-f442803f pid=2531168 tier=kid iter=L4.109
target=hypothesis:l4-dispatch-echoes-less-than-it-knows harness=pi
model=~deepseek/deepseek-v4-flash-latest
key=agi-iterL4.109-kid-a00-f442803f cap=$5.0 level=small strategy=extend_existing
```

— agent id, tier, iter, target, harness, model and the key's NAME and cap, and
no key value. Pillar (c) is the parent's tool result by construction; it cannot
be re-captured from inside the child.

## Conclusion

(d) observed: the redacted debug artifact lands on a real spawn. (c) observed
parent-side: the real spawn line is the one-line contract with key name + cap
and no value. Over-redaction of `GIT_CONFIG_KEY_0` (`core.hooksPath`, a path)
is a name-pattern false positive confined to spawn.json — harmless, noted.

## Agent Notes
## What I did

Observed the real-spawn redaction artifact for hypothesis:l4-dispatch-echoes-less-than-it-knows without spending a fresh spawn: my own session dir is the real Popen spawn the hypothesis (c)(d) pillars need.

Input: .agi/sessions/iter-L4.109/a00-f442803f/spawn.json (the parent's dispatch already wrote it on this spawn).
Checks: exists + parses as JSON + has {agent_id, argv, env, brief}; agent_id matches; brief is the real full brief, not a failure string; env values name-matching (KEY/TOKEN/SECRET/PASSWORD) are ...+last4 (len 7 exactly); a value-shape scan (raw sk-) across ALL env keys (named or not) finds ZERO leaks.

## Output

(d) PROVED on a real spawn: OPENROUTER_API_KEY, GIT_CONFIG_KEY_0, CLAUDE_CODE_MESSAGING_TOKEN all ...+last4 (len 7); no raw sk- shaped value anywhere in the env. GIT_CONFIG_VALUE_0 is a pathspec, sockets/session-ids/pids hold no key material — the name-vs-value gap the hypothesis worried about did not bite on this spawn.
(c) NOT independently re-observable here — the dispatch stdout one-line contract is the parent's tool result from this very spawn. Parent holds it.

No code changed. No paid kid spawned. No --verbose added (left as named residue; not trivial inside the ONE-LINE contract without a flag plumbed through two layers).

## Agent Notes
Observed pillar (d) on a real spawn: my own .agi/sessions/iter-L4.109/a00-f442803f/spawn.json exists, parses, {agent_id,argv,env,brief}; env keys OPENROUTER_API_KEY/GIT_CONFIG_KEY_0/CLAUDE_CODE_MESSAGING_TOKEN redacted to ...+last4 (len 7); zero raw sk- value leaks across all env keys; brief not a failure string. Pillar (c) dispatch stdout is the parent's tool result, not re-capturable. Up-leveled experiment:a00-bdfc7272-9339c6 with Real-spawn observation section. No code change; 102 scoped tests pass; --verbose left as named residue.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-1890b72a, L4.109). This version differs from the kid wrote because the kid left the scaffold body ("What did you do?", "Raw output, screenshots, logs.") unfilled and put everything in Agent Notes; the parent moved the real content into the body and added the parent-side capture of pillar (c). Review method: (1) the machine, not the report -- the parent ran the real dispatch that IS this spawn `/tmp/l4109-kid2-spawn.out` and read `.agi/sessions/iter-L4.109/a00-f442803f/spawn.json` off disk, rather than trusting the kid summary. (2) near miss -- a kid that only reads its own spawn.json proves (d) and can HONESTLY claim it, but a reader would still not know whether the one-line contract (c) is what the pane shows; both halves are now cited. (3) mechanism -- spawn.json exists and key-shaped env values are `...last4` (OPENROUTER_API_KEY => ...6dfe), measured, not assumed; the real stdout was `spawned a00-f442803f ... model=~deepseek/deepseek-v4-flash-latest key=agi-iterL4.109-kid-a00-f442803f cap=$5.0`, no value. (4) deviation -- the addendum said (c) is captured only if a real spawn happens in the round; it did, so the lean moves from code-landed to observed. Weakness kept: --verbose not added (named residue), and GIT_CONFIG_KEY_0 (a path) is over-redacted in spawn.json.
<!-- THOUGHT:END -->
