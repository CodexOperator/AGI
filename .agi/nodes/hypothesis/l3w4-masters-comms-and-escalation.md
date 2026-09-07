---
id: hypothesis:l3w4-masters-comms-and-escalation
mint_id: 4b6a45d3d5ed434ba79d3344e1e14c06
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-V
scaffold_hash: 5807b3ecddccc756
season: 2
testable_claim: send.py's new `report --to ASKER --ref TS` verb, following a prior `send.py ask --to NAME` call that wrote a `[ask]`-tagged dm block from ASKER to a `config:seats` row NAME whose name ends `-master` at timestamp TS, appends a `[report ref=TS]`-tagged reply back to ASKER only when TS and ASKER exactly match that block's `ts` and `from` fields (raising SystemExit and writing nothing for any other ts/from pair, or when NAME is not a registered `-master` seat), and send.py's new `escalate --to owner` verb delivers a `[owner-decision]`-tagged dm to `liaison` only when the caller's environment sets `AGI_ROLE=parent` and `AGI_LADDER_TIER=3`, refusing otherwise, with none of `ask`, `report`, or `escalate` ever writing to the prime's inbox.
thought_session: L3.26
title: Reach the Masters, climb to the owner
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-masters-comms-and-escalation

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## CLAIM

`send.py` gains three verbs on `send_dm`/`send_room`, tagged like
`audience_prime`'s existing `[audience request]`. `ask --to NAME TEXT`: any
seat dms a Master — a `config:seats` row whose `name` ends `-master`,
checked via `spawn_gate.read_seat_registry` — tagged `[ask]`. `report --to
ASKER --ref TS TEXT`: a Master replies only inside that same dm, only when
an `[ask]` from `ASKER` sits at `TS` — "report back to the asker," enforced.
`escalate [--to owner] [--concern V] TEXT`: no `--to` posts `[concern:V]`
into room `tier3-quorum`; `--to owner` dms `liaison`, never `prime`, gated
to `AGI_ROLE=parent AGI_LADDER_TIER=3`.

## WHY

Owner (9): "director-kids get to talk to whichever Master they want, and
Masters report things back to the director that asked them"; "point it out
... if its more of an owner decision they can vote to reach out to owner
instead via liaison"; "balance preserving Belam's context with limiting
owner interaction requirements." Owner (4): "No directors get free comms to
Belam ... The quorum IS Belam to anyone else." Collapsed ladder: no free
director-Belam comms; expanded: director-kid lateral plus limited vertical
comms only — never bypassing the quorum.

## FILES

- extensions/agi/bin/send.py :: `send_dm`, `send_room`, `_detect_sender`,
  `audience_prime` (tag precedent)
- extensions/agi/bin/spawn_gate.py :: `read_seat_registry` L588 — fails
  open with no `seats.md`
- .agi/nodes/.geometry/seats.md :: `seats` rows (read-only)
- extensions/agi/tests/test_send.py

## DESIGN

`ask`: `to` must be a `-master` row in `read_seat_registry` (fail-closed on
a present-but-unknown name, suffix-only when the registry is absent), else
`ERR`; `send_dm(croot, me, to, f"[ask] {text}", sender)`.
`report`: needs an `<me>--<to>.md` block with `ts==ref`, `from==to`, text
starting `[ask]`, else `ERR: no [ask] from {to} at {ref}`; then dms back
tagged `[report ref={ref}]`.
`escalate`: `to=="owner"` needs `AGI_ROLE=="parent"` and
`AGI_LADDER_TIER=="3"`, else `ERR`; dms `liaison` tagged `[owner-decision]`.
Else posts `[concern:{V}]` into room `tier3-quorum` — director lateral and
vertical comms are `hierarchy_state`'s own axis (`l3w4-sanctuary-master`),
untouched here.

## TESTS

Red-first: `test_report_refuses_without_matching_ask_from_named_asker` — a
`report --to X --ref TS` with no `[ask]` from `X` at that `ts` (wrong `ts`,
or right `ts`/wrong `from`) raises `SystemExit`, writes nothing; a genuine
prior `ask` at that exact `ts`/`from` lets the identical call through.

## GATE

Fixture: a `-master` row plus `liaison`. `ask` writes `[ask]`; `report`
succeeds only against that block's `ts`/asker, else refuses. `escalate`
with no `--to` posts `[concern:vision]` into `tier3-quorum`; `--to owner`
refuses without the quorum env, else dms `liaison` — never `prime`. Suite
green; no node or link touched.

## NOT IN SCOPE

Vote/tally for an owner-type outcome, and `audience prime` itself (predicate
mine reuses) — `l3w4-quorum-reviews`. Liaison's owner-banking duty on
`[owner-decision]` — `l3w4-liaison-seat`. Master seat rows,
add/remove/expand/collapse, `hierarchy_state` —
`l3w4-sanctuary-master`/`l3w4-bug-master-seat`. Plan/Training Master seats —
`l3w4-plan-master`/`l3w4-training-master`.

## SOURCE

`.agi/context/l3-command-ladder-brief.md`, "Owner text 2026-09-07 ...
perpetual seats, the quorum as reviewer, the owner liaison" — owner verbatim
(9), and (4) for the comms-rule constraint.

OWNER QUOTE (12), 2026-09-07 ~17:55 UTC (verbatim in doc:l3-command-ladder-brief): the Training Master of quote (9) is renamed MASTER SENSEI — the one seat looking over the Masters themselves (the Sanctuary Master included); the Sanctuary Master owns seat assignments, model selection and seat-structure changes. Read "Training Master" in this body as Master Sensei; his brief is hypothesis:l3w4-master-sensei.
