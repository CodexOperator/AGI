---
id: hypothesis:a00-7d8a9cdd-ab5bd4
mint_id: 1c3a316fe6fa4b3a94648427661bbdea
type: hypothesis
parents:
  - goal:g17.14.2
next_edges: []
confidence: 0.95
edited_by: a00-7d8a9cdd
evidence_runs:
  - experiment:grok-bot-seam-gate-corrected
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - "P7 seam: grep grok in dispatch.py and the three shipped adapters (pi/claude_code/copilot_cli) = 0 hits; config.json may carry harnesses.grok-bot (goal:g17.14.2 owns that row)."
profile: balanced
role: kid
scaffold_hash: 4bb41e69ea5535de
season: 2
testable_claim: grep -Ein grok on dispatch.py = 0 hits; on the three shipped adapters = 0 hits; .agi/config.json intentionally declares harnesses.grok-bot (goal:g17.14.2 owns that row), so a grok hit there is the deliverable not a leak; a seam gate must never assert 0 grok hits in config.json while that row is present.
title: "Grok-bot seam gate: dispatch.py + adapters grok-free, config row is the deliverable"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-7d8a9cdd-ab5bd4

## Hypothesis

The grok-bot seam invariant is:

- `grep -Ein 'grok' extensions/agi/bin/dispatch.py` = **0 hits**, and
- the three shipped adapters (`pi_adapter.py`, `claude_code_adapter.py`,
  `copilot_cli_adapter.py`) = **0 hits**;
- `.agi/config.json` **INTENTIONALLY** declares `harnesses."grok-bot"` — the row
  `goal:g17.14.2` owns — so a grok hit there is the **deliverable, not a leak**.

A seam gate must never assert 0 grok hits in `config.json` while that row is
present.

## Replaces — the false P7 it corrects

This hypothesis corrects a false probe. The P7 entry in the `probes:` field of
`hypothesis:a00-bfd0d94a-d67716` (branch
`season2/loops/goal-g17.14.1-a00-597f6b8f`, not in this worktree) read:

> "P7 seam: grep grok in dispatch.py, config.json and the three shipped
> adapters = 0 hits."

That text was written before `goal:g17.14.2` landed, and it is false the moment
the config row exists. `.agi/config.json` **must** carry the hit: the row IS the
subgoal's deliverable. The seam worth guarding is *"dispatch.py never learns the
harness name"* — not *"config.json is grok-free"*.

## Falsifiers

1. Any `grok` hit in `dispatch.py` — the fourth-harness seam collapsed into
   shared code (`goal:g4.6`).
2. Any `grok` hit in a shipped adapter — a harness leaking into its peers.
3. A gate that asserts zero `grok` hits across `config.json` *and* keeps the
   row: it is self-contradictory and fails on the bytes it is supposed to
   bless (that is exactly the false P7 above).

## Not in scope / what this is NOT

- Not a claim that `grok-bot` is fully spawnable. This worktree has **no**
  `grok_bot_adapter.py` (that file is `goal:g17.14.1`'s deliverable, on a
  different branch), so `adapters.load("grok_bot")` fails here. The seam this
  node fixes is the *gate text*, not a missing adapter.
- Not a licence to edit `dispatch.py`, any adapter, or `config.json`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Corrective round DT.13 residue #3: the inherited P7 probe asserted a
`config.json` property that the very lane it belongs to must violate. The
invariant is restated so config's grok row is the expected value rather than a
failure, and the probe is scoped to the two places where a grok name would
truly be a leak. Recorded under `goal:g17.14.2` so the false version is
superseded in this chain. Also measured and stated plainly: the config row
resolves to adapter `grok_bot`, but `adapters.load` fails in this worktree
because `grok_bot_adapter.py` has not landed here — an honest boundary, not a
seam violation.
<!-- THOUGHT:END -->

## Agent Notes
Corrected the false P7 seam gate under goal:g17.14.2: probe now asserts 0 grok hits ONLY in dispatch.py and the three shipped adapters, and names config.json's harnesses.grok-bot row as the intentional deliverable. All conjuncts measured live (gate+wire classes, plus a negative control proving the grep is live); config bytes read read-only from landed ref 76d141786. New chain: hyp a00-7d8a9cdd-ab5bd4 -> exp grok-bot-seam-gate-corrected -> verdict grok-bot-seam-gate-supersedes-false-p7 (proved, 0.95).
