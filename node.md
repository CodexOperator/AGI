---
id: experiment:a00-0f527d4c-75f4fe
mint_id: 98a4c90aa0f54a9faaca28afc4dcd31b
type: experiment
parents:
  - hypothesis:l3w4-context-load-minimal
next_edges: []
confidence: 0.6
edited_by: a00-0f527d4c
evidence_runs:
  - experiment:a00-0f527d4c-75f4fe
loop: hypothesis:l3w4-context-load-minimal@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2eeaf21da30d5353
season: 2
title: "\"Before baseline: assembled prompt per role ~24-25k tok, not ~68k\""
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-0f527d4c-75f4fe

## Experiment

**Measure the real "before" baseline of the always-injected prompt per role** — the first proof the hypothesis demands ("measure the assembled prompt per role before and after with an actual token count and report both numbers plus the percentage, per role, not in aggregate"). The "after" trim is the parent's multi-kid build; this run establishes the accurate denominator the 70-90% cut will be measured against.

Assembled the prompt exactly as `pi_adapter.build_command` does: `context_file` (`.agi/context/INJECTION.md`) + `brief.assemble()` segments (constitution head first, then role brief) + `skill_prompt` (`skills/agi/SKILL.md`) + `closing_line`. Counted tokens with tiktoken `o200k_base`. Script: `/tmp/measure_prompt.py`. Deterministic (reads the same files), reproducible across runs.

**Per-role total assembled prompt (tokens):**

| tier | head | brief | total |
|---|---|---|---|
| kid | 579 | 1125 | 22734 |
| parent | 1972 | 3039 | 24657 |
| advisor | 1972 | 2900 | 24523 |
| director | 2338 | 3071 | 24690 |
| prime_director | 3012 | 3830 | 25450 |
| liaison | 2338 | 2633 | 24258 |

**Static prefix** (INJECTION.md 8406 + SKILL.md 13180) = **21,586 tokens** — 85-89% of every role's total.

## Evidence

**Key finding — the hypothesis's ~68k estimate is ~2.7x too high.** It counted HANDOFF.md (~47k) and CLAUDE.md (~6k) as "always-injected context", but the adapter does NOT inject those: they are files a role reads on demand. The always-injected prompt is what `build_command` assembles, and it measures **~24-25k per role**, dominated by the 21,586-token static prefix (INJECTION.md + SKILL.md), not by HANDOFF.md.

**Where the leverage actually is:** SKILL.md (13,180 tok) + INJECTION.md (8,406 tok) = 85-89% of every role's total. The role briefs (1.1-3.8k) and the constitution head (0.6-3.0k) are small by comparison. A prayers-only head (move ONE) saves ~2,400 tok/turn for a prime (3,012 → ~600), but the head is a small fraction; the trim must land on the static prefix.

**What the 70% bar really means:** 70% of a prime's 25,450 = under 7,635 tok. The hypothesis's "under 10,000" target is only a 61% cut. Meeting the owner's stated 70% therefore requires cutting the 21,586-token static prefix by ~65% AND trimming the role briefs — the head trim alone cannot reach it.

Measured components (tokens): INJECTION.md 8406; SKILL.md 13180; prayers section 501; words_jesus 1314; tao 103; sayings 385; current prime_director head 3012.

Raw output (reproducible):
```
context_file (INJECTION.md): 8406 tok, 25702 B
skill_prompt (SKILL.md):     13180 tok, 52793 B
tier               head   brief   total    chars
kid                 579    1125   22734    81982
parent             1972    3039   24657    88715
advisor            1972    2900   24523    88273
director           2338    3071   24690    88860
prime_director     3012    3830   25450    91992
liaison            2338    2633   24258    87259
static prefix = ctx + skill =  21586
```

## Agent Notes
Measured real before-baseline of always-injected prompt per role via pi_adapter assembly + tiktoken o200k: kid 22734, parent 24657, advisor 24523, director 24690, prime_director 25450, liaison 24258. Static prefix (INJECTION.md 8406 + SKILL.md 13180) = 21586 tok = 85-89% of every role. Corrects the hypothesis's ~68k estimate (~2.7x high): HANDOFF.md/CLAUDE.md are read-on-demand, not injected. 70% bar = <7635 tok for a prime, so trim must hit the static prefix, not just the head.
