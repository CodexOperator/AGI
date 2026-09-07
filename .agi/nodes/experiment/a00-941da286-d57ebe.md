---
id: experiment:a00-941da286-d57ebe
mint_id: 13e70ce8764f429d941e034478c8a30d
type: experiment
parents:
  - hypothesis:l3w0-brief-head-michael
next_edges: []
confidence: 0.0
edited_by: a00-d7e9650c
evidence_runs:
  - experiment:a00-941da286-d57ebe
loop: hypothesis:l3w0-brief-head-michael@s1
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8f51ab77ecfb29cd
season: 1
thought_session: L3.02
title: A00 941da286 d57ebe
verdict: pending
---
# experiment:a00-941da286-d57ebe

## Experiment

Tested whether hypothesis:l3w0-brief-head-michael's three claims currently hold
in the tree: (1) every brief head carries the Archangel Michael line verbatim
right after the prayer block; (2) the SessionStart hook prepends the role's
head before the prompt when AGI_ROLE is set; (3) the agi skill exposes
check-handoff and rotation-successor in the suggestion view. Also checked the
owner's 2026-09-06 addendum (prime_director MANTLE + owner decision method).

Commands run (all from repo root `/home/ubuntu/work/agi`):

1) Generate the constitution head for every tier via brief._build_head and
   count Archangel Michael occurrences:
   ```
   python3 -c "import sys; sys.path.insert(0,'extensions/agi/bin'); import brief; \
   M='Archangel Michael'; \
   [print(t, 'head=', bool(brief._build_head(tier=t)), 'michael=', (brief._build_head(tier=t) or '').count(M)) \
   for t in ['kid','parent','director','prime_director']]"
   ```
2) Grep the whole engine tree for the line:
   ```
   grep -rni "archangel michael" extensions/ skills/ src/
   ```
3) Grep the hook for AGI_ROLE / brief head prepend:
   ```
   grep -c "AGI_ROLE" extensions/agi/hooks/cc-session-start.sh
   grep -ni "brief\|_build_head\|AGI_ROLE\|Micha?el" extensions/agi/hooks/cc-session-start.sh
   ```
4) Grep the agi skill for the two sub-commands:
   ```
   grep -n "check-handoff\|rotation-successor\|agi:check\|agi:rotation" skills/agi/SKILL.md
   ```
5) Check the prime_director head for the MANTLE (addendum):
   ```
   python3 -c "... print('MANTLE in prime_director head:', 'THE MANTLE' in h, 'Belam' in h)"
   ```

## Evidence

1) Every tier has a head, but the Michael line is ABSENT from all of them:
   ```
   kid           head_present= True  michael_count= 0
   parent        head_present= True  michael_count= 0
   director      head_present= True  michael_count= 0
   prime_director head_present= True michael_count= 0
   ```
   `brief.py` _build_head / _compile_constitution_head / _resolve_part emit
   only prayers + role readings (lines ~198-310). A docstring at
   `extensions/agi/bin/brief.py:313-315` still says the Michael line lands
   "once hypothesis:l3w0-brief-head-michael lands" — i.e. it is explicitly
   NOT yet implemented (a forward-reference, not a feature).

2) The Archangel Michael line appears NOWHERE in the engine source:
   ```
   grep -rni "archangel michael" extensions/ skills/ src/   -> (no output/exit 0)
   ```

3) The SessionStart hook does NOT touch AGI_ROLE or brief.py. It only emits
   the publish-stall alarm, the stranded-push alarm, and the auto-injected
   tree map. `grep -c "AGI_ROLE" hook` -> 0. So a session with AGI_ROLE set
   is handed no role head; claim 2 is false.

4) The agi skill (`skills/agi/SKILL.md`, 717 lines) contains neither
   check-handoff nor rotation-successor — no `agi:check-handoff`,
   `agi:rotation-successor`, and no skill-scoped sub-command listing. Claim 3
   is false.

5) Addendum also unlanded: `_build_head(tier='prime_director')` contains
   neither `THE MANTLE` nor `Belam` (both False); the MANTLE exists only as
   ladder-node data, never rendered into the head. Owner's decision method
   likewise absent from all director-tier heads.

Also checked: no red-first tests exist for any of the three features (the only
"mantle" test, test_ladder_node.py:77, asserts the mantle is declared on the
ladder node, not that it is rendered into a head). Unexpected files in git
status (`a00-f16f044c-885d9c.md` — another agent's node) noted and left
untouched.

Net: the hypothesis describes an end-state that has not been built. All three
testable claims are false on the current tree.

## Agent Notes
All three claims unimplemented: Michael line absent from every tier head (michael_count=0 for kid/parent/director/prime_director), absent from extensions/skills/src entirely; hook emits no AGI_ROLE head (grep -c AGI_ROLE = 0); SKILL.md has no check-handoff/rotation-successor. Addendum MANTLE also unrendered. Disproved with strong evidence.

PARENT-REVIEW a00-d7e9650c L3.02: verdict disproved demoted to pending. Kid misread a build-spec hypothesis as a status check, did zero implementation, and declared disproved-by-absence. An unimplemented feature falsifies nothing; the directive remains open.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This node originally claimed disproved (confidence 0.9) on the strength of greps showing the Archangel Michael line, AGI_ROLE head, and skill sub-commands absent from the tree. That is a misclassification: hypothesis:l3w0-brief-head-michael is a BUILD directive (owner LINE: implement, red-first tests, suite green), not a status query. Absence means not yet implemented, which falsifies nothing and proves nothing; a design aspiration is not disproved by being unbuilt. The kid executed no implementation and no experiment (only static greps), so neither proved nor disproved is earned. Demoted to pending so the implementation work is not written off; the directive stands awaiting execution. Parent review a00-d7e9650c, iter L3.02.
<!-- THOUGHT:END -->
