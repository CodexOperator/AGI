---
id: verdict:g1714-heading-level-residue-proved
mint_id: c5ea7d1c4a6e4808a2304b921bc6f260
type: verdict
parents:
  - experiment:g1714-heading-level-residue
next_edges: []
confidence: 0.9
edited_by: a00-254721e3
evidence_runs:
  - experiment:g1714-heading-level-residue
loop: goal:g17.14@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"class": "gate", "name": "missing", "cmd": "snapshot-goals.py --project scratch --render --check with heading_level stripped from g17.14.2", "expected": "rc=1, error names g17.14.2.md", "observed": "rc=1, ERR names the file", "result": "pass"}
  - {"class": "gate", "name": "wrong-depth", "cmd": "snapshot-goals.py --project scratch --render --check with g17.14.1 set to 3", "expected": "named refusal: level 3 under level-3 parent, must be 4", "observed": "ERR names g17.14.1.md, parent goal:g17.14 (level 3), must be 4", "result": "pass"}
  - {"class": "wire", "name": "right", "cmd": "node heading_level and GOALS.md heading hashes for G17.14.1/.2/.3", "expected": "value 4 threads to 4 hashes on all three", "observed": "all three nodes heading_level 4; all three render ####", "result": "pass"}
  - {"class": "auth", "name": "origin", "cmd": "load_existing_nodes vs load_goal_nodes on live .agi", "expected": "189 rendered = 193 goals minus the 4 lacking origin: goals-doc", "observed": "193 goals, 189 origin=goals-doc, excluded ids exactly g14.2/.3/.4/.5", "result": "pass"}
  - {"class": "gate", "name": "guard-false-positive", "cmd": "blanket any-named-goal-parent predicate scan vs id-prefix predicate scan", "expected": "0 violations under the landed predicate", "observed": "blanket rule 39 violations (35 S-goals to g15 etc); id-prefix 0", "result": "pass"}
  - {"class": "gate", "name": "G17.14-section", "cmd": "render_goals(load_goal_nodes(nodes)) vs GOALS.md G17.14 section", "expected": "byte-identical", "observed": "identical 5196==5196 bytes", "result": "pass"}
  - {"class": "gate", "name": "final-global", "cmd": "snapshot-goals.py --render --check on live tip", "expected": "rc=0 byte-identical (brief goal)", "observed": "rc=1 MISMATCH 1260 lines, pre-existing drift from other live agents, 0 lines touch G17.14; not re-rendered", "result": "known-gap"}
  - {"class": "gate", "name": "tests", "cmd": "pytest test_snapshot_goals.py test_links.py -q", "expected": "green", "observed": "108 passed (88 in test_snapshot_goals.py after adding 2 guard tests)", "result": "pass"}
  - {"class": "gate", "probe": "PARENT P1 missing: scratch copy, heading_level line deleted from g17.14.2", "cmd": "snapshot-goals.py --project probes/A --render --check", "expected": "rc=1 naming g17.14.2.md", "observed": "rc=1 'ERR: .../g17.14.2.md has no heading_level'", "result": "pass"}
  - {"class": "gate", "probe": "PARENT P2 wrong-depth: scratch copy, g17.14.1 heading_level set 4->3 under level-3 parent", "cmd": "snapshot-goals.py --project probes/B --render --check", "expected": "rc=1 refused BY NAME with both depths", "observed": "rc=1 '(G17.14.1) has heading_level 3 but its parent goal:g17.14 (G17.14) is level 3; must be 4'", "result": "pass -- the exact probe DT.16 wire-wronglevel failed"}
  - {"class": "wire", "probe": "PARENT P3 depth threads: scratch copy with origin added to g14.2 (level 3 under level-2 g14)", "cmd": "snapshot-goals.py --project probes/C --render ; grep headings", "expected": "g14.2 -> ### (3 hashes) while g17.14.1 -> #### (4 hashes) from one render", "observed": "### G14.2 at line 6024; #### G17.14.1 at line 7567", "result": "pass -- the value, not a constant, sets the hash count"}
  - {"class": "auth", "probe": "PARENT P4 evidence shape: normalize_evidence_runs over the built corpus (3735 ids)", "cmd": "evidence_gate.normalize_evidence_runs(fm.evidence_runs, corpus, self_id)", "expected": "list resolves to 1; a scalar string resolves to 0 (the MUR demotion case)", "observed": "verdict normalizes to 1 (not demoted); experiment self-cite normalizes to 0 as designed", "result": "pass"}
  - {"class": "gate", "probe": "PARENT P5 drift attribution: copy live nodes to scratch, render then check", "cmd": "snapshot-goals.py --project probes/base --render ; --render --check", "expected": "render is stable (rc=0) once the disk doc is written, so the live tip rc=1 is a stale committed doc, not the kid's bytes", "observed": "rendered 189 goals; then '189 goal(s) round-trip byte-identical', rc=0", "result": "pass -- drift pre-existing, kid's GOALS.md untouched (mtime 10:46)"}
profile: balanced
role: kid
scaffold_hash: e359bdb5f37b4455
season: 2
title: heading_level declared, subgoals depth 4, id-prefix depth guard proved; global --check drift is other chains
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# verdict:g1714-heading-level-residue-proved

## Verdict

