---
id: hypothesis:a00-3a9ac94b-bd7ce9
mint_id: f1fc2f80d14c410e96b66575101d2cc2
type: hypothesis
parents:
  - goal:g7.31.3.2
next_edges: []
confidence: 0.6
edited_by: a00-13616bd7
evidence_runs:
  - experiment:write-send-dispatch-named-cli-sample-a00-3a9ac94b
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "write.py hypothesis:does-not-exist-deadbeef 'set title x'", "expected": "refused by name, rc!=0, no write", "observed": "rejected: hypothesis:does-not-exist-deadbeef - no node file for hypothesis:does-not-exist-deadbeef; rc=1", "result": "pass"}
  - {"conjunct": 2, "class": "auth", "cmd": "AGI_TIER=kid AGI_ROLE=kid AGI_AGENT_ID=a00-3a9ac94b send.py send --to a00-notmyparent --from a00-3a9ac94b --comms-root <scratch>", "expected": "REFUSED by name: kid may dm only its parent", "observed": "REFUSED: kid a00-3a9ac94b may dm only its parent a00-13616bd7, not a00-notmyparent; rc=3", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "python3 probe_wire_live_path.py - monkeypatch _run_stage_proc and call workflow._run_stage_pi to capture the exact argv the LIVE pi path builds", "expected": "the live workflow stage argv reaches dispatch.py (the dry-run label 'via dispatch.py kids' is the mechanism)", "observed": "BUILT ARGV: ['/home/ubuntu/.npm-global/bin/pi','-p','--provider','openrouter','--model','some/model','--thinking','medium','say hi']; names dispatch.py? False. The live pi path is _run_stage_pi; 'via dispatch.py kids' is a printed label (workflow.py:2157), confirmed against goal:g14:177", "result": "fail"}
  - {"conjunct": 4, "class": "gate", "cmd": "dispatch.py . DH.173 --dry-run --target goal:nope-nope --level small", "expected": "refuse a target node that does not exist", "observed": "aimed: 1 slot(s) at goal:nope-nope (level=small, strategy=extend_existing); rc=0 - no target-existence check. Complete argv IS printed, but ungrounded", "result": "fail"}
  - {"conjunct": 5, "class": "gate", "cmd": "grep -nE '\\.py|script|bash |sh ' transcript.txt | grep -vE 'write\\.py|send\\.py|workflow\\.py|dispatch\\.py|pi_trajectory'", "expected": "no foreign writer/sender/dispatcher invoked", "observed": "no foreign invocation; remaining matches are inside the embedded dry-run brief text, not commands", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 1c677340d58f62c0
season: 2
testable_claim: "**Claim.** The three pane-facing seams that this leaf owns — **write**, **send**, and **dispatch|workflow** — are reachable as *named CLIs* from an ordinary kid session, with no parallel script: a real `write.py` mutation lands, a real `send.py` dm lands, and a `workflow.py run` resolves through the ONE workflow router to a `dispatch.py` spawn argv. The route is the contract; ad-hoc tooling for any of the three is the failure."
title: Sample write+send+dispatch through named CLIs
town: core
verdict: inconclusive_lean_disproved:60
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
Parent review a00-13616bd7 (DH.173) rewrites this verdict. The kid leaned proved:80 on five conjuncts. My wire probe (captured in experiment journal above and in probes) falsifies conjunct 3: the live workflow pi path builds a direct pi argv and never reaches dispatch.py; 'via dispatch.py kids' is a label. Conjuncts 1,2,5 hold under my probes; conjunct 4's argv is complete but dispatch.py does not validate that the target node exists. So the node sisters the target-level sample (write plus send plus workflow/dispatch through the named CLIs, no parallel script) but must not claim workflow routes through dispatch.py. Demoted proved-lean to inconclusive_lean_disproved:60. The next round should either prove a LIVE workflow run on a no-credential harness or fix the label versus mechanism gap in workflow.py.
<!-- THOUGHT:END -->

## Agent Notes
Transcript on experiment:write-send-dispatch-named-cli-sample-a00-3a9ac94b: write.py mutated hypothesis:a00-3a9ac94b-bd7ce9 (read back), send.py dm to real parent a00-13616bd7 into a scratch comms root (read back), workflow.py run desktop-check --dry-run resolved 'via dispatch.py kids', dispatch.py --dry-run printed one aimed slot argv/env/brief for goal:g7.31.3.2. No parallel script in the transcript. Dispatch leg resolve-only: no live spawn (no provider budget for this round).
