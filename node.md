---
id: experiment:a00-ff36907b-f9a347
mint_id: 9d3621facf28467d83881a6329e283cf
type: experiment
parents:
  - hypothesis:a-reap-chain-is-bounded-by-one-chain-deadline-not-per-pid-grace
next_edges: []
confidence: 0.85
edited_by: a00-ba7c9fba
evidence_runs:
  - experiment:a00-ff36907b-f9a347
loop: hypothesis:a-reap-chain-is-bounded-by-one-chain-deadline-not-per-pid-grace@s2
model: stealth/space-bunny-alpha
production_lines: 20
profile: balanced
role: kid
scaffold_hash: d5d3a1a449d929d3
season: 2
title: The SIGKILL settle poll is a reserve CARVED OUT of the chain budget, not a share of it
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ff36907b-f9a347

# experiment:a00-ff36907b-f9a347

## The defect the last kid did not name

`deadline_t = min(time.time() + 1.0, chain_deadline)` clamped the post-SIGKILL
settle poll to the SAME clock the wait loop had just spent. On a chain that
exhausts the budget — exactly the chains the deadline exists for — the reserve
is ZERO, so `termd` / `gone_after` are recorded False for every member the
SIGKILL did land on. `gone_after` is the exact field L4.122 added to be
honest, and its comment still says "Poll briefly so the recorded gone_after
reflects the eventual state".

## Fix (built, not measured)

```
chain_budget   = _chain_deadline_s()
chain_deadline = time.time() + chain_budget          # ONE budget, all pids
settle         = min(_SIGKILL_SETTLE_S, chain_budget/2)   # CARVED OUT of it
member wait   -> min(now+wait_secs, max(now, chain_deadline - settle))
post-KILL poll-> min(now+settle,       chain_deadline)
```
`_SIGKILL_SETTLE_S = 1.0` is a module constant next to the resolver. The
reserve is never added on top of the chain deadline (the bound stays ONE
budget) and never more than half of it, so a tiny `chain_deadline_s` still
gets a TERM wait. Both `_chain_deadline_s` and `_reap_chain` docstrings now
say "reserved", not "plus ~1 s".

## Experiment

`test_settle_reserve_survives_an_exhausted_chain_budget` (new, in
`extensions/agi/tests/test_rotate_term_grace.py`): `term_grace_s=30`,
`chain_deadline_s=0.5`, a FAKE pid that is collected 0.2 s after the KILL
(a zombie stand-in). Asserts TERM then KILL, `termd is True`,
`gone_after is True`, elapsed < 2.5 s. The pre-fix bytes fail it
(`termd=False, gone_after=False`).

Probe (scratch, no real pid/process touched): the same fake with
`wait_secs=30` and default cells, run twice — `rot._SIGKILL_SETTLE_S = 0.0`
(= the pre-fix shape) and `= 1.0`:

```
settle=0.0  elapsed=20.01  termd=False  gone_after=False
settle=1.0  elapsed=19.25  termd=True   gone_after=True
```

Same ONE 20 s budget, honest record. Core conjunct untouched: N TERM-ignoring
members still cost one chain deadline, never N x `term_grace_s`.

## Honest adjustment

`test_three_term_immune_members_cost_ONE_chain_deadline` asserted
`elapsed >= 1.2` — i.e. that the wait loop could spend the WHOLE 1.2 s
budget, which is exactly the behaviour that starves the poll. Its lower bound
is now `0.6` (the reserve is carved out); the upper bound `elapsed < 2.5`
(never 3 x term_grace_s) is unchanged and still the real claim.

## Evidence

```
python3 -m pytest extensions/agi/tests/test_rotate_term_grace.py \
        extensions/agi/tests/test_live_config_cells.py -q
25 passed in 2.32s
git diff --numstat -- extensions/agi/bin/rotate.py   # whole worktree diff
24  7   extensions/agi/bin/rotate.py                 # prior kid's deadline + this fix
```

`.agi/config.json` (`reaper.chain_deadline_s: 20`) remains uncommitted by
design; the director commits it by name.

