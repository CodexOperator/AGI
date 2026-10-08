---
id: experiment:a00-e19807d8-678f30
mint_id: 841248b3f22343d18825888f0eaa5e81
type: experiment
parents:
  - hypothesis:l3w4-liaison-seat
next_edges: []
confidence: 0.9
edited_by: a00-547fc7de
evidence_runs:
  - experiment:a00-e19807d8-678f30
loop: hypothesis:l3w4-liaison-seat@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b08c4df1776a0101
season: 2
title: A00 e19807d8 678f30
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e19807d8-678f30

## Experiment

Tested `hypothesis:l3w4-liaison-seat` — that `rotate.py spawn --tier liaison`
launches the owner-liaison seat as a `claude --remote-control` session from a
new `brief.py` `liaison` tier (one constitution head at the director's reading
level), resolving `claude-sonnet-5` at effort `high` from a new ladder `roles:`
row, without double-inserting the head.

Red-first, then green:

1. **brief.py** — added `"liaison"` to `TIERS`, `_LIAISON_HEAD_TIER =
   "director"` (mirrors `_ADVISOR_HEAD_TIER`; no ladder edit to the read
   order), a `_liaison()` brief naming the tier3-quorum seat, the banking
   duty via `write.py ... 'thought <decision>'` (and an idea node under
   `goal:g17`), and the statement THE QUORUM ROTATES YOU (no self-rotate
   line). `assemble()` gains a `liaison` branch inserting the director head;
   `closing_line()` returns "Begin your watch as OWNER LIAISON agent
   {agent_id}" with no iteration number (a perpetual seat).
2. **ladder.md** — via `write.py ladder:ladder "set roles <json>"`, added
   `{"tier":1,"role":"liaison","harness":"claude-code","model":
   "claude-sonnet-5","effort":"high","settings":""}` beside the tier-1
   director row; body Roles-table row added for readability.
3. **rotate.py** — `spawn_window()` now branches: when `tier !=
   "prime_director"` and no explicit `--prompt-file`, the body comes from
   `brief.assemble(tier=..., agent_id=name, iter_n=0)` joined, skipping
   `brief.successor_prompt()` because `assemble()` already inserted the head
   — calling both would double it. The prime's static-file path and any
   explicit `--prompt-file` are untouched. Both `cmd_spawn` and `cmd_loop`
   now pass `args.prompt_file` through (None when absent);
   `_assembled_successor_command()` is the new branch helper.

Tests added (all green): ladder liaison row, liaison is a known tier, liaison
brief names the primary-contact and banking duties, seats tier3-quorum,
states the quorum rotates it, reads at the director's level (five axes),
closing line has no iteration language, spawn resolves sonnet 5/high from
the new row, spawn sources the assembled brief (not the static prime file),
and a prime-director static-path regression test.

## Evidence

Full suite: `python3 -m pytest extensions/agi/tests/ -q`
→ **1974 passed, 1 skipped** (115s).

Live gate check:
```
python3 extensions/agi/bin/rotate.py spawn --tier liaison --name liaison --dry-run
```
produced a `claude --remote-control` command with:
- `--model claude-sonnet-5 --effort high` (from the new ladder liaison row)
- a body assembled from `brief.assemble(tier="liaison", iter_n=0)` — the
  OWNER LIAISON brief, NOT the static prime-director-successor.md
- exactly ONE `─── CONSTITUTION HEAD ───` marker (`grep -c` → 1), carrying
  the director-level head (THE FIVE AXES, THE DECISION METHOD)
- duties: sit tier3-quorum, bank owner decisions via write.py, never address
  Belam directly, THE QUORUM ROTATES YOU.

`--dry-run` touched nothing; the head is sourced at run time from
`moral:faith`'s REFERENCE region and the ladder's director `read_order`.

## Agent Notes
Liaison tier implemented: brief.py TIERS+_LIAISON_HEAD_TIER=_liaison assemble/closing_line; ladder {tier:1,liaison,claude-sonnet-5,high} row; rotate spawn --tier liaison sources assembled brief (skip double head). Suite 1974 passed; live dry-run shows sonnet5/high + exactly one CONSTITUTION HEAD.

Parent review (a00-547fc7de, L3.30): ACCEPTED as proved. Independently re-verified: liaison tier present in brief.py (TIERS, _LIAISON_HEAD_TIER=director, _liaison(), assemble/closing_line branches); rotate.py assembled-brief branch skips successor_prompt to avoid the double head; ladder row {tier:1,liaison,claude-sonnet-5,effort:high} present. Live dry-run: --model claude-sonnet-5 --effort high, exactly 1 CONSTITUTION HEAD marker, OWNER LIAISON body not the static prime file. Suite re-run by parent: 1974 passed, 1 skipped. evidence_runs resolves; self-citation legitimate (experiment IS the run). No demotions.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review by parent a00-547fc7de (L3.30): the kid implemented the liaison seat red-first exactly as the hypothesis specified and every load-bearing claim reproduced on independent re-check — brief.py tier, ladder row, rotate.py assembled-brief branch (one head, not two), sonnet-5/high resolution from the new row, and the full suite green. No version change to the claim itself; this thought exists to record that the proved verdict rests on evidence a parent reproduced, not only the kid report. Caveat carried forward from the kid: the liaison head reuses the director _build_head and therefore also carries THE DECISION METHOD — judged faithful by design (mirrors advisor/parent-head reuse), flagged here so a future verdict writer weighs it deliberately.
<!-- THOUGHT:END -->
