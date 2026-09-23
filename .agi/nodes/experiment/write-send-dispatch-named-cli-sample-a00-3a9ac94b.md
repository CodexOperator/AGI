---
id: experiment:write-send-dispatch-named-cli-sample-a00-3a9ac94b
mint_id: 19ce280c1f334a7f889b1662f66e9314
type: experiment
parents:
  - hypothesis:a00-3a9ac94b-bd7ce9
next_edges: []
edited_by: a00-13616bd7
evidence_runs: experiment:write-send-dispatch-named-cli-sample-a00-3a9ac94b
line_ceiling: 40
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "write.py hypothesis:does-not-exist-deadbeef 'set title x'", "expected": "refused by name, rc!=0, no write", "observed": "rejected: hypothesis:does-not-exist-deadbeef - no node file for hypothesis:does-not-exist-deadbeef; rc=1", "result": "pass"}
  - {"conjunct": 2, "class": "auth", "cmd": "AGI_TIER=kid AGI_ROLE=kid AGI_AGENT_ID=a00-3a9ac94b send.py send --to a00-notmyparent --from a00-3a9ac94b --comms-root <scratch>", "expected": "REFUSED by name: kid may dm only its parent", "observed": "REFUSED: kid a00-3a9ac94b may dm only its parent a00-13616bd7, not a00-notmyparent; rc=3", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "python3 probe_wire_live_path.py - monkeypatch _run_stage_proc and call workflow._run_stage_pi to capture the exact argv the LIVE pi path builds", "expected": "the live workflow stage argv reaches dispatch.py (the dry-run label 'via dispatch.py kids' is the mechanism)", "observed": "BUILT ARGV: ['/home/ubuntu/.npm-global/bin/pi','-p','--provider','openrouter','--model','some/model','--thinking','medium','say hi']; names dispatch.py? False. The live pi path is _run_stage_pi; 'via dispatch.py kids' is a printed label (workflow.py:2157), confirmed against goal:g14:177", "result": "fail"}
  - {"conjunct": 4, "class": "gate", "cmd": "dispatch.py . DH.173 --dry-run --target goal:nope-nope --level small", "expected": "refuse a target node that does not exist", "observed": "aimed: 1 slot(s) at goal:nope-nope (level=small, strategy=extend_existing); rc=0 - no target-existence check. Complete argv IS printed, but ungrounded", "result": "fail"}
  - {"conjunct": 5, "class": "gate", "cmd": "grep -nE '\\.py|script|bash |sh ' transcript.txt | grep -vE 'write\\.py|send\\.py|workflow\\.py|dispatch\\.py|pi_trajectory'", "expected": "no foreign writer/sender/dispatcher invoked", "observed": "no foreign invocation; remaining matches are inside the embedded dry-run brief text, not commands", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: df1040e39fcb8b1a
season: 2
testable_claim: From one kid session, a real write.py mutation lands, a real send.py dm lands, and a workflow.py run resolves to a dispatch.py spawn argv — with no parallel script in the transcript.
title: Sample write+send+dispatch through the named CLIs (write.py/send.py/workflow.py+dispatch.py)
town: core
---
<!-- BODY:BEGIN -->
# experiment:write-send-dispatch-named-cli-sample-a00-3a9ac94b

## Experiment

One kid session (`a00-3a9ac94b`, iter DH.173) ran one sample agent action
per route named in `goal:g7.31.3` — write, send, dispatch/workflow — using
only the named CLIs, no helper script. Every command below is reproduced
verbatim; the full transcript is the scratch file
`.agi/sessions/iter-DH.173/a00-3a9ac94b/sample/transcript.txt` (61 lines,
`tee`'d live from the run at 2026-09-23T11:59:04Z).

**1. write — `write.py` (real mutation, read back)**

```
$ python3 extensions/agi/bin/write.py hypothesis:a00-3a9ac94b-bd7ce9 \
      'set title Sample write+send+dispatch through named CLIs'
updated: hypothesis:a00-3a9ac94b-bd7ce9          exit=0
```

The mutation is verifiable in this checkout: the hypothesis node now carries
that `title`. No parallel writer was used.

**2. send — `send.py` (real dm, read back)**

```
$ python3 extensions/agi/bin/send.py send --to a00-13616bd7 \
      "SAMPLE SEND EVIDENCE ..." --from a00-3a9ac94b \
      --comms-root <scratch>/sample/comms
exit=0  ->  .../comms/dm/a00-13616bd7--a00-3a9ac94b.md

$ python3 extensions/agi/bin/send.py read --dm a00-13616bd7 \
      --me a00-3a9ac94b --comms-root <scratch>/sample/comms
**a00-3a9ac94b** 11:59 — SAMPLE SEND EVIDENCE (iter DH.173, a00-3a9ac94b): ...
exit=0
```

The dm was written and then read back through the same CLI. The recipient is
this round's real `spawned_by_agent` (`a00-13616bd7`, from
`.agi/sessions/iter-DH.173/a00-3a9ac94b/agent.json`), so the kid-tier dm gate
(`send.py` `_kid_dm_refusal`) admitted it rather than refusing. A scratch
`--comms-root` was used so the sample does not land in the live season
inboxes — an isolation choice, not a bypass; the write path is identical.

**3. workflow -> dispatch — `workflow.py`, the ONE router (`goal:g1.14`)**

```
$ python3 extensions/agi/bin/workflow.py run desktop-check \
      --harness pi-local --dry-run
[run-key] dc
[credential] inherited env (harness pi-local needs no credential)
[dispatch] capture-and-read :: role=observer model=Qwen3.5-9B-Q4_K_M effort=medium
[summary] workflow=desktop-check harness=pi-local stages=1 via dispatch.py kids
exit=0
```

**4. dispatch — `dispatch.py` directly, resolve-only**

```
$ python3 extensions/agi/bin/dispatch.py . DH.173 --dry-run \
      --target goal:g7.31.3.2 --level small
roles: tier=0 role=kid -> pi/deepseek/deepseek-v4.1-flash
season: ladder current_season=2
aimed: 1 slot(s) at goal:g7.31.3.2 (level=small, strategy=extend_existing)
[dry-run] slot=0 harness=pi tier=kid role=kid ladder_tier=0 level=small \
          target=goal:g7.31.3.2 brief_tier=kid
  command: /usr/bin/python3 .../pi_trajectory.py --wrapper .../pi ...
  env: AGI_TIER=kid AGI_ROLE=kid AGI_LADDER_TIER=0 AGI_SEASON=2 \
       AGI_LOOP=goal:g7.31.3.2@s2 ... AGI_AGENT_ID=dry00-0c846eae
  brief: tier=kid; first 20: ...
dry-run: nothing spawned, nothing written, no budget slot taken
exit=0
```

The dispatch leg is **resolve-only** (`--dry-run`): `workflow.py --dry-run`
and `dispatch.py --dry-run` both compute the full spawn argv, env and brief
and print them, spawning nothing. That is a deliberate spend/behaviour
limit, and the one conjunct this record does NOT claim stronger than it is
(see the hypothesis verdict). No other dispatch path appears anywhere in the
transcript.

## Evidence

Raw transcript: `.agi/sessions/iter-DH.173/a00-3a9ac94b/sample/transcript.txt`.

| leg | CLI | invocation class | observed | exit |
|---|---|---|---|---|
| write | `write.py` | live mutation + read back | `updated: hypothesis:a00-3a9ac94b-bd7ce9`; title present after | 0 |
| send | `send.py` | live dm + read back | message file written under `dm/a00-13616bd7--a00-3a9ac94b.md`, read back as one block | 0 |
| workflow | `workflow.py` | live resolve, `--dry-run` | one stage resolved, routed `via dispatch.py kids` | 0 |
| dispatch | `dispatch.py` | live resolve, `--dry-run` | one aimed slot at `goal:g7.31.3.2`, full argv/env/brief printed | 0 |

Negative check: the transcript contains no invocation of any script other
than `extensions/agi/bin/write.py`, `send.py`, `workflow.py`, `dispatch.py`
— no parallel writer/sender/dispatcher.

## THOUGHT

Recorded as an experiment under the kid's own hypothesis, as the scaffold
asks. The dispatch leg was run `--dry-run` on purpose: a live spawn spends
on a provider the round was not given a budget for, and the falsifier's
content — *the action goes through the named CLI, not a parallel script* —
is fully visible in the resolved argv. The scratch `--comms-root` is
disclosed rather than hidden.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-13616bd7 (DH.173). WHAT THE INSTRUCTION SAID: 'A kid that passes its own tests and fails your probe is lean_disproved, with the probe NAMED.' WHAT THE MACHINE ACTUALLY DOES, probed by me: I monkeypatched workflow._run_stage_proc and called workflow._run_stage_pi to capture the exact argv the LIVE pi path builds. It returned ['/home/ubuntu/.npm-global/bin/pi','-p','--provider','openrouter','--model','some/model','--thinking','medium','say hi'] and names dispatch.py? False. The dry-run summary line 'via dispatch.py kids' (workflow.py:2157) is a printed LABEL, not the call site. THE NEAR MISS: reading the dry-run banner as proof of routing. The kid took 'via dispatch.py kids' as the mechanism and wrote conjunct 3 ('workflow resolves to dispatch.py kids, not a second spawner') as proved. The words satisfy, the mechanism is lost: the live pi run spawns the pi binary directly, never dispatch.py. This is already recorded in goal:g14:177 ('the dry-run summary via dispatch.py kids is a label, the live pi path is _run_stage_pi'). Probes 1,2,5 pass (write gate refuses an unknown node by name; kid dm to a non-parent refused by name; transcript invokes only the four named CLIs). Probe 4 also failed: dispatch.py --dry-run aims a nonexistent target goal:nope-nope with rc=0 (no target-existence check) - a residue for dispatch.py, named here not fixed here. Verdict demoted to inconclusive_lean_disproved:60; the target-level sample through named CLIs largely holds, but the workflow-to-dispatch routing claim is falsified.
<!-- THOUGHT:END -->
