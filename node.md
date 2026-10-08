---
id: experiment:a00-de0024a3-e6eb43
mint_id: ea6495f68366409db3b877cdcd06978b
type: experiment
parents:
  - hypothesis:l3w4-context-load-minimal
next_edges: []
confidence: 0.6
edited_by: a00-de0024a3
evidence_runs:
  - experiment:a00-de0024a3-e6eb43
loop: hypothesis:l3w4-context-load-minimal@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 6b9d423f661aaa37
season: 2
title: "\"Rotation spawn prompt measured: 2,144 tok prime; rotate.py reuses brief.py head (no dup)\""
verdict: inconclusive_lean_proved:55
---
<!-- BODY:BEGIN -->
# experiment:a00-de0024a3-e6eb43

## Experiment

**Slice touched: the rotation spawn prompt. Move ONE's head trim, measured through the actual rotation path.** The owner's "THIRD TARGET THE OWNER NAMED" was the successor's first-user-message (≈16.4 KB per rotate.py's own construction, never counted). SD.07's separate round was meant to measure it and drifted off; the measurement never landed. This slice does it: measure rotate.py's assembled successor spawn prompt per rotation path, and test the separate-parent's predicted finding (`rotate.py constructs its OWN copy of the constitution head rather than reusing brief.py's assembler`).

NO engine code changed — the prediction had to be answered by reading the assembly path, and the numbers had to be counted by running it. Measurement script saved durably at `.agi/tmp/measure_rotate_prompt.py` (tmp/ is not durable across kids), method = tiktoken o200k_base on `/usr/bin/python3.12` (same encoder as the static-prefix baseline so numbers are comparable).

**Assembly trace (read from rotate.py):**
- `_successor_command` (prime `rotate-self` / `loop` / `spawn` default): reads `briefs/prime-director-successor.md`, replaces `{name}`, calls `brief.successor_prompt(tier='prime_director', body)` → head prepended through brief.py + body. NO own copy of the head in rotate.py — grep for any head-construction constant in rotate.py returns only the three `brief.*` call sites.
- `_assembled_successor_command` (non-prime seat, `spawn_window`, no `--prompt-file`): joins `brief.assemble(tier, agent_id, iter_n=0)` parts, and deliberately does NOT call `successor_prompt` again because assemble() already prepends the head (the double-insert is explicitly guarded against, `hypothesis:l3w4-liaison-seat`).

**Verdict on the prediction: DISPROVED.** The separate-parent hypothesised the fix would be "stop rotate.py re-injecting what the harness already provides" — there is no such re-injection. rotate.py reuses brief.py's assembler in both paths; the head is already prayers-only (move ONE landed, sibling a00-9a175ddd) and comes in exactly once. A fix that "removes rotate.py's own head copy" would have been a fix for a defect that does not exist.

**Measured assembled successor prompts (tokens, o200k):**

| rotation path | head tok | body tok | total tok | total bytes |
|---|---|---|---|---|
| prime rotate-self/spawn (prime_director) | 611 | 1,533 | **2,144** | 7,978 |
| non-prime seat tier=director (assemble) | — | — | **1,343** | 4,708 |
| non-prime seat tier=liaison (assemble) | — | — | **903** | 3,075 |
| non-prime seat tier=parent (assemble) | — | — | **1,605** | 5,762 |
| prayers-only constitution head (prime), standalone | — | — | **611** | 1,846 |

**The head is 28.5% of the prime's rotation prompt, not most of it.** 611 / 2,144 tokens. The successor brief body (1,533 tokens) is the larger half — and it is the genuinely new context a successor cannot get anywhere else (roles, first-action steps, standing rules, spend limits). Against the sibling's pre-trim prime head (3,012 tokens, same source method), the rotation prompt's head half is carried at −80% — so the prime rotation spawn prompt, pre-trim inferred ≈4,545 tokens (3,012 old head + 1,533 body) vs 2,144 now, has roughly **halved** purely from move ONE's head trim. The ≈16.4 KB that rotate.py's comment references is the whole tmux-launch ARGV (claude flags + chained.json debug path + prompt), not the prompt alone (7,978 bytes) — that argv-length concern is already retired by `_launch_window`'s script-file fallback for anything above `_TMUX_ARG_SAFE` (8,192), and is orthogonal to the context-load cost this node measures.

## Evidence

`/usr/bin/python3.12 .agi/tmp/measure_rotate_prompt.py` output (edited):
```
### PRIME  rotate-self/spawn (prime_director successor brief)
  total bytes : 7978
  total tokens: 2144
### non-prime seat  tier=director (assemble path)    total tokens: 1343
### non-prime seat  tier=liaison (assemble path)    total tokens: 903
### non-prime seat  tier=parent (assemble path)     total tokens: 1605
### prayers-only constitution head (prime), standalone  tokens: 611  bytes: 1846
```
Head/body split check: `prompt == head+'\n\n'+body` → `True`; head 611 tok / 1,846 B, body 1,533 tok / 6,130 B, total 2,144 / 7,978. Pre-trim inferred (old prime head 3,012 + body 1,533) = 4,545 tokens.

grep of rotate.py for any head constructor / `DEF CON`-style constant: only `brief.successor_prompt` (L720) and the two assemble-path comments (L738, L1090) — no own copy of the constitution head text anywhere in rotate.py.

No engine source changed; `brief.py` and `rotate.py` assembly paths exercised directly (import + call succeeded for prime/director/liaison/parent). The repo's `.env` untracked file (reported by sibling a00-9a175ddd, pre-existing) is untouched.

## Agent Notes
Measured rotate.py's successor spawn prompt (o200k): prime rotate-self/spawn 2,144 tok / 7,978 B (head 611 + successor brief 1,533); non-prime seats director 1,343 / liaison 903 / parent 1,605. Disproved the predicted finding: rotate.py reuses brief.py's assembler in both paths, no own copy of the constitution head, no double-injection to remove (guard already in place). Move ONE'...
