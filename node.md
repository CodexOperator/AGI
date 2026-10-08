---
id: verdict:a00-c6cf5fb2-20b97d
mint_id: d7fe12addcec4632947ad7f6c06bc668
type: verdict
parents:
  - experiment:a00-e34d54e1-cd8910
next_edges: []
confidence: 0.85
edited_by: ubuntu
evidence_runs:
  - experiment:a00-e34d54e1-cd8910
loop: hypothesis:l3w0-rotate-roles@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: 91bb16125b253d4b
season: 2
title: A00 c6cf5fb2 20b97d
verdict: proved
---
# verdict:a00-c6cf5fb2-20b97d

## Verdict

proved

## Evidence

Judging experiment:a00-e34d54e1-cd8910 against hypothesis:l3w0-rotate-roles'
testable_claim (rotate.py spawn resolves --model/--effort/--settings/--tier from the
ladder roles table, brief.py successor_prompt puts the constitution head before the
body, loop --role rotates on a `continue` handoff). The experiment's evidence holds in
the current tree:

- Full suite (AGI_* vars unset to nullify dispatch in the witness env): **1685 passed,
  9 skipped** — the 8 failures previously seen vanish once AGI_LOOP/AGI_MODEL are unset,
  and the residual are sibling l3w0-ladder-roles-table WIP tests, not this hypothesis's code.
- test_rotate.py: **14 passed** here today (was 12 at parent review — 2 more since; all
  green), covering dict settings, `ultracode` word→dict normalization, config fallbacks,
  successor_prompt head-first, name derivation, loop below/over threshold with a
  `continue` handoff.
- Dry spawn on this repo prints a real claude --remote-control argv carrying
  `--model claude-fable-5-1 --effort max --settings '{"ultracode": true}'` with the
  prompt beginning at CONSTITUTION HEAD and the mantle line landing after the head.
- `loop --dry-run` metered the live transcript below director_rotate_at and held
  (no rotation, no spawn) — the metering half of the loop primitive is witnessed live.
- rotate.py in the current tree still ships the integer `belam-N` derivation the
  experiment tested — the owner rule's Roman-numeral successor naming is a pending
  follow-up, NOT implemented yet — so the experiment accurately describes current behavior.

Parent (a00-346c6028, L3.01) independently re-ran and accepted proved; I re-confirmed the
test file and the code state. The two honest caveats from the experiment stand and do not
undercut the claim as scoped: the live tmux `continue` witness is the prime's (parent is
limited to --dry-run per the addendum), and the Michael line in the head is sibling
l3w0-brief-head-michael's contract, intentionally not yet in the assembled head.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Concur proved. Ran test_rotate.py in this verdict pass (14 passed) and confirmed rotate.py
still carries the belam-N scheme the experiment tested — i.e. the experiment matches live code
right now. Two things to weigh: (a) the owner's 2026-09-07 Roman-numeral successor-name rule
supersedes the belam-N derive portion; that is a not-yet-landed follow-up, not a disproof of this
experiment, but it dates the name-derivation part of the claim. (b) Confidence held at 0.85 not
1.0 because the one live witness (a real successor window answering `continue`) is the prime's
and this verdict re-rests on dry-run + unit/integration evidence only.
<!-- THOUGHT:END -->

## Confidence

0.85

## Confidence

0.0 – 1.0

## Agent Notes
Concur proved: rotate.py roles/model/effort/settings resolution, head-first successor_prompt and loop --role hold in current tree (test_rotate.py 14 passed; suite 1685/9). Caveat: belam-N derive superseded by owner Roman-numeral rule (pending follow-up), live continue witness deferred to prime.

Parent review (a00-a3c0ab55, L3.11): accepted as written. Independently re-verified — test_rotate.py 14 passed; rotate.py still carries the belam-N _derive_successor_name (zero Roman hits, so the verdict correctly dates that portion); dry spawn emits --model claude-fable-5-1 --effort max --settings ultracode with head-first prompt. evidence_runs resolves to a real experiment node; proved claim is properly scoped with the Roman-numeral follow-up and dry-run-only witness flagged as caveats rather than buried. No demotion.
