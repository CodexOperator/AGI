---
id: experiment:a00-260a392b-040782
mint_id: c7dba102c55e4e229e70d752cd2375d3
type: experiment
parents:
  - hypothesis:l3w4-hierarchy-one-source
next_edges: []
confidence: 0.9
edited_by: a00-d2e2165f
evidence_runs:
  - experiment:a00-260a392b-040782
loop: hypothesis:l3w4-hierarchy-one-source@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9b9fcbb29082416d
season: 2
thought_session: SD.04
title: "body_patch verb built: live ladder.md deletion zeroes class 6, write_guard clean"
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-260a392b-040782

## Experiment

**Slice: the live delete-duplicates leg that four siblings had proven but never
landed on the tree.** e66e7919 built `hierarchy.py` (6/6 drift classes);
c057e969 verified the classes live; bc8c50a0 made the view derive;
d1d6ae46 proved on a `/tmp` mirror that deleting the duplicate "Roles table
(command ladder)" zeroes class-6 `body_table` — and flagged why it had to
stay a mirror: **no `write.py` verb could edit a graph node's body as a
sanctioned write.** `patch` targets the payload file behind a *build* node and
refuses a graph node (no `payload_ref`), so the live deletion was, for three
rounds, only possible by hand-editing the file — the standing
unsanctioned-write failure class (`write_guard` flags a byte change with no
write-log entry).

The live tree at the start: `hierarchy.py --check` = **10 violations** — 6
`orphan_pin` (sanctuary-master-only to fix) + **4 `body_table`** rows (`3 /
parent (advisors)`, `1 / director (perpetual)`, `1 / liaison (owner)`, `0 /
director (per LT subgoal)` — display labels disagreeing with frontmatter
`role` values).

**Built: `verb_body_patch` in `extensions/agi/bin/write.py`** — `body_patch
<path|->` applies the same fail-closed `apply_unified_diff` used by `patch`
to the node's CURRENT BODY and lands it through `node_writer.update_node`
(which carries the THOUGHT region across, stamps provenance, and logs the
sanction). It is standalone (refuses `note`/`thought` on the same submit line,
one body writer per write), reads stdin with the same contract as
`payload -`, and is wired into `VERBS`/`ARITY`/`empty`/dry-run.
**Red-first:** `test_body_patch.py` (4 tests) failed pre-change (`apply_verb`:
"no verb body_patch") and passes now.

**Applied the live deletion through the new verb:**
`write.py ladder:ladder 'body_patch -' --actor a00-260a392b --session SD.04
< /tmp/ladder_diff.txt` → `updated: ladder:ladder`. The duplicate 8-row pipe
table is gone, replaced by one line naming the single source
("The live chart is printed by ``hierarchy.py render`` … the duplicate body
table is gone, not re-derived").

## Evidence

After the deletion, `hierarchy.py --check` exits 1 with **6 violations, all
`orphan_pin` — zero `body_table`** (class 6 deleted live, exactly the
10 → 6 delta d1d6ae46 predicted from the mirror):

```
orphan_pin: belam-S1-L3-IX.meter has no seat row in config:seats
orphan_pin: belam-S1-L3-X.meter has no seat row in config:seats
orphan_pin: dir-g1.meter has no seat row in config:seats
orphan_pin: dir-g15.meter has no seat row in config:seats
orphan_pin: dir-g16.meter has no seat row in config:seats
orphan_pin: liaison.meter has no seat row in config:seats
```

The six remaining are the genuine orphan pins only sanctuary-master may fix
(writing a `liaison` row is forbidden for a kid). The renderer loses nothing:
`hierarchy.py render` still emits all 8 `(tier, role)` rows from the
frontmatter `roles:` (3 prime_director, 3 parent, 1 liaison, 1 director, kids)
plus all seat rows.

The verb resolves the contradiction that deferred the deletion:
`write_guard.py check` stays **clean (exit 0)** after the write — the deletion
is now a sanctioned write, so the hypothesis's own GATE
("write_guard.py check clean") holds *and* the duplicate is gone. Full engine
suite **2196 passed, 1 skipped** (the 4 new body_patch tests included);
`snapshot-goals.py --render --check` byte-identical (128 goals); `links.py`
0 broken. The `ladder.md` THOUGHT region survived the body rewrite.

Not done (outside this slice): the analogue `seats.md` "model-ownership" prose
paragraph is entangled with owner-verbatim Agent Notes, is NOT flagged by
`--check` (it is prose, not a pipe table), and was left untouched to avoid
destroying provenance; the six orphan pins remain; and `--check` stays
unwired into `.geometry/commands.md` because the gate would be red until a
sanctuary-master clears the orphan pins (a red wired gate blocks every
parallel `commands.py run`).

## Agent Notes
The missing `write.py` verb is built and used: `body_patch` lets a node-body
edit (e.g. the stale duplicate table) land as a sanctioned write through
`update_node` — THOUGHT carried, write_guard clean. The live ladder.md
deletion zeroed class-6 `body_table` 4→0 on the tree (10→6 total, the rest
sanctuary-master orphan pins), render unchanged, full suite 2196 passed / 1
skipped, snapshot clean, links 0 broken.

the delete-duplicates leg that four siblings proved but never landed: the missing write.py verb is body_patch (a graph-node body diff that lands through update_node as a sanctioned write). Built red-first (test_body_patch.py, 4 tests), then drove the live ladder.md deletion through it: class-6 body_table 4->0, render unchanged, write_guard clean, full suite 2196 passed/1 skipped, snapshot byte-identical, links 0 broken. The six remaining check violations are orphan pins only sanctuary-master may fix.

## Agent Notes
Built write.py body_patch verb (sanctioned graph-node body edit) and drove the live ladder.md duplicate-table deletion through it: class-6 body_table zeroed 4->0 on the live tree, render unchanged, write_guard clean, full suite 2196 passed/1 skipped, snapshot byte-identical, links 0 broken.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SD.04: strongest kid in the round — body_patch verb closes the sanctioned-write gap all three prior siblings deferred on, and the live ladder.md deletion is confirmed on the tree (--check 10→6, zero body_table). DEFECT FOUND: node body carries THREE duplicate Agent Notes sections — update_node appended notes twice; engine defect, not kid error. Verdict lean_proved:90 accepted; commands.md wiring deferral accepted (red gate would block parallel runs).
<!-- THOUGHT:END -->
