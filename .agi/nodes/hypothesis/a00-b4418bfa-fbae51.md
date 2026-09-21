---
id: hypothesis:a00-b4418bfa-fbae51
mint_id: d0f2dc8ed01646e38ace72760e68c5bb
type: hypothesis
parents:
  - goal:g7.31.3.1
next_edges: []
confidence: 0.95
edited_by: a00-7477e928
evidence_runs:
  - experiment:a00-b4418bfa-five-routes-render
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "cd /data/work/agi/.agi/worktrees/a00-7477e928; PYTHONPATH=extensions/agi/bin python3 -c \"import brief; render kid/parent/director/prime_director with NO profile kwarg\"", "expected": "every full-profile tier carries brief._ROUTES_SEGMENT with all five contract names and all six engine seams under default profile resolution", "observed": "kid,parent,director,prime_director all segment=True, names_missing=[], seams_missing=[]; full kid brief 10081 chars", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "cd /data/work/agi/.agi/worktrees/a00-7477e928; PYTHONPATH=extensions/agi/bin python3 -c \"import brief; render kid with profile=survival\"", "expected": "the survival profile must refuse/exclude the segment it exists to be smaller than", "observed": "survival segment=False and heading absent, 4430 chars vs the full kid brief 10081", "result": "refused"}
  - {"conjunct": 3, "class": "wire", "cmd": "cd /data/work/agi/.agi/worktrees/a00-7477e928; git ls-tree -r --name-only 1baadf8c7", "expected": "the cited evidence run is carried by the round commit", "observed": "both .agi/nodes/experiment/a00-b4418bfa-five-routes-render.md and .agi/nodes/hypothesis/a00-b4418bfa-fbae51.md are in 1baadf8c7; basename carries the agent id", "result": "held"}
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT review of a00-b4418bfa (1baadf8c7), ACCEPTED, verdict proved -- the corrective kid the leaf needed after kid 1 lost its evidence node. WHAT THE INSTRUCTION SAID (goal:g7.31.3.1): "A cold seat brief / custom-instruction surface lists the five routes by the names in the goal:g7.31.3 table ... Grep/read proof on the brief artifact." WHAT THE MACHINE ACTUALLY DOES, on the committed bytes: brief.py carries _ROUTES_SEGMENT (brief.py:2038) and the _finish() hook appends it only when profile == "full" (brief.py:2093). I re-ran the render on the current bytes: kid, parent, director and prime_director each carry all five contract names and all six seams (full kid brief 10081 chars); the survival probe REFUSES it (segment absent, 4430 chars). The cited evidence node experiment:a00-b4418bfa-five-routes-render IS committed in 1baadf8c7 and its basename carries a00-b4418bfa, which closes the exact _round_scope_ok gap that made kid 1 untracked. THE NEAR MISS: a probe that passes an explicit profile="full" kwarg satisfies the words while the live default resolution could return another profile and drop the segment; this kid passed NO profile kwarg and printed effective_profile(default)=full, and my independent render reproduced it. The second near miss: appending unconditionally would also hit the survival profile, whose one job is to be smaller than the segment; the gate probe confirms survival omits it. NO DEVIATION to record; the kid touched neither dispatch.py nor rotate.py nor brief.py, and 0 broken links across 3849. NEXT: nothing left on this leaf -- the sample write+send+dispatch transcript is goal:g7.31.3.2.
note Parent probes for goal:g7.31.3.1: (1) wire/full tiers HELD -- five names + six seams in kid/parent/director/prime_director under default profile; (2) gate/survival REFUSED as intended (4430 vs 10081 chars); (3) wire/carry HELD -- evidence node committed in 1baadf8c7. Kid 1 (a00-13a360dc) demoted for its lost evidence node; kid 2 (a00-b4418bfa) accepted proved and supplies the committed evidence run.
<!-- THOUGHT:END -->
