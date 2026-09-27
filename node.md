---
id: hypothesis:reap-chain-members-get-their-full-term-grace-again
mint_id: 203c4e9a4d374c93a9b618ae4d20bcf1
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: belam
scaffold_hash: 0c80f78e61f472c0
season: 2
testable_claim: "a TERM-honouring member third in a 3-member reap chain is never SIGKILLed (fixed rotate.py:11547-11548 shared chain clock: 15/3/0 s at the live cells); a SIGKILLed chain records reaped True; the new fixture test is RED on 6c403aeb4b, GREEN on the fix"
title: "Every reap-chain member gets its full TERM grace again; a SIGKILLed chain records reaped: True (assigned: director-engine)"
town: core
---
# hypothesis:reap-chain-members-get-their-full-term-grace-again

# hypothesis: every reap-chain member gets its full TERM grace again (assigned: director-engine)

## Why this exists
**Parent `goal:g1`** (PASS residues; g15 -> g20 -> g1). PASS 10 chunk 14 DEMOTED round `a-reap-chain-is-bounded-by-one-chain-deadline-not-per-pid-waits` (run mur-p10chunk14of15, verify stage) on a live behaviour regression the Prime put FIRST in DE's queue (owner 03:4xZ 09-27: the priority must actually reach DE).

## Measured (at TIP 6c403aeb4b)
- `rotate.py:11547-11548`: `deadline = min(time.time() + wait_secs, max(time.time(), chain_deadline - settle))` -- one absolute chain clock shared by every member.
- At the live cells (term_grace_s 15 / chain_deadline_s 20) a 3-member chain gives 15 / 3 / 0 s of SIGTERM grace: the 3rd member is SIGKILLed ~0 s after its SIGTERM. Pre-round (868d87c4) every member waited `time.time() + wait_secs` = 15 s.
- `rotate.py:11584` the settle reserve reaches only the first budget-exhausting member; `:11706-11708` records a fully SIGKILLed belam-cap chain as `reaped: False`.
- `test_rotate_term_grace.py:202-222` asserts `all(gone_after)` for TERM-immune members, so it cannot require the per-member grace it names.

## Testable claim
Each member of a reap chain gets `min(term_grace_s, remaining chain budget)` with the chain budget sized so that a member that HONOURS SIGTERM within term_grace_s is never SIGKILLed (e.g. chain_deadline_s scales with the member count, or the bound applies only to TERM-immune members); a SIGKILLed chain is recorded as reaped: True with the kill named; a committed fixture-only test puts a TERM-honouring member THIRD in a 3-member chain and fails on the 6c403aeb4b bytes.

## Falsifier
1. The new test is RED on 6c403aeb4b and GREEN on the fix (fixtures only: no real pane, unit, or seat; never run from a post's pane without env -u TMUX -u TMUX_PANE).
2. `git grep -n 'max(time.time(), chain_deadline - settle)' -- extensions/agi/bin/rotate.py` = 0.
