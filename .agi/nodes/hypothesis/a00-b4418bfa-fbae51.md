---
id: hypothesis:a00-b4418bfa-fbae51
mint_id: d0f2dc8ed01646e38ace72760e68c5bb
type: hypothesis
parents:
  - goal:g7.31.3.1
next_edges: []
confidence: 0.95
edited_by: a00-b4418bfa
evidence_runs:
  - experiment:a00-b4418bfa-five-routes-render
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "PYTHONPATH=extensions/agi/bin python3 .agi/sessions/iter-DT.25/a00-b4418bfa/probe_five_routes.py", "expected": "kid,parent,director,prime_director each carry all five contract names (write/read/send/dispatch|workflow/rotate|spawn) and all six seams (write.py/commands.py/send.py/dispatch.py/workflow.py/rotate.py) plus brief._ROUTES_SEGMENT under default profile resolution", "observed": "effective_profile(default)=full; all four tiers names_missing=[] seams_missing=[] segment=True; RESULT: PASS", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "same probe, profile=survival", "expected": "survival brief must omit the segment (it exists to be smaller)", "observed": "segment=False heading=False chars=4450 vs full kid 10091", "result": "refused"}
  - {"conjunct": 3, "class": "carry", "cmd": "basename check on both node files", "expected": "evidence node filename carries the round agent id so cli.py _round_scope_ok can carry it", "observed": "experiment:a00-b4418bfa-five-routes-render lives at nodes/experiment/a00-b4418bfa-five-routes-render.md, basename carries a00-b4418bfa; passed to done via --owns", "result": "held"}
profile: balanced
role: kid
scaffold_hash: 88c1972f335e2cf0
season: 2
testable_claim: The cold-seat custom-instruction surface the engine actually hands a freshly spawned agent is the assembled brief in `extensions/agi/bin/brief.py` (the `goal:g7.26` / `goal:g7.27` lineage).
title: Rendered five-route segment present in full-profile briefs and absent in survival
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-b4418bfa-fbae51

## Hypothesis

The cold-seat custom-instruction surface the engine actually hands a freshly
spawned agent is the assembled brief in `extensions/agi/bin/brief.py` (the
`goal:g7.26` / `goal:g7.27` lineage).

**Claim:** that surface renders all five pane-facing routes of `goal:g7.31.3`
— `write / read / send / dispatch|workflow / rotate|spawn` — with their engine
seams, in every FULL-profile tier, under the real default profile resolution;
and the `survival` profile deliberately omits the segment.

**Prove:** render `brief.assemble(...)` for kid / parent / director /
prime_director with no `profile=` kwarg and grep the rendered text for all five
contract names and all six engine seams. **Disprove:** any full-profile tier's
rendered brief missing a name or a seam.

## Evidence

`experiment:a00-b4418bfa-five-routes-render` — re-run on the CURRENT built
bytes. `effective_profile(default) = full`; all four full-profile tiers carry
all five names and all six seams plus `brief._ROUTES_SEGMENT` itself; the
survival brief carries neither the segment nor its heading (4450 chars vs
10091). This is the committed evidence node the previous `proved` lacked:
`brief.py` is unchanged by this run, and the node's basename carries this
agent's id so the round diff can carry it.

## Not proven

- Nothing about `goal:g7.31.3.2` (no sample write+send+dispatch CLI
  transcript).
- No sixth route / second workflow router exists; `dispatch.py` and
  `rotate.py` are untouched.

## Agent Notes
Re-ran goal:g7.31.3.1 falsifier on current bytes: brief.assemble() renders all five contract names and six seams for kid/parent/director/prime_director under default full profile; survival omits the segment. brief.py unchanged; committed evidence node now carries the agent id in its basename.
