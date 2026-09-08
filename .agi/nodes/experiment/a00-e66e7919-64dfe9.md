---
id: experiment:a00-e66e7919-64dfe9
mint_id: e8e7c511a0194831bc27cbd2556460ff
type: experiment
parents:
  - hypothesis:l3w4-hierarchy-one-source
next_edges: []
confidence: 0.8
edited_by: a00-d2e2165f
evidence_runs:
  - experiment:a00-e66e7919-64dfe9
loop: hypothesis:l3w4-hierarchy-one-source@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b0ed98bae43ccf69
season: 2
thought_session: SD.04
title: hierarchy.py one-source renderer/checker — built, 6/6 classes proven live
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-e66e7919-64dfe9

## Experiment

Built `extensions/agi/bin/hierarchy.py` — the one-source-of-truth renderer and
drift checker for the command structure (hypothesis:l3w4-hierarchy-one-source).
`render` emits THE chart from exactly two declarations: `config:seats`'s
`seats:` (instance registry) and `ladder:ladder`'s `roles:` (class defaults),
reading both through `graph_core.persistence.frontmatter` — the single reader
anything else (seat_status, viewport's hierarchy layer) is meant to read
through. `--check` implements all SIX measured drift classes:

1. **orphan_pin** — a `.agi/sessions/<name>.meter` with no seat row, excluding
   `a00-*` agent-id pins (ephemeral spawns are not seats).
2. **duplicate_transcript** — two rows whose pins resolve to the same transcript
   (one would rotate on the other's number).
3. **rotated_by no row** — a `rotated_by` naming a seat that has no row,
   whitelisting the standing roleclasses `quorum` and `prime`.
4. **director_kids over cap** — `role==director AND tier==1 AND owning_goal`
   non-empty above `caps.director_kids` (honours the owner's same-day
   correction that quorum rows own no goal, so they never count).
5. **unresolved** — a seat whose `(tier, role)` has no ladder row AND no
   seat-level model.
6. **body_table** — a hand-written pipe table in a node body whose cells
   disagree with that node's own frontmatter.

Suite: `extensions/agi/tests/test_hierarchy.py` — 9 red-first tests. One per
class asserting `--check` exits NONZERO on a seeded violation reproducing the
real 2026-09-08 shapes, plus a self-consistent clean seed asserting ZERO, plus
the agent-id-pin exemption. Full engine suite: **2187 passed, 1 skipped**.

## Evidence

On the LIVE tree `hierarchy.py --check` exits 1 with 10 real violations —
exactly the drift the hypothesis claims is live:

```
orphan_pin: belam-S1-L3-IX.meter has no seat row in config:seats
orphan_pin: belam-S1-L3-X.meter has no seat row in config:seats
orphan_pin: dir-g1.meter has no seat row in config:seats
orphan_pin: dir-g15.meter has no seat row in config:seats
orphan_pin: dir-g16.meter has no seat row in config:seats
orphan_pin: liaison.meter has no seat row in config:seats
body_table: roles prose row ['3','parent (advisors)','claude-code','claude-opus-5','max','ultracode'] ...
body_table: roles prose row ['1','director (perpetual)','claude-code','claude-fable-5-1','max','—'] ...
body_table: roles prose row ['1','liaison (owner)','claude-code','claude-sonnet-5','high','—'] ...
body_table: roles prose row ['0','director (per LT subgoal)','pi','~z-ai/glm-flash-latest','—','—'] ...
```

Classes 2/3/4/5 run CLEAN on the live tree (director-kids = 2 = cap; all
`rotated_by` targets resolve to seats or `quorum`/`prime`; every seat
`(tier,role)` has a ladder row; no two live rows share a transcript — the
alive/self-perpetuating 3066c544 collision the hypothesis measured has since
been resolved). Class 1 finds 6 genuine orphans — including `liaison.meter`,
a live-owner-ordered seat with NO row (writing a liaison row is forbidden for
this seat), and the stale `dir-gNN.meter` pins from the quorum rename. Class 6
finds the duplicate "Roles table (command ladder)" in `ladder.md`'s body,
whose display labels (`director (perpetual)`, `liaison (owner)`) differ from
the frontmatter `role` values — the exact prose-vs-declaration drift the
hypothesis says must be deleted.

NOT DONE (banked, the continuing fix): (a) delete the duplicate Roles/Tiers
tables from `ladder.md` body via write.py (would zero class 6); (b) reconcile
the 6 orphan pins, `liaison` needing a row only sanctuary-master may add;
(c) rewire `viewport.py --layer hierarchy` and `seat_status.py` to read
through hierarchy.py; (d) wire `--check` into `.geometry/commands.md` under
verify. Wiring was deliberately deferred: the live tree is NOT clean, so a
wired verify gate would bake a red check that blocks every parallel
`commands.py run` until the cleanups land — the wiring belongs with the
cleanup pass, not before it. Documented here as a deviation rather than folded
silently, per the constitution.

`render` output confirmed correct on the live tree: 12 seat rows and 8 ladder
class rows printed from the two frontmatter declarations only, plus the
precedence line (seat row → (tier,role) class → config.harnesses) and the
note that the word "role" is overloaded across the rotate.py spawn profile and
the dispatch ladder role.

## Agent Notes
Built and red-first tested extensions/agi/bin/hierarchy.py: render (one-source chart from config:seats + ladder:ladder) and --check with all 6 measured drift classes. 9 tests green, full suite 2187 passed. Live --check exits 1 with 10 real violations (6 orphan pins incl. liaison, 4 duplicate Roles-table rows) proving the drift is live. Cleanup (delete duplicate tables via write.py, reconcile pins, rewire viewport/seat_status, wire into commands.md) deliberately deferred to a continue pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SD.04 (a00-d2e2165f): artifact verified live — hierarchy.py and test_hierarchy.py exist, 9/9 tests pass, --check exits 1 with the exact 10 violations reported. Verdict kept at lean_proved:80: the build is real but the tree is not yet clean, so the hypothesis is evidenced in construction, not yet in settled state.
<!-- THOUGHT:END -->
