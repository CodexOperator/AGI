---
id: experiment:a00-0e2c576a-e89643
mint_id: 30434f2926ae43f098cca91126e61ba6
type: experiment
parents:
  - hypothesis:l3w4-context-load-minimal
next_edges: []
confidence: 0.7
edited_by: a00-8e296aa5
evidence_runs:
  - experiment:a00-0e2c576a-e89643
loop: hypothesis:l3w4-context-load-minimal@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9128226ceb24d1c3
season: 2
title: "\"Rotation spawn prompt measured 2140 tok; no head duplication in rotate.py\""
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-0e2c576a-e89643

## Experiment

SD.08 rotate.py-focused slice: measure and trim rotate.py's successor-spawn-prompt assembly, nothing else. Did NOT touch skills/agi/SKILL.md or .agi/context/INJECTION.md (other round's territory), and did not do moves THREE/FOUR/FIVE.

**Method** (same as sibling SKILL.md/INJECTION.md round so numbers compare): tiktoken `o200k_base`. Script saved durably at `.agi/tmp/measure_spawn_prompt.py` (the /tmp copy does not survive across kids), runs under the venv at /home/ubuntu/work/agi/tmp/venv (base python lacks tiktoken; venv lacked pyyaml, installed for brief imports). Measurement calls `brief.successor_prompt` / `brief._build_head` the same way rotate.py does (project_root=None, so it walks up from brief.py to the worktree `.agi`).

**Measured, the rotation spawn prompt (head + successor brief body):**

| path | tokens | bytes | breakdown |
|---|---|---|---|
| constitution head (`brief._build_head`, prime_director) | 611 | 2275 | prayers-only post-move-ONE |
| body (`briefs/prime-director-successor.md`) | 1529 | 6159 | the static brief file |
| **rotate-self successor prompt (head+body)** | **2140** | **8436** | head = 28.6% of tokens |
| loop rotation (prompt + continuation) | 2175 | 8596 | continuation = 35 tok |
| non-prime spawn via assembled brief (tier=parent) | 1615 | 6263 | `brief.assemble` join |

**THE FINDING — finding 4 is NEGATED.** The brief predicted "rotate.py constructs its OWN copy of the constitution head text, and that duplication is probably most of the 16.4 KB." Measured false: `grep` of rotate.py for any literal prayer/head text returns **0 hits**; every successor path routes through `brief.successor_prompt(tier, body)` → `brief._build_head()`, the same single source the live head comes from (comments at L709, L720, L736-738, L1090 all confirm the no-double-insert guard, hypothesis:l3w4-liaison-seat). There is no second copy to remove.

**Second finding — the 16.4 KB estimate was stale.** That number measured the prime's rotation argv BEFORE move ONE landed. Move ONE (prayers-only head, already merged this hypothesis) cut the head 3012→611 tokens (−80%), which is exactly the byte that used to ride in the spawn prompt. The current successor prompt is **2140 tokens / 8.4 KB, ~2.9x smaller than the 16.4 KB estimate** — and it stays post-`_TMUX_ARG_SAFE` (8192), so the script-file launch path remains the rule, documented in the updated comment at `_launch_window`.

**Trim NOT done, and why (honest):** the remaining bulk is the static successor brief file (1529 tokens, 71% of the prompt), largely standing rules that duplicate the always-injected SKILL/HANDOFF context. Cutting them is where real savings are, but every candidate on the must-not-lose list (kill procedure, key-floor rule, exact next command, attribution, owner decisions as pointers) is in that file. A line-level trim of standing rules risks losing operational content (comprehension-wins metric), and the proper lever is the per-role SKILL.md/hierarchy slicing round — not this assembly slice. Left intact rather than ship a wrong-scoped cut.

**Change made (rotate.py, comment-only, no behavior):** updated the stale `~16KB` launch-size comment at `_launch_window` to the measured post-trim figure (2140 tok / 8436 B), so no later reader trusts the pre-trim number.

## Evidence

```
head prime_director:            611 tok / 2275 B
prime-director-successor.md:   1529 tok / 6159 B
successor_prompt (rotate-self):2140 tok / 8436 B   (head 28.6%)
loop (+continuation):          2175 tok / 8596 B   (cont. 35 tok)
non-prime assembled (parent):  1615 tok / 6263 B
```

grep rotate.py for prayer/head literals: **0 hits** (no self-built head copy).
Test suite: `python3 -m pytest extensions/agi/tests/ -q` → **2203 passed, 1 skipped** (comment-only change; suite green).

## Agent Notes
Rotate.py successor-spawn-prompt measured (tiktoken o200k): prime rotate-self 2140 tok/8436B (head 611 + brief body 1529), loop 2175, non-prime assembled parent 1615. Finding-4 NEGATED: rotate.py has zero literal head text, routes all paths through brief.successor_prompt/_build_head, no duplicate copy to remove. 16.4KB estimate stale post move-ONE; prompt already 2.9x smaller. Remaining 71% is the static successor brief (standing rules) - real trim is the per-role SKILL/hierarchy slicing round, not assembly. Comment-only rotate.py edit.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-8e296aa5), accepted as-is. Scope check: this is the rotate.py slice per the node standing note (kid spawned before my per-role brief note landed in the target — race, my defect, not the kids). Verified: parents resolve to the target hypothesis; verdict format valid; evidence_runs names itself, legitimate for an experiment node; measurement method matches the sibling round (tiktoken o200k_base, script saved durably under .agi/tmp/); rotate.py change is comment-only and the suite is green (2203 passed). The negative result (no head duplication in rotate.py; 16.4KB estimate stale post move-ONE) is a real finding and kills a wrong-costed work item. Verdict inconclusive_lean_disproved:70 is honest — it disproves the duplication claim, not the hypothesis.
<!-- THOUGHT:END -->
