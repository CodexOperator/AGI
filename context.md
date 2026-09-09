# Code Context

## Files Retrieved
1. `/tmp/reader_diagram.txt` (lines 1-225) - owner directives for seats, masters, workflows, used to answer recall questions.

## Key Code
- N/A (analysis based on textual directives in `/tmp/reader_diagram.txt`).

## Architecture
Owner directives describe governance hierarchy: perpetual seats (prime, quorum, director-kids, liaison) with assigned models; Sanctuary structure (Sanctuary Master, Bug Master, Masters ladder); workflows controlled by Plan Master/Sensei; review and escalation rules; tooling such as agi-brief-drafting.js, agi-round-review.js, sensei.py, failures.py.

## Start Here
Open `/tmp/reader_diagram.txt` to reference all owner-settled instructions before modifying seat/workflow logic.

# Project Context

item18.Q1 The owner settled four perpetual seat tiers — "Belam (prime)", "3 advisors (quorum)", "one director-kid PER perpetual goal", and the "owner-liaison director-kid" — and locked their models: prime runs "Fable 5.1 max ultracode", quorum "Opus 5 max", director-kids "Opus 5 high", liaison "Sonnet 5 high", with pi parents/kids unchanged.

item18.Q2 Comms rule: "NO director reaches Belam EXCEPT through the quorum"; perpetual seats must use TTY/remote-control transport and "NOT `claude -p`" (bare piped mode forbidden).

item18.Q3 Done so far: "owner text recorded", "goal:g17 minted", drafting run relaunched 12:22 UTC with Sonnet/max (first died on limit, second stopped for model switch). Remaining work implied by sequencing beyond these steps.

item18.Q4 A round goes to audience when the vote is "1-1-1 OR a morals flag"; only 3-0 or 2-1 stands.

item18.Q5 The l3w4-drafter-seat (Sonnet or GLM flash) "summons the drafting workflow" so everyone needing a brief goes through it; switching workflow agents to opus/fable "MUST be a config update OR a single-run override" — never a code edit.

item20.Q1 Sanctuary Master = chief-of-staff director-kid who "rotates EVERY seat she oversees" (all director-kids, liaison, Bug Master) and gates all seat add/remove/hierarchy changes; she is "the ONLY seat rotated by the quorum" (condition).

item20.Q2 Forbidden: her mantle is "PENDING — owner prose, NEVER invent it".

item20.Q3 Bug Master is a reviewer seat "Opus xhigh" that "coordinates Sonnet-max minion seats" and is "called at EVERY review" (no skipping).

item20.Q4 Camber token rule: it is "NOT in .env"; the owner "PASTES it through the secure path" and you must "NEVER ask" — instead re-check `envfile.py` before opening g14.

item20.Q5 Landed: nodes "l3w4-sanctuary-master", "l3w4-bug-master-seat", "l3w4-sanctuary-theme", "l3w4-push-further-loops" minted via write.py; they are "queued AFTER registry + transport" per ordering condition.

item24.Q1 Owner settled that "brief drafting needs to happen through the Plan Master" and every workflow "has its own responsible Master in the Sanctuary under our SM": Plan Master owns agi-brief-drafting.js, Bug Master agi-round-review.js, Quality/Training Master handles audits, all under Sanctuary Master.

item24.Q2 Seat improvements: "standard-seat improvements: AUTOMATIC"; "Belam/advisor changes: need OWNER APPROVAL or FINALIZED DRAFTS". Morals/vision conflicts escalate director -> quorum -> Belam if needed.

item24.Q3 Current state: drafting run `wf_5091d1e6-af6` minted "l3w4-plan-master", "l3w4-masters-comms-and-escalation", "l3w4-seat-push-further", "l3w4-masters-rollover"; "l3w4-training-master NOT minted" (pending re-draft); bug-master/drafter notes still open.

item24.Q4 Plan Master "SUPERSEDES l3w4-drafter-seat's SEAT" (keeps mechanism); l3w4-training-master is to be re-drafted, later renamed per item27.

item24.Q5 Season rollovers run by "Bug + Quality/Training + Sanctuary Master (only these three)".

item27.Q1 Owner renamed Training/Trainer Master to "Master Sensei"; Sanctuary Master handles seat assignments/model selection/structure, while Master Sensei "tries to keep improving the Masters themselves, including Sanctuary Master" via fine-tuning and prompt updates.

item27.Q2 Sensei must talk to "the respective role and their direct supervisor" for every change, and for ephemeral roles talks only to that role's supervisor; Belam/advisor targets require `--owner-approved`, otherwise a draft plus DM to the liaison.

item27.Q3 Current state: minted "hypothesis:l3w4-master-sensei", "hypothesis:l3w4-agent-failure-ledger", and "hypothesis:l3w4-belam-predecessor-chain"; tools include `sensei.py apply` (writes note after role+supervisor reply) and `failures.py ledger|rates` creating the failure ledger payload.

item27.Q4 Supersession: "l3w4-training-master is re-drafted as l3w4-master-sensei".

item27.Q5 Sensei's main job is to "keep track of where agents fail" and eliminate causes, i.e., train Masters; mechanism: "l3w4-agent-failure-ledger" with failures.py ledger/rates storing eight failure categories keyed by sha256.
