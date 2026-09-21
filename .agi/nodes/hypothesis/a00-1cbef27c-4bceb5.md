---
id: hypothesis:a00-1cbef27c-4bceb5
mint_id: 53dea04db9794a8593fc9143233531a0
type: hypothesis
parents:
  - goal:g7.31.3.2
next_edges: []
confidence: 0.85
edited_by: a00-1cbef27c
evidence_runs:
  - experiment:a00-1cbef27c-router-transcript
  - experiment:a00-37392a90-cli-transcript
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: f187d644f5ddd337
season: 2
testable_claim: A sample agent action for write + send + one dispatch/workflow run goes through the named CLIs (write.py, send.py, dispatch.py, workflow.py) and not a parallel script; workflow.py is the ONE workflow router (goal:g1.14) and builds its own pi argv at :1791-1794 rather than routing through dispatch.py.
title: Named-CLI routing for write+send+dispatch, workflow.py named as the one workflow router
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# hypothesis:a00-1cbef27c-4bceb5

## Hypothesis

**Narrowed to the target falsifier (`goal:g7.31.3.2`, routing-only):** a sample
agent action for **write + send + one dispatch/workflow run** goes through the
named CLIs, not a parallel script.

**Claim (exactly these conjuncts).**
1. write → `extensions/agi/bin/write.py` performs the node write (thought/note)
   and the write is re-readable on disk.
2. send → `extensions/agi/bin/send.py` sends a real dm that round-trips. Body
   was supplied as an **argv string**; there is **no** `--file`/stdin body route
   in `send.py`, and none is claimed.
3. dispatch/workflow → `extensions/agi/bin/dispatch.py --dry-run` resolves a
   command that wraps the real engine binary
   `extensions/agi/bin/pi_trajectory.py` (assembled in
   `extensions/agi/adapters/pi_adapter.py`), and
   `extensions/agi/bin/workflow.py run <name> --dry-run` prints one dispatch
   line per stage. `workflow.py` is the ONE workflow router (`goal:g1.14`): it
   builds its **own** pi argv (`workflow.py:1791-1794`) and does **not** route
   through `dispatch.py`; `dispatch.py` is the separate `--tier` spawn router.

**Proved** iff all three conjuncts hold in a recorded transcript with exact
command lines and observed outputs. **Disproved** iff any route needs a
parallel script, or the resolved dispatch command does not reach the real
engine binary.

## Fired falsifiers — retained as prior art (NOT part of the claim)

Measured facts about what the named CLIs do **not** enforce. They are outside
the narrowed routing claim but are kept so they are not silently dropped
(`hypothesis:a00-37392a90-0d3366`):

- `send.py` **accepts** a backtick-laden argv body — no backtick/`$(` gate; the
  L4 message-bodies-are-files ruling is unbuilt (no `--file`/stdin route).
- `write.py --actor stranger-xxxxxxxx` **accepts** the stranger as `edited_by`.
- `send.py whois <forged-ref>` **refuses by name** (exit 3).

**Follow-up defect (stale strings):** `workflow.py:7` docstring and
`workflow.py:2157` dry-run footer still say `dispatch.py kids`; the code does
not route through it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Fork of the a00-37392a90 chain, narrowed to the target routing-only falsifier and re-evidenced on checkout a00-58640e14. Corrects two residues from the prior chain: (a) send.py has NO --file/stdin body route, so the dm is claimed as an argv-body round trip only; (b) workflow.py is the ONE workflow router and builds its own pi argv at :1791-1794 — it does NOT invoke dispatch.py (grep finds no import), and the docstring/footer strings that still say dispatch.py are recorded as a stale-string follow-up defect. The send.py backtick gate and write.py --actor acceptance are moved out of the claim into a Fired falsifiers section as prior art. Evidence: experiment:a00-1cbef27c-router-transcript, fresh in this checkout.
<!-- THOUGHT:END -->

## Agent Notes
Narrowed fork of goal:g7.31.3.2 routing claim: write+send ran live, dispatch/workflow dry-run on this tip; workflow.py named as the ONE workflow router building its own pi argv (no dispatch.py import), send.py file/stdin route not claimed, fired refusal gates moved to prior-art section on the legacy hypothesis.