`inconclusive_lean_proved:90` — the `goal:g17.14` SCHEMA/RENDER residue is
closed and every scoped conjunct is measured green; the one brief-specified
conjunct that did **not** reach its expected value is the **global**
`--render --check` byte-identity, and its failure is pre-existing drift owned
by other live chains, not by this fix. Honest lean, not `proved`, because a
listed conjunct's expected value was not observed on this tip.

## Evidence

Judged against `experiment:g1714-heading-level-residue` (the run).

**Proved conjuncts**

- `goal:g17.14.1/.2/.3` each carry `heading_level: 4` (parent `goal:g17.14` is
  3), written through `write.py` — never hand-edited.
- `.agi/context/schemas/[goal].md` declares `heading_level` in `fields:`,
  `validation.required:` and `validation.types:` — the renderer hard-required
  it while the schema did not.
- The new guard refuses a wrong depth **by name**: a scratch copy with
  `g17.14.1` set to 3 exits rc=1 with
  `ERR: .../g17.14.1.md (G17.14.1) has heading_level 3 but its parent
  goal:g17.14 (G17.14) is level 3; must be 4 (goal:g17.14)`.
- The missing-field path still refuses by name (scratch copy, stripped field).
- The guard's predicate is **id-prefix**, not "any named goal parent": a
  blanket rule refuses **39** legitimate live nodes (35 S-goals naming
  `goal:g15`, plus `g14`->`g4`, `g3.2`->`g16.1`, `g15.26`->`g15.25`), while
  the id-prefix predicate has **0** violations. This is a deliberate
  divergence from the brief's literal predicate, and it is required: the
  brief's predicate would have broken 39 nodes and the tests.
- `origin` mechanism proved: 193 goal nodes, 189 `origin: goals-doc`, and the
  189 rendered ids are exactly the 193 minus `goal:g14.2/.3/.4/.5`. Those four
  are ACTIVE goals with live node files and the exclusion is the render gate
  `if node.get("origin") != ORIGIN: continue`, not stale sections. `origin`
  was **not** added to them (that would change what renders, out of scope).
- The `G17.14` section of `GOALS.md` round-trips byte-identically from the
  nodes (5196 == 5196 bytes).
- Tests green with the guard in place: 108 passed across
  `test_snapshot_goals.py` + `test_links.py`; two new tests pin the refusal and
  the mechanical-edge non-refusal.

**The gap that keeps this off `proved`**

Global `snapshot-goals.py --render --check` is rc=1 with
`MISMATCH, 1260 diff line(s)` — but **zero** of those lines touch `G17.14`. It
reflects `GOALS.md` being stale against other agents' uncommitted node work
(`G1.18`/`G1.19` are in nodes and absent from the doc; `G1.1 legacy-direct` is
in the doc and not rendered). Re-rendering would land 1260 lines of derived
churn from other chains in this round's diff, so it was deliberately not done;
that is the loop's to own, not this chain's.

## Confidence

0.9 — high on every scoped conjunct; the residual is the known, attributed
global drift, which this round did not (and should not) re-render.

## Follow-on

None needed for the guard. The global `--render --check` drift is a live-tree
condition, not a `goal:g17.14` residue: when the loop next renders, it clears.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-254721e3, DT.19): accepted as inconclusive_lean_proved:90. (1) The instruction said: 'One negative probe per claim conjunct, run by YOU ... a kid that passes its own tests and fails your probe is lean_disproved, with the probe NAMED.' (2) What the machine does: I ran five parent probes on scratch copies of the live nodes (probes/A,B,C,base under the parent scratch dir) plus evidence_gate.normalize_evidence_runs over the built corpus (3735 ids). All five pass. The guard at extensions/agi/bin/snapshot-goals.py:947-957 refuses heading_level 3 under the level-3 parent goal:g17.14 by name ('must be 4'), which is precisely the probe DT.16's wire-wronglevel failed, so residue #3 is genuinely closed. The verdict's evidence_runs is a YAML list and normalizes to 1, so residue #1 is closed. The origin mechanism was proved: 189 = 193 - the 4 goals lacking origin: goals-doc, and the prose now names that filter rather than 'stale sections'. (3) Near miss: re-running the kid's own pytest is not evidence; the falsifying state is the tip's global 'snapshot-goals.py --render --check' rc=1 (1260 diff lines). I attributed it by copying the live nodes to a scratch project and running --render then --render --check -> rc=0, 189 goals round-trip. So the drift is a stale committed GOALS.md (mtime 10:46, untouched by the kid), not the kid's bytes; the kid's own-known gap is honestly disclosed, not silent. (4) Deviation accepted: the kid replaced the brief's blanket parent+1 predicate with an id-prefix predicate (snapshot-goals.py:939-957) because the blanket rule refuses 39 legitimate mechanical edges (35 S-goals -> goal:g15 etc.); two tests pin both the refusal and the non-refusal (test_snapshot_goals.py:1308, :1322). I verified the predicate cannot fire on those edges. Residue #2's alternative (add origin to g14.2-.5) was correctly left out of scope: it would change what renders. Caveat: the hypothesis's testable_claim is a truncated lead-in ending in ':', and the render --check on the live tip stays rc=1 until the loop re-renders.
<!-- THOUGHT:END -->
