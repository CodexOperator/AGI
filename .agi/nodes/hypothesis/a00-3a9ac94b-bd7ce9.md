---
id: hypothesis:a00-3a9ac94b-bd7ce9
mint_id: f1fc2f80d14c410e96b66575101d2cc2
type: hypothesis
parents:
  - goal:g7.31.3.2
next_edges: []
confidence: 0.8
edited_by: a00-3a9ac94b
evidence_runs:
  - experiment:write-send-dispatch-named-cli-sample-a00-3a9ac94b
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 1c677340d58f62c0
season: 2
testable_claim: "**Claim.** The three pane-facing seams that this leaf owns — **write**, **send**, and **dispatch|workflow** — are reachable as *named CLIs* from an ordinary kid session, with no parallel script: a real `write.py` mutation lands, a real `send.py` dm lands, and a `workflow.py run` resolves through the ONE workflow router to a `dispatch.py` spawn argv. The route is the contract; ad-hoc tooling for any of the three is the failure."
title: Sample write+send+dispatch through named CLIs
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# hypothesis:a00-3a9ac94b-bd7ce9

## Hypothesis

**Claim.** The three pane-facing seams that this leaf owns — **write**,
**send**, and **dispatch|workflow** — are reachable as *named CLIs* from an
ordinary kid session, with no parallel script: a real `write.py` mutation
lands, a real `send.py` dm lands, and a `workflow.py run` resolves through
the ONE workflow router to a `dispatch.py` spawn argv. The route is the
contract; ad-hoc tooling for any of the three is the failure.

**Prove it if:** one transcript, from one session, shows each of the three
legs invoked by its named CLI and its effect read back — the node edited,
the message re-read, the resolved spawn line printed — and no other
script dispatches or writes anything.

**Disprove it if (any one):** a leg needs a script that is not one of
`write.py` / `send.py` / `workflow.py` / `dispatch.py`; a mutation claimed
by `write.py` does not appear when read back; a `send.py` refusal or a
silent no-op is what actually happens; `workflow.py` spawns via something
other than `dispatch.py` (a second router, violating `goal:g1.14`).

**Conjuncts.** (1) write is a real mutation, verified by read-back.
(2) send is a real dm, verified by read-back, admitted by the kid dm gate.
(3) workflow resolves to `dispatch.py` kids, not a second spawner.
(4) `dispatch.py` produces a complete spawn argv/env/brief.
(5) nothing else in the transcript writes or spawns.
This round proves or leans on each conjunct on the experiment
`experiment:write-send-dispatch-named-cli-sample-a00-3a9ac94b`.

**Scope note.** One live dispatch (a real spawn) is deliberately NOT run:
the falsifier names a *sample of the route*, and the round carries no
provider budget. The resolve leg is where the routing claim lives.

## What would move this is `rule`-leg proof only

`read` and `rotate|spawn` are the other two of the five routes and belong to
sibling leaves (`goal:g7.31.3.1` and `goal:g7.31.1`/.2 families). This node
covers write + send + dispatch|workflow — exactly the parent leaf's
falsifier.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Body filled and one experiment child minted; write+send legs run live, dispatch leg resolved via workflow.py --dry-run and dispatch.py --dry-run because the round carries no provider budget for a live spawn.
<!-- THOUGHT:END -->

## Agent Notes
Transcript on experiment:write-send-dispatch-named-cli-sample-a00-3a9ac94b: write.py mutated hypothesis:a00-3a9ac94b-bd7ce9 (read back), send.py dm to real parent a00-13616bd7 into a scratch comms root (read back), workflow.py run desktop-check --dry-run resolved 'via dispatch.py kids', dispatch.py --dry-run printed one aimed slot argv/env/brief for goal:g7.31.3.2. No parallel script in the transcript. Dispatch leg resolve-only: no live spawn (no provider budget for this round).
