---
id: hypothesis:l3w4-masters-comms-and-escalation
mint_id: 4b6a45d3d5ed434ba79d3344e1e14c06
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-XI
scaffold_hash: 5807b3ecddccc756
season: 2
testable_claim: send.py's new `report --to ASKER --ref TS` verb, following a prior `send.py ask --to NAME` call that wrote a `[ask]`-tagged dm block from ASKER to a `config:seats` row NAME whose name ends `-master` at timestamp TS, appends a `[report ref=TS]`-tagged reply back to ASKER only when TS and ASKER exactly match that block's `ts` and `from` fields (raising SystemExit and writing nothing for any other ts/from pair, or when NAME is not a registered `-master` seat), and send.py's new `escalate --to owner` verb delivers a `[owner-decision]`-tagged dm to `liaison` only when the caller's environment sets `AGI_ROLE=parent` and `AGI_LADDER_TIER=3`, refusing otherwise, with none of `ask`, `report`, or `escalate` ever writing to the prime's inbox.
thought_session: belam-S1-L3-XI
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

BUILD IMPERATIVE (added by belam-S1-L3-IX; standing until `hypothesis:l3-brief-build-imperative-missing` lands it in `brief.py`'s kid template, after which this paragraph is redundant rather than wrong).

YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done. This brief is an instruction to BRING A STATE ABOUT, not a question about whether that state holds today. Measuring the present, confirming the defect and stopping is NOT a result here — it was measured six times in this loop, decisively at L3.34 where four independent parents returned four honest red-first baselines with zero lines of code between them. Diagnose, then FIX, then prove it with a test that is RED before your change and GREEN after. A fix you tried that turned out to be wrong or impossible, stated plainly with the measurement that shows why, is a real result. Silence about the code is not.

TWO STANDING PROHIBITIONS FOR EVERY WAVE-4 SEAT BRIEF: (1) do not write to `.agi/nodes/.geometry/seats.md` — the Sanctuary Master owns that registry, and a seat that installs its own row is the exact failure this separation exists to prevent (it happened twice at L3.36 and both rows were dropped). If your seat needs a row, STATE THE ROW YOU WANT IN YOUR NODE BODY as a request to her. (2) Do not start, populate or run any real seat: the owner's standing gate (HANDOFF.md §6 item 47, verbatim "once we verify that perpetual seats work well and fully let's just stop there for a bit before we start them running") means BUILD the mechanism, PROVE it live, then STOP.

HARNESS CONSTRAINT FOR THIS ROUND (Belam XI, 2026-09-08, operational — not part of the claim). The `.env` OpenRouter runtime key is at its cap, so `dispatch.py` refuses every pi spawn with `ERR: runtime key ... below the configured floor`. Spawn your kid on the subscription:

    python3 extensions/agi/bin/dispatch.py . L3.42 --target <this node> --level small --tier kid --harness claude-code

Measured this session: `--harness claude-code` on the PARENT invocation does NOT reach the kid — the parent's own dispatch call falls back to the ladder row's pi harness and is refused. Pass the flag explicitly. Do NOT raise the key limit or edit `.env`; that is the owner's decision and it is banked. Do NOT do the kid's work yourself because the spawn was refused — report `pending` and say so, as two parents correctly did earlier this session.

YOU HOLD A BRANCH. You were dispatched with `--branch`, so you are working in your own git worktree on your own `loop/...@s2` branch, cut from the spawner's tip. Commit your kid's work there — a `--branch` parent that lands nothing leaves `merge-up` merging an empty branch and reporting green, which is exactly the defect fixed at L3.40 and never yet exercised live. You are the live proof of that fix. Do not push, do not merge, do not touch `season/s2`; the director merges.

HARNESS CORRECTION — SUPERSEDES THE claude-code CONSTRAINT NOTE ABOVE (Belam XI, 2026-09-08). Owner instruction, verbatim: "Use openrouter" / "Subscription will get drained". The runtime key cap was raised to $15 (usage $5.02, headroom ~$9.98) and pi spawns resolve again. **Run on pi/OpenRouter, not on the subscription.** Your kid:

    python3 extensions/agi/bin/dispatch.py . L3.42 --target <this node> --level small --tier kid --harness pi

Ignore the earlier paragraph telling you to pass `--harness claude-code`; it was written while the key was at its cap and is no longer true. `dispatch.py` resolves the correct cheap OpenRouter slugs by itself (`~z-ai/glm-flash-latest` parent, `~deepseek/deepseek-v4-flash-latest` kid) — that path was never the leaky one.

DO NOT run `workflow.py run` on the pi harness in this round for any reason. The fail-closed model guard that makes it safe landed minutes ago and is not yet merged into your branch. A workflow run before that guard is what burned an entire monthly key cap on `anthropic/claude-sonnet-4.6` (`hypothesis:l3-workflow-model-crosses-harness-namespace`). Rounds are cheap; workflows currently are not.

The BRANCH paragraph above still applies in full: you hold a worktree, commit your kid's work to your own `loop/...@s2` branch, never push, never touch `season/s2`.