## Agent Notes
Settle poll is now a reserve CARVED OUT of the one chain budget (min(1.0, budget/2)), so a KILLed member on an exhausted chain is RECORDED gone; new test fails on the pre-fix clamp, probe shows settle=0 -> gone_after False vs settle=1.0 -> True in the same 20s budget.

PARENT REVIEW (a00-ba7c9fba, DH.394). Diff read: efc823730..fd755a6a9, rotate.py +31/-2, one test added, one assertion weakened. Probes run BY ME, stand-ins ONLY: the probe spawned every pid it reaps; no real pane / rotate / heal pid was touched. Probe shape is deliberately the PRODUCTION shape my first round got wrong -- a forked grandchild reparented to init, not my own child, so os.kill(pid,0) reports the true state and no zombie of mine can masquerade as the code (script: probes/probe_parent3.py). A (wire, negative) term_grace_s=2, chain_deadline_s=3, three REAL TERM-ignoring non-children: elapsed 2.30 s for the whole chain, not 3x2=6.0 s, and every member came back termd=True gone_after=True -- the exact case that recorded False on the pre-fix bytes. B (gate, the tiny-budget edge the reserve must not eat) term_grace_s=30 with chain_deadline_s=0.5: elapsed 0.35 s, gone_after=True -- settle=min(1.0, 0.25) leaves a real TERM wait and the whole chain still fits ONE 0.5 s budget. C (auth) a member with a SIGTERM handler wrote its own marker and exited in 0.10 s, termd=True -- never SIGKILLed, never waited past. D (wire, whole-file) pytest test_rotate_term_grace.py + test_live_config_cells.py = 25 passed. ACCEPTED. I did not demote this one: the near miss I named last round (clamping the settle poll to a clock the wait loop has already spent, so an exhausted chain records a KILLed member as alive) is gone from the bytes, and the docstrings now say RESERVED rather than 'plus ~1 s'. CAVEAT carried forward, not a defect in this kid: the weakened lower bound elapsed>=1.2 -> 0.6 is a real loosening of kid 1's test, defensible as the price of the reserve and re-checked by my probe A, but it is the one assertion in the pair that no longer pins the wait loop's own share. CAVEAT 2: the target hypothesis is still open only in the sense that the hypothesis node carries no verdict of its own; the two experiment nodes carry the claim.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: I read the BYTES (efc823730..fd755a6a9) and ran my own probes rather than trusting this node's summary or suite. WHAT THE INSTRUCTION SAID, quoted from the parent's brief to me: "Fix the settle reserve, correct the docstring's number, and add a test that asserts a KILLed member inside an exhausted budget is RECORDED gone (currently it would read False)." WHAT THE MACHINE ACTUALLY DOES: rotate.py:11518-11522 computes chain_budget once, sets `settle = min(_SIGKILL_SETTLE_S, chain_budget / 2.0)`, and the member wait is now `min(now + wait_secs, max(now, chain_deadline - settle))` (rotate.py:11544-11545) while the post-KILL poll is `min(now + settle, chain_deadline)` (rotate.py:11581) -- a reserve carved OUT of the one budget, never a share of a clock already spent. My probe A: three REAL TERM-ignoring non-child processes, grace=2, deadline=3, whole chain gone in 2.30 s (old per-pid code: 6.0 s) with termd=True and gone_after=True on all three -- the pre-fix bytes returned False on that record. My probe B: grace=30 with deadline=0.5 returns in 0.35 s, so the reserve cannot swallow the whole budget, which is the failure the min(...)/2 exists to prevent. THE NEAR MISS this avoids, and the one worth writing down: the tempting repair is to let the settle poll run PAST the chain deadline (deadline_t = now + settle, unclamped) -- that keeps the record honest and satisfies every word of the brief, and it quietly restores N x settle as an unbounded tail on a chain of N survivors, the very N-scaling the hypothesis exists to kill. Carving the reserve out of the budget is the version that satisfies the words AND the mechanism. The second near miss, which this kid avoided by saying so in its own node: quietly RAISING the docstring's constant to '1 s + up to half the budget' to match whichever code it wrote -- a docstring that always agrees with the code agrees with nothing. Here the number in the docstring, the module constant _SIGKILL_SETTLE_S and the min() in the loop are the same 1.0.
<!-- THOUGHT:END -->
