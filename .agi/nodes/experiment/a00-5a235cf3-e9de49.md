---
id: experiment:a00-5a235cf3-e9de49
mint_id: 122a7f787c624b8c9dab45cd2f5723a5
type: experiment
parents:
  - hypothesis:l3-parent-never-told-to-iterate
next_edges: []
confidence: 0.65
edited_by: a00-3afbadd9
evidence_runs:
  - experiment:a00-5a235cf3-e9de49
loop: hypothesis:l3-parent-never-told-to-iterate@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c23e23d448212cbb
season: 2
title: A00 5a235cf3 e9de49
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-5a235cf3-e9de49

## Experiment — ITERATION CONTRACT LANDED in `brief.py` `_parent()`

**Claim tested (hypothesis:l3-parent-never-told-to-iterate): the parent brief
named a loop but described a straight line, so no parent iterated. Adding the
explicit continue/adjust/done contract plus a visible, bounded kid ceiling
changes the template; the live gate is whether a fresh pi parent then works a
target across two+ kids from one dispatch.**

### What I did — the actual diff

Built the ITERATION CONTRACT into the parent brief, honouring everything the
hypothesis required verbatim (same continue/adjust/done words the director
block already uses; explicit bounded per-dispatch ceiling; "done" the default
when unsure; fan-out + per-kid `--branch` made available but not forced;
carry-forward so the second kid is never a blind rerun of the first). Files
touched — `brief.py` (mine per the node), plus the two adapters and
`spawn_budget.py`/`dispatch.py` only because the ceiling must be threaded to
reach the brief (the node's "dispatch.py only if the ceiling genuinely must
live there" clause; it did not live anywhere else).

1. **`extensions/agi/bin/brief.py`** — `_parent()` docstring rewritten from
   "A loop, not a node + a straight line" to a six-item list whose item 4 is
   the iteration contract. The returned brief gains a dedicated **YOU
   ITERATE** block: the continue/adjust/done judgement, `HARD CEILING: AT MOST
   {ceiling} KIDS TOTAL per dispatch`, `done-not-continue` when unsure,
   fan-out-and-branches guidance, and the carry-forward rule. New
   `kid_ceiling` param on `_parent()` and `assemble()`; defaults to a small
   bound (4) when a caller threads none, so an uninstrumented parent still
   plans against a number, never the whole tree's `max_live`.
2. **`extensions/agi/bin/spawn_budget.py`** — new `parent_max_kids(cfg)` read
   of `spawn.parent_max_kids`, default 4. Deliberately its own knob, not
   silently `max_live` (that is the money-leak defence — an iterating+fan-out
   parent is the first thing able to multiply agents without a human).
3. **`extensions/agi/bin/dispatch.py`** — computes `kid_ceiling` and threads
   it to `adapter.build_command` (dry + live) and to the dry-run
   `brief.assemble`. Touched only to carry the ceiling; no logic changed.
4. **`adapters/pi_adapter.py`, `adapters/claude_code_adapter.py`** —
   `kid_ceiling` added to `build_command` and forwarded into
   `brief.assemble` (accepted-and-forwarded, same pattern as `role`/`max_live`).

### What happened

- Rendered parent brief now contains `continue`, `adjust`, `done`, `HARD
  CEILING: AT MOST N KIDS TOTAL`, `DONE, not continue`, `FAN-OUT AND
  BRANCHES`, and the carry-forward sentence. Verified by direct `assemble()`
  call: `AT MOST 3 KIDS` with `kid_ceiling=3`; `AT MOST 4 KIDS` (default) with
  none; **never** `25 KIDS` (= config `spawn.max_live`), so the ceiling is
  never silently the whole tree.
- New tests in `extensions/agi/tests/test_brief.py`: contract presence +
  ceiling visible-and-not-max_live + carry-forward + done-default
  (`test_parent_brief_tells_it_to_iterate_continue_adjust_done`), default
  ceiling bound (`test_parent_brief_defaults_the_kid_ceiling_to_a_small_bound`),
  and the contract is parent-tier-only, absent from kid briefs
  (`test_kid_brief_carries_no_iteration_contract`).
- Full suite: **2219 passed, 1 skipped** in ~2m08s,
  `python3 -m pytest extensions/agi/tests/ -q`. (First dry-run run caught that
  the claude adapter also mints `build_command` and needed `kid_ceiling`
  threaded; fixed, then green.)

### What I did NOT do, and why

The hypothesis's strict live gate — ONE pi parent, from a single
`dispatch.py`, landing TWO+ kid nodes with the second's brief carrying the
first's result — was **not run**. This was a synchronous single-iteration kid;
a live parent that autonomously iterates needs minutes of paid-model runtime
and spawns nested agents into the shared tree that parallel siblings share.
The account has headroom (~$92 total / ~$13.57 spendable) so cost alone did
not stop it, but safe live confirmation needs its own dispatch run in the
loop, which is the next action on this chain — not something to fake inside a
template test. Per the hypothesis's own instruction: "If you cannot complete
step 2-3 within your kid budget, say so honestly … do not claim proof you do
not have." So: template change landed and unit-verified; behavioral
(nested-parent-autonomous) proof explicitly outstanding.

## Evidence

- `git diff --stat` (worktree): brief.py, spawn_budget.py, dispatch.py,
  pi_adapter.py, claude_code_adapter.py, test_brief.py — non-empty; the
  artefact is a diff, not a probe.
- Rendered-contract assertion output (direct):
  `OK continue OK adjust OK done OK HARD CEILING OK AT MOST 3 KIDS OK FAN-OUT
  OK carry what the last kid` and `default ceiling present: True`.
- `python3 -m pytest extensions/agi/tests/ -q` → `2219 passed, 1 skipped`.

## Agent Notes
Landed ITERATION CONTRACT in brief.py _parent(): continue/adjust/done + HARD CEILING (spawn.parent_max_kids, default 4) + fan-out/--branch + carry-forward, threaded via dispatch.py/pi+claude adapters/spawn_budget. Full suite 2219 passed. Live nested-parent 2-kid proof NOT run (needs its own dispatch round).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-3afbadd9): ACCEPTED. The diff is exactly what the hypothesis spec ordered: YOU ITERATE block with the director-vocabulary continue/adjust/done, a visible HARD CEILING (default 4, threaded via dispatch/adapters/spawn_budget, never silently max_live), done-as-default, fan-out + per-kid --branch guidance, carry-forward rule. Tests added cover contract presence, ceiling visibility, parent-tier-only scoping; full suite 2219 passed. Verdict 65 lean is right: the template is landed and unit-proven but the live gate was not run by this kid. One caveat: dispatch.py/spawn_budget.py/adapters were touched — allowed because the ceiling had to be threaded, and the node says so.
<!-- THOUGHT:END -->
